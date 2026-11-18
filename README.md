# DataiTECH website

Static one-page website for DataiTECH (Data Informatics and Technologies), Zoetermeer.

| File | Purpose |
| --- | --- |
| `index.html` | Main site (dark) |
| `light.html` | Light version of the same site (marked `noindex`) |
| `privacy.html` | Privacy statement (AVG/GDPR) – have it reviewed before launch |
| `fonts/` | Self-hosted fonts (Montserrat, Inter, IBM Plex Mono – SIL Open Font License) |
| `favicon.svg` | Browser tab icon |
| `og-image.png` | 1200×630 preview image for LinkedIn and other social links |

## Before going live

- The canonical URL, `og:url`, `og:image` and structured data assume the site runs at `https://www.dataitechbv.com/`. Change them in the `<head>` of `index.html` if the domain differs.
- Replace the LinkedIn link in the contact section with the company page.
- No build step: upload the files to any static host (for example Netlify, Cloudflare Pages, GitHub Pages or your own web server) and serve over HTTPS.
