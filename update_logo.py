"""update_logo.py [bearded-logos dir] — copy the Analog Beard logo files in from the bearded-logos
repo (default ~/code/bearded-logos) and inline the stacked dark lockup into index.html, tagging the
glow and filament so the page's CSS can make them flicker. Run it after the logo changes, then commit.
The site itself has no build step: GitHub Pages serves these files as they are."""
import math, os, random, re, shutil, sys

SRC = os.path.join(os.path.expanduser(sys.argv[1] if len(sys.argv) > 1 else "~/code/bearded-logos"), "analogbeard", "web")
HERE = os.path.dirname(os.path.abspath(__file__))

for f, dest in (("favicon-32.png", ""), ("favicon-16.png", ""), ("apple-touch-icon.png", ""),
                ("analogbeard_banner_1600.png", "assets"), ("analogbeard_lockup_stacked_dark.svg", "assets")):
    shutil.copy(os.path.join(SRC, f), os.path.join(HERE, dest, f))

svg = open(os.path.join(SRC, "analogbeard_lockup_stacked_dark.svg")).read().strip()
tags = [
    ('<circle cx="200" cy="230" r="220" fill="url(#glow)"/>', '<circle class="glow" cx="200" cy="230" r="220" fill="url(#glow)"/>'),
    ('<path d="', '<path class="fil-glow" d="', 'stroke="#ff8a1f"'),
    ('<path d="', '<path class="fil" d="', 'stroke="#ffb347" stroke-width="6"'),
]
svg = svg.replace(*tags[0][:2], 1)
for old, new, marker in tags[1:]:
    # the filament paths: find the <path ...> element carrying the marker attribute and add the class
    m = re.search(r'<path d="[^"]*"[^>]*' + re.escape(marker), svg)
    if not m: sys.exit(f"could not find the element with {marker}: has the logo changed?")
    svg = svg[:m.start()] + svg[m.start():m.end()].replace(old, new, 1) + svg[m.end():]
if 'class="glow"' not in svg: sys.exit("could not find the glow circle: has the logo changed?")
svg = svg.replace("<svg ", '<svg aria-hidden="true" focusable="false" ', 1)


def need(text, what):
    if text not in svg: sys.exit(f"could not find {what}: has the logo changed?")


# --- the site's pencil sketch of the tube (web only: the logo itself stays plain so it still works
# as a PCB silkscreen). The page opens on this drawing, then the tube lights and the colored logo
# fades in over it. The colored parts get class="art" so the page's CSS can fade and dim them, and
# the filament gets its own group so it can light up separately from the glass around it.
g_open = '<g stroke="#2b2420" stroke-linecap="round" stroke-linejoin="round">'
need(g_open, "the outlined group"); need('<path d="M 140 118', "the getter line after the filament")
gi = svg.index(g_open); ge = svg.index('\n</g>', gi)
body = svg[gi + len(g_open):ge]
fg = body.index(' <path class="fil-glow"'); fe = body.index('<path d="M 140 118')
svg = (svg[:gi]
       + f'<g class="art" {g_open[3:]}{body[:fg]}</g>\n<g stroke-linecap="round">{body[fg:fe]}</g>\n'
       + f'<g class="art" {g_open[3:]}{body[fe:]}\n</g>' + svg[ge + 5:])
for g, cls in (('<g fill="#2b2420"><circle', "art"), ('<g clip-path="url(#bc)">', "art beard"),
               ('<g fill="#6e6a64"', "art beard")):   # beard, then mustache
    need(g, f"the group {g}")
    svg = svg.replace(g, f'<g class="{cls}" ' + g[3:], 1)

# every outline of the tube except the filament (which stays real) and the beard's clip path,
# drawn twice with jittered lines like a pencil going over it again
inner = svg[svg.index("<svg", 1):]
shapes = [d for d in re.findall(r'<path (?:class="[^"]*" )?d="([^"]+)"', inner[:inner.index("</svg>")])
          if not d.startswith(("M 172 300 V 150", "M -14.00"))]
strokes = "".join(f'<path pathLength="1" d="{d}"/>' for d in shapes) \
          + '<circle pathLength="1" cx="142" cy="223" r="9"/><circle pathLength="1" cx="258" cy="223" r="9"/>'
# construction lines and handwritten labels; the coordinates are placed by hand for this logo's
# shapes, so check them by eye if the logo changes
notes = (
    '<g class="guides">'
    '<path d="M 200 40 V 520" stroke-dasharray=".02 .015" pathLength="1"/>'
    '<path d="M 85 404 H 320" pathLength="1"/><path d="M 85 96 H 320" pathLength="1"/>'
    '<path pathLength="1" d="M 304 104 V 396 M 296 104 L 304 96 L 312 104 M 296 396 L 304 404 L 312 396"/>'
    '<path d="M 76 104 Q 100 108 121 128"/><path d="M 111 125 L 121 128 L 119 118"/>'
    '<path d="M 316 70 Q 270 92 229 172"/><path d="M 228 161 L 229 172 L 237 164"/>'
    '<path d="M 64 392 Q 80 380 97 362"/><path d="M 86 365 L 97 362 L 95 373"/>'
    '<path d="M 276 486 Q 262 474 248 472"/><path d="M 256 466 L 248 472 L 257 478"/>'
    '</g>'
    '<text x="70" y="108" text-anchor="end">tube</text>'
    '<text class="small" x="70" y="134" text-anchor="end">(2A3)</text>'
    '<text x="320" y="66">filament</text>'
    '<text x="60" y="410" text-anchor="end">beard</text>'
    '<text x="280" y="500">plug</text>'
)
sketch = ('\n<g class="sketch" fill="none" stroke="#e6d9c0" stroke-linecap="round" stroke-linejoin="round">'
          f'<g class="pass1" stroke-width="2.4" filter="url(#pencil1)">{strokes}</g>'
          f'<g class="pass2" stroke-width="1.6" filter="url(#pencil2)" transform="translate(2.2 -1.6) rotate(.6 200 280)">{strokes}</g>'
          f'<g stroke-width="1.6" filter="url(#pencil1)">{notes}</g></g>')
pencil = ''.join(f'<filter id="pencil{n}" x="-10%" y="-10%" width="120%" height="120%">'
                 f'<feTurbulence type="fractalNoise" baseFrequency="{f}" numOctaves="2" seed="{seed}"/>'
                 f'<feDisplacementMap in="SourceGraphic" scale="{s}"/></filter>'
                 for n, f, seed, s in ((1, ".045", 3, 5), (2, ".06", 11, 6)))
need("</defs>", "the defs")
svg = svg.replace("</defs>", pencil + "</defs>", 1)
glow = svg.index('<circle class="glow"'); glow = svg.index("/>", glow) + 2
svg = svg[:glow] + sketch + svg[glow:]   # above the glow, below the colored tube


# --- charcoal shading over the colored tube: dense short strokes, mostly parallel, uneven in
# length, gap, pressure and angle, broken up by a paper-grain filter. One set of strokes is used
# twice: dark graphite while the tube is lit, light pencil while it is out (the page's CSS swaps
# them). Strokes are seeded, so re-running this script gives the same drawing.
def charcoal(box, angle, spacing, seed):
    """Strokes filling box (x0, y0, x1, y1), as a few <path>s grouped by pressure and width."""
    x0, y0, x1, y1 = box
    r = random.Random(seed); a = math.radians(angle)
    dx, dy, nx, ny = math.cos(a), math.sin(a), -math.sin(a), math.cos(a)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; R = math.hypot(x1 - x0, y1 - y0) / 2 + 10
    buckets = {}; t = -R
    while t < R:
        t += spacing * r.uniform(.6, 1.4); s = -R
        while s < R:
            L, gap, ja = r.uniform(10, 34), r.uniform(1, 8), a + r.uniform(-.06, .06)
            px, py = cx + nx * t + dx * s, cy + ny * t + dy * s
            key = (r.choice((.4, .6, .8, 1)), r.choice((.8, 1.1, 1.4)))
            if x0 - 5 < px + dx * L / 2 < x1 + 5 and y0 - 5 < py + dy * L / 2 < y1 + 5:
                buckets.setdefault(key, []).append(f"M{px:.0f} {py:.0f}l{math.cos(ja)*L:.0f} {math.sin(ja)*L:.0f}")
            s += L + gap
    return "".join(f'<path opacity="{o}" stroke-width="{w}" d="{"".join(d)}"/>' for (o, w), d in sorted(buckets.items()))

beard_d = re.search(r'<g class="art beard" clip-path="url\(#bc\)">\s*<path d="([^"]+)"', svg).group(1)
mi = svg.index('<g class="art beard" fill="#6e6a64"'); mustache = re.findall(r'<path d="([^"]+)"', svg[mi:svg.index("</g>", mi)])
glass = re.search(r'<path d="(M 120 404 L 120 128[^"]*)"', svg)
if not glass or not mustache: sys.exit("could not find the glass or mustache for the shading: has the logo changed?")
fades = {"up": (0, 255, 0, 420, ((0, .15), (.55, .55), (1, 1))), "under": (0, 262, 0, 300, ((0, 1), (1, 0))),
         "right": (215, 0, 281, 0, ((0, 0), (1, 1))), "left": (119, 0, 150, 0, ((0, .7), (1, 0)))}
shading_defs = (
    f'<clipPath id="c-beard"><path d="{beard_d}"/></clipPath>'
    '<clipPath id="c-mus">' + "".join(f'<path d="{d}"/>' for d in mustache) + '</clipPath>'
    f'<clipPath id="c-glass"><path d="{glass.group(1)}"/></clipPath>'
    + "".join(f'<linearGradient id="g-{n}" gradientUnits="userSpaceOnUse" x1="{a}" y1="{b}" x2="{c}" y2="{d}">'
              + "".join(f'<stop offset="{o}" stop-color="#fff" stop-opacity="{v}"/>' for o, v in stops) + '</linearGradient>'
              f'<mask id="m-{n}" maskUnits="userSpaceOnUse" x="0" y="0" width="400" height="560">'
              f'<rect width="400" height="560" fill="url(#g-{n})"/></mask>' for n, (a, b, c, d, stops) in fades.items())
    + '<filter id="charcoal" x="-5%" y="-5%" width="110%" height="110%">'
      '<feTurbulence type="fractalNoise" baseFrequency="1.4" numOctaves="2" seed="5" result="n"/>'
      '<feColorMatrix in="n" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 2.2 -.75" result="tooth"/>'
      '<feComposite in="SourceGraphic" in2="tooth" operator="in"/><feGaussianBlur stdDeviation=".35"/></filter>'
    '<g id="shading" stroke-linecap="round" fill="none">'
    f'<g clip-path="url(#c-beard)"><g mask="url(#m-up)">{charcoal((75, 240, 325, 425), 62, 2.6, 1)}</g>'
    f'<g mask="url(#m-under)">{charcoal((80, 255, 320, 305), 58, 2.2, 2)}</g></g>'           # under the mustache
    f'<g clip-path="url(#c-mus)" opacity=".7">{charcoal((85, 240, 315, 275), 64, 2.8, 3)}</g>'
    f'<g clip-path="url(#c-glass)"><g mask="url(#m-right)">{charcoal((205, 96, 282, 410), 66, 2.4, 4)}</g>'
    f'<g mask="url(#m-left)" opacity=".6">{charcoal((118, 96, 155, 410), 66, 2.8, 5)}</g></g></g>'
)
svg = svg.replace("</defs>", shading_defs + "</defs>", 1)
mi = svg.index('<g class="art beard" fill="#6e6a64"')   # again: the defs above it just grew
top = svg.index("</g>", mi) + 4   # on top of the colored tube, after the mustache
svg = (svg[:top]
       + '\n<g class="shade-dark" filter="url(#charcoal)"><use href="#shading" stroke="#2b2420" opacity=".55"/></g>'
       + '<g class="shade-light" filter="url(#charcoal)"><use href="#shading" stroke="#e6d9c0" opacity=".35"/></g>'
       + svg[top:])

p = os.path.join(HERE, "index.html"); html = open(p).read()
html = re.sub(r"(<!-- logo:start[^>]*-->\n).*?(<!-- logo:end -->)", lambda m: m.group(1) + svg + "\n" + m.group(2), html, flags=re.S)
open(p, "w").write(html)
print("logo updated")
