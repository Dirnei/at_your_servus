# Tasks

## 1. Chapter order and story

- [x] 1.1 `git mv` the main chapter files `03-cellar.toml` ... `08-finale.toml` one number up; run `python -m tools.questgen.generate`; verify `git diff config/ftbquests/quests` shows only order changes and no changed quest IDs, and `python -m pytest` passes
- [x] 1.2 In `docs/story.md`, add the beat row for 3 The Fields (Shuttles fields, bees, food variety; the Huber farm fed the miners, Vinzenz put shuttles on the fields, bees by the old orchard keep the copper bright), renumber the later rows and drop "fields" from The Trading House beat; verify the table lists nine chapters in the order of the quest-line spec

## 2. The Fields

- [x] 2.1 Write `quests/chapters/03-fields.toml` with the chain from design D2 (`fields-letter` depending on `old-works:terminal`, `farm-rail`, `field-head`, `shuttle-workshop`, `harvester`, `first-harvest`, `stock-levels`, `spreader`, `range`, `corrosion`, `bees`, `honeycomb`, `anti-corrosion`, `food-variety`, `fields-done`), letters in the style of `docs/story.md`; run `python -m tools.questgen.generate`; verify `python -m tools.checks.quest_check --quests quests --mods server/local-data/mods` and `python -m pytest` pass
- [x] 2.2 In The Trading House, remove `fields`, remove `range` (now in The Fields), make `workshop` ask only for the Mk2 and mention the Shuttle Workshop in its text, make `wireless` depend on `mk3`; in `02-old-works.toml`, end the terminal letter with the fields and the cellar; regenerate; verify no quest outside `03-fields.toml` depends on a `fields:` quest (`grep -rn 'fields:' quests` lists only The Fields) and the checks from 2.1 pass
- [ ] 2.3 Manual, on the test server with a fresh player who has finished the Works: verify The Fields and The Cellar open together; build a field the way the quests say and get a first harvest into the warehouse; let the copper age one stage and scrape it with an axe; get honeycomb from a nest with a campfire and shears, set it as anti-corrosion and see the stage hold

## 3. Side chapters

- [x] 3.1 Write `quests/side/05-kitchen.toml` per design D5 and remove `kitchen` from `04-building.toml` (fix any deps on it); check the default oven and fridge items in JEI and use them; regenerate; verify the checks from 2.1 pass
- [x] 3.2 Look up the Advanced Sensor's area limit in its config under `server/local-data/config/` (or in-game); write `quests/side/06-just-dire-things.toml` per design D6 with the limit in the sensor text and no generator, energy transmitter, block breaker or block placer tasks; regenerate; verify the checks from 2.1 pass and `grep -E 'generatort|energytransmitter|blockbreaker|blockplacer' quests/side/06-just-dire-things.toml` finds nothing
- [ ] 3.3 Manual: open the quest book on the test server; verify both side chapters show in the side group, the Advanced Sensor set to Player gives a signal when a player walks into its area, and no side quest is required by a main quest

## 4. Integration

- [x] 4.1 Run `python -m pytest`, `python -m tools.checks.pack_check`, `python -m tools.checks.quest_check --quests quests --mods server/local-data/mods` and `packwiz refresh`; verify all pass and `config/ftbquests/quests/` is committed with the sources

## Workflow follow-up

- Archive `playtest-fixes-and-mods` before this change.
- One commit for the change, for example `feat: add The Fields chapter, Kitchen and Just Dire Things side quests`.
