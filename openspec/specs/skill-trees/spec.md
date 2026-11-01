# skill-trees Specification

## Purpose
Gives players character progression through three skill trees, earned by playing and by the story, with FTB Ultimine's range tied to the mining tree.

## Requirements

### Requirement: Skill mod
The pack SHALL include Pufferfish's Skills from CurseForge on both sides. Its skill screen SHALL open with the K key by default.

#### Scenario: Open the skill screen
- **WHEN** a player in a world presses K
- **THEN** the skill screen opens with the tabs Miner, Hunter and Wanderer, in that order

#### Scenario: K does nothing else on a new install
- **WHEN** a player on a fresh install presses K in a world
- **THEN** only the skill screen opens and shaders are not toggled

#### Scenario: Existing keys kept
- **WHEN** a player who had already saved their own key bindings updates the pack
- **THEN** their bindings are unchanged

### Requirement: Three skill trees
The pack SHALL ship three skill trees, unlocked for every player from the start: Miner for mining, Hunter for combat and Wanderer for travel. Every skill SHALL give a player attribute bonus while it is unlocked. Each tree SHALL have at least one skill a player can buy with their first point.

#### Scenario: Hunter skill
- **WHEN** a player unlocks a Hunter skill that adds attack damage
- **THEN** their attack damage attribute is higher by that amount

#### Scenario: Wanderer skill
- **WHEN** a player unlocks a Wanderer skill that adds movement speed
- **THEN** they walk faster than a player without it

#### Scenario: First point
- **WHEN** a player has one point in a tree and no skills there
- **THEN** at least one skill in that tree can be unlocked

### Requirement: Ultimine grows with Miner
FTB Ultimine SHALL let a player without Miner Ultimine skills mine at most 8 blocks at once. Four Miner skills, each needing the one before, SHALL raise the limit to 16, 32, 64 and 128 blocks.

#### Scenario: New player
- **WHEN** a player without Miner skills ultimines a vein of 20 ores
- **THEN** 8 blocks are mined

#### Scenario: Second Ultimine skill
- **WHEN** a player has unlocked the first two Ultimine skills
- **THEN** ultimining mines up to 32 blocks

#### Scenario: Skills in order
- **WHEN** a player has not unlocked the first Ultimine skill
- **THEN** the second Ultimine skill cannot be unlocked

### Requirement: Points from playing
Each tree SHALL have its own experience, and every level SHALL give one point in that tree. Miner SHALL gain experience from mining blocks with the correct tool, Hunter from killing mobs, and Wanderer from walking and swimming. Kill experience SHALL be limited per chunk, so a mob farm stops paying after a limit until some time has passed.

#### Scenario: Mining levels Miner
- **WHEN** a player mines stone and ore with a pickaxe until the Miner level goes up
- **THEN** they gain one Miner point and no Hunter or Wanderer point

#### Scenario: Mob farm
- **WHEN** a player kills mobs in one chunk beyond its limit
- **THEN** further kills there give no Hunter experience until the limit resets

### Requirement: Points from the story
Some main-line quests SHALL give skill points for a named tree as a reward. Each tree SHALL get at least one point from the main line.

#### Scenario: Claiming a story point
- **WHEN** a player claims a quest reward of one Miner point
- **THEN** their unspent Miner points go up by one and they see a message naming the tree

### Requirement: Progress kept on death
Skills, points and experience SHALL stay when a player dies.

#### Scenario: Death
- **WHEN** a player with three Hunter skills dies and respawns
- **THEN** they still have the three skills and their bonuses
