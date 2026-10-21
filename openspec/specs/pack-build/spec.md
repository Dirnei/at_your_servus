# pack-build Specification

## Purpose
Turns the repository into versioned, installable pack artifacts: a CurseForge client pack and a matching server pack, built the same way on a developer machine and in CI.

## Requirements

### Requirement: Single build command
The repository SHALL provide one build command that produces both the client pack and the server pack for the version in the pack metadata, in a `dist/` folder that is not committed.

#### Scenario: Build from a clean checkout
- **WHEN** the build command runs on a clean checkout with the required tools installed
- **THEN** `dist/` contains `at-your-servus-<version>.zip` and `at-your-servus-<version>-server.zip`

### Requirement: Client pack format
The client pack SHALL be a CurseForge modpack zip: `manifest.json` (manifestType `minecraftModpack`, manifestVersion 1, name `Servus`, author `Dirnei`, Minecraft 26.1.2, primary loader `neoforge-26.1.2.122`), `modlist.html` and an `overrides/` folder.

#### Scenario: Import into the CurseForge app
- **WHEN** the client pack is imported into the CurseForge app
- **THEN** the instance installs NeoForge 26.1.2.122, downloads all mods and applies configs, KubeJS scripts and quests from `overrides/`

### Requirement: Server pack contents
The server pack SHALL contain every mod marked server or both as a jar, plus configs, default configs, KubeJS scripts and quests, and start scripts that install NeoForge 26.1.2.122 on first run. It MUST NOT contain client-only mods.

#### Scenario: No client-only jars
- **WHEN** the server pack is built
- **THEN** no jar of a client-only mod (for example Sodium) is inside it, and the build fails if one is

### Requirement: Client and server match
The server pack SHALL contain exactly the same file version of each shared mod as the client pack.

#### Scenario: Version check
- **WHEN** both packs of one build are compared
- **THEN** every mod in the server pack has the same file version as its entry in the client manifest

### Requirement: Undownloadable mods are reported
When a mod file cannot be downloaded automatically for the server pack, for example because its author disabled third-party distribution, the build SHALL fail and name the mod and the file to download by hand.

#### Scenario: Distribution disabled
- **WHEN** a CurseForge mod blocks third-party downloads
- **THEN** the build stops with an error that names the mod and its download page

### Requirement: Public export guard
A public build SHALL fail when any mod is not sourced from CurseForge, because the CurseForge manifest cannot reference it.

#### Scenario: Alchemy still from GitHub
- **WHEN** a public build runs while Alchemy is still sourced from GitHub
- **THEN** the build fails and says Alchemy must be switched to CurseForge first

#### Scenario: Playtest build
- **WHEN** a playtest build runs while Alchemy is sourced from GitHub
- **THEN** the build succeeds, and the client pack carries Alchemy in `overrides/mods/` with a warning that this zip is not for public upload

### Requirement: Versioning
The pack version SHALL follow semantic versioning, start at 0.1.0 and be set in one place.

#### Scenario: Version bump
- **WHEN** the version in the pack metadata changes
- **THEN** both artifact names and the manifest version follow it
