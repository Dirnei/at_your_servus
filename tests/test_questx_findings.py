from pathlib import Path

from tools.questgen.model import Chapter, Quest, load_sources
from tools.questx.findings import find


def quest(slug, x=0.0, y=0.0, **kw):
    return Quest(chapter="arrival", slug=slug, title=slug, x=x, y=y, **kw)


def chapter(quests, slug="arrival", group="main"):
    for q in quests:
        q.chapter = slug
    return Chapter(group=group, order=1, slug=slug, title=slug, quests=quests)


def bread(count):
    return [{"type": "item", "item": "minecraft:bread", "count": count}]


def test_reward_upstream_covers_task():
    c = chapter([quest("letter", rewards=bread(8)),
                 quest("bench", x=2, deps=["letter"]),
                 quest("food", x=4, deps=["bench"], tasks=bread(8))])
    [f] = find([c])
    assert (f.chapter, f.slug, f.kind) == ("arrival", "food", "covered")
    assert f.line() == "arrival:food: task 8 minecraft:bread is already covered by rewards of arrival:letter"


def test_smaller_reward_partly_covers_task():
    c = chapter([quest("letter", rewards=bread(4)), quest("food", x=2, deps=["letter"], tasks=bread(8))])
    assert [f.kind for f in find([c])] == ["partly-covered"]


def test_reward_off_the_path_does_not_count():
    c = chapter([quest("letter"), quest("side", x=2, rewards=bread(8)),
                 quest("food", x=4, deps=["letter"], tasks=bread(8))])
    assert find([c]) == []


def test_same_position_and_main_needs_side():
    side = chapter([quest("trip")], slug="exploration", group="side")
    main = chapter([quest("a"), quest("b", deps=["exploration:trip"])])
    kinds = sorted(f.kind for f in find([main, side]))
    assert kinds == ["main-needs-side", "same-position"]


def test_current_quest_line_has_no_covered_task():
    assert [f for f in find(load_sources(Path("quests"))) if f.kind == "covered"] == []
