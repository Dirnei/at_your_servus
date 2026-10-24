# Proposal

## Why

Players miss the usual server commands: a home to return to, fixed warps to shared places, and a way back to where they were, including their grave after a death. FTB Essentials adds them, has a NeoForge build for 26.1.2 on CurseForge, and its FTB Library is already in the pack.

## What Changes

- Add FTB Essentials (NeoForge 26.1.2.5, both sides) from CurseForge.
- Players get `/sethome`, `/home` and `/delhome` with one home each, `/warp`, `/back` and `/tpa`. These are the mod's defaults.
- Only ops can create or remove warps: `/setwarp` and `/delwarp` need permission level 2. This is built into the mod.
- `/rtp` is switched off in the shipped config, because it does not respect FTB Chunks claims yet. This is the pack's only config change to FTB Essentials and gets an entry in `docs/gates.md`.
- Waystones stay and become free and shared. Warps are for hubs that ops set up; Waystones are the players' own travel network. Teleporting costs no XP, warp stones lose no durability, and newly placed or found waystones are global: every player can travel to them without visiting them first. Both are config changes and get entries in `docs/gates.md`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `mod-selection`: a new requirement for player teleport commands (one home, op-only warps, `/back`, no `/rtp`) and one for free, shared waystones. This capability is still defined by the unarchived change `add-servus-pack-0-1`.

## Impact

- `mods/ftb-essentials.pw.toml` (new), `index.toml`.
- `config/ftbessentials.json5` (new, with `/rtp` off).
- `config/waystones-common.toml` (XP costs and durability off, global visibility).
- `docs/mods.md` and `docs/gates.md`.
- Server and client pack: the mod runs on both sides.
