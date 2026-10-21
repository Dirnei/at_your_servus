# Proposal

## Why

Players asked for shaders. Iris was left out of 0.1.0 only to keep the first release small, and Iris now has a release build for NeoForge 26.1.2 on CurseForge. Shaders cost a lot of frame rate, so they must stay off for players who don't want them, such as friends on weaker PCs.

## What Changes

- Add Iris (NeoForge 26.1.2, client only) from CurseForge. Sodium, which Iris needs, is already in the pack.
- Add the Complementary Reimagined shader pack from CurseForge to `shaderpacks/`, client only.
- Shaders are off by default: the pack ships no Iris config, so no shader pack is selected until the player picks one under Video Settings > Shader Packs. Pack updates never reset that choice.
- Iris is no longer an excluded mod: it leaves the pack check's exclusion list and the "Excluded on purpose" table in `docs/mods.md`.
- The pack check and the mod list test also cover `shaderpacks/`: shader packs must be client only, come from CurseForge for a public build, and have a row in `docs/mods.md`.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `mod-selection`: Iris leaves the excluded list; Iris and shader packs are client only; a new requirement that the pack ships a shader pack, off by default. This capability is still defined by the unarchived change `add-servus-pack-0-1`.

## Impact

- `mods/iris.pw.toml` (new), `shaderpacks/complementary-reimagined.pw.toml` (new), `index.toml`.
- `tools/checks/pack_check.py` and `tests/test_pack_check.py`.
- `docs/mods.md`.
- Client zip only: the server pack is unchanged.
- Possibly `mods/sodium.pw.toml`, if Iris 1.11.4 needs a newer Sodium than 0.9.2.
