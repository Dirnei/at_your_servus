"""Small zip helpers for the build: forward-slash entry names on every OS (Compress-Archive in Windows PowerShell 5.1 writes backslashes)."""
import argparse
import sys
import zipfile
from pathlib import Path


def zip_dir(src: Path, dest: Path, exclude: set[str]) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as z:
        for p in sorted(src.rglob("*")):
            rel = p.relative_to(src).as_posix()
            if p.is_file() and rel not in exclude:
                z.write(p, rel)


def add_file(zip_path: Path, file: Path, arcname: str) -> None:
    with zipfile.ZipFile(zip_path, "a", zipfile.ZIP_DEFLATED) as z:
        z.write(file, arcname)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("dir")
    d.add_argument("src", type=Path)
    d.add_argument("dest", type=Path)
    d.add_argument("--exclude", action="append", default=[])
    a = sub.add_parser("add")
    a.add_argument("zip", type=Path)
    a.add_argument("file", type=Path)
    a.add_argument("arcname")
    args = parser.parse_args(argv)
    if args.cmd == "dir":
        zip_dir(args.src, args.dest, set(args.exclude))
    else:
        add_file(args.zip, args.file, args.arcname)
    return 0


if __name__ == "__main__":
    sys.exit(main())
