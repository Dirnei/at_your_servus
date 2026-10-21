# Tasks

## 1. Commit check

- [x] 1.1 Add `tools/checks/commit_check.py` (D2, D3, D6). Every non-merge commit since the latest reachable `v*` tag must be a single-line conventional commit with a known type, at most 74 characters. The check prints short hash, reason and subject per bad commit and exits 1. Add `tests/test_commit_check.py`: a valid commit, a known-type list, a leading space, 75 characters, a body, an unknown type. Its git tests run on a throwaway repo in `tmp_path`. Verify `python -m pytest tests/test_commit_check.py` passes.
- [x] 1.2 In `.github/workflows/build.yml`, set `fetch-depth: 0` on `actions/checkout` and add a "Commit format" step running `python -m tools.checks.commit_check` before the tests. Add `python -m tools.checks.commit_check` to the checks in `CLAUDE.md`, plus a line on the commit format (conventional, one line, at most 74 characters; only `feat`, `fix` and `perf` reach the changelog). Verify the workflow YAML parses (`python -c "import yaml..."` or a review) and the command runs locally. It is expected to name `c988568` and `f01fb8e` until they are reworded.

## 2. Changelog draft

- [x] 2.1 Add `tools/changelog.py`, run as `python -m tools.changelog <version>` (D2-D5):
  - the previous tag via `git describe --exclude`
  - New/Fixes/Performance from `feat`/`fix`/`perf`, every other type left out
  - Mods from comparing the `mods/` and `shaderpacks/` metafiles at the tag with the working tree: added, removed, updated by `filename`
  - inserts the section below `# Changelog`, and creates `CHANGELOG.md` with that title if it is missing
  - refuses an existing section

  Add `tests/test_changelog.py` on a throwaway git repo:
  - feat and chore commits (chore left out)
  - an added shader pack and an updated mod
  - the drafted version already tagged
  - running twice (refused, file unchanged)
  - empty groups omitted

  Verify `python -m pytest tests/test_changelog.py` passes.

## 3. Publish with the changelog

- [x] 3.1 In `tools/publish.py`, add `changelog_section(root, version)` (D5). `--check` calls it and fails naming the missing or empty section. The client upload sends the section body as `changelog`, while the server upload keeps its text. Update the module docstring. In `tests/test_publish.py`:
  - the section is read up to the next `## `
  - `--check` fails without a section, and with an empty one
  - the client upload gets the section text (via a fake `upload`)
  - the existing tests get a `CHANGELOG.md` in `tmp_path`

  Verify `python -m pytest` passes.
- [x] 3.2 In `docs/development.md` under Releases: the commit format, `python -m tools.changelog <version>`, editing the section, committing it, then tagging. A release tag without a section fails. Verify the documented commands run as written.

## 4. Changelog for 0.2.0-alpha

- [x] 4.1 Run `python -m tools.changelog 0.2.0-alpha`. Check that "Mods" lists:
  - Iris, FTB Essentials and Inventory Sorter as added
  - Complementary Reimagined as an added shader pack
  - Servus Foundation, Servus Shuttles, JEI, FTB XMod Compat, Sophisticated Core and Sophisticated Storage as updated

  Show the draft to the user; they chose to ship it unedited. Verify the user accepts the text and `python -m tools.publish --tag v0.2.0-alpha --check` prints `0.2.0-alpha`.
- [x] 4.2 Manual (user): reword the commits since `v0.1.0-alpha` as conventional commits, content unchanged. The user keeps the 104-character Iris commit on purpose; it is out of the check's range once `v0.2.0-alpha` is tagged. Verify `python -m tools.checks.commit_check` passes after tagging.
- [x] 4.3 Run `python -m pytest`, `python -m tools.checks.pack_check --public` and `.\tools\build.ps1 -Public -Version 0.2.0-alpha`, and verify they pass.

## Workflow follow-up

- Commit the change as one `chore(tools): ...` commit, then `git tag v0.2.0-alpha` on it. Push `main` and the tag only when the user says so; the tag publishes to CurseForge.
- After publishing, check the CurseForge file page shows the changelog, then archive this change.
