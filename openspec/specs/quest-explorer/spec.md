# quest-explorer Specification

## Purpose

Lets the pack authors look at the whole quest line, with icons and quest-line findings, without starting Minecraft or a server, so they can review quests and then change the sources in conversation.

## Requirements

### Requirement: Offline explorer build
One command SHALL build the explorer from `quests/` and the server pack's jars into `build/quest-explorer/`. The result SHALL open from disk in a browser, with no server, no network access and no Minecraft.

#### Scenario: Build after a pack build
- **WHEN** the server pack's jars exist and the command runs
- **THEN** `build/quest-explorer/index.html` and its icon files are written, and opening `index.html` from disk shows the quest line

#### Scenario: Jars missing
- **WHEN** the command runs and the server pack's mods folder does not exist
- **THEN** the command fails with a message that names the missing folder and says to build the server pack first

### Requirement: Read only
The explorer build SHALL NOT write to any tracked file. It writes only below `build/`.

#### Scenario: Working tree unchanged
- **WHEN** the command runs on a clean working tree
- **THEN** `git status` shows no changes

### Requirement: Chapter maps
The explorer SHALL show every chapter of the main and side groups, in source order, as its own map. Each quest SHALL sit at its x/y position, with an arrow from each dependency in the same chapter. A dependency on a quest in another chapter SHALL show as a marker with that quest's chapter and title, and selecting it SHALL open that chapter with the quest selected.

#### Scenario: Same-chapter dependency
- **WHEN** `arrival:food` depends on `arrival:workbench`
- **THEN** the Arrival map shows an arrow from the workbench quest to the food quest

#### Scenario: Cross-chapter dependency
- **WHEN** a side quest depends on `arrival:iron-pick`
- **THEN** its map shows a marker "Arrival: Iron from the Hill", and selecting it shows the Arrival map with that quest selected

### Requirement: Quest details
Selecting a quest SHALL show its title, subtitle, description, tasks and rewards (item, count, icon and English name; XP amounts; checkmarks; advancements), its dependencies, and its reference `chapter:slug` in a form that can be copied.

#### Scenario: Reference to copy
- **WHEN** the user selects the food quest in Arrival
- **THEN** the quest popup shows `arrival:food` and a control that copies it

### Requirement: Item icons
Every item in a task, reward or quest icon SHALL show an icon taken from the pack's jars or the Minecraft client jar for the pack's version: flat items as their texture, full blocks as a small three-sided cube. An item whose icon cannot be built SHALL show a placeholder with its item ID instead of failing the build.

#### Scenario: Vanilla item
- **WHEN** a quest rewards `minecraft:wheat_seeds`
- **THEN** the reward shows the wheat seeds texture and the name "Wheat Seeds"

#### Scenario: Unrenderable model
- **WHEN** an item uses a model the explorer cannot draw
- **THEN** it shows a placeholder with the item ID, and the build lists the item in its output

### Requirement: Client jar cache
The Minecraft client jar for the pack's Minecraft version SHALL be downloaded from Mojang once, checked against the published hash, and reused from `build/` on later runs.

#### Scenario: Second run offline
- **WHEN** the client jar was downloaded on an earlier run and there is no network
- **THEN** the build succeeds using the cached jar

### Requirement: Quest-line findings
The explorer SHALL report these findings, as badges on the affected quests and as text lines starting with `chapter:slug`: an item task fully covered by rewards of the quests it depends on (directly or through other quests); an item task partly covered that way; two quests in one chapter at the same position; a main quest that depends on a side quest. Findings SHALL NOT fail the build.

#### Scenario: Auto-complete
- **WHEN** a quest asks for 8 bread and a quest it depends on rewards 8 bread
- **THEN** the quest shows an auto-complete badge, and the command prints a line starting with that quest's `chapter:slug` naming the item and the rewarding quest

#### Scenario: No findings
- **WHEN** the quest line has no findings
- **THEN** no badges show and the command prints that there are no findings
