"""Checks the quest sources against the quest-line rules: known items, task counts, English titles, side chapters never gate the main line."""
import argparse
import re
import sys
import tomllib
from pathlib import Path

from tools.checks.item_ids import known_items
from tools.questgen.model import Chapter, QuestSourceError, load_sources

MAX_COUNT = 16
# Materials players gather in bulk; anything else asked for more than 16 times is reported.
_BULK = re.compile(r":(.*_)?(ingot|nugget|dust|gem|planks|log|cobblestone|cobbled_deepslate|stone|sand|gravel|dirt|glass|coal|"
                   r"redstone|quartz|crystal|shard|salt|sulfur|ash|quicksilver|raw_[a-z_]+|[a-z_]+_ore)$")
# Items no quest may give as a reward: the Sealed Flask is a Rubedo product and would skip the Great Work.
DENIED_REWARDS = {"servus_alchemy:sealed_flask"}


def bulk_items(quests_dir: Path) -> set[str]:
    path = quests_dir / "bulk.toml"
    return set(tomllib.loads(path.read_text(encoding="utf-8")).get("items", [])) if path.exists() else set()


def _item_refs(chapter: Chapter):
    if chapter.icon:
        yield None, chapter.icon
    for q in chapter.quests:
        if q.icon:
            yield q, q.icon
        for entry in q.tasks + q.rewards:
            if entry.get("type") == "item":
                yield q, entry["item"]


def check(chapters: list[Chapter], items: set[str], bulk: set[str]) -> list[str]:
    errors = []
    group_of = {c.slug: c.group for c in chapters}
    for c in chapters:
        if not c.title:
            errors.append(f"{c.slug}: chapter has no English title")
        for q, item in _item_refs(c):
            if item not in items:
                where = f"{c.slug}:{q.slug}" if q else c.slug
                errors.append(f"{where}: unknown item {item}")
        for q in c.quests:
            where = f"{c.slug}:{q.slug}"
            if not q.title:
                errors.append(f"{where}: quest has no English title")
            if not q.tasks:
                errors.append(f"{where}: quest has no task")
            for r in q.rewards:
                if r.get("type") == "item" and r["item"] in DENIED_REWARDS:
                    errors.append(f"{where}: {r['item']} must never be a reward")
            for t in q.tasks:
                if t.get("type") == "item" and t.get("count", 1) > MAX_COUNT \
                        and t["item"] not in bulk and not _BULK.search(t["item"]):
                    errors.append(f"{where}: asks for {t['count']} {t['item']}, more than {MAX_COUNT} of a non-bulk item")
            if c.group == "main":
                for dep_chapter, dep_quest in q.dep_keys():
                    if group_of.get(dep_chapter) == "side":
                        errors.append(f"{where}: main quest depends on side quest {dep_chapter}:{dep_quest}")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quests", type=Path, default=Path("quests"))
    parser.add_argument("--mods", type=Path, default=Path("build/server/mods"))
    args = parser.parse_args(argv)
    try:
        chapters = load_sources(args.quests)
    except QuestSourceError as e:
        print(f"quest check: {e}", file=sys.stderr)
        return 1
    errors = check(chapters, known_items(args.mods), bulk_items(args.quests))
    for e in errors:
        print(f"quest check: {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
