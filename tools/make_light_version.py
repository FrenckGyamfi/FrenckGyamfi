import sys
src, dst = sys.argv[1], sys.argv[2]
h = open(src).read()
OPTIONAL = ('#3A3A3A', '#2E2E2E', 'background: #1C1C1C;', '#343434', '1px solid #333')
def rep(a, b, count=None):
    global h
    n = h.count(a)
    if n == 0 and a in OPTIONAL: return
    assert n, a
    if count is not None: assert n == count, (a, n)
    h = h.replace(a, b)
rep('''  --bg: #060606;
  --panel: #0E0E0E;
  --fg: #FFFFFF;
  --muted: #A9A9A9;
  --dim: #6B6B6B;
  --line: #262626;
  --signal: #D6AE5C;
  --signal-ink: #1A1306;''', '''  --bg: #F6F6F3;
  --panel: #FFFFFF;
  --fg: #0B0B0B;
  --muted: #4E4E4B;
  --dim: #8C8C87;
  --line: #E1E1DC;
  --line-strong: #C9C9C3;
  --chip: #EFEFEA;
  --signal: #D6AE5C;
  --signal-ink: #1A1306;
  --signal-text: #85651F;
  --signal-line: #B8893A;''')
rep('color-scheme: dark;', 'color-scheme: light;', 1)
rep('dark studio frame', 'light studio frame')
rep('Single dark look by design.', 'Single light look by design.')
# yellow used as text → deeper gold
import re
h = re.sub(r'(?<![-\w])color: var\(--signal\);', 'color: var(--signal-text);', h)
h = h.replace('.sorter-bar button:hover { border-color: var(--signal);', '.sorter-bar button:hover { border-color: var(--signal-text);')
rep('border: 1px solid var(--signal); border-radius: 999px; padding: 5px 12px;', 'border: 1px solid var(--signal-text); border-radius: 999px; padding: 5px 12px;')
rep('.svc-index a.active { color: var(--signal-text); }', '.svc-index a.active { color: var(--fg); text-decoration: underline; text-decoration-color: var(--signal); text-decoration-thickness: 3px; text-underline-offset: 6px; }')
# hard-coded dark-theme greys
for a in ['#4A4A4A', '#3A3A3A', '#2E2E2E', '#343434', '1px solid #333']:
    rep(a, 'var(--line-strong)' if not a.startswith('1px') else '1px solid var(--line-strong)')
rep('background: #1C1C1C;', 'background: var(--chip);')
# illustrations
rep('.svc .art .s { stroke: #FFFFFF; stroke-opacity: .55;', '.svc .art .s { stroke: var(--fg); stroke-opacity: .6;')
rep('.svc .art .f { fill: #FFFFFF; fill-opacity: .08; }', '.svc .art .f { fill: var(--signal); fill-opacity: .10; }')
rep('.svc .art .y { stroke: var(--signal);', '.svc .art .y { stroke: var(--signal-line);')
rep('.svc .art .d { fill: #FFFFFF; fill-opacity: .55; }', '.svc .art .d { fill: var(--fg); fill-opacity: .55; }')
rep('.svc .art .g { stroke: #FFFFFF; stroke-opacity: .12;', '.svc .art .g { stroke: var(--fg); stroke-opacity: .10;')
# brand mark
rep('images/logo-on-dark.png', 'images/logo.png', 2)
# hero field
rep('radial-gradient(120% 140% at 85% 50%, #18140B 0%, var(--panel) 55%)', 'radial-gradient(120% 140% at 85% 50%, #FBF1DC 0%, var(--panel) 55%)')
rep("'rgba(214,174,92,' + (0.35 + k * 0.65) + ')'", "'rgba(184,137,58,' + (0.35 + k * 0.65) + ')'")
rep("'rgba(255,255,255,0.12)'", "'rgba(11,11,11,0.10)'")
rep("'rgba(255,255,255,' + (0.28 + k * 0.42) + ')'", "'rgba(11,11,11,' + (0.22 + k * 0.5) + ')'")
rep('color-mix(in srgb, var(--bg) 70%, transparent); padding: 4px 8px;', 'color-mix(in srgb, var(--panel) 85%, transparent); padding: 4px 8px;')
# softer shadow ring on to-top for light ground
rep('0 0 0 6px color-mix(in srgb, var(--signal) 18%, transparent)', '0 6px 18px -6px rgba(0,0,0,.25)')
# contact block: keep light, add a yellow full stop line under email
rep('border-bottom: 1px solid var(--fg); padding-bottom: 8px;', 'border-bottom: 2px solid var(--signal); padding-bottom: 8px;')
open(dst, 'w').write(h)
print('ok')
h = open(dst).read()
h = h.replace('.hl { color: var(--signal-text); }', '.hl { color: var(--signal-line); }')
h = h.replace('.svc h3 { font-size: clamp(1.4rem, 2.2vw, 1.85rem); color: var(--signal-text); }', '.svc h3 { font-size: clamp(1.4rem, 2.2vw, 1.85rem); color: var(--fg); }')
h = h.replace('.sector .ico .y { stroke: var(--signal);', '.sector .ico .y { stroke: var(--signal-line);')
h = h.replace('<meta name="theme-color" content="#060606">', '<meta name="theme-color" content="#F6F6F3">')
h = h.replace('<link rel="canonical" href="https://www.dataitechbv.com/">', '<link rel="canonical" href="https://www.dataitechbv.com/">\n<meta name="robots" content="noindex">')
open(dst, 'w').write(h)
print('light extras ok')
_t = {}
exec(open(__file__.rsplit('/', 1)[0] + '/isotokens.py').read(), _t)
h = open(dst).read()
assert h.count(_t['DARK']) == 1, 'iso tokens'
h = h.replace(_t['DARK'], _t['LIGHT'])
open(dst, 'w').write(h)
print('iso light ok')
h = open(dst).read()
assert h.count('src="images/dark/') == 6
h = h.replace('src="images/dark/', 'src="images/')
h = h.replace('.svc .art.photo { max-width: 340px; height: auto; aspect-ratio: auto; margin-top: 14px; }',
              '.svc .art.photo { max-width: 340px; height: auto; aspect-ratio: auto; margin-top: 14px; border-radius: 12px; background: #FFFFFF; border: 1px solid var(--line); }')
open(dst, 'w').write(h); print('light images ok')
