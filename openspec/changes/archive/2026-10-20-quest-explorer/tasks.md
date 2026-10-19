# Tasks

## 1. Findings

- [x] 1.1 Create `tools/questx/` with `findings.py`: covered and partly covered item tasks (rewards of all quests the quest depends on, directly or through others, naming the rewarding quests), same position in a chapter, main depending on side; each finding is `(chapter, slug, kind, message)`. Verify with `tests/test_questx_findings.py` on small in-memory chapters: 8 bread rewarded upstream of an 8 bread task is covered, 4 is partly covered, a reward on a quest that does not lead to the task is not counted, two quests at one (x, y) are reported, and the current `quests/` has no covered finding

## 2. Assets and icons

- [x] 2.1 Write the client jar download in `assets.py`: Minecraft version from `pack.toml`, manifest → version JSON → `downloads.client`, SHA-1 check, cache at `build/minecraft/client-<version>.jar`, no network when cached. Verify with a test that the cached path skips the network (the download function is passed in), and that a hash mismatch raises an error and leaves no cached file
- [x] 2.2 Write the asset index and model resolution in `assets.py` per design: client jar first, later mod jars win; item definitions (`model`, `condition`/`select`/`range_dispatch`/`composite` first branch or fallback), parent chain with merged `textures` and `#var` references, flat (`item/generated`, `item/handheld`), cube (`cube`, `cube_all`, `cube_column`, `cube_bottom_top`, `orientable`), particle fallback, placeholder. Verify with `tests/test_questx_assets.py` using tiny zip jars built in `tmp_path`, one case per outcome
- [x] 2.3 Add item names from `en_us.json` (`item.<ns>.<id>`, then `block.<ns>.<id>`, else the ID) and copy used textures to `<out>/icons/<ns>/<path>.png`. Verify with a test against a fake jar with a lang file and a texture

## 3. Page and command

- [x] 3.1 Write `page.py`: one `index.html` with the quest data, icon descriptions and findings embedded as JSON, inline CSS/JS, no external URLs. chapter list on the left grouped like the quest book, in source order, nodes at x/y scaled by grid unit and `size`, SVG arrows for same-chapter dependencies, cross-chapter markers that switch the tab and select the target, flat icons and CSS-drawn cubes (strips cropped to the top square), finding badges, a quest popup with title, subtitle, description, tasks, rewards, dependencies and a copy control for `chapter:slug`, selection kept in the URL hash, build time shown. Verify with a test that the page contains every quest reference and no `http` URL
- [x] 3.2 Write `__main__.py`: `python -m tools.questx [--quests] [--mods] [--out]`, failing with a message that names the folder and says to build the server pack first when `--mods` is missing; print findings as `chapter:slug: message` (or `no findings`) and the placeholder items; exit 0. Verify with a test for the missing mods folder, then run the command on the real pack and check that `git status` is unchanged
- [x] 3.3 Document the command in `docs/development.md` under "Quests" (what it reads, where the page lands, the one-time client jar download). Verify the documented command runs as written

## 4. Check in the browser

- [x] 4.1 Open `build/quest-explorer/index.html` from disk and check: every chapter tab shows its quests and arrows, Arrival's first quest shows the seeds, carrot and potato icons with their names, a block reward (for example `minecraft:chest` in Old Works) shows a cube, a side quest's marker jumps to `arrival:iron-pick`, and `#arrival:food` in the URL opens that quest after a reload. Note any items with bad icons in the summary
- [x] 4.2 Run `python -m pytest`, `python -m tools.checks.pack_check` and `python -m tools.checks.quest_check --mods build/server/mods`; verify all pass
