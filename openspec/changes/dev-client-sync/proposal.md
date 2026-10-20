# Proposal

## Why

Testing a change on a client means building the pack, importing the zip in the CurseForge app and waiting for it to install. That is slow for checks like the shader and FTB Essentials tests in `add-shaders` and `add-ftb-essentials`, which only need the current working tree on a client that joins the local server.

## What Changes

- New `tools/client-sync.ps1`: serves the working tree with `packwiz serve` and installs its client side with packwiz-installer into a dev CurseForge profile, by default `At Your Servus (dev)`. Only changed files are downloaded, and files the pack dropped are removed.
- The script stops if the profile folder is missing, and warns if the profile's Minecraft or NeoForge version differs from `pack.toml`.
- It never touches other profiles.
- `docs/development.md` describes the one-time profile setup and the test loop.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

None. This is developer tooling; the pack and its build don't change (`skip_specs: true`).

## Impact

- `tools/client-sync.ps1` (new), `docs/development.md`.
- Uses the `packwiz-installer-bootstrap.jar` that `tools/build.ps1` already downloads to `build/tools/`.
