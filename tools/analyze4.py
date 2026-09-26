import os
import numpy as np
from PIL import Image

DIR = "pics"

# ---- structural descriptor on luminance: high-pass filtered, so color/contrast don't matter ----
def structure_vec(im, size=48):
    g = np.asarray(im.convert("L").resize((size, size), Image.LANCZOS), dtype=np.float64)
    g = (g - g.mean()) / (g.std() + 1e-9)
    # high-pass: subtract 4-neighbor average
    hp = g - (np.roll(g, 1, 0) + np.roll(g, -1, 0) + np.roll(g, 1, 1) + np.roll(g, -1, 1)) / 4
    v = np.concatenate([g.ravel(), hp.ravel()])
    v = (v - v.mean()) / (v.std() + 1e-9)
    return v

def rms(a, b):
    return float(np.sqrt(np.mean((a - b) ** 2)))

files = sorted(f for f in os.listdir(DIR) if f.lower().endswith((".jpg", ".jpeg", ".png")))
vecs = {}
for f in files:
    im = Image.open(os.path.join(DIR, f))
    im.load()
    vecs[f] = structure_vec(im)

pairs = []
for i in range(len(files)):
    for j in range(i + 1, len(files)):
        f1, f2 = files[i], files[j]
        pairs.append((rms(vecs[f1], vecs[f2]), f1, f2))
pairs.sort()

print("Top 30 closest pairs (high-pass structure):")
for d, f1, f2 in pairs[:30]:
    print(f"  {d:.3f}  {f1}  <->  {f2}")

ds = sorted(p[0] for p in pairs)
n = len(ds)
print(f"\nmin={ds[0]:.3f} p2={ds[n//50]:.3f} p5={ds[n//20]:.3f} p10={ds[n//10]:.3f} median={ds[n//2]:.3f}")
