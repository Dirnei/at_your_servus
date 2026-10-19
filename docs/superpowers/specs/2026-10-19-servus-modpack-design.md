# Servus Modpack: Design

Date: 2026-10-19
Status: for approval

## 1. Intent

A public kitchen-sink modpack for Minecraft 26.1.2 on NeoForge, built to showcase the Servus mod family by Dirnei: **Servus: Foundation**, **Servus: Alchemy** and **Servus: Shuttles** (source in `C:\games\minecraft\servus_mc_mods`). Every other mod is there to fill a gap around them. The pack is published on CurseForge. Dirnei and friends test it first on Dirnei's own server.

A guided FTB Quests path with a story leads players through the Servus mods. The story gives the parts of the pack a common frame. Alchemy keeps its own story, Paracelsus' life told through his journal.

## 2. Goals, non-goals, anti-goals

**Goals**
- Servus is the main path. Storage and autocrafting are Shuttles, logistics is the Foundation Utility Duct, resources come from Alchemy.
- Still a real kitchen-sink pack: magic, exploration, RPG loot, building, QoL.
- A guided quest line with a story (see section 5).
- The pack is built from text files in this folder and is reproducible. Later, a GitHub Action publishes it to CurseForge.

**Non-goals**
- No expert pack with every recipe gated. Recipe changes only where a mod would undercut a Servus mod or where progression needs a gate.
- No duplicate of Alchemy's journal in FTB Quests.

**Anti-goals: the pack has failed if**
- players ignore Shuttles because a different storage or autocrafting mod is easier (that's why AE2 and Refined Storage are out);
- other resource mods make Alchemy pointless;
- quests get tedious ("craft 64 of X") or bury the story under checklists.

## 3. Constraints

- Minecraft **26.1.2**, NeoForge **26.1.2.x** (the example export uses `neoforge-26.1.2.122`), Java 25.
- Every mod must be on CurseForge with a NeoForge 26.1.2 file and allow distribution in modpacks.
- **Servus jars come from CurseForge releases**, for the public pack and the playtest alike. Mod fixes are released before they get tested.
- **Servus: Alchemy** was unlisted on CurseForge and was switched to public on 2026-10-19; when it becomes visible is unknown. Until then the pack gets it from the GitHub release (`github.com/Dirnei/servus_mc_mods`, tag `alchemy-v0.1.0-alpha`) as a packwiz URL metafile. That works for the playtest, but `packwiz cf export` doesn't put URL mods in the CurseForge manifest, and CurseForge doesn't allow third-party jars in `overrides/`. So **the first public upload waits until Alchemy is on CurseForge**; then the metafile is switched over to CurseForge. Foundation (project 1747973) and Shuttles (1746893) are live as 0.1.0-beta.
- **The first version (0.1.0) contains everything**, all chapters including the finale. According to Dirnei, Alchemy's Rubedo (Philosopher's Stone, Salamander) is done (`PLAN.md` M12 is out of date), so no temporary gates are needed.
- Many large mods have no 26.1.2 build yet (Ars Nouveau, Mekanism, Create, Thermal, Immersive Engineering, Botania, Iron's Spells, Tinkers, Farmer's Delight, Supplementaries). The mod list is limited to what exists today.

## 4. Mod selection

Availability was checked on 2026-10-19 against CurseForge file data. "alpha"/"beta" means only such a file exists for 26.1.2.

### 4.1 Core path
| Mod | Role | Note |
|---|---|---|
| Servus: Foundation | duct, tanks, pump, coal generator, tools: early logistics and early power | |
| Servus: Shuttles | warehouse, storage, autocrafting, field work, outposts | quest backbone |
| Servus: Alchemy | resource generation, the Great Work, Philosopher's Stone | must be published first; needs Modonomicon |
| Powah! (Rearchitected) | mid-to-late power | alpha; power only, so it doesn't compete with the duct |
| Iron Jetpacks | mid-game flight | upper tiers gated behind Servus materials via KubeJS |
| Re:Avaritia | endgame capstone, Infinity Armor = creative flight | recipes rewritten so the Philosopher's Stone/Alchemy is required |
| Just Dire Things | Nether preparation: goo progression, tools, weapons, armor | tune anything that overlaps with Alchemy's resource role |
| Cobblegen Galore | cobble generation | tune so it doesn't replace Alchemy |

### 4.2 Gap fillers
- **Magic/RPG:** Occultism; Apotheosis with its modules (Apothic Enchanting, Apothic Spawners, Apothic Attributes; verify module names and 26.1.2 files); Artifacts; Curios API.
- **Mob farms:** Dark Utilities (Vector and Damage Plates) + Apothic Spawners for farms players build; Hostile Neural Networks (beta) as the powered late-game farm, with output going into Shuttles.
- **Exploration:** The Twilight Forest (alpha), The Undergarden (beta), The Bumblezone (beta), Alex's Mobs (NeoForge), YUNG's API + the YUNG's structure mods with 26.1.2 builds, Dungeons and Taverns, Towns and Towers, Terralith, Nature's Compass, Explorer's Compass.
- **Utility:** Iron Furnaces, Crafting on a Stick, Building Wands, Rechiseled, Cooking for Blockheads, Carry On, Corail Tombstone (one grave mod only).
- **Storage, nice to have:** Sophisticated Storage, Sophisticated Backpacks, Functional Storage. They stay unchanged, with no KubeJS restrictions on their controllers (Claude's call); quests send storage questions to Shuttles. Revisit if the playtest shows players skipping Shuttles.
- **Quests and scripting:** FTB Quests, FTB XMod Compat, FTB Library/Teams/Chunks/Ultimine (already in the pack), KubeJS, LootJS.
- **Already in the example export, kept:** Macaw's set, Waystones, Lootr, Comforts, OpenBlocks Elevator, Leaves Be Gone, JEI, Jade, MezzConfig, Shogi, plus their libraries.
- **QoL:** AppleSkin, Mouse Tweaks, Controlling, Searchables, Just Enough Resources (alpha), Better Advancements, Enchantment Descriptions, Clumps, FastWorkbench, FastFurnace.
- **Performance (client):** Sodium, Entity Culling, FerriteCore, ModernFix, ImmediatelyFast. Iris and SecurityCraft stay out of 0.1.0 (Claude's call).

### 4.3 Deliberately out
- Applied Energistics 2, Refined Storage: compete with Shuttles.
- Mystical Agriculture, Productive Bees, Replication: compete with Alchemy as the resource mod or the "make anything" endgame.
- Ender IO, Oritech: bring their own pipes/conduits that clash with the duct. Energized Power is the fallback if Powah turns out unusable in the playtest (Claude's call).
- Easy Mob Farm/Tiny Mob Farm: too easy next to built farms.
- Storage Drawers, Traveler's Backpack: overlap with Functional Storage and Sophisticated Backpacks.
- Xaero's maps: FTB Chunks already has a map.

### 4.4 Later
- Ars Nouveau as soon as a 26.1.2 build exists.

## 5. Story and quests

### 5.1 Frame
The player inherits a run-down estate in Tyrol from a great-uncle. The quest texts are his letters and notes, each starting with "Servus, ...". In the cellar is Paracelsus' journal (Alchemy's own journal), which the uncle was researching. The family once ran a trading business, a nod to the trading houses of Schwaz in Paracelsus' time, and the uncle wanted to revive it with a modern warehouse.

**The uncle's mystery (Claude writes it, Dirnei approves it):** the uncle didn't simply die. He finished the Great Work and wanted to go "beyond the Stone." The letters reveal step by step that he disappeared while trying. The finale (Avaritia) follows his path and resolves what became of him.

### 5.2 Chapters
1. **Prologue: Arrival.** First letter, basics, first gap fillers (backpack, Waystones, food).
2. **The Old Works.** Foundation (Utility Duct, tanks, pump, coal generator) **and the small warehouse right away**: racks, rails, Mk1 shuttle (no power), then Warehouse Controller on coal power and the Storage Terminal. "A merchant without a warehouse is just a peddler."
3. **The Cellar (Alchemy).** Milestone quests per stage (Nigredo, Albedo, Citrinitas, Rubedo) that point to the journal. The journal stays Alchemy's real tech tree.
4. **The Power Station (Powah).** Triggered because the growing warehouse and the machines need more than coal.
5. **Into the Nether (Just Dire Things).** Better tools, weapons and armor for the Nether; connects to Alchemy's Salamander.
6. **The Trading House (Shuttles grows up).** Put-away rules, data cable and on-demand autocrafting (Alchemy machines produce on order), field work on Farm Rails, outposts and wireless.
7. **The Uncle's Workshop (Iron Jetpacks).** Mid-game flight, the uncle's invention.
8. **Finale: Beyond the Stone (Re:Avaritia).** After the Philosopher's Stone. Resolves the mystery. Reward: Infinity Armor.

Alchemy and the warehouse run in parallel. Quests keep crossing the two (first Alchemy output stored in the warehouse; later the warehouse orders from Alchemy machines), because that integration is what sets the pack apart.

**Side chapters,** optional and lighter on story: Exploration and dimensions, Occultism, Apotheosis and mob farms, building and decor.

### 5.3 Quest rules
- Tasks are mostly "make/do something for the first time", rarely quantities.
- Rewards are mostly useful items for the next step; little loot-box clutter.
- Claude writes the full quest and letter texts, including the ending. Dirnei reviews them before the first public upload.
- Quest text is in English (Claude's call: public pack, the mods are documented in English). Use FTB Quests translation keys if the version supports them, so a German translation can follow.

## 6. How it's built

### 6.1 Repository
This folder (`C:\games\minecraft\servus_modpack`) is the pack's source and becomes a git repository (later on GitHub).

**Tooling (Claude's call): packwiz.**
- `pack.toml`, `index.toml`; one `mods/*.pw.toml` per mod with CurseForge project/file ID and side (`client`, `server`, `both`).
- `config/`, `defaultconfigs/`, `kubejs/`, `config/ftbquests/quests/` as plain files; they end up in `overrides/`.
- The configs from `Servus-0.1.0.zip` are the starting point.
- `packwiz cf export` builds the CurseForge zip (manifest.json + overrides), the same format as the example export.

### 6.2 Artifacts per version
- **Client pack:** CurseForge zip.
- **Server pack:** all `both`/`server` mods as jars plus configs/KubeJS/quests, without client-only mods. Uploaded to CurseForge as the server pack of the client file.
- Version from `pack.toml`, semver, starting at 0.1.0.

### 6.3 Test server
Dirnei's existing Docker setup (`servus_mc_mods/server`, itzg/minecraft-server) serves the playtest. It is fed from this pack's server pack and must load exactly the same mod versions as the client pack. Note: `docker-compose.yml` there is still on 1.21.1/NeoForge 21.1/Java 21 and must be updated to 26.1.2/Java 25.

### 6.4 Publishing (later)
A GitHub Action on tag: build client zip and server pack, upload both to the CurseForge project through the CurseForge upload API (API token as a repository secret).

## 7. Left to the builder
- Exact versions and dependency libraries per mod (packwiz resolves them).
- Which config values to change for Cobblegen Galore and Just Dire Things, once their overlap with Alchemy has been looked at in game.
- KubeJS recipe changes for Iron Jetpacks tiers and the Avaritia capstone, within the gates described above.
- The exact quest list per chapter, following section 5.
- The server pack build script.
