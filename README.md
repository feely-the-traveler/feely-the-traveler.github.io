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
│   └── build-gallery.py    Scan chapter folders → generate gallery-data.js
├── assets/
│   ├── css/style.css
│   ├── img/
│   └── js/
│       ├── gallery-data.js   Auto-generated (do not edit by hand)
│       └── main.js
└── chapter/
    ├── ch1/
    │   ├── name.txt        Chapter name
    │   ├── front.PNG       Prologue image (optional)
    │   ├── front.txt       Prologue story note (optional)
    │   ├── ep01.PNG        Episode image
    │   ├── ep01.txt        Episode story note
    │   ├── back.PNG        Epilogue image (optional)
    │   ├── back.txt        Epilogue story note (optional)
    │   └── ...
    ├── ch2/
    └── ch3/                (hidden on the site until images are added)
└── companion/
    ├── companion.jpg       Companion Feely portrait (artist col 3)
    ├── companion_img.jpg   Artist carrying Feely (artist col 4)
    └── companion.txt       Companion story note (optional)
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

Changes under `chapter/ch*` will regenerate `gallery-data.js` automatically.

### Rules

| File | Role |
|---|---|
| `chapter/chN/` | Chapter folder (`ch1`, `ch2`, `ch10`, …) |
| `name.txt` | Chapter name shown in tabs |
| `front.png`, etc. | Prologue image → shown as **Prologue** (optional; first in the chapter) |
| `front.txt` | Prologue story note |
| `epXX.png`, etc. | Episode image (any case/extension; stem must be `ep01` style) |
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

Not listed in The Journey gallery.

---

## Local preview

```powershell
python -m http.server 8000
```

http://localhost:8000

---

## Deploy

Workflow:

1. Add or edit works under `chapter/`
2. Run `python scripts/build-gallery.py`
3. Commit `gallery-data.js` + images, then push to `main`

→ GitHub Pages deploys the site.

In `Settings → Pages`, set Source to `Deploy from a branch`, branch `main` / `(root)`.
