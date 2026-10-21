"""Checks that every commit since the latest release tag is a one-line conventional commit (openspec release-changelog).
  python -m tools.checks.commit_check
The changelog is drafted from these commits (python -m tools.changelog), so their format matters."""
import argparse
import re
import subprocess
import sys
from pathlib import Path

TYPES = ("feat", "fix", "perf", "chore", "docs", "ci", "test", "build", "refactor", "style", "revert")
MAX_LENGTH = 74
SUBJECT = re.compile(rf"^({'|'.join(TYPES)})(\([a-z0-9-]+\))?(!)?: (\S.*)$")


def git(root: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=root, check=True, capture_output=True, text=True,
                          encoding="utf-8").stdout


def previous_tag(root: Path, exclude: str | None = None) -> str | None:
    """The nearest v* tag reachable from HEAD (other than `exclude`), or None without one."""
    args = ["describe", "--tags", "--abbrev=0", "--match", "v*"] + (["--exclude", exclude] if exclude else []) + ["HEAD"]
    try:
        return git(root, *args).strip()
    except subprocess.CalledProcessError:
        return None


def commits(root: Path, since: str | None) -> list[tuple[str, str]]:
    """(hash, message) of the non-merge commits after `since`, oldest first."""
    out = git(root, "log", "--no-merges", "--reverse", "--format=%H%x00%B%x00", *([f"{since}..HEAD"] if since else []))
    parts = out.split("\x00")
    return [(parts[i].strip(), parts[i + 1].strip("\n")) for i in range(0, len(parts) - 1, 2)]


def parse(subject: str) -> tuple[str, str] | None:
    """(type, subject without prefix) of a conventional commit subject, or None."""
    m = SUBJECT.match(subject)
    return (m[1], m[4]) if m else None


def problem(message: str) -> str | None:
    lines = message.split("\n")
    subject = lines[0]
    if any(line.strip() for line in lines[1:]):
        return "message must be one line"
    if parse(subject) is None:
        return "not a conventional commit (type(scope): subject)"
    if len(subject) > MAX_LENGTH:
        return f"{len(subject)} characters, at most {MAX_LENGTH}"
    return None


def check(found: list[tuple[str, str]]) -> list[str]:
    return [f"{sha[:7]}: {reason}: {message.split(chr(10))[0]}"
            for sha, message in found if (reason := problem(message))]


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args(argv)
    errors = check(commits(args.root, previous_tag(args.root)))
    for e in errors:
        print(e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
