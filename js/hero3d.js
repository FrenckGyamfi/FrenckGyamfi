/* DataiTECH opening scene (Three.js).
   Loose data blocks drift in, settle into an ordered grid on a storage platform, and a gold
   check emblem lights up: raw data, made orderly and protected.
   Phones and visitors who prefer reduced motion get the finished scene as a still image. */
import * as THREE from './vendor/three.module.min.js';

const host = document.getElementById('hero3d');
const hero = document.querySelector('.hero');

function fail() { if (hero) hero.classList.add('no-3d'); }

try { init(); } catch (e) { fail(); }

function init() {
  if (!host) return;
  const probe = document.createElement('canvas');
  if (!(probe.getContext('webgl2') || probe.getContext('webgl'))) { fail(); return; }

  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const still = reduce || window.matchMedia('(max-width: 700px)').matches;

  const C = { gold: 0xE2B04A, goldDeep: 0xB8893A, light: 0xECE8DF, graphite: 0x2A303B, slab: 0x1A1F28 };

  const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'low-power' });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  host.appendChild(renderer.domElement);

  const scene = new THREE.Scene();
  const camera = new THREE.OrthographicCamera(-1, 1, 1, -1, 0.1, 100);
  camera.position.set(12, 10.5, 12);
  camera.lookAt(0, 1.9, 0);

  // Light from the top-left, like the isometric illustrations
  scene.add(new THREE.HemisphereLight(0xFFFFFF, 0x0F131A, 1.1));
  const sun = new THREE.DirectionalLight(0xFFF4DE, 2.2); sun.position.set(-4, 14, 9); scene.add(sun);
  const rim = new THREE.DirectionalLight(0x6E8FC8, 0.9); rim.position.set(10, 4, -8); scene.add(rim);

  const world = new THREE.Group(); scene.add(world);

  const mat = {
    slab: new THREE.MeshStandardMaterial({ color: C.slab, roughness: 0.75, metalness: 0.2 }),
    light: new THREE.MeshStandardMaterial({ color: C.light, roughness: 0.55, metalness: 0.05 }),
    gold: new THREE.MeshStandardMaterial({ color: C.gold, roughness: 0.3, metalness: 0.55, emissive: C.goldDeep, emissiveIntensity: 0.28 }),
    graphite: new THREE.MeshStandardMaterial({ color: C.graphite, roughness: 0.5, metalness: 0.35 }),
  };
  const edgeMat = (color, opacity) => new THREE.LineBasicMaterial({ color, transparent: true, opacity });
  function withEdges(mesh, color = 0xFFFFFF, opacity = 0.18) {
    mesh.add(new THREE.LineSegments(new THREE.EdgesGeometry(mesh.geometry), edgeMat(color, opacity)));
    return mesh;
  }

  // Soft contact shadow
  const sh = document.createElement('canvas'); sh.width = sh.height = 128;
  const g = sh.getContext('2d'); const grad = g.createRadialGradient(64, 64, 8, 64, 64, 64);
  grad.addColorStop(0, 'rgba(0,0,0,0.55)'); grad.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = grad; g.fillRect(0, 0, 128, 128);
  const shadow = new THREE.Mesh(new THREE.PlaneGeometry(15, 11), new THREE.MeshBasicMaterial({ map: new THREE.CanvasTexture(sh), transparent: true, depthWrite: false }));
  shadow.rotation.x = -Math.PI / 2; shadow.position.y = -0.45; world.add(shadow);

  // Platform with a fine grid
  const slab = withEdges(new THREE.Mesh(new THREE.BoxGeometry(10, 0.36, 7), mat.slab), C.gold, 0.45);
  slab.position.y = -0.18; world.add(slab);
  const COLS = 6, ROWS = 4, CELL = 1.05, GX = -2.1, GZ = 0.2;
  const gridPts = [];
  for (let i = 0; i <= COLS; i++) { const x = GX + (i - COLS / 2) * CELL; gridPts.push(x, 0.005, GZ - ROWS / 2 * CELL, x, 0.005, GZ + ROWS / 2 * CELL); }
  for (let j = 0; j <= ROWS; j++) { const z = GZ + (j - ROWS / 2) * CELL; gridPts.push(GX - COLS / 2 * CELL, 0.005, z, GX + COLS / 2 * CELL, 0.005, z); }
  const gridGeo = new THREE.BufferGeometry(); gridGeo.setAttribute('position', new THREE.Float32BufferAttribute(gridPts, 3));
  world.add(new THREE.LineSegments(gridGeo, edgeMat(0xFFFFFF, 0.12)));

  // Storage stack: the protected store
  const stack = new THREE.Group(); stack.position.set(3.15, 0, -1.2); world.add(stack);
  for (let i = 0; i < 4; i++) {
    const disc = withEdges(new THREE.Mesh(new THREE.CylinderGeometry(1.15, 1.15, 0.46, 48), mat.graphite), C.gold, i === 3 ? 0.7 : 0.22);
    disc.position.y = 0.25 + i * 0.54; stack.add(disc);
  }
  const cap = new THREE.Mesh(new THREE.CylinderGeometry(1.16, 1.16, 0.06, 48), mat.gold); cap.position.y = 0.25 + 3 * 0.54 + 0.26; stack.add(cap);
  const leds = new THREE.MeshBasicMaterial({ color: C.gold });
  for (let i = 0; i < 4; i++) { const led = new THREE.Mesh(new THREE.BoxGeometry(0.16, 0.06, 0.04), leds); led.position.set(0.55, 0.25 + i * 0.54, 1.0); led.rotation.y = 0.5; stack.add(led); }

  // Data blocks
  let seed = 7; const rnd = () => (seed = (seed * 16807) % 2147483647) / 2147483647;
  const blocks = [];
  const blockGeo = new THREE.BoxGeometry(0.82, 0.5, 0.82);
  const goldCells = new Set([2, 7, 9, 14, 16, 21]);
  for (let r = 0; r < ROWS; r++) for (let c = 0; c < COLS; c++) {
    const i = r * COLS + c;
    const kind = goldCells.has(i) ? 'gold' : (i % 11 === 4 ? 'graphite' : 'light');
    const m = withEdges(new THREE.Mesh(blockGeo, mat[kind].clone()), kind === 'gold' ? 0xFFFFFF : C.gold, kind === 'gold' ? 0.25 : 0.3);
    const tall = kind === 'gold' ? 1.5 : 1;
    m.scale.y = tall;
    const target = new THREE.Vector3(GX + (c - COLS / 2 + 0.5) * CELL, 0.25 * tall, GZ + (r - ROWS / 2 + 0.5) * CELL);
    const start = new THREE.Vector3(-9 - rnd() * 5, 1.5 + rnd() * 6, -5 + rnd() * 10);
    const spin = new THREE.Euler(rnd() * 3, rnd() * 3, rnd() * 3);
    m.position.copy(still ? target : start);
    if (!still) m.rotation.copy(spin);
    world.add(m);
    blocks.push({ m, target, start, spin, delay: 0.25 + (r * COLS + c) * 0.075 + rnd() * 0.12, kind });
  }

  // Gold check emblem
  const emblem = new THREE.Group(); emblem.position.set(-1.2, 4.7, 0.6); scene.add(emblem);
  emblem.add(new THREE.Mesh(new THREE.TorusGeometry(1.0, 0.085, 16, 96), mat.gold));
  emblem.add(new THREE.Mesh(new THREE.CircleGeometry(0.93, 64), new THREE.MeshBasicMaterial({ color: 0x0F131A, transparent: true, opacity: 0.55 })));
  const checkMat = new THREE.MeshStandardMaterial({ color: C.gold, roughness: 0.3, metalness: 0.6, emissive: C.gold, emissiveIntensity: 0.35 });
  function leg(x1, y1, x2, y2) {
    const len = Math.hypot(x2 - x1, y2 - y1);
    const b = new THREE.Mesh(new THREE.BoxGeometry(len + 0.14, 0.15, 0.1), checkMat);
    b.position.set((x1 + x2) / 2, (y1 + y2) / 2, 0.02); b.rotation.z = Math.atan2(y2 - y1, x2 - x1); emblem.add(b);
  }
  leg(-0.42, 0.02, -0.12, -0.3); leg(-0.12, -0.3, 0.44, 0.32);
  emblem.scale.setScalar(still ? 1.2 : 0.001);

  // Size and camera framing
  const VIEW = 11.2;
  function resize() {
    const w = host.clientWidth, h = host.clientHeight; if (!w || !h) return;
    renderer.setSize(w, h, false);
    const a = w / h, s = a >= 1 ? VIEW / 2 : VIEW / 2 / a * 0.92;
    camera.left = -s * a; camera.right = s * a; camera.top = s; camera.bottom = -s; camera.updateProjectionMatrix();
    render(lastT);
  }

  // Pointer tilt
  let tx = 0, ty = 0, px = 0, py = 0;
  if (!still) window.addEventListener('pointermove', (e) => {
    tx = (e.clientX / window.innerWidth - 0.5); ty = (e.clientY / window.innerHeight - 0.5);
  }, { passive: true });

  const ease = (t) => 1 - Math.pow(1 - Math.min(Math.max(t, 0), 1), 3);
  const back = (t) => { t = Math.min(Math.max(t, 0), 1); const k = 1.6; return 1 + (k + 1) * Math.pow(t - 1, 3) + k * Math.pow(t - 1, 2); };
  const landAt = blocks[blocks.length - 1].delay + 1.1;
  let pulseIdx = -1, pulseStart = 0, lastT = 0;

  function render(t) {
    lastT = t;
    if (!still) {
      for (const b of blocks) {
        const k = ease((t - b.delay) / 1.1);
        b.m.position.lerpVectors(b.start, b.target, k);
        b.m.position.y += Math.sin(k * Math.PI) * 1.2;
        b.m.rotation.set(b.spin.x * (1 - k), b.spin.y * (1 - k), b.spin.z * (1 - k));
      }
      const e = back((t - landAt) / 0.9);
      emblem.scale.setScalar(Math.max(0.001, e) * 1.2);
      emblem.position.y = 4.7 + Math.sin(t * 1.2) * 0.12;
      // Once everything has landed, one block at a time lights up: data being classified
      if (t > landAt + 1) {
        if (pulseIdx < 0 || t - pulseStart > 1.4) {
          if (pulseIdx >= 0) blocks[pulseIdx].m.material.emissiveIntensity = blocks[pulseIdx].kind === 'gold' ? 0.28 : 0;
          do { pulseIdx = Math.floor(rnd() * blocks.length); } while (blocks[pulseIdx].kind === 'gold');
          pulseStart = t; blocks[pulseIdx].m.material.emissive.setHex(C.gold);
        }
        const p = Math.sin(Math.min((t - pulseStart) / 1.4, 1) * Math.PI);
        blocks[pulseIdx].m.material.emissiveIntensity = p * 0.55;
      }
      px += (tx - px) * 0.05; py += (ty - py) * 0.05;
      world.rotation.y = px * 0.35; world.rotation.x = py * 0.08;
    }
    emblem.quaternion.copy(camera.quaternion);
    renderer.render(scene, camera);
  }

  new ResizeObserver(resize).observe(host);
  resize();
  hero.classList.add('has-3d');

  if (still) return;
  let running = false, t0 = null;
  function loop(now) {
    if (!running) return;
    if (t0 === null) t0 = now;
    render((now - t0) / 1000);
    requestAnimationFrame(loop);
  }
  new IntersectionObserver((es) => {
    const vis = es[0].isIntersecting;
    if (vis && !running) { running = true; if (t0 !== null) t0 = performance.now() - lastT * 1000; requestAnimationFrame(loop); }
    else if (!vis) running = false;
  }).observe(host);
}
