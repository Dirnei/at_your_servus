# Spec Delta

## ADDED Requirements

### Requirement: Ampersands shown as written
Quest and chapter titles, subtitles and descriptions SHALL show an `&` from the quest sources as a plain `&` in the quest book, and MUST NOT make FTB Quests report a formatting error.

#### Scenario: Company name
- **WHEN** a player opens the quest "A Merchant Needs a Warehouse"
- **THEN** its text shows "Huber & Co., since 1521" and no "Invalid formatting" message

## MODIFIED Requirements

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

### Requirement: Chapter content
The Power Station chapter SHALL cover Powah, Into the Nether SHALL cover Just Dire Things, The Trading House SHALL cover put-away rules, autocrafting, field work and wireless, The Uncle's Workshop SHALL cover Iron Jetpacks, and the Finale SHALL cover Re:Avaritia up to Infinity Armor.

#### Scenario: Finale reward
- **WHEN** a player completes the last finale quest
- **THEN** the mystery is resolved in its text and the task is a piece of Infinity Armor
