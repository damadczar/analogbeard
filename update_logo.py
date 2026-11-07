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

p = os.path.join(HERE, "index.html"); html = open(p).read()
html = re.sub(r"(<!-- logo:start[^>]*-->\n).*?(<!-- logo:end -->)", lambda m: m.group(1) + svg + "\n" + m.group(2), html, flags=re.S)
open(p, "w").write(html)
print("logo updated")
