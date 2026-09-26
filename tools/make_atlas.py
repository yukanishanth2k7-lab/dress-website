import os
from PIL import Image, ImageDraw, ImageFont

DIR = "pics"
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
    W + "7.36.19 PM (2).jpeg", W + "7.36.19 PM.jpeg",    W + "7.36.20 PM (1).jpeg",
    W + "7.36.20 PM (2).jpeg", W + "7.36.20 PM.jpeg", W + "7.36.21 PM (1).jpeg",
    W + "7.36.21 PM.jpeg",
]
assert len(FILES) == 67, len(FILES)

try:
    font = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 44)
    small = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 20)
except Exception:
    font = small = None

COLS, TW, TH, LBL = 4, 380, 480, 64
os.makedirs("tools/atlas", exist_ok=True)

def build(batch, out):
    rows = (len(batch) + COLS - 1) // COLS
    sheet = Image.new("RGB", (COLS * TW, rows * (TH + LBL)), (15, 15, 18))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(batch):
        im = Image.open(os.path.join(DIR, f)).convert("RGB")
        im.thumbnail((TW - 12, TH - 12), Image.LANCZOS)
        x = (i % COLS) * TW
        y = (i // COLS) * (TH + LBL)
        sheet.paste(im, (x + (TW - im.width) // 2, y + (TH - im.height) // 2))
        tag = f.replace("WhatsApp Image 2026-09-16 at ", "").replace(" PM", "").replace(".jpeg", "")
        d.rectangle([x, y + TH, x + TW, y + TH + LBL], fill=(15, 15, 18))
        d.text((x + 10, y + TH + 8), f"#{batch_start + i + 1}", fill=(255, 210, 90), font=font)
        d.text((x + 110, y + TH + 20), tag, fill=(200, 200, 200), font=small)
    sheet.save(out, quality=80)
    print(out, sheet.size)

for half in (0, 1):
    batch = FILES[half * 33:(half + 1) * 33]
    batch_start = half * 33
    build(batch, f"tools/atlas/atlas_{half + 1}.jpg")
