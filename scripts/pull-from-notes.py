import os
import re
import sys
from pathlib import Path
from datetime import datetime, timezone

import dateparser

SOURCE_DIR = Path.home() / "Notes" / "Blog"
DEST_DIR = Path.home() / "src" / "blog" / "posts"


def datetime_fmt(dt: datetime) -> str:
    if dt.hour or dt.minute or dt.second:
        return dt.strftime("%Y-%m-%d %H:%M")
    return dt.strftime("%Y-%m-%d")


def parse_timestamp(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    if not value:
        return None
    dt = dateparser.parse(value)
    if dt is None:
        print(f"  warning: could not parse date {value!r}, using file mtime", file=sys.stderr)
        return None
    return datetime_fmt(dt)


def file_mtime(path: Path) -> str:
    mtime = os.path.getmtime(path)
    dt = datetime.fromtimestamp(mtime, tz=timezone.utc)
    return datetime_fmt(dt)


def convert_filetags(value: str | None) -> str | None:
    if not value:
        return None
    value = value.strip()
    if not value:
        return None
    if value.startswith(":") and value.endswith(":"):
        value = value[1:-1]
    parts = [p.strip() for p in value.split(":") if p.strip()]
    if not parts:
        parts = [p.strip() for p in value.split(",") if p.strip()]
    if not parts:
        parts = [p.strip() for p in value.split() if p.strip()]
    return ", ".join(parts) if parts else None


def is_backup(name: str) -> bool:
    return name.endswith("~") or name.endswith("#")


def extract_meta(lines: list[str]) -> dict:
    meta: dict[str, str | None] = {
        "title": None,
        "status": None,
        "created": None,
        "date": None,
        "filetags": None,
        "hugo_tags": None,
    }
    for line in lines:
        stripped = line.strip()
        m = re.match(r"^#\+title:\s*(.*)", stripped, re.IGNORECASE)
        if m:
            meta["title"] = m.group(1).strip()
            continue
        m = re.match(r"^#\+status:\s*(.*)", stripped, re.IGNORECASE)
        if m:
            meta["status"] = m.group(1).strip()
            continue
        m = re.match(r"^#\+created:\s*(.*)", stripped, re.IGNORECASE)
        if m:
            meta["created"] = m.group(1).strip()
            continue
        m = re.match(r"^#\+date:\s*(.*)", stripped, re.IGNORECASE)
        if m:
            meta["date"] = m.group(1).strip()
            continue
        m = re.match(r"^#\+filetags:\s*(.*)", stripped, re.IGNORECASE)
        if m:
            meta["filetags"] = m.group(1).strip()
            continue
        m = re.match(r"^#\+hugo_tags:\s*(.*)", stripped, re.IGNORECASE)
        if m:
            meta["hugo_tags"] = m.group(1).strip()
            continue
    return meta


def process_file(src_path: Path) -> None:
    slug = src_path.stem
    lines = src_path.read_text(encoding="utf-8").splitlines(keepends=False)

    header_end = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#+") or stripped == "":
            header_end = i + 1
        else:
            break

    header_lines = lines[:header_end]
    body_lines = lines[header_end:]

    meta = extract_meta(header_lines)

    title = meta.get("title")
    if not title:
        print(f"  error: no #+title found, skipping", file=sys.stderr)
        return

    raw_date = meta.get("created") or meta.get("date")
    date_str = parse_timestamp(raw_date) if raw_date else None
    if not date_str:
        date_str = file_mtime(src_path)

    status = (meta.get("status") or "DRAFT").lower()

    tags = None
    if meta.get("filetags"):
        tags = convert_filetags(meta["filetags"])
    elif meta.get("hugo_tags"):
        tags = convert_filetags(meta["hugo_tags"])

    nikola = [
        "#+BEGIN_COMMENT",
        f".. title: {title}",
        f".. slug: {slug}",
        f".. date: {date_str}",
        f".. status: {status}",
    ]
    if tags:
        nikola.append(f".. tags: {tags}")
    nikola.append("#+END_COMMENT")

    body = "\n".join(body_lines)
    if body_lines and body_lines[0] != "":
        nikola.append("")

    nikola.append(body)

    dest_path = DEST_DIR / f"{slug}.org"
    dest_path.write_text("\n".join(nikola) + "\n", encoding="utf-8")
    print(f"  wrote {dest_path}")

    old_md = dest_path.with_suffix(".md")
    if old_md.exists():
        old_md.unlink()
        print(f"  removed stale {old_md.name}")


def main() -> None:
    if not SOURCE_DIR.is_dir():
        print(f"error: source directory {SOURCE_DIR} does not exist", file=sys.stderr)
        sys.exit(1)

    DEST_DIR.mkdir(parents=True, exist_ok=True)

    org_files = sorted(f for f in SOURCE_DIR.iterdir() if f.suffix == ".org" and not is_backup(f.name))

    if not org_files:
        print("no .org files found in source directory")
        return

    for src in org_files:
        print(f"{src.name}")
        first_line = src.read_text(encoding="utf-8").split("\n", 1)[0].strip()
        if first_line.startswith("#+BEGIN_COMMENT"):
            print("  already in Nikola format, skipping")
            continue
        process_file(src)


if __name__ == "__main__":
    main()
