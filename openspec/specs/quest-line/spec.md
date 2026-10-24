# quest-line Specification

## Purpose
Defines the pack's guided FTB Quests line: a story told in the great-uncle's letters that leads players through the Servus mods first and the other mods second.

## Requirements

### Requirement: Story frame
The quest line SHALL tell the story of a player who inherits a great-uncle's land in the Bavarian mountains above Berchtesgaden, where the house has sunk into the mountain and the player builds everything again. Story texts are the uncle's letters and notes in plain English, and each letter opens with "Servus, ...". A mystery about the uncle's fate runs through the chapters and is resolved in the finale.

#### Scenario: First letter
- **WHEN** a player opens the quest book for the first time
- **THEN** the first quest is the uncle's first letter, starting with "Servus,"

### Requirement: Story bible
The repository SHALL contain a story document with the uncle, the estate, the mystery's beats per chapter and the ending, which all quest texts follow.

#### Scenario: Consistent names
- **WHEN** a quest text names a person or place
- **THEN** that name matches the story document

### Requirement: Main chapters
The quest line SHALL contain these chapters in this order: Prologue: Arrival; The Old Works; The Fields; The Cellar; The Power Station; Into the Nether; The Trading House; The Uncle's Workshop; Finale: Beyond the Stone.

#### Scenario: Chapter order
- **WHEN** the quest book is opened
- **THEN** the nine main chapters appear in the listed order in one chapter group

### Requirement: Early warehouse
The Old Works chapter SHALL teach Foundation's Utility Duct, Fluid Tank, pump and Coal Generator and SHALL build a first warehouse: Heavy Duty Rack, Warehouse Rail, Shuttle Garage, Mk1 Shuttle, Warehouse Controller powered by the Coal Generator, Data Cable, Packing Station, and Storage Terminal. The Data Cable and Packing Station quests SHALL come before the Storage Terminal quest, and their texts SHALL say that the terminal reaches the warehouse over the data cable and through a Packing Station. No quest in the chapter SHALL ask for a block the chapter's machines don't need.

#### Scenario: Warehouse before Powah
- **WHEN** a player completes The Old Works
- **THEN** they own a working warehouse, and no quest in that chapter requires a Powah item

#### Scenario: Terminal works when its quest unlocks
- **WHEN** the Storage Terminal quest unlocks
- **THEN** the player has already been asked for a Data Cable and a Packing Station, and a terminal connected the way the quests describe lists the racks' contents

#### Scenario: Coal Generator quest
- **WHEN** a player opens the Coal Generator quest
- **THEN** it asks for the Coal Generator and not for a Chimney

### Requirement: Alchemy milestones only
The Cellar chapter SHALL contain milestone quests for the four Great Work stages (Nigredo, Albedo, Citrinitas, Rubedo) that point to Paracelsus' Journal, and MUST NOT duplicate the journal's own tasks.

#### Scenario: Stage milestone
- **WHEN** a player reaches a new Athanor stage
- **THEN** one milestone quest completes and its text points to the matching journal chapter

### Requirement: Crossing Alchemy and the warehouse
The quest line SHALL contain quests that combine Alchemy and Shuttles, including storing a first Alchemy product in the warehouse and ordering an Alchemy product on demand through the Crafting CPU.

#### Scenario: On-demand order
- **WHEN** a player reaches the on-demand quest in The Trading House
- **THEN** its task requires a Crafting CPU and a Machine Adapter or Production Terminal set up for an Alchemy machine

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

### Requirement: Storage questions go to Shuttles
Quests that teach storage or autocrafting SHALL use Shuttles. Sophisticated Storage, Sophisticated Backpacks and Functional Storage MAY appear only in side or optional quests.

#### Scenario: Storage quest
- **WHEN** a main chapter quest asks for storage
- **THEN** it asks for a Shuttles block

### Requirement: Quest task style
Quest tasks SHALL mostly be "obtain or do something for the first time". Item tasks MUST NOT ask for more than 16 of an item unless the item is a bulk material. Rewards SHALL be useful items for the next step; no random loot tables in main chapters.

#### Scenario: Count limit
- **WHEN** the quest check runs
- **THEN** it reports every item task asking for more than 16 of a non-bulk item

### Requirement: Stable quest identities
Every chapter and quest SHALL keep the same ID across rebuilds as long as its source slug is unchanged, so player progress survives pack updates.

#### Scenario: Regenerate without changes
- **WHEN** the quest files are generated twice from the same sources
- **THEN** the output is byte-identical

#### Scenario: Text edit
- **WHEN** only a quest's text changes
- **THEN** the quest's ID is unchanged

### Requirement: Translatable texts
All quest and chapter titles, subtitles and descriptions SHALL be English and stored as translation entries, so a German translation can be added without touching quest structure.

#### Scenario: Missing translation entry
- **WHEN** a quest or chapter has no English title entry
- **THEN** the quest check fails and names it

### Requirement: Valid references
Every item referenced by a quest task, reward or icon SHALL exist in the pack.

#### Scenario: Unknown item
- **WHEN** a quest references an item ID no mod in the pack provides
- **THEN** the quest check fails and names the quest and the ID

### Requirement: Quest book on first join
A player joining the world for the first time SHALL receive the FTB Quests book once.

#### Scenario: Second join
- **WHEN** the same player joins again
- **THEN** no second book is given

### Requirement: Ampersands shown as written
Quest and chapter titles, subtitles and descriptions SHALL show an `&` from the quest sources as a plain `&` in the quest book, and MUST NOT make FTB Quests report a formatting error.

#### Scenario: Company name
- **WHEN** a player opens the quest "A Merchant Needs a Warehouse"
- **THEN** its text shows "Huber & Co., since 1521" and no "Invalid formatting" message

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

### Requirement: Dimension branches
The side chapter Exploration and Dimensions SHALL have a branch of quests for each of the Twilight Forest, the Undergarden, the Bumblezone and The End, each following that dimension's own progression from entering it to its strongest boss or gear. The existing first quest of a dimension SHALL keep its slug and start its branch. No main chapter quest SHALL depend on a quest of these branches.

#### Scenario: Twilight Forest bosses
- **WHEN** a player has entered the Twilight Forest and defeated the Naga
- **THEN** the next quest asks for the Lich, and later quests lead on through the Minoshroom, the Hydra, the Knight Phantoms and the Ur-Ghast

#### Scenario: The End
- **WHEN** a player has finished the Nether's blaze quest
- **THEN** the End branch opens and asks the player to enter The End, kill the dragon, find an End City and bring back an Elytra

#### Scenario: Progress kept
- **WHEN** a player completed `exploration:twilight` before this change
- **THEN** that quest is still complete after the update
