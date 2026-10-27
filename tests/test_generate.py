import json

import pytest

from tools.questgen import generate
from tools.questgen.model import QuestSourceError, load_sources, stable_id

ARRIVAL = '''[chapter]
title = "Arrival"
subtitle = "A cold house"
icon = "minecraft:oak_door"

[[quest]]
slug = "first-letter"
title = "A Letter"
subtitle = "Servus, heir"
description = """
Servus, heir,

the house is yours."""
x = 0.0
y = 0.0
shape = "gear"
tasks = [{ type = "checkmark" }]
rewards = [{ type = "item", item = "minecraft:bread", count = 8 }, { type = "xp", amount = 20 }]

[[quest]]
slug = "jetpack"
title = "A Jetpack"
x = 2.0
y = 0.0
deps = ["first-letter"]
tasks = [{ type = "item", item = "ironjetpacks:jetpack", components = { "ironjetpacks:jetpack_id" = "ironjetpacks:iron" } },
         { type = "item", item = "minecraft:iron_ingot", count = 16 }]
'''

SIDE = '''[chapter]
title = "Exploration"

[[quest]]
slug = "compass"
title = "A Compass"
x = 0.0
y = 0.0
deps = ["arrival:first-letter"]
tasks = [{ type = "item", item = "minecraft:compass" }]
'''


@pytest.fixture
def sources(tmp_path):
    (tmp_path / "chapters").mkdir()
    (tmp_path / "side").mkdir()
    (tmp_path / "chapters" / "01-arrival.toml").write_text(ARRIVAL, encoding="utf-8")
    (tmp_path / "side" / "01-exploration.toml").write_text(SIDE, encoding="utf-8")
    return tmp_path


def test_ids_are_valid_ftb_quests_longs():
    for parts in [("arrival",), ("arrival", "first-letter"), ("group", "main")]:
        code = stable_id(*parts)
        assert len(code) == 16 and code == code.upper()
        assert 2 <= int(code, 16) <= 0x7FFFFFFFFFFFFFFF


def test_quest_id_depends_only_on_slugs():
    assert stable_id("arrival", "first-letter") == stable_id("arrival", "first-letter")
    assert stable_id("arrival", "first-letter") != stable_id("arrival", "second-letter")


def test_rerun_is_byte_identical(sources):
    assert generate.build(load_sources(sources)) == generate.build(load_sources(sources))


def test_text_edit_keeps_ids(sources):
    before = generate.build(load_sources(sources))["chapters/arrival.json5"]
    path = sources / "chapters" / "01-arrival.toml"
    path.write_text(path.read_text(encoding="utf-8").replace("the house is yours.", "the house is all yours."), encoding="utf-8")
    files = generate.build(load_sources(sources))
    assert files["chapters/arrival.json5"] == before
    assert "the house is all yours." in files["lang/en_us/chapters/arrival.json5"]


def test_chapter_file_layout(sources):
    files = generate.build(load_sources(sources))
    chapter = json.loads(files["chapters/arrival.json5"])
    assert chapter["filename"] == "arrival"
    assert chapter["group"] == stable_id("group", "main")
    letter, jetpack = chapter["quests"]
    assert letter["shape"] == "gear" and letter["x"] == 0.0
    assert letter["rewards"][0]["item"] == {"id": "minecraft:bread", "count": 1} and letter["rewards"][0]["count"] == 8
    assert letter["rewards"][1] == {"id": letter["rewards"][1]["id"], "type": "xp", "xp": 20}
    assert jetpack["dependencies"] == [letter["id"]]
    assert jetpack["tasks"][0]["item"]["components"] == {"ironjetpacks:jetpack_id": "ironjetpacks:iron"}
    assert jetpack["tasks"][0]["match_components"] == "fuzzy"
    assert jetpack["tasks"][1]["count"] == 16 and "count" not in jetpack["tasks"][0]


def test_cross_chapter_dependency_and_groups(sources):
    files = generate.build(load_sources(sources))
    side = json.loads(files["chapters/exploration.json5"])
    assert side["group"] == stable_id("group", "side")
    assert side["quests"][0]["dependencies"] == [stable_id("arrival", "first-letter")]
    groups = json.loads(files["chapter_groups.json5"])["chapter_groups"]
    assert [g["id"] for g in groups] == [stable_id("group", "main"), stable_id("group", "side")]


def test_every_title_goes_to_english_lang_files(sources):
    files = generate.build(load_sources(sources))
    quest_lang = json.loads(files["lang/en_us/chapters/arrival.json5"])
    qid = stable_id("arrival", "first-letter")
    assert quest_lang[f"quest.{qid}.title"] == "A Letter"
    assert quest_lang[f"quest.{qid}.quest_subtitle"] == "Servus, heir"
    assert quest_lang[f"quest.{qid}.quest_desc"] == ["Servus, heir,", "", "the house is yours."]
    chapters = json.loads(files["lang/en_us/chapter.json5"])
    assert chapters[f"chapter.{stable_id('arrival')}.title"] == "Arrival"
    assert chapters[f"chapter.{stable_id('arrival')}.chapter_subtitle"] == ["A cold house"]
    assert '"title"' not in files["chapters/arrival.json5"]


def test_ampersand_is_escaped_for_ftb_quests(sources):
    path = sources / "chapters" / "01-arrival.toml"
    path.write_text(ARRIVAL.replace('title = "A Letter"', 'title = "Huber & Co."')
                    .replace("the house is yours.", "Huber & Co., since 1521"), encoding="utf-8")
    files = generate.build(load_sources(sources))
    quest_lang = json.loads(files["lang/en_us/chapters/arrival.json5"])
    qid = stable_id("arrival", "first-letter")
    assert quest_lang[f"quest.{qid}.title"] == "Huber \\& Co."
    assert quest_lang[f"quest.{qid}.quest_desc"][-1] == "Huber \\& Co., since 1521"


def test_data_file_has_required_keys(sources):
    data = json.loads(generate.build(load_sources(sources))["data.json5"])
    for key in ["version", "default_reward_team", "default_consume_items", "default_autoclaim_rewards",
                "default_quest_shape", "default_quest_disable_jei", "drop_loot_crates"]:
        assert key in data
    assert data["version"] == 13


def test_unknown_dependency_fails(sources):
    path = sources / "side" / "01-exploration.toml"
    path.write_text(SIDE.replace("arrival:first-letter", "arrival:nope"), encoding="utf-8")
    with pytest.raises(QuestSourceError):
        generate.build(load_sources(sources))


def test_any_of_dependencies_written_only_when_set(sources):
    path = sources / "chapters" / "01-arrival.toml"
    path.write_text(ARRIVAL.replace('deps = ["first-letter"]', 'deps = ["first-letter"]\ndependency_requirement = "one_completed"'),
                    encoding="utf-8")
    letter, jetpack = json.loads(generate.build(load_sources(sources))["chapters/arrival.json5"])["quests"]
    assert jetpack["dependency_requirement"] == "one_completed"
    assert "dependency_requirement" not in letter


def test_observation_task(sources):
    path = sources / "chapters" / "01-arrival.toml"
    path.write_text(ARRIVAL.replace('tasks = [{ type = "checkmark" }]',
                                    'tasks = [{ type = "observation", observe = "minecraft:nether_portal" }]'), encoding="utf-8")
    letter = json.loads(generate.build(load_sources(sources))["chapters/arrival.json5"])["quests"][0]
    task = letter["tasks"][0]
    assert (task["type"], task["observation_type"], task["to_observe"], task["timer"]) ==         ("observation", "block", "minecraft:nether_portal", 0)


def test_unknown_observation_type_fails(sources):
    path = sources / "chapters" / "01-arrival.toml"
    path.write_text(ARRIVAL.replace('tasks = [{ type = "checkmark" }]',
                                    'tasks = [{ type = "observation", observe = "minecraft:pig", observation_type = "mob" }]'),
                    encoding="utf-8")
    with pytest.raises(QuestSourceError, match="observation_type"):
        generate.build(load_sources(sources))


def test_unknown_dependency_requirement_fails(sources):
    path = sources / "chapters" / "01-arrival.toml"
    path.write_text(ARRIVAL.replace('deps = ["first-letter"]', 'deps = ["first-letter"]\ndependency_requirement = "any"'),
                    encoding="utf-8")
    with pytest.raises(QuestSourceError, match="dependency_requirement"):
        load_sources(sources)
