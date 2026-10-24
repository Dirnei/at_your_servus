# Design

## Context

Quests are written in TOML under `quests/side/` and generated to JSON5; quest IDs come from the chapter and quest slugs. The quest check verifies item IDs against the server jars but not advancement IDs. Facts from the jars (Twilight Forest 4.9.3817, The Undergarden 0.9.8, The Bumblezone 7.18.0):

- Twilight Forest has boss trophies (`naga_trophy`, `lich_trophy`, `minoshroom_trophy`, `hydra_trophy`, `knight_phantom_trophy`, `ur_ghast_trophy`, `alpha_yeti_trophy`, `snow_queen_trophy`). Its `twilightforest:root` advancement needs being in the dimension.
- The Undergarden has `undergarden:undergarden/enter_undergarden` and `undergarden:undergarden/kill_forgotten_guardian`, and items `catalyst`, `cloggrum_ingot`, `froststeel_ingot`, `utherium_crystal`, `regalium_crystal`, `forgotten_ingot`.
- The Bumblezone's root advancement is granted on the first tick, so it cannot show entry; `bee_bread` is only found there. Items: `honey_compass`, `stinger_spear`, `royal_jelly_bottle`, `essence_of_the_bees`.
- Vanilla: `minecraft:story/enter_the_end`, `minecraft:end/kill_dragon`, `minecraft:end/find_end_city`, item `minecraft:elytra`.

## Goals / Non-Goals

**Goals:**
- A guided path through each dimension, in the chapter the player already knows.

**Non-Goals:**
- New side chapters, rewards that skip a dimension's progression, or quests for every item a dimension has.
- Changes to the Nether main chapter.

## Decisions

- **One chapter, four branches.** Each branch is a row on the chapter map, starting from `compasses` (End: from `nether:blaze`, since eyes of ender need blaze powder). Alternative: one side chapter per dimension. Rejected by the user: the chapter holds the world beyond the farm.
- **Boss quests use trophies.** A trophy always drops and works as an item task for every player in a team. Alternative: kill tasks or the progress advancements. Rejected: advancements are per player, and trophies show in the quest and in JEI.
- **Entry tasks:** Twilight Forest `twilightforest:root`; Undergarden the catalyst plus `undergarden:undergarden/enter_undergarden`; Bumblezone `bee_bread`; End `minecraft:story/enter_the_end`. Advancement IDs are checked against the jars by hand, since the quest check does not cover them.
- **Changed tasks on existing slugs:** `twilight` asks for entering instead of a magic map and the Lich trophy (the Lich moves to its own quest); `undergarden` keeps the catalyst and adds entering, and the cloggrum helmet moves to `cloggrum`; `bumblezone` keeps bee bread. A player who completed them keeps the completion.
- **Optional flags:** gear and side-line quests (ironwood, steeleaf, fiery, yeti line, regalium, royal jelly) are `optional`; the boss and ore spine is not. The whole chapter is a side chapter and gates nothing.
- **Texts:** one or two short sentences each, in the voice of the existing exploration quests (Vinzenz in the third person).
- **Sketch:**

```
              +-- artifact (opt)
compasses ----+-- twilight -> naga -> lich -> minoshroom -> hydra -> knights -> ur-ghast
              |      +-> ironwood (opt), steeleaf (opt)   lich -> yeti (opt) -> snow-queen (opt)
              |                                           hydra -> fiery (opt)
              +-- undergarden -> cloggrum -> froststeel -> utherium -> forgotten-guardian -> forgotten
              |                     +-> regalium (opt)
              +-- bumblezone -> honey-compass -> stinger-spear -> essence
                      +-> royal-jelly (opt)
nether:blaze --- end -> dragon -> end-city -> elytra
```

## Risks / Trade-offs

- [The chapter grows to about 30 quests] → one row per dimension keeps it readable; the quest explorer reports overlapping quests.
- [An advancement ID is wrong] → the task can never complete; each ID is looked up in its jar before writing, and the manual test enters each dimension.
- [Twilight Forest locks areas until the previous boss is beaten] → the quest order follows the mod's own progression, so no quest asks for a locked boss first.
