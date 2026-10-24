# Proposal

## Why

Macaw's Furniture is the only furniture mod in the pack. Players who build a farmhouse, a trading house or Vinzenz's study want more styles and furniture that holds things, and three furniture mods now have 26.1.2 NeoForge builds on CurseForge.

## What Changes

- Add Adorn: sofas, chairs, tables, kitchen counters in vanilla style.
- Add Bibliocraft Legacy: bookcases, shelves, tool racks, display cases, a clipboard; furniture that holds and shows items.
- Add Fantasy's Furniture: whole furniture sets in several styles, decoration only.
- Add any library these mods need.
- No quests: the mods are there for building, and the Building side chapter stays as it is.
- One `feat` commit per mod, each with its libraries, so the changelog gets one entry per mod.

## Capabilities

### New Capabilities

### Modified Capabilities
- `mod-selection`: the gap-filling mod set gains a requirement for more furniture mods.

## Impact

- `mods/`: three metafiles plus library metafiles; `index.toml` and `pack.toml` refreshed.
- `docs/mods.md`: rows for each new mod and library.
- Client and server packs both grow: all three mods add blocks, so they run on both sides.
- No change to quests, KubeJS or `docs/gates.md`.
