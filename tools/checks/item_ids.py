"""Known item IDs of the pack: vanilla's registry report plus every item definition (assets/<ns>/items/<id>.json) in the server pack's jars.
Client-only mods add no items, so the server pack covers the pack."""
import re
import zipfile
from pathlib import Path

VANILLA = Path(__file__).with_name("vanilla_items.txt")
_ITEM_DEFINITION = re.compile(r"^assets/([a-z0-9_.-]+)/items/([a-z0-9_/.-]+)\.json$")


def items_in_jar(jar: Path) -> set[str]:
    with zipfile.ZipFile(jar) as z:
        return {f"{m[1]}:{m[2]}" for m in map(_ITEM_DEFINITION.match, z.namelist()) if m}


def known_items(mods_dir: Path) -> set[str]:
    ids = set(VANILLA.read_text(encoding="utf-8").split())
    for jar in sorted(mods_dir.glob("*.jar")):
        ids |= items_in_jar(jar)
    return ids
