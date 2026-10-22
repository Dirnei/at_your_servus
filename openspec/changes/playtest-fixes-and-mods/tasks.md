# Tasks

## 1. Ampersands in quest texts

- [x] 1.1 In `tools/questgen/generate.py`, replace every `&` with `\&` in each title, subtitle and description line written to the lang files (chapter, group and quest lang); add a test in `tests/test_generate.py` that a description "Huber & Co." decodes to `Huber \& Co.` from the lang file (the file itself holds `Huber \\& Co.`); run `python -m tools.questgen.generate`; verify `python -m pytest tests/test_generate.py` passes and `grep -rn '[^\\]& ' config/ftbquests/quests/lang` finds nothing

## 2. Works storage chain and chimney

- [x] 2.1 In `quests/chapters/02-old-works.toml`, drop the `servus_foundation:chimney` task and the chimney sentence from `coal-generator`; verify the generated quest has one task
- [x] 2.2 Move `data-cable` and `packing` from `06-trading-house.toml` to `02-old-works.toml` as `data-cable` and `packing-station`, chained `controller -> data-cable -> packing-station -> terminal`; rewrite their texts for the Works (the cable joins terminal, controller and Packing Station; the Packing Station is the warehouse's door to the data line) and the terminal letter where it says how the terminal reaches the racks; shift `terminal` right on the map; in The Trading House, make `crafting-station` depend on `outbound` and drop `packing` from `alchemy-order`'s deps; run `python -m tools.questgen.generate`; verify `python -m tools.checks.quest_check --quests quests --mods server/local-data/mods` and `python -m pytest` pass
- [ ] 2.3 Manual, on the test server with a fresh player: build the Works warehouse the way the quests say (controller powered, Data Cable from terminal to controller, Packing Station on the line at the rails); verify the terminal lists the racks, a request arrives at the terminal, an item stored at the terminal ends up in a rack, and "A Merchant Needs a Warehouse" shows "Huber & Co." with no formatting error

## 3. Gap-filling mods

- [x] 3.1 `packwiz curseforge add spice-of-life-carrot-edition`, `entangled` and `"TorchMaster: Version Locked"` (slug `torchmaster-version-locked`); keep `side = "both"`; add rows to `docs/mods.md` (Spice of Life: hearts for food variety; Torchmaster: Feral Flare Lantern, Megatorch, Dread Lamp; Entangled: linked blocks); run `packwiz refresh`; verify `python -m tools.checks.pack_check --public` and `python -m pytest` pass
- [x] 3.2 `packwiz curseforge add lighty`, set `side = "client"`, add `lighty` to `CLIENT_ONLY_SLUGS` in `tools/checks/pack_check.py` and a row to `docs/mods.md` ("Light level overlay, F7"); run `packwiz refresh`; verify `python -m tools.checks.pack_check --public` and `python -m pytest` pass

## 4. Shaders

- [x] 4.1 In `tools/checks/pack_check.py`, add a rule that the `r<version>` in the file names of `euphoria-patches` and every `complementary-*` shader pack are equal and present, naming the files on failure; add tests in `tests/test_pack_check.py` for matching versions, a mismatch and a missing version; verify `python -m pytest tests/test_pack_check.py` passes
- [x] 4.2 `packwiz curseforge add complementary-unbound --meta-folder shaderpacks` and `packwiz curseforge add euphoria-patches`; set `side = "client"` on both, add `euphoria-patches` to `CLIENT_ONLY_SLUGS`; add `complementary-unbound` to the "Shader packs" table and `euphoria-patches` to the mods list in `docs/mods.md`, and say there that the patched packs appear at the first game start; run `packwiz refresh`; verify `python -m tools.checks.pack_check --public` and `python -m pytest` pass

## 5. Integration

- [x] 5.1 Run `.\tools\build.ps1 -Public`; verify it passes, the client zip's `manifest.json` lists the five new mods and Complementary Unbound, and `build/server/` contains neither Lighty, Euphoria Patches nor a `shaderpacks/` folder
- [ ] 5.2 Manual, client from the zip: verify no shader pack is active at the first start and Shader Packs lists Reimagined, Unbound and both Euphoria versions; F7 toggles Lighty and the controls menu shows no F7 conflict; the Feral Flare Lantern and the Entangled Block have recipes in JEI; eating different foods reaches the first Spice of Life milestone and adds health; a Megatorch doesn't stop an Apothic spawner (if it does, add the config change and a `docs/gates.md` entry)

## Workflow follow-up

- Archive this change before `add-fields-and-side-quests`; both modify the quest-line "Chapter content" requirement.
- One commit for the change, for example `feat: playtest fixes, food hearts, lanterns, Entangled, light overlay`.
