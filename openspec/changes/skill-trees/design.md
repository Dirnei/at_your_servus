## Context

See proposal.md for why. Facts this design builds on, checked during exploration:

- FTB Ultimine 26.1.2.6 (in the pack) registers player attributes `ftbultimine:max_blocks_modifier`, `cooldown_modifier` and `exhaustion_modifier`. `FTBUltimineServerConfig.getMaxBlocks` returns `max(0, max_blocks + round(max_blocks_modifier))`, with the FTB Ranks node used only if FTB Ranks is installed (it is not).
- Pufferfish's Skills (CurseForge `puffish-skills`, latest 26.1 NeoForge file `puffish_skills-0.19.2-26.1-neoforge.jar`) loads trees from `config/puffish_skills/`: `config.json` (version 3, list of category ids, a-z and `_` only) plus one folder per category under `categories/<id>/` with `category.json`, `definitions.json`, `skills.json`, `connections.json` and `experience.json`. Rewards include `puffish_skills:attribute` (any attribute id, operations `addition`, `multiply_base`, `multiply_total`). Experience sources include `mine_block` (correct tool only), `kill_entity` (with `anti_farming` per chunk) and `increase_stat`. Commands: `/puffish_skills points add <player> <category> <count>`.
- FTB Quests 26.1.2.9 command rewards take `command`, `permission_level`, `silent`, `feedback_message`, and replace `{p}` with the player name (`tools/questgen/FORMAT.md` section 7).
- The quest generator supports only `item` and `xp` rewards (`tools/questgen/generate.py` `_reward`). The pack has Apothic Attributes (crit, life steal and more) and Spice of Life (extra hearts from food variety).

## Goals / Non-Goals

**Goals:**
- A working first version of the three trees that can be tuned by editing JSON only.
- One source of truth for tree ids, used by the trees and the quest check.

**Non-Goals:**
- A fourth tree (household, farming). Later change.
- Skills that are not attribute bonuses (new abilities, recipes, gated items).
- Perfect balance. Numbers below are a first pass; playtesting tunes them.

## Decisions

### Pufferfish's Skills, configured from scratch
It is what FTB Evolution uses, it has attribute rewards, and it ships no default trees, so nothing needs removing. We write our own trees rather than installing "Pufferfish's Default Skill Trees", whose mining tree knows nothing about Ultimine. Alternative: KubeJS-driven levelling, rejected as far more code for the same result.

### Ultimine limit through the attribute
`config/ftbultimine-server.json5` `max_blocks` goes from 64 to 8, and four Miner skills each add a `max_blocks_modifier` of +8, +16, +32, +64 (addition), giving 16, 32, 64, 128. No KubeJS, no FTB Ranks. Alternatives: FTB Ranks nodes (another mod, needs rank promotion glue) or a KubeJS event (more code, same effect).

### Trees in `config/puffish_skills/`, not a datapack
Datapacks live per world; the config folder ships with the pack and reaches every world and server. The files are listed in the pack index (not in `.packwizignore`). `show_warnings: true` so config mistakes appear in the server log.

### K stays with the skill tree
Iris ("Toggle Shaders") also defaults to K (Apotheosis' "Toggle Boots Attribute Bonuses" is Ctrl+K and does not clash). Default Options (CurseForge, client) ships `config/defaultoptions/keybindings.txt`: the shader toggle is unbound (Iris' shader menu on O can still switch shaders) and the skill tree keeps K. Default Options changes a key only if the player never saved that binding, so existing installs keep their keys. Alternatives: a shipped `options.txt` (overwrites every player's options on each update) or living with the clash.

### Category ids and titles
Ids `miner`, `hunter`, `wanderer`. Titles in the skill screen: "Miner", "Hunter", "Wanderer", each with a one-line description ("Mining. Ultimine reaches further."). English names, like the rest of the pack: the first draft used Bergmann and Jaeger, but English players could not read them and "Jaeger" without its umlaut looks misspelled to German players.

### First layout
Each tree starts with one root skill and branches; costs 1 point per skill, deeper skills 2.

```
BERGMANN                         JAEGER                        WANDERER
Ultimine 16 (root)               +1 attack damage (root)       +5% movement speed (root)
 +- Ultimine 32                   +- +2 max health              +- +5% movement speed
 |   +- Ultimine 64               |   +- +2 max health          |   +- +10% movement speed
 |       +- Ultimine 128 (2 pts)  +- +1 attack damage           +- swim speed / water movement
 +- +10% block break speed        |   +- +5% crit chance        +- +0.5 step height
 |   +- +10% block break speed    |       +- +5% crit damage    +- +3 safe fall distance
 +- mining efficiency             +- +3% life steal (2 pts)     +- +1 block interaction range
     (underwater: submerged
      mining speed)
```

Attribute ids are taken from the jars at implementation (vanilla `minecraft:*`, Apothic `apothic_attributes:*`); any id that does not exist fails loudly with `show_warnings`. Health stays modest (+4 total) because Spice of Life also adds hearts.

### Experience and levels
- Miner: `mine_block` (only fires when the tool can harvest the block), 1 XP for `#minecraft:base_stone_overworld` and `#minecraft:base_stone_nether`, 5 for `#c:ores`. Ultimine breaks blocks through the same break event, so ultimined blocks count too; the curve accounts for it.
- Hunter: `kill_entity`, XP = the mob's dropped XP (the mod has no max-health operation), `anti_farming_per_chunk` limit (start: 15 kills, reset after 300 s) so Apothic Spawners farms stop paying.
- Wanderer: `increase_stat` on `walk_one_cm`, `sprint_one_cm`, `swim_one_cm`, `walk_on_water_one_cm`, `walk_under_water_one_cm`, 1 XP per 10 blocks. Riding, flying and elytra do not count. The mod rounds the experience of every single stat increase, and walking adds about 20 cm per tick, so `amount / 1000` always rounds to 0. Instead each stat reads its total before the increase (`get_stat_value`) and gives `floor((total + amount) / 1000) - floor(total / 1000)`.
- `experience_per_level`: an expression that grows with the level and is capped, with a level limit that is enough to buy every skill in the tree plus spare. `reset_on_death` and `erase_on_death` off.

### `skill_points` reward in the quest sources
TOML: `{ type = "skill_points", tree = "miner", amount = 1 }`. The generator emits:

```json5
{ id: "...", type: "command",
  command: "/puffish_skills points add {p} miner 1",
  permission_level: 2, silent: true,
  feedback_message: "+1 Miner point" }
```

`feedback_message` is English text inline in the reward; if FTB Quests reads it only from lang files, move it to the chapter's lang file instead (checked at implementation). The quest check reads the valid tree ids from `config/puffish_skills/config.json` `categories`, so adding a tree needs no code change. The quest explorer lists the reward as "1 Miner point". Alternative: let quest sources write raw `command` rewards; rejected because typos in a command fail silently in game.

### Story points
About 8 to 10 rewards on existing main-line quests, no new quests and no slug changes: the iron pickaxe quest in Arrival and one or two in The Works (Miner), The Fields and The Trading House (Wanderer), Into the Nether (Hunter), and one per tree in the Workshop or Finale. Quest texts gain a sentence in Uncle Vinzenz's voice where it fits (docs/story.md style).

## Risks / Trade-offs

- [packwiz finds no file for `puffish-skills` by slug (the 26.1 files are tagged `26.1.2+2`)] → added by file URL; `packwiz update puffish-skills` may need the same, so check it on the next mod update.

- [Existing worlds drop from 64 to 8 Ultimine blocks] → changelog line under the release, players earn it back; story points in Arrival and The Works make the first steps quick.
- [Client shows a 64-block preview while the server mines 8] → Ultimine syncs config and reads attributes on both sides, but this is only verified by joining with a client; listed as a task.
- [Config schema differs from the docs in 0.19.x] → validate against the server log with `show_warnings`; the editor at puffish.net/skillsmod/editor can export a reference layout.
- [Walking XP numbers are huge] → scale in the expression; tune in playtest.
- [Ultimine mining levels Miner very fast late game] → cap per level in the curve; tune.
- [Pufferfish's Skills needs another mod] → check its CurseForge relations before adding; add any required dependency with its own `docs/mods.md` row.

## Migration Plan

Ships in the next release. No world migration: players keep their worlds and start with no skills and 8 Ultimine blocks. Rollback: remove the mod, set `max_blocks` back to 64, remove the `skill_points` rewards; skill data in worlds is then ignored.

## Open Questions

- Exact XP numbers and level curve: settled by playtesting, not by this design.
