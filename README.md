# At Your Servus

A kitchen-sink pack built around the Servus mods, for Minecraft 26.1.2 on NeoForge. A guided FTB Quests line tells the story of a great-uncle's estate in Tyrol and leads through the Servus mods first.

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

## Working on the pack

```powershell
packwiz curseforge add <slug>   # add a mod (then add it to docs/mods.md)
packwiz update <slug>           # update a mod
packwiz remove <slug>
```

Configs live in `config/` and `defaultconfigs/`, scripts in `kubejs/`. Everything that is not listed in `.packwizignore` ends up in the pack.
