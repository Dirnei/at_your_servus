# Spec Delta

## ADDED Requirements

### Requirement: Fields beside the Cellar
The Fields SHALL open when the Storage Terminal quest of The Old Works is done, at the same time as The Cellar. No quest outside The Fields SHALL depend on a quest in The Fields.

#### Scenario: Both chapters open
- **WHEN** a player completes the Storage Terminal quest
- **THEN** the first quests of The Fields and of The Cellar are both available

#### Scenario: Skipping the fields
- **WHEN** a player completes no quest in The Fields
- **THEN** every quest in the other main chapters is still reachable

### Requirement: Bees protect the fields
The Fields SHALL teach that a field's copper rails corrode, that an axe scrapes them back, and that honeycomb in the Field Head stops the corrosion, and SHALL lead the player to vanilla bees for the honeycomb. The bee quests SHALL be optional: the chapter's closing quest MUST NOT depend on them.

#### Scenario: Honeycomb quest
- **WHEN** a player reaches the bee quests
- **THEN** they are asked to harvest honeycomb from a nest or hive and to set honeycomb as the Field Head's anti-corrosion item

#### Scenario: Fields without bees
- **WHEN** a player has scraped a field but skipped the bee quests
- **THEN** the closing quest of The Fields can still be completed

## MODIFIED Requirements

### Requirement: Main chapters
The quest line SHALL contain these chapters in this order: Prologue: Arrival; The Old Works; The Fields; The Cellar; The Power Station; Into the Nether; The Trading House; The Uncle's Workshop; Finale: Beyond the Stone.

#### Scenario: Chapter order
- **WHEN** the quest book is opened
- **THEN** the nine main chapters appear in the listed order in one chapter group

### Requirement: Chapter content
The Fields SHALL cover Farm Rail, Field Head, Shuttle Workshop, Harvester, Spreader, stock levels, rail corrosion with honeycomb from bees, and food variety. The Power Station chapter SHALL cover Powah, Into the Nether SHALL cover Just Dire Things, The Trading House SHALL cover put-away rules, autocrafting and wireless, The Uncle's Workshop SHALL cover Iron Jetpacks, and the Finale SHALL cover Re:Avaritia up to Infinity Armor.

#### Scenario: First harvest
- **WHEN** a player completes the harvest quests of The Fields
- **THEN** they have a field with a Field Head and a Harvester shuttle that brought a crop into the warehouse

#### Scenario: Finale reward
- **WHEN** a player completes the last finale quest
- **THEN** the mystery is resolved in its text and the task is a piece of Infinity Armor

### Requirement: Side chapters
The quest line SHALL contain optional side chapters, in a separate chapter group, for Exploration and Dimensions, Occultism, Apotheosis and Mob Farms, Building and Decor, The Kitchen (Cooking for Blockheads), and Just Dire Things. Side chapters MUST NOT gate main chapters. The Just Dire Things side chapter MUST NOT ask for Just Dire Things generators, energy transmitters, block breakers or block placers, which overlap with Servus Foundation.

#### Scenario: Skipping side chapters
- **WHEN** a player completes no side quest
- **THEN** every main chapter quest is still reachable

#### Scenario: Player detector
- **WHEN** a player reads the Just Dire Things side chapter
- **THEN** one quest asks for the Advanced Sensor and its text explains detecting players in an area
