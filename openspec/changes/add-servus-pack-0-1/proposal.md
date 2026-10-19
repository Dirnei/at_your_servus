# Proposal

## Why

The Servus mods (Foundation, Alchemy, Shuttles) need a public pack that shows them off: a kitchen-sink pack for Minecraft 26.1.2 on NeoForge, where Servus is the main path and a guided quest line with a story leads players through it. Today there is only a hand-made CurseForge export (`Servus-0.1.0.zip`) with QoL and building mods, no quests and no reproducible build. The full design was agreed on 2026-10-19 in `docs/superpowers/specs/2026-10-19-servus-modpack-design.md`.

## What Changes

- This folder becomes the pack's source: a git repository managed with packwiz, seeded from the configs and mods of `Servus-0.1.0.zip`.
- The mod list grows into a kitchen-sink pack around the Servus mods: Powah for mid/late power, Iron Jetpacks for mid-game flight, Re:Avaritia as the endgame capstone, Just Dire Things for Nether preparation, Occultism, Apotheosis, mob farm mods, exploration, QoL and performance mods. Mods that compete with Servus (AE2, Refined Storage, Mystical Agriculture, Productive Bees, Replication, Ender IO, Oritech) are kept out.
- Servus: Alchemy comes from its GitHub release until it is visible on CurseForge.
- An FTB Quests line with eight story chapters (the great-uncle's letters, "Servus, ...") plus optional side chapters, generated from text sources so quest IDs stay stable and texts are translatable.
- KubeJS recipe gates: upper Iron Jetpacks tiers need Servus materials, and the Avaritia capstone needs Alchemy's Rubedo products. Cobblegen Galore and Just Dire Things are tuned so they don't replace Alchemy.
- A build that produces the CurseForge client zip and a server pack without client-only mods.
- A Docker test server in this repo that runs the built server pack, plus a smoke check.
- A GitHub Actions workflow that builds the pack and, once a CurseForge project exists, uploads client and server pack on tag.

## Capabilities

### New Capabilities
- `mod-selection`: which mods the pack contains or excludes, where each comes from, and which side (client, server, both) each runs on.
- `pack-build`: producing versioned client and server pack artifacts from the repository, and guarding the public export.
- `quest-line`: the story frame, the chapter structure, quest rules, and how quest files are generated from sources.
- `progression-gates`: recipe and config changes that tie other mods' progression to the Servus mods and protect Alchemy's role.
- `test-server`: running the built server pack in Docker and checking that it starts cleanly.
- `release-publishing`: building in CI and uploading releases to CurseForge.

### Modified Capabilities
(none, there are no existing specs)

## Impact

- New files in this repository: packwiz metadata (`pack.toml`, `index.toml`, `mods/*.pw.toml`), `config/`, `kubejs/`, quest sources and generated `config/ftbquests/quests/`, `tools/` build and check scripts, `server/` Docker setup, `.github/workflows/`.
- New tooling dependencies: packwiz (Go), packwiz-installer-bootstrap (Java), Python 3 for the quest generator and checks, Docker for the test server.
- External: the first public CurseForge upload waits until Servus: Alchemy is visible on CurseForge. The mod repo's own playtest flow (`servus_mc_mods/server`) is not changed by this change.
