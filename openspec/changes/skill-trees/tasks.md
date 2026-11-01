# Tasks

## 1. Add the mod

- [x] 1.1 Check the CurseForge relations of Pufferfish's Skills for required dependencies, then `packwiz curseforge add puffish-skills` (and any required dependency) with side `both`; verify `mods/puffish-skills.pw.toml` points at a CurseForge 26.1 NeoForge file and `python -m tools.checks.pack_check` passes
- [x] 1.2 Add a row for each new mod to `docs/mods.md` and add `puffish-skills` to `REQUIRED_SLUGS` in `tools/checks/pack_check.py`; verify `python -m pytest` passes (the mods.md test)

## 2. Skill trees

- [x] 2.1 Write `config/puffish_skills/config.json` (version 3, `show_warnings: true`, categories `miner`, `hunter`, `wanderer`) and one `category.json` per tree with title, description, icon and background; verify the server log after `docker compose restart mc` shows the three categories loaded and no Pufferfish's Skills warnings
- [x] 2.2 Write the Miner tree (definitions, skills, connections) per design.md, with the four Ultimine skills adding `ftbultimine:max_blocks_modifier` +8, +16, +32, +64 in a chain; verify on the local server with `/puffish_skills skills unlock` and `/attribute @s ftbultimine:max_blocks_modifier get` that the values add up to 8, 24, 56, 120
- [x] 2.3 Write the Hunter and Wanderer trees per design.md, taking every attribute id from the jars (vanilla, Apothic Attributes); verify the server log has no unknown-attribute warnings and `/attribute` shows each unlocked bonus
- [x] 2.4 Write `experience.json` for each tree (mine_block, kill_entity with per-chunk anti-farming, walk/sprint/swim stats; level curve; no reset on death); verify on the local server that mining raises only Miner experience, walking only Wanderer, and kills only Hunter, using the skill screen or `/puffish_skills experience`
- [x] 2.5 Set `max_blocks: 8` in `config/ftbultimine-server.json5`, add the Ultimine limit and its reason to `docs/gates.md`; verify `packwiz refresh` lists the new config files and the docs test passes

- [x] 2.6 Add Default Options (client) with `config/defaultoptions/keybindings.txt` so K only opens the skill tree on new installs (Iris shader toggle unbound), with rows in `docs/mods.md` and `docs/gates.md`; verify in a fresh client profile that no other binding is on plain K and that a profile with saved keys keeps them

## 3. Skill point rewards in the quest tools

- [x] 3.1 Add the `skill_points` reward (`tree`, `amount`) to `_reward` in `tools/questgen/generate.py`, emitting a silent command reward with `permission_level: 2` and a feedback message naming the tree; document it in `tools/questgen/model.py` and `tools/questgen/FORMAT.md`; verify with a new test in `tests/test_generate.py` that checks the generated reward and `test_rerun_is_byte_identical`
- [x] 3.2 Check in the FTB Quests jar whether `feedback_message` is read inline or from the lang file, and move it to the chapter lang file if needed; verify by claiming a generated reward on the local server and seeing the message
- [x] 3.3 In `tools/checks/quest_check.py`, read valid tree ids from `config/puffish_skills/config.json` and fail on an unknown tree or a non-positive amount, naming the quest; verify with tests for an unknown tree, a zero amount and a valid reward in `tests/test_quest_check.py`
- [x] 3.4 Show `skill_points` rewards in the quest explorer (`tools/questx/page.py`) as "<amount> <Tree> point(s)"; verify with a questx test or by opening the rebuilt explorer

## 4. Story points

- [x] 4.1 Add `skill_points` rewards to 8 to 10 existing main-line quests per design.md (each tree at least one, Miner first in Arrival), with a sentence from Uncle Vinzenz where it fits (`docs/story.md` style); no slug changes; verify `python -m tools.questgen.generate`, the quest check against the server mods and `python -m pytest` pass

## 5. In-game check

- [ ] 5.1 Rebuild the server pack, `docker compose restart mc`, join with a client: K opens the skill screen with three tabs, a new player ultimines 8 blocks of a larger vein, and the Ultimine preview on the client shows 8 too
- [x] 5.2 In the same session: claim a story point reward and see the message and the point, unlock the first two Ultimine skills and ultimine 32 blocks, die and respawn with the skills kept
- [ ] 5.3 Add a changelog note for the release that existing worlds start at 8 Ultimine blocks and earn the rest back with Miner skills; verify it appears in the drafted `CHANGELOG.md` section

## Workflow follow-up

- Close GitHub issue #1 with a short note once the release with the skill trees is out.
- Archive the change after the in-game check.
