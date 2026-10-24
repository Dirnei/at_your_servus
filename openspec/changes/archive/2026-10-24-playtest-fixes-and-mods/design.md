# Design

## Context

See `proposal.md` for the why, and `specs/quest-line/spec.md` and `specs/mod-selection/spec.md` for the requirements.

Current state (checked 2026-10-21):
- `tools/questgen/generate.py` writes titles, subtitles and description lines into the lang JSON5 files unchanged. Five texts contain `&`, all as "Huber & Co." (`02-old-works.toml` warehouse-letter, `03-cellar.toml` salt quest, `06-trading-house.toml` chapter subtitle, trading-letter title, open-for-business subtitle). No quest text uses an FTB formatting code (`&a`, `&l`, ...).
- The Coal Generator (`servus_foundation:coal_generator`) is a two-block machine with its own chimney half. `servus_foundation:chimney` is a part of the Sink multiblock only.
- In Shuttles, the Storage Terminal opens the stock of the warehouses it reaches over the data line, and the Packing Station is the warehouse's door to the data line (items requested at the terminal leave through it, items stored from the terminal come back through it). Recipes: Data Cable is 3 copper ingots and 2 redstone for 4; Packing Station is iron, redstone, copper, a chest and planks. No KubeJS gate touches either.
- `trading-house:data-cable` (16 cables) and `trading-house:packing` exist. `crafting-station` depends on `data-cable`, `alchemy-order` depends on `packing`.
- CurseForge files for NeoForge 26.1.2 (resolved with `packwiz cf add` in a scratch copy): `solcarrot-26.1-1.19.0.jar`; `torchmaster-neoforge-26.1.2-26.1.2-1.0.0.jar` (Torchmaster Version Locked, an unofficial port; the jar contains the Feral Flare Lantern, Megatorch and Dread Lamp); `entangled-1.3.21-neoforge-mc26.1.jar` (its SuperMartijn642 libraries are already in the pack for Rechiseled); `lighty-neoforge-4.0.1+26.1.2.jar`; `ComplementaryUnbound_r5.9.3.zip`; `EuphoriaPatcher-1.10.5-r5.9.3-neoforge.jar`. The pack has `ComplementaryReimagined_r5.9.3.zip`. packwiz writes `side = "both"` for all of them.
- Euphoria Patcher's jar detects both the Reimagined and the Unbound style of Complementary.
- `pack_check.py` has `CLIENT_ONLY_SLUGS` and already loads `shaderpacks/`.

## Goals / Non-Goals

**Goals:**
- The Works chapter ends with a warehouse that works the way its quests describe.
- Quest texts can contain `&` without anyone having to remember an escape.
- The two shader packs and the patcher can't drift apart unnoticed.

**Non-Goals:**
- No tuned Spice of Life milestones, Torchmaster radii or Lighty settings: mod defaults until playtesting says otherwise.
- No quests for the new mods; the fields chapter (`add-fields-and-side-quests`) adds the Spice of Life quest.
- No new chapter layout beyond the Works storage chain.

## Decisions

### D1: Escape every `&` in the generator
Every string the generator writes to a lang file gets each `&` replaced with `\&`. The JSON writer turns that into `\\&` in the file, which FTB Quests reads as an escaped, literal `&`. Quest sources keep "Huber & Co." as plain text.
- Alternative: escape only `&` followed by whitespace, as the error message asks. Rejected: `&` followed by a letter would then turn into a formatting code silently, for example "Salt&Co" showing a colour change. The pack uses no formatting codes, so escaping all of them costs nothing.
- Alternative: write `\&` in the TOML sources. Rejected: easy to forget, and the TOML texts are what people read and review.

### D2: Two moved quests, not new ones
The Trading House's `data-cable` and `packing` quests move to `02-old-works.toml` as `data-cable` and `packing-station`, between `controller` and `terminal`: `controller -> data-cable -> packing-station -> terminal`. Their texts are rewritten for the Works: the cable connects terminal, controller and Packing Station; the Packing Station is the warehouse's door to the data line. In The Trading House, `crafting-station` then depends on `outbound` (the data cable is already done, since the chapter opens after `old-works:terminal`), and `alchemy-order` drops `packing`. The terminal and all later quests keep their slugs, so only the two moved quests lose progress.
- Alternative: keep the Trading House quests and add copies to the Works. Rejected: two quests that ask for the same thing.

### D3: Chimney task dropped, slug kept
`old-works:coal-generator` keeps its slug and asks only for the Coal Generator. Its text loses "Give it a chimney, ...".

### D4: Version lock as a pack check rule
The pack check reads the Complementary version from `r<version>` in the file names of `euphoria-patches` and of every `complementary-*` shader pack, and fails, naming the files, when they differ or a file name has no version. That catches a `packwiz update` of only one of them.
- Alternative: rely on the patcher's own warning at game start. Rejected: it shows up only on a client, after a release.

### D5: Torchmaster Version Locked as is
The original TorchMaster has no 26.1 build, so the port is the only source of the Feral Flare Lantern. The Megatorch blocks natural hostile spawns in a large radius; spawner-based farms (Apothic Spawners) and Hostile Neural Networks don't depend on natural spawns, so no gate is planned. If playtesting shows it breaks a side quest's mob farm, a config change follows, with an entry in `docs/gates.md`.

### D6: Client-only additions
`lighty` and `euphoria-patches` join `CLIENT_ONLY_SLUGS` and their metafiles get `side = "client"`. Spice of Life, Torchmaster and Entangled stay `both`. `complementary-unbound` gets `side = "client"` like every shader pack.

## Risks / Trade-offs

- [FTB Quests might show `\&` literally instead of `&`] → Check in the quest book on the test server before the generator change is done; if it does, switch to the escape FTB documents and update the test.
- [Unofficial Torchmaster port may stop being updated] → It's a convenience block; if it dies, the lanterns go and the mod is listed as waiting in `docs/mods.md`.
- [Euphoria Patcher may switch an active shader selection to its patched pack] → It doesn't change "off by default". Verify once in-game; note it in `docs/mods.md` if it does.
- [Spice of Life changes health balance for the boss fights] → Defaults are moderate; tune after the fields chapter brings the food quests.
- [Lighty's F7 may collide with another key] → Check the controls menu for F7 conflicts in the manual test.

## Migration Plan

Players on 0.x lose the progress of `trading-house:data-cable` and `trading-house:packing`; both are quick to redo and the pack is alpha. The changelog says so.
