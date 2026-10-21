# Development

How the pack is built, tested and released. The pack's contents are in [`mods.md`](mods.md), the story in [`story.md`](story.md), recipe changes in [`gates.md`](gates.md).

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
.\tools\build.ps1 -Version 0.1.0-alpha   # name the build like a release (default: dev)
python -m pytest            # tests for the checks and the quest generator
```

The build writes to `dist/`:

| File | For |
|---|---|
| `at-your-servus-<version>.zip` | CurseForge app import (client) |
| `at-your-servus-<version>-server.zip` | dedicated servers: run `start.sh` or `start.ps1` (installs NeoForge 26.1.2.122 on first run, needs Java 25) |
| `at-your-servus-latest-server.zip` | the same server pack, picked up by the test server |

A playtest build carries mods that are not on CurseForge (none at the moment) inside the client zip's `overrides/mods`. Such a zip must not be uploaded to CurseForge; the build warns about it, and `-Public` refuses to build.

If a mod's author blocks third-party downloads, the server pack build stops and names the mod and its download page.

## Local server

For quick testing on this machine, `docker-compose.yml` in the repo root runs a server straight from the working tree, with no build. An nginx container serves the repo, and the server installs the pack with packwiz on every start.

```powershell
docker compose up -d
docker compose logs -f mc              # wait for "Done", then connect to localhost:25567
```

After changing mods or configs: `packwiz refresh`, then `docker compose restart mc`. The world lives in `server/local-data`; delete it for a fresh world. Set `LOCAL_PORT`, `MEMORY` or `OPS` in the environment or a root `.env` to change them.

**Dev client:** to test the working tree on a client without building and importing the zip, use a dev profile. Once: in the CurseForge app, Create Custom Profile, name it `At Your Servus (dev)`, Minecraft 26.1.2, NeoForge 26.1.2.122, and leave it empty. Then, after each change:

```powershell
.\tools\client-sync.ps1                # installs the client side of the working tree into the dev profile
docker compose restart mc              # if mods or configs changed
```

Start the profile in the CurseForge app and join `localhost:25567`. After the first join, the profile page in the CurseForge app lists the server under recently played; starting from that entry joins it directly. Only changed files are downloaded, and files the pack dropped are removed. `-Instance <folder>` syncs into another profile folder. The script warns if the profile's Minecraft or NeoForge version differs from `pack.toml`.

## Test server

The test server runs the latest built server pack in Docker (`itzg/minecraft-server:java25`). The world lives in `server/data` and survives restarts.

```powershell
copy server\.env.example server\.env   # once: set OPS, WHITELIST, MEMORY
.\tools\build.ps1
cd server; docker compose up -d
docker compose logs -f                 # wait for "Done"
```

After a new build: `docker compose restart` in `server/`; the new server pack is applied on start. Friends need the client zip of the same build, or they cannot join.

**Friends:** in the CurseForge app, Create Custom Profile, Import, pick `at-your-servus-<version>.zip`. Give the profile at least 6 GB of memory, start it, Multiplayer, add the server (LAN IP, or a forwarded port 25565 / Tailscale from elsewhere).

**Smoke check:** `.\tools\smoke.ps1` starts the server pack in a throwaway world on port 25566, waits for it to be ready (at most 10 minutes), fails on a crash or on FTB Quests/KubeJS errors, and stops it again. Your playtest world is not touched.

## Releases

GitHub Actions builds every push (`.github/workflows/build.yml`): tests, both packs, and a check that the committed quest book matches `quests/`. The packs are kept as build artifacts.

The version lives only in the release tag; `pack.toml` always says `dev`, and local builds are named `at-your-servus-dev.zip`. A tag `v<major>.<minor>.<patch>` (optionally `-alpha` or `-beta`, e.g. `v0.1.0-alpha`) runs `.github/workflows/publish.yml`: it runs a public build with that version (`build.ps1 -Public -Version 0.1.0-alpha`) and uploads the client zip and its server pack to CurseForge. `-alpha` and `-beta` tags are uploaded as alpha and beta.

**Changelog:** CurseForge shows the version's section of [`CHANGELOG.md`](../CHANGELOG.md) as the changelog of the client file. Commits are conventional commits, one line of at most 74 characters (`feat: ...`, `fix: ...`, `chore(tools): ...`). Mod updates are `chore(deps): ...`, because the changelog lists them under Mods anyway; adding a mod is a `feat`. CI runs `python -m tools.checks.commit_check` on every commit since the last `v*` tag. For a release:

```powershell
python -m tools.changelog 0.2.0-alpha   # drafts the ## 0.2.0-alpha section at the top of CHANGELOG.md
python -m tools.publish --tag v0.2.0-alpha --check   # passes once the section exists
```

The draft has `feat` commits under New, `fix` under Fixes, `perf` under Performance (other types such as `chore` are left out), and under Mods every mod and shader pack added, removed or updated since the previous tag. Edit it into text for players, commit it, then tag that commit. A tag without a section for its version fails before the build and uploads nothing. So does a tag whose commits since the previous tag break the commit format (`commit_check --release <tag>`), or whose tests or quest book check fail.

First public release:

1. `.\tools\build.ps1 -Public` must pass locally.
2. Create the modpack project on CurseForge.
3. In the GitHub repository settings, add the variable `CF_PROJECT_ID` (the project ID) and the secret `CF_API_TOKEN` (an API token from your CurseForge account settings). Without them, the publish job builds and uploads nothing.
4. `git tag v0.1.0-alpha` and push the tag. No file needs a version change.

## Quests

Quests are written in `quests/chapters/` (main line) and `quests/side/` (side chapters), one TOML file per chapter; the format is described at the top of `tools/questgen/model.py`. The build turns them into `config/ftbquests/quests/` (commit the result). Never edit the generated files or use the in-game editor on them: quest IDs come from the slugs, so renaming a slug resets that quest's progress. The story the texts follow is in [`docs/story.md`](docs/story.md); recipe changes are listed in [`docs/gates.md`](docs/gates.md).

To look at the quest line without Minecraft, build the quest explorer after a server pack build:

```powershell
python -m tools.questx      # writes build/quest-explorer/index.html, open it in a browser
```

It reads `quests/` and the jars in `build/server/mods/`, and downloads the Minecraft client jar once into `build/minecraft/` for the vanilla icons. It prints its findings (a task already covered by earlier rewards, two quests on one spot, a main quest behind a side quest) as `chapter:slug: ...` lines, and the page shows them as badges. It never changes the sources; rerun it after editing a quest.

## Working on the pack

```powershell
packwiz curseforge add <slug>   # add a mod (then add it to docs/mods.md)
packwiz update <slug>           # update a mod
packwiz remove <slug>
```

Configs live in `config/` and `defaultconfigs/`, scripts in `kubejs/`. Everything that is not listed in `.packwizignore` ends up in the pack.
