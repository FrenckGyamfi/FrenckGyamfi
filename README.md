# DataiTECH website

Static one-page website for DataiTECH (Data Informatics and Technologies), Zoetermeer.

| File | Purpose |
| --- | --- |
| `index.html` | **Main site** (premium design). Built from `dark.html`: `python3 tools/build_premium.py dark.html index.html` |
| `dark.html` | Dark alternative, and the **single source of all site text**: edit copy here, then rebuild (marked `noindex`) |
| `light.html` | Light alternative, built from `dark.html` with `tools/make_light_version.py` (marked `noindex`) |
| `privacy.html` | Privacy statement (AVG/GDPR) – have it reviewed before launch |
| `fonts/` | Self-hosted fonts (Plus Jakarta Sans, Montserrat, Inter, IBM Plex Mono – SIL Open Font License) |
| `favicon-32.png`, `apple-touch-icon.png` | Browser tab and home-screen icons |
| `brand-kit/` | Email signature, invoice template and email templates (see brand-kit/README.md) |
| `images/` | Logo (light and dark versions) and service illustrations (WebP); `images/dark/` has transparent versions for the dark site |
| `og-image.png` | 1200×630 preview image for LinkedIn and other social links |
| `tools/` | Build scripts for the site versions, illustrations, invoice and brand kit |

## Before going live

- The canonical URL, `og:url`, `og:image` and structured data assume the site runs at `https://www.dataitechbv.com/`. If the domain differs, change them in `dark.html` and rebuild (see below).
- Replace the LinkedIn link in the contact section with the company page.
- Upload the files to any static host (for example Netlify, Cloudflare Pages, GitHub Pages or your own web server) and serve over HTTPS.

## Changing the website text

1. Edit the text in `dark.html`.
2. Rebuild the other versions:
   - `python3 tools/make_light_version.py dark.html light.html`
   - `python3 tools/build_premium.py dark.html index.html`
