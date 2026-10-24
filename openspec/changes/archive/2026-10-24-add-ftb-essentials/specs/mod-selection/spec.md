# Spec Delta

## ADDED Requirements

### Requirement: Player teleport commands
The pack SHALL include FTB Essentials from CurseForge. Every player SHALL have one home, `/warp` to warps set by ops, `/back` to the previous location and the last death point, and `/tpa`. Only ops SHALL create or remove warps. `/rtp` SHALL be switched off.

#### Scenario: One home
- **WHEN** a player who already has a home runs `/sethome` with a new name
- **THEN** the command is refused and the first home stays

#### Scenario: Warp set by a player
- **WHEN** a player without op runs `/setwarp`
- **THEN** the command is unknown or refused, and no warp is created

#### Scenario: Warp set by an op
- **WHEN** an op runs `/setwarp town` and a player then runs `/warp town`
- **THEN** the player is teleported to the town warp

#### Scenario: Back to the grave
- **WHEN** a player dies and then runs `/back`
- **THEN** the player is teleported to the death point

#### Scenario: Random teleport
- **WHEN** a player runs `/rtp`
- **THEN** the command is unknown or refused, and the player does not move

### Requirement: Free shared waystones
Teleporting with Waystones SHALL cost no XP and SHALL NOT wear down warp stones. A waystone that is newly placed or found SHALL be global, so every player can travel to it without visiting it first.

#### Scenario: Long trip
- **WHEN** a player teleports from one waystone to a distant one, or to another dimension
- **THEN** the player keeps all their XP

#### Scenario: Warp stone use
- **WHEN** a player teleports with a warp stone
- **THEN** the warp stone's durability does not change

#### Scenario: Waystone placed by another player
- **WHEN** one player places a waystone and another player, who never visited it, opens any waystone
- **THEN** the new waystone is listed and the second player can teleport to it
