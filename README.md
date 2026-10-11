# G Con Associates — V2

A separate, modern engineering-consultancy website for **G Con Associates** (architecture, structural engineering, project management), New Town, Kolkata.

**Live:** https://nelbinxav.github.io/gcon-associates-v2/

V1 (https://nelbinxav.github.io/gcon-associates/) is a different repository and is not touched by this project.

## Design concept

*Premium architecture + engineering precision + a blue identity.* Editorial composition and generous white space (from V1), with the technical language, project numbering and specification detail of V2.

- **Palette:** Navy `#0A2342`, Deep blue `#123B68`, Professional blue `#1769AA`, Technical blue `#2F80ED`, pale blues and white. A single warm neutral `#F5F3EF` is used once.
- **Type:** Space Grotesk (headings, navigation), Inter (body), IBM Plex Mono (project numbers, labels, metadata).
- **Shapes:** rectangles, rules and grids; radius 2px.
- **Imagery:** the company has no project photography, so all imagery is drawn: windowed architectural elevations generated from the figures in the company profile (floor counts, beds, acres, areas), clearly labelled as schematic. Real photographs can replace them in `tools/build.py` / `index.src.html` when available.
- **Content:** every figure, name and qualification comes from the company profile and V1. Nothing is invented.

## Technology

Static HTML, CSS and vanilla JS (nav, scroll reveals, counters, building-type tabs). No frameworks, no build step at runtime. SVG drawings are generated at author time.

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
