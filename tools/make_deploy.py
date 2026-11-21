"""Builds the Hostinger upload package from the Astro site.

Usage: python3 tools/make_deploy.py <output.zip>
Runs `npm run build` in website/ and zips website/dist: the public site only
(pages, styles, fonts, images, icons, .htaccess, robots.txt, sitemap.xml).
"""
import datetime
import os
import subprocess
import sys
import zipfile

out = os.path.abspath(sys.argv[1])
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'website')
subprocess.run(['npm', 'run', 'build'], cwd=root, check=True, stdout=subprocess.DEVNULL)
dist = os.path.join(root, 'dist')

files = []
for base, _, names in os.walk(dist):
    for n in names:
        files.append(os.path.relpath(os.path.join(base, n), dist))
files.sort()
assert 'index.html' in files and 'privacy.html' in files and '.htaccess' in files
assert not any(f.startswith(('brand-kit', 'tools', 'src', 'node_modules')) for f in files)

with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in files:
        info = zipfile.ZipInfo(f, date_time=datetime.datetime.now().timetuple()[:6])
        info.external_attr = 0o100644 << 16
        info.compress_type = zipfile.ZIP_DEFLATED
        z.writestr(info, open(os.path.join(dist, f), 'rb').read())
total = sum(os.path.getsize(os.path.join(dist, f)) for f in files)
print(f'{out}: {len(files)} files, {total / 1024:.0f} KB')
for f in files:
    print('  ' + f)
