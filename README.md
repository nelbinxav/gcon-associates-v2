# G Con Associates — V2

A separate, modern engineering-consultancy website for **G Con Associates** (architecture, structural engineering, project management), New Town, Kolkata.

**Live:** https://nelbinxav.github.io/gcon-associates-v2/

V1 (https://nelbinxav.github.io/gcon-associates/) is a different repository and is not touched by this project.

## Design concept

*Blueprint precision meets modern architectural consultancy.* White canvas, navy authority, blue identity, with thin technical lines, grids, section numbers and dimension labels as accents.

- **Palette:** Navy `#0B1F3A`, Blue `#1557A6`, Technical blue `#2F80ED`, pale blues and white. Cyan `#55B8D9` only on dark panels.
- **Type:** Space Grotesk (headings), Inter (body), IBM Plex Mono (project numbers, labels, metrics).
- **Shapes:** rectangles, rules and grids; radius 0–3px.
- **Imagery:** the company profile contains no project photography, so the register uses schematic linework drawings generated from the figures in the profile (floor counts, beds, acres, area). They are labelled as schematic and not to scale.
- **Content:** every project figure, name and qualification comes from V1 / the company profile. Nothing was invented.

## Technology

Static HTML, CSS and ~60 lines of vanilla JS. No frameworks, no build step at runtime. SVG drawings are generated at author time.

| File | Purpose |
|---|---|
| `index.src.html` | Page source with `{{drawing}}` tokens |
| `tools/build.py` | Expands tokens into inline SVG → `index.html` |
| `styles.css`, `main.js` | Styles, nav/scroll/reveal behaviour |
| `.github/workflows/pages.yml` | GitHub Pages deployment |

## Local development

```bash
python3 tools/build.py        # regenerate index.html after editing index.src.html
python3 -m http.server 8000   # open http://localhost:8000
```

Edit `index.src.html` (not `index.html`) and rebuild.

## Deployment (GitHub Pages)

Pushing to `main` runs the workflow, which publishes `index.html`, `styles.css`, `main.js`, `favicon.svg`, `og.png` and `robots.txt`.
Repository **Settings → Pages → Source** must be set to **GitHub Actions** (done once).
