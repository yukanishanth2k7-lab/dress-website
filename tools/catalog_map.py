import os, json
from PIL import Image

# Catalog: pNN.jpg -> [name, type, hex swatch]   (single-color listings)
# Crop-derived and variant-grouped images are wired separately in build_site.py.
CATALOG = {
    1:  ("Kanchi Silk 'Mayil Koel'", "Pattu Pavadai", "#2F4CB3"),
    2:  ("Pachai Kili Set", "Pattu Pavadai", "#DF6D1E"),
    3:  ("Rani Sunset Pavadai", "Pattu Pavadai", "#F2C230"),
    4:  ("Riri Peacock Set", "Pattu Pavadai", "#7A2E8E"),
    5:  ("Mayil Kanavu Set", "Pattu Pavadai", "#1E50A2"),
    6:  ("Vaiyali Dress", "Silk Gown", "#8E1F4B"),
    7:  ("Thendral Silk Gown", "Silk Gown", "#F2A7C3"),
    8:  ("Veera Vanjikko Set", "Pattu Pavadai", "#2BB5A0"),
    9:  ("Blue Rose Pavadai", "Pattu Pavadai", "#2795B8"),
    10: ("Aanchal Kali Set", "Pattu Pavadai", "#DF6D1E"),
    11: ("Bharat Asset Silk Set", "Pattu Pavadai", "#F2C230"),
    12: ("Ivory & Wine Pavadai", "Pattu Pavadai", "#7B1E3C"),
    13: ("Mallika Rani Set", "Pattu Pavadai", "#C2185B"),
    14: ("Parijat Vintage Set", "Pattu Pavadai", "#48A9A6"),
    15: ("Coimbatore Cotton Set", "Cotton Set", "#3BBFA5"),
    16: ("Anaya Tissue Set", "Pattu Pavadai", "#E2571E"),
    17: ("Kanmani Pattu Set", "Pattu Pavadai", "#2C6E49"),
    18: ("Radha Rukmani Set", "Pattu Pavadai", "#F2C230"),
    19: ("Meenakshi Oonjal Set", "Pattu Pavadai", "#C2185B"),
    20: ("Mullai Poo Set", "Pattu Pavadai", "#C2185B"),
    21: ("Peacock Teal Pavadai", "Pattu Pavadai", "#2BB5A0"),
    22: ("Anthuri Velvet Set", "Pattu Pavadai", "#3E1C3C"),
    23: ("Rani Pink Silk Set", "Pattu Pavadai", "#F06292"),
    24: ("Thamaraik Kili Set", "Pattu Pavadai", "#D95F13"),
    25: ("Vaigai Silk Set", "Pattu Pavadai", "#9CB4CC"),
    26: ("Mayil Kan Silks Set", "Pattu Pavadai", "#C2185B"),
    27: ("Anjali Silk Set", "Pattu Pavadai", "#5B2D8E"),
    28: ("Arasi Kottadi Set", "Pattu Pavadai", "#7A2E8E"),
    29: ("Nalli Bhagalpuri Set", "Bhagalpuri Set", "#C9163F"),
    30: ("Lotus Trail Pavadai", "Pattu Pavadai", "#4A7FA5"),
    31: ("Pachai Veshthi Set", "Pattu Pavadai", "#8DB600"),
    32: ("Kachhi Kundan Set", "Pattu Pavadai", "#D95F13"),
    33: ("Pattu Langa Pastel Set", "Pattu Pavadai", "#E8DCC8"),
    34: ("Thamarai Silks Set", "Pattu Pavadai", "#8E1F4B"),
    35: ("Chinna Ponnu Gown", "Silk Gown", "#F06292"),
    36: ("Sindhoori Kanchi Set", "Pattu Pavadai", "#C9163F"),
    37: ("Maragatha Green Set", "Pattu Pavadai", "#3E7C1F"),
    38: ("Nalli Silks Party Set", "Partywear Set", "#3E1C3C"),
    39: ("Meenakshi Party Set", "Partywear Set", "#C2185B"),
    40: ("Kutchi Emb Set", "Pattu Pavadai", "#F06292"),
    41: ("Vaiyali Silk Set", "Pattu Pavadai", "#DF6D1E"),
    42: ("Nizam Collection Set", "Pattu Pavadai", "#2E8B57"),
    43: ("Vaiyali Designer Set", "Designer Set", "#E91E63"),
    44: ("Radha Designer Set", "Designer Set", "#F06292"),
    45: ("Karishma/Kanha Silk Set", "Pattu Pavadai", "#1E50A2"),
    46: ("Peacock Blue Fancy Set", "Fancy Langa", "#1E50A2"),
    47: ("Kanchi Pattu Pavadai", "Kanchi Pattu", "#7A2E8E"),
    48: ("Radha Kanchi Set", "Kanchi Pattu", "#5B2D8E"),
    49: ("Sakura Pearl Set", "Silk Gown", "#F2C230"),
    50: ("Sakura Pearl Gown", "Silk Gown", "#C9A227"),
    51: ("Noon Silk Set", "Silk Gown", "#2BB5A0"),
    52: ("Sri Kanchan Silks Set", "Kanchi Pattu", "#C2185B"),
    53: ("Maroon Party Gown", "Party Gown", "#8E1F4B"),
    54: ("Neon & Navy Kali Set", "Kali Kutchi", "#5B2D8E"),
    55: ("Roop Kathak Set", "Kali Kutchi", "#C2185B"),
    56: ("Sri Kanchan Frocks Set", "Silk Frocks", "#2795B8"),
    57: ("Sri Kanchan Silk Set", "Silk Frocks", "#E91E63"),
    58: ("Valentina Lilac Set", "Party Gown", "#7A2E8E"),
    59: ("Sri Kanchan Party Set", "Party Gown", "#1E50A2"),
    60: ("Sai Meenakshi Silk Set", "Pattu Pavadai", "#F2C230"),
    61: ("Kanchi Pattu Langa", "Kanchi Pattu", "#C2185B"),
    62: ("Saree Style Pattu Langa", "Kanchi Pattu", "#2C6E49"),
    63: ("RadhaKalyanam Silk Set", "Pattu Pavadai", "#C2185B"),
    64: ("Pink Chanderi Set", "Chanderi Set", "#F2C230"),
    65: ("Pure Zari Pattu Pavadai", "Chanderi Set", "#2795B8"),
    66: ("Mayil Kanchi Border", "Kanchi Pattu", "#5B2D8E"),
    67: ("Peacock & Mint Frock", "Silk Frocks", "#2BB5A0"),
}

DIR = "tools/assets/img"
report = []
for i in range(1, 68):
    f = f"p{i:02d}.jpg" if i <= 66 else "p67.jpg"
    p = os.path.join(DIR, f)
    im = Image.open(p)
    entry = CATALOG[i]
    report.append({"i": i, "file": f, "name": entry[0], "type": entry[1],
                   "hex": entry[2], "w": im.width, "h": im.height,
                   "kb": round(os.path.getsize(p) / 1024, 1)})
json.dump(report, open("tools/catalog_map.json", "w"), indent=1)
print("entries:", len(report))
print("types:", sorted(set(r["type"] for r in report)))
