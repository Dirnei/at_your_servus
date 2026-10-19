# Spec Delta

## Purpose

Ties other mods' progression to the Servus mods with recipe and config changes, and keeps Alchemy the pack's resource-generation mod, without turning the pack into an expert pack.

## ADDED Requirements

### Requirement: Minimal recipe changes
Recipe changes SHALL exist only to gate progression on Servus mods or to keep another mod from undercutting a Servus mod. Every change SHALL be listed with its reason in the repository.

#### Scenario: Unlisted change
- **WHEN** a recipe is changed by a script
- **THEN** the change and its reason appear in the gates documentation

### Requirement: Jetpack tiers gated
Iron Jetpacks tiers from diamond upward SHALL need Quicksilver (`servus_alchemy:quicksilver`), the netherite tier SHALL also need Ignis Perpetuus (`servus_alchemy:ignis_perpetuus`), and the creative jetpack MUST NOT be craftable. Lower tiers keep their recipes.

#### Scenario: Diamond jetpack
- **WHEN** a player looks up the diamond jetpack tier recipe in JEI
- **THEN** it includes Quicksilver

#### Scenario: Iron jetpack
- **WHEN** a player crafts an iron tier jetpack
- **THEN** the recipe is unchanged from Iron Jetpacks' default

### Requirement: Avaritia capstone gated on Rubedo
Re:Avaritia's endgame SHALL need Alchemy's Rubedo products: the Infinity Catalyst recipe SHALL include Ignis Perpetuus, Quicksilver and Caput Mortuum, plus a Shuttles Crafting CPU and a top-tier Powah item.

#### Scenario: Infinity Catalyst lookup
- **WHEN** a player looks up the Infinity Catalyst in JEI
- **THEN** the recipe lists the Alchemy, Shuttles and Powah items above

### Requirement: Resource mods do not replace Alchemy
Cobblegen Galore and Just Dire Things SHALL be configured so they do not produce ores, raw metals or gems faster or cheaper than Alchemy's gnome veins. Cobblestone, stone variants and non-ore resources stay allowed.

#### Scenario: Cobblegen output
- **WHEN** a Cobblegen Galore generator runs at its top tier
- **THEN** it produces no ores, raw metals or gems

### Requirement: Storage mods unchanged
Sophisticated Storage, Sophisticated Backpacks and Functional Storage SHALL keep their default recipes.

#### Scenario: Storage controller recipe
- **WHEN** a player looks up the Functional Storage controller recipe
- **THEN** it is the mod's default recipe

### Requirement: Scripts load cleanly
All KubeJS scripts SHALL load without errors or warnings about missing items or recipes.

#### Scenario: Server start
- **WHEN** the test server starts the pack
- **THEN** the KubeJS server log has no errors
