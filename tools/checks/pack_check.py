"""Checks the packwiz mod list against the pack's rules (see openspec mod-selection and pack-build)."""
import argparse
import json
import sys
import tomllib
import zipfile
from pathlib import Path

# CurseForge project IDs of mods that compete with a Servus mod or were left out on purpose.
EXCLUDED_PROJECTS = {
    223794: "Applied Energistics 2",
    243076: "Refined Storage",
    246640: "Mystical Agriculture",
    377897: "Productive Bees",
    638351: "Replication",
    64578: "Ender IO",
    1030830: "Oritech",
    223852: "Storage Drawers",
    321117: "Traveler's Backpack",
    263420: "Xaero's Minimap",
    317780: "Xaero's World Map",
    64760: "SecurityCraft",
}
# Mods excluded by metafile slug, for mods without a known CurseForge ID.
EXCLUDED_SLUGS = {"iris": "Iris", "iris-shaders": "Iris", "irisshaders": "Iris"}

REQUIRED_SLUGS = [
    "servus-foundation", "servus-shuttles", "servus-alchemy", "modonomicon",
    "powah-rearchitected", "iron-jetpacks", "re-avaritia", "just-dire-things", "cobblegen-galore",
    "ftb-quests-forge", "ftb-xmod-compat", "kubejs", "crafting-on-a-stick",
]

CLIENT_ONLY_SLUGS = [
    "sodium", "immediatelyfast", "mouse-tweaks", "controlling", "searchables",
    "better-advancements", "enchantment-descriptions",
]

EXAMPLE_EXPORT = "Servus-0.1.0.zip"


def load_metafiles(mods_dir: Path) -> dict[str, dict]:
    return {p.name.removesuffix(".pw.toml"): tomllib.loads(p.read_text(encoding="utf-8"))
            for p in sorted(mods_dir.glob("*.pw.toml"))}


def project_id(meta: dict) -> int | None:
    return meta.get("update", {}).get("curseforge", {}).get("project-id")


def example_project_ids(root: Path) -> set[int]:
    zip_path = root / EXAMPLE_EXPORT
    if not zip_path.exists():
        return set()
    with zipfile.ZipFile(zip_path) as z:
        return {f["projectID"] for f in json.load(z.open("manifest.json"))["files"]}


def check(metas: dict[str, dict], public: bool = False, example_ids: set[int] = frozenset()) -> list[str]:
    errors = []
    ids = {project_id(m): slug for slug, m in metas.items() if project_id(m) is not None}
    for pid, name in EXCLUDED_PROJECTS.items():
        if pid in ids:
            errors.append(f"excluded mod {name} is in the pack ({ids[pid]})")
    for slug, name in EXCLUDED_SLUGS.items():
        if slug in metas:
            errors.append(f"excluded mod {name} is in the pack ({slug})")
    for slug in REQUIRED_SLUGS:
        if slug not in metas:
            errors.append(f"required mod {slug} is missing")
    for pid in sorted(example_ids - ids.keys()):
        errors.append(f"mod from {EXAMPLE_EXPORT} is missing (CurseForge project {pid})")
    for slug in CLIENT_ONLY_SLUGS:
        if slug in metas and metas[slug].get("side") != "client":
            errors.append(f"{slug} must be side = \"client\", is {metas[slug].get('side')!r}")
    if public:
        for slug, m in metas.items():
            if project_id(m) is None:
                errors.append(f"{slug} is not sourced from CurseForge; switch it to CurseForge before a public build")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--public", action="store_true")
    parser.add_argument("--list-url-mods", action="store_true", help="print the filenames of mods not sourced from CurseForge")
    args = parser.parse_args(argv)
    if args.list_url_mods:
        for meta in load_metafiles(args.root / "mods").values():
            if project_id(meta) is None:
                print(meta["filename"])
        return 0
    errors =check(load_metafiles(args.root / "mods"), args.public, example_project_ids(args.root))
    for e in errors:
        print(f"pack check: {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
