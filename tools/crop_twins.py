import os
from PIL import Image, ImageOps

im = Image.open("pics/WhatsApp Image 2026-09-16 at 7.36.14 PM (2).jpeg")
im = ImageOps.exif_transpose(im).convert("RGB")
w, h = im.size
os.makedirs("tools/assets/img", exist_ok=True)
for name, box in (("malligai_l", (0, 0, w // 2, h)), ("malligai_r", (w // 2, 0, w, h))):
    crop = im.crop(box)
    crop.thumbnail((560, 800), Image.LANCZOS)
    out = f"tools/assets/img/{name}.jpg"
    crop.save(out, "JPEG", quality=68, optimize=True, progressive=True)
    print(name, crop.size, round(os.path.getsize(out) / 1024, 1), "KB")
