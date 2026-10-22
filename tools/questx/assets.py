"""Icons and English names for quest items, read from the Minecraft client jar and the server pack's mod jars.

Item definition -> plain model -> parent chain with merged textures -> a flat texture, a cube (top and two sides),
a flat particle texture, or nothing (placeholder)."""
import hashlib
import json
import tomllib
import urllib.request
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

MANIFEST = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
FLAT_PARENTS = {"minecraft:item/generated", "minecraft:builtin/generated"}
CUBE = "minecraft:block/cube"


class AssetError(Exception):
    pass


def minecraft_version(pack_toml: Path) -> str:
    return tomllib.loads(pack_toml.read_text(encoding="utf-8"))["versions"]["minecraft"]


def _fetch(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=120) as response:
        return response.read()


def client_jar(version: str, cache_dir: Path, fetch=_fetch) -> Path:
    """The client jar for `version`, downloaded from Mojang once and checked against its SHA-1."""
    path = cache_dir / f"client-{version}.jar"
    if path.exists():
        return path
    manifest = json.loads(fetch(MANIFEST))
    entry = next((v for v in manifest["versions"] if v["id"] == version), None)
    if entry is None:
        raise AssetError(f"Minecraft {version} is not in Mojang's version manifest")
    client = json.loads(fetch(entry["url"]))["downloads"]["client"]
    data = fetch(client["url"])
    if hashlib.sha1(data).hexdigest() != client["sha1"]:
        raise AssetError(f"client jar for {version}: SHA-1 does not match the version manifest")
    cache_dir.mkdir(parents=True, exist_ok=True)
    part = path.with_suffix(".part")
    part.write_bytes(data)
    part.replace(path)
    return path


def _location(ref: str) -> tuple[str, str]:
    ns, _, path = ref.rpartition(":")
    return ns or "minecraft", path


def _full(ref: str) -> str:
    return "%s:%s" % _location(ref)


@dataclass
class Icon:
    kind: str  # flat, cube, none
    textures: list[str] = field(default_factory=list)  # flat: [texture]; cube: [top, left, right]


def _plain_model(node: dict | None) -> str | None:
    """The model a GUI icon would use, picked from an item definition's model node.
    Mod types (servus_foundation:wood, avaritia:halo, neoforge:trimmed_armor, ...) are followed through model, base or base_model."""
    if not isinstance(node, dict):
        return None
    kind = node.get("type", "").removeprefix("minecraft:")
    if kind == "condition":
        return _plain_model(node.get("on_false")) or _plain_model(node.get("on_true"))
    if kind == "select":
        gui = [c for c in node.get("cases", []) if "gui" in json.dumps(c.get("when"))]
        branches = [c.get("model") for c in gui] + [node.get("fallback")] + [c.get("model") for c in node.get("cases", [])]
        return next((m for m in map(_plain_model, branches) if m), None)
    if kind == "range_dispatch":
        branches = [node.get("fallback")] + [e.get("model") for e in node.get("entries", [])]
        return next((m for m in map(_plain_model, branches) if m), None)
    if kind == "composite":
        return next((m for m in map(_plain_model, node.get("models", [])) if m), None)
    for key in ("model", "base", "base_model"):
        value = node.get(key)
        found = value if isinstance(value, str) else _plain_model(value)
        if found:
            return found
    return None


class Assets:
    """Every assets/ file of the given jars; a later jar wins, language files are merged."""

    def __init__(self, jars: list[Path]):
        self._where: dict[str, zipfile.ZipFile] = {}
        self._lang: dict[str, str] = {}
        for jar in jars:
            z = zipfile.ZipFile(jar)
            for name in z.namelist():
                if not name.startswith("assets/"):
                    continue
                self._where[name] = z
                if name.endswith("/lang/en_us.json"):
                    try:
                        self._lang.update(json.loads(z.read(name)))
                    except ValueError:
                        pass

    def read(self, path: str) -> bytes | None:
        z = self._where.get(path)
        return z.read(path) if z else None

    def _json(self, path: str) -> dict | None:
        data = self.read(path)
        try:
            return json.loads(data) if data else None
        except ValueError:
            return None

    def name(self, item: str) -> str:
        ns, path = _location(item)
        key = f"{ns}.{path.replace('/', '.')}"
        return self._lang.get(f"item.{key}") or self._lang.get(f"block.{key}") or item

    def texture_path(self, texture: str) -> str:
        ns, path = _location(texture)
        return f"assets/{ns}/textures/{path}.png"

    def icon(self, item: str) -> Icon:
        ns, path = _location(item)
        definition = self._json(f"assets/{ns}/items/{path}.json")
        ref = _plain_model(definition.get("model")) if definition else None
        textures, chain, elements_from = {}, [], None
        while ref and len(chain) < 32:
            ref = _full(ref)
            chain.append(ref)
            mns, mpath = _location(ref)
            model = self._json(f"assets/{mns}/models/{mpath}.json") or {}
            for key, value in model.get("textures", {}).items():
                # A texture can also be an object: {"sprite": "...", "force_translucent": true}.
                textures.setdefault(key, value.get("sprite") if isinstance(value, dict) else value)
            if elements_from is None and "elements" in model:
                elements_from = ref
            ref = model.get("parent")

        def texture(*names):
            for name in names:
                value, hops = textures.get(name), 0
                while value and value.startswith("#") and hops < 16:
                    value, hops = textures.get(value[1:]), hops + 1
                if value and self.read(self.texture_path(value)):
                    return _full(value)
            return None

        if FLAT_PARENTS & set(chain) and elements_from is None and texture("layer0"):
            return Icon("flat", [texture("layer0")])
        if elements_from == CUBE:
            faces = [texture("up"), texture("north"), texture("east")]
            if all(faces):
                return Icon("cube", faces)
        if texture("particle"):
            return Icon("flat", [texture("particle")])
        return Icon("none")

    def export(self, icon: Icon, out_dir: Path) -> list[str]:
        """Copies the icon's textures below out_dir/icons/ and returns their paths relative to out_dir."""
        paths = []
        for texture in icon.textures:
            ns, path = _location(texture)
            rel = f"icons/{ns}/{path}.png"
            target = out_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(self.read(self.texture_path(texture)))
            paths.append(rel)
        return paths
