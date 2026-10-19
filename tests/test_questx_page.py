import json
import re
from pathlib import Path

from tools.questgen.model import load_sources
from tools.questx import __main__ as questx, page
from tools.questx.findings import find


def test_page_embeds_every_quest_and_loads_nothing_from_the_web():
    chapters = load_sources(Path("quests"))
    items = {i: {"name": i, "kind": "none", "textures": []} for i in page.used_items(chapters)}
    html = page.render(page.page_data(chapters, items, find(chapters), "2026-10-20 12:00"))
    data = json.loads(re.search(r'<script type="application/json" id="data">(.*?)</script>', html, re.S)[1])
    keys = {f"{c['slug']}:{q['slug']}" for c in data["chapters"] for q in c["quests"]}
    assert keys == {f"{c.slug}:{q.slug}" for c in chapters for q in c.quests}
    assert "arrival:food" in keys
    assert not re.search(r"https?://", html.replace("http://www.w3.org/2000/svg", ""))


def test_script_end_tag_in_text_is_escaped():
    html = page.render({"chapters": [], "items": {}, "findings": [], "built": "</script><b>"})
    assert "</script><b>" not in html


def test_quest_icon_defaults_to_first_item_task():
    [arrival] = [c for c in load_sources(Path("quests")) if c.slug == "arrival"]
    food = next(q for q in arrival.quests if q.slug == "food")
    assert page.quest_icon(food) == "minecraft:bread"


def test_missing_mods_folder_says_to_build_first(tmp_path, capsys):
    assert questx.main(["--mods", str(tmp_path / "nope")]) == 1
    err = capsys.readouterr().err
    assert "nope" in err and "build the server pack first" in err
