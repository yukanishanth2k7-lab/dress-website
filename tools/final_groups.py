import os
import numpy as np
from PIL import Image

DIR = "pics"

def structure_vec(im, size=48, crop=None):
    if crop:
        w, h = im.size
        cw, ch = int(w * crop), int(h * crop)
        im = im.crop(((w - cw) // 2, (h - ch) // 2, (w + cw) // 2, (h + ch) // 2))
    g = np.asarray(im.convert("L").resize((size, size), Image.LANCZOS), dtype=np.float64)
    g = (g - g.mean()) / (g.std() + 1e-9)
    hp = g - (np.roll(g, 1, 0) + np.roll(g, -1, 0) + np.roll(g, 1, 1) + np.roll(g, -1, 1)) / 4
    v = np.concatenate([g.ravel(), hp.ravel()])
    return (v - v.mean()) / (v.std() + 1e-9)

def rms(a, b):
    return float(np.sqrt(np.mean((a - b) ** 2)))

def color_hist(img, bins=8):
    im = img.convert("RGB").resize((100, 100), Image.LANCZOS)
    px = np.asarray(im, dtype=np.int32).reshape(-1, 3)
    hist = np.zeros(bins ** 3)
    idx = (px[:, 0] * bins // 256) * bins ** 2 + (px[:, 1] * bins // 256) * bins + (px[:, 2] * bins // 256)
    for i in idx:
        hist[i] += 1
    return hist / hist.sum()

def hist_dist(a, b):
    return float(np.abs(a - b).sum() / 2)

files = sorted(f for f in os.listdir(DIR) if f.lower().endswith((".jpg", ".jpeg", ".png")))
Vg, Vc, H = {}, {}, {}
for f in files:
    im = Image.open(os.path.join(DIR, f)); im.load()
    Vg[f] = structure_vec(im, crop=None)
    Vc[f] = structure_vec(im, crop=0.62)
    H[f] = color_hist(im)

n = len(files)
# global mutual-nearest
nearest = {}
for f in files:
    ds = sorted((rms(Vg[f], Vg[g2]), g2) for g2 in files if g2 != f)
    nearest[f] = ds[:3]

print("Mutual nearest-neighbour pairs (global d, center-crop d, color-hist d):")
seen = set()
for f in files:
    d1, m1 = nearest[f][0]
    if nearest[m1][0][1] == f and f < m1:
        dc = min(rms(Vc[f], Vc[m1]), 9)
        hd = hist_dist(H[f], H[m1])
        print(f"  {d1:.3f}  crop={dc:.3f}  hd={hd:.3f}   {f}  <->  {m1}")

print("\nSecond-nearest context for suspect images:")
for f in ["WhatsApp Image 2026-09-16 at 7.35.59 PM.jpeg",
          "WhatsApp Image 2026-09-16 at 7.36.08 PM (1).jpeg",
          "WhatsApp Image 2026-09-16 at 7.36.06 PM.jpeg",
          "WhatsApp Image 2026-09-16 at 7.36.09 PM (1).jpeg",
          "WhatsApp Image 2026-09-16 at 7.36.15 PM (1).jpeg",
          "WhatsApp Image 2026-09-16 at 7.36.10 PM (3).jpeg",
          "WhatsApp Image 2026-09-16 at 7.36.19 PM.jpeg",
          "WhatsApp Image 2026-09-16 at 7.36.11 PM (2).jpeg",
          "WhatsApp Image 2026-09-16 at 7.36.18 PM (2).jpeg"]:
    print(f"  {f}")
    for d, g2 in nearest[f]:
        dc = rms(Vc[f], Vc[g2])
        hd = hist_dist(H[f], H[g2])
        print(f"      d={d:.3f} crop={dc:.3f} hd={hd:.3f}  {g2}")

# center-crop distance distribution for calibration
cc = sorted(rms(Vc[files[i]], Vc[files[j]]) for i in range(n) for j in range(i + 1, n))
print(f"\ncenter-crop dist: min={cc[0]:.3f} p1={cc[n*99//10000]:.3f} p2={cc[n*2//10000]:.3f} p5={cc[n//20]:.3f} median={cc[n//2]:.3f}")
