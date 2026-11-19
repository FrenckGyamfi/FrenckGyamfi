import sys
from collections import deque
import numpy as np
from PIL import Image, ImageFilter
names = sys.argv[1].split(',')
LUM_MIN, SAT_MAX, GRAD_MAX = float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4])
for n in names:
    im = Image.open(f'images/{n}.webp').convert('RGB')
    a = np.asarray(im).astype(np.float32); H, W, _ = a.shape
    lum = a @ np.array([.299, .587, .114], np.float32)
    sat = a.max(2) - a.min(2)
    # local gradient (max abs diff to 4-neighbours) on a lightly blurred luminance
    L = np.asarray(Image.fromarray(lum.astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6))).astype(np.float32)
    g = np.zeros_like(L)
    g[:, 1:] = np.maximum(g[:, 1:], abs(L[:, 1:] - L[:, :-1])); g[:, :-1] = np.maximum(g[:, :-1], abs(L[:, 1:] - L[:, :-1]))
    g[1:, :] = np.maximum(g[1:, :], abs(L[1:, :] - L[:-1, :])); g[:-1, :] = np.maximum(g[:-1, :], abs(L[1:, :] - L[:-1, :]))
    ok = (lum >= LUM_MIN) & (sat <= SAT_MAX) & (g <= GRAD_MAX)
    from PIL import ImageDraw
    prot = Image.new('L', (W, H), 0); dd = ImageDraw.Draw(prot)
    if n == 'consultancy':
        for b in [(256,45,704,196),(96,371,317,558),(365,371,592,558),(640,371,864,558),(437,259,523,299)]: dd.rounded_rectangle(b, radius=6, fill=255)
    if n == 'kubernetes':
        dd.ellipse((144,150,660,482), fill=255)
        dd.polygon([(316,123),(536,123),(576,167),(613,213),(613,300),(233,300),(233,213),(273,167)], fill=255)
    ok &= ~(np.asarray(prot) > 0)
    ext = np.zeros((H, W), bool); q = deque()
    for x in range(W): q.extend([(0, x), (H - 1, x)])
    for y in range(H): q.extend([(y, 0), (y, W - 1)])
    okf = ok.ravel(); extf = ext.ravel()
    while q:
        y, x = q.popleft(); i = y * W + x
        if extf[i] or not okf[i]: continue
        extf[i] = True
        if x > 0: q.append((y, x - 1))
        if x < W - 1: q.append((y, x + 1))
        if y > 0: q.append((y - 1, x))
        if y < H - 1: q.append((y + 1, x))
    # grow 2px into light, low-saturation antialias pixels to kill white fringes
    grow = ext.copy()
    light = (lum >= 185) & (sat <= 22)
    for _ in range(2):
        nb = grow.copy()
        nb[1:, :] |= grow[:-1, :]; nb[:-1, :] |= grow[1:, :]; nb[:, 1:] |= grow[:, :-1]; nb[:, :-1] |= grow[:, 1:]
        grow = grow | (nb & light)
    m = np.asarray(Image.fromarray((grow * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.7))).astype(np.float32) / 255
    ext_a = np.clip((255 - lum) / 255 * 1.4, 0, 1)          # shadows become soft dark shadows
    alpha = (1 - m) + m * ext_a
    rgb = np.where(alpha[..., None] > 1e-3, a * ((1 - m) / np.maximum(alpha, 1e-3))[..., None], 0)
    out = np.dstack([np.clip(rgb, 0, 255), np.clip(alpha * 255, 0, 255)]).astype(np.uint8)
    Image.fromarray(out, 'RGBA').save(f'images/dark/{n}.webp', 'WEBP', quality=88, method=6)
    print(n, round(grow.mean() * 100), '% background')
