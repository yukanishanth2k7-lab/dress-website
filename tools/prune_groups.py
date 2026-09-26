import os, re

css = open("tools/fonts/cormorant.css").read()
blocks = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{[^}]+\})", css)
for subset, block in blocks:
    if subset not in ("latin", "latin-ext"):
        continue
    ur = re.search(r"unicode-range:\s*([^;]+);", block).group(1)
    print(subset, "::", ur.strip()[:140])
