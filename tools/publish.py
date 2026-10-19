"""Uploads a built pack to CurseForge: the client zip, then the server zip as its server pack (openspec release-publishing).
  python -m tools.publish --tag v0.1.0
Reads CF_PROJECT_ID and CF_API_TOKEN from the environment. Without them it reports what is missing and uploads nothing."""
import argparse
import json
import os
import re
import sys
import tomllib
import urllib.request
import uuid
from pathlib import Path

API = "https://minecraft.curseforge.com/api"
MINECRAFT_VERSION = "26.1.2"


class PublishError(Exception):
    pass


def pack_version(root: Path) -> str:
    return tomllib.loads((root / "pack.toml").read_text(encoding="utf-8"))["version"]


def check_tag(tag: str, version: str) -> None:
    if tag != f"v{version}":
        raise PublishError(f"tag {tag} does not match pack version {version} (expected v{version})")


def release_type(version: str) -> str:
    if re.search(r"-alpha", version):
        return "alpha"
    if re.search(r"-beta", version):
        return "beta"
    return "release"


def _request(url: str, token: str, body: bytes | None = None, content_type: str | None = None) -> dict | list:
    request = urllib.request.Request(url, data=body, headers={"X-Api-Token": token})
    if content_type:
        request.add_header("Content-Type", content_type)
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def game_version_id(token: str) -> int:
    for v in _request(f"{API}/game/versions", token):
        if v.get("name") == MINECRAFT_VERSION:
            return v["id"]
    raise PublishError(f"CurseForge does not list Minecraft {MINECRAFT_VERSION}")


def upload(project_id: str, token: str, file: Path, metadata: dict) -> int:
    boundary = uuid.uuid4().hex
    parts = [
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"metadata\"\r\n\r\n{json.dumps(metadata)}\r\n".encode(),
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{file.name}\"\r\n"
        f"Content-Type: application/zip\r\n\r\n".encode() + file.read_bytes() + b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ]
    result = _request(f"{API}/projects/{project_id}/upload-file", token, b"".join(parts),
                      f"multipart/form-data; boundary={boundary}")
    return result["id"]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    try:
        version = pack_version(args.root)
        check_tag(args.tag, version)
        project_id, token = os.environ.get("CF_PROJECT_ID", ""), os.environ.get("CF_API_TOKEN", "")
        missing = [name for name, value in (("CF_PROJECT_ID", project_id), ("CF_API_TOKEN", token)) if not value]
        if missing:
            print(f"Not publishing: {', '.join(missing)} not configured. The packs are built; nothing was uploaded.")
            return 0
        dist = args.root / "dist"
        client, server = dist / f"Servus-{version}.zip", dist / f"Servus-{version}-server.zip"
        kind = release_type(version)
        client_id = upload(project_id, token, client, {
            "changelog": f"Servus {version}", "changelogType": "markdown", "displayName": f"Servus {version}",
            "gameVersions": [game_version_id(token)], "releaseType": kind})
        upload(project_id, token, server, {
            "changelog": f"Server pack for Servus {version}", "changelogType": "markdown",
            "displayName": f"Servus {version} Server", "parentFileID": client_id, "releaseType": kind})
        print(f"Published Servus {version} ({kind}) as CurseForge file {client_id}, with its server pack")
        return 0
    except PublishError as e:
        print(f"publish: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
