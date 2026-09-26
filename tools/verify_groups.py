import os
from PIL import Image, ImageDraw

DIR = "pics"

CANDS = {
    "A_kotki": ["WhatsApp Image 2026-09-16 at 7.35.59 PM (2).jpeg", "WhatsApp Image 2026-09-16 at 7.36.11 PM.jpeg"],
    "B_tealfloral": ["WhatsApp Image 2026-09-16 at 7.36.01 PM (1).jpeg", "WhatsApp Image 2026-09-16 at 7.36.07 PM.jpeg"],
    "C_greenpouch": ["WhatsApp Image 2026-09-16 at 7.36.09 PM (1).jpeg", "WhatsApp Image 2026-09-16 at 7.36.15 PM (1).jpeg"],
    "D_kanchi_mat": ["WhatsApp Image 2026-09-16 at 7.36.06 PM.jpeg", "WhatsApp Image 2026-09-16 at 7.36.08 PM (1).jpeg",
                     "WhatsApp Image 2026-09-16 at 7.36.20 PM (2).jpeg", "WhatsApp Image 2026-09-16 at 7.36.20 PM.jpeg"],
    "E_yellowskirt": ["WhatsApp Image 2026-09-16 at 7.35.59 PM (1).jpeg", "WhatsApp Image 2026-09-16 at 7.36.01 PM (3).jpeg"],
    "J_checks": ["WhatsApp Image 2026-09-16 at 7.36.07 PM (1).jpeg", "WhatsApp Image 2026-09-16 at 7.36.08 PM.jpeg",
                 "WhatsApp Image 2026-09-16 at 7.36.13 PM.jpeg"],
}

os.makedirs("tools/cmp", exist_ok=True)
for name, files in CANDS.items():
    thumbs = []
    for f in files:
        im = Image.open(os.path.join(DIR, f)).convert("RGB")
        im.thumbnail((330, 440), Image.LANCZOS)
        thumbs.append((f, im))
    W = sum(t.width for _, t in thumbs) + 10 * (len(thumbs) + 1)
    H = max(t.height for _, t in thumbs) + 46
    sheet = Image.new("RGB", (W, H), (18, 18, 22))
    d = ImageDraw.Draw(sheet)
    x = 10
    for f, t in thumbs:
        sheet.paste(t, (x, 8))
        d.text((x, H - 30), f[-28:-5], fill=(255, 215, 120))
        x += t.width + 10
    sheet.save(f"tools/cmp/{name}.jpg", quality=85)
    print(name, "->", len(files))
