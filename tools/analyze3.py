import os
from PIL import Image

DIR = "pics"

def norm_gray_vec(im, size=32):
    g = im.convert("L").resize((size, size), Image.LANCZOS)
    px = [float(v) for v in g.getdata()]
    m = sum(px) / len(px)
    var = sum((p - m) ** 2 for p in px) / len(px)
    sd = var ** 0.5 or 1.0
    return [(p - m) / sd for p in px]

def rms(a, b):
    return (sum((x - y) ** 2 for x, y in zip(a, b)) / len(a)) ** 0.5

def color_hist(img, bins=8):
    im = img.convert("RGB").resize((100, 100), Image.LANCZOS)
    px = list(im.getdata())
    hist = [0] * (bins ** 3)
    for r, g, b in px:
        hist[(r * bins // 256) * bins ** 2 + (g * bins // 256) * bins + (b * bins // 256)] += 1
    n = len(px)
    return [v / n for v in hist]

def hist_dist(a, b):
    return sum(abs(x - y) for x, y in zip(a, b)) / 2.0

files = sorted(f for f in os.listdir(DIR) if f.lower().endswith((".jpg", ".jpeg", ".png")))
structs, hists = {}, {}
for f in files:
    im = Image.open(os.path.join(DIR, f))
    im.load()
    structs[f] = norm_gray_vec(im)
    hists[f] = color_hist(im)

pairs = []
for i in range(len(files)):
    for j in range(i + 1, len(files)):
        f1, f2 = files[i], files[j]
        pairs.append((rms(structs[f1], structs[f2]), hist_dist(hists[f1], hists[f2]), f1, f2))

pairs.sort()
print("Top 40 closest pairs:")
for d, hd, f1, f2 in pairs[:40]:
    print(f"  {d:.3f}  hd={hd:.3f}  {os.path.basename(f1)}  <->  {os.path.basename(f2)}")

ds = sorted(p[0] for p in pairs)
n = len(ds)
print(f"\nmin={ds[0]:.3f} p5={ds[n//20]:.3f} p10={ds[n//10]:.3f} p25={ds[n//4]:.3f} median={ds[n//2]:.3f}")
