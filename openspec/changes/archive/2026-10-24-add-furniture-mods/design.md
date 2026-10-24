# Design

## Context

Mods are added with `packwiz cf add`; every mod must come from CurseForge, and every mod has a row in `docs/mods.md` (a test checks this). The changelog lists `feat` commits and, separately, the mods added since the last release.

Checked on CurseForge: Adorn 8.0.0 for 26.1.x, `bibliocraft-26.1.2-1.7.1.jar`, `fantasyfurniture-26.1.7.jar`, all NeoForge 26.1.2. Their required libraries are not known yet; `packwiz cf add` lists them.

## Goals / Non-Goals

**Goals:**
- Three furniture mods, each in its own commit with the libraries it needs.

**Non-Goals:**
- Quests, recipe changes or gates for the new furniture.
- Removing Macaw's Furniture or any other building mod.

## Decisions

- **One change, three commits.** The tasks have one section per mod; each section ends with the checks and a commit, so every commit is a working pack. Alternative: one commit for all three. Rejected: the changelog would show one entry for three mods. The change folder goes into the first commit; archiving is a later `chore(openspec)` commit, as for earlier changes.
- **Libraries go with the first mod that needs them.** A library shared by two of the mods is committed with the first one, and the later commit only adds its name to the library's row in `docs/mods.md`.
- **Both sides.** All three add blocks and block entities, so the server needs them; `packwiz cf add` sets the side from CurseForge, and the task checks it is `both`.
- **Commit messages:** `feat: add Adorn furniture`, `feat: add Bibliocraft Legacy furniture`, `feat: add Fantasy's Furniture`.

## Risks / Trade-offs

- [A mod pulls in a library from outside CurseForge or one that competes with a Servus mod] → `pack_check --public` and the excluded-mods list catch it; if it fails, stop and report.
- [Recipe or tag conflicts with Macaw's or with Servus recipes] → check the test server's KubeJS log for "with 0 failed recipes" and look at the server log for registry errors after each mod.
- [Adorn's 26.1 build is new, about 1K downloads] → the in-game test covers it; if it breaks, its commit can be reverted alone.
