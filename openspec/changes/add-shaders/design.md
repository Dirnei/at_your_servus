# Design

## Context

See `proposal.md` for the why and `specs/mod-selection/spec.md` for the requirements.

Current state:
- `tools/checks/pack_check.py` loads only `mods/*.pw.toml`. Iris is excluded by slug (`EXCLUDED_SLUGS`), and `tests/test_pack_check.py` has a test that Iris fails the check. `test_every_metafile_is_documented` compares `mods/` with the backticked rows in `docs/mods.md`.
- The pack has no `shaderpacks/` folder yet.
- On CurseForge (checked 2026-10-20): Iris 1.11.4 for NeoForge 26.1.2 (release, 2026-09-13), whose only required dependency is Sodium; Complementary Reimagined r5.9.3 (2026-09-15), listed for 26.1.2. The pack has Sodium 0.9.2 (`sodium-neoforge-0.9.2+mc26.1.2.jar`).
- The `mod-selection` spec exists only as a delta in the unarchived change `add-servus-pack-0-1`; `openspec/specs/` has no `mod-selection` yet.

## Goals / Non-Goals

**Goals:**
- Shaders work for players who want them, and nothing changes for players who don't.
- The checks treat shader packs like mods: client only, from CurseForge for a public build, documented.

**Non-Goals:**
- No second shader pack, and no tuned shader settings.
- No changes to how the server pack is built: `side = "client"` already keeps both new files out of it.

## Decisions

### D1: Off by default through no config, not through a shipped `iris.properties`
Iris with no selected shader pack renders the normal game. The pack ships only the shader pack file, so nothing is selected until the player picks it.
- Alternative: ship `config/iris.properties` with `shaderPack=...` and `enableShaders=false`. Rejected: the CurseForge app overwrites the pack's config files on update, so a player who turned shaders on would find them off again after every update.

### D2: Shader pack from CurseForge through packwiz
`packwiz curseforge add complementary-reimagined --meta-folder shaderpacks` writes `shaderpacks/complementary-reimagined.pw.toml` (`--category shaders` does not pick the folder: packwiz writes the metafile to the repo root). The export then lists it in the manifest like a mod, and the CurseForge app downloads it into `shaderpacks/`. Its `side` is set to `client` if packwiz writes `both`.
- Alternative: ship the shader zip in `overrides/shaderpacks/`. Rejected: the license only allows the official download, and the public build refuses files that don't come from CurseForge.

### D3: pack_check reads `shaderpacks/` too
`load_metafiles` is called for `mods/` and `shaderpacks/` and the results are merged, so the public-source check and the docs test cover shader packs without new rules. A new rule makes every metafile from `shaderpacks/` fail unless `side = "client"`. `irisshaders` joins `CLIENT_ONLY_SLUGS`, and `EXCLUDED_SLUGS` goes away (Iris was its only entry).
- Alternative: leave the checks alone for shader packs. Rejected: a shader pack marked `both` would end up in the server pack, and a non-CurseForge one would slip past the public guard.

### D4: Docs
`docs/mods.md` gets an `irisshaders` row under "QoL and performance" and a new "Shader packs" table with a `complementary-reimagined` row. Iris leaves the "Excluded on purpose" row ("Iris, SecurityCraft" becomes "SecurityCraft"). The changes don't touch another mod's recipes or config, so `docs/gates.md` stays as it is.

## Risks / Trade-offs

- [Iris 1.11.4 may want a newer Sodium than 0.9.2] → Check the Iris jar's `neoforge.mods.toml` dependency range, or watch the first client start; if it's too old, update Sodium with `packwiz update sodium` in the same change.
- [Modded rendering looks wrong with shaders: Servus blocks with custom renderers, Jade overlay, FTB Chunks map] → A manual client test with Complementary on. Small glitches are noted in `docs/mods.md`; anything that breaks play blocks the change.
- [Archive order: this change modifies `mod-selection`, which only exists once `add-servus-pack-0-1` is archived] → Archive `add-servus-pack-0-1` first.
- [Slower client start and more memory use] → None needed; it's small next to the 6 GB the docs recommend, and it only applies to players who turn shaders on.

## Migration Plan

Ships with the next tagged release. Existing profiles get Iris and the shader pack on update, with shaders still off. Rollback: remove the two metafiles and run `packwiz refresh`.
