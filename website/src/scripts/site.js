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
  if (copyBtn) copyBtn.addEventListener('click', function () {
    var el = document.getElementById('email');
    function selectIt() { var r = document.createRange(); r.selectNodeContents(el); var s = getSelection(); s.removeAllRanges(); s.addRange(r); copyBtn.textContent = 'Selected'; }
    try { navigator.clipboard.writeText(el.textContent).then(function () { copyBtn.textContent = 'Copied'; }, selectIt); } catch (e) { selectIt(); }
    setTimeout(function () { copyBtn.textContent = 'Copy'; }, 1800);
  });
})();
