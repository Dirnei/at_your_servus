# Spec Delta

## Purpose

Keeps a player-facing changelog in the repo, drafts each release's entry from conventional commits and mod changes, and shows it on CurseForge with the pack file.

## ADDED Requirements

### Requirement: Changelog in the repo
The repository SHALL have a `CHANGELOG.md` in its root with one section per released version, headed `## <version>` (the version as the tag names it, without `v`), newest first, written in Markdown.

#### Scenario: Section for a release
- **WHEN** `v0.2.0-alpha` is released
- **THEN** `CHANGELOG.md` contains a `## 0.2.0-alpha` section above the sections of older versions

### Requirement: Draft from commits
The changelog tool SHALL draft a version's section from the commits since the previous `v*` tag, grouped by conventional commit type: `feat` under "New", `fix` under "Fixes", `perf` under "Performance". Commits of other types, including `chore`, SHALL be left out. Each entry is the commit subject without its type prefix. Empty groups are omitted.

#### Scenario: Feature and chore commits
- **WHEN** the commits since the previous tag are `feat: add FTB Essentials with /rtp off` and `chore(tools): add client-sync.ps1`
- **THEN** the draft lists "Add FTB Essentials with /rtp off" under "New" and does not mention client-sync.ps1

#### Scenario: Version already tagged
- **WHEN** the draft for `0.2.0-alpha` is made while tag `v0.2.0-alpha` already exists
- **THEN** the commits are counted from the `v*` tag before it

### Requirement: Mod changes in the draft
The draft SHALL list, under "Mods", the metafiles in `mods/` and `shaderpacks/` that were added, removed or changed since the previous `v*` tag, with the mod name and its file name (before and after for an update).

#### Scenario: Updated mod
- **WHEN** `mods/servus-shuttles.pw.toml` changed from `servus_shuttles-0.1.0-beta.jar` to `servus_shuttles-0.2.0.jar`
- **THEN** "Mods" lists Servus: Shuttles as updated from `servus_shuttles-0.1.0-beta.jar` to `servus_shuttles-0.2.0.jar`

#### Scenario: Added shader pack
- **WHEN** `shaderpacks/complementary-reimagined.pw.toml` is new since the previous tag
- **THEN** "Mods" lists it as added

### Requirement: Draft never overwrites
The changelog tool SHALL insert the draft at the top of `CHANGELOG.md` and SHALL refuse, naming the version, when a section for that version already exists.

#### Scenario: Run twice
- **WHEN** the tool runs for `0.2.0-alpha` and `CHANGELOG.md` already has a `## 0.2.0-alpha` section
- **THEN** it fails, says the section exists, and leaves the file unchanged

### Requirement: Changelog on CurseForge
Publishing a release SHALL upload the body of the tagged version's `CHANGELOG.md` section as the Markdown changelog of the client pack file on CurseForge.

#### Scenario: Tag push
- **WHEN** `v0.2.0-alpha` is pushed and published
- **THEN** the CurseForge file "At Your Servus 0.2.0-alpha" shows the text of the `## 0.2.0-alpha` section

### Requirement: No release without a changelog
The tag check SHALL fail, before any build or upload, when `CHANGELOG.md` has no section for the tagged version or the section is empty.

#### Scenario: Tag without a section
- **WHEN** `v0.3.0-alpha` is pushed and `CHANGELOG.md` has no `## 0.3.0-alpha` section
- **THEN** the publish job fails at the tag check, names the missing section, and uploads nothing

### Requirement: Conventional commit format
Every commit since the latest `v*` tag SHALL have a single-line message of at most 74 characters of the form `type(scope)!: subject` (scope and `!` optional), where type is one of `feat`, `fix`, `perf`, `chore`, `docs`, `ci`, `test`, `build`, `refactor`, `style`, `revert`. The CI build SHALL fail and name each commit that breaks the format.

#### Scenario: Message too long
- **WHEN** a pushed commit's subject is 80 characters long
- **THEN** the CI build fails and names that commit and its length

#### Scenario: Leading space
- **WHEN** a commit message is ` chore(tools): add the quest explorer`
- **THEN** the check reports it as not a conventional commit

#### Scenario: Message with a body
- **WHEN** a commit message has a second paragraph
- **THEN** the check reports that the message must be one line

### Requirement: Checks gate the release
The tag build SHALL run the commit format check over the release's commits (from the previous `v*` tag up to the tagged commit), the tests and the quest book check before building, and SHALL upload nothing when any of them fails.

#### Scenario: Release with a long commit message
- **WHEN** `v0.3.0-alpha` is pushed and one of its commits since `v0.2.0-alpha` has an 80-character subject
- **THEN** the publish job fails at the commit check, names that commit, and nothing reaches CurseForge
