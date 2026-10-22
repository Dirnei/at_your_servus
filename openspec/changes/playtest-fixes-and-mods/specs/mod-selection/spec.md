# Spec Delta

## ADDED Requirements

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

## MODIFIED Requirements

### Requirement: Side assignment
Every mod and every shader pack SHALL be marked as client-only, server-only or both. Rendering, input and HUD-only mods SHALL be client-only, and shader packs SHALL be client-only.

#### Scenario: Client-only mods
- **WHEN** the mod list is checked
- **THEN** Sodium, Iris, Entity Culling, ImmediatelyFast, Mouse Tweaks, Controlling, Searchables, Better Advancements, Enchantment Descriptions, Lighty and Euphoria Patches are client-only

#### Scenario: Shader pack marked for both sides
- **WHEN** a shader pack in the pack is not marked client-only
- **THEN** the pack check fails and names the shader pack

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
