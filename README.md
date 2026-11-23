# DataiTECH website

Live at **https://dataitech.eu**. The site is built with [Astro](https://astro.build) in `website/`.

## Website (Astro)

| Path | What it is |
| --- | --- |
| `website/src/data/content.json` | **All website text**: hero, challenges, assessment, services, sectors, platforms, method, FAQ, contact, footer, SEO details |
| `website/src/pages/index.astro` | Home page layout (one block per section) |
| `website/src/pages/privacy.astro` | Privacy statement |
| `website/src/layouts/Base.astro` | Page frame: head, SEO tags, header, footer |
| `website/src/components/` | Header, footer, section heading, arrow icon |
| `website/src/styles/global.css` | Premium design (colours, type, layout) |
| `website/src/scripts/site.js` | Menu, header on scroll, 1s-and-0s animation, services index, copy email |
| `website/public/` | Fonts, images, icons, `.htaccess`, `robots.txt`, `sitemap.xml` (copied as-is) |

Work on the site (Node 22.23+):

```
cd website
npm install
npm run dev       # live preview at http://localhost:4321
npm run build     # static site in website/dist (open dist/index.html directly, or upload it)
```

## Publishing to Hostinger

**Automatic (on merge to `main`).** `.github/workflows/publish.yml` builds the site and uploads `website/dist` to `public_html` over FTPS, then checks that dataitech.eu serves the new page. It runs when a change to `website/` lands on `main`, or by hand from the Actions tab ("Publish website" › Run workflow). Only the built site is uploaded.

One-time setup:
1. hPanel › Files › FTP Accounts: create an account (e.g. `deploy`) whose folder is `public_html`. Note the FTP host, username and password.
2. GitHub › repository Settings › Secrets and variables › Actions › New repository secret: add `FTP_SERVER`, `FTP_USERNAME` and `FTP_PASSWORD`.
3. Only if the account's folder is not `public_html` itself: add a repository *variable* `FTP_DIR`, e.g. `public_html/`.

**By hand (fallback).**
1. `python3 tools/make_deploy.py dataitech-website.zip` (builds the site and zips `website/dist`).
2. hPanel › File Manager › `public_html`: delete the old site files, upload the zip, extract, delete the zip.
3. Check https://dataitech.eu.

Earlier live versions are kept in `archive/` (see `archive/README.md`).

Do not connect this repository to Hostinger's Git deployment: it would publish the private `brand-kit/` folder.

## Other files

| File | Purpose |
| --- | --- |
| `index.html` | Previous build of the main site (before Astro), kept for reference |
| `dark.html` | Dark alternative from before Astro (marked `noindex`); not used by the live site |
| `light.html` | Light alternative, built from `dark.html` with `tools/make_light_version.py` (marked `noindex`) |
| `privacy.html` | Privacy statement (AVG/GDPR) – have it reviewed before launch |
| `fonts/` | Self-hosted fonts (Plus Jakarta Sans, Montserrat, Inter, IBM Plex Mono – SIL Open Font License) |
| `favicon-32.png`, `apple-touch-icon.png` | Browser tab and home-screen icons |
| `brand-kit/` | Email signature, invoice template and email templates (see brand-kit/README.md) |
| `images/` | Logo (light and dark versions) and service illustrations (WebP); `images/dark/` has transparent versions for the dark site |
| `og-image.png` | 1200×630 preview image for LinkedIn and other social links |
| `tools/` | Build scripts for the site versions, illustrations, invoice and brand kit |
