# Tasks

## 1. Mod

- [x] 1.1 `packwiz curseforge add ftb-essentials` (FTB Essentials Neoforge 26.1.2.5), keep `side = "both"`, and check that `index.toml` gains no new library besides FTB Library; add an `ftb-essentials` row to "Utility and building" in `docs/mods.md` ("Homes, op-set warps, /back, /tpa"); verify `python -m tools.checks.pack_check --public` and `python -m pytest` pass

## 2. Config

- [x] 2.1 Start the local server once (`docker compose up -d`) and copy the generated `config/ftbessentials.json5` from `server/local-data/` into the repo's `config/`. Check that the file's location and format match design.md, and set `teleportation.rtp.enabled` to `false`; add a row to "Config changes" in `docs/gates.md` (`/rtp` off: it ignores FTB Chunks claims); run `packwiz refresh`; verify `docker compose restart mc` starts cleanly, the server log shows FTB Essentials loaded, and `python -m pytest` passes
- [x] 2.2 In `config/waystones-common.toml` `[rules]`, set `enableXpCosts = false`, `enableDurability = false` and `defaultVisibility = "GLOBAL"`, and change nothing else; add three rows to "Config changes" in `docs/gates.md` (no XP cost and no warp stone wear: travel is QoL, not a cost; global visibility: friends share one network); run `packwiz refresh`; verify `docker compose restart mc` starts cleanly and `python -m pytest` passes
- [x] 2.3 Add `tests/test_ftbessentials_config.py`: it reads `config/ftbessentials.json5` and fails unless `teleportation.rtp.enabled` is `false`, so a mod update that restores the default is caught; verify the test passes, and fails when the value is set to `true`

## 3. Integration

- [x] 3.1 Manual, as a client that has joined the local server with op: `/setwarp town` works; as a non-op player, `/setwarp` is refused, `/warp town` works, a second `/sethome` with another name is refused, `/rtp` is unknown or refused, and `/back` after a death returns to the grave
- [ ] 3.2 Manual, with two players on a fresh world: player A places a waystone; player B, who never visited it, sees it in another waystone's menu and teleports there without losing XP; a teleport to another dimension costs no XP either; a warp stone keeps its durability after use; also find a village waystone with one player and note in `docs/gates.md` whether the other player sees it before or only after it is found

## Workflow follow-up

- Archive `add-servus-pack-0-1` before this change, because this change adds to its `mod-selection` spec.
- Archive this change after the manual check passes.
