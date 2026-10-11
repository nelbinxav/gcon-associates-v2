#!/usr/bin/env python3
"""Builds index.html from index.src.html by expanding {{token}} markers into
static inline SVG illustrations. Run from the repo root: python3 tools/build.py

The company has no project photography, so imagery is drawn: architectural
elevations built only from figures in the company profile (floor counts,
beds, acres, areas). Everything is schematic and labelled as such."""
import pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent

DAY = dict(sky="#EDF5FC", band="#DDEAF6", ground="#CFE0F0", body="#FFFFFF", edge="#123B68", win="#9EC4E8",
           lit="#9EC4E8", shade="#0A2342", shadeop=".13", cap="#123B68", grid="#2F80ED", gridop=".08",
           text="#0A2342", muted="#5C6977", tree="#BCD4EA", line="#1769AA", accent="#2F80ED")
DUSK = dict(sky="#0A2342", band="#0F315B", ground="#071A33", body="#123B68", edge="#5E9BE0", win="#1B528A",
            lit="#CFE6FF", shade="#050F1E", shadeop=".34", cap="#6FA8E0", grid="#2F80ED", gridop=".16",
            text="#EAF3FF", muted="#9CB7D6", tree="#0D2B50", line="#6FA8E0", accent="#2F80ED")

_uid = [0]


def uid():
    _uid[0] += 1
    return f"u{_uid[0]}"


def rng(seed):
    s = [seed]

    def r():
        s[0] = (s[0] * 1103515245 + 12345) & 0x7FFFFFFF
        return s[0] / 0x7FFFFFFF
    return r


def tower(x, base, w, floors, fh, th, cols=None, lit=0.0, seed=1, plant=True, lobby=True):
    """A windowed block. Windows come from one SVG pattern, keeping markup small."""
    h = floors * fh
    y = base - h
    cols = cols or max(3, round(w / (fh * 1.15)))
    pw = w / cols
    pid = "p" + uid()
    o = [
        f'<defs><pattern id="{pid}" x="{x:.1f}" y="{y:.1f}" width="{pw:.2f}" height="{fh}" patternUnits="userSpaceOnUse">'
        f'<rect x="{pw*.15:.2f}" y="{fh*.24:.2f}" width="{pw*.70:.2f}" height="{fh*.52:.2f}" fill="{th["win"]}"/></pattern></defs>',
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{th["body"]}" stroke="{th["edge"]}" stroke-width="1.4"/>',
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="url(#{pid})"/>',
    ]
    if lit:
        r = rng(seed)
        for rr in range(floors):
            for cc in range(cols):
                if r() < lit:
                    o.append(f'<rect x="{x+cc*pw+pw*.15:.1f}" y="{y+rr*fh+fh*.24:.1f}" width="{pw*.70:.1f}" height="{fh*.52:.1f}" fill="{th["lit"]}"/>')
    o.append(f'<rect x="{x+w*.8:.1f}" y="{y:.1f}" width="{w*.2:.1f}" height="{h:.1f}" fill="{th["shade"]}" fill-opacity="{th["shadeop"]}"/>')
    if lobby:
        o.append(f'<rect x="{x:.1f}" y="{base-fh*1.25:.1f}" width="{w:.1f}" height="{fh*1.25:.1f}" fill="{th["body"]}" stroke="{th["edge"]}" stroke-width="1"/>')
        o.append(f'<rect x="{x+w*.08:.1f}" y="{base-fh*1.05:.1f}" width="{w*.84:.1f}" height="{fh*.95:.1f}" fill="{th["win"]}" fill-opacity=".75"/>')
    o.append(f'<rect x="{x-3:.1f}" y="{y-4:.1f}" width="{w+6:.1f}" height="4" fill="{th["cap"]}"/>')
    if plant:
        o.append(f'<rect x="{x+w*.3:.1f}" y="{y-fh*.9-4:.1f}" width="{w*.4:.1f}" height="{fh*.9:.1f}" fill="{th["body"]}" stroke="{th["edge"]}" stroke-width="1.2"/>')
        o.append(f'<line x1="{x+w*.5:.1f}" y1="{y-fh*.9-4:.1f}" x2="{x+w*.5:.1f}" y2="{y-fh*.9-24:.1f}" stroke="{th["edge"]}" stroke-width="1.4"/>')
    return "".join(o)


def tree(x, base, h, th):
    return (f'<rect x="{x-1.5}" y="{base-h*.28:.1f}" width="3" height="{h*.28:.1f}" fill="{th["tree"]}"/>'
            f'<ellipse cx="{x}" cy="{base-h*.62:.1f}" rx="{h*.17:.1f}" ry="{h*.4:.1f}" fill="{th["tree"]}"/>')


def trees(xs, base, th, h=70):
    return "".join(tree(x, base, h * (0.8 + (i % 3) * 0.2), th) for i, x in enumerate(xs))


def tag(x, y, text, th, size=15, anchor="middle", fill=None):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" class="t" fill="{fill or th["text"]}">{text}</text>'


def leader(x, y1, y2, th):
    return f'<line x1="{x:.1f}" y1="{y1:.1f}" x2="{x:.1f}" y2="{y2:.1f}" stroke="{th["line"]}" stroke-width="1" stroke-dasharray="2 4"/>'


def scene(vb_w, vb_h, base, inner, label, th, ground_h=None, slice_=True, grid=100):
    gh = ground_h if ground_h is not None else vb_h - base
    g = []
    for gx in range(0, vb_w + 1, grid):
        g.append(f'M{gx} 0V{vb_h}')
    for gy in range(0, vb_h + 1, grid):
        g.append(f'M0 {gy}H{vb_w}')
    par = "xMidYMid slice" if slice_ else "xMidYMid meet"
    return (
        f'<svg class="scene" viewBox="0 0 {vb_w} {vb_h}" preserveAspectRatio="{par}" role="img" aria-label="{label}">'
        f'<rect width="{vb_w}" height="{vb_h}" fill="{th["sky"]}"/>'
        f'<rect y="{base-vb_h*.17:.0f}" width="{vb_w}" height="{vb_h*.17:.0f}" fill="{th["band"]}"/>'
        f'<path d="{"".join(g)}" stroke="{th["grid"]}" stroke-opacity="{th["gridop"]}" stroke-width="1" fill="none"/>'
        f'<rect y="{base}" width="{vb_w}" height="{gh}" fill="{th["ground"]}"/>'
        f'{inner}'
        f'<line x1="0" y1="{base}" x2="{vb_w}" y2="{base}" stroke="{th["edge"]}" stroke-width="1.6"/></svg>'
    )


def skyline(vb_w, base, th, seed=3):
    """Faint, abstract background massing for depth. Not a depiction of real context."""
    r = rng(seed)
    o, x = [], -20
    while x < vb_w:
        w = 50 + r() * 70
        h = 50 + r() * 150
        o.append(f'<rect x="{x:.0f}" y="{base-h:.0f}" width="{w:.0f}" height="{h:.0f}" fill="{th["band"]}" fill-opacity=".85"/>')
        x += w + 8 + r() * 30
    return "".join(o)


# ----------------------------------------------------------------- scenes
def union_group(th, vb_w, base, fh, ws, gap, lit=0.0, label_size=17):
    floors = [18, 24, 10]  # G+17, G+23, G+9 above ground
    names = ["B+G+17", "B+G+23", "B+G+9"]
    total = sum(ws) + gap * 2
    x = (vb_w - total) / 2
    o = [skyline(vb_w, base, th)]
    pod_h = fh * 1.9
    o.append(f'<rect x="{x-34:.1f}" y="{base-pod_h:.1f}" width="{total+68:.1f}" height="{pod_h:.1f}" fill="{th["body"]}" stroke="{th["edge"]}" stroke-width="1.4"/>')
    o.append(f'<rect x="{x-24:.1f}" y="{base-fh*1.5:.1f}" width="{total+48:.1f}" height="{fh*.9:.1f}" fill="{th["win"]}" fill-opacity=".7"/>')
    for i, (fl, w, nm) in enumerate(zip(floors, ws, names)):
        o.append(tower(x, base - pod_h + 1, w, fl, fh, th, lit=lit, seed=7 + i, lobby=False))
        top = base - pod_h - fl * fh - fh * .9 - 4
        o.append(leader(x + w / 2, top - 24, top - 46, th))
        o.append(tag(x + w / 2, top - 56, nm, th, label_size))
        x += w + gap
    o.append(trees([40, 90, vb_w - 60, vb_w - 110], base, th, 80))
    return "".join(o)


def hero_scene():
    th = DUSK
    return scene(820, 760, 640, union_group(th, 820, 640, 20, [150, 126, 138], 26, lit=0.22),
                 "Illustration of the three Union Bank buildings at New Town: a B+G+17 headquarters, B+G+23 residential apartments and a B+G+9 hostel and amenities block", th)


def featured_scene():
    th = DAY
    return scene(1100, 820, 720, union_group(th, 1100, 720, 23, [210, 176, 190], 44, label_size=19),
                 "Illustration of the Union Bank Headquarters complex, New Town, Kolkata: a B+G+17 headquarters, B+G+23 residential apartments and a B+G+9 hostel and amenities block", th)


def sheet_scene():
    """Technical elevation sheet: outline drawing with height dimensions."""
    th = DAY
    vb_w, vb_h, base, fh = 1400, 470, 395, 14.6
    ws, gap = [270, 230, 240], 110
    floors = [18, 24, 10]
    names = ["B+G+17", "B+G+23", "B+G+9"]
    subs = ["HEADQUARTERS", "RESIDENTIAL APARTMENTS", "HOSTEL & AMENITIES"]
    total = sum(ws) + gap * 2
    x = (vb_w - total) / 2
    o = []
    for fl, w, nm, sb in zip(floors, ws, names, subs):
        h = fl * fh
        o.append(f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}" fill="#fff" stroke="{th["line"]}" stroke-width="1.6"/>')
        for i in range(1, 6):
            o.append(f'<line x1="{x+w*i/6:.1f}" y1="{base-h}" x2="{x+w*i/6:.1f}" y2="{base}" stroke="{th["accent"]}" stroke-opacity=".28" stroke-width=".8"/>')
        for f in range(1, fl):
            o.append(f'<line x1="{x}" y1="{base-f*fh:.1f}" x2="{x+w}" y2="{base-f*fh:.1f}" stroke="{th["accent"]}" stroke-opacity=".34" stroke-width=".7"/>')
        o.append(tag(x + w / 2, base - h - 14, nm, th, 19))
        o.append(tag(x + w / 2, base + 30, sb, th, 13, fill=th["muted"]))
        dx = x + w + 20
        o.append(f'<g stroke="{th["line"]}" stroke-width="1"><line x1="{dx}" y1="{base-h}" x2="{dx}" y2="{base}"/><line x1="{dx-5}" y1="{base-h}" x2="{dx+5}" y2="{base-h}"/><line x1="{dx-5}" y1="{base}" x2="{dx+5}" y2="{base}"/></g>')
        x += w + gap
    o.append(f'<line x1="60" y1="{base}" x2="{vb_w-60}" y2="{base}" stroke="{th["edge"]}" stroke-width="2"/>')
    return scene(vb_w, vb_h, base, "".join(o), "Technical elevation of the three Union Bank buildings at relative height", th, ground_h=0, slice_=False, grid=60)


def hospital(th=DAY, vb_w=900, vb_h=680, slice_=True):
    base = vb_h - 110
    fh = 42
    o = [skyline(vb_w, base, th, 11)]
    o.append(tower(60, base, 120, 3, fh, th, plant=False))
    o.append(tower(170, base, 440, 5, fh, th, plant=False, cols=13))
    o.append(tower(610, base, 200, 4, fh, th, plant=False))
    o.append(tower(372, base, 140, 8, fh, th, plant=False, cols=4))
    cx = 442
    o.append(f'<rect x="{cx-21}" y="{base-8*fh+18}" width="42" height="42" fill="{th["line"]}"/>'
             f'<path d="M{cx} {base-8*fh+28}v22M{cx-11} {base-8*fh+39}h22" stroke="#fff" stroke-width="5"/>')
    o.append(f'<rect x="{cx-85}" y="{base-fh*1.25-14}" width="170" height="8" fill="{th["edge"]}"/>')
    o.append(trees([30, 840, 220, 700], base, th, 80))
    return scene(vb_w, vb_h, base, "".join(o), "Illustration of the Neotia Getwel Healthcare Centre in Siliguri, a 250-bed multispecialty hospital", th, slice_=slice_)


def housing(th=DAY, vb_w=900, vb_h=680, slice_=True):
    base = vb_h - 110
    fh = 37
    o = [skyline(vb_w, base, th, 5)]
    o.append(tower(60, base, 120, 9, fh, th, plant=True, cols=4))
    o.append(tower(205, base, 120, 10, fh, th, plant=True, cols=4))
    xs = [365, 480, 595, 710]
    for x in xs:
        o.append(tower(x, base, 95, 5, fh, th, plant=False, cols=3))
    o.append(tag(120, base - 9 * fh - 74, "G+8", th, 18))
    o.append(tag(265, base - 10 * fh - 74, "G+9", th, 18))
    o.append(tag((xs[0] + xs[-1] + 95) / 2, base - 5 * fh - 30, "25 × G+4", th, 18))
    o.append(f'<path d="M{xs[0]} {base-5*fh-14}v-10h{xs[-1]+95-xs[0]}v10" fill="none" stroke="{th["line"]}" stroke-width="1.2"/>')
    o.append(trees([185, 345, 450, 880], base, th, 70))
    return scene(vb_w, vb_h, base, "".join(o), "Illustration of HIDCO co-operative housing at New Town: a G+8 building, a G+9 building and blocks of G+4", th, slice_=slice_)


def punjab():
    th = DUSK
    vb_w, vb_h, base, fh = 1400, 700, 610, 24
    o = [skyline(vb_w, base, th, 9)]
    w, gap = 78, 34
    x0 = (vb_w - (12 * w + 11 * gap)) / 2
    for i in range(12):
        x = x0 + i * (w + gap)
        o.append(tower(x, base, w, 4, fh, th, plant=False, cols=3, lit=0.18, seed=20 + i))
        cx = x + w / 2
        o.append(f'<rect x="{cx-11}" y="{base-4*fh-38}" width="22" height="22" fill="{th["line"]}"/>'
                 f'<path d="M{cx} {base-4*fh-34}v14M{cx-7} {base-4*fh-27}h14" stroke="#fff" stroke-width="3"/>')
        o.append(tag(cx, base + 34, f"H-{i+1:02d}", th, 12, fill=th["muted"]))
    return scene(vb_w, vb_h, base, "".join(o), "Twelve hospital buildings representing the Punjab healthcare renovation programme", th)


def school(th=DAY, vb_w=640, vb_h=480):
    base, fh = vb_h - 100, 40
    o = [skyline(vb_w, base, th, 2)]
    cx = vb_w / 2
    o.append(tower(cx - 220, base, 440, 3, fh, th, plant=False, cols=11))
    o.append(tower(cx - 40, base, 80, 4, fh, th, plant=False, cols=2))
    o.append(f'<line x1="{cx}" y1="{base-4*fh-4}" x2="{cx}" y2="{base-4*fh-44}" stroke="{th["edge"]}" stroke-width="1.4"/><path d="M{cx} {base-4*fh-44}h26l-6 7 6 7h-26z" fill="{th["line"]}"/>')
    o.append(trees([cx - 270, cx + 260, cx + 300], base, th, 80))
    return scene(vb_w, vb_h, base, "".join(o), "Illustration of a school building", th)


def temple(th=DAY, vb_w=640, vb_h=480):
    base = vb_h - 100
    o = [skyline(vb_w, base, th, 4)]
    cx = vb_w / 2
    steps = [(300, 70), (230, 60), (170, 50), (125, 40), (85, 34)]
    y = base
    for w, h in steps:
        y -= h
        o.append(f'<rect x="{cx-w/2}" y="{y}" width="{w}" height="{h}" fill="{th["body"]}" stroke="{th["edge"]}" stroke-width="1.4"/>'
                 f'<rect x="{cx-w/2+w*.78}" y="{y}" width="{w*.22}" height="{h}" fill="{th["shade"]}" fill-opacity="{th["shadeop"]}"/>')
        o.append(f'<line x1="{cx-w/2+8}" y1="{y+h*.5}" x2="{cx+w/2-8}" y2="{y+h*.5}" stroke="{th["win"]}" stroke-width="3"/>')
    o.append(f'<path d="M{cx} {y-34}V{y-8}" stroke="{th["edge"]}" stroke-width="1.6"/><path d="M{cx-20} {y}Q{cx} {y-30} {cx+20} {y}Z" fill="{th["line"]}"/>')
    o.append(f'<rect x="{cx-26}" y="{base-70}" width="52" height="70" fill="{th["win"]}" stroke="{th["edge"]}" stroke-width="1.2"/>')
    o.append(trees([cx - 280, cx - 230, cx + 230, cx + 280], base, th, 85))
    return scene(vb_w, vb_h, base, "".join(o), "Illustration of a temple building", th)


def interior(th=DAY, vb_w=640, vb_h=480):
    e, ln = th["edge"], th["line"]
    ox, oy = (vb_w - 500) / 2, (vb_h - 330) / 2
    o = [
        f'<g transform="translate({ox} {oy-70})">',
        f'<rect x="0" y="70" width="500" height="300" fill="#fff" stroke="{e}" stroke-width="1.6"/>',
        f'<rect x="0" y="340" width="500" height="30" fill="{th["band"]}" stroke="{e}" stroke-width="1.4"/>',
        f'<rect x="40" y="110" width="150" height="150" fill="{th["win"]}" fill-opacity=".6" stroke="{e}" stroke-width="1.4"/>',
        f'<path d="M115 110v150M40 185h150" stroke="{e}" stroke-width="1.2"/>',
        f'<rect x="230" y="270" width="170" height="40" fill="{ln}" fill-opacity=".85"/><rect x="220" y="250" width="190" height="30" fill="{ln}" fill-opacity=".55"/>',
        f'<rect x="250" y="318" width="130" height="14" fill="{e}" fill-opacity=".8"/>',
        f'<path d="M440 70v90" stroke="{e}" stroke-width="1.4"/><path d="M420 160h40l-8-28h-24z" fill="{ln}"/>',
        f'<path d="M230 130h160M230 170h160M230 210h160" stroke="{e}" stroke-width="2"/>',
        f'<rect x="242" y="104" width="22" height="26" fill="{th["win"]}"/><rect x="270" y="110" width="14" height="20" fill="{ln}" fill-opacity=".6"/><rect x="310" y="144" width="26" height="26" fill="{th["win"]}"/>',
        f'<rect x="20" y="300" width="70" height="40" fill="{e}" fill-opacity=".14"/></g>',
    ]
    return scene(vb_w, vb_h, vb_h, "".join(o), "Illustration of an interior design scheme", th, ground_h=0, grid=80)


def hotel(th=DAY, vb_w=900, vb_h=600):
    base, fh = vb_h - 110, 30
    o = [skyline(vb_w, base, th, 6)]
    o.append(tower(220, base, 460, 3, fh, th, plant=False, cols=13))
    o.append(tower(290, base - 3 * fh, 320, 3, fh, th, plant=False, cols=9, lobby=False))
    o.append(tower(360, base - 6 * fh, 180, 3, fh, th, plant=False, cols=5, lobby=False))
    o.append(f'<rect x="60" y="{base+8}" width="140" height="22" fill="{th["win"]}" stroke="{th["edge"]}" stroke-width="1.2"/>')
    o.append(trees([40, 710, 790, 860], base, th, 90))
    return scene(vb_w, vb_h, base, "".join(o), "Illustration of a hospitality building", th)


def tall(th=DAY, vb_w=900, vb_h=600):
    base, fh = vb_h - 100, 21
    o = [skyline(vb_w, base, th, 8)]
    o.append(tower(250, base, 150, 14, fh, th, cols=6))
    o.append(tower(430, base, 180, 22, fh, th, cols=7))
    o.append(tower(640, base, 130, 9, fh, th, cols=5))
    o.append(trees([60, 200, 820], base, th, 80))
    return scene(vb_w, vb_h, base, "".join(o), "Illustration of a commercial tower group", th)


TOKENS = {
    "scene-hero": hero_scene(),
    "scene-featured": featured_scene(),
    "scene-sheet": sheet_scene(),
    "scene-hospital": hospital(),
    "scene-housing": housing(),
    "scene-punjab": punjab(),
    "scene-school": school(),
    "scene-temple": temple(),
    "scene-interior": interior(),
    "type-residential": housing(DAY, 900, 600),
    "type-healthcare": hospital(DAY, 900, 600),
    "type-commercial": tall(),
    "type-education": school(DAY, 900, 600),
    "type-hospitality": hotel(),
    "type-interior": interior(DAY, 900, 600),
    "type-worship": temple(DAY, 900, 600),
}


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
