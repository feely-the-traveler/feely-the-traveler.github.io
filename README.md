# FEELY the Traveler

> Every feeling deserves a place.
> A curious traveler collecting stories and feelings, one encounter at a time.

Official website source for the brand. Deployed with GitHub Pages.

- Repository: `feely-the-traveler.github.io`
- Public URL: https://feely-the-traveler.github.io
- Instagram: https://www.instagram.com/feely_the_traveler/
- Shop: https://thedropmuse.com/artist/feely_the_traveler

---

## Folder structure

```
.
├── index.html
├── .nojekyll
├── scripts/
│   └── build-gallery.py    Scan content folders → generate *-data.js
├── assets/
│   ├── css/style.css
│   ├── img/
│   └── js/
│       ├── gallery-data.js   Auto-generated (do not edit by hand)
│       ├── news-data.js      Auto-generated (do not edit by hand)
│       └── main.js
├── chapter/
│   ├── ch1/
│   │   ├── name.txt        Chapter name
│   │   ├── front.PNG       Prologue image (optional)
│   │   ├── front.txt       Prologue story note (optional)
│   │   ├── ep01.PNG        Episode image
│   │   ├── ep01_2.PNG      Side/angle image of ep01 (optional)
│   │   ├── ep01.txt        Episode story note
│   │   ├── back.PNG        Epilogue image (optional)
│   │   ├── back.txt        Epilogue story note (optional)
│   │   └── ...
│   ├── ch2/
│   └── ch3/                (hidden on the site until images are added)
├── companion/
│   ├── companion.jpg       Companion Feely portrait (artist col 3)
│   ├── companion_img.jpg   Artist carrying Feely (artist col 4)
│   └── companion.txt       Companion story note (optional)
├── special/
│   └── ch2-special01/
│       ├── front.jpg       Cover image
│       ├── right.jpg       Optional additional view
│       ├── left.jpg        Optional additional view
│       ├── side.jpg        Optional additional view
│       └── content.txt     Title, chapter, optional story
└── news/
    └── 2026-09-26-on-a-whim.txt   One file per news item
```

---

## Adding a new chapter / artwork (no HTML edits)

### 1. Add folders and files only

```
chapter/ch3/
  name.txt          ← chapter name (one line)
  front.jpg         ← prologue image (optional)
  front.txt         ← prologue story note (optional)
  ep01.jpg          ← episode image (.png / .jpg / .jpeg / .webp)
  ep01_2.jpg        ← optional side/angle image of ep01 (ep01_3, ep01_4, ... also work)
  ep01.txt          ← episode story note (optional)
  ep02.png
  ep02.txt
  back.jpg          ← epilogue image (optional)
  back.txt          ← epilogue story note (optional)
```

Display order inside a chapter: **Prologue → episodes → Epilogue**.

Prefer **1K JPEG** (long edge ~1000–1200px) — about 200–500KB per file, so storage stays manageable.

### 2. Build locally, then push

```powershell
python scripts/build-gallery.py
```

This updates `gallery-data.js`. Commit and push that file together with your images.
(If you push without building, the gallery will not update.)

For auto-rebuild while developing:

```powershell
python scripts/watch-gallery.py
```

Changes under `chapter/`, `special/`, and `companion/` will regenerate
`gallery-data.js` automatically.

### Rules

| File | Role |
|---|---|
| `chapter/chN/` | Chapter folder (`ch1`, `ch2`, `ch10`, …) |
| `name.txt` | Chapter name shown in tabs |
| `front.png`, etc. | Prologue image → shown as **Prologue** (optional; first in the chapter) |
| `front.txt` | Prologue story note |
| `epXX.png`, etc. | Episode image (any case/extension; stem must be `ep01` style) |
| `epXX_2.png`, `epXX_3.png`, ... | Optional side/angle images of the same episode → shown as clickable thumbnails under the main photo in the lightbox |
| `epXX.txt` | Episode story note → shown in the card / lightbox |
| `back.png`, etc. | Epilogue image → shown as **Epilogue** (optional; last in the chapter) |
| `back.txt` | Epilogue story note |

Only works with an image are included. Notes without an image are skipped.

### Companion Feely (artist section)

```
companion/
  companion.jpg         ← portrait (.png / .jpg / .jpeg / .webp)
  companion_img.jpg     ← how the artist carries Feely (optional)
  companion.txt         ← optional story note
```

When those files exist, the artist section becomes **4 columns**:

1. **Made by Jae.Y**
2. **Companion Feely** + not-for-sale copy
3. `companion.jpg` portrait
4. `companion_img.jpg` on-the-road photo

Also listed in The Journey's **Special** tab, with both photos and the same
story note. The gallery identifies it as **Chapter 1 · Special · Not for sale**. The artist
section stays unchanged; no image or story files need to be copied.

### Special works (The Journey → Special)

The Journey has **Chapter 1**, **Chapter 2**, …, and **Special** tabs.
Special works from every chapter share the Special tab, using the same
three-column desktop grid, two-column mobile grid, and click-to-enlarge
viewer as regular works. **View all** includes Special too.

Add one folder per work; keep its folder name unique across chapters:

```
special/ch2-special01/
  front.jpg       Cover image (required)
  right.jpg       Optional
  left.jpg        Optional
  side.jpg        Optional
  content.txt
```

`content.txt` uses this format:

```
title: Special 02
chapter: Chapter 2
---
Optional story text, preserving line breaks.
```

- `title` is the work's name, shown in the enlarged viewer; defaults to the
  folder name if omitted. Numbered photo badges are generated separately.
- `chapter` is an optional label, not a filter. A Chapter 3 special still
  appears in the same Special tab.
- Only folders with a `front` image are included. The same image formats
  as chapter works are supported; original filenames/casing are preserved.
- Images appear in **front → right → left → side** order. Additional views
  become clickable thumbnails in the enlarged viewer.
- Companion Feely from `companion/` appears first as **Special 01**.
  Other works follow in folder-name order as **Special 02**, **Special 03**,
  and so on. Folder names do not need to match these gallery-wide numbers.
  The Special tab is hidden when neither has any works.
- Run `python scripts/build-gallery.py` and include the updated
  `assets/js/gallery-data.js` with your images when committing.

---

## News

Shown right below the hero, before "Who is Feely?". Add one file per item:

```
news/2026-09-26-on-a-whim.txt
```

```
title: Feely selected for "On a Whim"
date: 2026-09-26
link: https://www.instagram.com/p/DcRxjAPkj3S/
---
Feely has been selected for the group exhibition "On a Whim" at
6M Community Arts in San Francisco, on view September 26 through
October 26.
```

- `title` / `date` / `link` go above the `---` line; `link` is optional.
- Everything after `---` is the body text.
- Sorted newest first by `date` (filename breaks ties). Only the latest 10
  items are shown on the site; the first 4 are visible by default, the rest
  appear after clicking "More news".
- Run `python scripts/build-gallery.py` to regenerate `assets/js/news-data.js`.

---

## Local preview

```powershell
python -m http.server 8000
```

http://localhost:8000

### Gallery data checks

```powershell
python -m unittest discover -s scripts -p "test_*.py"
```

---

## Deploy

Workflow:

1. Add or edit works under `chapter/`, `special/`, or `companion/`
2. Run `python scripts/build-gallery.py`
3. Commit `gallery-data.js` + images, then push to `main`

→ GitHub Pages deploys the site.

In `Settings → Pages`, set Source to `Deploy from a branch`, branch `main` / `(root)`.
