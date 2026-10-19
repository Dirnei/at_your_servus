# Tasks

Commit after each task with a one-line message of at most 74 characters, no body.

## 1. Repository and packwiz setup

- [x] 1.1 `git init`, add `.gitignore` (`dist/`, `build/`, `server/data/`, `server/.env`) and `.packwizignore` per design D10; verify `git status` shows only intended files
- [x] 1.2 Install packwiz with `go install github.com/packwiz/packwiz@latest`; verify `packwiz --help` runs
- [x] 1.3 Seed the pack: `packwiz cf import Servus-0.1.0.zip` (or `packwiz init` with name Servus, author Dirnei, version 0.1.0, MC 26.1.2, NeoForge 26.1.2.122, then import); verify `pack.toml` has those values, `mods/` has one metafile per project ID in the zip's `manifest.json`, and `config/` holds the zip's override configs
- [x] 1.4 Verify `packwiz refresh` and `packwiz cf export` succeed and the exported `manifest.json` lists the same 32 project IDs as `Servus-0.1.0.zip`

## 2. Mod selection and pack check

- [x] 2.1 Write `tools/checks/pack_check.py` with tests in `tests/test_pack_check.py`: excluded project IDs/slugs fail (design D4 list), required mods missing fails, listed client-only mods with a side other than `client` fail, `--public` fails on any metafile without `[update.curseforge]`; verify `pytest tests/test_pack_check.py` passes against fixture metafiles
- [ ] 2.2 Add the core path mods with `packwiz cf add`: Powah (Rearchitected), Iron Jetpacks, Re:Avaritia, Just Dire Things, Cobblegen Galore, FTB Quests, FTB XMod Compat, KubeJS, LootJS, Crafting on a Stick; verify each metafile references a 26.1.2 NeoForge file
- [ ] 2.3 Add Servus: Alchemy as a URL metafile (design D2) with the GitHub asset's sha256, plus Modonomicon via `packwiz cf add`; verify `packwiz refresh` succeeds and `pack_check.py` passes without `--public` and fails with it
- [ ] 2.4 Add the gap fillers from design document section 4.2 that have a 26.1.2 NeoForge file (look up YUNG's, Apotheosis module and Dungeons and Taverns slugs); verify `pack_check.py` passes
- [ ] 2.5 Set `side = "client"` for Sodium, Entity Culling, ImmediatelyFast, Mouse Tweaks, Controlling, Searchables, Better Advancements, Enchantment Descriptions and any other render/input/HUD-only mod; verify `pack_check.py` passes
- [ ] 2.6 Write `docs/mods.md`: every mod with its role, plus excluded and waiting mods (Ars Nouveau, Mekanism, ...) with reasons; verify every metafile in `mods/` has an entry (add this as a test in `tests/test_pack_check.py`)

## 3. Build: client and server pack

- [ ] 3.1 Write `tools/checks/version_check.py` with tests: given a `manifest.json` and a server `mods/` folder plus `mods/*.pw.toml`, fail when a shared mod's jar filename differs from its metafile's filename or a client-only jar is present; verify `pytest tests/test_version_check.py` passes
- [ ] 3.2 Write `tools/build.ps1 [-Public]` per design D3/D4: pack check, `packwiz refresh`, `packwiz cf export` to `dist/Servus-<version>.zip`, copy URL-mod jars into its `overrides/mods/` with a printed "not for public upload" warning (skipped and failing in `-Public`), `packwiz serve` + packwiz-installer-bootstrap `-g -s server` into `build/server/`, add `start.ps1`/`start.sh` that install NeoForge 26.1.2.122 on first run, zip to `dist/Servus-<version>-server.zip` and copy to `dist/Servus-latest-server.zip`, then run the version check; verify a clean run produces all three files
- [ ] 3.3 Verify the server zip has no Sodium jar, and that `-Public` fails while Alchemy is a URL metafile with a message naming Alchemy
- [ ] 3.4 Verify the build fails with the mod named when packwiz-installer reports a file that cannot be downloaded (simulate with a metafile pointing at a non-existent URL in a scratch copy)
- [ ] 3.5 Document the build in `README.md` (tools to install, `tools/build.ps1`, outputs); verify the documented command runs as written

## 4. Test server and smoke check

- [ ] 4.1 Write `server/docker-compose.yml` and `server/.env.example` per design D8; verify `docker compose config` succeeds
- [ ] 4.2 Write `tools/smoke.ps1` per design D8 (10-minute timeout, scans for FTB Quests/KubeJS errors and crash reports, always stops the container); verify it passes on the current build
- [ ] 4.3 Verify the smoke check fails and prints the log line when a scratch KubeJS script references `minecraft:not_an_item`, then remove the script
- [ ] 4.4 Document the test server in `README.md` (setup, start, update, how friends install the client zip); verify the steps match `server/`

## 5. Quest generator

- [ ] 5.1 Read FTB Quests 26.1.2.9's quest file format from its source and write `tools/questgen/FORMAT.md` (file layout, keys for chapter groups, chapters, quests, item/checkmark/advancement tasks, item/XP rewards, dependencies, lang file support); verify every key the generator will write is listed
- [ ] 5.2 Write `tools/questgen/snbt.py` (SNBT serialiser with sorted keys, typed numbers, escaped strings) with tests in `tests/test_snbt.py`; verify pytest passes
- [ ] 5.3 Write `tools/questgen/generate.py` (TOML sources → `config/ftbquests/quests/`) per design D5 with tests: IDs from `sha256("servus:" + chapter + ":" + quest)[:16]` uppercased, byte-identical rerun, text-only edit keeps IDs, unknown dependency slug fails, every title goes into `lang/en_us.snbt`; verify pytest passes
- [ ] 5.4 Write `tools/checks/item_ids.py` and `tools/checks/quest_check.py` with tests (design D6): unknown item IDs fail with quest and ID named, item tasks over 16 of a non-bulk item fail (bulk = items tagged `c:ingots`, `c:dusts`, `c:gems`, `c:cobblestones`, `c:stones`, `c:raw_materials`, logs, or listed in `quests/bulk.toml`), missing English titles fail; verify pytest passes
- [ ] 5.5 Wire generator and quest check into `tools/build.ps1` before the export; verify a build with one sample chapter loads in the smoke check without FTB Quests errors

## 6. Story and main chapters

- [ ] 6.1 Write `docs/story.md`: the uncle (name, life), the estate, the family trading business and its Schwaz link, the mystery's beat per chapter, the ending (uncle finished the Great Work and disappeared going "beyond the Stone"); verify each of the eight chapters has a beat
- [ ] 6.2 Write `quests/chapters/01-arrival.toml` and `02-old-works.toml` (Foundation basics plus the early warehouse per quest-line "Early warehouse"; first Alchemy product stored in the warehouse can link to chapter 3); verify the quest check passes and no chapter-2 quest needs a Powah item
- [ ] 6.3 Write `03-cellar.toml`: Paracelsus' Journal found, then one milestone per stage (Nigredo, Albedo, Citrinitas, Rubedo) that points to the journal chapter (Villach, Schwaz, Wandering years, Basel and Salzburg), with the Rubedo milestone on the Prelum; verify the quest check passes
- [ ] 6.4 Write `04-power-station.toml` (Powah) and `05-into-the-nether.toml` (Just Dire Things, link to Alchemy's Salamander); verify the quest check passes
- [ ] 6.5 Write `06-trading-house.toml` (put-away rules, data cable, Crafting CPU, Pattern Storage, Machine Adapter/Production Terminal on an Alchemy machine, Shuttle Workshop and Mk2/Mk3, Farm Rail and Field Head, Wireless Upgrade); verify the quest check passes and no main quest asks for Sophisticated/Functional Storage items
- [ ] 6.6 Write `07-workshop.toml` (Iron Jetpacks tiers) and `08-finale.toml` (Re:Avaritia up to Infinity Armor, resolves the mystery); verify the quest check passes
- [ ] 6.7 Verify the whole main line in the smoke check, and that no main quest depends on a side chapter quest (add this as a test in `tests/test_quest_check.py`)

## 7. Side chapters

- [ ] 7.1 Write `quests/side/` chapters in their own group: Exploration and Dimensions, Occultism, Apotheosis and Mob Farms (Dark Utilities, Apothic Spawners, Hostile Neural Networks), Building and Decor (Sophisticated/Functional Storage may appear here); verify the quest check and the side-chapter test pass

## 8. Progression gates

- [ ] 8.1 Read Iron Jetpacks' and Re:Avaritia's recipe IDs from their jars; write `kubejs/server_scripts/gates/iron_jetpacks.js` (Quicksilver from diamond tier up, Ignis Perpetuus for netherite, creative jetpack uncraftable) and `gates/avaritia.js` (Infinity Catalyst needs Ignis Perpetuus, Quicksilver, Caput Mortuum, Crafting CPU and a top-tier Powah item); verify the item ID check passes on both scripts and the smoke check shows no KubeJS errors
- [ ] 8.2 Write `kubejs/server_scripts/first_join.js` (give `ftbquests:book` once, persistent tag `servus_got_quest_book`); verify on the test server that a first join gives the book and a rejoin doesn't
- [ ] 8.3 Read Cobblegen Galore's and Just Dire Things' configs and recipes; change config/datapack values so neither produces ores, raw metals or gems; verify by looking up their generator outputs in JEI on a test client
- [ ] 8.4 Write `docs/gates.md` listing every recipe and config change with its reason; verify every script file in `kubejs/server_scripts/gates/` and every changed config is listed

## 9. CI and publishing

- [ ] 9.1 Write `.github/workflows/build.yml` per design D9 (pytest, build, no diff after quest regeneration, artifacts); verify with `act` or on the first GitHub push that the run is green
- [ ] 9.2 Write `.github/workflows/publish.yml` per design D9 (tag equals version, `-Public` build, upload only when `CF_PROJECT_ID` and `CF_API_TOKEN` are set, token never echoed); verify the tag/version mismatch check by running its script step locally with a mismatched tag
- [ ] 9.3 Document the release steps in `README.md` (switch Alchemy to CurseForge, create the CurseForge project, set variable and secret, tag); verify the steps match the workflows

## 10. Integration

- [ ] 10.1 Full build plus smoke check from a clean clone; verify both pass
- [ ] 10.2 Manual: Dirnei imports `dist/Servus-0.1.0.zip` in the CurseForge app and joins the test server; verify no mod mismatch and the quest book arrives
- [ ] 10.3 Manual: Dirnei reviews `docs/story.md` and the quest texts; verify feedback is folded in before the first public upload

## Workflow follow-up

- First public upload once Servus: Alchemy is visible on CurseForge (README release steps).
- Archive the change after the playtest with friends.
