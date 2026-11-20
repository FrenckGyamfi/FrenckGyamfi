"""Builds premium.html: a clean, single-stylesheet premium page.

Content (challenges, assessment, services, sectors, platforms, method, FAQ, contact text,
metadata) is read from index.html, so copy changes are made once and flow into every version.
Usage: python3 tools/build_premium.py index.html premium.html
"""
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
h = open(src).read()


def one(pattern, text=h, flags=re.S):
    m = re.search(pattern, text, flags)
    if not m:
        raise SystemExit(f'pattern not found: {pattern[:70]}')
    return m.group(1)


def section(sid):
    return one(r'<section[^>]*id="%s">(.*?)\n  </section>' % sid)


def head(sec):
    """(h2 html, intro paragraph html) from a section-head block."""
    m = re.search(r'<h2>(.*?)</h2>\s*</div>\s*<p>(.*?)</p>', sec, re.S)
    return m.group(1), m.group(2)


meta = one(r'(<meta name="description".*?<meta name="twitter:card"[^>]*>)')
meta = meta.replace('<meta name="theme-color" content="#060606">', '<meta name="theme-color" content="#0F131A">')
jsonld = one(r'(<script type="application/ld\+json">.*?</script>)')
hero_lead = one(r'<div class="hero-copy">\s*<p>(.*?)</p>')

s_ch = section('challenges'); ch_h2, ch_p = head(s_ch)
challenges = one(r'<div class="challenges">\n(.*?)\n      </div>', s_ch)

s_of = section('first-engagement')
of_h2 = one(r'<h2>(.*?)</h2>', s_of)
of_lede = one(r'<p class="offer-lede">(.*?)</p>', s_of)
of_facts = one(r'<dl class="offer-facts">\n(.*?)\n\s*</dl>', s_of)

s_sv = section('services'); sv_h2, sv_p = head(s_sv)
sv_index = one(r'<ul class="svc-index" id="svc-index">\n(.*?)\n\s*</ul>', s_sv)
sv_cards = one(r'<div class="svc-cards">\n(.*</article>)', s_sv).replace('src="images/dark/', 'src="images/')

s_se = section('sectors'); se_h2, se_p = head(s_se)
sectors = one(r'<div class="sectors">\n(.*</article>)', s_se)

s_te = section('technology'); te_h2, te_p = head(s_te)
eco = one(r'<div class="eco"[^>]*>\n(.*?)\n      </div>', s_te)
toolkit = one(r'<span class="lbl">Also in our toolkit</span>\n(.*?)\n      </div>', s_te)

s_hw = section('how-we-work'); hw_h2, hw_p = head(s_hw)
steps = one(r'<div class="steps">\n(.*</article>)', s_hw)
outcomes = one(r'<div class="reasons">\n(.*?)\n      </div>', s_hw)

s_fq = section('faq'); fq_h2, fq_p = head(s_fq)
faq = one(r'<div class="faq">\n(.*</details>)', s_fq)

contact_p = one(r'<div class="contact-row">\s*<p>(.*?)</p>')
footer_legal = one(r'<div class="legal">\n(.*?)\n    </div>').replace('<img class="foot-logo"', '<img class="foot-logo"')

ARROW = '<span class="dot" aria-hidden="true"><svg viewBox="0 0 12 12" fill="none" stroke-width="1.7"><path d="M2 10 10 2M4 2h6v6"/></svg></span>'
NAV = [('first-engagement', 'Assessment'), ('services', 'Services'), ('sectors', 'Sectors'),
       ('technology', 'Platforms'), ('how-we-work', 'Method'), ('faq', 'FAQ')]
nav_links = '\n'.join(f'        <a href="#{i}">{t}</a>' for i, t in NAV)
nav_mobile = '\n'.join(f'      <a href="#{i}">{t}</a>' for i, t in NAV + [('contact', 'Contact')])

FONTFACE = ''.join(
    f'@font-face {{ font-family: "{fam}"; font-weight: {w}; font-display: swap; src: url("fonts/{file}-latin-{w}-normal.woff2") format("woff2"); }}\n'
    for fam, file, weights in [('Plus Jakarta Sans', 'plus-jakarta-sans', (600, 700, 800)),
                               ('Inter', 'inter', (400, 500)),
                               ('IBM Plex Mono', 'ibm-plex-mono', (400, 500))]
    for w in weights)

CSS = r'''
/* DataiTECH premium. Dark glowing bands for the moments that matter (opening, offer, method, contact),
   a warm dotted paper for reading, and white cards that float above it. One gold accent from the logo. */
:root {
  --ink: #0F131A;            /* dark bands */
  --ink-2: #0B0E13;          /* footer */
  --paper: #F7F6F2;          /* light bands */
  --card: #FFFFFF;
  --text: #14171F;
  --muted: #535866;
  --dim: #8A8F9A;
  --line: #E8E5DD;
  --gold: #E2B04A;           /* accent on dark, buttons */
  --gold-deep: #8E6A1F;      /* gold text on light (AA contrast) */
  --gold-line: #C8952F;      /* gold marks on light */
  --navy: #33415F;           /* eyebrows on light */
  --on-dark: #FFFFFF;
  --on-dark-muted: #B8BEC9;
  --on-dark-dim: #7F8796;
  --display: "Plus Jakarta Sans", "Helvetica Neue", Arial, sans-serif;
  --body: "Inter", "Helvetica Neue", Arial, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
  --wrap: 76rem;
  --radius: 22px;
  --shadow: 0 1px 2px rgba(20,23,31,.04), 0 28px 56px -32px rgba(20,23,31,.30);
  --glow: radial-gradient(55% 75% at 16% 30%, rgba(226,176,74,.22), transparent 62%),
          radial-gradient(50% 70% at 88% 22%, rgba(74,112,170,.30), transparent 65%), var(--ink);
  color-scheme: light;
}
*, *::before, *::after { box-sizing: border-box; }
html { scroll-behavior: smooth; scroll-padding-top: 84px; }
@media (prefers-reduced-motion: reduce) { html { scroll-behavior: auto; } }
body {
  margin: 0; color: var(--text); font: 400 1rem/1.65 var(--body); -webkit-font-smoothing: antialiased;
  background: radial-gradient(circle, rgba(20,23,31,.09) 1px, transparent 1.3px) 0 0 / 22px 22px, var(--paper);
}
body::before { content: ""; position: fixed; inset: 0 0 auto; height: env(safe-area-inset-top, 0px); z-index: 30; background: var(--ink); }
img { max-width: 100%; height: auto; }
a { color: inherit; }
p { margin: 0; }
h1, h2, h3 { margin: 0; font-family: var(--display); text-wrap: balance; }
h1, h2 { font-weight: 800; letter-spacing: -0.04em; }
h2 { font-size: clamp(2.2rem, 4.6vw, 3.7rem); line-height: 1.02; }
h3 { font-weight: 700; letter-spacing: -0.02em; }
.hl, .pd { margin-left: -0.05em; }
.hl { color: var(--gold-line); }
:focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; border-radius: 6px; }

.wrap { max-width: var(--wrap); margin: 0 auto; padding-left: max(20px, env(safe-area-inset-left, 0px)); padding-right: max(20px, env(safe-area-inset-right, 0px)); }
.band { padding-block: clamp(72px, 8.5vw, 116px); }
.statement + .band { padding-top: clamp(16px, 2vw, 28px); }
.dark { background: var(--glow); color: var(--on-dark); }
.dark .hl { color: var(--gold); }
.eyebrow { font: 600 0.76rem/1.2 var(--body); letter-spacing: 0.14em; text-transform: uppercase; color: var(--navy); }
.dark .eyebrow { color: var(--gold); }
.head { display: grid; grid-template-columns: 1.1fr 1fr; gap: 20px 64px; align-items: end; margin-bottom: clamp(32px, 4vw, 52px); }
.head > * { min-width: 0; }
.head h2 { margin-top: 16px; }
.head > p { color: var(--muted); font-size: 1.08rem; max-width: 32rem; }
.dark .head > p { color: var(--on-dark-muted); }
@media (max-width: 860px) { .head { grid-template-columns: 1fr; } }

/* buttons */
.btn { display: inline-flex; align-items: center; gap: 14px; padding: 8px 8px 8px 22px; border-radius: 999px; font: 600 0.95rem var(--body); text-decoration: none; border: 1px solid rgba(20,23,31,.16); color: var(--text); background: transparent; transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease; }
.btn .dot { width: 32px; height: 32px; border-radius: 50%; display: grid; place-items: center; background: var(--text); transition: transform .25s ease; }
.btn .dot svg { width: 12px; height: 12px; stroke: var(--paper); }
.btn:hover .dot { transform: rotate(-45deg); }
.btn.gold { background: var(--gold); border-color: var(--gold); color: #14171F; box-shadow: 0 14px 36px -12px rgba(226,176,74,.8); }
.btn.gold .dot { background: #14171F; }
.btn.gold .dot svg { stroke: var(--gold); }
.btn.gold:hover { transform: translateY(-1px); box-shadow: 0 18px 42px -12px rgba(226,176,74,.9); }
.dark .btn:not(.gold) { color: var(--on-dark); border-color: rgba(255,255,255,.28); }
.dark .btn:not(.gold) .dot { background: #FFFFFF; }
.dark .btn:not(.gold) .dot svg { stroke: var(--ink); }
@media (prefers-reduced-motion: reduce) { .btn, .btn .dot { transition: none; } .btn:hover .dot { transform: none; } }

/* header */
.site-header { position: sticky; top: env(safe-area-inset-top, 0px); z-index: 20; background: var(--ink); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border-bottom: 1px solid transparent; transition: background .25s ease, border-color .25s ease; }
.site-header.scrolled { background: rgba(15,19,26,.9); border-bottom-color: rgba(255,255,255,.08); }
.nav { display: flex; align-items: center; justify-content: space-between; gap: 20px; padding-block: 14px; }
.brand img { display: block; height: 38px; width: auto; }
.nav-links { display: flex; align-items: center; gap: 26px; }
.nav-links a:not(.btn) { color: rgba(255,255,255,.78); text-decoration: none; font-size: .93rem; font-weight: 500; }
.nav-links a:not(.btn):hover { color: #FFFFFF; }
.nav-links .btn { padding: 5px 5px 5px 16px; font-size: .88rem; }
.nav-links .btn .dot { width: 26px; height: 26px; }
.menu-btn { display: none; align-items: center; gap: 10px; background: none; border: 1px solid rgba(255,255,255,.25); color: #FFFFFF; border-radius: 999px; padding: 8px 14px; font: 500 .9rem var(--body); cursor: pointer; }
.menu-btn .bars { width: 16px; height: 10px; position: relative; }
.menu-btn .bars::before, .menu-btn .bars::after { content: ""; position: absolute; left: 0; right: 0; height: 1.6px; background: currentColor; transition: transform .2s ease, top .2s ease; }
.menu-btn .bars::before { top: 1px; } .menu-btn .bars::after { top: 7px; }
.site-header.open .menu-btn .bars::before { top: 4px; transform: rotate(45deg); }
.site-header.open .menu-btn .bars::after { top: 4px; transform: rotate(-45deg); }
.mobile-panel { display: none; }
@media (max-width: 1040px) {
  .nav-links { display: none; }
  .menu-btn { display: inline-flex; }
  .site-header.open { background: rgba(15,19,26,.97); }
  .site-header.open .mobile-panel { display: flex; flex-direction: column; padding-block: 4px 24px; }
  .mobile-panel a { color: #FFFFFF; text-decoration: none; font: 700 1.6rem var(--display); letter-spacing: -0.02em; padding: 12px 0; border-bottom: 1px solid rgba(255,255,255,.1); }
  .mobile-panel a:last-child { border-bottom: 0; color: var(--gold); }
}
@media (max-width: 520px) { .brand img { height: 30px; } }

/* hero */
.hero { position: relative; overflow: hidden; padding-block: clamp(88px, 12vw, 168px) clamp(80px, 10vw, 140px); }
.hero canvas { position: absolute; inset: 0; width: 100%; height: 100%; display: block;
  -webkit-mask-image: linear-gradient(90deg, transparent 0%, transparent 46%, #000 80%); mask-image: linear-gradient(90deg, transparent 0%, transparent 46%, #000 80%); opacity: .9; }
.hero .wrap { position: relative; }
.hero h1 { font-size: clamp(2.6rem, 7vw, 6.2rem); line-height: .98; margin-top: 22px; }
.hero h1 .line { white-space: nowrap; }
@media (max-width: 420px) { .hero h1 .line { white-space: normal; } }
.hero h1 .gold { color: var(--gold); }
.hero-lead { margin-top: 30px; max-width: 36rem; font-size: 1.22rem; line-height: 1.55; color: var(--on-dark-muted); }
.hero-lead strong { color: #FFFFFF; font-weight: 500; }
.hero-ctas { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 38px; }
.assure { list-style: none; margin: 30px 0 0; padding: 0; display: flex; flex-wrap: wrap; gap: 10px 28px; color: var(--on-dark-muted); font-size: .92rem; }
.assure li { display: flex; align-items: center; gap: 9px; }
.assure li::before { content: ""; flex: none; width: 18px; height: 18px; border-radius: 50%; background: rgba(226,176,74,.16) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 18 18'%3E%3Cpath d='M5.2 9.3l2.4 2.4 5.2-5.4' fill='none' stroke='%23E2B04A' stroke-width='1.8' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center / 18px no-repeat; }
@media (max-width: 700px) { .hero canvas { -webkit-mask-image: linear-gradient(180deg, transparent 0%, transparent 55%, #000 100%); mask-image: linear-gradient(180deg, transparent 0%, transparent 55%, #000 100%); opacity: .55; } }

/* statement */
.statement { padding-block: clamp(64px, 8vw, 104px) clamp(56px, 7vw, 88px); text-align: center; }
.statement p { font: 800 clamp(1.6rem, 3.6vw, 2.8rem)/1.14 var(--display); letter-spacing: -0.035em; max-width: 64rem; margin: 0 auto; text-wrap: balance; }
.statement .soft { color: #A3A7B0; }
.statement .gold { color: var(--gold-line); }

/* cards on paper */
.card { background: var(--card); border: 1px solid rgba(20,23,31,.06); border-radius: var(--radius); box-shadow: var(--shadow); }

/* when to call */
#challenges { background: radial-gradient(40% 55% at 8% 35%, rgba(226,176,74,.14), transparent 70%), radial-gradient(40% 55% at 94% 70%, rgba(110,145,205,.14), transparent 70%); }
.challenges { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.challenge { display: flex; flex-direction: column; gap: 12px; padding: 28px; text-decoration: none; color: inherit; min-width: 0; transition: transform .2s ease, border-color .2s ease; }
.challenge:hover { transform: translateY(-3px); border-color: rgba(200,149,47,.5); }
.challenge .tag { font: 600 .7rem/1.3 var(--body); letter-spacing: .12em; text-transform: uppercase; color: var(--navy); }
.challenge h3 { font-size: clamp(1.25rem, 1.8vw, 1.5rem); line-height: 1.15; }
.challenge p { color: var(--muted); font-size: .95rem; }
.challenge .more { margin-top: auto; padding-top: 8px; font-weight: 600; font-size: .92rem; color: var(--gold-deep); }
@media (prefers-reduced-motion: reduce) { .challenge, .challenge:hover { transition: none; transform: none; } }
@media (max-width: 960px) { .challenges { grid-template-columns: 1fr 1fr; } }
@media (max-width: 620px) { .challenges { grid-template-columns: 1fr; } }

/* first engagement */
.offer { display: grid; grid-template-columns: 1.1fr 1fr; gap: clamp(32px, 5vw, 72px); align-items: start; padding: clamp(28px, 5vw, 56px); border-radius: 28px; background: rgba(255,255,255,.045); border: 1px solid rgba(255,255,255,.12); box-shadow: 0 40px 90px -50px rgba(0,0,0,.7); }
.offer > * { min-width: 0; }
.offer h2 { margin-top: 16px; font-size: clamp(2.1rem, 4.4vw, 3.5rem); }
.offer-lede { margin: 20px 0 32px; color: var(--on-dark-muted); font-size: 1.15rem; max-width: 30rem; }
.offer-lede strong { color: #FFFFFF; font-weight: 500; }
.facts { margin: 0; }
.facts > div { padding: 18px 0; border-top: 1px solid rgba(255,255,255,.12); }
.facts > div:last-child { border-bottom: 1px solid rgba(255,255,255,.12); }
.facts dt { font: 600 .72rem var(--body); letter-spacing: .14em; text-transform: uppercase; color: var(--gold); }
.facts dd { margin: 6px 0 0; color: #E4E7EC; }
@media (max-width: 860px) { .offer { grid-template-columns: 1fr; } }

/* services */
.services { display: grid; grid-template-columns: 17rem 1fr; gap: 48px; align-items: start; }
.services > * { min-width: 0; }
.svc-index { position: sticky; top: 104px; list-style: none; margin: 0; padding: 0; display: grid; gap: 4px; }
.svc-index a { display: block; padding: 6px 0 6px 16px; border-left: 2px solid var(--line); color: var(--dim); text-decoration: none; font: 600 1.02rem var(--display); letter-spacing: -0.01em; transition: color .2s ease, border-color .2s ease; }
.svc-index a:hover { color: var(--text); }
.svc-index a.active { color: var(--text); border-left-color: var(--gold-line); }
.svc-cards { display: grid; gap: 20px; }
.svc { display: grid; grid-template-columns: minmax(0, .9fr) minmax(0, 1.1fr); gap: 32px; align-items: center; padding: 28px; scroll-margin-top: 104px; }
.svc .num { display: block; font: 600 .72rem var(--body); letter-spacing: .14em; color: var(--navy); }
.art-tile { display: block; margin-top: 12px; border-radius: 18px; overflow: hidden; isolation: isolate; background: linear-gradient(160deg, #F8F5EE, #EEEAE0); }
.art-tile .art { display: block; width: 100%; height: auto; mix-blend-mode: multiply; }
.svc h3 { font-size: clamp(1.4rem, 2.1vw, 1.75rem); line-height: 1.12; }
.svc p { color: var(--muted); margin-top: 10px; }
.svc .cats { margin-top: 18px; font: 600 .7rem var(--body); letter-spacing: .12em; text-transform: uppercase; color: var(--dim); }
.svc ul { list-style: none; margin: 10px 0 0; padding: 0; display: flex; flex-wrap: wrap; gap: 6px; }
.svc li { font-size: .78rem; padding: 4px 10px; border-radius: 999px; color: var(--muted); border: 1px solid #E6E2D7; }
@media (max-width: 1000px) { .services { grid-template-columns: 1fr; } .svc-index { display: none; } }
@media (max-width: 680px) { .svc { grid-template-columns: 1fr; gap: 16px; padding: 22px; } }

/* sectors */
.sectors { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.sector { padding: 28px; min-width: 0; }
.sector .ico { width: 46px; height: 46px; padding: 9px; border-radius: 14px; background: #F6EEDC; }
.sector .ico .s { fill: none; stroke: var(--text); stroke-opacity: .75; stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }
.sector .ico .y { fill: none; stroke: var(--gold-line); stroke-width: 1.9; stroke-linecap: round; stroke-linejoin: round; }
.sector h3 { margin-top: 18px; font-size: 1.2rem; }
.sector p { margin-top: 8px; color: var(--muted); font-size: .95rem; }
@media (max-width: 960px) { .sectors { grid-template-columns: 1fr 1fr; } }
@media (max-width: 620px) { .sectors { grid-template-columns: 1fr; } }

/* platforms */
.eco { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; }
.eco-item { padding: 22px 20px; display: grid; gap: 4px; align-content: start; min-width: 0; }
.eco-item b { font: 700 1.08rem var(--display); letter-spacing: -0.015em; }
.eco-item span { color: var(--muted); font-size: .86rem; line-height: 1.45; }
.toolkit { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin-top: 28px; }
.toolkit .lbl { font: 600 .72rem var(--body); letter-spacing: .12em; text-transform: uppercase; color: var(--dim); margin-right: 8px; }
.toolkit .p { font-size: .88rem; font-weight: 500; padding: 7px 14px; border-radius: 999px; background: var(--card); border: 1px solid rgba(20,23,31,.08); }
.dev { display: inline-block; margin-left: 6px; font: 600 .6rem/1 var(--body); letter-spacing: .08em; text-transform: uppercase; color: var(--gold-deep); border: 1px solid var(--gold-line); border-radius: 999px; padding: 3px 6px; vertical-align: 1px; }
@media (max-width: 1000px) { .eco { grid-template-columns: repeat(2, 1fr); } }

/* method */
.steps { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.step { display: flex; flex-direction: column; gap: 12px; padding: 28px; color: var(--text); min-width: 0; }
.step .n { font: 600 .72rem var(--body); letter-spacing: .14em; text-transform: uppercase; color: var(--navy); }
.step .ask { align-self: flex-start; font: 400 .8rem var(--mono); color: var(--text); background: #F6F4EF; border: 1px solid var(--line); border-radius: 999px; padding: 5px 12px; }
.step h3 { font-size: 1.6rem; }
.step p { color: var(--muted); }
.step ul { margin: 2px 0 0; padding-left: 18px; color: var(--muted); display: grid; gap: 6px; }
.step .out { margin-top: auto; padding-top: 14px; border-top: 1px solid var(--line); font-size: .92rem; color: var(--text); }
.step .out b { color: var(--gold-deep); font-weight: 600; }
.outcomes-head { margin: clamp(48px, 6vw, 72px) 0 18px; font: 600 .76rem var(--body); letter-spacing: .14em; text-transform: uppercase; color: var(--on-dark-dim); }
.outcomes { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; }
.outcomes > div { padding: 24px; color: var(--text); min-width: 0; }
.outcomes .index { font: 600 .7rem var(--body); letter-spacing: .12em; text-transform: uppercase; color: var(--navy); }
.outcomes h3 { margin-top: 14px; font-size: 1.2rem; }
.outcomes p { margin-top: 8px; color: var(--muted); font-size: .95rem; }
.dark .card { box-shadow: 0 34px 70px -40px rgba(0,0,0,.75); border-color: rgba(255,255,255,.15); }
@media (max-width: 960px) { .steps { grid-template-columns: 1fr; } .outcomes { grid-template-columns: 1fr 1fr; } }
@media (max-width: 560px) { .outcomes { grid-template-columns: 1fr; } }

/* faq */
.faq-grid { display: grid; grid-template-columns: 1fr 1.4fr; gap: 24px 64px; align-items: start; }
.faq-grid > * { min-width: 0; }
.faq-grid .intro h2 { margin-top: 16px; }
.faq-grid .intro p { margin-top: 18px; color: var(--muted); max-width: 26rem; }
.faq { padding: 6px 30px; }
.faq details { border-bottom: 1px solid var(--line); }
.faq details:last-child { border-bottom: 0; }
.faq summary { list-style: none; cursor: pointer; display: flex; justify-content: space-between; align-items: center; gap: 20px; padding: 22px 0; font: 700 1.12rem/1.3 var(--display); letter-spacing: -0.015em; }
.faq summary::-webkit-details-marker { display: none; }
.faq summary::after { content: "+"; flex: none; width: 30px; height: 30px; border-radius: 50%; display: grid; place-items: center; background: #F6EEDC; color: var(--gold-deep); font: 500 1.1rem var(--body); transition: transform .2s ease; }
.faq details[open] summary::after { transform: rotate(45deg); }
.faq .a { padding: 0 0 22px; color: var(--muted); display: grid; gap: 10px; }
.faq .a a { color: var(--gold-deep); }
@media (max-width: 860px) { .faq-grid { grid-template-columns: 1fr; } .faq { padding: 4px 22px; } }

/* contact */
.contact h2 { font-size: clamp(3.6rem, 12vw, 10rem); line-height: .9; letter-spacing: -0.055em; margin-top: 18px; }
.contact-row { display: grid; grid-template-columns: 1fr 1fr; gap: 32px 64px; align-items: end; margin-top: clamp(32px, 5vw, 56px); }
.contact-row > * { min-width: 0; }
.contact-copy > p { color: var(--on-dark-muted); font-size: 1.1rem; max-width: 30rem; }
.person { display: flex; align-items: center; gap: 16px; margin-top: 28px; }
.portrait { flex: none; width: 72px; height: 72px; border-radius: 50%; object-fit: cover; border: 2px solid var(--gold); box-shadow: 0 12px 32px -12px rgba(226,176,74,.7); }
.person div b { display: block; font: 700 1.08rem var(--display); color: #FFFFFF; letter-spacing: -0.01em; }
.person div span { display: block; font-size: .88rem; color: var(--on-dark-muted); }
.contact-actions { display: grid; gap: 16px; justify-items: start; }
.email { display: flex; flex-wrap: wrap; align-items: center; gap: 14px; padding-bottom: 10px; border-bottom: 2px solid var(--gold); }
.email a { color: #FFFFFF; text-decoration: none; font: 700 clamp(1.25rem, 2.6vw, 1.9rem) var(--display); letter-spacing: -0.02em; overflow-wrap: anywhere; }
.email button { font: 600 .78rem var(--body); color: var(--gold); background: none; border: 1px solid var(--gold); border-radius: 999px; padding: 6px 14px; cursor: pointer; }
@media (max-width: 820px) { .contact-row { grid-template-columns: 1fr; } }

/* footer */
.site-footer { background: var(--ink-2); color: #9AA2B1; font-size: .85rem; }
.site-footer .wrap { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 14px 28px; padding-block: 30px; }
.site-footer .legal { display: flex; flex-wrap: wrap; align-items: center; gap: 6px 18px; }
.site-footer .foot-logo { height: 24px; width: auto; margin-right: 6px; }
.site-footer a { color: #D9DDE4; }
.site-footer .mono { font-family: var(--mono); color: #7F8796; }

.to-top { position: fixed; z-index: 15; right: calc(20px + env(safe-area-inset-right, 0px)); bottom: calc(20px + env(safe-area-inset-bottom, 0px)); width: 48px; height: 48px; border-radius: 50%; display: grid; place-items: center; background: var(--gold); color: #14171F; box-shadow: 0 10px 28px -8px rgba(226,176,74,.75); opacity: 0; pointer-events: none; transition: opacity .25s ease; }
.to-top.show { opacity: 1; pointer-events: auto; }
.to-top svg { width: 18px; height: 18px; stroke: currentColor; }
'''

JS = r'''
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var header = document.querySelector('.site-header');
  var toTop = document.querySelector('.to-top');
  function onScroll() {
    var y = window.scrollY || 0;
    header.classList.toggle('scrolled', y > 24);
    toTop.classList.toggle('show', y > 900);
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  var menuBtn = document.getElementById('menu-btn');
  menuBtn.addEventListener('click', function () {
    var open = header.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.querySelectorAll('#mobile-panel a').forEach(function (a) {
    a.addEventListener('click', function () { header.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); });
  });

  /* Opening background: scattered data points settle into ordered, classified rows */
  (function () {
    var cv = document.getElementById('field');
    if (!cv || !cv.getContext) return;
    var ctx = cv.getContext('2d'), pts = [], W = 0, H = 0;
    function rnd(seed) { var x = Math.sin(seed * 9301 + 49297) * 233280; return x - Math.floor(x); }
    function build() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = cv.clientWidth; H = cv.clientHeight;
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      pts = [];
      var gap = Math.max(16, Math.min(24, W / 64));
      var rows = Math.floor((H - 60) / gap), cols = Math.floor(W / gap), top = (H - (rows - 1) * gap) / 2, n = 0;
      for (var c = 0; c < cols; c++) for (var r = 0; r < rows; r++) {
        n++;
        var gx = c * gap + gap / 2, gy = top + r * gap, kind = rnd(n * 3.1);
        pts.push({ gx: gx, gy: gy, rx: gx + (rnd(n) - 0.5) * gap * 9, ry: rnd(n * 7.7) * H, ph: rnd(n * 1.3) * 6.28,
                   sp: 0.4 + rnd(n * 5.1) * 0.8, sig: (r % 5 === 1 && kind > 0.35), dim: kind < 0.12, b: rnd(n * 2.7) < 0.5 ? 0 : 1 });
      }
    }
    function ease(t) { t = Math.max(0, Math.min(1, t)); return t * t * (3 - 2 * t); }
    function draw(time) {
      ctx.clearRect(0, 0, W, H);
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; var lastFs = 0;
      var t = time / 1000;
      for (var i = 0; i < pts.length; i++) {
        var p = pts[i], k = ease((p.gx / W - 0.42) / 0.36), wob = (1 - k) * 10;
        var x = p.rx + (p.gx - p.rx) * k + Math.sin(t * p.sp + p.ph) * wob;
        var y = p.ry + (p.gy - p.ry) * k + Math.cos(t * p.sp * 0.8 + p.ph) * wob;
        var r = 1.1 + k * 1.1;
        if (p.sig && k > 0.6) { ctx.fillStyle = 'rgba(236,190,96,' + (0.35 + k * 0.65) + ')'; r += 0.6; }
        else if (p.dim && k > 0.6) ctx.fillStyle = 'rgba(255,255,255,0.10)';
        else ctx.fillStyle = 'rgba(255,255,255,' + (0.16 + k * 0.46) + ')';
        var bit = k < 0.6 ? (p.b + Math.floor(t * p.sp * 0.7 + p.ph)) % 2 : p.b;
        var fs = Math.round(8 + r * 3.4);
        if (fs !== lastFs) { ctx.font = '500 ' + fs + 'px "IBM Plex Mono", ui-monospace, monospace'; lastFs = fs; }
        if (p.sig && k > 0.6) { ctx.shadowColor = ctx.fillStyle; ctx.shadowBlur = 8; ctx.fillText(bit, x, y); ctx.shadowBlur = 0; }
        else ctx.fillText(bit, x, y);
      }
    }
    var running = false;
    function loop(ts) { draw(ts); if (running) requestAnimationFrame(loop); }
    build(); draw(0);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { draw(performance.now()); });
    if (!reduce && 'IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        var vis = es[0].isIntersecting;
        if (vis && !running) { running = true; requestAnimationFrame(loop); } else if (!vis) running = false;
      }).observe(cv);
    }
    var rt; window.addEventListener('resize', function () { clearTimeout(rt); rt = setTimeout(function () { build(); draw(performance.now()); }, 120); });
  })();

  /* Services index follows the card in view */
  var links = Array.prototype.slice.call(document.querySelectorAll('#svc-index a'));
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) links.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === '#' + e.target.id); });
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    document.querySelectorAll('.svc').forEach(function (s) { io.observe(s); });
  }

  /* Copy email */
  var copyBtn = document.getElementById('copy-email');
  copyBtn.addEventListener('click', function () {
    var el = document.getElementById('email');
    function selectIt() { var r = document.createRange(); r.selectNodeContents(el); var s = getSelection(); s.removeAllRanges(); s.addRange(r); copyBtn.textContent = 'Selected'; }
    try { navigator.clipboard.writeText(el.textContent).then(function () { copyBtn.textContent = 'Copied'; }, selectIt); } catch (e) { selectIt(); }
    setTimeout(function () { copyBtn.textContent = 'Copy'; }, 1800);
  });
})();
'''

# content blocks: give them the card surface
challenges = challenges.replace('<a class="challenge"', '<a class="challenge card"')
sv_cards = sv_cards.replace('<article class="svc"', '<article class="svc card"')
sv_cards = re.sub(r'(<img class="art photo"[^>]*>)', r'<span class="art-tile">\1</span>', sv_cards)
sectors = sectors.replace('<article class="sector">', '<article class="sector card">')
eco = eco.replace('<div class="eco-item">', '<div class="eco-item card">')
steps = steps.replace('<article class="step">', '<article class="step card">')
outcomes = outcomes.replace('<div>', '<div class="card">')
toolkit = toolkit.strip()

page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>DataiTECH · Data and AI: Now it makes sense!</title>
<meta name="claude:viewport-fit-sides" content="cover">
{meta}
{jsonld}
<!--FONTS-->
<style>
/*FONTFACE*/
{FONTFACE}{CSS}
</style>
</head>
<body>

<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="#top" aria-label="DataiTECH home"><img src="images/logo-on-dark.png" alt="DataiTECH" width="504" height="120"></a>
    <nav class="nav-links" aria-label="Main">
{nav_links}
        <a class="btn gold" href="#contact">Contact {ARROW}</a>
    </nav>
    <button class="menu-btn" type="button" id="menu-btn" aria-expanded="false" aria-controls="mobile-panel">Menu <span class="bars" aria-hidden="true"></span></button>
  </div>
  <nav class="wrap mobile-panel" id="mobile-panel" aria-label="Mobile">
{nav_mobile}
  </nav>
</header>

<main id="top">

  <section class="hero dark" aria-labelledby="hero-title">
    <canvas id="field" aria-hidden="true"></canvas>
    <div class="wrap">
      <p class="eyebrow">Infrastructure &amp; data protection · Zoetermeer</p>
      <h1 id="hero-title"><span class="line">Data and AI<span class="pd">.</span></span><br><span class="line">Now it <span class="gold">makes sense</span><span class="pd gold">.</span></span></h1>
      <p class="hero-lead">{hero_lead}</p>
      <div class="hero-ctas">
        <a class="btn gold" href="#first-engagement">Request the assessment {ARROW}</a>
        <a class="btn" href="#challenges">When to call us {ARROW}</a>
      </div>
      <ul class="assure" aria-label="What you can count on">
        <li>Fixed scope, fixed price</li>
        <li>Success agreed upfront</li>
        <li>Tested recovery, with evidence</li>
      </ul>
    </div>
  </section>

  <section class="statement" aria-label="Our conviction">
    <div class="wrap">
      <p>No data, no business<span class="pd">.</span><br>No protection, no data<span class="pd">.</span><br>We turn <span class="soft">raw data</span> into <span class="gold">decisions you can&nbsp;trust</span><span class="pd">.</span></p>
    </div>
  </section>

  <section class="band" id="challenges">
    <div class="wrap">
      <div class="head">
        <div><p class="eyebrow">Challenges we solve</p><h2>{ch_h2}</h2></div>
        <p>{ch_p}</p>
      </div>
      <div class="challenges">
{challenges}
      </div>
    </div>
  </section>

  <section class="band dark" id="first-engagement">
    <div class="wrap">
      <div class="offer">
        <div>
          <p class="eyebrow">Your first engagement</p>
          <h2>{of_h2}</h2>
          <p class="offer-lede">{of_lede}</p>
          <a class="btn gold" href="#contact">Request the assessment {ARROW}</a>
        </div>
        <dl class="facts">
{of_facts}
        </dl>
      </div>
    </div>
  </section>

  <section class="band" id="services">
    <div class="wrap">
      <div class="head">
        <div><p class="eyebrow">What we do</p><h2>{sv_h2}</h2></div>
        <p>{sv_p}</p>
      </div>
      <div class="services">
        <ul class="svc-index" id="svc-index">
{sv_index}
        </ul>
        <div class="svc-cards">
{sv_cards}
        </div>
      </div>
    </div>
  </section>

  <section class="band" id="sectors">
    <div class="wrap">
      <div class="head">
        <div><p class="eyebrow">Sectors we serve</p><h2>{se_h2}</h2></div>
        <p>{se_p}</p>
      </div>
      <div class="sectors">
{sectors}
      </div>
    </div>
  </section>

  <section class="band" id="technology">
    <div class="wrap">
      <div class="head">
        <div><p class="eyebrow">Platforms</p><h2>{te_h2}</h2></div>
        <p>{te_p}</p>
      </div>
      <div class="eco" aria-label="Core technology ecosystem">
{eco}
      </div>
      <div class="toolkit" aria-label="Also in our toolkit">
        <span class="lbl">Also in our toolkit</span>
        {toolkit}
      </div>
    </div>
  </section>

  <section class="band dark" id="how-we-work">
    <div class="wrap">
      <div class="head">
        <div><p class="eyebrow">Our method</p><h2>{hw_h2}</h2></div>
        <p>{hw_p}</p>
      </div>
      <div class="steps">
{steps}
      </div>
      <h3 class="outcomes-head">What every client can count on</h3>
      <div class="outcomes">
{outcomes}
      </div>
    </div>
  </section>

  <section class="band" id="faq">
    <div class="wrap faq-grid">
      <div class="intro"><p class="eyebrow">Helpful answers</p><h2>{fq_h2}</h2><p>{fq_p}</p></div>
      <div class="faq card">
{faq}
      </div>
    </div>
  </section>

  <section class="band dark contact" id="contact">
    <div class="wrap">
      <p class="eyebrow">Let's work together</p>
      <h2>Let's talk<span class="hl">.</span></h2>
      <div class="contact-row">
        <div class="contact-copy">
          <p>{contact_p}</p>
          <div class="person"><img class="portrait" src="images/frenck-gyamfi.webp" alt="Frenck F.N Gyamfi" width="480" height="480" loading="lazy" decoding="async"><div><b>Frenck F.N Gyamfi</b><span>Data Informatics &amp; Technologies B.V. · Zoetermeer</span></div></div>
        </div>
        <div class="contact-actions">
          <div class="email"><a id="email" href="mailto:enquiries@dataitechbv.com">enquiries@dataitechbv.com</a><button type="button" id="copy-email">Copy</button></div>
          <a class="btn" href="https://www.linkedin.com/" target="_blank" rel="noopener">Connect on LinkedIn {ARROW}</a>
        </div>
      </div>
    </div>
  </section>

</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="legal">
{footer_legal}
    </div>
    <span class="mono">No data, no business.</span>
  </div>
</footer>

<a class="to-top" href="#top" aria-label="Back to top"><svg viewBox="0 0 18 18" fill="none" stroke-width="2"><path d="M9 15V3M4 8l5-5 5 5"/></svg></a>

<script>{JS}</script>
</body>
</html>
'''
open(dst, 'w').write(page)
print('built', dst, len(page))
