"""Builds premium.html from light.html: dark glowing hero/contact/footer, dotted light body,
floating white cards, bold Plus Jakarta Sans headlines, glowing gold pills."""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
h = open(src).read()
def rep(a, b, count=1):
    global h
    n = h.count(a); assert n == count, (a[:80], n); h = h.replace(a, b)

# --- fonts ---
rep('/*FONTFACE*/\n', '/*FONTFACE*/\n' + ''.join(
    f'@font-face {{ font-family: "Plus Jakarta Sans"; font-weight: {w}; font-display: swap; src: url("fonts/plus-jakarta-sans-latin-{w}-normal.woff2") format("woff2"); }}\n' for w in (600, 700, 800)))

# --- dark zones: header, hero, contact, footer ---
rep('<header class="site-header gutter">', '<header class="site-header gutter dz">')
rep('<section class="hero gutter">', '<section class="hero gutter dz">')
rep('<section class="contact gutter" id="contact">', '<section class="contact gutter dz" id="contact">')
rep('<footer class="gutter divider">', '<footer class="gutter divider dz">')
rep('<section class="section gutter offer-sec" id="first-engagement">', '<section class="section gutter offer-sec dz" id="first-engagement">')
rep('<section class="section gutter" id="how-we-work">', '<section class="section gutter dz" id="how-we-work">')
h = h.replace('src="images/logo.png"', 'src="images/logo-on-dark.png"')

rep('<h1>Data and AI.<br>', '<h1>Data and AI<span class="pd">.</span><br>')

# --- hero canvas: light dots on dark ---
rep("'rgba(184,137,58,' + (0.35 + k * 0.65) + ')'", "'rgba(236,190,96,' + (0.35 + k * 0.65) + ')'")
rep("'rgba(11,11,11,0.10)'", "'rgba(255,255,255,0.10)'")
rep("'rgba(11,11,11,' + (0.22 + k * 0.5) + ')'", "'rgba(255,255,255,' + (0.16 + k * 0.5) + ')'")

# --- the banner becomes a centred brand statement on the dotted background ---
h, n = re.subn(r'<div class="marquee".*?</div>\s*</div>', '''<section class="statement-p gutter" aria-label="Our conviction">
    <div class="rail">
      <p>No data, no business<span class="pd">.</span><br>No protection, no data<span class="pd">.</span><br>We turn <span class="dim">raw data</span> into <span class="gold">decisions you can&nbsp;trust</span><span class="pd">.</span></p>
    </div>
  </section>''', h, count=1, flags=re.S)
assert n == 1

PREMIUM = '''
/* ===== Premium layer ===== */
:root {
  --bg: #F7F6F2; --panel: #FFFFFF; --fg: #14171F; --muted: #4F5563; --dim: #8A8F9A; --line: #E7E4DC; --line-strong: #D6D2C6;
  --signal: #E2B04A; --signal-ink: #14171F; --signal-text: #8C6A1E; --signal-line: #C8952F; --navy: #34426A;
  --font-display: "Plus Jakarta Sans", "Montserrat", "Helvetica Neue", Arial, sans-serif;
  --card-shadow: 0 1px 2px rgba(20,23,31,.04), 0 24px 48px -28px rgba(20,23,31,.28);
  --glow: radial-gradient(55% 75% at 18% 35%, rgba(226,176,74,.24), transparent 62%), radial-gradient(50% 70% at 88% 25%, rgba(74,112,170,.30), transparent 65%), #10141B;
}
body { background: radial-gradient(circle, rgba(20,23,31,.10) 1px, transparent 1.3px) 0 0 / 22px 22px, var(--bg); }
body::before { background: #10141B; }
.dz { --bg: #10141B; --panel: rgba(255,255,255,.04); --fg: #FFFFFF; --muted: #B7BDC8; --dim: #7F8796; --line: rgba(255,255,255,.12); --line-strong: rgba(255,255,255,.22); --signal-text: #ECBE60; --signal-line: #ECBE60; color: var(--fg); }
.hero.dz, .contact.dz, footer.dz { background: var(--glow); }
.site-header.dz { background: rgba(16,20,27,.82); border-bottom-color: rgba(255,255,255,.08); }
.rail { border-left: 0; border-right: 0; }
.divider { border-top: 0; }
h1, h2, h3 { font-family: var(--font-display); }
h1, h2 { font-weight: 800; letter-spacing: -0.04em; }
.hero h1 { font-size: clamp(2.9rem, 7.6vw, 6.4rem); line-height: .98; }
.hero .label .index, .contact .label .index { color: var(--signal); }
.hero .label { text-transform: uppercase; letter-spacing: .14em; font-size: .78rem; color: var(--signal); font-weight: 600; }
.hero h1 .soft { color: #7F8796; }
.hero .hl, .contact .hl { color: var(--signal); }
.hero-copy p { color: #D9DDE4; }
.hero-copy p strong { color: #FFFFFF; }
.field { border: 0; background: transparent; }
.field .tag { background: rgba(255,255,255,.06); color: #9AA2B1; }
.field .tag.r { color: var(--signal); }
.pill { border-color: rgba(20,23,31,.18); }
.dz .pill { border-color: rgba(255,255,255,.28); }
.pill.solid { background: var(--signal); border-color: var(--signal); color: #14171F; font-weight: 600; box-shadow: 0 12px 34px -10px rgba(226,176,74,.75); }
.pill.solid .dot { background: #14171F; }
.pill.solid .dot svg { stroke: var(--signal); }
.statement-p .rail { padding-block: clamp(72px, 10vw, 128px); text-align: center; }
.statement-p p { font-family: var(--font-display); font-weight: 800; font-size: clamp(1.6rem, 3.6vw, 2.8rem); line-height: 1.14; letter-spacing: -0.035em; margin: 0 auto; max-width: 64rem; text-wrap: balance; }
h1 .hl, h2 .hl, .pd { margin-left: -0.06em; }
.statement-p .dim { color: #A3A7B0; }
.statement-p .gold { color: var(--signal-line); }
#challenges { background: radial-gradient(40% 55% at 10% 35%, rgba(226,176,74,.16), transparent 70%), radial-gradient(40% 55% at 92% 65%, rgba(110,145,205,.16), transparent 70%); }
.label { font-weight: 500; }
.label .index { color: var(--navy); }
.section-head p { color: var(--muted); }
/* floating cards */
.challenge, .svc, .step, .tpl { border: 1px solid rgba(20,23,31,.06); border-radius: 18px; background: #FFFFFF; box-shadow: var(--card-shadow); }
.challenge .tag, .svc .num, .step .n { color: var(--navy); letter-spacing: .12em; font-weight: 600; }
.challenge:hover { transform: translateY(-3px); border-color: rgba(226,176,74,.55); }
.challenge .more { color: var(--signal-line); font-weight: 600; }
.svc h3 { color: var(--fg); }
.svc .art.photo { border: 0; border-radius: 14px; }
.svc li { border-radius: 999px; border-color: var(--line); background: #FBFAF7; }
.sectors, .eco { border: 0; gap: 16px; }
.sector, .eco-item { border: 1px solid rgba(20,23,31,.06) !important; border-radius: 18px; background: #FFFFFF; box-shadow: var(--card-shadow); }
.eco-item { padding: 22px 20px; }
.platforms span.p { background: #FFFFFF; border-color: rgba(20,23,31,.08); }
.reasons { border-top: 0; gap: 16px; }
.reasons > div, .reasons > div + div { border: 1px solid rgba(20,23,31,.06); border-radius: 18px; background: #FFFFFF; box-shadow: var(--card-shadow); padding: 24px; }
.reasons .index { margin-bottom: 18px; color: var(--navy); }
.faq { background: #FFFFFF; border: 1px solid rgba(20,23,31,.06); border-radius: 18px; box-shadow: var(--card-shadow); padding: 4px 28px; border-top: 1px solid rgba(20,23,31,.06); }
.faq details:last-child { border-bottom: 0; }
.contact h2 { font-weight: 800; }
.email-box { border-bottom-color: var(--signal); }
.email-box a { color: #FFFFFF; }
footer.dz .rail { color: #9AA2B1; }
footer.dz a { color: #D9DDE4; }
/* dark feature bands: offer + method (white cards on dark, as in the reference slides) */
.offer-sec.dz, #how-we-work.dz { background: var(--glow); }
.dz .label .index { color: var(--signal); }
.dz .offer { background: rgba(255,255,255,.04); border-color: rgba(255,255,255,.12); border-radius: 22px; box-shadow: 0 30px 80px -40px rgba(0,0,0,.6); }
.dz .offer h2 { color: #FFFFFF; }
.dz .offer-lede { color: #C9CED7; }
.dz .offer-lede strong { color: #FFFFFF; }
.dz .offer-facts dd { color: #E3E6EB; }
.dz .step, .dz .reasons > div, .dz .reasons > div + div { --fg: #14171F; --muted: #4F5563; --dim: #8A8F9A; --line: #E7E4DC; --signal-text: #8C6A1E; color: var(--fg); background: #FFFFFF; border-color: rgba(255,255,255,.2); box-shadow: 0 30px 70px -40px rgba(0,0,0,.7); }
.dz .commit-head { color: #9AA2B1; }
.dz .step .out b { color: var(--signal-text); }
@media (max-width: 960px) { .reasons > div, .reasons > div + div, .reasons > div:nth-child(2n) { border: 1px solid rgba(20,23,31,.06); padding: 22px; } }
'''
rep('</style>\n</head>', PREMIUM + '</style>\n</head>')
h = h.replace('<meta name="theme-color" content="#F6F6F3">', '<meta name="theme-color" content="#10141B">')
open(dst, 'w').write(h); print('premium ok')
