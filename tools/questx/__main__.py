"""Builds the quest explorer: a static page of the quest line with icons and findings, opened from disk without Minecraft.
Needs the server pack's jars (tools/build.ps1); downloads the Minecraft client jar once into build/minecraft/."""
import argparse
import sys
from datetime import datetime
from pathlib import Path

from tools.questgen.model import QuestSourceError, load_sources
from tools.questx import page
from tools.questx.assets import AssetError, Assets, client_jar, minecraft_version
from tools.questx.findings import find


def build(quests_dir: Path, mods_dir: Path, out_dir: Path, client: Path) -> tuple[Path, list, list[str]]:
    chapters = load_sources(quests_dir)
    findings = find(chapters)
    assets = Assets([client] + sorted(mods_dir.glob("*.jar")))
    items, placeholders = {}, []
    for item in sorted(page.used_items(chapters)):
        icon = assets.icon(item)
        if icon.kind == "none":
            placeholders.append(item)
        items[item] = {"name": assets.name(item), "kind": icon.kind, "textures": assets.export(icon, out_dir)}
    built = datetime.now().strftime("%Y-%m-%d %H:%M")
    return page.write(out_dir, page.page_data(chapters, items, findings, built)), findings, placeholders


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quests", type=Path, default=Path("quests"))
    parser.add_argument("--mods", type=Path, default=Path("build/server/mods"))
    parser.add_argument("--out", type=Path, default=Path("build/quest-explorer"))
    parser.add_argument("--pack", type=Path, default=Path("pack.toml"))
    args = parser.parse_args(argv)
    if not args.mods.is_dir():
        print(f"quest explorer: {args.mods} does not exist; build the server pack first (tools/build.ps1)", file=sys.stderr)
        return 1
    try:
        client = client_jar(minecraft_version(args.pack), Path("build/minecraft"))
        index, findings, placeholders = build(args.quests, args.mods, args.out, client)
    except (QuestSourceError, AssetError, OSError) as e:
        print(f"quest explorer: {e}", file=sys.stderr)
        return 1
    for f in findings:
        print(f.line())
    if not findings:
        print("no findings")
    if placeholders:
        print("no icon: " + ", ".join(placeholders))
    print(f"wrote {index}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
