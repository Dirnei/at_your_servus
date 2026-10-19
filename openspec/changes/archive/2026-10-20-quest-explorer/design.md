# Design

## Context

- Quest sources load through `tools/questgen/model.py` (`load_sources`, `Chapter`, `Quest`, `dep_keys`). The explorer reuses it, so it sees exactly what the generator sees.
- `build.ps1` leaves the server pack's jars in `build/server/mods/` (106 jars today). `tools/checks/item_ids.py` already reads item definitions from them. Client-only mods add no items, so these jars cover every quest item except vanilla.
- The vanilla server jar has no assets. Textures and `en_us.json` for vanilla are only in the client jar, which Mojang's version manifest lists for 26.1.2 (`piston-meta.mojang.com`).
- A survey of the item models in the mod jars: about 1,800 are flat (`item/generated`, `item/handheld`), about 1,500 are full cubes (`cube`, `cube_all`, `cube_column`), and about 3,000 are slabs, stairs, roofs and other custom shapes. Some use `minecraft:condition`/`select` item definitions. The quests reference only about 200 distinct items.
- Python standard library only (see `pyproject.toml`); there is no PNG decoder.

## Goals / Non-Goals

**Goals:**
- One command, one static folder, opened from disk.
- Icons that are right for flat items and full blocks; a readable fallback for everything else.
- Findings logic that can be unit tested without jars.

**Non-Goals:**
- Editing quests (edits happen in the TOML, in conversation).
- Recipe or progression analysis ("can the player make X here?").
- Tint colors (grass, leather, spawn eggs), animated textures, special item renderers, 3D models other than full cubes.
- Running in CI or shipping in either pack.

## Decisions

**Package `tools/questx/`**, run as `python -m tools.questx [--quests quests] [--mods build/server/mods] [--out build/quest-explorer]`. It has four modules: `findings.py` (pure, works on `Chapter` lists), `assets.py` (jar index, client jar, model resolution, lang names), `page.py` (HTML writer) and `__main__.py`. The defaults follow `quest_check`'s flags. *Alternative:* adding it to `tools/questgen`. Rejected, because the generator is part of the release path and the explorer is not.

**One `index.html` with the data embedded, icons as files.** The quest data goes into the page as `<script type="application/json">`, because `fetch` does not work from `file://`. Plain JS and CSS are inline, with no CDN, so the page works offline. Icon textures are copied to `icons/<ns>/<path>.png`, because `<img src>` works from `file://`. *Alternative:* inlining the icons as data URIs. Rejected: separate files keep the HTML readable and diffable while working on the page, and about 200 icons fit either way.

**Asset index over all jars.** It maps each `assets/...` path to the jar holding it: the client jar first, then the mod jars in sorted order, with later jars winning, as resource packs do. Model resolution for an item:
1. Item definition `assets/<ns>/items/<id>.json`. For `minecraft:model`, take its model. For `condition`/`select`/`range_dispatch`/`composite`, take the first branch or the fallback, recursively, until a plain model is found.
2. Walk the `parent` chain and merge `textures`, resolving `#var` references.
3. If the chain reaches `item/generated` or `item/handheld`, the icon is flat: `layer0`.
4. If it reaches `block/cube`, `cube_all`, `cube_column`, `cube_bottom_top` or `orientable`, the icon is a cube with `up` and two side faces (`north` or `side`, `south` or `side`; `all` for every face).
5. Otherwise the icon is flat from the `particle` texture, if there is one.
6. Otherwise a placeholder, and the item is listed in the command's output.

**The cube is drawn in the browser.** The three face PNGs are placed with CSS transforms (top, left, right, with the side faces slightly darkened by a CSS filter). That needs no image processing in Python. Animated texture strips (taller than wide) are shown as the top square through `object-fit: cover; object-position: top`.

**Item names** come from `assets/<ns>/lang/en_us.json`, trying `item.<ns>.<id>` and then `block.<ns>.<id>`. Without a match, the item ID is shown.

**Client jar.** The Minecraft version is read from `pack.toml` `[versions] minecraft`. The command downloads the version manifest, then the version JSON, then `downloads.client`, and checks the SHA-1 against the version JSON. The file is cached as `build/minecraft/client-<version>.jar`. If the cache exists, no network is used. *Alternative:* reading the jar from a local launcher install. Rejected: the path differs per machine, and the jar may not be the right version.

**Findings** (`findings.py`) work only on the loaded chapters:
- *covered / partly covered*: for each quest, add up the item rewards of all quests it depends on, directly or through other quests. Each item task is compared with that total; the finding names the rewarding quests.
- *same position*: two quests in one chapter with equal (x, y).
- *main depends on side*: same rule as `quest_check`, reported here for the badge.

Each finding is `(chapter, slug, kind, message)`. The command prints `chapter:slug: message`, one per line, or `no findings`. Exit code 0 either way.

**Map layout** uses the quest x/y in the same orientation as FTB Quests (y grows downward), with a fixed number of pixels per grid unit, and the `size` field scales the node. Same-chapter dependencies become SVG lines under the nodes. Cross-chapter dependencies are a small marker left of the quest; clicking it switches the tab and selects the target. Chapters are listed on the left, grouped like the quest book ("The Huber Farm", "Side Chapters", with the group icons from `tools/questgen/generate.py`). Clicking a quest opens a popup over the map, as in-game: tasks and rewards side by side, then dependencies and what it unlocks; Esc or a click outside closes it. The selected quest is kept in the URL hash (`#arrival:food`), so a reload or a pasted link opens the same quest.

## Risks / Trade-offs

- [Tinted items show gray (grass, leaves, leather armor, spawn eggs)] → Accepted for a planning view; the name next to the icon is still correct.
- [Custom-shaped blocks (slabs, stairs, Servus machines with Blockbench models) show as a flat particle texture] → Clearly an approximation, but still recognizable; the build lists the placeholders so the worst ones are visible.
- [Model or item definition formats change between Minecraft versions] → Resolution falls through to the particle texture or a placeholder instead of failing, and tests cover each step with tiny fake jars.
- [Downloading Mojang's client jar] → Only to `build/` for local use, never committed or packed.
- [The explorer shows stale data after a TOML edit] → The page shows its build time; rerun the command.
