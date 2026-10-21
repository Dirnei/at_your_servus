# Design

## Context

See `proposal.md` for the why and `specs/release-changelog/spec.md` for the requirements.

Current state:
- `tools/publish.py`
  - `--check` validates the tag and prints the version. `publish.yml` runs it before the build.
  - The upload sends the fixed changelog `"At Your Servus {version}"` for the client file and `"Server pack for At Your Servus {version}"` for the server file, both with `changelogType: markdown`.
- `build.yml` checks out the repo with the default `fetch-depth: 1`, so CI has no tags and no history.
- The commits since `v0.1.0-alpha` (`0faa63e`, which is also `origin/main`) are conventional commits, except:
  - `c988568` starts with a space.
  - `f01fb8e` is 80 characters long.
- No tag `v0.2.0-alpha` exists right now.
- The metafiles name the jar in `filename`, and its version is in that name (`servus_shuttles-0.2.0.jar`). The display name is in `name`.

## Goals / Non-Goals

**Goals:**
- One command produces a draft that only needs editing, not writing.
- A release can't reach CurseForge without its changelog section.

**Non-Goals:**
- No GitHub releases and no changelog for the server pack file. It keeps its short text, and players read the client file's changelog.
- No changelog sections for versions before 0.2.0-alpha.
- No rewriting of commit history by the tools. The two bad commits get reworded by hand.

## Decisions

### D1: `CHANGELOG.md` is the source, commits only feed the draft
`publish.py` reads the section from the file at the tagged commit, never from the commits. That way the text the players see is the edited one.
- Alternative: annotated tag messages, as in `servus_mc_mods`. Rejected because the text is written only at tagging time, isn't in the repo, and a fix means moving a pushed tag.
- Alternative: generate the changelog straight from the commits at publish time. Rejected because commit subjects are written for developers (`feat: Updated mods`), and nothing could be edited.

### D2: Previous tag through `git describe`
The draft's range is `git describe --tags --abbrev=0 --match "v*" --exclude "v<version>" HEAD`..HEAD. That's the nearest release tag reachable from HEAD, other than the version being drafted. The commit check uses the same command without `--exclude`. Without any tag, both use the whole history.
- Alternative: sort the tags by version. Rejected because `-alpha`/`-beta` ordering needs git config, and a tag that isn't reachable (from another branch) would count.

### D3: Commits: `git log --no-merges --format=%H%x00%B%x00`
The tool parses each message with one regex: `^(type)(\([a-z0-9-]+\))?(!)?: (\S.*)$` on the first line. The changelog tool keeps only `feat`, `fix` and `perf`, drops the scope and `!`, and capitalizes the first letter, oldest first within each group. The commit check also requires that the message has no further non-empty lines and that the subject is at most 74 characters. Merge commits are skipped, because a pull request's CI checks out a merge ref.

### D4: Mod changes from `git show <tag>:<path>`
The tool lists `mods/*.pw.toml` and `shaderpacks/*.pw.toml` at the previous tag with `git ls-tree` and in the working tree, and parses both with `tomllib`.
- A metafile only in the working tree is "Added".
- One only at the tag is "Removed".
- A metafile in both with a different `filename` is "Updated". A change to other fields (such as `side`) isn't listed.

Entries use `name` with the file name in backticks, sorted by name.
- Alternative: take mod updates from `chore(deps)` commits. Rejected because a commit names several mods in shortened form.

### D5: Section format and reading
The heading is `## <version>`, with `### New`, `### Fixes`, `### Performance` and `### Mods` inside, as `- ` bullets. A section's body runs from its heading up to the next line that starts with `## `, with blank lines trimmed. `publish.py` gets a `changelog_section(root, version)` that raises `PublishError` when the section is missing or empty. `--check` calls it too, so the tag job fails before building (`publish.yml` already runs `--check` first). The tool inserts a new draft below the file's `# Changelog` title and above the newest section.

### D6: Commit check in `build.yml`
`actions/checkout` gets `fetch-depth: 0` (full history and tags). A step `python -m tools.checks.commit_check` runs before the tests. The check prints one line per bad commit (short hash, reason, subject) and exits 1.

## Risks / Trade-offs

- [The two bad commits make the first CI run fail] → Reword `c988568` and `f01fb8e` before pushing. Auto mode blocks history rewrites by Claude, so the user runs it.
- [`feat: Updated mods` shows under "New" next to the mod list] → The draft is edited before committing. Commit type choice is covered by the commit format, not by the tool.
- [Untagged releases (tag deleted, re-tagged elsewhere) shift the range] → The range comes from the reachable tags, so moving a tag before pushing is harmless. Pushed tags aren't moved.
- [Full-history checkout makes CI slower] → The repo is small; the cost is negligible.

## Migration Plan

1. Implement the tools, then run `python -m tools.changelog 0.2.0-alpha` and edit the section together with the user.
2. Commit everything as one commit (`chore(tools): ...`, which stays out of the changelog).
3. The user rewords the two bad commits. `python -m tools.checks.commit_check` passes locally.
4. `git tag v0.2.0-alpha` on that commit. The push of `main` and the tag happens only when the user says so.

Rollback: revert the commit. `publish.py` goes back to the fixed text.
