# Progression gates

Every recipe and config change the pack makes to another mod, with its reason. The rule: change a recipe only to tie another mod's progression to the Servus mods, or to keep a mod from undercutting a Servus mod. Everything else stays at the mod's defaults.

## Recipe changes (KubeJS)

| Script | Change | Reason |
|---|---|---|
| `kubejs/server_scripts/gates/iron_jetpacks.js` | Elite Coil needs 2 Quicksilver (`servus_alchemy:quicksilver`) | Iron Jetpacks generates thruster recipes at runtime, and each tier takes its coil: diamond and emerald take the Elite Coil. Jetpacks from diamond up need Alchemy. |
| `kubejs/server_scripts/gates/iron_jetpacks.js` | Ultimate Coil needs Quicksilver and Ignis Perpetuus (`servus_alchemy:ignis_perpetuus`) | Only the netherite tier takes the Ultimate Coil, so the top jetpack needs the Rubedo-era Alchemy products. |
| `kubejs/server_scripts/gates/avaritia.js` | Infinity Catalyst (both recipes) additionally needs Ignis Perpetuus, Quicksilver, Caput Mortuum, a Shuttles Crafting CPU and a Powah Nitro Crystal | The Avaritia capstone comes after the Great Work, the trading house and the power station. |
| `kubejs/server_scripts/fixes/bumblezone.js` | Removes The Bumblezone's two Potion Candle recipes (type `the_bumblezone:potion_candle_recipe`) | Bug in Bumblezone 7.18.0: the recipe fails to decode on the client, so joining a world disconnects. Not a gate; remove the script once a fixed Bumblezone is out. |
| `kubejs/server_scripts/first_join.js` | Gives the FTB Quests book once per player (stage `servus_got_quest_book`) | Players find the quest line without knowing the key binding. |

Lower jetpack tiers (wood to gold) keep their default recipes. The creative jetpack has no crafting material, so Iron Jetpacks generates no recipe for it.

## Config changes

| File | Change | Reason |
|---|---|---|
| `config/ironjetpacks/jetpacks/netherite.json` | New tier 6 jetpack, crafted from netherite ingots | Gives the top of the jetpack line a home in the Uncle's Workshop chapter; it takes the Ultimate Coil and so the Alchemy gate. The other files in that folder are Iron Jetpacks' defaults, shipped so the folder is complete. |

## Checked and left unchanged

| Mod | Finding (2026-10-19) |
|---|---|
| Cobblegen Galore | Its generators only make stone types (cobblestone, stone, deepslate, basalt, blackstone, obsidian and similar). The iron to netherite generators are speed tiers. No ores, raw metals or gems. |
| Just Dire Things | Goo only converts vanilla storage blocks into Just Dire Things' own materials (iron block to raw ferricore and so on). It makes no vanilla ores, raw metals or gems. |
| Sophisticated Storage, Sophisticated Backpacks, Functional Storage | Default recipes on purpose; quests send storage to Shuttles. |
