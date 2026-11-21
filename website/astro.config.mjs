// DataiTECH website · https://dataitech.eu
import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://dataitech.eu',
  build: { format: 'file' },      // privacy.astro -> /privacy.html, matching the live URLs
  compressHTML: true,
});
