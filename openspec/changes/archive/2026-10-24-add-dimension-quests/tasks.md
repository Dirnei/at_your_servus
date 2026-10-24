# Tasks

## 1. Branches

- [x] 1.1 Rewrite the dimension entry quests in `quests/side/01-exploration.toml` per design: `twilight` (advancement `twilightforest:root`), `undergarden` (catalyst and `undergarden:undergarden/enter_undergarden`), `bumblezone` (bee bread); verify every advancement ID exists under `data/<ns>/advancement/` in its jar
- [x] 1.2 Add the Twilight Forest branch: `naga`, `lich`, `minoshroom`, `hydra`, `knights`, `ur-ghast` with trophies, and optional `ironwood`, `steeleaf`, `fiery`, `yeti`, `snow-queen`
- [x] 1.3 Add the Undergarden branch: `cloggrum` (ingot and the cloggrum helmet), `froststeel`, `utherium`, `forgotten-guardian` (advancement `undergarden:undergarden/kill_forgotten_guardian`), `forgotten`, and optional `regalium`
- [x] 1.4 Add the Bumblezone branch: `honey-compass`, `stinger-spear`, `essence`, and optional `royal-jelly`
- [x] 1.5 Add the End branch: `end` (deps `nether:blaze`, advancement `minecraft:story/enter_the_end`), `dragon` (`minecraft:end/kill_dragon`), `end-city` (`minecraft:end/find_end_city`), `elytra` (item)

## 2. Checks

- [x] 2.1 Run `python -m tools.questgen.generate`; verify `python -m pytest`, `python -m tools.checks.quest_check --quests quests --mods build/server/mods` and `packwiz refresh` pass, `python -m tools.questx` reports no findings, and `grep -rn 'exploration:' quests/chapters` finds nothing
- [ ] 2.2 Manual, on the test server: open the quest book and see the four branches without overlapping quests; enter the Twilight Forest and the Undergarden and see their entry quests complete; check that `exploration:twilight` stays complete for a player who had it

## Workflow follow-up

- One commit, for example `feat: add dimension quest lines to Exploration and Dimensions`.
- Archive the change after the manual test.
