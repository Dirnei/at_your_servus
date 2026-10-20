# Tasks

## 1. Sync script

- [x] 1.1 Write `tools/client-sync.ps1` (parameter `-Instance`, default `%USERPROFILE%\curseforge\minecraft\Instances\At Your Servus (dev)`): stop with setup instructions if the folder is missing; warn if `minecraftinstance.json`'s `gameVersion` or `baseModLoader.name` differ from `pack.toml`; run `packwiz refresh`; serve the pack on port 28418 and run `packwiz-installer-bootstrap.jar -g -s client` in the instance folder (download the bootstrap to `build/tools/` if missing); stop the server in `finally`; verify a sync into a test folder installs client mods such as `irisshaders` and the shader pack, a second run downloads nothing, and a missing folder gives the setup message
- [x] 1.2 Describe the dev profile in `docs/development.md` (create an empty custom profile "At Your Servus (dev)" with Minecraft 26.1.2 and NeoForge 26.1.2.122, run `.\tools\client-sync.ps1`, start the profile, join `localhost:25567`); verify the steps match the script

## 2. Integration

- [x] 2.1 Manual: create the dev profile in the CurseForge app, run the script, start the profile and join the local server; verify no mod mismatch
