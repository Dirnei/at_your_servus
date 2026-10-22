import hashlib
import json
import zipfile

import pytest

from tools.questx import assets
from tools.questx.assets import AssetError, Assets, Icon

PNG = b"\x89PNG fake"


def jar(path, files):
    with zipfile.ZipFile(path, "w") as z:
        for name, content in files.items():
            z.writestr(name, content if isinstance(content, (bytes, str)) else json.dumps(content))
    return path


def item(model):
    return {"model": model}


def plain(ref):
    return {"type": "minecraft:model", "model": ref}


VANILLA = {
    "assets/minecraft/models/item/generated.json": {"parent": "builtin/generated"},
    "assets/minecraft/models/item/handheld.json": {"parent": "item/generated"},
    "assets/minecraft/models/block/cube.json": {"elements": [{"from": [0, 0, 0], "to": [16, 16, 16]}]},
    "assets/minecraft/models/block/cube_all.json": {"parent": "block/cube", "textures": {
        "particle": "#all", "up": "#all", "north": "#all", "east": "#all"}},
    "assets/minecraft/models/block/slab.json": {"elements": [{"from": [0, 0, 0], "to": [16, 8, 16]}]},
    "assets/minecraft/textures/item/bread.png": PNG,
    "assets/minecraft/textures/block/stone.png": PNG,
    "assets/minecraft/lang/en_us.json": {"item.minecraft.bread": "Bread", "block.minecraft.stone": "Stone"},
}


@pytest.fixture
def pack(tmp_path):
    client = jar(tmp_path / "client.jar", VANILLA | {
        "assets/minecraft/items/bread.json": item(plain("minecraft:item/bread")),
        "assets/minecraft/models/item/bread.json": {"parent": "minecraft:item/generated", "textures": {"layer0": "minecraft:item/bread"}},
        "assets/minecraft/items/stone.json": item(plain("minecraft:block/stone")),
        "assets/minecraft/models/block/stone.json": {"parent": "block/cube_all", "textures": {"all": "block/stone"}},
        "assets/minecraft/items/stone_slab.json": item(plain("minecraft:block/stone_slab")),
        "assets/minecraft/models/block/stone_slab.json": {"parent": "block/slab", "textures": {"particle": "block/stone"}},
        "assets/minecraft/items/chest.json": item({"type": "minecraft:select", "property": "minecraft:local_time",
                                                   "cases": [{"when": "12-24", "model": {"type": "minecraft:special", "base": "item/chest_xmas"}}],
                                                   "fallback": {"type": "minecraft:special", "base": "minecraft:item/chest",
                                                                "model": {"type": "minecraft:chest"}}}),
        "assets/minecraft/models/item/chest.json": {"textures": {"particle": "block/stone"}},
    })
    mod = jar(tmp_path / "mod.jar", {
        "assets/servus_shuttles/items/rail.json": item({"type": "servus_foundation:wood", "model": "servus_shuttles:item/rail"}),
        "assets/servus_shuttles/models/item/rail.json": {"parent": "minecraft:item/handheld", "textures": {"layer0": "minecraft:item/bread"}},
        "assets/servus_shuttles/items/ghost.json": item({"type": "servus_shuttles:shuttle", "model": "servus_shuttles:item/ghost"}),
        "assets/servus_shuttles/items/tool.json": item({"type": "minecraft:condition", "property": "minecraft:using_item",
                                                        "on_true": plain("minecraft:block/stone"), "on_false": plain("minecraft:item/bread")}),
        "assets/servus_shuttles/items/glass.json": item(plain("servus_shuttles:item/glass")),
        "assets/servus_shuttles/models/item/glass.json": {"parent": "minecraft:item/generated", "textures": {
            "layer0": {"sprite": "minecraft:item/bread", "force_translucent": True}}},
        "assets/servus_shuttles/lang/en_us.json": {"item.servus_shuttles.rail": "Warehouse Rail"},
    })
    return Assets([client, mod])


def test_flat_item(pack):
    assert pack.icon("minecraft:bread") == Icon("flat", ["minecraft:item/bread"])


def test_mod_definition_type_and_handheld_parent(pack):
    assert pack.icon("servus_shuttles:rail") == Icon("flat", ["minecraft:item/bread"])


def test_texture_given_as_sprite_object(pack):
    assert pack.icon("servus_shuttles:glass") == Icon("flat", ["minecraft:item/bread"])


def test_condition_takes_the_default_branch(pack):
    assert pack.icon("servus_shuttles:tool").kind == "flat"


def test_full_block_is_a_cube_with_resolved_variables(pack):
    assert pack.icon("minecraft:stone") == Icon("cube", ["minecraft:block/stone"] * 3)


def test_other_shape_falls_back_to_particle(pack):
    assert pack.icon("minecraft:stone_slab") == Icon("flat", ["minecraft:block/stone"])


def test_special_renderer_uses_the_fallback_base_model(pack):
    assert pack.icon("minecraft:chest") == Icon("flat", ["minecraft:block/stone"])


def test_missing_model_or_definition_is_a_placeholder(pack):
    assert pack.icon("servus_shuttles:ghost") == Icon("none")
    assert pack.icon("minecraft:nothing") == Icon("none")


def test_names_from_merged_lang_files(pack):
    assert pack.name("minecraft:bread") == "Bread"
    assert pack.name("minecraft:stone") == "Stone"
    assert pack.name("servus_shuttles:rail") == "Warehouse Rail"
    assert pack.name("servus_shuttles:ghost") == "servus_shuttles:ghost"


def test_export_copies_textures(pack, tmp_path):
    out = tmp_path / "out"
    assert pack.export(pack.icon("minecraft:stone"), out) == ["icons/minecraft/block/stone.png"] * 3
    assert (out / "icons/minecraft/block/stone.png").read_bytes() == PNG


def test_later_jar_wins(tmp_path):
    a = jar(tmp_path / "a.jar", {"assets/x/textures/t.png": b"a"})
    b = jar(tmp_path / "b.jar", {"assets/x/textures/t.png": b"b"})
    assert Assets([a, b]).read("assets/x/textures/t.png") == b"b"


def fake_mojang(client_bytes, sha1=None):
    calls = []
    version = {"downloads": {"client": {"url": "client-url", "sha1": sha1 or hashlib.sha1(client_bytes).hexdigest()}}}
    responses = {assets.MANIFEST: json.dumps({"versions": [{"id": "26.1.2", "url": "version-url"}]}).encode(),
                 "version-url": json.dumps(version).encode(), "client-url": client_bytes}

    def fetch(url):
        calls.append(url)
        return responses[url]
    return fetch, calls


def test_client_jar_downloads_once(tmp_path):
    fetch, calls = fake_mojang(b"jar")
    path = assets.client_jar("26.1.2", tmp_path, fetch)
    assert path.read_bytes() == b"jar" and len(calls) == 3
    assert assets.client_jar("26.1.2", tmp_path, fetch) == path and len(calls) == 3


def test_client_jar_hash_mismatch_leaves_nothing(tmp_path):
    fetch, _ = fake_mojang(b"jar", sha1="0" * 40)
    with pytest.raises(AssetError):
        assets.client_jar("26.1.2", tmp_path, fetch)
    assert list(tmp_path.iterdir()) == []


def test_minecraft_version_from_pack_toml(tmp_path):
    (tmp_path / "pack.toml").write_text('[versions]\nminecraft = "26.1.2"\n')
    assert assets.minecraft_version(tmp_path / "pack.toml") == "26.1.2"
