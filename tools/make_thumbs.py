import os
import numpy as np
from PIL import Image
import json

DIR = "pics"
OUT = "tools/thumbs"

os.makedirs(OUT, exist_ok=True)
files = sorted(f for f in os.listdir(DIR) if f.lower().endswith((".jpg", ".jpeg", ".png")))
for f in files:
    im = Image.open(os.path.join(DIR, f))
    im.load()
    im = im.convert("RGB")
    im.thumbnail((320, 320), Image.LANCZOS)
    im.save(os.path.join(OUT, f.replace(" ", "_")), quality=85)
print("done", len(files))
