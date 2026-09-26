import os
from PIL import Image, ImageOps

DIR = "tools/assets/img"
total_before = total_after = 0
for f in sorted(os.listdir(DIR)):
    if not f.endswith(".jpg"):
        continue
    p = os.path.join(DIR, f)
    total_before += os.path.getsize(p)
    im = Image.open(p)
    im = ImageOps.exif_transpose(im).convert("RGB")
    im.thumbnail((640, 640), Image.LANCZOS)
    im.save(p, "JPEG", quality=72, optimize=True, progressive=True)
    total_after += os.path.getsize(p)
print(f"{total_before/1e6:.2f} MB -> {total_after/1e6:.2f} MB")
