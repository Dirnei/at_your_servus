# Proposal

## Why

Playtesting turned up quest bugs and missing mods. The Works chapter asks for a chimney the Coal Generator doesn't need, and it ends on a Storage Terminal that can't work yet: the terminal reaches the warehouse over the data cable and through a Packing Station, and both are only taught in The Trading House. Every quest text with "Huber & Co." fails in FTB Quests with "Invalid formatting! you must escape whitespace after & with \&!". Players also missed a reward for eating different foods, the Feral Flare Lantern, Entangled blocks and a light level overlay on F7, and asked for Complementary Unbound with Euphoria Patches next to Complementary Reimagined.

## What Changes

- The quest generator escapes `&` in every text it writes to the lang files, so "Huber & Co." shows as written.
- `old-works:coal-generator` no longer asks for `servus_foundation:chimney` (the Coal Generator has its own chimney; the chimney block belongs to the Sink), and its text drops the chimney line.
- The Works teach the data line before the terminal: controller, then Data Cable, then Packing Station, then Storage Terminal. The `data-cable` and `packing` quests of The Trading House move to The Works as `old-works:data-cable` and `old-works:packing-station`. **BREAKING** for saves: players lose the progress of those two quests (new IDs); the pack is alpha.
- Add Spice of Life: Carrot Edition (extra hearts for eating different foods), Torchmaster Version Locked (Feral Flare Lantern, Megatorch, Dread Lamp), Entangled, and Lighty (light level overlay on F7, client only), all from CurseForge.
- Add the Complementary Unbound shader pack next to Complementary Reimagined, and Euphoria Patches (client only), which writes patched copies of both shader packs at game start. Shaders stay off by default.
- The pack check fails when the Euphoria Patches file and a Complementary shader pack are built for different Complementary versions.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `quest-line`: the Early warehouse requirement adds the Data Cable and Packing Station; The Trading House no longer teaches the data cable; a new requirement that quest texts show `&` as written.
- `mod-selection`: shaders requirement covers Complementary Unbound and Euphoria Patches with matching versions; Lighty and Euphoria Patches join the client-only mods; a new requirement for the playtest gap fillers (food variety hearts, Feral Flare Lantern, Entangled, light overlay).

## Impact

- `tools/questgen/generate.py`, `tests/test_generate.py`; regenerated `config/ftbquests/quests/`.
- `quests/chapters/02-old-works.toml`, `quests/chapters/06-trading-house.toml`.
- New metafiles: `mods/spice-of-life-carrot-edition.pw.toml`, `mods/torchmaster-version-locked.pw.toml`, `mods/entangled.pw.toml`, `mods/lighty.pw.toml`, `mods/euphoria-patches.pw.toml`, `shaderpacks/complementary-unbound.pw.toml`; `index.toml`.
- `tools/checks/pack_check.py`, `tests/test_pack_check.py`.
- `docs/mods.md`; `docs/gates.md` only if the Megatorch needs a config change.
- Should be archived before `add-fields-and-side-quests`, which builds on the same quest-line requirements.
