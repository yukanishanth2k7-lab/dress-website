# -*- coding: utf-8 -*-
"""Builds kc-collection.html — fully self-contained (fonts + images inlined as base64)."""
import base64, json, os, sys
from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "site_parts"))
from styles import CSS
from scripts import JS

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
IMG = os.path.join(ROOT, "tools", "assets", "img")
FONTDIR = os.path.join(ROOT, "tools", "fonts", "subset")

# ------------------------------------------------------------------ assets --
def b64(path):
    with open(path, "rb") as fh:
        return "data:image/webp;base64," + base64.b64encode(fh.read()).decode()

def lqip(path, px=14):
    im = Image.open(path).convert("RGB")
    im.thumbnail((px, px), Image.LANCZOS)
    out = os.path.join(ROOT, "tools", "assets", "_lqip.jpg")
    im.save(out, "JPEG", quality=45)
    data = base64.b64encode(open(out, "rb").read()).decode()
    os.remove(out)
    return "data:image/jpeg;base64," + data

# Embed every product WebP as base64 (66 originals + 2 twin-crops + teal frock).
IMGS_JSON = {}
LQIP_JSON = {}
KEYS = [f"p{i:02d}" for i in range(1, 67)] + ["p67", "malligai_l", "malligai_r"]
for key in KEYS:
    f = os.path.join(IMG, f"{key}.webp")
    IMGS_JSON[key] = b64(f)
    LQIP_JSON[key] = lqip(f)

# ------------------------------------------------------------------ fonts --
def font_face(fam, style, weight, fname, urange):
    data = base64.b64encode(open(os.path.join(FONTDIR, fname), "rb").read()).decode()
    return (
        "@font-face{font-family:'%s';font-style:%s;font-weight:%s;font-display:swap;"
        "src:url(data:font/woff2;base64,%s)format('woff2');unicode-range:%s}"
        % (fam, style, weight, data, urange)
    )

UR_LATIN = ("U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,"
            "U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,"
            "U+2212,U+2215,U+FEFF,U+FFFD")
UR_EXT = ("U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+0304,"
          "U+0308,U+0329,U+1D00-1DBF,U+1E00-1E9F,U+1EF2-1EFF,U+2020,U+20A0-20AB,"
          "U+20AD-20C0,U+2113,U+2C60-2C7F,U+A720-A7FF")

faces = []
for style, sname in (("normal", "normal"), ("italic", "italic")):
    corm_weights = (400, 500, 600, 700) if style == "italic" else (400, 500, 600)
    for weight in corm_weights:
        for sub, ur in (("latin", UR_LATIN), ("latin-ext", UR_EXT)):
            faces.append(font_face("Cormorant Garamond", style, weight,
                                   f"CormorantGaramond-{sname}-{weight}-{sub}.woff2", ur))
for weight in (400, 500, 600, 700, 800):
    for sub, ur in (("latin", UR_LATIN), ("latin-ext", UR_EXT)):
        faces.append(font_face("Manrope", "normal", weight,
                               f"Manrope-normal-{weight}-{sub}.woff2", ur))
FONTS_CSS = "\n".join(faces)

# ------------------------------------------------------------------ catalog --
# imgKey -> embedded image.  "lqip-only" keys resolve at runtime from LQIPS.
def P(id_, name, type_, imgKey, hex_, desc, badge=None, colors=None):
    return {"id": str(id_), "name": name, "type": type_, "imgKey": imgKey,
            "hex": hex_, "desc": desc, "badge": badge, "colors": colors}

def C(name, hex_, imgKey):
    return {"name": name, "hex": hex_, "imgKey": imgKey}

D = "Handloom poly-silk pattu pavadai set — top & flared skirt. Soft, itch-free lining; sisters' festive favourite. Fits ages 2-11."

PRODUCTS = [
    P(1,  "Kanchi Silk \u2018Mayil Koel\u2019",  "Pattu Pavadai", "p01", "#2F4CB3", "Royal-blue Kanchi body with a woven peacock-green border and elephant zari motifs.", "Bestseller"),
    P(2,  "Pachai Kili Set",        "Pattu Pavadai", "p02", "#DF6D1E", "Parrot-green scanned silk with a chunky orange Kanchi border and contrast blouse.", None),
    P(3,  "Rani Sunset Pavadai",    "Pattu Pavadai", "p03", "#F2C230", "Sunshine rani skirt, deep purple blouse, and a brindled zari fall — sunset in three pleats."),
    P(4,  "Riri Peacock Set",       "Pattu Pavadai", "p04", "#7A2E8E", "Peacock teal skirt with a wine brocade blouse and purple sheer dupatta.", "New"),
    P(5,  "Mayil Kanavu Set",       "Pattu Pavadai", "p05", "#1E50A2", "True-blue silk skirt, grey-blue border, bow-back top — made for twirl photographs.", "Bestseller"),
    P(6,  "Vaiyali Dress",          "Silk Gown",     "p06", "#8E1F4B", "Wine checked silk gown with a mandarin collar, flared skirt, and glass-bead work."),
    P(7,  "Thendral Silk Gown",     "Silk Gown",     "p07", "#F2A7C3", "Blush-pink pattu gown with a zari kamarbandh and a tissue flare — pastel-pack favourite.", "Bestseller"),
    P(8,  "Veera Vanjikko Set",     "Pattu Pavadai", "p08", "#2BB5A0", "Aqua Kanchi top over a silver-tissue skirt; the aladi-pattam plait comes included.", None),
    P(9,  "Blue Rose Pavadai",      "Pattu Pavadai", "p09", "#2795B8", "Floral-print skirt with a silver Kanchi fall, pink peplum top, and seashell buttons.", None, [C("Blue Rose", "#2795B8", "p09"), C("Fuchsia", "#D6336C", "p28")]),
    P(10, "Aanchal Kali Set",       "Pattu Pavadai", "p10", "#DF6D1E", "Peacock-teal Kanchi skirt with an orange ruffle-blouse; rainbow-bright for shot-run photos.", None),
    P(11, "Bharat Asset Silk Set",  "Pattu Pavadai", "p11", "#F2C230", "Zari-dotted purple blouse over a heavy-box-pleat yellow skirt with maroon gold borders.", "Bestseller"),
    P(12, "Ivory & Wine Pavadai",   "Pattu Pavadai", "p12", "#7B1E3C", "Cream latté silk skirt with a wine embroidery blouse and gold tassels for the plait."),
    P(13, "Mallika Rani Set",       "Pattu Pavadai", "p13", "#C2185B", "Teal Kanchi skirt, rose-pink silk top, and a woven drape — twin-ready and photo-classic.", None, [C("Teal Rose", "#C2185B", "p13"), C("Midnight", "#1F3A93", "p25")]),
    P(14, "Parijat Vintage Set",    "Pattu Pavadai", "p14", "#48A9A6", "Powder-blue floral jacket with pastel roses over a blush floral skirt; vintage-rose palette.", None),
    P(15, "Coimbatore Cotton Set",  "Cotton Set",    "p15", "#3BBFA5", "Mint-green cotton top, gold woven Kanchi skirt — the every-occasion cotton comfort pick."),
    P(16, "Anaya Tissue Set",       "Pattu Pavadai", "p16", "#E2571E", "Rust-orange zari blouse with ivory tissue skirt and copper-gold border fall.", None),
    P(17, "Kanmani Pattu Set",      "Pattu Pavadai", "p17", "#2C6E49", "Emerald Kanchi blouse over a teal-black checked pattu skirt; a green-gold statement.", None),
    P(18, "Radha Rukmani Set",      "Pattu Pavadai", "p18", "#F2C230", "Blue-rose printed skirt with a scarlet rose-appliqué top; a flower-fresh Holi pick.", "New"),
    P(19, "Meenakshi Oonjal Set",   "Pattu Pavadai", "p19", "#C2185B", "Rose Kanchi skirt with a deep-magenta velvet-touch top and a woven side-drape.", None),
    P(20, "Mullai Poo Set",         "Pattu Pavadai", "p20", "#C2185B", "Emerald Kanchi blouse with mint-green skirt; silver-border hamsa woven hem.", None),
    P(21, "Peacock Teal Pavadai",   "Pattu Pavadai", "p21", "#2BB5A0", "Deep-purple top, teal checked skirt, scallop hem — jewel tones for the win.", None),
    P(22, "Anthuri Velvet Set",     "Pattu Pavadai", "p22", "#3E1C3C", "Plum silk blouse with a taupe-gold woven skirt; muted, grown-up, and rare.", None),
    P(23, "Rani Pink Silk Set",     "Pattu Pavadai", "p23", "#F06292", "Silk gown with a rani-pink drape-dupatta, beaded belt, and a soft satin flare.", None),
    P(24, "Thamaraik Kili Set",     "Pattu Pavadai", "p24", "#D95F13", "Pumpkin-orange Kanchi skirt with a brown velvet blouse; deepavali-ready.", None),
    P(25, "Vaigai Silk Set",        "Pattu Pavadai", "p25", "#9CB4CC", "Sky-blue Kanchi skirt with a navy brocade blouse; a calm-sky festive look.", None, [C("Sky Navy", "#9CB4CC", "p25"), C("Teal Rose", "#C2185B", "p13")]),
    P(26, "Mayil Kan Silks Set",    "Pattu Pavadai", "p26", "#C2185B", "Magenta rose-print skirts with ruffle tops — one for her, one for her cousin.", "Twin Set"),
    P(27, "Anjali Silk Set",        "Pattu Pavadai", "p27", "#5B2D8E", "Purple Kanchi blouse with a green-border pattu skirt; classic gem tones.", None),
    P(28, "Arasi Kottadi Set",      "Pattu Pavadai", "p28", "#7A2E8E", "Blue-rose printed skirt with a fuchsia peplum top and a tie-back bow.", None),
    P(29, "Nalli Bhagalpuri Set",   "Bhagalpuri Set","p29", "#C9163F", "Bhagalpuri red-orange silk set with a woven border; rich, light, and breathable.", None),
    P(30, "Lotus Trail Pavadai",    "Pattu Pavadai", "p30", "#4A7FA5", "Blue-grey silk skirt with a pink lotus-trail blouse; petal-pink bloom up top.", None),
    P(31, "Pachai Veshthi Set",     "Pattu Pavadai", "p31", "#8DB600", "Parrot-green veshthi with a bottle-green Kanchi top and peacock side-tie.", None),
    P(32, "Kachhi Kundan Set",      "Pattu Pavadai", "p32", "#D95F13", "Rust-orange blouse with a gold-zari kachhi-kundan neckline and a burnt-sienna skirt.", None),
    P(33, "Pattu Langa Pastel Set", "Pattu Pavadai", "p33", "#E8DCC8", "Beige-gold silk top with a grey-gold Kanchi skirt; an heirloom pastel.", None),
    P(34, "Thamarai Silks Set",     "Pattu Pavadai", "p34", "#8E1F4B", "Wine-red pattu skirt, gold zari border, bottle-green Kanchi blouse, and a jhumka tag.", None),
    P(35, "Chinna Ponnu Gown",      "Silk Gown",     "p35", "#F06292", "Ivory silk gown with lotus-print skirt and a rani-pink neck-scarf; garden-party ready.", None),
    P(36, "Sindhoori Kanchi Set",   "Pattu Pavadai", "p36", "#C9163F", "Sindhoori-red Kanchi skirt with a majanta-gold blouse and gold border fall.", None),
    P(37, "Maragatha Green Set",    "Pattu Pavadai", "p37", "#3E7C1F", "Emerald blouse with an olive-silver Kanchi skirt; maragatha-green festive energy.", None),
    P(38, "Nalli Silks Party Set",  "Partywear Set", "p38", "#3E1C3C", "Deep-purple silk skirt with woven floral vines and a plum blouse.", None),
    P(39, "Meenakshi Party Set",    "Partywear Set", "p39", "#C2185B", "Rani party set — ruffle top with a zari-bordered skirt.", None),
    P(40, "Kutchi Emb Set",         "Pattu Pavadai", "p40", "#F06292", "Kuttchi bird-print silk skirt with a mirror-work orange blouse; playful pastel silk.", None),
    P(41, "Vaiyali Silk Set",       "Pattu Pavadai", "p41", "#DF6D1E", "Pista-green blouse with a lotus-pink Kanchi skirt; a pista-pink garden pairing.", None),
    P(42, "Nizam Collection Set",   "Pattu Pavadai", "p42", "#2E8B57", "Red-orange skirt, gold border, and a gamthi-work blouse; a Nizam-era colour story.", "Bestseller"),
    P(43, "Vaiyali Designer Set",   "Designer Set",  "p43", "#E91E63", "Blue-teal Kanchi skirt with a majanta-gold blouse; a designer colour block.", None),
    P(44, "Radha Designer Set",     "Designer Set",  "p44", "#F06292", "Orange ruched bodice over a blue silk skirt; modern draping, classic soul.", None),
    P(45, "Karishma/Kanha Silk Set","Pattu Pavadai", "p45", "#1E50A2", "Royal-blue Kanchi skirt with a mustard-gold border; Kanha-blue festive pick.", None),
    P(46, "Peacock Blue Fancy Set", "Fancy Langa",   "p46", "#1E50A2", "Peacock-blue printed langa with an orange frill blouse; a fancy-dress ready set.", None),
    P(47, "Kanchi Pattu Pavadai",   "Kanchi Pattu",  "p47", "#7A2E8E", "Half-saree-style pattu pavadai with a purple-gold skirt and gold-border fall.", None),
    P(48, "Radha Kanchi Set",       "Kanchi Pattu",  "p48", "#5B2D8E", "Purple-gold tissue skirt with a maroon-gold blouse; a Kanchi-purple heirloom.", None),
    P(49, "Sakura Pearl Set",       "Silk Gown",     "p49", "#F2C230", "Lemon top with a sea-blue floral skirt and pearl drops; a pastel sakura story.", None),
    P(50, "Sakura Pearl Gown",      "Silk Gown",     "p50", "#C9A227", "Green-gold blouse with a lemon-yellow silk skirt and silver fall — Lemon-paatu fresh.", None),
    P(51, "Noon Silk Set",          "Silk Gown",     "p51", "#2BB5A0", "Sun-beam yellow top with an orange-gold Kanchi skirt; bright as noon.", None),
    P(52, "Sri Kanchan Silks Set",  "Kanchi Pattu",  "p52", "#C2185B", "Purple velvet-touch blouse over a purple-gold Kanchi skirt; a deep-purple statement.", None),
    P(53, "Maroon Party Gown",      "Party Gown",    "p53", "#8E1F4B", "Maroon silk party gown with gold zari work; 3-12 yr size chart shown.", None),
    P(54, "Neon & Navy Kali Set",   "Kali Kutchi",   "p54", "#5B2D8E", "Navy top with neon-pink kutchi-work kali skirt; festive folk-chic.", None),
    P(55, "Roop Kathak Set",        "Kali Kutchi",   "p55", "#C2185B", "Magenta polka-dot blouse over an ivory-red Kanchi skirt; Roop-kathak energy.", None),
    P(56, "Sri Kanchan Frocks Set", "Silk Frocks",   "p56", "#2795B8", "Navy-blue silk frock set with a tissue drape; infant-ready festive set.", None),
    P(57, "Sri Kanchan Silk Set",   "Silk Frocks",   "p57", "#E91E63", "Rose-pink silk frock with silver buttis and a neck-bow; grown-girl grace.", None),
    P(58, "Valentina Lilac Set",    "Party Gown",    "p58", "#7A2E8E", "Black silk skirt with pink lotus kurti and tassels; Valentina-lilac story.", None),
    P(59, "Sri Kanchan Party Set",  "Party Gown",    "p59", "#1E50A2", "Magenta-gold party langa with a woven jacket; bold and ballistic.", None),
    P(60, "Sai Meenakshi Silk Set", "Pattu Pavadai", "p60", "#F2C230", "Mustard-gold temple-top with a purple-gold Kanchi skirt; little-po' twist.", None),
    P(61, "Kanchi Pattu Langa",     "Kanchi Pattu",  "p61", "#C2185B", "Rani-red Kanchi with a white dotted skirt and red-gold border; classic Kanchi look.", None, [C("Malligai Green", "#2C6E49", "malligai_l"), C("Malligai Wine", "#7A2440", "malligai_r")]),
    P(62, "Saree Style Pattu Langa",  "Kanchi Pattu", "p62", "#2C6E49", "Rani-pink blouse with an ivory-gold saree-print skirt; miniature-saree magic.", None),
    P(63, "RadhaKalyanam Silk Set", "Pattu Pavadai", "p63", "#C2185B", "Rani-pink blouse with a mustard-gold pattu skirt; Radha-kalyanam festive set.", None),
    P(64, "Pink Chanderi Set",      "Chanderi Set",  "p64", "#F2C230", "Rani-pink top with a sunset-orange skirt; Chanderi-light and twirl-tested.", None),
    P(65, "Pure Zari Pattu Pavadai","Chanderi Set",  "p65", "#2795B8", "Red Kanchi zari skirt with a rani blouse; pure-zari festive heirloom.", None),
    P(66, "Mayil Kanchi Border",    "Kanchi Pattu",  "p66", "#5B2D8E", "Purple-gold Kanchi pavadai with a green-blouse; mayil-chakram border.", None),
    P(67, "Peacock & Mint Frock",   "Silk Frocks",   "p67", "#2BB5A0", "Peacock-teal silk frock with a mint woven skirt; hairband included.", None),
]

PRODUCTS_JSON = json.dumps(PRODUCTS, ensure_ascii=False)
IMGS_JSON_S = json.dumps(IMGS_JSON)
LQIP_JSON_S = json.dumps(LQIP_JSON)

# ------------------------------------------------------------------ html --
HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Ankita Sharma Collection \u00B7 Kids Fashion Store \u2014 \u20B9550 Flat</title>
<meta name="description" content="Ankita Sharma Collection — party frocks, pattu pavadai sets & kids fashion. \u20B9550 flat with combo savings up to 10 dresses. All-India delivery, prepaid only. Order on WhatsApp.">
<meta name="theme-color" content="#111111">
<link rel="icon" type="image/png" href="data:image/png;base64,__LOGO_FAV__">
<style>
__FONTS__
__CSS__
</style>
</head>
<body>

<div class="boot" id="boot" aria-hidden="true">
  <img class="boot-logo" src="data:image/png;base64,__LOGO_FAV__" alt="">
  <div class="boot-name">Ankita Sharma <i>Collection</i></div>
  <span class="boot-spin"></span>
</div>
<a class="skip-link" href="#grid">Skip to dresses</a>

<header class="topbar" id="top">
  <a class="brand" href="#top" id="brandLink" aria-label="Ankita Sharma Collection — back to top">
    <img class="brand-logo" src="data:image/png;base64,__LOGO__" alt="Ankita Sharma Collection logo">
    <span class="brand-txt">
      <span class="brand-name">Ankita Sharma <i>Collection</i></span>
      <span class="brand-tag">Kids Fashion Store</span>
    </span>
  </a>
  <span class="ver-badge" aria-hidden="true">v2.3</span>
  <div class="search-wrap">
    <svg class="search-ico" viewBox="0 0 24 24" fill="none" stroke-width="2.2" stroke-linecap="round"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>
    <input id="searchInput" class="search-input" type="search" placeholder="Search dresses" autocomplete="off" aria-label="Search dresses">
  </div>
  <a class="ig-link" href="https://www.instagram.com/kc_kids_collection" target="_blank" rel="noopener" aria-label="Ankita Sharma Collection on Instagram" title="@kc_kids_collection on Instagram">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5"/><circle cx="12" cy="12" r="4.3"/><circle cx="17.4" cy="6.6" r="1.15" fill="currentColor" stroke="none"/></svg>
  </a>
  <button class="menu-btn" id="menuBtn" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="navDrawer">
    <span></span><span></span><span></span>
  </button>
</header>

<div class="delivery-strip" role="note">
  <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1.5 6h12v10h-12z"/><path d="M13.5 9h4l3 3v4h-7"/><circle cx="6" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/></svg>
  <b>All India Delivery Available</b><span class="ds-sep">&bull;</span><span>Prepaid orders only &mdash; no Cash on Delivery</span>
</div>

<section class="hero">
  <div class="bflies" aria-hidden="true">
    <svg class="bfly b1" viewBox="0 0 64 52"><defs><linearGradient id="bfg1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F07AB0"/><stop offset="1" stop-color="#E85A9B"/></linearGradient></defs><g class="wing" fill="url(#bfg1)"><path d="M31 26C22 8 4 4 4 16c0 9 12 16 25 14z"/><path d="M31 28c-10-2-22 2-20 11 1.8 8 14 6 21-5z" opacity='.82'/></g><g class="wing" fill="url(#bfg1)"><path d="M33 26C42 8 60 4 60 16c0 9-12 16-25 14z"/><path d="M33 28c10-2 22 2 20 11-1.8 8-14 6-21-5z" opacity='.82'/></g><rect x="30.6" y="13" width="2.8" height="25" rx="1.4" fill="#8A5A2B"/></svg>
    <svg class="bfly b2" viewBox="0 0 64 52"><defs><linearGradient id="bfg2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E85A9B"/><stop offset="1" stop-color="#F6A8CD"/></linearGradient></defs><g class="wing" fill="url(#bfg2)"><path d="M31 26C22 8 4 4 4 16c0 9 12 16 25 14z"/><path d="M31 28c-10-2-22 2-20 11 1.8 8 14 6 21-5z" opacity='.82'/></g><g class="wing" fill="url(#bfg2)"><path d="M33 26C42 8 60 4 60 16c0 9-12 16-25 14z"/><path d="M33 28c10-2 22 2 20 11-1.8 8-14 6-21-5z" opacity='.82'/></g><rect x="30.6" y="13" width="2.8" height="25" rx="1.4" fill="#8A5A2B"/></svg>
  </div>
  <div class="hero-eyebrow">Flat \u20B9550 &middot; Every Single Dress</div>
  <h1 class="hero-title">
    <span class="shimmer">Dress Up<br><small>Little Happiness</small></span>
  </h1>
  <p class="hero-sub">Party frocks, twirl-ready pattu pavadais &amp; festive sets for little girls &mdash; premium finish, one honest price.</p>
  <div class="hero-price"><span class="rs">\u20B9550</span><span class="flat">Flat &middot; no MRP games</span></div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track" id="marqueeTrack"></div></div>

<div class="jump-row" aria-label="Quick links">
  <a href="#combos">&nbsp;Combo Prices</a>
  <a href="#delivery">Delivery &amp; No-COD Info</a>
  <a href="#visit">Store Address</a>
  <a href="#/privacy">Privacy Policy</a>
</div>

<div class="sticky-bar">
  <div class="chips" id="chips"></div>
</div>

<main class="grid" id="grid" aria-label="Dress collection">__CARDS__<div class="no-results" id="noRes" style="display:none"><div class="big">No dresses found</div>Try a different colour or name.</div></main>

<section class="combo" id="combos">
  <div class="combo-kicker">Combo Savings</div>
  <h2 class="combo-title">Buy more, pay less</h2>
  <p class="combo-sub">Mix any dresses &mdash; colours, styles, sizes. Your combo price applies to the whole order at checkout.</p>
  <div class="combo-table" id="comboTable" role="table" aria-label="Combo pricing — buy more, save more">
    <div class="combo-head-row" role="row"><span role="columnheader">Quantity</span><span class="cr-c" role="columnheader">You pay</span><span class="cr-c" role="columnheader">You save</span></div>
  </div>
</section>

<section class="delivery-info" id="delivery">
  <div class="visit-kicker">Delivery &amp; Orders</div>
  <h2 class="combo-title">How ordering works</h2>
  <div class="faq-card">
    <div class="faq"><b>How do I order?</b><span>Tap a dress, pick a size and quantity, then <b>Add to Cart</b> and <b>Checkout on WhatsApp</b> &mdash; we confirm everything with you in chat.</span></div>
    <div class="faq"><b>Do you offer Cash on Delivery?</b><span>No &mdash; strictly prepaid. Payment details are shared on WhatsApp before dispatch; we never ask for COD.</span></div>
    <div class="faq"><b>Where do you deliver?</b><span>All India. Orders dispatch in 2&ndash;3 days.</span></div>
    <div class="faq"><b>What sizes are available?</b><span>Every dress comes in XS&ndash;XXL &mdash; see the Size Chart on any product page.</span></div>
    <div class="faq"><b>Combo pricing?</b><span>Buy 2 or more and combo rates apply automatically &mdash; see the table above.</span></div>
  </div>
</section>

<section class="visit" id="visit">
  <div class="visit-kicker">Visit Our Store</div>
  <h2 class="combo-title">Find us in Hyderabad</h2>
  <div class="visit-card">
    <div class="visit-addr">Nampally Station Rd, Chirag Ali Lane, Abids,<br>Hyderabad, Telangana 500001</div>
    <div class="visit-actions">
      <a class="btn btn-wine" target="_blank" rel="noopener" href="https://maps.app.goo.gl/7aJ8KQNhZ599H7ZA6"><svg class="btn-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M12 21s-6.5-5.3-6.5-10a6.5 6.5 0 0 1 13 0C18.5 15.7 12 21 12 21z"/><circle cx="12" cy="10.6" r="2.3"/></svg>Get Directions</a>
      <a class="btn btn-gold" target="_blank" rel="noopener" href="https://wa.me/916375101619"><svg class="btn-ico" viewBox="0 0 24 24" fill="#FFFFFF"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 13.9c-.2.6-1.2 1.2-1.7 1.2-.4.1-1 .1-1.6-.1-.4-.1-.9-.3-1.5-.5-2.6-1.1-4.3-3.7-4.4-3.9-.1-.2-1.1-1.4-1.1-2.7s.7-1.9.9-2.2c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.4s.8 1.9.8 2c.1.1.1.3 0 .5-.3.6-.7.9-.5 1.2.7 1.2 1.6 2 2.8 2.6.3.2.5.1.7-.1l.9-1.1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.3.1.1.1.6-.3 1.8z"/></svg>WhatsApp Us</a>
    </div>
    <div class="visit-meta">Store hours &amp; live stock &mdash; just message us &middot; <a href="https://www.instagram.com/kc_kids_collection" target="_blank" rel="noopener">@kc_kids_collection</a></div>
    <div class="visit-note">No Cash on Delivery &mdash; prepaid orders only &middot; All-India delivery</div>
  </div>
</section>

<footer class="footer">
  <a href="#top" class="footer-logo-link" aria-label="Ankita Sharma Collection — back to top"><img class="footer-logo" src="data:image/png;base64,__LOGO__" alt=""></a>
  <div class="fbrand">Ankita Sharma Collection</div>
  <div class="ftag">Dress Up Little Happiness &hearts;</div>
  <div class="frow"><span class="fgold">__NP__ styles</span> &middot; one flat price &middot; ages 2&ndash;11</div>
  <div class="frow">All-India delivery &middot; dispatched in 2&ndash;3 days &middot; prepaid only</div>
  <nav class="fnav" aria-label="Footer">
    <a href="#top">Home</a><span aria-hidden="true">&middot;</span>
    <a href="#combos">Combo Offers</a><span aria-hidden="true">&middot;</span>
    <a href="#delivery">Delivery Info</a><span aria-hidden="true">&middot;</span>
    <a href="#visit">Contact</a><span aria-hidden="true">&middot;</span>
    <a href="#/privacy">Privacy Policy</a>
  </nav>
  <a class="ig-pill" href="https://www.instagram.com/kc_kids_collection" target="_blank" rel="noopener">
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"><rect x="2.5" y="2.5" width="19" height="19" rx="5.5"/><circle cx="12" cy="12" r="4.3"/><circle cx="17.4" cy="6.6" r="1.15" fill="currentColor" stroke="none"/></svg>
    Follow us on Instagram &middot; <span>@kc_kids_collection</span>
  </a>
  <div class="fcopy">&copy; 2026 Ankita Sharma Collection &middot; all rights reserved &middot; v2.3</div>
</footer>

<!-- floating cart bar -->
<button class="cartbar" id="cartbar" aria-label="Open basket">
  <span class="cb-count" id="cbCount">0</span>
  <span class="cb-txt">
    <span class="cb-items" id="cbItems">0 dresses</span><br>
    <span class="cb-total" id="cbTotal">\u20B90</span>
  </span>
  <span class="cb-go">Checkout <svg viewBox="0 0 24 24"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 13.9c-.2.6-1.2 1.2-1.7 1.2-.4.1-1 .1-1.6-.1-.4-.1-.9-.3-1.5-.5-2.6-1.1-4.3-3.7-4.4-3.9-.1-.2-1.1-1.4-1.1-2.7s.7-1.9.9-2.2c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.4s.8 1.9.8 2c.1.1.1.3 0 .5-.3.6-.7.9-.5 1.2.7 1.2 1.6 2 2.8 2.6.3.2.5.1.7-.1l.9-1.1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.3.1.1.1.6-.3 1.8z"/></svg></span>
</button>

<!-- product sheet -->
<div class="sheet-layer" id="sheetLayer" aria-hidden="true">
  <div class="scrim" id="sheetScrim"></div>
  <div class="sheet" id="sheet" role="dialog" aria-modal="true" aria-labelledby="pdName">
    <div class="sheet-grab" id="sheetGrab"><span></span></div>
    <button class="sheet-close" id="sheetClose" aria-label="Close">&#10005;</button>
    <div class="sheet-scroll" id="sheetScroll">
      <div class="car" id="car" role="group" aria-roledescription="carousel" aria-label="Product photos">
        <div class="car-track" id="carTrack"></div>
        <button class="car-nav prev" id="carPrev" aria-label="Previous image">&#8249;</button>
        <button class="car-nav next" id="carNext" aria-label="Next image">&#8250;</button>
        <span class="car-tag" id="carTag"></span>
        <div class="car-dots" id="carDots"></div>
      </div>
      <div class="pd-info">
      <div class="pd-head">
        <div>
          <h2 class="pd-name" id="pdName"></h2>
          <div class="pd-type" id="pdType"></div>
        </div>
        <div class="pd-price">
          <span class="rs">\u20B9550</span>
          <span class="mrp">\u20B91,200</span>
          <span class="save" id="pdSave">SAVE \u20B9650</span>
        </div>
      </div>
      <p class="pd-desc" id="pdDesc"></p>
      <div class="pd-label" id="swLabel"><span>Colour</span><b id="swName"></b></div>
      <div class="swatch-row" id="pdSwatches" role="group" aria-label="Colour options"></div>
      <div class="pd-label"><span>Select Size</span><button class="size-link" id="sizeChartBtn" type="button"><svg viewBox="0 0 24 24" fill="none" stroke-width="2" stroke-linecap="round"><path d="M3 8h18v8H3z"/><path d="M7 8v3M11 8v4M15 8v3M19 8v4"/></svg>Size Chart</button></div>
      <div class="size-row" id="sizeRow"></div>
      <div class="pd-label"><span>Quantity</span></div>
      <div class="qty-row">
        <div class="qty" role="group" aria-label="Quantity">
          <button id="qtyMinus" aria-label="Decrease quantity">&#8722;</button>
          <b id="pdQty" aria-live="polite">1</b>
          <button id="qtyPlus" aria-label="Increase quantity">+</button>
        </div>
      </div>
      <div class="pd-cta">
        <button class="btn btn-gold" id="btnAdd">Add to Cart &middot; <span id="btnAddTotal">\u20B9550</span>
          <span class="check"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12.5l5.2 5.2L20 6.5"/></svg></span>
        </button>
        <button class="btn btn-wine" id="btnWa">
          <svg class="btn-ico" viewBox="0 0 24 24" fill="#4BC855"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 13.9c-.2.6-1.2 1.2-1.7 1.2-.4.1-1 .1-1.6-.1-.4-.1-.9-.3-1.5-.5-2.6-1.1-4.3-3.7-4.4-3.9-.1-.2-1.1-1.4-1.1-2.7s.7-1.9.9-2.2c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.4s.8 1.9.8 2c.1.1.1.3 0 .5-.3.6-.7.9-.5 1.2.7 1.2 1.6 2 2.8 2.6.3.2.5.1.7-.1l.9-1.1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.3.1.1.1.6-.3 1.8z"/></svg>
          Order on WhatsApp
        </button>
      </div>
      <div class="cod-note">
        <svg viewBox="0 0 24 24" fill="none" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l7 3v5c0 4.4-2.9 7.6-7 9-4.1-1.4-7-4.6-7-9V6z"/><path d="M9.5 11.5l2 2 3.5-3.5"/></svg>
        <span><b>No Cash on Delivery</b> &mdash; prepaid only, pay on WhatsApp &middot; <b>All-India delivery</b></span>
      </div>
      <div class="trust">
        <span>\u2726 Soft lining</span><span>\u2726 2&ndash;3 day dispatch</span><span>\u2726 Ages 2&ndash;11</span><span>\u2726 Exchange on size</span>
      </div>
      <div class="pd-details">
        <div class="pd-details-title">Product Details</div>
        <div class="spec-grid">
          <div class="spec"><b>Size Tip</b><span>Buy a size up for growing girls</span></div>
          <div class="spec"><b>Neckline</b><span>Round neck</span></div>
          <div class="spec"><b>Package Contains</b><span>1 dress</span></div>
          <div class="spec"><b>Wash Care</b><span>First wash dry-clean</span></div>
          <div class="spec"><b>Fabric Composition</b><span>Poly-silk (handloom finish)</span></div>
        </div>
        <button class="more-details" id="moreDetails" type="button" aria-expanded="false" aria-controls="morePanel">More Details
          <svg viewBox="0 0 24 24" fill="none" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>
        </button>
        <div class="more-panel" id="morePanel">
          <div class="more-row"><b>Country of Origin</b><span>India</span></div>
          <div class="more-row"><b>Marketed by</b><span>Ankita Sharma Collection &middot; Dress Up Little Happiness</span></div>
          <div class="more-row"><b>Dispatch</b><span>Ships in 2&ndash;3 days &middot; all-India delivery</span></div>
          <div class="more-row"><b>Age Group</b><span>2&ndash;11 years &middot; exchange available on size</span></div>
        </div>
      </div>
      </div>
    </div>
  </div>
</div>

<!-- cart sheet / drawer -->
<div class="cart-layer" id="cartLayer" aria-hidden="true">
  <div class="scrim" id="cartScrim"></div>
  <div class="cart" role="dialog" aria-modal="true" aria-labelledby="cartTitle">
    <div class="cart-head">
      <div>
        <div class="cart-title" id="cartTitle">Your Basket</div>
        <div class="cart-count" id="cartCountLbl"></div>
      </div>
      <button class="cart-x" id="cartX" aria-label="Close cart">&#10005;</button>
    </div>
    <div class="cart-items" id="cartItems" aria-live="polite"></div>
    <div class="cart-foot" id="cartFoot">
      <div class="cart-save" id="cartSave"></div>
      <div class="cart-total"><span class="lbl">Order total</span><span class="val" id="cartTotal">\u20B90</span></div>
      <button class="btn btn-gold" id="btnCheckout">
        <svg class="btn-ico" viewBox="0 0 24 24" fill="#FFFFFF"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm5.3 13.9c-.2.6-1.2 1.2-1.7 1.2-.4.1-1 .1-1.6-.1-.4-.1-.9-.3-1.5-.5-2.6-1.1-4.3-3.7-4.4-3.9-.1-.2-1.1-1.4-1.1-2.7s.7-1.9.9-2.2c.2-.3.5-.3.7-.3h.5c.2 0 .4 0 .6.4s.8 1.9.8 2c.1.1.1.3 0 .5-.3.6-.7.9-.5 1.2.7 1.2 1.6 2 2.8 2.6.3.2.5.1.7-.1l.9-1.1c.2-.3.4-.2.7-.1l2 1c.3.1.5.2.5.3.1.1.1.6-.3 1.8z"/></svg>
        Checkout on WhatsApp
      </button>
      <div class="cart-note">Prepaid only &mdash; no Cash on Delivery &middot; All-India delivery &middot; confirm sizes on WhatsApp \u2726</div>
    </div>
  </div>
</div>

<div class="modal-layer" id="sizeLayer" aria-hidden="true">
  <div class="scrim" id="sizeScrim"></div>
  <div class="modal" role="dialog" aria-modal="true" aria-label="Size chart">
    <div class="modal-head">
      <div class="modal-title">Size Chart</div>
      <button class="cart-x" id="sizeX" aria-label="Close size chart">&#10005;</button>
    </div>
    <div class="modal-body">
      <table class="size-table">
        <thead><tr><th>Size</th><th>Bust</th><th>Waist</th><th>Hips</th><th>Length</th></tr></thead>
        <tbody>
          <tr><td>XS</td><td>22&quot;</td><td>21&quot;</td><td>23&quot;</td><td>23&quot;</td></tr>
          <tr><td>S</td><td>24&quot;</td><td>22&quot;</td><td>25&quot;</td><td>26&quot;</td></tr>
          <tr><td>M</td><td>26&quot;</td><td>24&quot;</td><td>27&quot;</td><td>29&quot;</td></tr>
          <tr><td>L</td><td>28&quot;</td><td>25&quot;</td><td>29&quot;</td><td>32&quot;</td></tr>
          <tr><td>XL</td><td>30&quot;</td><td>27&quot;</td><td>31&quot;</td><td>35&quot;</td></tr>
          <tr><td>XXL</td><td>32&quot;</td><td>28&quot;</td><td>33&quot;</td><td>38&quot;</td></tr>
        </tbody>
      </table>
      <p class="size-note">Approximate garment measurements in inches (kids 2&ndash;11 yrs). Between sizes? Buy one size up.</p>
    </div>
  </div>
</div>

<!-- mobile nav drawer -->
<div class="nav-layer" id="navLayer" aria-hidden="true">
  <div class="scrim" id="navScrim"></div>
  <nav class="nav-drawer" id="navDrawer" role="dialog" aria-modal="true" aria-label="Site menu">
    <div class="nav-head">
      <div class="nav-title">Menu</div>
      <button class="cart-x" id="navX" aria-label="Close menu">&#10005;</button>
    </div>
    <a class="nav-link" href="#top">Home <span class="narr" aria-hidden="true">top</span></a>
    <a class="nav-link" href="#grid">Shop All Dresses</a>
    <button class="nav-link" id="navSize" type="button">Size Chart <span class="narr" aria-hidden="true">XS&ndash;XXL</span></button>
    <a class="nav-link" href="#combos">Combo Offers</a>
    <a class="nav-link" href="#delivery">Delivery Info</a>
    <a class="nav-link" href="#visit">Contact / Store</a>
    <a class="nav-link" href="#/privacy">Privacy Policy</a>
    <button class="nav-link fx-toggle" id="fxToggle" type="button" role="switch" aria-checked="true" aria-label="Turn animations on or off">Animations <span class="fx-state" id="fxState">ON</span></button>
    <div class="nav-foot">
      <a href="https://wa.me/916375101619" target="_blank" rel="noopener">WhatsApp &middot; +91 63751 01619</a>
      <a href="https://www.instagram.com/kc_kids_collection" target="_blank" rel="noopener">Instagram &middot; @kc_kids_collection</a>
      <span>Prepaid only &mdash; no COD &middot; All-India delivery</span>
    </div>
  </nav>
</div>

<!-- privacy policy view -->
<div class="pageview" id="pagePrivacy" hidden>
  <div class="page-inner pp">
    <button class="page-back" id="privacyBack" type="button">&larr; Back to shop</button>
    <h1>Privacy Policy</h1>
    <p>We're a small family-run kids' fashion store. This policy explains, in plain words, what we do (and don't do) with your information.</p>
    <h2>What we collect</h2>
    <p>Only what's needed to deliver your order:</p>
    <ul>
      <li><b>Name</b> &mdash; so we know who the order belongs to.</li>
      <li><b>Delivery address</b> &mdash; so the parcel reaches you.</li>
      <li><b>Phone / WhatsApp number</b> &mdash; so we can confirm your order and share payment details.</li>
    </ul>
    <h2>How we use it</h2>
    <p>Your details are used only to confirm orders, arrange delivery, and help with size exchanges. We may message you on WhatsApp about your order &mdash; never for spam.</p>
    <h2>What we never do</h2>
    <p>We do not sell, rent, or share your personal information with any third party for marketing. Delivery partners receive only the address details required to ship your parcel.</p>
    <h2>Cookies &amp; local storage</h2>
    <p>This site doesn't use tracking cookies. Your basket is saved in your own browser's local storage so it's there when you come back &mdash; it never leaves your device.</p>
    <h2>Payments</h2>
    <p>Orders are prepaid via UPI or bank transfer, arranged directly on WhatsApp. We never see or store your card or UPI credentials.</p>
    <h2>Questions?</h2>
    <p>Message us any time on <a href="https://wa.me/916375101619" target="_blank" rel="noopener">WhatsApp (+91 63751 01619)</a> or Instagram <a href="https://www.instagram.com/kc_kids_collection" target="_blank" rel="noopener">@kc_kids_collection</a>, or visit the store in Abids, Hyderabad.</p>
    <p class="pp-upd">Last updated: September 2026.</p>
  </div>
</div>

<!-- 404 view -->
<div class="pageview" id="page404" hidden>
  <div class="page-inner err404">
    <div class="err-ico" aria-hidden="true">
      <svg viewBox="0 0 64 64" fill="none"><path d="M32 8l9 11-4.5 33a4.5 4.5 0 0 1-9 0L23 19z" fill="#F9DCEA" stroke="#E85A9B" stroke-width="2.4" stroke-linejoin="round"/><path d="M23 19c2.5 4.5 15.5 4.5 18 0" stroke="#D4A84F" stroke-width="2.4" stroke-linecap="round"/><circle cx="32" cy="6" r="2.8" fill="none" stroke="#D4A84F" stroke-width="2.2"/></svg>
    </div>
    <h1>This page took a wrong turn</h1>
    <p>Even our prettiest frocks get lost sometimes. Let's get you back to the good stuff.</p>
    <button class="btn btn-gold" id="errHome" type="button">Back to the shop</button>
  </div>
</div>

<div class="toast" id="toast" role="status" aria-live="polite"></div>

<script>
window.CHINNARI_PRODUCTS = __PRODUCTS__;
window.CHINNARI_IMGS = __IMGS__;
window.CHINNARI_LQIP = __LQIP__;
</script>
<script>
__JS__
</script>
</body>
</html>
"""

LOGO_B64 = base64.b64encode(open(os.path.join(ROOT, "tools", "brand", "logo.png"), "rb").read()).decode()
LOGO_FAV_B64 = base64.b64encode(open(os.path.join(ROOT, "tools", "brand", "logo_fav.png"), "rb").read()).decode()

html = (HTML
        .replace("__LOGO_FAV__", LOGO_FAV_B64)
        .replace("__LOGO__", LOGO_B64)
        .replace("__FONTS__", FONTS_CSS)
        .replace("__CSS__", CSS)
        .replace("__PRODUCTS__", PRODUCTS_JSON)
        .replace("__IMGS__", IMGS_JSON_S)
        .replace("__LQIP__", LQIP_JSON_S)
        .replace("__JS__", JS)
        .replace("__CARDS__", "")
        .replace("__NP__", str(len(PRODUCTS))))

out = os.path.join(ROOT, "ankita-sharma-collection.html")
open(out, "w", encoding="utf-8").write(html)
size = os.path.getsize(out)
print(f"ankita-sharma-collection.html  ->  {size/1024/1024:.2f} MB  ({len(PRODUCTS)} products, {len(IMGS_JSON)} full imgs)  [v2.3]")
