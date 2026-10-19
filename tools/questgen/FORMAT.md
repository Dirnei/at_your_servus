# FTB Quests 26.1.2.9 on-disk format (NeoForge 26.1.2)

Source: github.com/FTBTeam/FTB-Quests, tag `v26.1.2.9` (`gradle.properties`: `minecraft_version=26.1.2`,
`mod_version=9`). The jar's `neoforge.mods.toml` reports `version = "26.1.2.9"`. Paths below are relative
to `common/src/main/java/dev/ftb/mods/ftbquests/`.

## 0. The format is JSON5, not SNBT

CHANGELOG `[26.1.2.1]`: *"All quest and progress data is now saved in Json5 format; SNBT is no longer used"*.
`BaseQuestFile.FILE_SUFFIX = Json5Util.FILE_EXT = ".json5"` (ftb-library 26.1.2.9, `dev.ftb.mods.ftblibrary.json5.Json5Util`).
The loader only lists `*.json5`, and the source has no SNBT import path, so **`.snbt` files are ignored without any warning**.
(`tools/questgen/snbt.py` targets the old format and is wrong for this version.)

- The parser is `de.marhali.json5` (json5-java 3.0.0). Plain JSON is valid input. Comments, unquoted keys and trailing commas also parse.
- Numbers have **no type suffixes**: write `0`, `1.5`, `-3.0`, never `0.0d`, `1L` or `1b`. Ints and doubles can be swapped
  (`Json5Util.getInt/getDouble` only check `isNumber()`).
- Booleans **must** be `true`/`false` (`getBoolean` checks `isBoolean()`, so `1`/`1b` count as missing).
- Strings are JSON strings. Item stacks are nested objects in vanilla Codec form (section 6).
- Files are written as UTF-8 (`Json5Util.save`, `Files.writeString(..., UTF_8)`). Write UTF-8 without a BOM.

## 1. Folder layout (`ServerQuestFile#<init>`, `BaseQuestFile#readDataFull`)

```
config/ftbquests/quests/
  data.json5                    # quest-file root object (required)
  chapter_groups.json5          # optional
  chapters/<filename>.json5     # one per chapter; every *.json5 in the folder is loaded
  reward_tables/<filename>.json5
  lang/<locale>/**/*.json5      # e.g. lang/en_us/chapters/getting_started.json5
```
- `chapters/` and `reward_tables/` filenames get lower-cased on load (`checkAndFixFileCase`). Case-clashing older files are renamed `.OLD`.
  **Use lowercase filenames.**
- Lang (`TranslationManager#loadFromFile`, `TranslationTable#loadAndCombine`): each **directory** under `lang/` whose name matches
  `^\w+$` is one locale. Every `*.json5` under it (recursively, via `Files.walk`) is merged into one flat key->value map, so the layout
  inside a locale folder does not matter for loading. A flat `lang/en_us.json5` or `lang/en_us.snbt` file is **ignored**.
- The layout FTBQ writes itself (`TranslationTable#splitAndSerialize`/`getPathForQuestObject`): quest, task and quest_link keys go to
  `lang/<locale>/chapters/<chapter filename>.json5`. Every other object goes to `lang/<locale>/<type>.json5`, e.g. `chapter.json5`,
  `chapter_group.json5`, `reward.json5`, `reward_table.json5`, `file.json5`. Copy this layout so a later in-game save does not move keys around.

### Translation keys (`TranslationManager#makeKey`, `TranslationKey`, `QuestObjectType`)
Key = `<objectType>.<16-hex ID>.<subkey>`. objectType is one of `file chapter quest task reward reward_table chapter_group quest_link image`.

| subkey             | value type      | used by |
|--------------------|-----------------|---------|
| `title`            | string          | any object (chapter, quest, task, reward, group, table) |
| `quest_subtitle`   | string          | quest |
| `quest_desc`       | list of strings | quest (one entry per line, `""` = blank line, `"{@pagebreak}"` = page break) |
| `chapter_subtitle` | list of strings | chapter |

```json5
// lang/en_us/chapters/getting_started.json5
{
  "quest.1A2B3C4D5E6F7081.title": "Punch a Tree",
  "quest.1A2B3C4D5E6F7081.quest_subtitle": "Every journey starts somewhere",
  "quest.1A2B3C4D5E6F7081.quest_desc": ["Get some &alogs&r.", "", "{@pagebreak}", "Page two."],
  "task.2B3C4D5E6F708192.title": "Any log"
}
// lang/en_us/chapter.json5
{ "chapter.0F00000000000001.title": "Getting Started", "chapter.0F00000000000001.chapter_subtitle": ["The basics"] }
// lang/en_us/chapter_group.json5
{ "chapter_group.0E00000000000001.title": "Early Game" }
```
Lookup (`getStringTranslation`): the requested locale's table, then `fallback_locale` from data.json5 (default `en_us`).
Text is FTB raw text with `&` colour codes. A string wrapped in `{...}` or `[...]` is parsed as a JSON text component (`util/TextUtils`).

## 2. data.json5 (`BaseQuestFile#writeDataFull` / `#readData`)
`readData` calls `orElseThrow()`/`get().getAsString()` on the keys marked (R). A missing (R) key throws out of `readDataFull`.
`ServerQuestFile#load` catches it and logs "failed to load quest data", which **aborts loading the entire quest book**.
```json5
{
  "version": 13,                          // (R) BaseQuestFile.VERSION; other values mark the book dirty -> rewritten on save
  "default_reward_team": false,           // (R)
  "default_consume_items": false,         // (R)
  "default_autoclaim_rewards": "disabled",// (R) disabled|enabled|no_toast|invisible
  "default_quest_shape": "circle",        // (R) circle|square|rsquare|diamond|pentagon|hexagon|octagon|heart|gear|none
  "default_quest_disable_jei": false,     // (R)
  "drop_loot_crates": false,              // (R)
  "emergency_items_cooldown": 300,
  "grid_scale": 0.5, "pause_game": false, "lock_message": "", "progression_mode": "linear", // linear|flexible
  "detection_delay": 20, "show_lock_icons": false, "drop_book_on_death": false,
  "hide_excluded_quests": false, "fallback_locale": "en_us", "verify_on_load": false, "disable_gui": false
}
```
Optional: `icon`, `tags`, `disable_toast`, `emergency_items` (list of item objects), `loot_crate_no_drop`, `presets`,
`preset`, `suppress_all_autoclaiming`. When `presets` is missing, the server uses `VisualPresets.makeDefaults()`.

## 3. chapter_groups.json5 (`BaseQuestFile#writeChapterGroupsFile`, `#readChapterGroupsFile`)
`ChapterGroup` has no `writeData` of its own, so a group has only `id` plus the base keys `icon`, `tags` and `disable_toast`.
The list order is the display order. The default (ungrouped) group is implicit and never listed.
```json5
{ "chapter_groups": [ { "id": "0E00000000000001", "icon": { "id": "minecraft:iron_pickaxe", "count": 1 } } ] }
```

## 4. Chapter file (`BaseQuestFile#writeChapterJsonFiles`, `Chapter#writeData/readData`)
```json5
{
  "id": "0F00000000000001",
  "group": "0E00000000000001",   // "" = default group; unknown ID also falls back to default (getChapterGroup)
  "order_index": 0,              // sort order inside the group
  "filename": "getting_started", // REQUIRED (orElseThrow); keep == file basename (sanitized: [a-z0-9_])
  "icon": { "id": "minecraft:oak_log", "count": 1 },
  "default_quest_shape": "",     // "" = use data.json5 default
  "default_hide_dependency_lines": false,
  "quests": [ /* section 5 */ ],
  "quest_links": [ { "id": "...", "linked_quest": "<quest hex id>", "x": 2.0, "y": 0.0 } ], // + optional shape, size
  "images": []
}
```
Optional chapter keys: `always_invisible`, `default_quest_size` (default 1.0), `default_min_width`, `progression_mode`
(`default|linear|flexible`), `consume_items` (tristate), `hide_quest_details_until_startable`, `hide_quest_until_deps_visible`,
`hide_quest_until_deps_complete`, `hide_text_until_complete`, `default_repeatable_quest`, `require_sequential_tasks`, `preset`, `autofocus_id`, `tags`.
The chapter is first built with the filename taken from the path, then `readData` replaces it with `"filename"`. A later save writes
to `chapters/<filename>.json5` and does not delete the old file, so a mismatch leaves a duplicate.
A chapter's `readData` errors are caught and logged per object, so a broken chapter does not stop the rest from loading.

**Tristate keys** (`ftblibrary Tristate#write/read`): leave the key out for DEFAULT, or write `true`/`false`.

## 5. Quest object (`Quest#writeData/readData`, `Quest#writeDataFull`)
```json5
{
  "id": "1A2B3C4D5E6F7081",
  "x": 0.0, "y": 0.0,                         // REQUIRED (orElseThrow), doubles, grid units
  "dependencies": ["0123456789ABCDEF"],       // list of hex-ID strings (FTBQCodecs.QUEST_ID_CODEC)
  "icon": { "id": "minecraft:oak_log", "count": 1 },
  "shape": "hexagon",                         // omit = chapter/file default
  "size": 1.5,                                // omit -> 1.0 (clamped 0..MAX)
  "optional": true,
  "hide_dependency_lines": true,              // tristate
  "tasks": [ /* section 6 */ ],
  "rewards": [ /* section 7 */ ]
}
```
More keys: `guide_page`, `hide_dependent_lines`, `min_required_dependencies`, `dep_control_pts`, `disable_recipe_mod`(T),
`hide_until_deps_visible`(T), `hide_until_deps_complete`(T), `dependency_requirement` (`all_completed`(default)|`one_completed`|
`all_started`|`one_started`), `hide_text_until_complete`(T), `icon_scale`, `min_width`, `can_repeat`(T), `invisible`,
`invisible_until_tasks`, `ignore_reward_blocking`, `progression_mode`, `hide_details_until_startable`(T),
`require_sequential_tasks`(T), `hide_lock_icon`, `max_completable_dependents`, `repeat_cooldown`, `preset`, `disable_toast`, `tags`.
(T) = tristate. **There is no title/subtitle/description key here. All text lives in lang (section 9).**

## 6. Tasks (`Quest#writeTasks`, `BaseQuestFile#readQuestsFromChapterJson`, `quest/task/*`)
Every task has `"id"` and `"type"`. The type is the registry path without `ftbquests:`. `"ftbquests:item"` also works
(`FTBQUtils.modDefaultedId`). An unknown type throws `IllegalArgumentException`, which aborts the whole load.
Base keys: `optional_task`, `icon`, `tags`, `disable_toast`.

**Item stacks** use the vanilla 26.1.2 `ItemStack.CODEC`, verified with javap on `server-26.1.2.jar`. Fields: `id` (required),
`count` (`fieldOf("count").orElse(1)`, range 1..99), and `components` (optional `DataComponentPatch`). They are an **object, never a bare string**:
```json5
{ "id": "ftbquests:item_task_id", "type": "item",
  "item": { "id": "minecraft:oak_log", "count": 1 },   // ItemTask writes copyWithCount(1)
  "count": 16,                                        // long, omit when 1
  "consume_items": true }                             // tristate; also only_from_crafting(T),
                                                      // match_components: none|fuzzy|strict, task_screen_only
// with data components: "item": { "id": "minecraft:potion", "count": 1, "components": { "minecraft:potion_contents": {...} } }
{ "id": "...", "type": "checkmark" }                                       // no extra keys
{ "id": "...", "type": "advancement", "advancement": "minecraft:story/mine_stone", "criterion": "" } // both REQUIRED
{ "id": "...", "type": "kill", "entity": "minecraft:zombie", "value": 10 } // + entityTypeTag, custom_name
{ "id": "...", "type": "gamestage", "stage": "iron_age" }                  // + team_stage; stage REQUIRED
{ "id": "...", "type": "observation", "timer": 0, "observation_type": "block", "to_observe": "minecraft:diamond_ore" }
//   observation_type: block|block_tag|block_state|block_entity|block_entity_type|entity_type|entity_type_tag (REQUIRED)
```
Other registered types: `custom xp dimension stat location biome structure fluid interaction`.
`gamestage` checks stages through ftb-library's `StageHelper` provider.

## 7. Rewards (`Quest#writeRewards`, `quest/reward/*`)
Base keys (`Reward#writeData`): `team_reward` (tristate), `auto` (`default|disabled|enabled|no_toast|invisible`),
`exclude_from_claim_all`, `ignore_reward_blocking`, `disable_reward_screen_blur`.
```json5
{ "id": "...", "type": "item", "item": { "id": "minecraft:bread", "count": 1 }, "count": 8 } // + random_bonus, only_one
{ "id": "...", "type": "xp", "xp": 100 }              // REQUIRED key
{ "id": "...", "type": "xp_levels", "xp_levels": 5 }
{ "id": "...", "type": "command", "command": "/say {p} did it"   /* {p} = player name; default "/say Hi, @p!" */, "permission_level": 2, "silent": true } // + feedback_message
```
Other types: `choice random all_table loot`. These reference `table_id`, which is read with `getLong`, so it is a **JSON number** (the decimal long), not hex, `advancement toast gamestage currency custom`.
In a reward-table file the `type` is left out when it is `item` (`RewardTable#writeData`). The table also has `loot_size` and `rewards`, and optionally `weight`.

## 8. IDs and number typing
- ID = signed 64-bit long, written as a **16-character uppercase zero-padded hex string** (`QuestObjectBase.getCodeString`: `"%016X"`).
- Parsed with `Long.parseLong(s, 16)` (`BaseQuestFile#readID`), optionally with a leading `#`. **The first hex digit must be 0-7**:
  `FFFF...` overflows, fails to parse and is silently replaced by a random ID. IDs `0` and `1` are reserved (1 = the file). FTBQ generates
  IDs with `nextLong(Long.MAX_VALUE)`.
- A duplicate ID (already in `questObjectMap`), an unparseable ID or a missing ID gets a **new random ID** and marks the book dirty.
  Lang keys for the old ID are then orphaned and dropped on the next save. Keep IDs globally unique across every object type.
- Numeric (non-string) IDs are accepted but mark the book dirty. Always write strings.
- Deterministic generation: derive e.g. `sha1(name)[:16]` and clear the top bit (`& 0x7FFFFFFFFFFFFFFF`), then check for collisions.

## 9. Inline text vs lang files
Titles, subtitles and descriptions are read **only** from the translation tables. `getRawTitle()` -> `TranslationManager.getStringTranslation`.
`Quest#getRawDescription`/`Chapter` subtitle read the same way. No `readData` reads `title`, `subtitle` or `description`.
An inline `"title": "..."` in a chapter or quest file is **ignored** and is lost the next time FTBQ saves.
The one inline exception: reward-table rewards and create-packets may carry `{"locale":"en_us","translate":{"title":"..."}}`
(`TranslationManager#processInitialTranslation`). That is for network create-ops, not hand-written files. With no title, FTBQ shows an
auto-generated alt title (for example the task item name).

## 10. Server loading and client sync
- Path: `Platform.paths().configPath()/ftbquests/quests`. On a dedicated server that is `<server>/config/ftbquests/quests`.
  **There is no world-local copy of the quest book.** `world/ftbquests/` holds only team progress (`<uuid>.json5`, `TeamData`).
- Load: `FTBQuestsEventHandler#serverAboutToStart` -> `ServerQuestFile.startup`. Then `#serverStarted` -> `load(true, true)`,
  which runs `readDataFull` only if the folder exists.
- Vanilla `/reload` does **not** reload quests. Use `/ftbquests reload [quests|team_progress]` (`command/ReloadCommand`, needs the editor
  permission). It reloads from disk, sends `SyncQuestsMessage` to every player, and resends translations.
- Save-back: `onWorldSaved`/shutdown -> `saveNow()`. If the book is dirty (version != 13, re-IDs, edits) it **rewrites every file**
  in canonical form, with sorted keys and default values left out. Lang tables are rewritten only when they changed.
  Generated files should therefore match the canonical form, or they will churn on the first save.
- Clients never read the config folder. On login (`ServerQuestFile#playerLoggedIn`) the server sends `SyncQuestsMessage` (the full
  book, via `BaseQuestFile.STREAM_CODEC`/`writeNetData`) and `SyncTranslationTableMessage` for `en_us`, the `fallback_locale`
  and the player's client language (`TranslationManager#sendTranslationsToPlayer`). Clients without the matching quest files see the server's book.
