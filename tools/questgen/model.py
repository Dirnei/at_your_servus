"""Loads the quest sources (quests/chapters/*.toml = main group, quests/side/*.toml = side group).

A chapter file looks like:

    [chapter]
    title = "The Old Works"
    subtitle = "..."              # optional
    icon = "servus_foundation:utility_duct"

    [[quest]]
    slug = "utility-duct"
    title = "..."
    subtitle = "..."              # optional
    description = "..."           # optional, may span lines
    icon = "..."                  # optional, defaults to the first item task
    x = 0.0
    y = 0.0
    deps = ["first-letter", "arrival:first-letter"]   # same chapter, or "chapter:quest"
    optional = false              # optional
    shape = "gear"                # optional
    size = 1.5                    # optional
    tasks = [{ type = "item", item = "servus_foundation:utility_duct", count = 4 },
             { type = "checkmark" },
             { type = "advancement", advancement = "minecraft:story/mine_stone" }]
    rewards = [{ type = "item", item = "minecraft:bread", count = 8 }, { type = "xp", amount = 50 }]

The file name is "<NN>-<slug>.toml"; NN orders the chapters, slug identifies the chapter.
"""
import hashlib
import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

GROUPS = {"main": "chapters", "side": "side"}
_FILE = re.compile(r"^(\d\d)-([a-z0-9-]+)\.toml$")


class QuestSourceError(Exception):
    pass


def stable_id(*parts: str) -> str:
    return hashlib.sha256(("servus:" + ":".join(parts)).encode("utf-8")).hexdigest()[:16].upper()


@dataclass
class Quest:
    chapter: str
    slug: str
    title: str
    x: float
    y: float
    subtitle: str = ""
    description: str = ""
    icon: str = ""
    deps: list[str] = field(default_factory=list)
    optional: bool = False
    shape: str = ""
    size: float = 0.0
    tasks: list[dict] = field(default_factory=list)
    rewards: list[dict] = field(default_factory=list)

    @property
    def id(self) -> str:
        return stable_id(self.chapter, self.slug)

    def dep_keys(self) -> list[tuple[str, str]]:
        return [tuple(d.split(":", 1)) if ":" in d else (self.chapter, d) for d in self.deps]


@dataclass
class Chapter:
    group: str
    order: int
    slug: str
    title: str
    subtitle: str = ""
    icon: str = ""
    quests: list[Quest] = field(default_factory=list)

    @property
    def id(self) -> str:
        return stable_id(self.slug)


def load_chapter(path: Path, group: str) -> Chapter:
    m = _FILE.match(path.name)
    if not m:
        raise QuestSourceError(f"{path.name}: chapter files are named NN-slug.toml")
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    meta = data.get("chapter", {})
    chapter = Chapter(group=group, order=int(m[1]), slug=m[2], title=meta.get("title", ""),
                      subtitle=meta.get("subtitle", ""), icon=meta.get("icon", ""))
    for q in data.get("quest", []):
        unknown = set(q) - set(Quest.__dataclass_fields__) - {"chapter"}
        if unknown:
            raise QuestSourceError(f"{path.name}: quest {q.get('slug')}: unknown keys {sorted(unknown)}")
        chapter.quests.append(Quest(chapter=chapter.slug, **q))
    return chapter


def load_sources(quests_dir: Path) -> list[Chapter]:
    chapters = []
    for group, folder in GROUPS.items():
        for path in sorted((quests_dir / folder).glob("*.toml")):
            chapters.append(load_chapter(path, group))
    _validate(chapters)
    return chapters


def _validate(chapters: list[Chapter]) -> None:
    slugs = [c.slug for c in chapters]
    if len(set(slugs)) != len(slugs):
        raise QuestSourceError("two chapters share a slug")
    known = set()
    for c in chapters:
        seen = set()
        for q in c.quests:
            if q.slug in seen:
                raise QuestSourceError(f"{c.slug}: quest slug {q.slug} used twice")
            seen.add(q.slug)
            known.add((c.slug, q.slug))
    for c in chapters:
        for q in c.quests:
            for dep in q.dep_keys():
                if dep not in known:
                    raise QuestSourceError(f"{c.slug}:{q.slug} depends on unknown quest {':'.join(dep)}")
