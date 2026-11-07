# analogbeard.com

The Analog Beard website: for now a single "coming soon" page. Where old-world electronics meet the
modern age: arcade, audio, pinball.

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

## The logo

The logo comes from the **bearded-logos** repo (`~/code/bearded-logos/analogbeard/web/`); don't edit
it here. After it changes there:

```sh
python3 update_logo.py        # or: python3 update_logo.py /path/to/bearded-logos
```

The logo is inline (not an `<img>`) so the page's CSS can make the tube's glow and filament flicker.
The flicker is switched off for visitors whose system asks for reduced motion.

The text is set in Fraunces (from Google Fonts), the same family as the wordmark.
