"""Drafts a version's CHANGELOG.md section from the commits and mod changes since the previous release tag
(openspec release-changelog). Edit the draft, commit it, then tag the release.
  python -m tools.changelog 0.2.0-alpha
New, Fixes and Performance come from feat, fix and perf commits; other types (chore, docs, ...) are left out.
Mods compares the mods/ and shaderpacks/ metafiles at the previous tag with the working tree."""
import argparse
import re
import sys
import tomllib
from pathlib import Path

from tools.checks.commit_check import commits, git, parse, previous_tag

GROUPS = {"feat": "New", "fix": "Fixes", "perf": "Performance"}
METAFILE_DIRS = ("mods", "shaderpacks")
TITLE = "# Changelog\n"


class ChangelogError(Exception):
    pass


def commit_groups(found: list[tuple[str, str]]) -> dict[str, list[str]]:
    groups = {title: [] for title in GROUPS.values()}
    for _, message in found:
        parsed = parse(message.split("\n")[0])
        if parsed and parsed[0] in GROUPS:
            subject = parsed[1]
            groups[GROUPS[parsed[0]]].append(subject[:1].upper() + subject[1:])
    return groups


def metafiles_at(root: Path, tag: str | None) -> dict[str, dict]:
    """path -> parsed metafile, at `tag` or (None) in the working tree."""
    if tag is None:
        paths = [p.relative_to(root).as_posix() for folder in METAFILE_DIRS for p in sorted((root / folder).glob("*.pw.toml"))]
        return {p: tomllib.loads((root / p).read_text(encoding="utf-8")) for p in paths}
    paths = [p for p in git(root, "ls-tree", "-r", "--name-only", tag, "--", *METAFILE_DIRS).splitlines()
             if p.endswith(".pw.toml")]
    return {p: tomllib.loads(git(root, "show", f"{tag}:{p}")) for p in paths}


def mod_changes(before: dict[str, dict], after: dict[str, dict]) -> list[str]:
    entries = []
    for path in after.keys() - before.keys():
        entries.append((after[path]["name"], f"Added: {after[path]['name']} (`{after[path]['filename']}`)"))
    for path in before.keys() - after.keys():
        entries.append((before[path]["name"], f"Removed: {before[path]['name']} (`{before[path]['filename']}`)"))
    for path in before.keys() & after.keys():
        old, new = before[path]["filename"], after[path]["filename"]
        if old != new:
            entries.append((after[path]["name"], f"Updated: {after[path]['name']} (`{old}` to `{new}`)"))
    return [text for _, text in sorted(entries, key=lambda e: e[0].lower())]


def draft(root: Path, version: str) -> str:
    since = previous_tag(root, exclude=f"v{version}")
    groups = commit_groups(commits(root, since))
    groups["Mods"] = mod_changes(metafiles_at(root, since) if since else {}, metafiles_at(root, None))
    lines = [f"## {version}", ""]
    for title, entries in groups.items():
        if entries:
            lines += [f"### {title}", "", *(f"- {e}" for e in entries), ""]
    return "\n".join(lines).rstrip("\n") + "\n"


def insert(changelog: str, version: str, section: str) -> str:
    if re.search(rf"^## {re.escape(version)}\s*$", changelog, re.M):
        raise ChangelogError(f"CHANGELOG.md already has a section for {version}")
    if not changelog.startswith(TITLE):
        changelog = TITLE + ("\n" + changelog if changelog else "")
    rest = changelog[len(TITLE):].lstrip("\n")
    return TITLE + "\n" + section + ("\n" + rest if rest else "")


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", help="the version as the tag names it, without v (0.2.0-alpha)")
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    path = args.root / "CHANGELOG.md"
    try:
        current = path.read_text(encoding="utf-8") if path.exists() else ""
        path.write_bytes(insert(current, args.version, draft(args.root, args.version)).encode("utf-8"))
    except ChangelogError as e:
        print(f"changelog: {e}", file=sys.stderr)
        return 1
    print(f"Drafted {args.version} in {path}; edit it, then commit and tag v{args.version}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
