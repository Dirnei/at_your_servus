import zipfile

from tools.checks import item_ids


def test_known_items_reads_item_definitions_and_vanilla(tmp_path):
    with zipfile.ZipFile(tmp_path / "a.jar", "w") as z:
        z.writestr("assets/servus_alchemy/items/quicksilver.json", "{}")
        z.writestr("assets/servus_alchemy/models/item/not_an_item.json", "{}")
        z.writestr("data/servus_alchemy/recipe/x.json", "{}")
    ids = item_ids.known_items(tmp_path)
    assert "servus_alchemy:quicksilver" in ids
    assert "servus_alchemy:not_an_item" not in ids
    assert "minecraft:stone" in ids
