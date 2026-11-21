(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var header = document.querySelector('.site-header');
  var toTop = document.querySelector('.to-top');
  function onScroll() {
    var y = window.scrollY || 0;
    header.classList.toggle('scrolled', y > 24);
    if (toTop) toTop.classList.toggle('show', y > 900);
  }
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();

  var menuBtn = document.getElementById('menu-btn');
  if (menuBtn) menuBtn.addEventListener('click', function () {
    var open = header.classList.toggle('open');
    menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
  document.querySelectorAll('#mobile-panel a').forEach(function (a) {
    a.addEventListener('click', function () { header.classList.remove('open'); menuBtn.setAttribute('aria-expanded', 'false'); });
  });

  /* Opening background: scattered 1s and 0s settle into ordered, classified rows.
     Performance: each digit is pre-rendered once into a small sprite and copied with drawImage;
     30 frames a second; digits hidden by the fade mask are skipped; pauses when off screen or hidden. */
  (function () {
    var cv = document.getElementById('field');
    if (!cv || !cv.getContext) return;
    var ctx = cv.getContext('2d'), pts = [], W = 0, H = 0, dpr = 1, narrow = false, sprites = {};
    var GOLD = 'rgb(236,190,96)';
    function rnd(seed) { var x = Math.sin(seed * 9301 + 49297) * 233280; return x - Math.floor(x); }
    function sprite(bit, fs, gold) {
      var key = bit + '-' + fs + (gold ? 'g' : 'w');
      if (sprites[key]) return sprites[key];
      var pad = gold ? 10 : 2, size = Math.ceil(fs * 1.4) + pad * 2;
      var c = document.createElement('canvas'); c.width = c.height = Math.ceil(size * dpr);
      var x = c.getContext('2d'); x.scale(dpr, dpr);
      x.font = '500 ' + fs + 'px "IBM Plex Mono", ui-monospace, monospace'; x.textAlign = 'center'; x.textBaseline = 'middle';
      x.fillStyle = gold ? GOLD : '#FFFFFF';
      if (gold) { x.shadowColor = GOLD; x.shadowBlur = 8; }
      x.fillText(String(bit), size / 2, size / 2);
      return (sprites[key] = { c: c, s: size });
    }
    function build() {
      dpr = Math.min(window.devicePixelRatio || 1, 2); sprites = {};
      W = cv.clientWidth; H = cv.clientHeight; narrow = W < 700;
      cv.width = Math.round(W * dpr); cv.height = Math.round(H * dpr);
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      pts = [];
      var gap = narrow ? 22 : Math.max(16, Math.min(24, W / 64));
      var rows = Math.floor((H - 60) / gap), cols = Math.floor(W / gap), top = (H - (rows - 1) * gap) / 2, n = 0;
      for (var c = 0; c < cols; c++) for (var r = 0; r < rows; r++) {
        n++;
        var gx = c * gap + gap / 2, gy = top + r * gap, kind = rnd(n * 3.1);
        var p = { gx: gx, gy: gy, rx: gx + (rnd(n) - 0.5) * gap * 9, ry: rnd(n * 7.7) * H, ph: rnd(n * 1.3) * 6.28,
                  sp: 0.4 + rnd(n * 5.1) * 0.8, sig: (r % 5 === 1 && kind > 0.35), dim: kind < 0.12, b: rnd(n * 2.7) < 0.5 ? 0 : 1 };
        // the CSS mask hides the left part (desktop) or the top part (phones): skip digits that can never show
        if (!narrow && Math.max(p.gx, p.rx) < W * 0.46 - 12) continue;
        if (narrow && Math.max(p.gy, p.ry) < H * 0.55 - 12) continue;
        pts.push(p);
      }
    }
    function ease(t) { t = Math.max(0, Math.min(1, t)); return t * t * (3 - 2 * t); }
    function draw(time) {
      ctx.clearRect(0, 0, W, H);
      var t = time / 1000;
      for (var i = 0; i < pts.length; i++) {
        var p = pts[i], k = ease((p.gx / W - 0.42) / 0.36), wob = (1 - k) * 10;
        var x = p.rx + (p.gx - p.rx) * k + Math.sin(t * p.sp + p.ph) * wob;
        var y = p.ry + (p.gy - p.ry) * k + Math.cos(t * p.sp * 0.8 + p.ph) * wob;
        var r = 1.1 + k * 1.1, gold = p.sig && k > 0.6, a;
        if (gold) { a = 0.35 + k * 0.65; r += 0.6; }
        else if (p.dim && k > 0.6) a = 0.10;
        else a = 0.16 + k * 0.46;
        var bit = k < 0.6 ? (p.b + Math.floor(t * p.sp * 0.7 + p.ph)) % 2 : p.b;
        var sp = sprite(bit, Math.round(8 + r * 3.4), gold);
        ctx.globalAlpha = a;
        ctx.drawImage(sp.c, x - sp.s / 2, y - sp.s / 2, sp.s, sp.s);
      }
      ctx.globalAlpha = 1;
    }
    var running = false, last = 0;
    function loop(ts) {
      if (!running) return;
      if (ts - last >= (narrow ? 48 : 32)) { last = ts; draw(ts); }   // 20 fps on phones, 30 on desktop
      requestAnimationFrame(loop);
    }
    function start() { if (!running && !document.hidden) { running = true; requestAnimationFrame(loop); } }
    requestAnimationFrame(function () { build(); draw(0); });   // measure after the first layout, not during it
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { sprites = {}; if (W) draw(performance.now()); });
    if (!reduce && 'IntersectionObserver' in window) {
      var visible = false;
      new IntersectionObserver(function (es) { visible = es[0].isIntersecting; if (visible) start(); else running = false; }).observe(cv);
      document.addEventListener('visibilitychange', function () { if (document.hidden) running = false; else if (visible) start(); });
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
  if (copyBtn) copyBtn.addEventListener('click', function () {
    var el = document.getElementById('email');
    function selectIt() { var r = document.createRange(); r.selectNodeContents(el); var s = getSelection(); s.removeAllRanges(); s.addRange(r); copyBtn.textContent = 'Selected'; }
    try { navigator.clipboard.writeText(el.textContent).then(function () { copyBtn.textContent = 'Copied'; }, selectIt); } catch (e) { selectIt(); }
    setTimeout(function () { copyBtn.textContent = 'Copy'; }, 1800);
  });
})();
