"""update_logo.py [bearded-logos dir] — copy the Analog Beard logo files in from the bearded-logos
repo (default ~/code/bearded-logos) and inline the stacked dark lockup into index.html, tagging the
glow and filament so the page's CSS can make them flicker. Run it after the logo changes, then commit.
The site itself has no build step: GitHub Pages serves these files as they are."""
import os, re, shutil, sys

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
for g in ('<g fill="#2b2420"><circle', '<g clip-path="url(#bc)">', '<g fill="#6e6a64"'):
    need(g, f"the group {g}")
    svg = svg.replace(g, '<g class="art" ' + g[3:], 1)

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
    '<text class="small" x="70" y="134" text-anchor="end">(12AX7)</text>'
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

p = os.path.join(HERE, "index.html"); html = open(p).read()
html = re.sub(r"(<!-- logo:start[^>]*-->\n).*?(<!-- logo:end -->)", lambda m: m.group(1) + svg + "\n" + m.group(2), html, flags=re.S)
open(p, "w").write(html)
print("logo updated")
