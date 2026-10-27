## Context

The Servus Alchemy journal (`WorkshopCategory.java` in the mods repo) builds the workshop as one chain: Calciner, Purifier, Coagulator, Athanor. The Athanor's fire then rises through rituals built around it: a white ring of 16 Salt Crystal Blocks (Albedo), three Principle Vats plus an Amethyst Block (Citrinitas), four Obsidian plus a Ghast Tear (Rubedo). Every Athanor recipe declares the fire it needs (`AlchemyRecipeTable.athanor()`, tier 0 to 3):

| Fire | Products |
|---|---|
| Nigredo (0) | Salt Crystal Block |
| Albedo (1) | Seed of Coal / Iron / Copper, Elixir of Sight, Gnome Hollow |
| Citrinitas (2) | Seed of Gold / Redstone / Quartz, Principle Dropper, Ignis Perpetuus |
| Rubedo (3) | Seed of Diamond / Emerald, Sealed Flask, Prelum Screw |

All seeds are one item, `servus_alchemy:seed`, told apart by the `servus_alchemy:vein` component (e.g. `servus_alchemy:iron`). The quest generator already writes item tasks with components and `match_components: fuzzy` (used for jetpacks in `08-workshop.toml`).

FTB Quests matches one item per item task and has no "any of these items" task without FTB Filter System, which is not in the pack. It does have `dependency_requirement: one_completed` on quests.

## Goals / Non-Goals

**Goals:**
- Cellar quests in the journal's order, with the Athanor upgrades visible in the quest texts.
- Stage milestones that accept any one of a few products of their fire.
- Keep every existing slug so player progress survives.

**Non-Goals:**
- No new mod (FTB Filter System) for any-of item tasks.
- No automatic check that a product option belongs to the right fire; the options are picked by hand from the table above.
- No change to the Nether, Trading House or Finale quests beyond the Sealed Flask reward.

## Decisions

**Any-of through dependencies, not tasks.** Each product option is its own small quest with one item task. The stage hexagon depends on all options with `dependency_requirement = "one_completed"` and has one checkmark task, which the player ticks once one option is done. A taskless hexagon was rejected: in FTB Quests 26.1.2.9 a quest is only recorded as complete through `Task.onCompleted`, so a quest without tasks shows 100% but never enters the team's completed set, and quests behind it would stay locked. Alternatives: FTB Filter System (a new mod just for this), or one fixed item per stage (simple but not what the user wants).

**Quest source key.** Quests get an optional `dependency_requirement` key with the FTB values (`all_completed` default, `one_completed`). The generator writes it only when it is not the default, so other chapters stay byte-identical. Every quest still needs a task. The checkmark hexagons get an explicit `icon`, since they have no item task to take one from.

**Chapter layout (`04-cellar.toml`).**

```
journal -> calciner -> purifier -> coagulator -> athanor -> nigredo
                                       |                      |
                               salt-in-the-racks        +-----+------+
                                                     seed     seed-     elixir
                                                    (iron)   copper    -of-sight
                                                        \      |       /
                                                          albedo (any, checkmark)
                                                         /     |     \
                                                 seed-gold dropper ignis-perpetuus
                                                         \     |     /
                                                        citrinitas (any, checkmark)
                                                         /     |     \
                                                  seed-diamond   seed-emerald
                                                           \         /
                                                          rubedo (any, checkmark)
                                                                |
                                            receptaculum (Receptaculum + Sealed Flask)
                                                                |
                                                           prelum-screw
                                                                |
                                                      netherite (Prelum + Caput Mortuum)
```

- New slugs: `purifier` (Purifier, Catch Basin, Residue Crock), `coagulator` (Coagulator, Principle Vat), the option quests `seed-copper`, `elixir`, `seed-gold`, `dropper`, `ignis-perpetuus`, `seed-diamond`, `seed-emerald`, and after Rubedo the chain `receptaculum` (Receptaculum and Sealed Flask), `prelum-screw`, `netherite` (Prelum and Caput Mortuum, takes Rubedo's Netherite Scrap reward). The Prelum is the last thing in the Work, so its screw comes at the end, not as a Rubedo option; Rubedo's fan has two options.
- `seed` becomes the Seed of Iron option (now with the vein component). Players who finished it already had Albedo, so nothing is lost.
- `athanor` depends on `coagulator`; `nigredo` asks for a Salt Crystal Block instead of the Coagulator.
- `salt-in-the-racks` depends on `coagulator`, where Salt Crystals come from.
- Gnome Hollow, Coal, Redstone and Quartz seeds are left out to keep the Albedo and Citrinitas fans at three options.

**Upgrade texts.** Each milestone's text tells how to raise the fire to the next stage, since the next fan needs it: Nigredo explains the white ring, Albedo the yellow ring, Citrinitas the red crown. Texts stay in Vinzenz' plain style and point to the journal.

**Sealed Flask.** `trading-house:alchemy-order` rewards 8 emeralds instead. The quest check keeps a deny list of reward items, starting with `servus_alchemy:sealed_flask`.

## Risks / Trade-offs

- [Players must tick the checkmark by hand] → The milestone texts say so; it is one click.
- [Players who already finished `nigredo` see the new `purifier` and `coagulator` quests open behind it] → They can still complete them and get the rewards; only the order looks odd on existing worlds.
- [Fan options are hand-picked] → The table above comes from `AlchemyRecipeTable`; recheck it when Alchemy changes tiers.
