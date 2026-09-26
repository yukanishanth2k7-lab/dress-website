import os
from PIL import Image, ImageDraw

DIR = "pics"
OUT = "tools/sheets"
os.makedirs(OUT, exist_ok=True)

files = sorted(f for f in os.listdir(DIR) if f.lower().endswith((".jpg", ".jpeg", ".png")))

def short(f):
    # "WhatsApp Image 2026-09-16 at 7.36.05 PM (1).jpeg" -> "05-1"
    base = f.replace("WhatsApp Image 2026-09-16 at ", "").replace(" PM.jpeg", "").replace(" PM (", "-").replace(".jpeg", "")
    return base.replace(" PM", "")

per = 12
cols, rows = 4, 3
TW, TH, LBL = 300, 380, 26
for si in range(0, len(files), per):
    batch = files[si:si + per]
    sheet = Image.new("RGB", (cols * TW, rows * (TH + LBL)), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(batch):
        im = Image.open(os.path.join(DIR, f)).convert("RGB")
        im.thumbnail((TW - 8, TH - 8), Image.LANCZOS)
        x = (i % cols) * TW
        y = (i // cols) * (TH + LBL)
        sheet.paste(im, (x + (TW - im.width) // 2, y + (TH - im.height) // 2))
        d.text((x + 8, y + TH + 4), f"{si + i + 1}: {short(f)}", fill=(255, 215, 120))
    sheet.save(os.path.join(OUT, f"sheet_{si // per + 1}.jpg"), quality=82)
    print(f"sheet_{si // per + 1}.jpg -> {len(batch)} imgs")
