# mod-selection Specification

## Purpose
Defines which mods the Servus pack ships, which it deliberately excludes, where each mod is sourced from, and on which side each mod runs, so that Servus stays the main path.

## Requirements

### Requirement: Platform
The pack SHALL target Minecraft 26.1.2 with NeoForge 26.1.2.122, and every included mod MUST have a NeoForge file for Minecraft 26.1.2.

#### Scenario: Mod without a 26.1.2 build
- **WHEN** a wanted mod has no NeoForge 26.1.2 file
- **THEN** it is not added, and the mod list documentation names it as waiting for a port

### Requirement: Servus mods are included
The pack SHALL include Servus: Foundation, Servus: Alchemy and Servus: Shuttles, together with their required dependencies (including Modonomicon for Alchemy).

#### Scenario: Servus mods load
- **WHEN** the pack starts on client or server
- **THEN** the mods `servus_foundation`, `servus_alchemy` and `servus_shuttles` are loaded

### Requirement: Servus jars come from releases
Servus mods SHALL be referenced as published release files, never as local builds. Servus: Alchemy SHALL come from the GitHub release `alchemy-v0.1.0-alpha` until it is visible on CurseForge, and from CurseForge afterwards.

#### Scenario: Alchemy not yet on CurseForge
- **WHEN** the pack is built while Alchemy is not visible on CurseForge
- **THEN** Alchemy is downloaded from `https://github.com/Dirnei/servus_mc_mods/releases/download/alchemy-v0.1.0-alpha/servus_alchemy-0.1.0-alpha.jar`

### Requirement: Gap-filling mod set
The pack SHALL include the core path mods Powah, Iron Jetpacks, Re:Avaritia, Just Dire Things and Cobblegen Galore, plus FTB Quests and KubeJS, plus the gap fillers listed in the design document's section 4.2 that have a 26.1.2 build.

#### Scenario: Core path present
- **WHEN** the mod list is checked
- **THEN** Powah, Iron Jetpacks, Re:Avaritia, Just Dire Things, Cobblegen Galore, FTB Quests, FTB XMod Compat, KubeJS and Crafting on a Stick are all present

#### Scenario: Example export mods kept
- **WHEN** the mod list is checked
- **THEN** every mod from `Servus-0.1.0.zip` is still present, at the same or a newer file

### Requirement: Competing mods are excluded
The pack MUST NOT contain Applied Energistics 2, Refined Storage, Mystical Agriculture, Productive Bees, Replication, Ender IO, Oritech, Storage Drawers, Traveler's Backpack, Xaero's Minimap, Xaero's World Map or SecurityCraft.

#### Scenario: Excluded mod added by mistake
- **WHEN** one of the excluded mods appears in the mod list, also as a dependency
- **THEN** the pack check fails and names the mod

### Requirement: Side assignment
Every mod and every shader pack SHALL be marked as client-only, server-only or both. Rendering, input and HUD-only mods SHALL be client-only, and shader packs SHALL be client-only.

#### Scenario: Client-only mods
- **WHEN** the mod list is checked
- **THEN** Sodium, Iris, Entity Culling, ImmediatelyFast, Mouse Tweaks, Controlling, Searchables, Better Advancements and Enchantment Descriptions are client-only

#### Scenario: Shader pack marked for both sides
- **WHEN** a shader pack in the pack is not marked client-only
- **THEN** the pack check fails and names the shader pack

### Requirement: Mod list documentation
The repository SHALL contain a human-readable list of all mods and shader packs with each one's role in the pack, and a list of excluded and waiting mods with the reason.

#### Scenario: New mod added
- **WHEN** a mod is added to the pack
- **THEN** the mod list documentation gains an entry with its role

#### Scenario: New shader pack added
- **WHEN** a shader pack is added to the pack
- **THEN** the mod list documentation gains an entry with its role

### Requirement: Shaders available, off by default
The client pack SHALL include Iris and the Complementary Reimagined shader pack, both from CurseForge. A fresh install and a pack update SHALL leave shaders off until the player selects a shader pack, and a pack update MUST NOT change the player's shader choice.

#### Scenario: Fresh install
- **WHEN** a player imports the client zip and starts the game for the first time
- **THEN** Iris is loaded, Complementary Reimagined is listed under Video Settings > Shader Packs, and no shader pack is active

#### Scenario: Pack update after selecting shaders
- **WHEN** a player has turned on Complementary Reimagined and then updates the pack
- **THEN** Complementary Reimagined is still active after the update

#### Scenario: Server pack
- **WHEN** the server pack is built
- **THEN** it contains neither Iris nor any shader pack
