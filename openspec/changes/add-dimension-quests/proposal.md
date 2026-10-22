# Proposal

## Why

The side chapter Exploration and Dimensions has one quest per dimension: a player who enters the Twilight Forest, the Undergarden or the Bumblezone gets one task and is then on their own, and The End has no quest at all. Each of these dimensions has its own progression (bosses, ores, gear) that the quest book can guide.

## What Changes

- Extend the side chapter **Exploration and Dimensions** (`quests/side/01-exploration.toml`) with one branch per dimension:
  - **Twilight Forest**: the boss progression (Naga, Lich, Minoshroom, Hydra, Knight Phantoms, Ur-Ghast; Alpha Yeti and Snow Queen as a second line), with ironwood, steeleaf and fiery gear on the side.
  - **Undergarden**: catalyst, cloggrum, froststeel, utherium, regalium, the Forgotten Guardian and forgotten metal.
  - **Bumblezone**: bee bread, honey compass, stinger spear, royal jelly, Essence of the Bees.
  - **The End** (new): enter, kill the dragon, find an End City, take an Elytra.
- The existing quests `twilight`, `undergarden` and `bumblezone` stay, with their slugs, as the first quest of their branch; their tasks change to fit the start of the branch.
- No other chapter changes. No main quest depends on the new quests.

## Capabilities

### New Capabilities

### Modified Capabilities
- `quest-line`: the Exploration and Dimensions side chapter gains a requirement for a branch per dimension.

## Impact

- `quests/side/01-exploration.toml` and the generated `config/ftbquests/quests/`.
- No mod, recipe or config change.
