import os, json
from PIL import Image
from PIL.ExifTags import TAGS

DIR = "pics"

def phash(img, size=16):
    g = img.convert("L").resize((size+1, size), Image.LANCZOS)
    px = list(g.getdata())
    rows = [px[i*(size+1):(i+1)*(size+1)] for i in range(size)]
    # dHash horizontal: bit = left brighter than right
    bits = []
    for row in rows:
        for x in range(size):
            bits.append(1 if row[x] > row[x+1] else 0)
    return bits

def dist(a, b):
    return sum(1 for x, y in zip(a, b) if x != y)

def dom_color(img, size=60):
    im = img.convert("RGB").resize((size, size), Image.LANCZOS)
    px = list(im.getdata())
    # average of pixels, and also a quantized mode
    n = len(px)
    avg = tuple(sum(c[i] for c in px)//n for i in range(3))
    # saturation-weighted: most common quantized color bucket
    from collections import Counter
    buckets = Counter((c[0]//24, c[1]//24, c[2]//24) for c in px)
    top = buckets.most_common(6)
    return avg, top

files = sorted(f for f in os.listdir(DIR) if f.lower().endswith((".jpg", ".jpeg", ".png")))
out = []
for f in files:
    p = os.path.join(DIR, f)
    im = Image.open(p)
    im.load()
    w, h = im.size
    thumb = im.convert("RGB").resize((200, 200), Image.LANCZOS)
    hsh = phash(im)
    avg, top = dom_color(im)
    hsv = Image.merge("HSV", [thumb.convert("RGB").split()[i] for i in range(3)])
    hsv = hsv.resize((1,1)).getpixel((0,0))
    out.append({
        "file": f, "size_kb": round(os.path.getsize(p)/1024), "w": w, "h": h,
        "ratio": round(w/h, 3), "hash": "".join(map(str, hsh)),
        "avg": avg, "hsv": hsv, "top_buckets": top,
    })

# group by hash distance <= 12 (of 256 bits)
groups = []
for item in out:
    placed = False
    for g in groups:
        if dist(item["hash"], g[0]["hash"]) <= 14:
            g.append(item); placed = True; break
    if not placed:
        groups.append([item])

print(f"{len(files)} files, {len(groups)} hash-groups")
for gi, g in enumerate(groups):
    print(f"\n## Group {gi+1} ({len(g)} imgs)")
    for it in g:
        print(f"  {it['file']}  {it['w']}x{it['h']} kb={it['size_kb']} avg={it['avg']} hsv={it['hsv']}")
