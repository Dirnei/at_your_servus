# Tasks

## 1. Adorn

- [x] 1.1 Run `packwiz cf add` for Adorn (the 8.0.0 file for 26.1.x) and any library it pulls in; check every new metafile is from CurseForge with side `both` (or `client` only for a library CurseForge marks client-only)
- [x] 1.2 Add a row for Adorn under "Utility and building" in `docs/mods.md`, and a row under "Libraries" for each new library; run `packwiz refresh`; verify `python -m pytest`, `python -m tools.checks.pack_check --public` and `python -m tools.checks.quest_check --quests quests --mods server/local-data/mods` pass
- [x] 1.3 Restart the test server (`docker compose restart mc`); verify it reaches "Done" and the KubeJS log says "with 0 failed recipes"; commit the mod, its libraries, the docs, the refreshed index and this change folder as `feat: add Adorn furniture`

## 2. Bibliocraft Legacy

- [ ] 2.1 Run `packwiz cf add` for Bibliocraft Legacy (`bibliocraft-26.1.2-1.7.1.jar`) and any new library; check source and side as in 1.1
- [ ] 2.2 Add its rows to `docs/mods.md` (add Bibliocraft to the row of any library it shares with Adorn); run `packwiz refresh`; verify the checks from 1.2 pass
- [ ] 2.3 Restart the test server and verify as in 1.3; commit as `feat: add Bibliocraft Legacy furniture`

## 3. Fantasy's Furniture

- [ ] 3.1 Run `packwiz cf add` for Fantasy's Furniture (`fantasyfurniture-26.1.7.jar`) and any new library; check source and side as in 1.1
- [ ] 3.2 Add its rows to `docs/mods.md`; run `packwiz refresh`; verify the checks from 1.2 pass
- [ ] 3.3 Restart the test server and verify as in 1.3; commit as `feat: add Fantasy's Furniture`

## 4. Integration

- [ ] 4.1 Run `build.ps1 -Public`; verify the client manifest and the server zip both contain Adorn, Bibliocraft Legacy and Fantasy's Furniture, and `python -m tools.checks.commit_check` passes
- [ ] 4.2 Manual, with a client on the test server: find furniture from all three mods in JEI with recipes; place an Adorn chair and sit on it; put a book in a Bibliocraft bookcase, rejoin and see it still there; place a Fantasy's Furniture piece next to Macaw's furniture with no missing textures

## Workflow follow-up

- Archive this change in a `chore(openspec)` commit after the manual test.
