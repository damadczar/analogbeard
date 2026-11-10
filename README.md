# analogbeard.com

The Analog Beard website: for now a single "coming soon" page. Curious inventions. Greybeard
ingenuity. Circuits, code, coin-op.

The tagline's first word rotates: the page says "Curious" (what search engines and link previews
see), and it changes only when the tube goes out and relights (every 15 to 35 seconds, see below):
the word goes dark with the tube and a new one comes on as the filament catches: Uncanny, Curious,
Wondrous. Edit `WORDS` there to change the set. Visitors who ask for
reduced motion get one random word and no flicker.

## How it's served

- **GitHub Pages** serves the `main` branch as it is: no build step (`.nojekyll` turns off Jekyll).
- **Cloudflare** sits in front for the domain (`CNAME`: analogbeard.com): it handles HTTPS, the
  http-to-https redirect and `www` to the bare domain.

## Files

| File | What |
|---|---|
| `index.html` | The page; CSS is inline. The logo is inlined between the `logo:start` / `logo:end` markers. |
| `favicon-32.png`, `favicon-16.png`, `apple-touch-icon.png` | Browser and phone icons |
| `assets/analogbeard_banner_1600.png` | The preview image when the link is shared (Open Graph) |
| `assets/analogbeard_lockup_stacked_dark.svg` | The logo as a file (the page uses the inlined copy) |
| `update_logo.py` | Copies the logo files in from the bearded-logos repo and re-inlines the logo |
| `tools/taglines.sh` | Previews the page with other tagline words: `tools/taglines.sh Uncanny Wondrous "Golden-age machinery"` screenshots each and opens them in Preview |
| `tools/phone.html` | Open in Chrome to see the page at phone widths (390 and 320 px) |

## The logo

The logo comes from the **bearded-logos** repo (`~/code/bearded-logos/analogbeard/web/`); don't edit
it here. After it changes there:

```sh
python3 update_logo.py        # or: python3 update_logo.py /path/to/bearded-logos
```

The logo is inline (not an `<img>`) so the page's CSS can make the tube's glow and filament flicker.

`update_logo.py` also adds a pencil sketch of the tube (a web-only layer: the logo itself stays plain
so it still works as a PCB silkscreen). The page opens on that sketch drawing itself, with
handwritten labels (tube, filament, beard, plug), then the filament catches and the colored tube
fades in over it. After that the stutters only dim the tube, and every 15 to 35 seconds it goes dark for a moment
(dim and partly see-through, so the cold filament and the pencil lines show through) and relights. Charcoal-style pencil shading (seeded random strokes, so re-running the script gives the same drawing) sits over the beard, mustache and glass: dark graphite while the tube is lit, light pencil while it is out, when the beard also goes darker than the glass. The label positions and shading areas are placed by hand for this logo,
so check them by eye if the logo changes. All of the motion is switched off for visitors whose
system asks for reduced motion: they see the lit tube with its labels.

The text is set in Saira and the sketch labels in Nanum Pen Script (both from Google Fonts); the wordmark in the logo stays Fraunces. A film-grain and vignette overlay (CSS, no image files) sits over the whole page.

## Ideas for later

- **"Golden-age machinery."** was the first line of the tagline before "Arcane inventions."
  Keep it in mind as a subheading for the coin-op work (arcade and pinball) when that gets its own
  section or page.
