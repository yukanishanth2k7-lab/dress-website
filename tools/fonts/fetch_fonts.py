import re, os, urllib.request

css = open("tools/fonts/cormorant.css").read()
blocks = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{[^}]+\})", css)
os.makedirs("tools/fonts/files", exist_ok=True)
out_css = []
seen = {}
for subset, block in blocks:
    if subset not in ("latin", "latin-ext"):
        continue
    fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
    style = re.search(r"font-style:\s*(\w+)", block).group(1)
    weight = re.search(r"font-weight:\s*(\d+)", block).group(1)
    url = re.search(r"url\((https://[^)]+)\)", block).group(1)
    urange = re.search(r"unicode-range:\s*([^;]+);", block).group(1)
    fname = f"{fam.replace(' ', '')}-{style}-{weight}-{subset}.woff2"
    if fname not in seen:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        data = urllib.request.urlopen(req, timeout=30).read()
        open(os.path.join("tools/fonts/files", fname), "wb").write(data)
        seen[fname] = len(data)
    block = re.sub(r"url\(https://[^)]+\)\s*format\('woff2'\)", f"url(fonts/files/{fname}) format('woff2')", block)
    out_css.append(f"/* {subset} */\n{block}")
    print(f"{fam} {style} {weight} {subset}: {seen[fname]//1024} KB")

open("tools/fonts/fonts.css", "w").write("\n".join(out_css))
total = sum(seen.values())
print(f"\n{len(seen)} files, {total//1024} KB total")
