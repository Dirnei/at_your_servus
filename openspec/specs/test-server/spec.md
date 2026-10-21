# test-server Specification

## Purpose
Lets Dirnei and friends play the exact built server pack on Dirnei's own machine, and gives every build an automatic check that the pack starts cleanly.

## Requirements

### Requirement: Docker test server
The repository SHALL contain a Docker Compose setup that runs the latest built server pack on Minecraft 26.1.2, NeoForge 26.1.2.122 and Java 25, with the world kept outside the container.

#### Scenario: Start the test server
- **WHEN** the pack has been built and the compose setup is started
- **THEN** the server loads the mods from the latest `dist/` server pack and listens on port 25565

#### Scenario: Restart keeps the world
- **WHEN** the server container is restarted
- **THEN** the world is still there

### Requirement: Player settings outside git
Operators, whitelist and memory SHALL be set in an environment file that is not committed, with a committed example file.

#### Scenario: First setup
- **WHEN** the example environment file is copied and filled in
- **THEN** the server uses those operators, that whitelist and that memory

### Requirement: Smoke check
The repository SHALL provide a command that starts the server pack, waits until the server reports it is ready, checks the logs and stops the server again. It SHALL fail on a crash, on a startup timeout of 10 minutes, or on errors from FTB Quests or KubeJS.

#### Scenario: Clean start
- **WHEN** the smoke check runs on a good build
- **THEN** it exits successfully after the server reported it is ready

#### Scenario: Broken script
- **WHEN** a KubeJS script references an unknown item
- **THEN** the smoke check fails and prints the matching log lines

### Requirement: Client joins
A client installed from the client pack of the same build SHALL be able to join the test server.

#### Scenario: Join from the CurseForge app
- **WHEN** a player imports the client pack in the CurseForge app and connects to the test server
- **THEN** they join without a mod mismatch error
