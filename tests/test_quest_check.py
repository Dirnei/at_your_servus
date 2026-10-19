import pytest

from tools.checks import quest_check
from tools.questgen.model import Chapter, Quest, QuestSourceError, load_sources

ITEMS = {"minecraft:stone", "minecraft:bread", "servus_shuttles:heavy_rack", "minecraft:iron_ingot"}


def chapter(slug="old-works", group="main", quests=None):
    return Chapter(group=group, order=1, slug=slug, title="The Old Works", quests=quests or [])


def quest(slug="rack", chapter_slug="old-works", **kw):
    kw.setdefault("tasks", [{"type": "item", "item": "servus_shuttles:heavy_rack"}])
    return Quest(chapter=chapter_slug, slug=slug, title="A Rack", x=0.0, y=0.0, **kw)


def test_clean_chapter_passes():
    assert quest_check.check([chapter(quests=[quest()])], ITEMS, set()) == []


def test_unknown_item_names_quest_and_id():
    c = chapter(quests=[quest(tasks=[{"type": "item", "item": "servus_shuttles:rak"}])])
    assert quest_check.check([c], ITEMS, set()) == ["old-works:rack: unknown item servus_shuttles:rak"]


def test_unknown_icon_and_reward_fail():
    c = chapter(quests=[quest(icon="minecraft:nope", rewards=[{"type": "item", "item": "minecraft:nada"}])])
    assert len(quest_check.check([c], ITEMS, set())) == 2


def test_count_over_16_of_non_bulk_item_fails():
    c = chapter(quests=[quest(tasks=[{"type": "item", "item": "servus_shuttles:heavy_rack", "count": 32}])])
    assert quest_check.check([c], ITEMS, set()) == [
        "old-works:rack: asks for 32 servus_shuttles:heavy_rack, more than 16 of a non-bulk item"]


def test_count_over_16_of_bulk_item_passes():
    c = chapter(quests=[quest(tasks=[{"type": "item", "item": "minecraft:iron_ingot", "count": 64},
                                     {"type": "item", "item": "minecraft:bread", "count": 32}])])
    assert quest_check.check([c], ITEMS, {"minecraft:bread"}) == []


def test_missing_titles_fail():
    c = chapter(quests=[quest()])
    c.title = ""
    c.quests[0].title = ""
    assert quest_check.check([c], ITEMS, set()) == ["old-works: chapter has no English title",
                                                    "old-works:rack: quest has no English title"]


def test_main_quest_must_not_depend_on_side_quest():
    side = chapter(slug="exploration", group="side", quests=[quest(slug="portal", chapter_slug="exploration")])
    main = chapter(quests=[quest(deps=["exploration:portal"])])
    assert quest_check.check([main, side], ITEMS, set()) == [
        "old-works:rack: main quest depends on side quest exploration:portal"]


def test_side_quest_may_depend_on_main_quest():
    main = chapter(quests=[quest()])
    side = chapter(slug="exploration", group="side",
                   quests=[quest(slug="portal", chapter_slug="exploration", deps=["old-works:rack"])])
    assert quest_check.check([main, side], ITEMS, set()) == []


def test_loader_rejects_unknown_dependency(tmp_path):
    (tmp_path / "chapters").mkdir()
    (tmp_path / "chapters" / "01-arrival.toml").write_text(
        '[chapter]\ntitle = "Arrival"\n[[quest]]\nslug = "a"\ntitle = "A"\nx = 0.0\ny = 0.0\ndeps = ["missing"]\n'
        'tasks = [{ type = "checkmark" }]\n', encoding="utf-8")
    with pytest.raises(QuestSourceError, match="unknown quest arrival:missing"):
        load_sources(tmp_path)


def test_main_line_sources_pass_the_check():
    """The real quest sources: every main chapter quest is reachable without side chapters."""
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent
    mods = root / "build" / "server" / "mods"
    if not mods.exists():
        pytest.skip("no server pack built yet")
    chapters = load_sources(root / "quests")
    assert quest_check.check(chapters, quest_check.known_items(mods), quest_check.bulk_items(root / "quests")) == []
