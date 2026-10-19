# At Your Servus

A kitchen-sink pack built around the Servus mods, for Minecraft 26.1.2 on NeoForge. A guided FTB Quests line tells the story of Uncle Vinzenz's land above Berchtesgaden, in Bavaria, and leads through the Servus mods first.

- What is in the pack and why: [`docs/mods.md`](docs/mods.md)
- Design: [`docs/superpowers/specs/2026-10-19-servus-modpack-design.md`](docs/superpowers/specs/2026-10-19-servus-modpack-design.md), specs in [`openspec/`](openspec/)

## Tools

| Tool | Install |
|---|---|
| packwiz | `go install github.com/packwiz/packwiz@latest` (needs Go) |
| Java 21 or newer | runs packwiz-installer during the build |
| Python 3.11 or newer | checks, quest generator; `pip install pytest` for the tests |
| PowerShell | Windows PowerShell 5.1 or PowerShell 7 |
| Docker | only for the test server |

## Build

```powershell
.\tools\build.ps1           # playtest build
.\tools\build.ps1 -Public   # public build, fails while any mod is not from CurseForge
python -m pytest            # tests for the checks and the quest generator
```

The build writes to `dist/`:

| File | For |
|---|---|
| `Servus-<version>.zip` | CurseForge app import (client) |
| `Servus-<version>-server.zip` | dedicated servers: run `start.sh` or `start.ps1` (installs NeoForge 26.1.2.122 on first run, needs Java 25) |
| `Servus-latest-server.zip` | the same server pack, picked up by the test server |

A playtest build carries mods that are not on CurseForge (for now Servus: Alchemy) inside the client zip's `overrides/mods`. Such a zip must not be uploaded to CurseForge; the build warns about it, and `-Public` refuses to build.

If a mod's author blocks third-party downloads, the server pack build stops and names the mod and its download page.

## Local server

For quick testing on this machine, `docker-compose.yml` in the repo root runs a server straight from the working tree, with no build. An nginx container serves the repo, and the server installs the pack with packwiz on every start.

```powershell
docker compose up -d
docker compose logs -f mc              # wait for "Done", then connect to localhost:25567
```

After changing mods or configs: `packwiz refresh`, then `docker compose restart mc`. The world lives in `server/local-data`; delete it for a fresh world. Set `LOCAL_PORT`, `MEMORY` or `OPS` in the environment or a root `.env` to change them.

## Test server

The test server runs the latest built server pack in Docker (`itzg/minecraft-server:java25`). The world lives in `server/data` and survives restarts.

```powershell
copy server\.env.example server\.env   # once: set OPS, WHITELIST, MEMORY
.\tools\build.ps1
cd server; docker compose up -d
docker compose logs -f                 # wait for "Done"
```

After a new build: `docker compose restart` in `server/`; the new server pack is applied on start. Friends need the client zip of the same build, or they cannot join.

**Friends:** in the CurseForge app, Create Custom Profile, Import, pick `Servus-<version>.zip`. Give the profile at least 6 GB of memory, start it, Multiplayer, add the server (LAN IP, or a forwarded port 25565 / Tailscale from elsewhere).

**Smoke check:** `.\tools\smoke.ps1` starts the server pack in a throwaway world on port 25566, waits for it to be ready (at most 10 minutes), fails on a crash or on FTB Quests/KubeJS errors, and stops it again. Your playtest world is not touched.

## Releases

GitHub Actions builds every push (`.github/workflows/build.yml`): tests, both packs, and a check that the committed quest book matches `quests/`. The packs are kept as build artifacts.

A tag `v<version>` runs `.github/workflows/publish.yml`: it checks the tag against `pack.toml`, runs a public build and uploads the client zip and its server pack to CurseForge. `-alpha` and `-beta` versions are uploaded as alpha and beta.

First public release:

1. Wait until Servus: Alchemy is listed on CurseForge, then switch it over: `packwiz remove servus-alchemy`, `packwiz curseforge add servus-alchemy`.
2. `.\tools\build.ps1 -Public` must pass locally.
3. Create the modpack project on CurseForge.
4. In the GitHub repository settings, add the variable `CF_PROJECT_ID` (the project ID) and the secret `CF_API_TOKEN` (an API token from your CurseForge account settings). Without them, the publish job builds and uploads nothing.
5. Set `version` in `pack.toml`, commit, then `git tag v<version>` and push the tag.

## Quests

Quests are written in `quests/chapters/` (main line) and `quests/side/` (side chapters), one TOML file per chapter; the format is described at the top of `tools/questgen/model.py`. The build turns them into `config/ftbquests/quests/` (commit the result). Never edit the generated files or use the in-game editor on them: quest IDs come from the slugs, so renaming a slug resets that quest's progress. The story the texts follow is in [`docs/story.md`](docs/story.md); recipe changes are listed in [`docs/gates.md`](docs/gates.md).

## Working on the pack

```powershell
packwiz curseforge add <slug>   # add a mod (then add it to docs/mods.md)
packwiz update <slug>           # update a mod
packwiz remove <slug>
```

Configs live in `config/` and `defaultconfigs/`, scripts in `kubejs/`. Everything that is not listed in `.packwizignore` ends up in the pack.
