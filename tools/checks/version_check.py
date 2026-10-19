"""Checks that a built client manifest and server mods folder carry the same mod files (openspec pack-build)."""
import argparse
import json
import sys
import zipfile
from pathlib import Path

from tools.checks.pack_check import load_metafiles, project_id


def check(metas: dict[str, dict], manifest: dict, server_jars: set[str]) -> list[str]:
    errors = []
    manifest_files = {f["projectID"]: f["fileID"] for f in manifest["files"]}
    expected_jars = set()
    for slug, meta in metas.items():
        side = meta.get("side", "both")
        pid = project_id(meta)
        if pid is not None:
            file_id = meta["update"]["curseforge"]["file-id"]
            if manifest_files.get(pid) != file_id:
                errors.append(f"{slug}: manifest has file {manifest_files.get(pid)}, metafile has {file_id}")
        if side == "client":
            if meta["filename"] in server_jars:
                errors.append(f"{slug}: client-only jar {meta['filename']} is in the server pack")
        else:
            expected_jars.add(meta["filename"])
            if meta["filename"] not in server_jars:
                errors.append(f"{slug}: {meta['filename']} is missing from the server pack")
    known = {m["filename"] for m in metas.values()}
    for jar in sorted(server_jars - known):
        errors.append(f"server pack has a jar no metafile describes: {jar}")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--client-zip", type=Path, required=True)
    parser.add_argument("--server-mods", type=Path, required=True)
    args = parser.parse_args(argv)
    with zipfile.ZipFile(args.client_zip) as z:
        manifest = json.load(z.open("manifest.json"))
    jars = {p.name for p in args.server_mods.glob("*.jar")}
    errors = check(load_metafiles(args.root / "mods"), manifest, jars)
    for e in errors:
        print(f"version check: {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
