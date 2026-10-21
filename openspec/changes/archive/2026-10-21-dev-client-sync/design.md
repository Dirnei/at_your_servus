# Design

## Context

`tools/build.ps1` already installs the server side of the pack with `packwiz serve` and `packwiz-installer-bootstrap.jar -g -s server`. A CurseForge profile folder (`%USERPROFILE%\curseforge\minecraft\Instances\<name>`) is the game folder itself (`mods/`, `config/`, ...), and its `minecraftinstance.json` holds `gameVersion` and `baseModLoader.name` (e.g. `neoforge-26.1.2.122`).

## Goals / Non-Goals

**Goals:**
- One command brings a dev profile to the state of the working tree.

**Non-Goals:**
- Launching the game, logging in, or turning shaders on. The player starts the profile in the CurseForge app.
- Creating the profile. The CurseForge app does that once, and it installs Minecraft and NeoForge.

## Decisions

- **packwiz-installer with `-s client`, the same tool the server pack uses.** It honours `side`, downloads only what changed and keeps a `packwiz.json` in the target folder, from which it removes files the pack no longer lists. Alternative: build the client zip and unpack its overrides plus the manifest's files ourselves. Rejected: it would need the CurseForge API for the downloads.
- **A separate, empty custom profile.** The CurseForge app tracks the addons of profiles made from a modpack and may restore or remove files there. An empty custom profile has no addons it tracks, so it leaves the synced files alone.
- **Port.** `packwiz serve` runs on its own port (28418), so the script can run while `build.ps1` uses 28417.
- **Version check, not version fix.** The script compares `minecraftinstance.json` with `pack.toml` and warns. Changing the loader of a profile is the CurseForge app's job.

## Risks / Trade-offs

- [Files added by hand to the dev profile stay, and so do files from before the first sync] → Start from an empty profile, as the docs say.
- [packwiz-installer asks about optional mods] → `-g` runs it without a window; the pack has no optional mods.
