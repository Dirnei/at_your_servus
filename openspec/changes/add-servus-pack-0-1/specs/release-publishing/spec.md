# Spec Delta

## Purpose

Builds the pack in CI on every push and publishes tagged versions to CurseForge, so releases don't depend on one developer machine.

## ADDED Requirements

### Requirement: CI build
Every push and pull request SHALL run the pack checks, the quest check and the build in GitHub Actions, and keep the client and server packs as build artifacts.

#### Scenario: Push with a broken quest
- **WHEN** a push contains a quest with an unknown item
- **THEN** the CI run fails at the quest check

### Requirement: Publish on tag
A tag `v<version>` matching the pack version SHALL run a public build and upload the client pack to the CurseForge project, then the server pack as its server pack file. Release type follows the version: `-alpha` and `-beta` suffixes map to alpha and beta, others to release.

#### Scenario: Tag push
- **WHEN** tag `v0.1.0` is pushed and the pack version is 0.1.0
- **THEN** CurseForge receives the client zip and the server zip linked to it

#### Scenario: Tag and version disagree
- **WHEN** the tag is `v0.2.0` but the pack version is 0.1.0
- **THEN** the publish job fails before uploading

### Requirement: Publishing needs configuration
Publishing SHALL only run when the CurseForge project ID and API token are configured in the repository; otherwise the tag build stops after building and says what is missing.

#### Scenario: No CurseForge project yet
- **WHEN** a tag is pushed and no project ID is configured
- **THEN** the job builds the packs, uploads nothing and reports the missing setting

### Requirement: No secrets in the repository
The CurseForge API token SHALL only be stored as a GitHub secret and MUST NOT appear in files or logs.

#### Scenario: Log output
- **WHEN** the publish job runs
- **THEN** the token is not printed in the log
