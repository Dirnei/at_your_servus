# Proposal

## Why

After the Works, the next thing a player has to care about is food, and the quest book says nothing about it. Shuttle farming is one of the deepest parts of Shuttles (fields, water, harvest and spreader shuttles, stock levels, copper that corrodes and honeycomb that stops it), yet it is only three quests at the end of The Trading House. Players also found that Cooking for Blockheads and most of Just Dire Things (sensors, clickers, the higher tool tiers) are never mentioned, so they don't find them.

## What Changes

- New main chapter **The Fields** (`03-fields.toml`), opening from `old-works:terminal` in parallel to The Cellar. It teaches Farm Rail, Field Head with water from the Works, the Shuttle Workshop, a Harvester shuttle, stock levels, the Spreader with fertilizer, the Range Upgrade, rail corrosion and scraping, vanilla bees for honeycomb as the anti-corrosion item, and food variety with Spice of Life. It opens and closes with letters from Uncle Vinzenz. No main chapter depends on it.
- Later chapters are renumbered (Cellar 04 ... Finale 09); their slugs and quest IDs don't change.
- From The Trading House, `fields` and `range` move to The Fields, and `workshop` asks only for the Mk2 (the Shuttle Workshop is taught in The Fields). `wireless` depends on `mk3` instead of `fields`. **BREAKING** for saves: the two moved quests lose their progress.
- The Storage Terminal letter now sends the player to the fields and the cellar.
- New side chapter **The Kitchen** for Cooking for Blockheads, from the Cooking Table to a full kitchen, with the Spice of Life food book. The Building side chapter's `kitchen` quest moves there.
- New side chapter **Just Dire Things** for what Servus doesn't do: sensors (including the Advanced Sensor as a player detector), clicker, creature catcher, the higher goo tiers with Celestigem and Eclipse Alloy, the Time Wand and the Portal Gun. JDT's generators, energy transmitter and block breakers and placers stay out of the quests.
- `docs/story.md` gets the beat for The Fields; The Trading House beat loses "fields".

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `quest-line`: Main chapters gain The Fields after The Old Works; Chapter content moves field work from The Trading House to The Fields; Side chapters gain The Kitchen and Just Dire Things; a new requirement that The Fields opens beside The Cellar and gates no main chapter.

## Impact

- `quests/chapters/`: new `03-fields.toml`; `03-cellar.toml` to `08-workshop.toml` and `08-finale.toml` renamed to the next number; edits in `02-old-works.toml` (terminal letter) and the Trading House file.
- `quests/side/`: new `05-kitchen.toml` and `06-just-dire-things.toml`; `04-building.toml` loses `kitchen`.
- Regenerated `config/ftbquests/quests/`.
- `docs/story.md`.
- Needs `playtest-fixes-and-mods` first (Spice of Life, and the Works storage chain in the same files); archive that change before this one.
