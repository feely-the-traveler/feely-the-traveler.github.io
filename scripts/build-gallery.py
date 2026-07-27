#!/usr/bin/env python3
"""
Scan chapter/ch*/ folders and regenerate assets/js/gallery-data.js

Convention
----------
chapter/
  ch1/, ch2/, ...        chapter folders (digits after "ch")
    name.txt             chapter display name
    front.png / .jpg     prologue image (optional)
    front.txt            prologue story note (optional)
    ep01.png / .jpg ...  episode image (any common image extension)
    ep01.txt             episode story note (optional)
    back.png / .jpg      epilogue image (optional)
    back.txt             epilogue story note (optional)

Display order inside a chapter: Prologue → episodes → Epilogue.

companion/
  companion.png / .jpg     companion Feely portrait (optional)
  companion_img.png / .jpg how the artist carries Feely (optional)
  companion.txt            companion story note (optional)

Run from repo root:
  python scripts/build-gallery.py
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "js" / "gallery-data.js"

# ---------------------------------------------------------------------------
# CDN base URL (optional).
#
# Leave empty ("") → relative paths like chapter/ch1/ep01.jpg (served by GitHub Pages).
# When you move images to a CDN, set the base URL here and re-run this script.
#   e.g. CDN_BASE_URL = "https://cdn.feelythetraveler.com"
#        → https://cdn.feelythetraveler.com/chapter/ch1/ep01.jpg
# Keep the same folder layout (chapter/chN/epXX.jpg) on the CDN.
# ---------------------------------------------------------------------------
CDN_BASE_URL = ""

IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".PNG", ".JPG", ".JPEG", ".WEBP", ".GIF"}
EP_RE = re.compile(r"^ep(\d+)$", re.IGNORECASE)
CH_RE = re.compile(r"^ch(\d+)$", re.IGNORECASE)

# Special stems → gallery tag shown in the UI
SPECIAL_TAGS = {
    "front": "Prologue",
    "back": "Epilogue",
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    raw = path.read_bytes()
    for enc in ("utf-8-sig", "utf-8", "cp949", "euc-kr"):
        try:
            return raw.decode(enc).strip()
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace").strip()


def js_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def find_image(folder: Path, stem: str) -> Path | None:
    """Find image by stem; prefer exact stem match, any image extension."""
    matches = []
    for path in folder.iterdir():
        if not path.is_file():
            continue
        if path.stem.lower() != stem.lower():
            continue
        if path.suffix in IMAGE_EXTS or path.suffix.lower() in {e.lower() for e in IMAGE_EXTS}:
            matches.append(path)
    if not matches:
        return None
    # Prefer png, then jpg/jpeg, then others; keep original casing of chosen file
    priority = {".png": 0, ".jpg": 1, ".jpeg": 2, ".webp": 3, ".gif": 4}
    matches.sort(key=lambda p: (priority.get(p.suffix.lower(), 9), p.name.lower()))
    return matches[0]


def find_note(folder: Path, stem: str) -> str:
    for name in (f"{stem}.txt", f"{stem.upper()}.txt", f"{stem.lower()}.txt"):
        path = folder / name
        if path.exists():
            return read_text(path)
    # Case-insensitive fallback
    for path in folder.iterdir():
        if path.is_file() and path.suffix.lower() == ".txt" and path.stem.lower() == stem.lower():
            return read_text(path)
    return ""


def make_work(folder: Path, img: Path, note: str, tag: str = "") -> dict:
    rel = (folder.relative_to(ROOT) / img.name).as_posix()
    if CDN_BASE_URL:
        rel = CDN_BASE_URL.rstrip("/") + "/" + rel
    return {
        "file": rel,
        "tag": tag,
        "emotion": "",
        "primary": "",
        "support": ["", ""],
        "note": note,
    }


def scan_special(folder: Path, stem: str) -> dict | None:
    img = find_image(folder, stem)
    if not img:
        return None
    return make_work(folder, img, find_note(folder, stem), SPECIAL_TAGS[stem])


def scan_chapter(folder: Path) -> dict | None:
    m = CH_RE.match(folder.name)
    if not m:
        return None

    num = int(m.group(1))
    name = read_text(folder / "name.txt")
    label = f"Chapter {num}"

    # Collect episode numbers that have an image
    episodes: dict[int, dict] = {}
    for path in folder.iterdir():
        if not path.is_file():
            continue
        ep = EP_RE.match(path.stem)
        if not ep:
            continue
        n = int(ep.group(1))
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif"}:
            episodes.setdefault(n, {})["image"] = path
        elif path.suffix.lower() == ".txt":
            episodes.setdefault(n, {})["note"] = read_text(path)

    works = []

    # Prologue first (front.*)
    prologue = scan_special(folder, "front")
    if prologue:
        works.append(prologue)

    for n in sorted(episodes):
        img = episodes[n].get("image")
        if not img:
            # note-only: skip (needs a visual)
            # try find_image in case casing weirdness
            img = find_image(folder, f"ep{n:02d}") or find_image(folder, f"ep{n}")
        if not img:
            continue
        note = episodes[n].get("note", "")
        if not note:
            note = find_note(folder, f"ep{n:02d}") or find_note(folder, f"ep{n}")

        works.append(make_work(folder, img, note))

    # Epilogue last (back.*)
    epilogue = scan_special(folder, "back")
    if epilogue:
        works.append(epilogue)

    if not works:
        return None

    return {
        "id": folder.name.lower(),
        "label": label,
        "title": name,
        "num": num,
        "works": works,
    }


def scan_companion() -> dict | None:
    folder = ROOT / "companion"
    if not folder.is_dir():
        return None

    portrait = find_image(folder, "companion")
    life = find_image(folder, "companion_img")
    if not portrait and not life:
        return None

    def to_rel(path: Path | None) -> str:
        if not path:
            return ""
        rel = (folder.relative_to(ROOT) / path.name).as_posix()
        if CDN_BASE_URL:
            return CDN_BASE_URL.rstrip("/") + "/" + rel
        return rel

    return {
        "file": to_rel(portrait),
        "img": to_rel(life),
        "note": find_note(folder, "companion"),
    }


def render(chapters: list[dict], companion: dict | None) -> str:
    lines = [
        "/*",
        " * FEELY the Traveler — Gallery data",
        " * ---------------------------------",
        " * AUTO-GENERATED by scripts/build-gallery.py — do not edit by hand.",
        " *",
        " * Add a chapter folder (chapter/ch3/, chapter/ch4/, ...) with:",
        " *   name.txt      chapter name",
        " *   front.png     prologue (optional)",
        " *   front.txt     prologue note (optional)",
        " *   ep01.png      episode image (.png / .jpg / .jpeg / .webp)",
        " *   ep01.txt      episode story note (optional)",
        " *   back.png      epilogue (optional)",
        " *   back.txt      epilogue note (optional)",
        " *",
        " * Optional companion/ folder (artist section, 4 columns):",
        " *   companion.png / .jpg       Companion Feely portrait",
        " *   companion_img.png / .jpg   how the artist carries Feely",
        " *   companion.txt              story note (optional)",
        " *",
        " * Then run:  python scripts/build-gallery.py",
        " */",
        "",
        "const GALLERY = [",
    ]

    for i, ch in enumerate(chapters):
        lines.append("  {")
        lines.append(f"    id: {js_string(ch['id'])},")
        lines.append(f"    label: {js_string(ch['label'])},")
        lines.append(f"    title: {js_string(ch['title'])},")
        lines.append("    works: [")
        for j, work in enumerate(ch["works"]):
            comma = "," if j < len(ch["works"]) - 1 else ""
            support = json.dumps(work["support"], ensure_ascii=False)
            lines.append(
                "      { "
                f"file: {js_string(work['file'])}, "
                f"tag: {js_string(work.get('tag', ''))}, "
                f"emotion: {js_string(work['emotion'])}, "
                f"primary: {js_string(work['primary'])}, "
                f"support: {support}, "
                f"note: {js_string(work['note'])} "
                f"}}{comma}"
            )
        lines.append("    ]")
        lines.append("  }" + ("," if i < len(chapters) - 1 else ""))

    lines.append("];")
    lines.append("")

    if companion:
        lines.append("const COMPANION = {")
        lines.append(f"  file: {js_string(companion['file'])},")
        lines.append(f"  img: {js_string(companion.get('img', ''))},")
        lines.append(f"  note: {js_string(companion['note'])}")
        lines.append("};")
    else:
        lines.append("const COMPANION = null;")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    chapters = []
    base = ROOT / "chapter"
    if not base.is_dir():
        print(f"Missing folder: {base.relative_to(ROOT)}/")
        print("Expected: chapter/ch1/, chapter/ch2/, ...")
    else:
        for path in sorted(base.iterdir()):
            if path.is_dir() and CH_RE.match(path.name):
                chapter = scan_chapter(path)
                if chapter:
                    chapters.append(chapter)

    chapters.sort(key=lambda c: c["num"])
    companion = scan_companion()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(chapters, companion), encoding="utf-8")

    total = sum(len(c["works"]) for c in chapters)
    print(f"Wrote {OUT.relative_to(ROOT)} - {len(chapters)} chapters, {total} works")
    for c in chapters:
        label = c["label"].encode("ascii", "backslashreplace").decode("ascii")
        print(f"  {c['id']}: {label} ({len(c['works'])})")
    if companion:
        bits = []
        if companion.get("file"):
            bits.append(f"portrait={companion['file']}")
        if companion.get("img"):
            bits.append(f"life={companion['img']}")
        print(f"  companion: {', '.join(bits) or '(empty)'}")
    else:
        print("  companion: (none)")


if __name__ == "__main__":
    main()
