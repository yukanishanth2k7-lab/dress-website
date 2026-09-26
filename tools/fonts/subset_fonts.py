import os, re
from fontTools.subset import Subsetter, Options, load_font, save_font

NEEDED = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-–—'’&.,!?%():;/+₹×★✦●⟶♥~"

FDIR = "tools/fonts/files"
OUT = "tools/fonts/subset"
os.makedirs(OUT, exist_ok=True)

total = 0
for f in sorted(os.listdir(FDIR)):
    if not f.endswith(".woff2"):
        continue
    src = os.path.join(FDIR, f)
    opts = Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga", "calt"]
    opts.drop_tables += ["DSIG"]
    opts.desubroutinize = True
    font = load_font(src, opts)
    ss = Subsetter(opts)
    ss.populate(text=NEEDED)
    ss.subset(font)
    dst = os.path.join(OUT, f)
    save_font(font, dst, opts)
    kb = os.path.getsize(dst) / 1024
    total += os.path.getsize(dst)
    print(f"{f}: {kb:.1f} KB")
print(f"TOTAL {total/1024:.1f} KB")
