import math, random
C, S_ = math.cos(math.radians(30)), 0.5
W, H = 320, 240

def fmt(v): return ('%.1f' % v).rstrip('0').rstrip('.')
def pts(ps): return ' '.join('%s,%s' % (fmt(x), fmt(y)) for x, y in ps)

class Scene:
    def __init__(self, sid, ox=160, oy=120):
        self.sid, self.ox, self.oy, self.out, self.defs = sid, ox, oy, [], []
        self.defs.append(f'<filter id="{sid}b" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="7"/></filter>')
        for name, a, b in [('w', '--iso-left', '--iso-right'), ('g', '--iso-gleft', '--iso-gright')]:
            self.defs.append(f'<linearGradient id="{sid}{name}" x1="0" x2="1" y1="0" y2="0"><stop offset="0" style="stop-color:var(--iso-top)"/><stop offset=".45" style="stop-color:var({a})"/><stop offset="1" style="stop-color:var({b})"/></linearGradient>' if name == 'w' else
                             f'<linearGradient id="{sid}{name}" x1="0" x2="1" y1="0" y2="0"><stop offset="0" style="stop-color:var(--iso-gtop)"/><stop offset=".45" style="stop-color:var({a})"/><stop offset="1" style="stop-color:var({b})"/></linearGradient>')
        self.defs.append(f'<linearGradient id="{sid}f" x1="0" x2="1" y1="0" y2="1"><stop offset="0" style="stop-color:var(--iso-gtop)"/><stop offset="1" style="stop-color:var(--iso-gleft)"/></linearGradient>')
    def P(self, x, y, z): return (self.ox + (x - y) * C, self.oy + (x + y) * S_ - z)
    def poly(self, ps, fill, edge='var(--iso-edge)', extra=''):
        self.out.append(f'<polygon points="{pts(ps)}" style="fill:{fill};stroke:{edge}" {extra}/>')
    def raw(self, s): self.out.append(s)
    def shadow(self, ps, op=1):
        self.out.append(f'<polygon points="{pts(ps)}" style="fill:var(--iso-shadow);opacity:var(--iso-shadow-o)" filter="url(#{self.sid}b)"/>')
    def box_shadow(self, x0, y0, x1, y1, z0=0, grow=6):
        P = self.P
        ps = [P(x0, y0, z0), P(x1 + grow, y0, z0), P(x1 + grow * 1.6, y1 + grow * 1.6, z0), P(x0, y1 + grow, z0)]
        self.shadow([(x + 5, y + 4) for x, y in ps])
    def box(self, x0, y0, z0, x1, y1, z1, gold=None):
        gold = gold or ()
        P = self.P
        f = lambda face, base: ('var(--iso-g%s)' % base if face in gold else 'var(--iso-%s)' % base)
        e = lambda face: 'var(--iso-gedge)' if face in gold else 'var(--iso-edge)'
        self.poly([P(x1, y0, z1), P(x1, y1, z1), P(x1, y1, z0), P(x1, y0, z0)], f('right', 'right'), e('right'))
        self.poly([P(x0, y1, z1), P(x1, y1, z1), P(x1, y1, z0), P(x0, y1, z0)], f('left', 'left'), e('left'))
        self.poly([P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)], f('top', 'top'), e('top'))
    def line3(self, a, b, style='stroke:var(--iso-detail);stroke-width:1.2', extra=''):
        (x1, y1), (x2, y2) = self.P(*a), self.P(*b)
        self.out.append(f'<line x1="{fmt(x1)}" y1="{fmt(y1)}" x2="{fmt(x2)}" y2="{fmt(y2)}" style="{style};stroke-linecap:round" {extra}/>')
    def dot3(self, p, r=2.2, fill='var(--iso-dot)'):
        x, y = self.P(*p); self.out.append(f'<circle cx="{fmt(x)}" cy="{fmt(y)}" r="{r}" style="fill:{fill}"/>')
    def cyl(self, cx, cy, r, z0, z1, gold_top=False, gold_side=False, edge=None):
        X, Yt = self.P(cx, cy, z1); _, Yb = self.P(cx, cy, z0)
        rx, ry = r * math.sqrt(2) * C, r * math.sqrt(2) * S_
        side = f'url(#{self.sid}{"g" if gold_side else "w"})'
        ed = edge or ('var(--iso-gedge)' if gold_side else 'var(--iso-edge)')
        self.out.append(f'<path d="M{fmt(X-rx)} {fmt(Yt)}V{fmt(Yb)}A{fmt(rx)} {fmt(ry)} 0 0 0 {fmt(X+rx)} {fmt(Yb)}V{fmt(Yt)}Z" style="fill:{side};stroke:{ed}"/>')
        top = 'var(--iso-gtop)' if gold_top else 'var(--iso-top)'
        te = 'var(--iso-gedge)' if gold_top else ed
        self.out.append(f'<ellipse cx="{fmt(X)}" cy="{fmt(Yt)}" rx="{fmt(rx)}" ry="{fmt(ry)}" style="fill:{top};stroke:{te}"/>')
        return X, Yt, Yb, rx, ry
    def grid(self):
        g = []
        k = math.tan(math.radians(30))
        for c in range(-300, 560, 26):
            g.append(f'M0 {c}L{W} {fmt(c + W * k)}'); g.append(f'M0 {c}L{W} {fmt(c - W * k)}')
        self.out.insert(0, f'<path d="{"".join(g)}" style="fill:none;stroke:var(--iso-grid);stroke-width:1"/>')
    def svg(self, label):
        self.grid()
        return (f'<svg class="art iso" viewBox="0 0 {W} {H}" role="img" aria-label="{label}"><defs>{"".join(self.defs)}</defs>'
                f'<g style="stroke-linejoin:round;stroke-width:1">{"".join(self.out)}</g></svg>')

def extrude(sc, d, fill_front, steps=9, dx=1.1, dy=0.65, side='var(--iso-right)', edge='var(--iso-edge)', front_edge='var(--iso-gedge)'):
    for i in range(steps, 0, -1):
        sc.raw(f'<path d="{d}" transform="translate({fmt(i*dx)} {fmt(i*dy)})" style="fill:{side};stroke:{edge if i==steps else "none"}"/>')
    sc.raw(f'<path d="{d}" style="fill:{fill_front};stroke:{front_edge}"/>')

arts = {}

# 1 ---- Storage: stacked discs with a gold cap
s = Scene('i1', 160, 168)
rr = 64; rx, ry = rr * math.sqrt(2) * C, rr * math.sqrt(2) * S_
X0, Y0 = s.P(0, 0, 0)
s.raw(f'<ellipse cx="{fmt(X0+10)}" cy="{fmt(Y0+12)}" rx="{fmt(rx+6)}" ry="{fmt(ry+4)}" style="fill:var(--iso-shadow);opacity:var(--iso-shadow-o)" filter="url(#i1b)"/>')
for i in range(4):
    z0 = i * 25; z1 = z0 + 21
    X, Yt, Yb, _, _ = s.cyl(0, 0, rr, z0, z1, edge='var(--iso-gedge)')
    py = (Yt + Yb) / 2 + ry - 6
    s.raw(f'<rect x="{fmt(X-34)}" y="{fmt(py-6)}" width="30" height="12" rx="2.5" style="fill:none;stroke:var(--iso-gedge)"/>')
    for j in range(3): s.raw(f'<circle cx="{fmt(X-29+j*4.5)}" cy="{fmt(py-1.5)}" r="1" style="fill:var(--iso-gedge)"/><circle cx="{fmt(X-29+j*4.5)}" cy="{fmt(py+2.5)}" r="1" style="fill:var(--iso-gedge)"/>')
    s.raw(f'<circle cx="{fmt(X-11)}" cy="{fmt(py)}" r="3.2" style="fill:var(--iso-gleft);stroke:var(--iso-gedge)"/>')
    s.raw(f'<circle cx="{fmt(X+rx-12)}" cy="{fmt(py-8)}" r="1.8" style="fill:var(--iso-dot)"/>')
X, Yt, _, _, _ = s.cyl(0, 0, rr, 100, 106, gold_top=True, gold_side=True)
s.raw(f'<ellipse cx="{fmt(X)}" cy="{fmt(Yt)}" rx="{fmt(rx*0.78)}" ry="{fmt(ry*0.78)}" style="fill:none;stroke:var(--iso-gright);stroke-width:.8"/>')
s.raw(f'<ellipse cx="{fmt(X)}" cy="{fmt(Yt+3)}" rx="17" ry="9.8" style="fill:var(--iso-gright)"/><ellipse cx="{fmt(X)}" cy="{fmt(Yt)}" rx="17" ry="9.8" style="fill:var(--iso-gleft);stroke:var(--iso-gedge)"/><ellipse cx="{fmt(X)}" cy="{fmt(Yt-2)}" rx="9" ry="5.2" style="fill:var(--iso-gtop)"/>')
arts['storage'] = s.svg('Isometric stack of storage discs with a gold top')

# 2 ---- Backup: gold shield with 3-2-1 copies on an orbit
s = Scene('i2', 160, 120)
s.raw('<ellipse cx="160" cy="168" rx="128" ry="42" style="fill:none;stroke:var(--iso-gedge);stroke-dasharray:3 5;opacity:.8"/>')
s.raw('<ellipse cx="168" cy="196" rx="52" ry="12" style="fill:var(--iso-shadow);opacity:var(--iso-shadow-o)" filter="url(#i2b)"/>')
for (cx, cy, gold) in [(50, 136, False), (268, 128, False)]:
    s.ox, s.oy = cx, cy
    s.box_shadow(-14, -14, 14, 14)
    s.box(-14, -14, 0, 14, 14, 9); s.box(-14, -14, 11, 14, 14, 20, gold=('top',) if gold else ())
    s.dot3((14, 4, 15), 1.6); s.dot3((14, 4, 4.5), 1.6, 'var(--iso-detail)')
s.ox, s.oy = 236, 206
s.box_shadow(-14, -14, 14, 14)
s.box(-14, -14, 0, 14, 14, 9, gold=('top', 'left', 'right')); s.box(-14, -14, 11, 14, 14, 20, gold=('top', 'left', 'right'))
shield = 'M160 30 L210 48 V96 C210 134 190 157 160 172 C130 157 110 134 110 96 V48 Z'
extrude(s, shield, f'url(#i2f)', steps=10, side='var(--iso-gright)', edge='var(--iso-gedge)')
s.raw('<path d="M160 43 L199 57 V96 C199 127 183 146 160 158 C137 146 121 127 121 96 V57 Z" style="fill:none;stroke:var(--iso-gedge);stroke-width:1.2"/>')
s.raw('<path d="M160 43 V158 C137 146 121 127 121 96 V57 Z" style="fill:var(--iso-gleft);opacity:.35"/>')
s.raw('<path d="M139 101 L154 116 L183 85" style="fill:none;stroke:var(--iso-gink);stroke-width:7;stroke-linecap:round;stroke-linejoin:round"/>')
s.raw('<circle cx="32" cy="168" r="2.6" style="fill:var(--iso-dot)"/><circle cx="288" cy="168" r="2.6" style="fill:var(--iso-dot)"/>')
arts['backup'] = s.svg('Gold shield surrounded by three backup copies, one of them off-site')

# 3 ---- Virtualisation & hybrid cloud: server stack and a floating cloud
s = Scene('i3', 104, 112)
s.box_shadow(-12, -12, 92, 92, -8, 10)
s.box(-12, -12, -8, 92, 92, 0)
for i, (z0, z1) in enumerate([(0, 26), (30, 56), (60, 86)]):
    s.box(0, 0, z0, 80, 80, z1, gold=('top',) if i == 2 else ())
    for k in range(4): s.line3((8, 80, z1 - 7 - k * 3.6), (36, 80, z1 - 7 - k * 3.6))
    for k in range(3): s.dot3((52 + k * 7, 80, z1 - 12), 1.7, 'var(--iso-gedge)' if k else 'var(--iso-dot)')
    for k in range(2): s.line3((80, 14, z1 - 9 - k * 6), (80, 62, z1 - 9 - k * 6), 'stroke:var(--iso-detail);stroke-width:1.2')
cx, cy = s.P(40, 40, 86)
s.raw(f'<path d="M{fmt(cx)} {fmt(cy)}V22H226V58" style="fill:none;stroke:var(--iso-gedge);stroke-dasharray:3 4"/>')
s.raw(f'<circle cx="{fmt(cx)}" cy="{fmt(cy)}" r="3" style="fill:var(--iso-dot)"/>')
cloud = 'M196 112 C178 112 172 92 186 84 C184 66 206 58 218 68 C224 50 254 48 262 68 C278 64 292 78 286 92 C298 96 296 112 282 112 Z'
s.raw('<ellipse cx="248" cy="142" rx="50" ry="8" style="fill:var(--iso-shadow);opacity:var(--iso-shadow-o)" filter="url(#i3b)"/>')
extrude(s, cloud, 'var(--iso-top)', steps=11, side='var(--iso-gleft)', edge='var(--iso-gedge)')
s.raw('<path d="M188 104 C200 108 270 108 288 104" style="fill:none;stroke:var(--iso-gedge);opacity:.6"/>')
s.raw('<circle cx="226" cy="58" r="3" style="fill:var(--iso-dot)"/>')
arts['virt'] = s.svg('Isometric server stack connected to a cloud')

# 4 ---- Kubernetes: hexagonal prisms on a round platform
s = Scene('i4', 160, 136)
pr = 88; prx, pry = pr * math.sqrt(2) * C, pr * math.sqrt(2) * S_
X0, Y0 = s.P(0, 0, -16)
s.raw(f'<ellipse cx="{fmt(X0+10)}" cy="{fmt(Y0+12)}" rx="{fmt(prx)}" ry="{fmt(pry)}" style="fill:var(--iso-shadow);opacity:var(--iso-shadow-o)" filter="url(#i4b)"/>')
s.cyl(0, 0, pr, -16, -8)
s.cyl(0, 0, pr - 8, -8, 0)
R = 14.5
cells = []
for q in range(-4, 5):
    for r in range(-4, 5):
        x = math.sqrt(3) * R * (q + r / 2); y = 1.5 * R * r
        if math.hypot(x, y) <= 58: cells.append((x, y))
cells.sort(key=lambda c: (c[0] + c[1], c[0]))
gold_idx = {2, 7, 11, 15}
for i, (hx, hy) in enumerate(cells):
    g = i in gold_idx
    h = 20 if g else 13
    vs = [(hx + R * math.cos(math.radians(30 + 60 * k)), hy + R * math.sin(math.radians(30 + 60 * k))) for k in range(6)]
    for k in range(6):
        a, b = vs[k], vs[(k + 1) % 6]
        nx = math.cos(math.radians(60 + 60 * k)); ny = math.sin(math.radians(60 + 60 * k))
        if nx + ny <= 0.01: continue
        shade = 'left' if ny > nx else 'right'
        s.poly([s.P(a[0], a[1], h), s.P(b[0], b[1], h), s.P(b[0], b[1], 0), s.P(a[0], a[1], 0)],
               'var(--iso-g%s)' % shade if g else 'var(--iso-%s)' % shade, 'var(--iso-gedge)' if g else 'var(--iso-edge)')
    s.poly([s.P(vx, vy, h) for vx, vy in vs], 'var(--iso-gtop)' if g else 'var(--iso-top)', 'var(--iso-gedge)' if g else 'var(--iso-edge)')
    inner = [s.P(hx + (vx - hx) * .55, hy + (vy - hy) * .55, h) for vx, vy in vs]
    s.raw(f'<polygon points="{pts(inner)}" style="fill:none;stroke:{"var(--iso-gedge)" if g else "var(--iso-edge)"};opacity:.7"/>')
s.ox, s.oy = 282, 52
hexs = [(282 + 15 * math.cos(math.radians(30 + 60 * k)), 52 + 15 * math.sin(math.radians(30 + 60 * k))) for k in range(6)]
s.raw(f'<polygon points="{pts(hexs)}" style="fill:none;stroke:var(--iso-edge)"/>')
hexs2 = [(282 + 7 * math.cos(math.radians(30 + 60 * k)), 52 + 7 * math.sin(math.radians(30 + 60 * k))) for k in range(6)]
s.raw(f'<polygon points="{pts(hexs2)}" style="fill:var(--iso-gtop);stroke:var(--iso-gedge)"/><path d="M282 67V96" style="stroke:var(--iso-gedge);stroke-dasharray:2 3"/><circle cx="282" cy="99" r="2.4" style="fill:var(--iso-dot)"/>')
arts['k8s'] = s.svg('Isometric cluster of hexagonal container blocks, some highlighted in gold')

# 5 ---- Data classification: funnel to three validated slabs
s = Scene('i5', 92, 196)
random.seed(4)
for _ in range(46):
    t = random.random()
    yy = 12 + t * 52
    spread = 72 - t * 10
    xx = 92 + (random.random() - .5) * 2 * spread
    col = 'var(--iso-dot)' if random.random() < .35 else 'var(--iso-detail)'
    s.raw(f'<circle cx="{fmt(xx)}" cy="{fmt(yy)}" r="{fmt(1.4 + random.random() * 1.1)}" style="fill:{col}"/>')
s.box_shadow(-16, -16, 16, 16)
s.box(-16, -16, 0, 16, 16, 8)
s.raw(f'<path d="M30 82 L86 184 L98 184 L154 82 A62 18 0 0 1 30 82Z" style="fill:url(#i5w);stroke:var(--iso-edge)"/>')
s.raw('<ellipse cx="92" cy="82" rx="62" ry="18" style="fill:var(--iso-left);stroke:var(--iso-gedge);stroke-width:1.3"/>')
s.raw('<path d="M48 90 L88 176 M136 90 L96 176" style="stroke:var(--iso-gedge);stroke-width:.8;opacity:.8"/>')
for _ in range(26):
    yy = 80 + random.random() * 90; w = 56 * (1 - (yy - 80) / 104)
    s.raw(f'<circle cx="{fmt(92 + (random.random() - .5) * 2 * w * .8)}" cy="{fmt(yy)}" r="1.3" style="fill:{"var(--iso-dot)" if random.random() < .4 else "var(--iso-detail)"}"/>')
s.raw('<path d="M100 140 H150 M150 140 V78 H178 M150 140 H178 M150 140 V202 H178" style="fill:none;stroke:var(--iso-edge);stroke-width:1.2"/><circle cx="128" cy="140" r="3" style="fill:var(--iso-dot)"/>')
for i, (lab, icon) in enumerate([('STRUCTURED', 'db'), ('VALIDATED', 'ok'), ('AI-READY', 'net')]):
    y = 62 + i * 62
    s.raw(f'<path d="M178 {y} l8 -6 h120 l-8 6z" style="fill:var(--iso-top);stroke:var(--iso-edge)"/><path d="M298 {y} l8 -6 v30 l-8 6z" style="fill:var(--iso-right);stroke:var(--iso-edge)"/>')
    s.raw(f'<rect x="178" y="{y}" width="120" height="30" style="fill:var(--iso-left);stroke:var(--iso-edge)"/>')
    s.raw(f'<circle cx="194" cy="{y+15}" r="8" style="fill:none;stroke:var(--iso-detail)"/>')
    if icon == 'db': s.raw(f'<ellipse cx="194" cy="{y+11}" rx="4" ry="1.6" style="fill:none;stroke:var(--iso-ink)"/><path d="M190 {y+11}v7c0 2 8 2 8 0v-7" style="fill:none;stroke:var(--iso-ink)"/>')
    if icon == 'ok': s.raw(f'<path d="M190.5 {y+15}l2.5 2.5 4.5-5" style="fill:none;stroke:var(--iso-ink);stroke-width:1.3"/>')
    if icon == 'net': s.raw(f'<circle cx="191" cy="{y+17}" r="1.5" style="fill:var(--iso-ink)"/><circle cx="197" cy="{y+12}" r="1.5" style="fill:var(--iso-ink)"/><circle cx="197" cy="{y+19}" r="1.5" style="fill:var(--iso-ink)"/><path d="M191 {y+17}L197 {y+12}M191 {y+17}L197 {y+19}" style="stroke:var(--iso-ink)"/>')
    s.raw(f'<text x="208" y="{y+17}" style="font:500 7.4px var(--font-mono);letter-spacing:.05em;fill:var(--iso-ink)">{lab}</text>')
    s.raw(f'<rect x="208" y="{y+21}" width="16" height="1.6" style="fill:var(--iso-dot)"/><rect x="288" y="{y+12}" width="4" height="4" style="fill:var(--iso-dot)"/>')
arts['cleanup'] = s.svg('Data dots poured through a funnel into structured, validated and AI-ready outputs')

# 6 ---- Architecture & consultancy: root slab feeding three workstreams
s = Scene('i6', 160, 100)
s.box_shadow(-34, -34, 34, 34, 0, 8)
for a, b in [((22, 22, 0), (40, 40, 0)), ((40, 40, 0), (92, -12, 0)), ((40, 40, 0), (48, 48, 0)), ((40, 40, 0), (-12, 92, 0))]:
    s.line3(a, b, 'stroke:var(--iso-edge);stroke-width:2.2')
for p_ in [(30, 30, 0), (40, 40, 0), (66, 14, 0), (14, 66, 0)]: s.dot3(p_, 2.6)
s.box(-34, -34, 0, 34, 34, 16, gold=('top',))
for (xa, ya, za), (xb, yb, zb) in [((-22, -22, 16), (22, -22, 16)), ((-22, -22, 16), (-22, 22, 16))]:
    pass
t1 = [s.P(-24, -14, 16), s.P(14, -14, 16), s.P(14, -10, 16), s.P(-24, -10, 16)]
t2 = [s.P(-24, -4, 16), s.P(2, -4, 16), s.P(2, 0, 16), s.P(-24, 0, 16)]
s.poly(t1, 'var(--iso-gright)', 'none'); s.poly(t2, 'var(--iso-gleft)', 'none')
for (cx, cy), gold in [((114, -4), False), ((55, 55), True), ((-4, 114), False)]:
    s.box_shadow(cx - 22, cy - 22, cx + 22, cy + 22)
    s.box(cx - 22, cy - 22, 0, cx + 22, cy + 22, 12, gold=('right',) if gold else ())
    s.dot3((cx - 12, cy - 12, 12), 2.2)
    s.line3((cx - 6, cy - 14, 12), (cx + 14, cy - 14, 12), 'stroke:var(--iso-detail);stroke-width:1.4')
    s.line3((cx - 6, cy - 7, 12), (cx + 6, cy - 7, 12), 'stroke:var(--iso-detail);stroke-width:1.4')
arts['management'] = s.svg('Isometric consultancy structure: one strategy layer feeding three workstreams')

import json, sys
json.dump(arts, open(sys.argv[1], 'w'))
print({k: len(v) for k, v in arts.items()})
