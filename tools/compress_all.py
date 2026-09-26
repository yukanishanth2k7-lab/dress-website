import os, json
from PIL import Image, ImageOps

DIR = "pics"
OUT = "tools/assets/img"
os.makedirs(OUT, exist_ok=True)

W = "WhatsApp Image 2026-09-16 at "
FILES = [
    W + "7.35.58 PM (1).jpeg", W + "7.35.58 PM.jpeg", W + "7.35.59 PM (1).jpeg",
    W + "7.35.59 PM (2).jpeg", W + "7.35.59 PM.jpeg", W + "7.36.00 PM (1).jpeg",
    W + "7.36.00 PM (2).jpeg", W + "7.36.00 PM.jpeg", W + "7.36.01 PM (1).jpeg",
    W + "7.36.01 PM (2).jpeg", W + "7.36.01 PM (3).jpeg", W + "7.36.01 PM.jpeg",
    W + "7.36.02 PM (1).jpeg", W + "7.36.02 PM.jpeg", W + "7.36.03 PM (1).jpeg",
    W + "7.36.03 PM.jpeg", W + "7.36.04 PM (1).jpeg", W + "7.36.04 PM (2).jpeg",
    W + "7.36.04 PM.jpeg", W + "7.36.05 PM (1).jpeg", W + "7.36.05 PM (2).jpeg",
    W + "7.36.05 PM.jpeg", W + "7.36.06 PM (1).jpeg", W + "7.36.06 PM.jpeg",
    W + "7.36.07 PM (1).jpeg", W + "7.36.07 PM (2).jpeg", W + "7.36.07 PM (3).jpeg",
    W + "7.36.07 PM.jpeg", W + "7.36.08 PM (1).jpeg", W + "7.36.08 PM.jpeg",
    W + "7.36.09 PM (1).jpeg", W + "7.36.09 PM.jpeg", W + "7.36.10 PM (1).jpeg",
    W + "7.36.10 PM (2).jpeg", W + "7.36.10 PM (3).jpeg", W + "7.36.10 PM.jpeg",
    W + "7.36.11 PM (1).jpeg", W + "7.36.11 PM (2).jpeg", W + "7.36.11 PM.jpeg",
    W + "7.36.12 PM (1).jpeg", W + "7.36.12 PM (2).jpeg", W + "7.36.12 PM.jpeg",
    W + "7.36.13 PM (1).jpeg", W + "7.36.13 PM (2).jpeg", W + "7.36.13 PM.jpeg",
    W + "7.36.14 PM (1).jpeg", W + "7.36.14 PM (2).jpeg", W + "7.36.14 PM.jpeg",
    W + "7.36.15 PM (1).jpeg", W + "7.36.15 PM (2).jpeg", W + "7.36.15 PM.jpeg",
    W + "7.36.16 PM (1).jpeg", W + "7.36.16 PM (2).jpeg", W + "7.36.16 PM.jpeg",
    W + "7.36.17 PM (1).jpeg", W + "7.36.17 PM.jpeg", W + "7.36.18 PM (1).jpeg",
    W + "7.36.18 PM (2).jpeg", W + "7.36.18 PM.jpeg", W + "7.36.19 PM (1).jpeg",
    W + "7.36.19 PM (2).jpeg", W + "7.36.19 PM.jpeg", W + "7.36.20 PM (1).jpeg",
    W + "7.36.20 PM (2).jpeg", W + "7.36.21 PM (1).jpeg", W + "7.36.21 PM.jpeg",
]
assert len(FILES) == 66, len(FILES)

report = []
for idx, f in enumerate(FILES, 1):
    im = Image.open(os.path.join(DIR, f))
    im = ImageOps.exif_transpose(im)
    im = im.convert("RGB")
    im.thumbnail((720, 720), Image.LANCZOS)
    out = os.path.join(OUT, f"p{idx:02d}.jpg")
    im.save(out, "JPEG", quality=68, optimize=True, progressive=True)
    report.append({"i": idx, "file": f, "kb": round(os.path.getsize(out) / 1024, 1), "w": im.width, "h": im.height})

json.dump(report, open("tools/img_report.json", "w"), indent=1)
tot = sum(r["kb"] for r in report)
print(f"66 images -> {tot:.0f} KB total, avg {tot/66:.0f} KB")
