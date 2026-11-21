"""Builds the upload package for Hostinger: only the public website files.

Usage: python3 tools/make_deploy.py <output.zip>
Collects index.html, privacy.html and every file they reference (images, fonts, icons),
and adds .htaccess, robots.txt and sitemap.xml. Private files (brand-kit/, tools/,
README, the dark and light alternatives) are never included.
"""
import datetime
import os
import re
import sys
import zipfile

SITE = 'https://dataitech.eu/'
PAGES = ['index.html', 'privacy.html']
out = sys.argv[1]

files = set(PAGES) | {'og-image.png'}
for page in PAGES:
    html = open(page).read()
    for ref in re.findall(r'(?:src|href)="([^"#:]+)"', html) + re.findall(r'url\("([^"#:]+)"\)', html):
        ref = ref.split('?')[0]
        if ref and not ref.startswith(('http', 'mailto', 'tel', 'data')) and os.path.isfile(ref):
            files.add(ref)

missing = [f for f in files if not os.path.isfile(f)]
assert not missing, missing
assert not any(f.startswith(('brand-kit/', 'tools/')) for f in files)

today = datetime.date.today().isoformat()
extra = {
    '.htaccess': '''# DataiTECH · dataitech.eu
Options -Indexes
DirectoryIndex index.html

# Always use https://dataitech.eu (no www)
RewriteEngine On
RewriteCond %{HTTPS} !=on [OR]
RewriteCond %{HTTP_HOST} ^www\\. [NC]
RewriteRule ^ https://dataitech.eu%{REQUEST_URI} [L,R=301]

AddType font/woff2 .woff2
AddType image/webp .webp

<IfModule mod_headers.c>
  Header always set Strict-Transport-Security "max-age=31536000"
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"
</IfModule>

<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/html "access plus 0 seconds"
  ExpiresByType image/webp "access plus 1 month"
  ExpiresByType image/png "access plus 1 month"
  ExpiresByType font/woff2 "access plus 1 year"
</IfModule>

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css application/javascript image/svg+xml
</IfModule>
''',
    'robots.txt': f'User-agent: *\nAllow: /\n\nSitemap: {SITE}sitemap.xml\n',
    'sitemap.xml': f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{SITE}</loc><lastmod>{today}</lastmod></url>
  <url><loc>{SITE}privacy.html</loc><lastmod>{today}</lastmod></url>
</urlset>
''',
}

with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in sorted(files):
        z.write(f, f)
    for name, text in extra.items():
        info = zipfile.ZipInfo(name, date_time=datetime.datetime.now().timetuple()[:6])
        info.external_attr = 0o100644 << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, text)
total = sum(os.path.getsize(f) for f in files)
print(f'{out}: {len(files) + len(extra)} files, {total / 1024:.0f} KB of site files')
for f in sorted(files) + sorted(extra):
    print('  ' + f)
