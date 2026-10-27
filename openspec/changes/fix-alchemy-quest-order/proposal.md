## Why

The Cellar chapter teaches Alchemy in the wrong order. Paracelsus' Journal builds Calciner, Purifier, Coagulator and only then the Athanor, whose fire is upgraded three times (white ring, yellow ring, red crown). The quests skip the Purifier, put the Coagulator after the Athanor as the Nigredo task, and check each fire with fixed items, one of which (the Receptaculum) belongs to a later fire. A Trading House quest also hands out Sealed Flasks, a Rubedo product, which lets players skip ahead.

## What Changes

- The Cellar chapter follows the journal's build order: journal, Calciner, Purifier (new quest), Coagulator (new quest), Athanor.
- Nigredo completes with the first black-fire product, a Salt Crystal Block.
- Albedo, Citrinitas and Rubedo each complete when the player has made **any one** of a few products of that fire (seeds of that fire's veins, and fire-specific Athanor crafts). Each option is a small quest; the stage hexagon unlocks as soon as one of them is done, and the player ticks its checkmark.
- Rubedo's old Prelum and Caput Mortuum tasks and Citrinitas' Receptaculum task move to follow-up quests after Rubedo.
- The quest generator gains an "any one of the dependencies" option (FTB Quests `dependency_requirement: one_completed`).
- The Sealed Flask is never a quest reward. The `trading-house:alchemy-order` reward changes to emeralds, and the quest check fails on any Sealed Flask reward.
- The Nether chapter is no longer gated: `nether-letter` loses its dependency on `power-station:energized-steel`, so the letter and the Primal Goo quest behind it are open from the start. The letter rewards XP instead of golden carrots. It completes when the player looks at a lit Nether portal, through a new `observation` task type in the quest generator. The Cellar needs the Nether (Ghast Tear, salamander) before the Power Station is reached, and the Nether chapter does not use Powah.
- Existing slugs (`calciner`, `athanor`, `nigredo`, `albedo`, `seed`, `salt-in-the-racks`, `citrinitas`, `rubedo`) stay, so player progress is kept.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `quest-line`: the Alchemy milestone requirement changes to the journal's build order and any-of stage outputs; new requirements for any-of dependencies in quest sources and for never rewarding a Sealed Flask.

## Impact

- `quests/chapters/04-cellar.toml`, `quests/chapters/07-trading-house.toml`, and the generated `config/ftbquests/quests/`.
- `tools/questgen/model.py`, `tools/questgen/generate.py`, `tools/questgen/FORMAT.md` (new quest key).
- `tools/checks/quest_check.py` and `tests/test_quest_check.py`, `tests/test_generate.py`.
- `quests/chapters/06-nether.toml`: `nether-letter` loses its dependency and its golden carrot reward. Its Salamander quest still depends on `cellar:albedo`, whose slug stays.
