"""Small zip helpers for the build: forward-slash entry names on every OS (Compress-Archive in Windows PowerShell 5.1 writes backslashes)."""
import argparse
import json
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


def set_profile_image(zip_path: Path, image: Path) -> None:
    """Puts the CurseForge profile image into a client zip: profileImage/<name> plus manifest.json's "image" key,
    as the CurseForge app exports it. packwiz does not write either."""
    arcname = f"profileImage/{image.name}"
    with zipfile.ZipFile(zip_path) as z:
        entries = [(i, z.read(i)) for i in z.infolist() if i.filename != arcname and not i.filename.startswith("profileImage/")]
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for info, data in entries:
            if info.filename == "manifest.json":
                manifest = json.loads(data)
                manifest["image"] = arcname
                data = json.dumps(manifest, indent=2).encode("utf-8")
            z.writestr(info, data, zipfile.ZIP_DEFLATED)
        z.write(image, arcname)


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
    i = sub.add_parser("image")
    i.add_argument("zip", type=Path)
    i.add_argument("image", type=Path)
    args = parser.parse_args(argv)
    if args.cmd == "dir":
        zip_dir(args.src, args.dest, set(args.exclude))
    elif args.cmd == "image":
        set_profile_image(args.zip, args.image)
    else:
        add_file(args.zip, args.file, args.arcname)
    return 0


if __name__ == "__main__":
    sys.exit(main())
