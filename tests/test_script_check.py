from tools.checks import script_check

ITEMS = {"servus_alchemy:quicksilver", "ironjetpacks:elite_coil", "minecraft:bedrock"}


def test_known_items_pass_and_tags_and_ids_are_skipped():
    script = """
    event.remove({ id: 'ironjetpacks:elite_coil' })
    event.shaped('ironjetpacks:elite_coil', ['Q'], { Q: 'servus_alchemy:quicksilver', D: '#c:gems/diamond' }).id('servus:gates/elite_coil')
    event.custom({ type: 'avaritia:infinity_catalyst', ingredients: ['minecraft:bedrock'] })
    """
    assert script_check.check({"gates/a.js": script}, ITEMS) == []


def test_unknown_item_is_reported():
    assert script_check.check({"gates/a.js": "event.shaped('servus_alchemy:quiksilver', [], {})"}, ITEMS) == [
        "gates/a.js: unknown item servus_alchemy:quiksilver"]
