## MODIFIED Requirements

### Requirement: Alchemy milestones only
The Cellar chapter SHALL contain milestone quests for the four Great Work stages (Nigredo, Albedo, Citrinitas, Rubedo) that point to Paracelsus' Journal, and MUST NOT duplicate the journal's own tasks. Before the milestones, the chapter SHALL ask for the machines in the journal's build order: Calciner, Purifier, Coagulator, Athanor. Each milestone SHALL complete when the player has made a product of that stage's fire: Nigredo with a Salt Crystal Block, and Albedo, Citrinitas and Rubedo with any one of several products that need that fire.

#### Scenario: Stage milestone
- **WHEN** a player reaches a new Athanor stage
- **THEN** one milestone quest completes and its text points to the matching journal chapter

#### Scenario: Machine order
- **WHEN** a player follows the Cellar chapter from the journal quest
- **THEN** the Calciner, Purifier, Coagulator and Athanor quests unlock one after another in that order, and the Nigredo milestone unlocks only after the Athanor quest

#### Scenario: Any product of the fire
- **WHEN** a player with a white Athanor makes a Seed of Copper but no other Albedo product
- **THEN** the Albedo milestone unlocks and its checkmark can be ticked

#### Scenario: Product of a later fire
- **WHEN** a player has only reached the yellow fire
- **THEN** every product option of the Citrinitas milestone can be made, and none of them needs the red fire

#### Scenario: Progress kept
- **WHEN** a player completed `cellar:albedo` before this change
- **THEN** that quest is still complete after the update

## ADDED Requirements

### Requirement: Any-of dependencies
A quest source SHALL be able to declare that a quest unlocks when any one of its dependencies is complete instead of all of them. The Albedo, Citrinitas and Rubedo milestones SHALL use this, each with a checkmark task the player ticks once one product option is done.

#### Scenario: One of three done
- **WHEN** a quest depends on three quests with any-of dependencies and one of them is complete
- **THEN** the quest unlocks and its checkmark can be ticked

#### Scenario: None done
- **WHEN** none of the three option quests is complete
- **THEN** the milestone stays locked

### Requirement: No Sealed Flask rewards
No quest SHALL give a Sealed Flask as a reward, because it is a Rubedo product and would let players skip the Great Work.

#### Scenario: Sealed Flask reward
- **WHEN** a quest source lists `servus_alchemy:sealed_flask` as a reward
- **THEN** the quest check fails and names the quest
