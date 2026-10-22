# Design

## Context

See `proposal.md` for the why and `specs/quest-line/spec.md` for the requirements. This change builds on `playtest-fixes-and-mods` (Spice of Life in the pack, Works storage chain, `&` escaping).

Current state (checked 2026-10-21):
- Chapter files are `<NN>-<slug>.toml`; `NN` only orders, the slug is the chapter ID, so renumbering keeps every quest ID. Quest tasks can be `item`, `advancement` or `checkmark`; rewards `item` or `xp`.
- Shuttles field work (Shuttles docs and source): one connected run of Farm Rail is a field; a Field Head beside it takes water through a fluid pipe and keeps the farmland under the rails wet; the Harvester and the Spreader are tools fitted in the Shuttle Workshop, one per shuttle, and no shuttle tier limit was found in the source; supply runs keep the head stocked with seeds, fertilizer and anti-corrosion items; the head learns the field's produce and has "Harvest up to" and "Fertilize below" levels; the copper ages in five stages, one per `corrosion_water` (6000 mB) of water used, a corroded field gets no water, an axe scrapes the whole field back one stage, and one anti-corrosion item per step holds the stage.
- `#servus_shuttles:anti_corrosion` contains only `minecraft:honeycomb`.
- Recipes need nothing past the Works: Farm Rail (copper, planks), Field Head (iron, Fluid Tank, composter, planks, Farm Rail), Shuttle Workshop (iron, planks, crafting table), Harvester (iron, shears, iron hoe, hopper), Spreader (iron, hopper, dispenser, bone block), Range Upgrade (copper, seeds, bone meal, composter).
- A 32-rail field uses about 32 mB per 5 seconds, so a stage lasts about 15 minutes and a field dries out after about an hour.
- Spice of Life: Carrot Edition has no advancements; its only item is `solcarrot:food_book`.
- Cooking for Blockheads 26.1.2: ovens, fridges, sinks, counters and cabinets exist only as dyed variants (`white_oven`, `white_fridge`, ...) with tags like `cookingforblockheads:ovens`. Other items: `cooking_table`, `recipe_book`, `crafting_book`, `no_filter_edition`, `heating_unit`, `ice_unit`, `preservation_chamber`, `spice_rack`, `toaster`, `milk_jar`, `cow_jar`, `fruit_basket`, `cutting_board`, `tool_rack`.
- Just Dire Things quests today: Into the Nether covers goo tiers 1 and 2, ferricore and blazegold with gear and the lava immunity upgrade.

## Goals / Non-Goals

**Goals:**
- A player who just finished the Works can feed the farm with shuttles before the Cellar is done, and learns the whole field loop including corrosion.
- Side chapters make Cooking for Blockheads and the unquested Just Dire Things content findable.

**Non-Goals:**
- No changes to Shuttles, Spice of Life or Cooking for Blockheads behaviour or recipes.
- No German texts.
- The finale doesn't depend on The Fields.

## Decisions

### D1: The Fields as chapter 03, parallel to The Cellar
`fields-letter` depends on `old-works:terminal`, like `cellar:journal`. Files after it are renamed one number up (`03-cellar` to `04-cellar`, ..., `08-finale` to `09-finale`). No quest outside the chapter depends on it, so the long corrosion wait never blocks Alchemy.
- Alternative: The Cellar after The Fields. Rejected: the bee and corrosion quests take about an hour of play.
- Alternative: Finale depends on the fields' closing quest. Rejected for now: it would make an optional-feeling chapter mandatory; easy to add later.

### D2: Quest chain of The Fields
```
 fields-letter -> farm-rail -> field-head -> harvester -> first-harvest -> stock-levels
                        shuttle-workshop --^        |
                                                    +--> spreader -> range (optional)
                                                    +--> corrosion -> bees -> honeycomb -> anti-corrosion (bees on: optional)
 food-variety  (deps first-harvest)
 fields-done   (deps stock-levels, corrosion, food-variety)
```
- `farm-rail`: 16 Farm Rail. `field-head`: Field Head; text: water from the Works pump through a fluid pipe.
- `shuttle-workshop`: Shuttle Workshop. `harvester`: Harvester; text: fit it on a shuttle in the workshop and pick the crop on the head.
- `first-harvest`, `stock-levels`, `corrosion`, `anti-corrosion`: checkmark quests, because what they teach (a delivery, a GUI setting, scraping) has no item or advancement.
- `spreader`: Spreader and 16 bone meal. `range`: moved from The Trading House, optional.
- `bees`: advancement `minecraft:husbandry/safely_harvest_honey` (honey with a campfire below). `honeycomb`: 8 honeycomb (shears) and a beehive.
- `food-variety`: Spice of Life food book plus a checkmark for the first milestone.
- `fields` from The Trading House is removed; its content is split over `farm-rail`, `harvester` and `spreader`, so it isn't moved as one quest. `range` moves with its slug.
- Letters (`fields-letter`, `fields-done`) follow `docs/story.md`: the Huber farm fed the miners; Vinzenz put shuttles on the fields; bees by the old orchard keep the copper bright.

### D3: Trading House adjustments
`workshop` keeps its slug and asks only for `servus_shuttles:shuttle_mk2`. It keeps depending on `zones` only, not on `fields:shuttle-workshop`, because D1 forbids main quests outside The Fields from depending on it; its text points to the Shuttle Workshop for players who skipped the fields. `wireless` depends on `mk3`. The terminal letter ends with both directions: feed yourself from the fields, and dig a cellar.

### D4: Cooking for Blockheads tasks use the white variants
Item tasks can't take a tag, so oven and fridge tasks use `white_oven` and `white_fridge`, the variants crafted before dyeing. If JEI shows another default, use that.
- Alternative: extend the generator to FTB's tag filters. Rejected: needs FTB Filter System, which isn't in the pack, for two tasks.

### D5: The Kitchen side chapter
`building:kitchen` moves to `kitchen:cooking-table` (the Building chapter keeps wand, chisel and chests). Chain: cooking table -> recipe book -> counter and cabinet (connected kitchen) -> white oven with heating unit -> white fridge with ice unit -> sink -> spice rack, toaster, milk jar, cow jar (optional extras) -> food book. Rewards are food items, nudging food variety. The chapter is a side chapter, so it depends on nothing in the main line except being opened.

### D6: Just Dire Things side chapter
Entry depends on `nether:goo`. Quests: simple sensor, Advanced Sensor (text: target Player, set the area, a redstone signal while someone stands in it), clicker, creature catcher, goo tier 3 and Celestigem, Celestigem paxel, Time Wand, goo tier 4 and Eclipse Alloy, Portal Gun, and one optional quest for a utility upgrade such as the ore scanner. No generator, energy transmitter, block breaker or block placer tasks.

## Risks / Trade-offs

- [The Advanced Sensor's area limit might be too small for a "pressure plate" use] → Check its config in `config/` during implementation; mention the limit in the quest text.
- [Checkmark quests can be ticked without doing the thing] → Accepted for the four teaching quests; rewards there are small.
- [`safely_harvest_honey` is earned with a glass bottle, not shears] → The `bees` text says so; the `honeycomb` quest that follows covers the shears.
- [The moved and split quests lose progress] → Alpha pack; listed in the changelog.
