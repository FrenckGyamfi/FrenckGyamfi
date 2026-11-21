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

1. `python3 tools/make_deploy.py dataitech-website.zip` (builds the site and zips `website/dist`).
2. hPanel › File Manager › `public_html`: delete the old site files, upload the zip, extract, delete the zip.
3. Check https://dataitech.eu.

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
