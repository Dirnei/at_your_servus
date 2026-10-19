"""Generates config/ftbquests/quests/ (FTB Quests 26.1.2.9, JSON5 format, see FORMAT.md) from the TOML sources in quests/.
Output is plain JSON with sorted keys, which FTB Quests reads as JSON5; reruns are byte-identical."""
import argparse
import json
import shutil
import sys
from pathlib import Path

from tools.questgen.model import Chapter, Quest, QuestSourceError, load_sources, stable_id

GROUPS = {"main": ("The Lechnerhof", "minecraft:oak_door"), "side": ("Side Chapters", "minecraft:compass")}

DATA = {
    "version": 13,
    "default_reward_team": False,
    "default_consume_items": False,
    "default_autoclaim_rewards": "disabled",
    "default_quest_shape": "circle",
    "default_quest_disable_jei": False,
    "drop_loot_crates": False,
    "emergency_items_cooldown": 300,
    "grid_scale": 0.5,
    "pause_game": False,
    "lock_message": "",
    "progression_mode": "linear",
    "detection_delay": 20,
    "show_lock_icons": True,
    "drop_book_on_death": False,
    "hide_excluded_quests": False,
    "fallback_locale": "en_us",
    "verify_on_load": False,
    "disable_gui": False,
}


def _json(value) -> str:
    return json.dumps(value, indent="\t", sort_keys=True, ensure_ascii=False) + "\n"


def _stack(item: str, components: dict | None = None) -> dict:
    stack = {"id": item, "count": 1}
    if components:
        stack["components"] = components
    return stack


def _filename(slug: str) -> str:
    return slug.replace("-", "_")


def _task(quest: Quest, index: int, task: dict) -> dict:
    out = {"id": stable_id(quest.chapter, quest.slug, "task", str(index)), "type": task["type"]}
    if task["type"] == "item":
        out["item"] = _stack(task["item"], task.get("components"))
        if task.get("count", 1) != 1:
            out["count"] = task["count"]
        if task.get("components"):
            out["match_components"] = "fuzzy"
    elif task["type"] == "advancement":
        out["advancement"] = task["advancement"]
        out["criterion"] = task.get("criterion", "")
    elif task["type"] != "checkmark":
        raise QuestSourceError(f"{quest.chapter}:{quest.slug}: unsupported task type {task['type']}")
    return out


def _reward(quest: Quest, index: int, reward: dict) -> dict:
    out = {"id": stable_id(quest.chapter, quest.slug, "reward", str(index)), "type": reward["type"]}
    if reward["type"] == "item":
        out["item"] = _stack(reward["item"])
        if reward.get("count", 1) != 1:
            out["count"] = reward["count"]
    elif reward["type"] == "xp":
        out["xp"] = reward["amount"]
    else:
        raise QuestSourceError(f"{quest.chapter}:{quest.slug}: unsupported reward type {reward['type']}")
    return out


def _quest(quest: Quest, ids: dict[tuple[str, str], str]) -> dict:
    out = {"id": quest.id, "x": float(quest.x), "y": float(quest.y),
           "tasks": [_task(quest, i, t) for i, t in enumerate(quest.tasks)],
           "rewards": [_reward(quest, i, r) for i, r in enumerate(quest.rewards)]}
    if quest.deps:
        out["dependencies"] = [ids[d] for d in quest.dep_keys()]
    if quest.icon:
        out["icon"] = _stack(quest.icon)
    if quest.shape:
        out["shape"] = quest.shape
    if quest.size:
        out["size"] = float(quest.size)
    if quest.optional:
        out["optional"] = True
    return out


def _lines(text: str) -> list[str]:
    return text.strip("\n").split("\n")


def build(chapters: list[Chapter]) -> dict[str, str]:
    """Returns the files to write, relative path -> content."""
    ids = {(c.slug, q.slug): q.id for c in chapters for q in c.quests}
    all_ids = [c.id for c in chapters] + list(ids.values()) + [stable_id("group", g) for g in GROUPS]
    if len(set(all_ids)) != len(all_ids):
        raise QuestSourceError("two quest objects got the same ID; rename a slug")
    files = {"data.json5": _json(DATA)}
    groups = [g for g in GROUPS if any(c.group == g for c in chapters)]
    files["chapter_groups.json5"] = _json({"chapter_groups": [
        {"id": stable_id("group", g), "icon": _stack(GROUPS[g][1])} for g in groups]})
    group_lang = {f"chapter_group.{stable_id('group', g)}.title": GROUPS[g][0] for g in groups}
    chapter_lang = {}
    for index, c in enumerate(sorted(chapters, key=lambda c: (c.group, c.order))):
        name = _filename(c.slug)
        chapter = {"id": c.id, "group": stable_id("group", c.group), "order_index": c.order, "filename": name,
                   "quests": [_quest(q, ids) for q in c.quests]}
        if c.icon:
            chapter["icon"] = _stack(c.icon)
        files[f"chapters/{name}.json5"] = _json(chapter)
        chapter_lang[f"chapter.{c.id}.title"] = c.title
        if c.subtitle:
            chapter_lang[f"chapter.{c.id}.chapter_subtitle"] = [c.subtitle]
        lang = {}
        for q in c.quests:
            lang[f"quest.{q.id}.title"] = q.title
            if q.subtitle:
                lang[f"quest.{q.id}.quest_subtitle"] = q.subtitle
            if q.description:
                lang[f"quest.{q.id}.quest_desc"] = _lines(q.description)
        files[f"lang/en_us/chapters/{name}.json5"] = _json(lang)
    files["lang/en_us/chapter.json5"] = _json(chapter_lang)
    files["lang/en_us/chapter_group.json5"] = _json(group_lang)
    return files


def write(files: dict[str, str], out: Path) -> None:
    if out.exists():
        shutil.rmtree(out)
    for rel, content in files.items():
        path = out / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8"))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quests", type=Path, default=Path("quests"))
    parser.add_argument("--out", type=Path, default=Path("config/ftbquests/quests"))
    args = parser.parse_args(argv)
    try:
        write(build(load_sources(args.quests)), args.out)
    except QuestSourceError as e:
        print(f"quest generator: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
