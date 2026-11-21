# DataiTECH website

Static one-page website for DataiTECH (Data Informatics and Technologies), Zoetermeer.

| File | Purpose |
| --- | --- |
| `index.html` | **Main site** (premium design). Built from `dark.html`: `python3 tools/build_premium.py dark.html index.html` |
| `dark.html` | Dark alternative, and the **single source of all site text**: edit copy here, then rebuild (marked `noindex`) |
| `preview-3d.html` | Preview of the main site with a 3D opening scene (`js/hero3d.js`, Three.js in `js/vendor/`, MIT licence). Build: `python3 tools/build_premium.py dark.html preview-3d.html --hero3d` |
| `light.html` | Light alternative, built from `dark.html` with `tools/make_light_version.py` (marked `noindex`) |
| `privacy.html` | Privacy statement (AVG/GDPR) – have it reviewed before launch |
| `fonts/` | Self-hosted fonts (Plus Jakarta Sans, Montserrat, Inter, IBM Plex Mono – SIL Open Font License) |
| `favicon-32.png`, `apple-touch-icon.png` | Browser tab and home-screen icons |
| `brand-kit/` | Email signature, invoice template and email templates (see brand-kit/README.md) |
| `images/` | Logo (light and dark versions) and service illustrations (WebP); `images/dark/` has transparent versions for the dark site |
| `og-image.png` | 1200×630 preview image for LinkedIn and other social links |
| `tools/` | Build scripts for the site versions, illustrations, invoice and brand kit |

## Publishing to Hostinger (dataitech.eu)

1. Build the upload package: `python3 tools/make_deploy.py dataitech-website.zip`.
   It contains only public files; `brand-kit/`, `tools/` and the dark/light alternatives are never included.
2. In Hostinger hPanel, make sure SSL is active for dataitech.eu (Security › SSL). The package forces HTTPS.
3. Open File Manager › `public_html`, delete Hostinger's default page (`default.php` or `index.php`), upload the zip and extract it there.
4. Check https://dataitech.eu, then submit `https://dataitech.eu/sitemap.xml` in Google Search Console.

Do not connect this repository to Hostinger's Git deployment: it would publish the private `brand-kit/` folder.

## Changing the website text

1. Edit the text in `dark.html`.
2. Rebuild the other versions:
   - `python3 tools/make_light_version.py dark.html light.html`
   - `python3 tools/build_premium.py dark.html index.html`
