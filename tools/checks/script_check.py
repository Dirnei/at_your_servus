"""Checks that every item ID quoted in the KubeJS scripts exists in the pack (openspec progression-gates)."""
import argparse
import re
import sys
from pathlib import Path

from tools.checks.item_ids import known_items

# 'namespace:path' string literals; tags ('#c:...') and recipe IDs we create ('servus:...') are not items.
_LITERAL = re.compile(r"""['"]([a-z0-9_.-]+:[a-z0-9_/.-]+)['"]""")
NOT_ITEMS = {"servus", "ironjetpacks:jetpack_id"}
_NON_ITEM_TYPES = {"avaritia:infinity_catalyst"}


def item_refs(text: str) -> list[str]:
    refs = []
    for m in _LITERAL.finditer(text):
        value = m[1]
        start = m.start()
        if text[start - 1:start] == "#" or text[start + 1:start + 2] == "#":
            continue
        if value.split(":")[0] in NOT_ITEMS or value in NOT_ITEMS or value in _NON_ITEM_TYPES:
            continue
        if re.search(r"(id|type|group)\s*:\s*$", text[max(0, start - 12):start]):
            continue
        refs.append(value)
    return refs


def check(scripts: dict[str, str], items: set[str]) -> list[str]:
    return [f"{name}: unknown item {ref}" for name, text in sorted(scripts.items())
            for ref in item_refs(text) if ref not in items]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--kubejs", type=Path, default=Path("kubejs"))
    parser.add_argument("--mods", type=Path, default=Path("build/server/mods"))
    args = parser.parse_args(argv)
    scripts = {p.relative_to(args.kubejs).as_posix(): p.read_text(encoding="utf-8") for p in sorted(args.kubejs.rglob("*.js"))}
    errors = check(scripts, known_items(args.mods))
    for e in errors:
        print(f"script check: {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
