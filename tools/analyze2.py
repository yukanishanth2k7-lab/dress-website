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

# find candidate pairs: low structural distance AND not-too-different histogram
pairs = []
for i in range(len(files)):
    for j in range(i + 1, len(files)):
        f1, f2 = files[i], files[j]
        d = rms(structs[f1], structs[f2])
        if d < 0.45:
            hd = hist_dist(hists[f1], hists[f2])
            pairs.append((d, hd, f1, f2))

pairs.sort()
print("Similar pairs (structRMS, colorHistDist):")
for d, hd, f1, f2 in pairs:
    tag = "SAME-COLOR?" if hd < 0.10 else ("DIFF-COLOR?" if hd >= 0.10 else "")
    print(f"  {d:.3f}  hd={hd:.3f}  {tag}")
    print(f"      {f1}")
    print(f"      {f2}")
