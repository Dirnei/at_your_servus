# Tasks

## 1. Any-of dependencies in the quest generator

- [x] 1.1 Add the optional `dependency_requirement` key (`all_completed` default, `one_completed`) to `Quest` in `tools/questgen/model.py` and its docstring, rejecting other values; verify with a new loader test in `tests/test_generate.py`
- [x] 1.2 Write `dependency_requirement` in `_quest` in `tools/questgen/generate.py` only when it is not the default; verify with a test that checks the key in the generated chapter and with `test_rerun_is_byte_identical`
- [x] 1.3 Document the new key in `tools/questgen/FORMAT.md`; verify the generator still writes the existing chapters unchanged (`python -m tools.questgen.generate`, then `git diff --stat config/ftbquests` shows no changes)

## 2. Quest check rules

- [x] 2.1 Add a deny list of reward items holding `servus_alchemy:sealed_flask`; verify with a test that a Sealed Flask reward fails and names the quest

## 3. Sealed Flask reward

- [x] 3.1 Change the `alchemy-order` reward in `quests/chapters/07-trading-house.toml` to 8 emeralds; verify `python -m pytest tests/test_quest_check.py` passes (`test_main_line_sources_pass_the_check`)

## 4. Cellar chapter

- [x] 4.1 Rework `quests/chapters/04-cellar.toml` per design.md: add `purifier` and `coagulator`, point `athanor` at `coagulator`, change `nigredo` to a Salt Crystal Block, move `salt-in-the-racks` behind `coagulator`, keep every existing slug; verify with `python -m tools.checks.quest_check --quests quests --mods <mods folder>`
- [x] 4.2 Add the three product-option quests before each of `albedo`, `citrinitas` and `rubedo` (seeds with the `servus_alchemy:vein` component), give the three hexagons `one_completed`, one checkmark task and an icon, and turn `seed` into the Seed of Iron option; verify the quest check passes and every option item's fire matches the table in design.md
- [x] 4.3 Add the follow-ups `netherite` (Prelum, Caput Mortuum, with Rubedo's Netherite Scrap reward) and `receptaculum` after `rubedo`; verify `cellar:rubedo` no longer asks for them and the quest check passes
- [x] 4.4 Rewrite the milestone texts so Nigredo explains the white ring, Albedo the yellow ring and Citrinitas the red crown, following `docs/story.md` (Vinzenz' voice, plain short sentences, Bavarian setting); verify by reading the generated lang file `config/ftbquests/quests/lang/en_us/chapters/cellar.json5`
- [x] 4.5 Run `python -m tools.questgen.generate`, `packwiz refresh` and `python -m pytest`; verify all pass and the generated files are committed with the sources

## 5. Ungated Nether

- [x] 5.1 Remove the dependency of `nether:nether-letter` in `quests/chapters/06-nether.toml` and make its reward 50 XP, keeping `nether:goo` behind the letter; verify the quest check passes and the letter has no `dependencies` in the generated `chapters/nether.json5`

## 6. Playtest fixes

- [x] 6.1 Move `prelum-screw` out of the Rubedo fan: after `rubedo` comes `receptaculum` (Receptaculum and Sealed Flask), then `prelum-screw`, then `netherite`; Rubedo's fan keeps the two seeds
- [x] 6.2 Add an `observation` task type to the quest generator (`observe`, optional `observation_type` and `timer`) with tests, and show it in the quest explorer
- [x] 6.3 Complete `nether:nether-letter` by looking at a lit Nether portal instead of a checkmark

## 7. In-game check

- [x] 7.1 Start the local server (`docker compose restart mc`), join with a client and confirm in the quest book that the Cellar shows the new order, and that completing one option quest unlocks its hexagon's checkmark, and that the Nether letter is open from the start with Primal Goo behind it
- [ ] 7.2 Confirm `nether:salamander` still unlocks from `cellar:albedo` and that an existing world with `cellar:albedo` done keeps it done

## Workflow follow-up

- Commit the change as one `fix:` commit.
- Archive the change with `/opsx:archive` after review.
