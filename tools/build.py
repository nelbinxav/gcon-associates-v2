#!/usr/bin/env python3
"""Builds index.html from index.src.html by expanding {{drawing}} tokens
into static inline SVG linework. Run from the repo root: python3 tools/build.py
Only figures present in the G Con Associates company profile are drawn."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
BLUE, NAVY, BRIGHT = "#1557A6", "#0B1F3A", "#2F80ED"


def dim_v(x, y1, y2, label, side=1):
    """Vertical dimension line with end ticks and a rotated label."""
    mid = (y1 + y2) / 2
    return (
        f'<g class="dim"><line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}"/>'
        f'<line x1="{x-4}" y1="{y1}" x2="{x+4}" y2="{y1}"/>'
        f'<line x1="{x-4}" y1="{y2}" x2="{x+4}" y2="{y2}"/>'
        f'<text x="{x+side*8}" y="{mid}" transform="rotate(-90 {x+side*8} {mid})" text-anchor="middle">{label}</text></g>'
    )


def dim_h(y, x1, x2, label):
    mid = (x1 + x2) / 2
    return (
        f'<g class="dim"><line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}"/>'
        f'<line x1="{x1}" y1="{y-4}" x2="{x1}" y2="{y+4}"/>'
        f'<line x1="{x2}" y1="{y-4}" x2="{x2}" y2="{y+4}"/>'
        f'<text x="{mid}" y="{y-7}" text-anchor="middle">{label}</text></g>'
    )


def frame(vb_w, vb_h, body, label, uid):
    return (
        f'<svg class="dwg" viewBox="0 0 {vb_w} {vb_h}" role="img" aria-label="{label}" preserveAspectRatio="xMidYMid meet">'
        f'<defs><pattern id="g{uid}" width="20" height="20" patternUnits="userSpaceOnUse">'
        f'<path d="M20 0H0V20" fill="none" stroke="{BRIGHT}" stroke-opacity=".13" stroke-width=".6"/></pattern></defs>'
        f'<rect width="{vb_w}" height="{vb_h}" fill="url(#g{uid})"/>{body}</svg>'
    )


def elevation(blocks, fh, vb_w, vb_h, label, uid, gap=18, base=None, dims=True, bay=4):
    """blocks: list of (floors, width, tag). Floors are drawn as thin lines."""
    base = base if base is not None else vb_h - 56
    total = sum(w for _, w, _ in blocks) + gap * (len(blocks) - 1)
    x = (vb_w - total) / 2
    out = [f'<line class="ground" x1="12" y1="{base}" x2="{vb_w-12}" y2="{base}" pathLength="1"/>']
    for floors, w, tag in blocks:
        h = floors * fh
        y = base - h
        out.append(f'<rect class="mass" x="{x}" y="{y}" width="{w}" height="{h}" pathLength="1"/>')
        # bays (structural grid)
        for i in range(1, bay):
            bx = x + w * i / bay
            out.append(f'<line class="bay" x1="{bx:.1f}" y1="{y}" x2="{bx:.1f}" y2="{base}"/>')
        # floor lines
        for f in range(1, floors):
            fy = base - f * fh
            out.append(f'<line class="flr" x1="{x}" y1="{fy}" x2="{x+w}" y2="{fy}"/>')
        out.append(f'<rect class="mass2" x="{x+w*0.3}" y="{y-fh*0.8}" width="{w*0.4}" height="{fh*0.8}" pathLength="1"/>')
        out.append(f'<text class="tag" x="{x+w/2}" y="{y-fh*0.8-8}" text-anchor="middle">{tag}</text>')
        # column-head markers on the ground line
        out.append(f'<path class="mark" d="M{x-3} {base+9}h6M{x} {base+6}v6"/>')
        out.append(f'<path class="mark" d="M{x+w-3} {base+9}h6M{x+w} {base+6}v6"/>')
        x += w + gap
    if dims:
        tallest = max(f for f, _, _ in blocks) * fh
        x0 = (vb_w - total) / 2 - 22
        out.append(dim_v(x0, base - tallest, base, "RELATIVE HEIGHT"))
        out.append(dim_h(base + 30, (vb_w - total) / 2, (vb_w + total) / 2, "SCHEMATIC · NOT TO SCALE"))
    return frame(vb_w, vb_h, "".join(out), label, uid)


def site_plan(uid):
    """Abstract site diagram for Neotia Getwel: plot, footprint, dimensions."""
    vb_w, vb_h = 640, 400
    out = [
        '<rect class="mass" x="90" y="60" width="430" height="250" pathLength="1"/>',
        '<rect class="mass2" x="150" y="105" width="200" height="90" pathLength="1"/>',
        '<rect class="mass2" x="150" y="195" width="90" height="70" pathLength="1"/>',
        '<rect class="mass2" x="380" y="105" width="90" height="160" pathLength="1"/>',
    ]
    for i in range(1, 8):  # hatch inside main block
        out.append(f'<line class="bay" x1="{150+i*25}" y1="105" x2="{150+i*25}" y2="195"/>')
    for j in range(1, 4):
        out.append(f'<line class="bay" x1="150" y1="{105+j*22.5}" x2="350" y2="{105+j*22.5}"/>')
    out.append('<path class="mark" d="M90 60l-10-10M520 60l10-10M90 310l-10 10M520 310l10 10"/>')
    out.append(dim_h(345, 90, 520, "SITE · 3.9 ACRES"))
    out.append(dim_v(560, 60, 310, "BUILT AREA · 2 LAKH SQ FT"))
    out.append('<text class="tag" x="250" y="150" text-anchor="middle">250 BEDS</text>')
    out.append('<text class="micro" x="90" y="40">SITE DIAGRAM · SCHEMATIC</text>')
    return frame(vb_w, vb_h, "".join(out), "Schematic site diagram for Neotia Getwel Healthcare Centre, Siliguri: 3.9 acre site, 2 lakh square feet built area, 250 beds", uid)


def hospitals_grid(uid):
    """Twelve markers: 12 hospitals, Punjab. No geography is implied."""
    vb_w, vb_h = 640, 400
    out = []
    n = 0
    for r in range(3):
        for c in range(4):
            n += 1
            x, y = 130 + c * 110, 70 + r * 90
            out.append(f'<rect class="mass2" x="{x}" y="{y}" width="70" height="56" pathLength="1"/>')
            out.append(f'<path class="mark" d="M{x+35-6} {y+28}h12M{x+35} {y+22}v12"/>')
            out.append(f'<text class="micro" x="{x}" y="{y-8}">H-{n:02d}</text>')
    out.append(dim_h(360, 130, 570, "12 HOSPITALS · WORLD BANK SCHEME"))
    return frame(vb_w, vb_h, "".join(out), "Twelve numbered hospital markers representing the Punjab healthcare renovation programme", uid)


def institutions(uid):
    """Simple school and temple elevations (outline only)."""
    vb_w, vb_h = 640, 400
    base = 320
    out = [f'<line class="ground" x1="12" y1="{base}" x2="{vb_w-12}" y2="{base}" pathLength="1"/>']
    # school: long low block with entry
    out.append(f'<rect class="mass" x="60" y="{base-90}" width="260" height="90" pathLength="1"/>')
    out.append(f'<rect class="mass2" x="165" y="{base-120}" width="50" height="120" pathLength="1"/>')
    for i in range(1, 8):
        out.append(f'<line class="bay" x1="{60+i*32.5}" y1="{base-90}" x2="{60+i*32.5}" y2="{base}"/>')
    out.append(f'<line class="flr" x1="60" y1="{base-45}" x2="320" y2="{base-45}"/>')
    out.append(f'<text class="tag" x="190" y="{base-134}" text-anchor="middle">SCHOOLS</text>')
    # temple: base, shikhara-like stepped profile
    out.append(f'<path class="mass" d="M380 {base}V{base-60}H560V{base}" pathLength="1"/>')
    out.append(f'<path class="mass2" d="M410 {base-60}V{base-100}H530V{base-60}M440 {base-100}V{base-135}H500V{base-100}M470 {base-135}V{base-165}H470" pathLength="1"/>')
    out.append(f'<path class="mark" d="M470 {base-165}V{base-185}"/>')
    out.append(f'<text class="tag" x="470" y="{base-196}" text-anchor="middle">WORSHIP</text>')
    out.append(dim_h(base + 34, 60, 560, "SCHEMATIC · NOT TO SCALE"))
    return frame(vb_w, vb_h, "".join(out), "Outline elevations of a school block and a temple, representing the education and worship projects", uid)


def interior(uid):
    """Room plan with door swing and furniture outlines."""
    vb_w, vb_h = 640, 400
    out = [
        '<path class="mass" d="M110 70H530V330H110Z" pathLength="1"/>',
        '<path class="mass2" d="M110 200H330M330 70V200" pathLength="1"/>',
        '<path class="mark" d="M250 200a40 40 0 0 1 40 -40"/>',
        '<rect class="mass2" x="380" y="110" width="110" height="60" pathLength="1"/>',
        '<rect class="mass2" x="380" y="250" width="110" height="50" pathLength="1"/>',
        '<rect class="mass2" x="150" y="240" width="130" height="60" pathLength="1"/>',
        '<rect class="mass2" x="150" y="100" width="60" height="60" pathLength="1"/>',
        '<text class="micro" x="110" y="52">INTERIOR · PLAN DIAGRAM</text>',
        dim_h(360, 110, 530, "HEALTHCARE · HOSPITALITY · RETAIL · RESIDENTIAL"),
    ]
    return frame(vb_w, vb_h, "".join(out), "Schematic room plan representing interior design work", uid)


def hero(uid):
    vb_w, vb_h = 640, 640
    base = 520
    fh = 12.5
    # B+G+17 -> 19 levels incl. basement noted in tag only; draw above-ground G+17 = 18 levels
    blocks = [(18, 150, "B+G+17"), (24, 130, "B+G+23"), (10, 120, "B+G+9")]
    total = sum(w for _, w, _ in blocks) + 24 * 2
    x = (vb_w - total) / 2 + 8
    out = [f'<line class="ground" x1="20" y1="{base}" x2="{vb_w-20}" y2="{base}" pathLength="1"/>']
    names = ["HEADQUARTERS", "RESIDENTIAL", "HOSTEL & AMENITIES"]
    px0 = x - 14
    out.append(f'<rect class="mass2" x="{px0}" y="{base-2*fh}" width="{total-2}" height="{2*fh}" pathLength="1"/>')
    for (fl, w, tag), nm in zip(blocks, names):
        h = fl * fh
        y = base - h
        out.append(f'<rect class="mass" x="{x}" y="{y}" width="{w}" height="{h}" pathLength="1"/>')
        for i in range(1, 5):
            out.append(f'<line class="bay" x1="{x+w*i/5:.1f}" y1="{y}" x2="{x+w*i/5:.1f}" y2="{base}"/>')
        for f in range(1, fl):
            out.append(f'<line class="flr" x1="{x}" y1="{base-f*fh}" x2="{x+w}" y2="{base-f*fh}"/>')
        out.append(f'<rect class="mass2" x="{x+w*0.3}" y="{y-fh}" width="{w*0.4}" height="{fh}" pathLength="1"/>')
        out.append(f'<line class="lead" x1="{x+w/2}" y1="{y-fh}" x2="{x+w/2}" y2="{y-fh-24}"/>')
        out.append(f'<text class="tag" x="{x+w/2}" y="{y-fh-32}" text-anchor="middle">{tag}</text>')
        out.append(f'<text class="micro" x="{x+w/2}" y="{base+22}" text-anchor="middle">{nm}</text>')
        out.append(f'<path class="mark" d="M{x-3} {base+8}h6M{x} {base+5}v6"/>')
        x += w + 24
    out.append(dim_v(40, base - 24 * fh, base, "RELATIVE HEIGHT"))
    out.append(dim_h(base + 56, (vb_w - total) / 2 + 8, (vb_w + total) / 2 - 8, "THREE BUILDINGS · SCHEMATIC · NOT TO SCALE"))
    return frame(vb_w, vb_h, "".join(out),
                 "Schematic elevation of the three Union Bank buildings at New Town: a B+G+17 headquarters, B+G+23 residential apartments and a B+G+9 hostel and amenities block, drawn at relative height", uid)


def icons():
    s = lambda b: f'<svg class="ico" viewBox="0 0 48 48" aria-hidden="true" focusable="false">{b}</svg>'
    return {
        "ico-residential": s('<path d="M10 42V12h16v30M26 42V22h12v20M6 42h36M15 18h6M15 25h6M15 32h6M31 28h2M31 35h2"/>'),
        "ico-healthcare": s('<rect x="8" y="8" width="32" height="32"/><path d="M24 15v18M15 24h18"/>'),
        "ico-commercial": s('<path d="M14 42V6h20v36M8 42h32M20 13h8M20 20h8M20 27h8M20 34h8"/>'),
        "ico-education": s('<path d="M4 18L24 8l20 10-20 10zM12 23v10c0 3 6 6 12 6s12-3 12-6V23M44 18v12"/>'),
        "ico-hospitality": s('<path d="M6 38V12M6 28h36v10M42 28v-6a5 5 0 0 0-5-5H20v11M12 24a4 4 0 1 0 0 .1"/>'),
        "ico-interior": s('<path d="M8 8h32v32H8zM8 24h16M24 8v16M30 40v-8h10"/><path d="M16 24a8 8 0 0 0 8-8" />'),
        "ico-worship": s('<path d="M8 42V26h32v16M12 26c0-8 5-12 12-18 7 6 12 10 12 18M24 4v4M20 42v-8h8v8M4 42h40"/>'),
    }


TOKENS = {
    "dwg-hero": hero("h"),
    "dwg-union": elevation([(18, 62, "B+G+17"), (24, 54, "B+G+23"), (10, 50, "B+G+9")], 9, 640, 400, "Schematic elevation of the Union Bank headquarters, residential and hostel buildings at relative height", "u", gap=16, base=330),
    "dwg-neotia": site_plan("n"),
    "dwg-hidco": elevation([(9, 60, "G+8"), (10, 60, "G+9"), (5, 60, "G+4"), (5, 60, "G+4"), (5, 60, "G+4")], 16, 640, 400, "Schematic elevations of HIDCO co-operative housing blocks of G+8, G+9 and G+4", "d", gap=26, base=330, dims=True),
    "dwg-punjab": hospitals_grid("p"),
    "dwg-edu": institutions("e"),
    "dwg-interior": interior("i"),
}
TOKENS.update(icons())


def main():
    src = (ROOT / "index.src.html").read_text()
    def rep(m):
        k = m.group(1)
        if k not in TOKENS:
            raise SystemExit(f"unknown token {k}")
        return TOKENS[k]
    out = re.sub(r"\{\{([a-z0-9-]+)\}\}", rep, src)
    (ROOT / "index.html").write_text(out)
    print("built index.html", len(out), "bytes")


if __name__ == "__main__":
    main()
