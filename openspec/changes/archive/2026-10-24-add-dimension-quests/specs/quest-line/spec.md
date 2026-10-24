# Spec Delta

## ADDED Requirements

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
