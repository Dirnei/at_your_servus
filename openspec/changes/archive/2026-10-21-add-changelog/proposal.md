# Proposal

## Why

CurseForge shows a changelog for every pack file, but `tools/publish.py` uploads only the title ("At Your Servus 0.2.0-alpha"). Players can't see what a release changed, and nothing in the repo keeps that history. The commits since `v0.1.0-alpha` are now conventional commits, so most of a changelog can be drafted from them, and the mod changes can be read from the packwiz metafiles.

## What Changes

- New `CHANGELOG.md` in the repo root, with one `## <version>` section per release, newest first, in Markdown.
- New `python -m tools.changelog <version>`: drafts the section for `<version>` and inserts it at the top of `CHANGELOG.md`, for the user to edit before tagging.
  - It groups commits since the previous `v*` tag by type: `feat` under "New", `fix` under "Fixes", `perf` under "Performance". `chore`, `docs`, `ci`, `test`, `build`, `refactor`, `style` and `revert` are left out.
  - It compares the metafiles in `mods/` and `shaderpacks/` with the previous tag and lists them under "Mods": added, removed, and updated from the old to the new file.
  - It refuses to overwrite a section that already exists.
- `tools/publish.py` uploads the tagged version's section as the CurseForge changelog of the client pack. `--check` fails when the section is missing or empty, so the tag build stops before building.
- New `python -m tools.checks.commit_check`: every commit since the latest `v*` tag must be a single-line conventional commit (`type(scope)?!?: subject`, known type, no body) of at most 74 characters. `build.yml` runs it on every push, with full history and tags fetched.
- `docs/development.md` (Releases) and `CLAUDE.md` describe the commit format and the changelog step.

## Capabilities

### New Capabilities

- `release-changelog`: the changelog in the repo, how a version's section is drafted from commits and metafiles, its upload to CurseForge, and the commit format it depends on.

### Modified Capabilities

None. Upload on tag is `release-publishing`, which exists only in the unarchived change `add-servus-pack-0-1`. The new requirements live in `release-changelog`, so this change doesn't depend on that archive.

## Impact

- New: `CHANGELOG.md`, `tools/changelog.py`, `tools/checks/commit_check.py` and their tests.
- Changed: `tools/publish.py`, `tests/test_publish.py`, `.github/workflows/build.yml` (`fetch-depth: 0`, commit check step), `docs/development.md`, `CLAUDE.md`.
- Two commits since `v0.1.0-alpha` fail the new commit check: `c988568` has a leading space, and `f01fb8e` is 80 characters with the old text glued on. They must be reworded before `main` is pushed, or the first CI run fails.
- The release `v0.2.0-alpha` gets tagged on the commit that adds its changelog section.
