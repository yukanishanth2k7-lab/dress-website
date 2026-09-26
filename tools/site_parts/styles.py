# -*- coding: utf-8 -*-
"""Kc Collection stylesheet — cream/gold/rose-pink palette, mobile-first, reduced-motion aware."""

CSS = r"""
/* ============================ DESIGN TOKENS ============================ */
:root {
  --cream: #FFF9F5;          /* page background      */
  --ink-0: #111111;          /* black — header, text */
  --text-0: #241D1B;         /* primary text         */
  --text-1: #6B5F5C;         /* secondary text       */
  --text-2: #9C8E8A;         /* faint text           */
  --gold: #D4A84F;           /* brand gold           */
  --gold-hi: #E4BC6B;
  --gold-dim: #B08F45;
  --pink: #E85A9B;           /* primary CTA          */
  --pink-d: #C94482;         /* hover rose           */
  --pink-soft: #F9DCEA;
  --card: #FFFFFF;
  --card-br: #F0E5E8;
  --serif: 'Cormorant Garamond', 'Times New Roman', serif;
  --sans: 'Manrope', system-ui, sans-serif;
  --rad: 18px;
  --sheet-rad: 26px;
  --shadow-1: 0 2px 10px rgba(122, 58, 82, .08);
  --shadow-2: 0 18px 44px rgba(122, 58, 82, .16);
  --pink-grad: linear-gradient(120deg, #E85A9B, #F07AB0 55%, #E85A9B);
}

* { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
html { scroll-behavior: smooth; }
body {
  background:
    radial-gradient(1000px 620px at 88% -6%, rgba(232, 90, 155, .07), transparent 60%),
    radial-gradient(900px 600px at -10% 28%, rgba(212, 168, 79, .08), transparent 55%),
    radial-gradient(820px 700px at 110% 86%, rgba(232, 90, 155, .05), transparent 60%),
    var(--cream);
  color: var(--text-0);
  font-family: var(--sans);
  font-size: 15px;
  line-height: 1.55;
  min-height: 100dvh;
  overflow-x: hidden;
}
img { display: block; max-width: 100%; }
button { font: inherit; color: inherit; background: none; border: 0; cursor: pointer; }
::selection { background: var(--pink); color: #fff; }

/* delicate paisley watermark */
body::before {
  content: ''; position: fixed; inset: 0; z-index: 0; pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='340' height='340' viewBox='0 0 340 340'%3E%3Cg fill='none' stroke='%23D4A84F' stroke-width='1'%3E%3Cpath d='M60 20c34 0 52 22 52 46 0 30-24 44-44 44-24 0-40-16-40-36 0-18 14-30 30-30 14 0 24 10 24 22 0 10-8 18-18 18'/%3E%3Ccircle cx='60' cy='52' r='3'/%3E%3Cpath d='M250 200c34 0 52 22 52 46 0 30-24 44-44 44-24 0-40-16-40-36 0-18 14-30 30-30 14 0 24 10 24 22 0 10-8 18-18 18'/%3E%3Ccircle cx='250' cy='232' r='3'/%3E%3C/g%3E%3C/svg%3E");
  opacity: .06;
}

/* ============================== TYPOGRAPHY ============================= */
.serif-i { font-family: var(--serif); font-style: italic; font-weight: 600; }

/* ============================ LOADING SCREEN ============================ */
.boot {
  position: fixed; inset: 0; z-index: 400; display: flex; flex-direction: column;
  align-items: center; justify-content: center; gap: 14px; background: #FFF9F5;
  transition: opacity .35s ease, visibility .35s ease;
}
.boot-logo { width: 64px; height: 64px; border-radius: 50%; box-shadow: 0 0 0 2px rgba(212, 168, 79, .6); animation: bootIn .5s ease both; }
.boot-name { font-family: var(--serif); font-weight: 700; font-size: 18px; color: var(--text-0); }
.boot-name i { font-style: italic; color: var(--gold); }
.boot-spin { width: 22px; height: 22px; border-radius: 50%; border: 2.5px solid rgba(232, 90, 155, .25); border-top-color: var(--pink); animation: bootSpin .8s linear infinite; }
@keyframes bootIn { from { opacity: 0; transform: scale(.82); } }
@keyframes bootSpin { to { transform: rotate(360deg); } }
body.booted .boot { opacity: 0; visibility: hidden; pointer-events: none; }
/* failsafe: even if JS never runs, the boot screen can never hang */
body:not(.booted) .boot { animation: bootGone .5s ease 2.4s forwards; }
@keyframes bootGone { to { opacity: 0; visibility: hidden; } }

/* ============================== SKIP LINK =============================== */
.skip-link {
  position: fixed; top: -64px; left: 12px; z-index: 500;
  background: #111111; color: #FFF9F5; font: 700 13px var(--sans);
  padding: 12px 18px; border-radius: 12px; text-decoration: none; transition: top .2s ease;
}
.skip-link:focus { top: 12px; }

/* ================================ HEADER =============================== */
.topbar {
  position: sticky; top: 0; z-index: 60;
  display: flex; align-items: center; gap: 10px;
  padding: 10px 16px;
  background: rgba(17, 17, 17, .95);
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 1px 0 rgba(212, 168, 79, .28), 0 8px 26px rgba(17, 17, 17, .22);
}
.brand { display: flex; align-items: center; gap: 10px; flex: 1; min-width: 0; text-decoration: none; }
.brand-txt { display: flex; flex-direction: column; line-height: 1.05; min-width: 0; }
.brand-logo {
  width: 42px; height: 42px; border-radius: 50%; flex: 0 0 auto;
  box-shadow: 0 0 0 1.5px rgba(212, 168, 79, .75);
  animation: logoGlow 4.5s ease-in-out infinite;
  transition: transform .2s ease;
}
.brand:active .brand-logo { transform: scale(.92); }
.brand-name { font-family: var(--serif); font-style: normal; font-weight: 700; font-size: 15.5px; letter-spacing: .015em; color: #FFF9F5; white-space: nowrap; }
.brand-name i { font-style: italic; color: var(--gold); }
.brand-tag { font-size: 8.5px; letter-spacing: .3em; text-transform: uppercase; color: rgba(255, 249, 245, .8); white-space: nowrap; }

/* version badge (visible proof of the current build) */
.ver-badge {
  flex: 0 0 auto; font: 800 10px var(--sans); letter-spacing: .08em;
  color: #111111; background: var(--gold); border-radius: 999px; padding: 3px 8px;
}
@media (max-width: 560px) { .ver-badge { display: none; } }

/* hamburger (mobile) */
.menu-btn {
  display: grid; gap: 4.5px; place-content: center; width: 40px; height: 40px;
  border-radius: 12px; border: 1px solid rgba(212, 168, 79, .45); flex: 0 0 auto;
  transition: background .2s ease;
}
.menu-btn span { display: block; width: 17px; height: 1.8px; border-radius: 2px; background: #FFF9F5; transition: transform .28s ease, opacity .2s ease; }
.menu-btn:active { background: rgba(255, 249, 245, .08); }
body.nav-open .menu-btn span:nth-child(1) { transform: translateY(6.3px) rotate(45deg); }
body.nav-open .menu-btn span:nth-child(2) { opacity: 0; }
body.nav-open .menu-btn span:nth-child(3) { transform: translateY(-6.3px) rotate(-45deg); }
/* hamburger is available at every width now */

/* search */
.search-wrap { position: relative; display: flex; align-items: center; }
.search-input {
  width: 104px; padding: 9px 12px 9px 34px; border-radius: 999px;
  border: 1px solid rgba(212, 168, 79, .35); background: rgba(255, 249, 245, .08);
  color: #FFF9F5; font: 500 13px var(--sans); outline: none;
  transition: width .3s ease, border-color .3s ease, background .3s ease;
}
.search-input:focus { width: 150px; border-color: rgba(212, 168, 79, .8); background: rgba(255, 249, 245, .14); }
.search-input::placeholder { color: rgba(255, 249, 245, .5); }
.search-ico { position: absolute; left: 11px; width: 15px; height: 15px; stroke: var(--gold); pointer-events: none; }

/* mobile header: hide tagline so search never collides */
@media (max-width: 560px) {
  .brand-tag { display: none; }
  .brand-name { font-size: 13.5px; }
  .search-input { width: 92px; }
  .search-input:focus { width: 128px; }
  .topbar { gap: 8px; padding: 9px 12px; }
  .brand-logo { width: 38px; height: 38px; }
}

/* ========================= DELIVERY TRUST STRIP ========================= */
.delivery-strip {
  display: flex; align-items: center; justify-content: center; flex-wrap: wrap; gap: 8px;
  margin: 12px 16px 0; padding: 9px 16px; border-radius: 999px;
  background: linear-gradient(120deg, rgba(212, 168, 79, .16), rgba(212, 168, 79, .07) 55%, rgba(232, 90, 155, .1));
  border: 1px solid rgba(212, 168, 79, .4);
  font-size: 12px; color: var(--text-0); text-align: center;
  animation: rise .7s cubic-bezier(.22,1,.36,1) .1s backwards;
}
.delivery-strip svg { width: 17px; height: 17px; stroke: var(--gold-dim); flex: 0 0 auto; }
.delivery-strip b { font-weight: 800; color: var(--text-0); }
.delivery-strip .ds-sep { color: var(--gold-dim); }
@media (max-width: 560px) { .delivery-strip { font-size: 11px; } }

/* quick jump links so key sections are one tap away */
.jump-row { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin: 14px 16px 0; position: relative; z-index: 1; }
.jump-row a {
  font: 700 12px var(--sans); color: var(--pink-d); background: #FFFFFF;
  border: 1px solid var(--card-br); border-radius: 999px; padding: 9px 15px;
  min-height: 40px; display: inline-flex; align-items: center; text-decoration: none;
  box-shadow: var(--shadow-1); transition: transform .2s ease, border-color .2s ease;
}
.jump-row a:hover { border-color: var(--pink); transform: translateY(-2px); }
.jump-row a:active { transform: scale(.96); }

/* ============================== HERO =================================== */
.hero { position: relative; padding: 26px 20px 8px; text-align: center; z-index: 1; }
.hero > * { position: relative; z-index: 1; }
.hero-eyebrow {
  display: inline-flex; align-items: center; gap: 10px;
  font-size: 10.5px; letter-spacing: .3em; text-transform: uppercase; color: var(--gold-dim);
  animation: rise .8s cubic-bezier(.22,1,.36,1) .05s backwards;
}
.hero-eyebrow::before, .hero-eyebrow::after { content: ''; width: 34px; height: 1px; background: linear-gradient(90deg, transparent, var(--gold)); }
.hero-eyebrow::after { background: linear-gradient(90deg, var(--gold), transparent); }
.hero-title { margin-top: 12px; font-size: clamp(40px, 12vw, 88px); line-height: 1.02; animation: rise .8s cubic-bezier(.22,1,.36,1) .16s backwards; }
.shimmer { display: block; font-family: var(--serif); font-style: italic; font-weight: 600;
  background: linear-gradient(100deg, #241D1B 0%, #241D1B 36%, #D4A84F 46%, #F6D488 50%, #E85A9B 54%, #241D1B 64%, #241D1B 100%);
  background-size: 260% 100%; -webkit-background-clip: text; background-clip: text;
  -webkit-text-fill-color: transparent; color: transparent;
  animation: shimmer 6.5s ease-in-out infinite;
}
.shimmer small { display: block; font-size: .42em; letter-spacing: .1em; }
@keyframes shimmer { 0%, 100% { background-position: 0% 0; } 50% { background-position: -160% 0; } }
.hero-sub { margin: 14px auto 0; max-width: 440px; color: var(--text-1); font-size: 13.5px; animation: rise .8s cubic-bezier(.22,1,.36,1) .3s backwards; }
.hero-price {
  margin: 18px auto 0; display: inline-flex; align-items: baseline; gap: 10px;
  padding: 10px 22px; border-radius: 999px;
  border: 1px solid rgba(212, 168, 79, .55); background: #FFFFFF;
  box-shadow: 0 6px 22px rgba(212, 168, 79, .22);
  animation: rise .8s cubic-bezier(.22,1,.36,1) .44s backwards, floatY 5.5s ease-in-out 1.5s infinite;
}
@keyframes rise { from { opacity: 0; transform: translateY(18px); } }
@keyframes floatY { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-5px); } }
.hero-price .rs { font-family: var(--serif); font-style: italic; font-size: 30px; font-weight: 700; color: var(--pink); }
.hero-price .flat { font-size: 10px; letter-spacing: .26em; text-transform: uppercase; color: var(--text-1); }

/* ------------------------------ butterflies ---------------------------- */
.bflies { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
.bfly { position: absolute; overflow: visible; }
.bfly .wing { transform-origin: 32px 26px; animation: flap .46s ease-in-out infinite alternate; }
@keyframes flap { from { transform: scaleX(1); } to { transform: scaleX(.5); } }
.bfly.b1 { top: 6%; left: 5%; width: 46px; animation: drift1 17s ease-in-out infinite; }
.bfly.b2 { top: 38%; right: 6%; width: 34px; opacity: .9; animation: drift2 21s ease-in-out 2s infinite; }
.bfly.b2 .wing { animation-duration: .38s; }
@keyframes drift1 {
  0%   { transform: translate(0, 0) rotate(10deg); }
  25%  { transform: translate(46px, -16px) rotate(-6deg); }
  50%  { transform: translate(96px, 8px) rotate(8deg); }
  75%  { transform: translate(52px, 24px) rotate(-8deg); }
  100% { transform: translate(0, 0) rotate(10deg); }
}
@keyframes drift2 {
  0%   { transform: translate(0, 0) rotate(-8deg); }
  30%  { transform: translate(-52px, 20px) rotate(6deg); }
  60%  { transform: translate(-20px, -22px) rotate(-10deg); }
  100% { transform: translate(0, 0) rotate(-8deg); }
}

/* ============================== MARQUEE ================================ */
.marquee {
  margin: 26px 0 4px; overflow: hidden; position: relative; z-index: 1;
  -webkit-mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent);
  mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent);
}
.marquee-track { display: flex; gap: 14px; width: max-content; animation: marquee 70s linear infinite; }
.marquee:hover .marquee-track { animation-play-state: paused; }
.marquee-item {
  flex: 0 0 auto; width: 128px; height: 170px; border-radius: 14px; overflow: hidden;
  border: 1px solid var(--card-br); box-shadow: var(--shadow-1); background: #FFFFFF;
  transition: transform .35s ease, box-shadow .35s ease;
}
.marquee-item:hover { transform: translateY(-4px) rotate(-1deg); box-shadow: var(--shadow-2); }
.marquee-item img { width: 100%; height: 100%; object-fit: cover; }
@keyframes marquee { from { transform: translateX(0); } to { transform: translateX(-50%); } }

/* ============================ FILTER BAR =============================== */
.sticky-bar {
  position: sticky; top: 62px; z-index: 50;
  padding: 10px 16px; margin-top: 10px;
  background: rgba(255, 249, 245, .92);
  backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
  box-shadow: 0 1px 0 var(--card-br);
}
.chips { display: flex; gap: 8px; overflow-x: auto; scrollbar-width: none; padding-bottom: 2px; }
.chips::-webkit-scrollbar { display: none; }
.chip {
  flex: 0 0 auto; display: inline-flex; align-items: center; gap: 7px;
  padding: 8px 15px; border-radius: 999px; font: 600 12.5px var(--sans); letter-spacing: .02em;
  color: var(--text-1); border: 1px solid var(--card-br); background: #FFFFFF;
  transition: transform .2s ease, color .25s ease, border-color .25s ease, background .25s ease, box-shadow .25s ease;
}
.chip:active { transform: scale(.94); }
.chip.on { color: #fff; background: var(--pink-grad); border-color: transparent; box-shadow: 0 4px 18px rgba(232, 90, 155, .35); }
.chip .cdot { width: 11px; height: 11px; border-radius: 50%; border: 1.5px solid rgba(36, 29, 27, .18); }
.chip.on .cdot { border-color: rgba(255, 255, 255, .65); }

/* ============================== GRID =================================== */
.grid {
  position: relative; z-index: 1;
  display: grid; gap: 14px; padding: 14px 16px 120px;
  grid-template-columns: repeat(2, 1fr);
}
@media (min-width: 700px) { .grid { grid-template-columns: repeat(3, 1fr); gap: 20px; } }
@media (min-width: 1060px) { .grid { grid-template-columns: repeat(4, 1fr); } }

.card {
  position: relative; border-radius: var(--rad); overflow: hidden; cursor: pointer;
  background: var(--card); border: 1px solid var(--card-br);
  box-shadow: var(--shadow-1);
  opacity: 0; transform: translateY(26px) scale(.98);
  transition: opacity .6s ease, transform .6s cubic-bezier(.22,1,.36,1), box-shadow .3s ease, border-color .3s ease;
  will-change: transform, opacity;
}
.card.in { opacity: 1; transform: none; }
.card:hover { transform: translateY(-6px); box-shadow: var(--shadow-2), 0 0 0 1px rgba(232, 90, 155, .28); border-color: rgba(232, 90, 155, .4); }
.card-img-wrap { position: relative; aspect-ratio: 3/4; overflow: hidden; background: #F6EDEE; }
.card-img-wrap img { width: 100%; height: 100%; object-fit: cover; opacity: 0; transition: transform .7s cubic-bezier(.22,1,.36,1), opacity .5s ease; }
.card-img-wrap img.ld { opacity: 1; }
.card-img-wrap { background-size: cover; background-position: center; }
.card:hover .card-img-wrap img { transform: scale(1.055); }
.card-badge {
  position: absolute; top: 10px; left: 10px; z-index: 2;
  font: 700 9px var(--sans); letter-spacing: .18em; text-transform: uppercase;
  padding: 5px 10px; border-radius: 999px;
  animation: badgePulse 3.4s ease-in-out infinite;
}
.card-badge.b-gold { color: #111111; background: linear-gradient(120deg, #D4A84F, #EBCB8A 55%, #D4A84F); box-shadow: 0 3px 14px rgba(212, 168, 79, .45); }
.card-badge.b-pink { color: #fff; background: linear-gradient(120deg, #E85A9B, #F07AB0 55%, #E85A9B); box-shadow: 0 3px 14px rgba(232, 90, 155, .45); }
@keyframes badgePulse {
  0%, 100% { transform: scale(1); }
  50%      { transform: scale(1.055); }
}
.card-swatches { position: absolute; bottom: 10px; left: 10px; z-index: 2; display: flex; gap: 5px; }
.card-swatch { width: 15px; height: 15px; border-radius: 50%; border: 1.5px solid rgba(255, 255, 255, .9); box-shadow: 0 1px 5px rgba(17, 17, 17, .45); }
.card-veil {
  position: absolute; inset: 0; z-index: 1;
  background: linear-gradient(180deg, transparent 55%, rgba(17, 17, 17, .62) 96%);
}
.card-body { padding: 11px 12px 13px; }
.card-name { font-family: var(--serif); font-style: italic; font-weight: 600; font-size: 17.5px; line-height: 1.15; color: var(--text-0); }
.card-type { margin-top: 3px; font-size: 10px; letter-spacing: .2em; text-transform: uppercase; color: var(--gold-dim); }
.card-row { margin-top: 8px; display: flex; align-items: center; justify-content: space-between; }
.card-price { font: 800 15px var(--sans); color: var(--text-0); }
.card-price .cur { color: var(--pink); font-weight: 700; margin-right: 2px; }
.card-plus {
  width: 30px; height: 30px; border-radius: 50%; display: grid; place-items: center;
  border: 1px solid rgba(232, 90, 155, .5); color: var(--pink); font-size: 17px; line-height: 1;
  transition: background .25s ease, color .25s ease, transform .25s ease;
  will-change: transform;
}
.card-plus.added { animation: plusRing .5s cubic-bezier(.34,1.8,.5,1); }
@keyframes plusRing { 0% { box-shadow: 0 0 0 0 rgba(63, 160, 107, .55); } 100% { box-shadow: 0 0 0 12px rgba(63, 160, 107, 0); } }
.card:hover .card-plus { background: var(--pink); color: #fff; transform: rotate(90deg); }
.no-results { grid-column: 1/-1; text-align: center; padding: 70px 20px; color: var(--text-2); }
.no-results .big { font-family: var(--serif); font-style: italic; font-size: 30px; color: var(--text-1); }

/* ============================ PRODUCT SHEET ============================ */
/* Closed layers are fully inert: opacity 0 + visibility hidden, so they can never
   swallow wheel-scrolls or clicks on the page underneath (fixes "scroll only works
   on the right side" on PC). Visibility flips before/after the fade transitions. */
.sheet-layer { position: fixed; inset: 0; z-index: 100; pointer-events: none; opacity: 0; visibility: hidden; transition: opacity .32s ease, visibility 0s linear .32s; }
.sheet-layer.open { opacity: 1; visibility: visible; transition: opacity .32s ease; }
.sheet-layer .scrim {
  position: absolute; inset: 0; background: rgba(17, 17, 17, .55);
  opacity: 0; transition: opacity .32s ease; backdrop-filter: blur(3px); -webkit-backdrop-filter: blur(3px);
}
.sheet {
  visibility: hidden; transition: visibility 0s linear .42s, transform .42s cubic-bezier(.32,.72,.24,1), opacity .3s ease;
  position: absolute; left: 0; right: 0; bottom: 0; max-height: 93dvh;
  display: flex; flex-direction: column;
  background: #FFFFFF;
  border-radius: var(--sheet-rad) var(--sheet-rad) 0 0;
  border: 1px solid var(--card-br); border-bottom: 0;
  box-shadow: 0 -20px 60px rgba(17, 17, 17, .3);
  transform: var(--sheet-hide, translateY(104%));
  pointer-events: auto;
}
.sheet-layer.open .scrim { opacity: 1; }
.sheet-layer.open .sheet { visibility: visible; transition: visibility 0s, transform .42s cubic-bezier(.32,.72,.24,1), opacity .3s ease; transform: var(--sheet-show, translateY(0)); }
.sheet-grab { padding: 10px 0 4px; display: grid; place-items: center; cursor: grab; touch-action: none; flex: 0 0 auto; }
.sheet-grab span { width: 44px; height: 5px; border-radius: 3px; background: #E3D5D9; }
.sheet-close {
  position: absolute; top: 14px; right: 14px; z-index: 5;
  width: 34px; height: 34px; border-radius: 50%; display: grid; place-items: center;
  background: rgba(255, 255, 255, .88); border: 1px solid var(--card-br); color: var(--text-0);
  font-size: 15px; backdrop-filter: blur(6px);
}
.sheet-scroll { overflow-y: auto; overscroll-behavior: contain; -webkit-overflow-scrolling: touch; padding: 0 18px 24px; }
.sheet-body-drag { transition: transform .28s ease; }

/* desktop: product sheet becomes a centered split dialog — image left, details right */
@media (min-width: 900px) {
  .sheet-grab { display: none; }
  .sheet {
    left: 50%; right: auto; bottom: auto; top: 50%;
    width: min(980px, 94vw); height: min(660px, 92dvh); max-height: none;
    border-radius: 26px; border-bottom: 1px solid var(--card-br);
    --sheet-hide: translate(-50%, -46%) scale(.97); opacity: 0;
    --sheet-show: translate(-50%, -50%) scale(1);
  }
  .sheet-layer.open .sheet { opacity: 1; }
  .sheet-close { top: 16px; right: 16px; width: 38px; height: 38px; background: rgba(255, 255, 255, .92); box-shadow: 0 2px 10px rgba(17, 17, 17, .14); z-index: 9; }
  .sheet-scroll {
    display: grid; grid-template-columns: minmax(0, 46fr) minmax(0, 54fr);
    gap: 30px; align-items: start; padding: 26px 30px 30px; height: 100%;
  }
  .car { position: sticky; top: 4px; aspect-ratio: 4/4.4; max-height: calc(92dvh - 60px); }
  .pd-info { min-width: 0; }
  .pd-head { margin-top: 0; padding-right: 44px; }
  .pd-name { font-size: 34px; }
}

/* carousel */
.car { position: relative; border-radius: 20px; overflow: hidden; aspect-ratio: 4/4.2; max-height: 47dvh; background: #F6EDEE; border: 1px solid var(--card-br); touch-action: pan-y; }
.car-track { position: absolute; inset: 0; }
.car-slide { position: absolute; inset: 0; opacity: 0; transition: opacity .45s ease; background-size: cover; background-position: center; }
.car-slide.on { opacity: 1; }
.car-slide img { width: 100%; height: 100%; object-fit: cover; }
.marquee-item { background-size: cover; background-position: center; }
.marquee-item img { opacity: 0; transition: opacity .5s ease; }
.marquee-item img.ld { opacity: 1; }
.car-tag {
  position: absolute; left: 12px; bottom: 12px; z-index: 3;
  font: 700 10px var(--sans); letter-spacing: .16em; text-transform: uppercase;
  padding: 6px 11px; border-radius: 999px; color: var(--ink-0);
  background: rgba(255, 255, 255, .94);
}
.car-nav {
  position: absolute; top: 50%; transform: translateY(-50%); z-index: 4;
  width: 34px; height: 34px; border-radius: 50%; display: none; place-items: center;
  background: rgba(255, 255, 255, .8); border: 1px solid var(--card-br); color: var(--text-0);
  transition: background .2s ease;
}
.car-nav:hover { background: #FFFFFF; }
.car-nav.prev { left: 10px; } .car-nav.next { right: 10px; }
#car.single .car-nav, #car.single .car-dots { display: none !important; }
@media (hover:hover) { #car:not(.single) .car-nav { display: grid; } }
.car-dots { position: absolute; bottom: 10px; left: 0; right: 0; z-index: 3; display: flex; justify-content: center; gap: 6px; }
.car-dot { width: 7px; height: 7px; border-radius: 4px; background: rgba(255, 255, 255, .55); box-shadow: 0 1px 3px rgba(17,17,17,.25); transition: all .3s ease; }
.car-dot.on { width: 20px; background: var(--pink); }

/* product info */
.pd-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; margin-top: 16px; }
.pd-name { font-family: var(--serif); font-style: italic; font-weight: 600; font-size: 30px; line-height: 1.08; color: var(--text-0); }
.pd-type { margin-top: 5px; font-size: 10.5px; letter-spacing: .24em; text-transform: uppercase; color: var(--gold-dim); }
.pd-price { text-align: right; flex: 0 0 auto; }
.pd-price .rs { font-family: var(--serif); font-style: italic; font-weight: 700; font-size: 30px; color: var(--pink); }
.pd-price .mrp { display: block; font-size: 11.5px; color: var(--text-2); text-decoration: line-through; }
.pd-price .save { display: inline-block; margin-top: 3px; font: 700 9.5px var(--sans); letter-spacing: .1em; color: #fff; background: var(--pink); padding: 3px 8px; border-radius: 999px; }
.pd-desc { margin-top: 10px; color: var(--text-1); font-size: 13.5px; }

.pd-label { margin: 18px 0 9px; font: 700 10.5px var(--sans); letter-spacing: .22em; text-transform: uppercase; color: var(--text-2); display: flex; justify-content: space-between; }
.pd-label b { color: var(--pink-d); font-weight: 700; letter-spacing: .02em; text-transform: none; font-size: 12.5px; }
.swatch-row { display: flex; gap: 12px; flex-wrap: wrap; }
.swatch {
  position: relative; width: 42px; height: 42px; border-radius: 50%;
  border: 2px solid rgba(36, 29, 27, .1); box-shadow: inset 0 0 0 2px rgba(255, 255, 255, .55);
  transition: transform .3s cubic-bezier(.34,1.8,.5,1), border-color .25s ease;
}
.swatch::after {
  content: ''; position: absolute; inset: -7px; border-radius: 50%;
  border: 1.5px solid var(--pink); opacity: 0; transform: scale(.7); transition: all .3s cubic-bezier(.34,1.8,.5,1);
}
.swatch.on { transform: scale(1.14); border-color: #FFFFFF; box-shadow: inset 0 0 0 2px rgba(255,255,255,.9), 0 3px 12px rgba(232,90,155,.35); }
.swatch.on::after { opacity: 1; transform: scale(1); }
.swatch.pop { animation: swatchPop .45s cubic-bezier(.34,2,.5,1); }
@keyframes swatchPop { 0% { transform: scale(1); } 40% { transform: scale(1.35); } 100% { transform: scale(1.14); } }

.qty-row { display: flex; align-items: center; justify-content: space-between; gap: 14px; }
.qty { display: inline-flex; align-items: center; border: 1px solid var(--card-br); border-radius: 999px; overflow: hidden; background: var(--cream); }
.qty button { width: 42px; height: 42px; font-size: 19px; color: var(--pink-d); transition: background .2s ease; }
.qty button:hover { background: var(--pink-soft); }
.qty b { min-width: 34px; text-align: center; font-size: 16px; color: var(--text-0); }

.pd-cta { margin-top: 18px; display: grid; grid-template-columns: 1fr; gap: 10px; }
.btn {
  position: relative; display: flex; align-items: center; justify-content: center; gap: 10px;
  min-height: 52px; border-radius: 16px; font: 800 14px var(--sans); letter-spacing: .06em;
  transition: transform .2s ease, box-shadow .25s ease, background .25s ease; overflow: hidden;
}
.btn::after {
  content: ''; position: absolute; top: -10px; bottom: -10px; width: 42%; left: 0;
  background: linear-gradient(100deg, transparent, rgba(255, 255, 255, .5), transparent);
  transform: translateX(-160%) skewX(-18deg); transition: transform .65s ease; pointer-events: none;
  will-change: transform;
}
.btn:hover::after { transform: translateX(320%) skewX(-18deg); }
.btn:active { transform: scale(.965); }
.btn-gold { background: var(--pink-grad); color: #fff; box-shadow: 0 8px 24px rgba(232, 90, 155, .35); }
.btn-gold:hover { background: linear-gradient(120deg, #C94482, #E85A9B 55%, #C94482); box-shadow: 0 10px 30px rgba(232, 90, 155, .5); }
.btn-wine { background: #111111; color: #FFF9F5; border: 1px solid rgba(212, 168, 79, .5); }
.btn-wine:hover { box-shadow: 0 10px 26px rgba(17, 17, 17, .4); }
.btn-ico { width: 19px; height: 19px; flex: 0 0 auto; }
.btn .check { position: absolute; inset: 0; display: grid; place-items: center; background: linear-gradient(120deg, #2E7D4F, #3FA06B); color: #fff; opacity: 0; pointer-events: none; }
.btn.added .check { animation: checkIn 1.25s cubic-bezier(.22,1,.36,1) forwards; }
@keyframes checkIn { 0% { opacity: 0; transform: scale(.4); } 18% { opacity: 1; transform: scale(1.06); } 30% { transform: scale(1); } 78% { opacity: 1; } 100% { opacity: 0; transform: scale(1.02); } }
.trust { margin-top: 16px; display: flex; gap: 8px; flex-wrap: wrap; }
.trust span { font-size: 10.5px; letter-spacing: .08em; color: var(--text-1); border: 1px solid var(--card-br); background: var(--cream); padding: 5px 10px; border-radius: 999px; }

/* product details spec grid */
.pd-details { margin-top: 20px; border-top: 1px solid var(--card-br); padding-top: 15px; }
.pd-details-title { font: 800 14px var(--sans); color: var(--text-0); }
.spec-grid { margin-top: 6px; display: grid; grid-template-columns: 1fr 1fr; gap: 0 22px; }
.spec { padding: 10px 0 12px; border-bottom: 1px solid var(--card-br); }
.spec b { display: block; font: 700 12.5px var(--sans); color: var(--text-0); }
.spec span { display: block; margin-top: 3px; font-size: 12px; color: var(--text-1); }
@media (min-width: 900px) {
  .spec-grid { grid-template-columns: 1fr 1fr 1fr; }
  .spec-grid .spec:last-child { grid-column: auto; }
}
.more-details { width: fit-content; margin: 6px 0 0 auto; display: flex; align-items: center; gap: 6px; font: 700 12.5px var(--sans); color: var(--pink-d); }
.more-details svg { width: 14px; height: 14px; stroke: currentColor; transition: transform .3s ease; }
.more-details.open svg { transform: rotate(180deg); }
.more-panel { overflow: hidden; max-height: 0; opacity: 0; transition: max-height .4s ease, opacity .35s ease; }
.more-panel.open { max-height: 320px; opacity: 1; }
.more-row { display: flex; justify-content: space-between; gap: 16px; padding: 9px 2px; border-bottom: 1px dashed var(--card-br); font-size: 12px; color: var(--text-1); }
.more-row:last-child { border-bottom: 0; }
.more-row b { color: var(--text-0); font-weight: 700; flex: 0 0 auto; }

/* ============================ COMBO PRICING ============================= */
.combo { position: relative; z-index: 1; padding: 34px 16px 10px; text-align: center; }
.combo-kicker, .visit-kicker { display: inline-flex; align-items: center; gap: 10px; font-size: 10.5px; letter-spacing: .3em; text-transform: uppercase; color: var(--gold-dim); }
.combo-kicker::before, .combo-kicker::after, .visit-kicker::before, .visit-kicker::after { content: ''; width: 34px; height: 1px; background: linear-gradient(90deg, transparent, var(--gold)); }
.visit-kicker::after { background: linear-gradient(90deg, var(--gold), transparent); }
.combo-title { margin-top: 10px; font-family: var(--serif); font-style: italic; font-weight: 600; font-size: clamp(30px, 7vw, 46px); color: var(--text-0); }
.combo-sub { margin: 8px auto 0; max-width: 420px; color: var(--text-1); font-size: 13px; }
.combo-table { margin: 20px auto 0; max-width: 620px; text-align: left; }
.combo-head-row {
  display: grid; grid-template-columns: 1fr 92px 92px; gap: 8px; padding: 9px 18px;
  font: 800 10.5px var(--sans); letter-spacing: .2em; text-transform: uppercase; color: var(--text-2);
}
.combo-head-row .cr-c { text-align: center; }
.combo-row {
  display: grid; grid-template-columns: 1fr 92px 92px; gap: 8px; align-items: center;
  padding: 12px 18px; border-radius: 16px; background: #FFFFFF; border: 1px solid var(--card-br);
  margin-top: 8px; box-shadow: var(--shadow-1);
  opacity: 0; transform: translateY(14px);
  transition: opacity .38s ease, transform .38s cubic-bezier(.22,1,.36,1);
}
.combo-row.in { opacity: 1; transform: none; }
.cr-qty { display: flex; align-items: center; gap: 10px; min-width: 0; }
.cr-dot { width: 30px; height: 30px; border-radius: 50%; display: grid; place-items: center; flex: 0 0 auto;
  background: var(--pink-soft); color: var(--pink-d); font: 800 12.5px var(--sans); }
.cr-qty b { font: 700 14px var(--sans); color: var(--text-0); }
.cr-qty small { display: block; font: 600 10px var(--sans); letter-spacing: .08em; text-transform: uppercase; color: var(--text-2); }
.cr-price { text-align: center; font: 800 15.5px var(--sans); color: var(--text-0); }
.cr-save { text-align: center; font: 700 12.5px var(--sans); color: #2E7D4F; }
.combo-row .cr-save.cr-zero { color: var(--text-2); }
.combo-row.best {
  background: linear-gradient(120deg, #FFF6E3, #FFFDF7 55%, #FDEFF6);
  border: 1.5px solid var(--gold); box-shadow: 0 10px 30px rgba(212, 168, 79, .3);
  position: relative;
}
.combo-row.best .cr-dot { background: var(--gold); color: #fff; }
.cr-badge {
  position: absolute; top: -11px; right: 14px;
  font: 800 9.5px var(--sans); letter-spacing: .18em; text-transform: uppercase;
  color: #111; background: linear-gradient(120deg, #D4A84F, #EBCB8A 55%, #D4A84F);
  padding: 5px 12px; border-radius: 999px; box-shadow: 0 4px 14px rgba(212, 168, 79, .5);
  animation: badgePulse 3s ease-in-out infinite;
}
@media (max-width: 420px) {
  .combo-head-row { grid-template-columns: 1fr 78px 78px; padding: 9px 14px; }
  .combo-row { grid-template-columns: 1fr 78px 78px; padding: 11px 14px; }
  .cr-price { font-size: 14px; }
}

/* ============================ STORE LOCATION ============================ */
.visit { position: relative; z-index: 1; padding: 30px 16px 8px; text-align: center; }
.visit-card {
  margin: 18px auto 0; max-width: 620px; background: #FFFFFF; border: 1px solid var(--card-br);
  border-radius: 22px; padding: 22px 20px; box-shadow: var(--shadow-1);
}
.visit-addr { font: 700 15px var(--sans); color: var(--text-0); line-height: 1.5; }
.visit-actions { margin-top: 16px; display: flex; gap: 10px; justify-content: center; flex-wrap: wrap; }
.visit-actions .btn { min-height: 46px; padding: 0 18px; flex: 0 0 auto; }
.visit-meta { margin-top: 14px; font-size: 12px; color: var(--text-1); }
.visit-meta a { color: var(--pink-d); font-weight: 700; text-decoration: none; }
.visit-note { margin-top: 12px; font: 700 10.5px var(--sans); letter-spacing: .12em; text-transform: uppercase; color: #8A6B23; }

/* ============================ DELIVERY FAQ ============================= */
.delivery-info { position: relative; z-index: 1; padding: 30px 16px 8px; text-align: center; }
.faq-card { margin: 18px auto 0; max-width: 620px; background: #FFFFFF; border: 1px solid var(--card-br); border-radius: 22px; padding: 8px 20px; box-shadow: var(--shadow-1); text-align: left; }
.faq { padding: 13px 0; border-bottom: 1px dashed var(--card-br); }
.faq:last-child { border-bottom: 0; }
.faq b { display: block; font: 800 13.5px var(--sans); color: var(--text-0); }
.faq span { display: block; margin-top: 4px; font-size: 12.5px; color: var(--text-1); line-height: 1.6; }
.faq span b { display: inline; font-size: 12.5px; }

/* ========================= PRIVACY / 404 VIEWS ========================= */
.pageview { position: fixed; inset: 0; z-index: 150; background: var(--cream); overflow-y: auto; -webkit-overflow-scrolling: touch; }
.page-inner { max-width: 640px; margin: 0 auto; padding: calc(24px + env(safe-area-inset-top)) 22px 60px; }
.page-back { display: inline-flex; align-items: center; min-height: 44px; padding: 0 6px; font: 700 13.5px var(--sans); color: var(--pink-d); margin-bottom: 4px; }
.pp h1 { font-family: var(--serif); font-style: italic; font-weight: 600; font-size: clamp(34px, 8vw, 44px); color: var(--text-0); margin: 4px 0 10px; }
.pp h2 { font: 800 15px var(--sans); color: var(--text-0); margin: 22px 0 6px; }
.pp p, .pp li { font-size: 14px; color: var(--text-1); line-height: 1.65; }
.pp ul { padding-left: 20px; display: grid; gap: 6px; margin-top: 6px; }
.pp a { color: var(--pink-d); font-weight: 700; }
.pp-upd { margin-top: 26px; font-size: 11.5px; color: var(--text-2); letter-spacing: .06em; }
.err404 { text-align: center; padding-top: calc(14vh + env(safe-area-inset-top)); }
.err-ico { width: 88px; margin: 0 auto 14px; animation: sway 3.2s ease-in-out infinite; }
.err-ico svg { width: 100%; height: auto; }
@keyframes sway { 0%, 100% { transform: rotate(-5deg) translateY(0); } 50% { transform: rotate(5deg) translateY(-7px); } }
.err404 h1 { font-family: var(--serif); font-style: italic; font-weight: 600; font-size: clamp(32px, 8vw, 44px); color: var(--text-0); }
.err404 p { margin: 10px auto 20px; max-width: 320px; color: var(--text-1); font-size: 14px; }
.err404 .btn { min-width: 220px; margin: 0 auto; }

/* ======================= SIZES / SIZE CHART MODAL ======================= */
.size-row { display: flex; gap: 8px; flex-wrap: wrap; }
.size-chip {
  min-width: 46px; height: 40px; padding: 0 12px; border-radius: 12px;
  border: 1.5px solid var(--card-br); background: #FFFFFF; color: var(--text-0);
  font: 700 13px var(--sans); transition: border-color .2s ease, background .2s ease, color .2s ease;
}
.size-chip.on { background: var(--ink-0); border-color: var(--ink-0); color: var(--gold); }
.size-chip.pop { animation: chipPop .35s cubic-bezier(.34,2,.5,1); }
@keyframes chipPop { 0% { transform: scale(1); } 40% { transform: scale(1.08); } 100% { transform: scale(1); } }
.size-link { display: inline-flex; align-items: center; gap: 5px; font: 700 11.5px var(--sans); color: var(--pink-d); background: none; border: 0; cursor: pointer; }
.size-link svg { width: 14px; height: 14px; stroke: currentColor; }
.size-link:hover { text-decoration: underline; }
.pd-label .size-link { text-transform: none; letter-spacing: 0; }

.modal-layer { position: fixed; inset: 0; z-index: 120; display: grid; place-items: center; pointer-events: none; opacity: 0; visibility: hidden; transition: opacity .3s ease, visibility 0s linear .3s; }
.modal-layer.open { opacity: 1; visibility: visible; transition: opacity .3s ease; }
.modal-layer .scrim { position: absolute; inset: 0; background: rgba(17, 17, 17, .55); opacity: 0; transition: opacity .3s ease; }
.modal {
  position: relative; width: min(480px, calc(100vw - 36px)); max-height: 84dvh; overflow-y: auto;
  background: #FFFFFF; border-radius: 22px; border: 1px solid var(--card-br); box-shadow: 0 30px 80px rgba(17, 17, 17, .35);
  visibility: hidden; opacity: 0; transform: translateY(26px) scale(.97); transition: visibility 0s linear .38s, opacity .32s ease, transform .38s cubic-bezier(.22,1,.36,1);
  pointer-events: auto;
}
.modal-layer.open { pointer-events: auto; }
.modal-layer.open .scrim { opacity: 1; }
.modal-layer.open .modal { visibility: visible; opacity: 1; transform: none; }
.modal-head { display: flex; align-items: center; justify-content: space-between; padding: 16px 18px 10px; }
.modal-title { font-family: var(--serif); font-style: italic; font-weight: 600; font-size: 24px; color: var(--text-0); }
.size-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.size-table th { text-align: left; font: 800 10.5px var(--sans); letter-spacing: .14em; text-transform: uppercase; color: var(--text-2); padding: 10px 8px; border-bottom: 1.5px solid var(--card-br); }
.size-table td { padding: 11px 8px; border-bottom: 1px solid var(--card-br); color: var(--text-0); font-weight: 600; }
.size-table td:first-child { font-weight: 800; color: var(--pink-d); }
.size-table tr:last-child td { border-bottom: 0; }
.size-note { margin: 6px 4px 14px; font-size: 11.5px; color: var(--text-2); line-height: 1.5; }

/* cod note in sheet */
.cod-note {
  margin-top: 14px; display: flex; align-items: center; gap: 9px;
  padding: 10px 14px; border-radius: 14px;
  background: linear-gradient(120deg, rgba(212, 168, 79, .14), rgba(232, 90, 155, .07));
  border: 1px dashed rgba(212, 168, 79, .55); font-size: 11.5px; color: var(--text-1);
}
.cod-note svg { width: 16px; height: 16px; stroke: #2E7D4F; flex: 0 0 auto; }
.cod-note b { color: var(--text-0); }

/* cart savings line */
.cart-save { text-align: center; font: 700 11.5px var(--sans); color: #2E7D4F; margin-bottom: 8px; min-height: 15px; }
.cart-save:empty { display: none; }

/* =========================== MOBILE NAV DRAWER ========================== */
.nav-layer { position: fixed; inset: 0; z-index: 140; pointer-events: none; opacity: 0; visibility: hidden; transition: opacity .28s ease, visibility 0s linear .28s; }
.nav-layer.open { opacity: 1; visibility: visible; transition: opacity .28s ease; }
.nav-layer .scrim { position: absolute; inset: 0; background: rgba(17, 17, 17, .55); opacity: 0; transition: opacity .28s ease; backdrop-filter: blur(3px); -webkit-backdrop-filter: blur(3px); }
.nav-drawer {
  position: absolute; top: 0; right: 0; bottom: 0; width: min(320px, 86vw);
  background: #FFFFFF; border-left: 1px solid var(--card-br);
  transform: translateX(105%); transition: transform .32s cubic-bezier(.32, .72, .24, 1);
  display: flex; flex-direction: column; overflow-y: auto; pointer-events: auto;
  padding-bottom: env(safe-area-inset-bottom); box-shadow: -24px 0 60px rgba(17, 17, 17, .25);
}
.nav-layer.open { pointer-events: auto; }
.nav-layer.open .scrim { opacity: 1; }
.nav-layer.open .nav-drawer { transform: translateX(0); }
.nav-head { display: flex; align-items: center; justify-content: space-between; padding: 16px 18px 10px; }
.nav-title { font-family: var(--serif); font-style: italic; font-weight: 600; font-size: 24px; color: var(--text-0); }
.nav-link {
  display: flex; align-items: center; justify-content: space-between; gap: 10px;
  min-height: 48px; padding: 10px 18px; font: 700 14.5px var(--sans); color: var(--text-0);
  text-decoration: none; border: 0; border-bottom: 1px solid var(--card-br);
  width: 100%; text-align: left; background: none; cursor: pointer; transition: background .2s ease;
}
.nav-link:active { background: var(--pink-soft); }
.nav-link .narr { font: 600 10.5px var(--sans); letter-spacing: .14em; text-transform: uppercase; color: var(--pink-d); }
.nav-foot { margin-top: auto; padding: 18px; display: grid; gap: 9px; font-size: 12px; color: var(--text-1); }
.nav-foot a { color: var(--pink-d); font-weight: 700; text-decoration: none; }

/* ============================== CART =================================== */
.cart-layer { position: fixed; inset: 0; z-index: 110; pointer-events: none; opacity: 0; visibility: hidden; transition: opacity .32s ease, visibility 0s linear .32s; }
.cart-layer.open { opacity: 1; visibility: visible; transition: opacity .32s ease; }
.cart-layer .scrim { position: absolute; inset: 0; background: rgba(17, 17, 17, .55); opacity: 0; transition: opacity .32s ease; backdrop-filter: blur(3px); -webkit-backdrop-filter: blur(3px); }
.cart {
  position: absolute; bottom: 0; left: 0; right: 0; max-height: 88dvh; display: flex; flex-direction: column;
  background: #FFFFFF; border-radius: var(--sheet-rad) var(--sheet-rad) 0 0;
  border: 1px solid var(--card-br); border-bottom: 0;
  transform: translateY(104%); transition: transform .42s cubic-bezier(.32,.72,.24,1); pointer-events: auto;
}
.cart-layer.open .scrim { opacity: 1; }
.cart-layer.open .cart { transform: translateY(0); }
.cart-head { display: flex; align-items: center; justify-content: space-between; padding: 18px 18px 12px; border-bottom: 1px solid var(--card-br); flex: 0 0 auto; }
.cart-title { font-family: var(--serif); font-style: italic; font-weight: 600; font-size: 25px; color: var(--text-0); }
.cart-count { font: 700 10.5px var(--sans); letter-spacing: .18em; color: var(--pink-d); text-transform: uppercase; }
.cart-x { width: 34px; height: 34px; border-radius: 50%; border: 1px solid var(--card-br); display: grid; place-items: center; color: var(--text-0); }
.cart-items { overflow-y: auto; overscroll-behavior: contain; padding: 8px 18px; flex: 1; }
.cart-empty { text-align: center; padding: 46px 16px; color: var(--text-2); }
.cart-empty .big { font-family: var(--serif); font-style: italic; font-size: 26px; color: var(--text-1); margin-bottom: 6px; }
.ci { display: grid; grid-template-columns: 62px 1fr auto; gap: 12px; align-items: center; padding: 11px 0; border-bottom: 1px solid var(--card-br); animation: ciIn .35s ease; }
@keyframes ciIn { from { opacity: 0; transform: translateY(8px); } }
.ci-img { width: 62px; height: 74px; border-radius: 10px; object-fit: cover; border: 1px solid var(--card-br); }
.ci-name { font-family: var(--serif); font-style: italic; font-weight: 600; font-size: 16.5px; line-height: 1.15; color: var(--text-0); }
.ci-meta { display: flex; align-items: center; gap: 7px; margin-top: 3px; font-size: 11px; color: var(--text-2); }
.ci-meta .cdot { width: 10px; height: 10px; border-radius: 50%; border: 1px solid rgba(36, 29, 27, .15); }
.ci-qty { display: inline-flex; align-items: center; gap: 2px; margin-top: 7px; border: 1px solid var(--card-br); border-radius: 999px; }
.ci-qty button { width: 28px; height: 28px; color: var(--pink-d); font-size: 15px; }
.ci-qty b { min-width: 20px; text-align: center; font-size: 13px; color: var(--text-0); }
.ci-right { text-align: right; display: flex; flex-direction: column; align-items: flex-end; gap: 8px; }
.ci-price { font: 800 15px var(--sans); color: var(--pink-d); }
.ci-del { font-size: 11px; color: var(--pink); letter-spacing: .06em; }
.cart-foot { padding: 14px 18px calc(16px + env(safe-area-inset-bottom)); border-top: 1px solid var(--card-br); background: var(--cream); flex: 0 0 auto; }
.cart-total { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 12px; }
.cart-total .lbl { font-size: 11px; letter-spacing: .22em; text-transform: uppercase; color: var(--text-2); }
.cart-total .val { font-family: var(--serif); font-style: italic; font-weight: 700; font-size: 28px; color: var(--pink); }
.cart-note { text-align: center; font-size: 10.5px; color: var(--text-2); margin-top: 9px; letter-spacing: .04em; }
@media (min-width: 900px) {
  .cart {
    top: 0; bottom: 0; left: auto; right: 0; width: 420px; max-height: none;
    border-radius: 0; border: 0; border-left: 1px solid var(--card-br);
    transform: translateX(105%); box-shadow: -30px 0 80px rgba(17, 17, 17, .28);
  }
  .cart-layer.open .cart { transform: translateX(0); }
  .cart { transition: transform .45s cubic-bezier(.32,.72,.24,1); }
}

/* floating cart bar */
.cartbar {
  position: fixed; z-index: 90; left: 50%; bottom: calc(14px + env(safe-area-inset-bottom));
  transform: translate(-50%, 140%); width: min(480px, calc(100% - 28px));
  display: flex; align-items: center; gap: 12px;
  padding: 10px 12px 10px 18px; border-radius: 20px;
  background: #111111; border: 1px solid rgba(212, 168, 79, .45);
  color: #FFF9F5; box-shadow: 0 14px 44px rgba(17, 17, 17, .4);
  transition: transform .5s cubic-bezier(.22,1.4,.36,1);
}
.cartbar.show { transform: translate(-50%, 0); }
.cartbar:active { transform: translate(-50%, 0) scale(.97); }
.cb-count {
  min-width: 26px; height: 26px; padding: 0 6px; border-radius: 999px; display: grid; place-items: center;
  background: var(--gold); color: #111111; font: 800 13px var(--sans);
}
.cb-txt { flex: 1; min-width: 0; }
.cb-items { font: 700 12px var(--sans); letter-spacing: .04em; color: rgba(255, 249, 245, .72); }
.cb-total { font: 800 17px var(--sans); color: var(--gold); }
.cb-go { display: flex; align-items: center; gap: 8px; font: 800 12.5px var(--sans); letter-spacing: .05em; background: var(--pink); color: #fff; padding: 11px 16px; border-radius: 14px; transition: background .25s ease; }
.cartbar:hover .cb-go { background: var(--pink-d); }
.cb-go svg { width: 16px; height: 16px; fill: #FFFFFF; }
.cartbar.bump { animation: cbBump .45s cubic-bezier(.34,2,.5,1); }
@keyframes cbBump { 0% { transform: translate(-50%,0) scale(1); } 40% { transform: translate(-50%,0) scale(1.05); } 100% { transform: translate(-50%,0) scale(1); } }

/* ============================== FOOTER ================================= */
.footer { position: relative; z-index: 1; padding: 44px 24px calc(34px + env(safe-area-inset-bottom)); text-align: center; border-top: 1px solid var(--card-br); }
.footer-logo { width: 96px; height: 96px; border-radius: 50%; margin: 0 auto 12px; box-shadow: 0 0 0 2px rgba(212, 168, 79, .55), 0 10px 30px rgba(17, 17, 17, .18); }
.footer .fbrand { font-family: var(--serif); font-style: italic; font-weight: 600; font-size: 30px; color: var(--text-0); }
.footer .ftag { margin-top: 2px; font: 600 11px var(--sans); letter-spacing: .3em; text-transform: uppercase; color: var(--pink); }
.footer .frow { margin-top: 8px; color: var(--text-2); font-size: 11.5px; letter-spacing: .14em; text-transform: uppercase; }
.footer .fgold { color: var(--gold-dim); }
.footer-logo-link { display: inline-block; border-radius: 50%; }
.fnav { margin-top: 16px; display: flex; flex-wrap: wrap; align-items: center; justify-content: center; gap: 10px; }
.fnav a { color: var(--text-0); font: 700 12.5px var(--sans); text-decoration: none; min-height: 44px; display: inline-flex; align-items: center; }
.fnav a:hover { color: var(--pink-d); }
.fnav span { color: var(--card-br); }
.fcopy { margin-top: 18px; font-size: 10.5px; letter-spacing: .08em; color: var(--text-2); }

/* instagram links */
.ig-link {
  display: grid; place-items: center; width: 36px; height: 36px; border-radius: 50%; flex: 0 0 auto;
  border: 1px solid rgba(212, 168, 79, .45); color: var(--gold);
  transition: transform .25s ease, border-color .25s ease, background .25s ease, color .25s ease;
}
.ig-link svg { width: 17px; height: 17px; }
.ig-link:hover { border-color: var(--pink); background: rgba(232, 90, 155, .12); color: var(--pink); transform: translateY(-1px) scale(1.05); }
.ig-pill {
  display: inline-flex; align-items: center; gap: 9px; margin-top: 16px; padding: 10px 20px;
  border-radius: 999px; border: 1px solid rgba(212, 168, 79, .5); background: #FFFFFF;
  font: 700 12.5px var(--sans); color: var(--text-0); text-decoration: none;
  box-shadow: 0 4px 14px rgba(212, 168, 79, .18);
  transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease;
}
.ig-pill svg { width: 17px; height: 17px; color: var(--pink); }
.ig-pill:hover { transform: translateY(-2px); box-shadow: 0 10px 24px rgba(232, 90, 155, .25); border-color: var(--pink); }
.ig-pill span { color: var(--pink-d); }

/* ============================== MISC =================================== */
.toast {
  position: fixed; z-index: 130; left: 50%; bottom: calc(88px + env(safe-area-inset-bottom));
  transform: translate(-50%, 24px); padding: 11px 20px; border-radius: 999px;
  background: rgba(17, 17, 17, .94); border: 1px solid rgba(212, 168, 79, .55); color: #FFF9F5;
  font: 600 12.5px var(--sans); letter-spacing: .04em; opacity: 0; pointer-events: none;
  transition: opacity .3s ease, transform .3s ease; backdrop-filter: blur(8px);
}
.toast.show { opacity: 1; transform: translate(-50%, 0); }

/* OS "reduce motion": intentionally NOT auto-obeyed any more — Windows often
   ships with animations reduced, which made the whole site look static.
   Animations stay ON by default; the ☰ menu switch (html/body.fx-off below)
   turns absolutely everything off when the user wants it. */

/* more-details hover affordance */
.more-details:hover { color: var(--pink); }

/* =========================================================================
   MOTION SUITE v2.1 — every effect is transform/opacity only (GPU-composited,
   no layout, no paint) so it stays smooth on weak GPUs and cheap CPUs.
   Device tiering: body gets fx-0 / fx-1 / fx-2 from scripts.py.
   ========================================================================= */
/* hero title: gentle continuous float (one composited layer each) */
@keyframes heroFloat { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
.hero-title .shimmer { animation: shimmer 6.5s ease-in-out infinite, heroFloat 7s ease-in-out 1s infinite; }

/* --- Sparkle field (fx-1+) — hero-anchored, twinkle 0.25 -> full gold ---- */
.fx-1 .spark, .fx-2 .spark { position: absolute; z-index: 1; width: 7px; height: 7px; pointer-events: none;
  background: var(--gold-hi); border-radius: 50%; box-shadow: 0 0 14px 4px rgba(228, 188, 107, .9);
  animation: sparkTwinkle 3.2s ease-in-out infinite; will-change: transform, opacity; }
.fx-1 .spark.s2, .fx-2 .spark.s2 { width: 5px; height: 5px; animation-delay: -1.1s; }
.fx-1 .spark.s3, .fx-2 .spark.s3 { width: 6px; height: 6px; animation-delay: -2.2s; }
@keyframes sparkTwinkle { 0%, 100% { opacity: .25; transform: scale(.7); } 50% { opacity: 1; transform: scale(1.5); } }

/* --- Scroll cue (fx-1+) -------------------------------------------------- */
.scroll-cue { position: relative; margin: 26px auto 0; width: 24px; height: 40px; border: 2px solid var(--gold-dim);
  border-radius: 14px; display: flex; justify-content: center; padding-top: 7px; }
.scroll-cue .dot { width: 4px; height: 8px; border-radius: 3px; background: var(--gold);
  animation: cueDrop 1.6s cubic-bezier(.4, 0, .2, 1) infinite; will-change: transform, opacity; }
@keyframes cueDrop { 0% { opacity: 0; transform: translateY(0); } 28% { opacity: 1; } 72% { opacity: 1; } 100% { opacity: 0; transform: translateY(14px); } }
.fx-0 .scroll-cue { display: none; }

/* --- Reveal-on-scroll (fx-1+) -------------------------------------------- */
.fx-1 .rv, .fx-2 .rv { opacity: 0; transform: translateY(22px); transition: opacity .7s ease, transform .7s cubic-bezier(.22,1,.36,1); }
.fx-1 .rv.in, .fx-2 .rv.in { opacity: 1; transform: none; }
.fx-0 .rv { opacity: 1; transform: none; }

/* --- Staggered children --------------------------------------------------- */
.fx-1 .stagger > *, .fx-2 .stagger > * { opacity: 0; transform: translateY(16px); transition: opacity .55s ease, transform .55s cubic-bezier(.22,1,.36,1); }
.fx-1 .stagger.in > *, .fx-2 .stagger.in > * { opacity: 1; transform: none; }
.fx-0 .stagger > * { opacity: 1; transform: none; }

/* --- Desktop tilt-grade hover (fx-2 only) --------------------------------- */
.fx-2 .card { transition: opacity .6s ease, transform .35s cubic-bezier(.22,1,.36,1), box-shadow .3s ease, border-color .3s ease; }
.fx-2 .card:hover { transform: translateY(-6px) scale(1.012); }
.fx-2 .card:hover .card-img-wrap img { transform: scale(1.07); }
.fx-2 .card-plus { transition: transform .22s cubic-bezier(.34,1.6,.5,1); }
.fx-2 .card:hover .card-plus { transform: rotate(90deg) scale(1.12); }
.fx-2 .marquee-item:hover { transform: translateY(-4px) rotate(-1deg) scale(1.03); }

/* --- Topbar scroll-progress bar (all tiers) -------------------------------- */
.scroll-progress { position: fixed; top: 0; left: 0; height: 3px; width: 100%; z-index: 210;
  transform: scaleX(0); transform-origin: 0 50%; background: var(--pink-grad);
  pointer-events: none; will-change: transform; }

/* --- Page-enter for overlays (all tiers) -----------------------------------
   IMPORTANT: the sheet's resting transform is the desktop centring
   translate(-50%,-50%), so it must only ever animate OPACITY — a transform
   keyframe with `to { transform: none }` would leave it stuck to the
   bottom-right corner (the clipped-sheet bug). Cart/modal rest at identity
   transforms, so they can safely use the rise-in. --------------------------- */
@keyframes layerEnter { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: none; } }
@keyframes sheetFade { from { opacity: 0; } to { opacity: 1; } }
.sheet-layer.open .sheet { animation: sheetFade .32s ease both; }
.cart-layer.open .cart { animation: layerEnter .38s cubic-bezier(.22,1,.36,1) both; }
.modal-layer.open .modal { animation: layerEnter .34s cubic-bezier(.22,1,.37,1) both; }

/* --- Animations OFF switch (body.fx-off): the menu toggle controls this --- */
html.fx-off { scroll-behavior: auto; }
body.fx-off *, body.fx-off *::before, body.fx-off *::after { animation-duration: .01ms !important; animation-iteration-count: 1 !important; transition-duration: .01ms !important; }
body.fx-off .shimmer { -webkit-text-fill-color: var(--text-0); animation: none; }
body.fx-off .marquee-track { animation: none; }
body.fx-off .card { opacity: 1; transform: none; }
body.fx-off .bfly { display: none; }
body.fx-off .hero-price { animation: none; }
body.fx-off .spark, body.fx-off .scroll-cue, body.fx-off .scroll-progress { display: none; }
body.fx-off .combo-row, body.fx-off .rv, body.fx-off .stagger > * { opacity: 1 !important; transform: none !important; }
body.fx-off .sheet-layer.open .sheet, body.fx-off .cart-layer.open .cart, body.fx-off .modal-layer.open .modal { animation: none; }
body.fx-off .toast { transition: opacity .3s ease; transform: translate(-50%, 8px); }
body.fx-off .toast.show { transform: translate(-50%, 0); }

/* --- FX toggle row in the menu ------------------------------------------- */
.fx-state { font: 800 10.5px var(--sans); letter-spacing: .08em; color: #111111; background: var(--gold);
  border-radius: 999px; padding: 3px 10px; min-width: 34px; text-align: center; }
.fx-toggle[aria-checked="false"] .fx-state { background: var(--card-br); color: var(--text-1); }

/* ============================ A11Y POLISH =============================== */
:focus-visible { outline: 3px solid var(--pink); outline-offset: 2px; border-radius: 6px; }
.cart-note, .size-note { color: var(--text-1); }
.card-type, .hero-eyebrow, .combo-kicker, .visit-kicker { color: #8A6B23; }
.cr-qty small { color: var(--text-1); }
.trust span { color: var(--text-0); border-color: rgba(212, 168, 79, .45); }
.ci-del { min-height: 44px; padding: 0 8px; }
.ig-link { width: 40px; height: 40px; }
@media (min-width: 900px) { .page-back { margin-top: 6px; } }
"""
