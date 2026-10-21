# Tasks

## 1. Pack check covers shader packs

- [x] 1.1 In `tools/checks/pack_check.py`, load metafiles from `mods/` and `shaderpacks/`, fail any `shaderpacks/` metafile that isn't `side = "client"`, add `irisshaders` to `CLIENT_ONLY_SLUGS` and drop `EXCLUDED_SLUGS`; in `tests/test_pack_check.py`, replace the Iris exclusion test with a test that a shader pack marked `both` fails and is named, and make the docs test read `shaderpacks/` too; verify `python -m pytest tests/test_pack_check.py` passes

## 2. Iris

- [x] 2.1 `packwiz curseforge add irisshaders` (Iris 1.11.4 for NeoForge 26.1.2), set `side = "client"`; check the dependency range for Sodium in the jar's `META-INF/neoforge.mods.toml` and run `packwiz update sodium` if 0.9.2 is outside it; add the `irisshaders` row under "QoL and performance" in `docs/mods.md` and change "Iris, SecurityCraft" under "Excluded on purpose" to "SecurityCraft"; verify `python -m tools.checks.pack_check --public` and `python -m pytest` pass

## 3. Shader pack

- [x] 3.1 `packwiz curseforge add complementary-reimagined --meta-folder shaderpacks`, set `side = "client"` in `shaderpacks/complementary-reimagined.pw.toml`, add no `config/iris.properties`; add a "Shader packs" table with a `complementary-reimagined` row to `docs/mods.md`; run `packwiz refresh`; verify `python -m tools.checks.pack_check --public` and `python -m pytest` pass

## 4. Integration

- [x] 4.1 Run `.\tools\build.ps1 -Public`; verify it passes, the client zip's `manifest.json` lists Iris and Complementary Reimagined, and `build/server/` contains neither `iris` in `mods/` nor a `shaderpacks/` folder
- [x] 4.2 Manual: import the client zip in the CurseForge app and start it; verify the game starts with Iris loaded, no shader pack active, and Complementary Reimagined listed under Video Settings > Shader Packs
- [x] 4.3 Manual: turn Complementary Reimagined on and join the test server; verify Servus blocks (Shuttles, Alchemy, Foundation), the Jade overlay and the FTB Chunks map render usably, and note any glitches in `docs/mods.md`

## Workflow follow-up

- Archive `add-servus-pack-0-1` before this change, because this change modifies its `mod-selection` spec.
- Archive this change after the manual checks pass.
