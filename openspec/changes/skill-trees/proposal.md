## Why

Players asked for a skill tree like the one in FTB Evolution (GitHub issue #1): start with a small Ultimine range and earn upgrades to it, damage, walking speed and similar. The pack has no character progression of its own; Ultimine is fully open at 64 blocks from the first minute.

## What Changes

- Add Pufferfish's Skills (CurseForge, `puffish_skills`), opened with K, with three skill trees shipped in `config/puffish_skills/`:
  - **Miner** (mining): Ultimine block limit, mining speed and related skills.
  - **Hunter** (combat): attack damage, health, crit and life steal (Apothic Attributes).
  - **Wanderer** (travel): walk speed, swim speed, step height, safe fall distance.
- **BREAKING** for existing worlds: FTB Ultimine's `max_blocks` drops from 64 to 8. Four Miner skills raise it through the `ftbultimine:max_blocks_modifier` attribute to 16, 32, 64 and 128. Players of existing worlds start at 8 until they earn the skills back. Recorded in `docs/gates.md` and the changelog.
- Points come from two sources:
  - Doing the tree's activity: each tree has its own experience (Miner from mining with the correct tool, Hunter from kills, Wanderer from walking and swimming) with anti-farming limits; each level gives a point.
  - Story quests: a new `skill_points` reward in the quest sources (`{ type = "skill_points", tree = "miner", amount = 1 }`), generated as an FTB Quests command reward. About 8 to 10 main-line quests give one, in letters from Uncle Vinzenz.
- The quest check fails on a `skill_points` reward naming an unknown tree or a non-positive amount; the quest explorer shows the reward.
- Nothing is lost on death: skills, points and experience stay.

## Capabilities

### New Capabilities
- `skill-trees`: the skill mod, the three trees, how points are earned, and the Ultimine limit tied to the Miner tree.

### Modified Capabilities
- `quest-line`: quests can reward skill points for a named tree, and the quest check validates those rewards.

## Impact

- New mod `mods/puffish-skills.pw.toml`, row in `docs/mods.md`, possibly `REQUIRED_SLUGS` in `tools/checks/pack_check.py`.
- New config `config/puffish_skills/` (config, category, definitions, skills, connections, experience per tree); `config/ftbultimine-server.json5` (`max_blocks`).
- `tools/questgen/generate.py`, `tools/questgen/model.py` docs, `tools/questgen/FORMAT.md`, `tools/checks/quest_check.py`, `tools/questx/page.py`, and their tests.
- `quests/chapters/*.toml` (skill point rewards and texts) and the generated `config/ftbquests/quests/`.
- `docs/gates.md` (Ultimine limit), `docs/story.md` if the letters need a note, changelog.
