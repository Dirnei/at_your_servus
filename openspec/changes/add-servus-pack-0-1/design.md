# Design

## Context

See `proposal.md` for the why and `docs/superpowers/specs/2026-10-19-servus-modpack-design.md` for the agreed pack design (mod roles, story, chapters).

Current state:
- This folder holds `Servus-0.1.0.zip` (a CurseForge export with 32 mods and configs in `overrides/config/`), an empty `openspec/` and the design document. It is not a git repository yet.
- Tools on the machine: Go 1.27, Java 21 (Adoptium), Python 3.14, Docker, git. Not installed: packwiz, GitHub CLI.
- Servus releases on GitHub: `foundation-v0.1.0-beta`, `shuttles-v0.1.0-beta`, `alchemy-v0.1.0-alpha`. Foundation (CurseForge 1747973) and Shuttles (1746893) are on CurseForge; Alchemy isn't visible there yet.
- The released Alchemy jar has no "Philosopher's Stone" item. Rubedo is the red Athanor (Crying Obsidian crown) plus the Prelum, which turns Caput Mortuum into Netherite. Item IDs used for gates: `servus_alchemy:quicksilver`, `servus_alchemy:ignis_perpetuus`, `servus_alchemy:caput_mortuum`, `servus_alchemy:prelum`.
- CurseForge availability for 26.1.2 was checked on 2026-10-19 (see the design document, section 4).

## Goals / Non-Goals

**Goals:**
- Everything that makes up the pack is plain text in git, and the pack is rebuilt from it in one command.
- Quests are written as readable source files, not edited by hand in SNBT.
- The same build runs on Windows (Dirnei) and on Linux (GitHub Actions).

**Non-Goals:**
- No changes to the Servus mods or to `servus_mc_mods/server`.
- No automated client test; joining with a real client is a manual step.
- No German translation in 0.1.0 (only the structure that allows it).

## Decisions

### D1: packwiz manages the mod list
Each mod is a `mods/<slug>.pw.toml` with its CurseForge project and file ID and its `side`. `packwiz cf import Servus-0.1.0.zip` seeds the repo, `packwiz cf add <slug>` adds mods and resolves dependencies, `packwiz cf export` writes the CurseForge zip.
- Alternative: a hand-written JSON list plus our own export script. Rejected: packwiz already does dependency resolution, hashing and the export format.
- Alternative: build in the CurseForge app and export. Rejected: not reviewable, not CI-friendly.
- packwiz is installed with `go install github.com/packwiz/packwiz@latest`; CI does the same.

### D2: Alchemy as a URL metafile until CurseForge lists it
`mods/servus-alchemy.pw.toml` uses `mode = "url"` with the GitHub asset URL and its sha256. Its dependency Modonomicon is added explicitly, because packwiz doesn't resolve dependencies for URL mods. `packwiz cf export` leaves URL mods out of the manifest, so the build script copies their jars into `overrides/mods/` of the playtest zip itself. A `-Public` build refuses any metafile without a `[update.curseforge]` section (pack-build "Public export guard"). Once Alchemy is visible, the metafile is replaced with `packwiz cf add servus-alchemy`.

### D3: Server pack through packwiz-installer
The build serves the pack locally with `packwiz serve` and runs `packwiz-installer-bootstrap.jar -g -s server http://localhost:8080/pack.toml` into `build/server/`. That honours `side` and downloads only server/both mods. The script then adds `start.ps1`/`start.sh` (download and run the NeoForge 26.1.2.122 installer once, then start the server) and zips `build/server/` into `dist/at-your-servus-<version>-server.zip`. packwiz-installer fails on CurseForge files with distribution disabled and lists them; the build passes that error through (pack-build "Undownloadable mods are reported").
- Alternative: our own downloader using the CurseForge API. Rejected: needs an API key locally and duplicates packwiz-installer.

### D4: Build and checks as one PowerShell entry point plus Python checks
`tools/build.ps1 [-Public]` runs: pack check, quest generation, quest check, `packwiz refresh`, client export, server pack, version cross-check. PowerShell 7 runs on Windows and on GitHub's Linux runners. Checks are Python (stdlib only: `tomllib`, `json`, `zipfile`) under `tools/checks/` with pytest tests under `tests/`, because they are pure logic over files and easy to test.
- `tools/checks/pack_check.py`: excluded project IDs, required mods, client-only sides, public-source guard.
- `tools/checks/version_check.py`: compares `manifest.json` file IDs with server pack jars.
- Excluded CurseForge project IDs: AE2 223794, Refined Storage 243076, Mystical Agriculture 246640, Productive Bees 377897, Replication 638351, Ender IO 64578, Oritech 1030830, Storage Drawers 223852, Traveler's Backpack 321117, Xaero's Minimap 263420, SecurityCraft 64760; Xaero's World Map and Iris by slug (IDs looked up when the check is written).

### D5: Quests generated from TOML sources
Sources live in `quests/` (outside `config/`): `quests/chapters/<NN>-<slug>.toml`, one per chapter, with chapter metadata and a list of quests (slug, icon, position, dependencies, tasks, rewards, English title/subtitle/description). `tools/questgen/` (Python, stdlib) writes the FTB Quests folder `config/ftbquests/quests/`: `data.json5`, `chapter_groups.json5`, `chapters/<slug>.json5` and `lang/en_us/` (`chapter.json5`, `chapter_group.json5`, `chapters/<slug>.json5`). FTB Quests 26.1.2.x stores quests as JSON5 and ignores `.snbt` files (found during implementation, see `tools/questgen/FORMAT.md`); the generator writes plain JSON with sorted keys, which is valid JSON5.
- IDs are the first 16 hex characters of `sha256("servus:" + chapter_slug + ":" + quest_slug)` with the top bit cleared (FTB Quests parses them as positive longs), uppercased, so they depend only on slugs (quest-line "Stable quest identities"). Output is sorted and has no timestamps, so it is byte-identical on rerun.
- The generated folder is committed, so the pack works without running the generator, and CI checks that regenerating gives no diff.
- The exact keys are taken from FTB Quests 26.1.2.9 (tag `v26.1.2.9`) and written down in `tools/questgen/FORMAT.md`. Text lives only in the lang files; inline titles are ignored by FTB Quests.
- Alternative: write quests in game with the FTB Quests editor. Rejected: Claude writes the texts, and hand-edited SNBT IDs are unstable and unreadable in diffs.

### D6: Item ID check against the pack's jars
`tools/checks/item_ids.py` builds the set of known item IDs from the jars in `build/server/mods` plus client-only jars (cached by the build): every `assets/<ns>/items/<id>.json` (26.1 item model definitions) and `assets/<ns>/models/item/<id>.json`. Vanilla IDs come from the NeoForge server jar's data and a small checked-in list for gaps. The quest check and a KubeJS reference scan both use it.

### D7: KubeJS for gates and the first-join book
- `kubejs/server_scripts/gates/iron_jetpacks.js`, `kubejs/server_scripts/gates/avaritia.js`: recipe changes per progression-gates. Exact recipe IDs and component layout are read from the Iron Jetpacks and Re:Avaritia jars when the scripts are written.
- `kubejs/server_scripts/first_join.js`: on login, if the player lacks the persistent tag `servus_got_quest_book`, give `ftbquests:book` and set the tag.
- `docs/gates.md` lists every change with its reason.
- Cobblegen Galore and Just Dire Things are tuned through their config files in `config/` (and datapack overrides in `kubejs/data/` where configs don't reach). The values are chosen after reading their configs and recipes; the rule is progression-gates "Resource mods do not replace Alchemy".

### D8: Test server in this repo
`server/docker-compose.yml` uses `itzg/minecraft-server:java25` with `TYPE=NEOFORGE`, `VERSION=26.1.2`, `NEOFORGE_VERSION=26.1.2.122`, `GENERIC_PACK=/packs/at-your-servus-latest-server.zip` (the build also writes this copy), `./data:/data`, `../dist:/packs:ro`. `server/.env.example` holds `OPS`, `WHITELIST`, `MEMORY`. `tools/smoke.ps1` runs `docker compose up -d`, follows logs until `Done (` or 10 minutes, then scans `logs/latest.log` and `kubejs/server.log` in `server/data` for `ERROR` lines from `ftbquests` or `KubeJS` and for a crash report, prints them and runs `docker compose down`.
- Alternative: reuse `servus_mc_mods/server`. Rejected: that setup builds the mods from source for mod playtests; the pack server must run exactly the pack's server zip.

### D9: CI on GitHub Actions
`.github/workflows/build.yml`: on push/PR, Ubuntu, set up Go, Java 25, Python 3.14, PowerShell; install packwiz; `pytest`; `tools/build.ps1`; check `git diff --exit-code config/ftbquests`; upload `dist/*`. `.github/workflows/publish.yml`: on tag `v*`, check tag equals `pack.toml` version, `tools/build.ps1 -Public`, then if `vars.CF_PROJECT_ID` and `secrets.CF_API_TOKEN` are set, upload with `curl` to `https://minecraft.curseforge.com/api/projects/<id>/upload-file` (client zip first, server zip with `parentFileID`), game version 26.1.2, release type from the version suffix. Without them it stops with a notice.

### D10: Repository layout
```
pack.toml, index.toml          packwiz metadata (name Servus, author Dirnei, version 0.1.0)
mods/                          *.pw.toml
config/, defaultconfigs/       overrides (seeded from Servus-0.1.0.zip)
config/ftbquests/quests/       generated, committed
kubejs/                        scripts and data
quests/chapters/*.toml         quest sources
tools/build.ps1, smoke.ps1     entry points
tools/checks/, tools/questgen/ Python
tests/                         pytest
server/                        Docker test server
docs/mods.md, gates.md, story.md
.github/workflows/
```
`.packwizignore` excludes `docs/`, `quests/`, `tools/`, `tests/`, `server/`, `openspec/`, `.github/`, `dist/`, `build/` from the pack index. `.gitignore` excludes `dist/`, `build/`, `server/data/`, `server/.env`.

## Risks / Trade-offs

- [Powah has only an alpha for 26.1.2] → Playtest it first; Energized Power is the agreed fallback, and only the Power Station chapter and the Avaritia gate's Powah item would change.
- [Twilight Forest, Undergarden, Bumblezone, JER, FTB Filter System, KubeJS are beta/alpha] → They are gap fillers; drop any that crashes in the smoke check and note it in `docs/mods.md`.
- [packwiz may not know Minecraft 26.1.2 or NeoForge's new version scheme] → `packwiz init` gets explicit `--mc-version 26.1.2 --modloader neoforge --neoforge-version 26.1.2.122`; if it rejects them, edit `pack.toml` versions by hand and use `packwiz cf add --addon-id --file-id` for exact files.
- [A mod disables third-party distribution] → The server pack build fails and names it. Then that mod is either dropped or documented for manual download; the CurseForge client pack is unaffected.
- [FTB Quests file format differs from what the generator writes] → FORMAT.md is taken from the exact version's source, and the smoke check fails on FTB Quests load errors.
- [Alchemy's quest texts drift from the journal] → Cellar quests only name stages and point to the journal; no task text copies journal tasks.
- [Story quality] → Claude writes all texts; Dirnei reviews `docs/story.md` and the generated quest texts before the first public upload.

## Migration Plan

1. Create the repo and seed it from `Servus-0.1.0.zip`. The zip was later removed from the repo and its history; `pack_check.py` keeps its 32 project IDs.
2. Playtest builds go to Dirnei's test server and friends via the client zip.
3. When Alchemy appears on CurseForge: replace the URL metafile, run `tools/build.ps1 -Public`, create the CurseForge project, set `CF_PROJECT_ID`/`CF_API_TOKEN`, push tag `v0.1.0`.
Rollback for a bad release: CurseForge files can be archived; the previous tag rebuilds the previous pack.

## Open Questions

- Exact YUNG's, Apotheosis module and Dungeons and Taverns CurseForge slugs and whether each has a 26.1.2 file; looked up when the mods are added.
