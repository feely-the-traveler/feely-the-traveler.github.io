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
    │   ├── ep01.PNG        Episode image
    │   ├── ep01.txt        Episode story note
    │   └── ...
    ├── ch2/
    └── ch3/                (hidden on the site until images are added)
```

---

## Adding a new chapter / artwork (no HTML edits)

### 1. Add folders and files only

```
chapter/ch3/
  name.txt          ← chapter name (one line)
  ep01.jpg          ← image (.png / .jpg / .jpeg / .webp)
  ep01.txt          ← story note (optional)
  ep02.png
  ep02.txt
```

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
| `epXX.png`, etc. | Artwork image (any case/extension; stem must be `ep01` style) |
| `epXX.txt` | Story note → shown in the card / lightbox |

Only episodes with an image are included. Notes without an image are skipped.

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
