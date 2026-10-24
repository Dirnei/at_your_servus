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
- **THEN** Sodium, Iris, Entity Culling, ImmediatelyFast, Mouse Tweaks, Controlling, Searchables, Better Advancements, Enchantment Descriptions, Lighty and Euphoria Patches are client-only

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
The client pack SHALL include Iris, the Complementary Reimagined and Complementary Unbound shader packs, and Euphoria Patches, all from CurseForge. Euphoria Patches and both Complementary shader packs MUST be built for the same Complementary version. A fresh install and a pack update SHALL leave shaders off until the player selects a shader pack, and a pack update MUST NOT change the player's shader choice.

#### Scenario: Fresh install
- **WHEN** a player imports the client zip and starts the game for the first time
- **THEN** Iris is loaded, Complementary Reimagined and Complementary Unbound are listed under Video Settings > Shader Packs together with their Euphoria Patches versions, and no shader pack is active

#### Scenario: Pack update after selecting shaders
- **WHEN** a player has turned on Complementary Reimagined and then updates the pack
- **THEN** Complementary Reimagined is still active after the update

#### Scenario: Versions out of step
- **WHEN** a Complementary shader pack is updated to a version Euphoria Patches is not built for
- **THEN** the pack check fails and names both files

#### Scenario: Server pack
- **WHEN** the server pack is built
- **THEN** it contains neither Iris, Euphoria Patches nor any shader pack

### Requirement: Playtest gap fillers
The pack SHALL include, from CurseForge: Spice of Life: Carrot Edition, so eating different foods gives extra hearts; a mod that provides the Feral Flare Lantern; Entangled; and a light level overlay toggled with F7.

#### Scenario: Food variety
- **WHEN** a player has eaten enough different foods to reach the first Spice of Life milestone
- **THEN** their maximum health goes up

#### Scenario: Light overlay
- **WHEN** a player presses F7 in a world
- **THEN** a light level overlay turns on, or its mode menu opens, and pressing it again turns it off

#### Scenario: Feral Flare Lantern and Entangled blocks
- **WHEN** a player looks them up in JEI
- **THEN** the Feral Flare Lantern and the Entangled Block are listed with a crafting recipe

### Requirement: Player teleport commands
The pack SHALL include FTB Essentials from CurseForge. Every player SHALL have one home, `/warp` to warps set by ops, `/back` to the previous location and the last death point, and `/tpa`. Only ops SHALL create or remove warps. `/rtp` SHALL be switched off.

#### Scenario: One home
- **WHEN** a player who already has a home runs `/sethome` with a new name
- **THEN** the command is refused and the first home stays

#### Scenario: Warp set by a player
- **WHEN** a player without op runs `/setwarp`
- **THEN** the command is unknown or refused, and no warp is created

#### Scenario: Warp set by an op
- **WHEN** an op runs `/setwarp town` and a player then runs `/warp town`
- **THEN** the player is teleported to the town warp

#### Scenario: Back to the grave
- **WHEN** a player dies and then runs `/back`
- **THEN** the player is teleported to the death point

#### Scenario: Random teleport
- **WHEN** a player runs `/rtp`
- **THEN** the command is unknown or refused, and the player does not move

### Requirement: Free shared waystones
Teleporting with Waystones SHALL cost no XP and SHALL NOT wear down warp stones. A waystone that is newly placed or found SHALL be global, so every player can travel to it without visiting it first.

#### Scenario: Long trip
- **WHEN** a player teleports from one waystone to a distant one, or to another dimension
- **THEN** the player keeps all their XP

#### Scenario: Warp stone use
- **WHEN** a player teleports with a warp stone
- **THEN** the warp stone's durability does not change

#### Scenario: Waystone placed by another player
- **WHEN** one player places a waystone and another player, who never visited it, opens any waystone
- **THEN** the new waystone is listed and the second player can teleport to it

### Requirement: Furniture choice
The pack SHALL include, from CurseForge and on both sides, Adorn, Bibliocraft Legacy and Fantasy's Furniture next to Macaw's Furniture. No quest SHALL require their blocks.

#### Scenario: Furniture in JEI
- **WHEN** a player searches JEI for blocks from Adorn, Bibliocraft Legacy and Fantasy's Furniture
- **THEN** each mod's furniture is listed with a recipe the player can craft

#### Scenario: Sitting and storing
- **WHEN** a player places an Adorn chair and a Bibliocraft bookcase, sits on the chair and puts a book in the bookcase
- **THEN** the player sits, and the book stays in the bookcase after leaving and rejoining the world

#### Scenario: Server pack
- **WHEN** the server pack is built
- **THEN** it contains Adorn, Bibliocraft Legacy and Fantasy's Furniture
