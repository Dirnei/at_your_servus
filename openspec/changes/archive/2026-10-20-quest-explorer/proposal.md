# Proposal

## Why

Today, seeing the quest line means starting Minecraft and opening the quest book. That is slow, and it hides problems like the arrival bread reward that completed the "Something to Eat" quest on its own. A read-only view of the quest book, built from the sources, lets us look at the quests and think about them without starting the game. Edits stay in the TOML, made in conversation.

## What Changes

- New command `python -m tools.questx` that reads `quests/*.toml` and the server pack's jars and writes a static explorer to `build/quest-explorer/` (`index.html` plus icons). It opens from disk; it needs no server and no Minecraft.
- The explorer lists the chapters on the left, grouped like the quest book, quests placed by their x/y, dependency arrows, markers for dependencies from other chapters, item icons and English item names, and a popup per quest, as in-game (letter, tasks, rewards, reference `chapter:slug`).
- The explorer computes quest-line findings and shows them as badges: a task already covered by earlier rewards (auto-complete), partly covered tasks, two quests on one position, and main quests depending on side quests. The same findings are printed as text with `chapter:slug` references.
- Vanilla textures come from Mojang's client jar for the pack's Minecraft version, downloaded once and cached under `build/`.
- The explorer never writes to `quests/`, `config/` or any other tracked file.

## Capabilities

### New Capabilities
- `quest-explorer`: a read-only, offline view of the quest line built from the quest sources and the pack's jars, with icons and quest-line findings.

### Modified Capabilities

## Impact

- New code: `tools/questx/` (loader reuse from `tools/questgen/model.py`, icon extraction, HTML writer), tests in `tests/`.
- Reads `build/server/mods/*.jar` (from `build.ps1`) and downloads the Minecraft client jar from `piston-meta.mojang.com` into `build/` once.
- Standard library only; no new Python dependencies. Output lives in `build/` (git-ignored) and is not part of either pack.
- `docs/development.md` gets a short section on the command.
