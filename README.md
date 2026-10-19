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

## Working on the pack

```powershell
packwiz curseforge add <slug>   # add a mod (then add it to docs/mods.md)
packwiz update <slug>           # update a mod
packwiz remove <slug>
```

Configs live in `config/` and `defaultconfigs/`, scripts in `kubejs/`. Everything that is not listed in `.packwizignore` ends up in the pack.
