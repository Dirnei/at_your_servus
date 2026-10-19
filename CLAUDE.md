# At Your Servus modpack

packwiz modpack for Minecraft 26.1.2 / NeoForge 26.1.2.122, built around the Servus mods (source: `C:\games\minecraft\servus_mc_mods`). Build and release details: `docs/development.md`.

## Rules

- Servus mods are the main path; other mods only fill gaps. Storage and autocrafting are Shuttles' job: no AE2, no Refined Storage. `tools/checks/pack_check.py` enforces the excluded and required mods.
- Every mod has a row in `docs/mods.md` (a test checks this). Every recipe or config change to another mod goes into `docs/gates.md` with its reason.
- Servus is Bavarian, never Austrian. The story is set above Berchtesgaden.

## Quests

- Edit `quests/chapters/*.toml` (main) and `quests/side/*.toml`, then run `python -m tools.questgen.generate` and commit the generated `config/ftbquests/quests/` too. Never edit the generated JSON5 by hand.
- Quest IDs come from the chapter and quest slugs: renaming a slug resets player progress. Change titles and texts freely.
- Story texts follow `docs/story.md`: letters from Uncle Vinzenz (Vinzenz Huber), "Servus, kid," ... "Uncle Vinzenz". Plain, everyday English, short sentences.
- FTB Quests 26.1.2 reads JSON5 only and silently ignores `.snbt`. Text lives in the lang files, not inline.

## Checks

```powershell
python -m pytest
python -m tools.checks.pack_check
python -m tools.checks.quest_check --quests quests --mods <a mods folder with the jars>
python -m tools.checks.script_check
```

- After any change to `mods/`, `config/`, `kubejs/` or `defaultconfigs/`: `packwiz refresh`. Files not listed in `.packwizignore` (anchored `/paths`) end up in the pack.
- Test on the local server: `docker compose up -d` in the repo root (serves the working tree, port 25567), `docker compose restart mc` after changes. The server log only proves the server starts; network bugs like a recipe that fails to sync show up only when a client joins.
- KubeJS: recipes added in the same `ServerEvents.recipes` event are invisible to `forEachRecipe`. Check `server/local-data/logs/kubejs/server.log` for "with 0 failed recipes".

## Gotchas

- Line endings are LF (`.gitattributes`). Write files from Python with `write_bytes` or `newline=""`, or the packwiz index hashes differ in a fresh clone.
- Every mod must come from CurseForge: `build.ps1 -Public` (and so every release) refuses mods from other URLs.
- The client zip's profile image is added after `packwiz cf export` by `python -m tools.ziptool image`; packwiz does not write it.
