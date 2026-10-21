# Spec Delta

## ADDED Requirements

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

## MODIFIED Requirements

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
