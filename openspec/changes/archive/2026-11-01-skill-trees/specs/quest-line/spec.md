## ADDED Requirements

### Requirement: Skill point rewards
A quest source SHALL be able to reward skill points with a reward naming the tree and the amount. The generated quest SHALL add those points to the player who claims it, without showing command output, and SHALL show a message naming the tree.

#### Scenario: Generated reward
- **WHEN** a quest source has a reward of 1 skill point for `miner`
- **THEN** the generated quest gives the claiming player one Miner point and shows a message that names Miner

#### Scenario: Shown in the explorer
- **WHEN** the quest explorer shows a quest with a skill point reward
- **THEN** the reward is listed with its tree and amount

### Requirement: Valid skill point rewards
The quest check SHALL fail on a skill point reward whose tree is not one of the pack's skill trees, or whose amount is not a positive whole number, and SHALL name the quest.

#### Scenario: Unknown tree
- **WHEN** a quest source rewards skill points for `miners`
- **THEN** the quest check fails and names the quest and the tree

#### Scenario: Zero points
- **WHEN** a quest source rewards 0 skill points
- **THEN** the quest check fails and names the quest
