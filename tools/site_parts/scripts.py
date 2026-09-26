# -*- coding: utf-8 -*-
"""Chinnari page logic — carousel, sheets, cart, WhatsApp checkout."""

JS = r"""
'use strict';
const $  = (s, el=document) => el.querySelector(s);
const $$ = (s, el=document) => [...el.querySelectorAll(s)];
const RS = '\u20B9';
const WA_NUMBER = '916375101619';
const fmt = n => RS + n.toLocaleString('en-IN');

/* ------------------------------ state ------------------------------ */
let cart = [];           // {id, name, type, hexName, hex, price, qty, img}
let activeFilter = 'all';
let searchTerm = '';
const PRODUCTS = window.CHINNARI_PRODUCTS;
const IMGS = window.CHINNARI_IMGS;
const LQIPS = window.CHINNARI_LQIP;

/* resolve image keys -> embedded data URIs */
PRODUCTS.forEach(p => {
  if (p.colors) p.colors.forEach(c => {
    const keys = c.imgKeys || [c.imgKey];
    c.photos = keys.map(k => ({ img: IMGS[k], lqip: LQIPS[k] }));
    c.img = c.photos[0].img; c.lqip = c.photos[0].lqip;
  });
  else { p.img = IMGS[p.imgKey]; p.lqip = LQIPS[p.imgKey]; }
});

/* ------------------------------ routing ------------------------------ */
function showPage(name) {
  const home = !name || name === 'home';
  document.getElementById('pagePrivacy').hidden = name !== 'privacy';
  document.getElementById('page404').hidden = name !== '404';
  [...document.querySelectorAll('.topbar, .delivery-strip, .hero, .marquee, .jump-row, .sticky-bar, .grid, .combo, .delivery-info, .visit, .footer, .cartbar')].forEach(el => {
    el.style.display = home ? '' : 'none';
  }
  );
  document.body.style.overflow = home ? '' : 'hidden';
  if (home) {
    /* belt-and-braces: never leave the page locked or a ghost layer open */
    document.body.style.pointerEvents = '';
    document.body.classList.remove('nav-open', 'modal-open');
    ['#sheetLayer', '#cartLayer', '#sizeLayer', '#navLayer'].forEach(s => {
      const l = $(s); if (!l) return;
      l.classList.remove('open');
      l.setAttribute('aria-hidden', 'true');
      l.style.pointerEvents = 'none';
    });
  }
  window.scrollTo({ top: 0, behavior: 'instant' });
  return home;
}
let currentPage = null;
function route() {
  const h = (location.hash || '').replace(/^#\/?/, '');
  let page = 'home';
  if (h === 'privacy' || h === '/privacy') page = 'privacy';
  else if (h && !['top', 'grid', 'combos', 'delivery', 'visit'].includes(h)) {
    if (/^p\d+$/.test(h)) page = 'home';
    else page = '404';
  }
  /* same view: let the browser's native anchor scroll happen undisturbed */
  if (page === currentPage) return;
  currentPage = page;
  showPage(page);
}
window.addEventListener('hashchange', route);

/* ------------------------------ helpers ------------------------------ */
function showToast(msg) {
  const t = $('#toast');
  t.textContent = msg;
  t.classList.add('show');
  clearTimeout(showToast._h);
  showToast._h = setTimeout(() => t.classList.remove('show'), 1600);
}
function announce(msg) { showToast(msg); }

/* --------------------- overlay focus management ---------------------- */
let lastFocus = null;
function trapTab(e, layer) {
  if (e.key !== 'Tab') return;
  const f = [...layer.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])')]
    .filter(el => el.offsetParent !== null || el === document.activeElement);
  if (!f.length) return;
  const first = f[0], last = f[f.length - 1];
  if (e.shiftKey && document.activeElement === first) { last.focus(); e.preventDefault(); }
  else if (!e.shiftKey && document.activeElement === last) { first.focus(); e.preventDefault(); }
}
function onKeydown(e) {
  if (e.key === 'Escape') {
    if ($('#sizeLayer').classList.contains('open')) return closeSizeChart();
    if ($('#cartLayer').classList.contains('open')) return closeCart();
    if ($('#navLayer').classList.contains('open')) return closeNav();
    if ($('#sheetLayer').classList.contains('open')) return closeSheet();
    return;
  }
  if ($('#sizeLayer').classList.contains('open')) return trapTab(e, $('#sizeLayer'));
  if ($('#cartLayer').classList.contains('open')) return trapTab(e, $('#cartLayer'));
  if ($('#navLayer').classList.contains('open')) return trapTab(e, $('#navLayer'));
  if ($('#sheetLayer').classList.contains('open')) return trapTab(e, $('#sheetLayer'));
}

/* ------------------------------ cart core ------------------------------ */
const findLine = id => cart.find(l => l.id === id);

function addToCart(p, colorObj, qty, size) {
  const id = p.colors ? (p.id + '::' + colorObj.name + '::' + (size || '')) : (p.id + '::' + (size || ''));
  const line = findLine(id);
  if (line) { line.qty += qty; }
  else {
    cart.push({
      id, name: p.name, type: p.type, size: size || null,
      hexName: colorObj ? colorObj.name : null,
      hex: colorObj ? colorObj.hex : (p.hex || null),
      price: 550, qty, img: (colorObj && colorObj.photos) ? colorObj.photos[0].img : p.img
    });
  }
  saveCart(); renderCart(); bumpCartbar();
}
function setQty(id, q) {
  const line = findLine(id);
  if (!line) return;
  line.qty = q;
  if (line.qty <= 0) cart = cart.filter(l => l.id !== id);
  saveCart(); renderCart();
}
function saveCart() { try {  localStorage.setItem('kc-collection-cart', JSON.stringify(cart)); } catch(e){} }
function loadCart() { try {  cart = JSON.parse(localStorage.getItem('kc-collection-cart') || '[]'); } catch(e){ cart = []; } }
const cartCount = () => cart.reduce((s,l) => s + l.qty, 0);
const cartTotal = () => cart.reduce((s,l) => s + l.qty * l.price, 0);
const totalQty = () => cartCount();

/* ------------------------------ header/cartbar ------------------------------ */
function renderCartbar() {
  const n = cartCount(), bar = $('#cartbar');
  $('#cbCount').textContent = n;
  $('#cbItems').textContent = n === 1 ? '1 dress' : n + ' dresses';
  $('#cbTotal').textContent = fmt(cartTotal());
  bar.classList.toggle('show', n > 0);
}
function bumpCartbar() {
  renderCartbar();
  const bar = $('#cartbar');
  bar.classList.remove('bump'); void bar.offsetWidth; bar.classList.add('bump');
}

/* ------------------------------ grid ------------------------------ */
function cardHTML(p) {
  const key = p.colors ? p.colors[0].imgKey : p.imgKey;
  const img = p.colors ? p.colors[0].img : p.img;
  const hex = p.colors ? p.colors[0].hex : p.hex;
  const swatches = p.colors
    ? `<div class="card-swatches">${p.colors.map(c => `<span class="card-swatch" style="background:${c.hex}"></span>`).join('')}</div>`
    : '';
  const badge = p.badge ? `<div class="card-badge">${p.badge}</div>` : '';
  return `
  <article class="card" data-id="${p.id}" data-name="${p.name.toLowerCase()} ${p.type.toLowerCase()} ${p.colors ? p.colors.map(c=>c.name.toLowerCase()).join(' ') : ''}">
    <div class="card-img-wrap" style="background-image:url(${LQIPS[key]})">
      ${badge}
      ${swatches}
      <div class="card-veil"></div>
      <img loading="lazy" src="${img}" alt="${p.name}">
    </div>
    <div class="card-body">
      <h3 class="card-name">${p.name}</h3>
      <div class="card-type">${p.type}</div>
      <div class="card-row">
        <div class="card-price"><span class="cur">${RS}</span>550</div>
        <button class="card-plus" aria-label="Add ${p.name} to cart">+</button>
      </div>
    </div>
  </article>`;
}

function applyFilters() {
  let shown = 0;
  $$('.card').forEach(card => {
    const p = PRODUCTS.find(x => x.id === card.dataset.id);
    const matchSearch = !searchTerm || card.dataset.name.includes(searchTerm);
    let matchFilter = true;
    if (activeFilter === 'colors') matchFilter = !!p.colors;
    else if (activeFilter.startsWith('c:')) matchFilter = (p.colors || []).some(c => c.name.toLowerCase() === activeFilter.slice(2));
    const match = matchSearch && matchFilter;
    card.style.display = match ? '' : 'none';
    if (match) shown++;
  });
  $('#noRes').style.display = shown ? 'none' : '';
  requestAnimationFrame(watchCards);
}

function buildChips() {
  const colorNames = new Set();
  PRODUCTS.forEach(p => (p.colors || []).forEach(c => colorNames.add(c.name)));
  const chipBar = $('#chips');
  let html = `<button class="chip on" data-f="all">All ${PRODUCTS.length}</button>
              <button class="chip" data-f="colors">&#10022; Colour Options</button>`;
  [...colorNames].sort().forEach(cn => {
    html += `<button class="chip" data-f="c:${cn.toLowerCase()}"><span class="cdot" style="background:${(PRODUCTS.flatMap(p=>p.colors||[]).find(c=>c.name===cn)||{}).hex}"></span>${cn}</button>`;
  });
  chipBar.innerHTML = html;
  chipBar.addEventListener('click', e => {
    const chip = e.target.closest('.chip');
    if (!chip) return;
    $$('.chip').forEach(c => c.classList.remove('on'));
    chip.classList.add('on');
    activeFilter = chip.dataset.f;
    applyFilters();
  });
}

/* fade/lift-in on scroll */
let io;
function watchCards() {
  if (!('IntersectionObserver' in window)) { $$('.card').forEach(c => c.classList.add('in')); return; }
  if (!io) {
    io = new IntersectionObserver(entries => {
      entries.forEach(en => {
        if (en.isIntersecting) {
          const i = +en.target.dataset.seq || 0;
          en.target.style.transitionDelay = Math.min(i, 5) * 45 + 'ms';
          en.target.classList.add('in');
          /* keep hover snappy: after the reveal finishes, drop the stagger delay */
          const el = en.target;
          setTimeout(() => { el.style.transitionDelay = '0ms'; }, 1000);
          io.unobserve(en.target);
        }
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: .08 });
  }
  $$('.card:not(.in)').forEach((c, i) => { c.dataset.seq = i; io.observe(c); });
}

/* ------------------------------ combo pricing ------------------------------ */
const COMBOS = [
  { q: 1,  price: 550  },
  { q: 2,  price: 999  },
  { q: 3,  price: 1200 },
  { q: 4,  price: 1450 },
  { q: 5,  price: 1750 },
  { q: 6,  price: 2050 },
  { q: 7,  price: 2350 },
  { q: 8,  price: 2750 },
  { q: 9,  price: 3000 },
  { q: 10, price: 3250 },
];
const comboFor = q => COMBOS.slice().reverse().find(c => q >= c.q) || COMBOS[0];

function buildComboTable() {
  const wrap = $('#comboTable');
  if (!wrap) return;
  wrap.insertAdjacentHTML('beforeend', COMBOS.map((c, i) => {
    const save = 550 * c.q - c.price;
    const best = c.q === 10;
    return `
    <div class="combo-row${best ? ' best' : ''}" data-i="${i}">
      ${best ? '<span class="cr-badge">Best Value</span>' : ''}
      <div class="cr-qty"><span class="cr-dot">${c.q}</span><b>${c.q} ${c.q === 1 ? 'Dress' : 'Dresses'}</b><small>combo ${i + 1}</small></div>
      <div class="cr-price">${fmt(c.price)}</div>
      <div class="cr-save${save ? '' : ' cr-zero'}">${save ? 'save ' + fmt(save) : '&mdash;'}</div>
    </div>`;
  }).join(''));
  /* staggered fade+rise on scroll */
  if (!('IntersectionObserver' in window)) { $$('.combo-row').forEach(r => r.classList.add('in')); return; }
  const io2 = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (en.isIntersecting) {
        const i = +en.target.dataset.i;
        en.target.style.transitionDelay = Math.min(i, 9) * 55 + 'ms';
        en.target.classList.add('in');
        io2.unobserve(en.target);
      }
    });
  }, { rootMargin: '0px 0px -6% 0px', threshold: .1 });
  $$('.combo-row').forEach(r => io2.observe(r));
}

/* ------------------------------ sizes ------------------------------ */
const SIZES = ['XS', 'S', 'M', 'L', 'XL', 'XXL'];
let sheetSize = null;

function renderSizes() {
  const row = $('#sizeRow');
  sheetSize = null;
  row.innerHTML = SIZES.map(s => `<button class="size-chip" data-size="${s}" type="button" aria-pressed="false">${s}</button>`).join('');
}

function bindSizeChart() {
  $('#sizeRow').addEventListener('click', e => {
    const b = e.target.closest('.size-chip');
    if (!b) return;
    $$('#sizeRow .size-chip').forEach(x => { x.classList.remove('on', 'pop'); x.setAttribute('aria-pressed', 'false'); });
    b.classList.add('on', 'pop');
    b.setAttribute('aria-pressed', 'true');
    sheetSize = b.dataset.size;
  });
  const open = () => openSizeChart();
  const close = () => closeSizeChart();
  $('#sizeChartBtn').addEventListener('click', open);
  $('#sizeX').addEventListener('click', close);
  $('#sizeScrim').addEventListener('click', close);
}

/* ------------------------------ mobile nav ------------------------------ */
function openNav() { const l = $('#navLayer'); l.classList.add('open'); l.setAttribute('aria-hidden', 'false'); document.body.classList.add('nav-open'); document.body.style.overflow = 'hidden'; $('#menuBtn').setAttribute('aria-expanded', 'true'); lastFocus = document.activeElement; setTimeout(() => $('#navX').focus(), 300); }
function closeNav() { const l = $('#navLayer'); l.classList.remove('open'); l.setAttribute('aria-hidden', 'true'); document.body.classList.remove('nav-open'); document.body.style.overflow = ''; $('#menuBtn').setAttribute('aria-expanded', 'false'); if (lastFocus) { lastFocus.focus(); lastFocus = null; } }

/* ------------------------------ size chart ------------------------------ */
function openSizeChart() { const l = $('#sizeLayer'); l.classList.add('open'); l.setAttribute('aria-hidden', 'false'); l.style.pointerEvents = 'auto'; lastFocus = document.activeElement; setTimeout(() => $('#sizeX').focus(), 300); }
function closeSizeChart() { const l = $('#sizeLayer'); l.classList.remove('open'); l.setAttribute('aria-hidden', 'true'); l.style.pointerEvents = 'none'; if (lastFocus) { lastFocus.focus(); lastFocus = null; } }

/* ------------------------------ product sheet ------------------------------ */
let sheetP = null, sheetColor = null, carIdx = 0, drag = null;

function openSheet(id) {
  sheetP = PRODUCTS.find(p => String(p.id) === String(id));
  if (!sheetP) return;
  sheetColor = sheetP.colors ? sheetP.colors[0] : null;
  carIdx = 0;
  renderSheet();
  const layer = $('#sheetLayer');
  layer.classList.add('open');
  layer.setAttribute('aria-hidden', 'false');
  layer.style.pointerEvents = 'auto';
  document.body.style.overflow = 'hidden';
  document.body.classList.add('modal-open');
  lastFocus = document.activeElement;
  $('.sheet-scroll').scrollTop = 0;
  setTimeout(() => $('#sheetClose').focus(), 350);
}
function closeSheet() {
  const layer = $('#sheetLayer');
  layer.classList.remove('open');
  layer.setAttribute('aria-hidden', 'true');
  layer.style.pointerEvents = 'none';
  document.body.style.overflow = '';
  document.body.classList.remove('modal-open');
  drag = null;
  if (lastFocus) { lastFocus.focus(); lastFocus = null; }
}

function carouselSlides() {
  return sheetP.colors ? sheetColor.photos : [{ img: sheetP.img, lqip: sheetP.lqip }];
}

function renderCarousel() {
  const slides = carouselSlides();
  carIdx = Math.max(0, Math.min(carIdx, slides.length - 1));
  $('#car').classList.toggle('single', slides.length < 2);
  $('#carTrack').innerHTML = slides.map((s, i) =>
    `<div class="car-slide${i === carIdx ? ' on' : ''}" style="background-image:url(${s.lqip || ''})"><img src="${s.img}" alt="${sheetP.name}"></div>`).join('');
  $('#carDots').innerHTML = slides.map((s, i) =>
    `<button class="car-dot${i === carIdx ? ' on' : ''}" type="button" aria-label="Go to image ${i + 1} of ${slides.length}"${i === carIdx ? ' aria-current="true"' : ''}></button>`).join('');
  const tag = $('#carTag');
  if (sheetP.colors) {
    tag.style.display = '';
    tag.textContent = sheetColor.name;
    tag.style.background = sheetColor.hex;
    tag.style.color = pickText(sheetColor.hex);
  } else {
    tag.style.display = 'none';
  }
}

function pickText(hex) {
  const r = parseInt(hex.slice(1,3),16), g = parseInt(hex.slice(3,5),16), b = parseInt(hex.slice(5,7),16);
  return (r*.299 + g*.587 + b*.114) > 150 ? '#0A1812' : '#F5EFE3';
}

function showSlide(i) {
  const slides = $$('#carTrack .car-slide');
  if (!slides.length) return;
  carIdx = (i + slides.length) % slides.length;
  slides.forEach((s, k) => s.classList.toggle('on', k === carIdx));
  $$('#carDots .car-dot').forEach((d, k) => d.classList.toggle('on', k === carIdx));
}

function renderSheet() {
  const p = sheetP;
  $('#pdName').textContent = p.name;
  $('#pdType').textContent = p.type;
  $('#pdDesc').textContent = p.desc;
  $('#btnAddTotal').textContent = fmt(550 * (+$('#pdQty').textContent));

  /* swatches */
  const swWrap = $('#pdSwatches');
  if (p.colors) {
    $('#swLabel').style.display = '';
    swWrap.style.display = '';
    swWrap.innerHTML = p.colors.map((c, i) =>
      `<button class="swatch${c === sheetColor ? ' on' : ''}" data-i="${i}" style="background:${c.hex}" aria-label="Colour ${c.name}" aria-pressed="${c === sheetColor}"></button>`).join('');
    $('#swName').textContent = sheetColor.name;
  } else {
    $('#swLabel').style.display = 'none';
    swWrap.style.display = 'none';
    $('#swName').textContent = '';
  }
  renderCarousel();
  renderSizes();
  $('#pdQty').textContent = '1';
}

/* carousel swipe */
function bindCarousel() {
  const car = $('#car');
  car.addEventListener('pointerdown', e => {
    drag = { x: e.clientX, t: Date.now(), w: car.clientWidth };
    car.setPointerCapture(e.pointerId);
  });
  car.addEventListener('pointerup', e => {
    if (!drag) return;
    const dx = e.clientX - drag.x, dt = Date.now() - drag.t;
    if (Math.abs(dx) > drag.w * .18 || (Math.abs(dx) > 28 && dt < 260)) showSlide(carIdx + (dx < 0 ? 1 : -1));
    drag = null;
  });
  car.addEventListener('pointercancel', () => drag = null);
  $('.car-nav.prev').addEventListener('click', () => showSlide(carIdx - 1));
  $('.car-nav.next').addEventListener('click', () => showSlide(carIdx + 1));
  $('#carDots').addEventListener('click', e => {
    const d = e.target.closest('.car-dot');
    if (!d) return;
    showSlide([...$('#carDots').children].indexOf(d));
  });
}

/* swatch + qty events */
function bindSheet() {
  $('#pdSwatches').addEventListener('click', e => {
    const b = e.target.closest('.swatch');
    if (!b || !sheetP.colors) return;
    const c = sheetP.colors[+b.dataset.i];
    if (c === sheetColor) return;
    sheetColor = c;
    carIdx = 0;
    $$('#pdSwatches .swatch').forEach(x => { x.classList.remove('on', 'pop'); x.setAttribute('aria-pressed', 'false'); });
    b.classList.add('on', 'pop');
    b.setAttribute('aria-pressed', 'true');
    $('#swName').textContent = c.name;
    renderCarousel();
  });
  $('#qtyMinus').addEventListener('click', () => {
    const q = Math.max(1, +$('#pdQty').textContent - 1);
    $('#pdQty').textContent = q;
    $('#btnAddTotal').textContent = fmt(550 * q);
  });
  $('#qtyPlus').addEventListener('click', () => {
    const q = Math.min(10, +$('#pdQty').textContent + 1);
    $('#pdQty').textContent = q;
    $('#btnAddTotal').textContent = fmt(550 * q);
  });
  $('#btnAdd').addEventListener('click', () => {
    const qty = +$('#pdQty').textContent;
    addToCart(sheetP, sheetColor, qty, sheetSize);
    const b = $('#btnAdd');
    b.classList.remove('added'); void b.offsetWidth; b.classList.add('added');
  });
  $('#btnWa').addEventListener('click', () => {
    const qty = +$('#pdQty').textContent;
    const colorPart = sheetP.colors ? `\nColor: *${sheetColor.name}*` : '';
    const sizePart = sheetSize ? `\nSize: *${sheetSize}*` : '';
    const combo = comboFor(qty);
    const priceLine = combo.q < qty
      ? `\n\nCombo price for ${qty}: *${fmt(combo.price + 550 * (qty - combo.q))}* (I'll confirm on WhatsApp)`
      : `\nCombo price: *${fmt(combo.price)}*`;
    const msg =
`Hello Ankita Sharma Collection! I'd like to order:

*${sheetP.name}* (${sheetP.type})${colorPart}${sizePart}
Qty: ${qty}  x  ${RS}550
${priceLine}

Is this available?`;
    window.open('https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(msg), '_blank');
  });
  $('#sheetClose').addEventListener('click', closeSheet);
  $('#sheetScrim').addEventListener('click', closeSheet);
  $('#moreDetails').addEventListener('click', function () {
    const open = this.classList.toggle('open');
    this.setAttribute('aria-expanded', String(open));
    $('#morePanel').classList.toggle('open');
  });
  bindDragToClose();
}

/* drag-to-close the bottom sheet */
function bindDragToClose() {
  const grab = $('#sheetGrab'), sheet = $('#sheet'), scroll = $('#sheetScroll');
  let y0 = null, dy = 0, dragging = false;
  const start = e => { dragging = true; y0 = e.clientY; sheet.style.transition = 'none'; };
  grab.addEventListener('pointerdown', start);
  grab.addEventListener('pointermove', e => {
    if (!dragging) return;
    dy = Math.max(0, e.clientY - y0);
    sheet.style.transform = `translateY(${dy}px)`;
  });
  const end = () => {
    if (!dragging) return;
    dragging = false;
    sheet.style.transition = '';
    sheet.style.transform = '';
    if (dy > 110) closeSheet();
    dy = 0;
  };
  grab.addEventListener('pointerup', end);
  grab.addEventListener('pointercancel', end);
}

/* ------------------------------ cart sheet ------------------------------ */
function openCart() { const l = $('#cartLayer'); l.classList.add('open'); l.setAttribute('aria-hidden', 'false'); l.style.pointerEvents = 'auto'; document.body.style.overflow = 'hidden'; renderCart(); lastFocus = document.activeElement; setTimeout(() => $('#cartX').focus(), 350); }
function closeCart() { const l = $('#cartLayer'); l.classList.remove('open'); l.setAttribute('aria-hidden', 'true'); l.style.pointerEvents = 'none'; document.body.style.overflow = ''; if (lastFocus) { lastFocus.focus(); lastFocus = null; } }

function renderCart() {
  renderCartbar();
  const wrap = $('#cartItems');
  const n = cartCount();
  $('#cartCountLbl').textContent = n ? (n === 1 ? '1 little dress' : n + ' little dresses') : '';
  if (!cart.length) {
    wrap.innerHTML = `<div class="cart-empty"><div class="big">Your basket is empty</div>Little pattu dreams await below.</div>`;
    $('#cartFoot').style.display = 'none';
    return;
  }
  $('#cartFoot').style.display = '';
  wrap.innerHTML = cart.map(l => `
    <div class="ci" data-id="${l.id}">
      <img class="ci-img" src="${l.img}" alt="${l.name}">
      <div>
        <div class="ci-name">${l.name}</div>
        <div class="ci-meta">${l.hex ? `<span class="cdot" style="background:${l.hex}"></span>${l.hexName}` : ''}<span>${l.size ? 'Size ' + l.size : ''}</span><span>${l.type}</span></div>
        <div class="ci-qty">
          <button data-act="dec" aria-label="Decrease">&#8722;</button><b>${l.qty}</b><button data-act="inc" aria-label="Increase">+</button>
        </div>
      </div>
      <div class="ci-right">
        <div class="ci-price">${fmt(l.qty * 550)}</div>
        <button class="ci-del" data-act="del">Remove</button>
      </div>
    </div>`).join('');
  $('#cartTotal').textContent = fmt(cartTotal());
  const sv = $('#cartSave');
  const combo = comboFor(totalQty());
  const saving = cartTotal() - combo.price;
  sv.textContent = saving > 0 ? `\u2726 Combo price applied: ${fmt(combo.price)} — you save ${fmt(saving)}` : (totalQty() >= 2 ? '' : '\u2726 Buy 2+ for combo savings — see the pricing table');
}

function bindCart() {
  $('#cartItems').addEventListener('click', e => {
    const b = e.target.closest('button[data-act]');
    if (!b) return;
    const id = b.closest('.ci').dataset.id;
    const line = findLine(id);
    if (b.dataset.act === 'inc') setQty(id, line.qty + 1);
    if (b.dataset.act === 'dec') setQty(id, line.qty - 1);
    if (b.dataset.act === 'del') setQty(id, 0);
  });
  $('#cartX').addEventListener('click', closeCart);
  $('#cartScrim').addEventListener('click', closeCart);
  $('#btnCheckout').addEventListener('click', () => {
    const lines = cart.map(l =>
      `\u2022 ${l.name}${l.hexName ? ` (${l.hexName})` : ''} x${l.qty} = ${fmt(l.qty * 550)}`);
    const total = cartTotal();
    const combo = comboFor(totalQty());
    const comboNote = combo.price < total
      ? `\n\nCombo discount applies: *${fmt(combo.price)}* instead of ${fmt(total)} (I'll confirm final price on WhatsApp).`
      : '';
    const msg =
`Hello Ankita Sharma Collection! New order:

${lines.join('\n')}

*Order total: ${fmt(total)}*${comboNote}

I understand: prepaid only (no COD), all-India delivery.

Name:
Delivery address:
Size(s) if any:`;
    window.open('https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(msg), '_blank');
  });
}

/* ============================ MOTION SUITE (v2.1) ============================
   Device tiering: every effect is transform/opacity only (GPU-composited), and
   how much of the suite runs depends on the device. fx-0 = calm, fx-1 = standard
   (phones), fx-2 = full (desktops). Each step is individually guarded so a
   failure in one can never break the page. */
const FX = {
  tier: 1,
  init() {
    const cores = navigator.hardwareConcurrency || 4;
    const hover = matchMedia('(hover: hover) and (pointer: fine)').matches;
    /* animations are ON by default on every device; only very weak hardware drops to the base tier.
       (OS "reduce motion" no longer disables them — the user controls it via the menu toggle.) */
    this.tier = (hover && cores >= 4) ? 2 : 1;
    return this.tier;
  }
};

function initMotion() {
  const tier = FX.init();
  let off = false;
  try { off = localStorage.getItem('ankita-fx') === 'off'; } catch (e) {}
  if (off) { setFxOff(true); return; }
  document.body.classList.add('fx-' + tier);
  try { initSparkles(); } catch (e) {}
  try { initScrollCue(); } catch (e) {}
  try { initReveals(); } catch (e) {}
  try { initProgress(); } catch (e) {}
  try { initParallax(); } catch (e) {}
}

/* --- animations On/Off switch (in the ☰ menu, remembered on the device) ---- */
function setFxOff(off) {
  document.body.classList.toggle('fx-off', off);
  document.documentElement.classList.toggle('fx-off', off);
  try { localStorage.setItem('ankita-fx', off ? 'off' : 'on'); } catch (e) {}
  const t = $('#fxToggle'), s = $('#fxState');
  if (t) t.setAttribute('aria-checked', String(!off));
  if (s) s.textContent = off ? 'OFF' : 'ON';
  if (!off) { try { initSparkles(); } catch (e) {} }
}
function toggleFx() {
  setFxOff(!document.body.classList.contains('fx-off'));
  showToast(document.body.classList.contains('fx-off') ? 'Animations off' : 'Animations on \u2726');
}

/* --- twinkling gold sparkles in the hero ---------------------------------- */
function initSparkles() {
  const hero = document.querySelector('.hero');
  if (!hero || document.querySelector('.spark')) return;
  const spots = [[8, 22], [22, 60], [12, 88], [84, 18], [94, 52], [78, 82], [50, 8], [62, 95], [38, 4], [30, 92]];
  spots.forEach(([top, left], i) => {
    const s = document.createElement('div');
    s.className = 'spark' + (i % 3 === 1 ? ' s2' : i % 3 === 2 ? ' s3' : '');
    s.style.top = top + '%';
    s.style.left = left + '%';
    hero.appendChild(s);
  });
}

/* --- animated scroll cue under the hero ----------------------------------- */
function initScrollCue() {
  if (document.querySelector('.scroll-cue')) return;
  const el = document.createElement('div');
  el.className = 'scroll-cue';
  el.setAttribute('aria-hidden', 'true');
  el.innerHTML = '<span class="dot"></span>';
  const anchor = document.querySelector('.hero-price');
  if (anchor && anchor.parentNode) anchor.parentNode.insertBefore(el, anchor.nextSibling);
}

/* --- reveal-on-scroll for combo table, visit card, delivery card, footer --- */
function initReveals() {
  const targets = document.querySelectorAll('.combo-row, .visit-card, .delivery-info .faq-card, .footer');
  targets.forEach(el => el.classList.add('rv'));
  if (!('IntersectionObserver' in window)) { targets.forEach(el => el.classList.add('in')); return; }
  const ro = new IntersectionObserver(entries => {
    entries.forEach(en => {
      if (en.isIntersecting) { en.target.classList.add('in'); ro.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px -6% 0px', threshold: .08 });
  targets.forEach(el => ro.observe(el));
}

/* --- topbar reading-progress bar (rAF-throttled, transform only) ----------- */
function initProgress() {
  const bar = document.createElement('div');
  bar.className = 'scroll-progress';
  bar.setAttribute('aria-hidden', 'true');
  document.body.appendChild(bar);
  let raf = 0;
  const paint = () => {
    raf = 0;
    const max = document.documentElement.scrollHeight - innerHeight;
    bar.style.transform = 'scaleX(' + (max > 0 ? Math.min(1, (scrollY || 0) / max) : 0) + ')';
  };
  addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(paint); }, { passive: true });
  paint();
}

/* --- gentle hero parallax (rAF + transform only, desktops only) ------------ */
function initParallax() {
  if (FX.tier < 2) return;
  const bf = document.querySelector('.bflies');
  if (!bf) return;
  let raf = 0, lastY = -1;
  addEventListener('scroll', () => {
    if (raf) return;
    raf = requestAnimationFrame(() => {
      raf = 0;
      const y = scrollY || 0;
      if (Math.abs(y - lastY) > 2) { lastY = y; bf.style.transform = 'translateY(' + (y * .12) + 'px)'; }
    });
  }, { passive: true });
}

/* hard failsafe: boot screen must die even if something above throws */
setTimeout(() => document.body.classList.add('booted'), 2500);

/* scroll watchdog: if the wheel does nothing because some invisible layer still
   reports an open state, force everything shut and unstick the page. This makes
   "scroll only works on one side" structurally impossible. */
let wheelN = 0, wheelT = 0;
const LAYERS = ['#sheetLayer', '#cartLayer', '#sizeLayer', '#navLayer'];
window.addEventListener('wheel', e => {
  /* wheeling inside a genuinely open layer (sheet/cart/modal/drawer) is normal */
  const inOpen = LAYERS.some(s => { const l = $(s); return l && l.classList.contains('open') && l.contains(e.target); });
  if (inOpen) { wheelN = 0; return; }
  const now = Date.now();
  wheelN = now - wheelT > 700 ? 1 : wheelN + 1;
  wheelT = now;
  if (wheelN < 3) return;
  const ghost = LAYERS
    .some(s => { const l = $(s); return l && (l.classList.contains('open') || l.style.pointerEvents === 'auto'); });
  if (ghost) {
    LAYERS.forEach(s => { const l = $(s); if (!l) return; l.classList.remove('open'); l.style.pointerEvents = 'none'; });
    document.body.style.overflow = '';
    document.body.classList.remove('nav-open', 'modal-open');
    wheelN = 0;
  }
}, { passive: true });

document.addEventListener('DOMContentLoaded', () => {
  loadCart();
  document.body.classList.add('booted');
  route();
  /* build the product grid */
  $('#grid').insertAdjacentHTML('afterbegin', PRODUCTS.map(cardHTML).join(''));
  buildChips();
  watchCards();
  buildComboTable();
  bindSizeChart();
  bindCarousel();
  bindSheet();
  bindCart();
  renderCart();
  initMotion();

  /* grid interactions */
  $('#grid').addEventListener('click', e => {
    const plus = e.target.closest('.card-plus');
    const card = e.target.closest('.card');
    if (!card) return;
    const p = PRODUCTS.find(x => x.id === card.dataset.id);
    if (plus) {
      addToCart(p, p.colors ? p.colors[0] : null, 1, null);
      showToast('Added to basket \u2726');
      plus.textContent = '\u2713';
      plus.style.background = '#3FA06B'; plus.style.color = '#fff'; plus.style.borderColor = 'transparent';
      setTimeout(() => { plus.textContent = '+'; plus.style.background = ''; plus.style.color = ''; plus.style.borderColor = ''; }, 1100);
    } else {
      openSheet(p.id);
    }
  });

  /* marquee strip (doubled for a seamless loop) */
  const MQ = ['p03','p09','p18','p23','p31','p36','p39','p43','p49','p57','p61','p65'];
  $('#marqueeTrack').innerHTML = [...MQ, ...MQ].map(k =>
    `<div class="marquee-item" style="background-image:url(${LQIPS[k]})"><img loading="lazy" src="${IMGS[k]}" alt="Kc Collection dress"></div>`).join('');

  /* image fade-in over LQIP placeholders */
  document.addEventListener('load', e => {
    if (e.target.tagName === 'IMG') e.target.classList.add('ld');
  }, true);

  /* search */
  let sTimer;
  $('#searchInput').addEventListener('input', e => {
    clearTimeout(sTimer);
    sTimer = setTimeout(() => { searchTerm = e.target.value.trim().toLowerCase(); applyFilters(); }, 120);
  });

  $('#cartbar').addEventListener('click', openCart);

  /* mobile nav */
  $('#menuBtn').addEventListener('click', () => $('#navLayer').classList.contains('open') ? closeNav() : openNav());
  $('#navX').addEventListener('click', closeNav);
  $('#navScrim').addEventListener('click', closeNav);
  $('#navSize').addEventListener('click', () => { closeNav(); setTimeout(openSizeChart, 250); });
  $('#navDrawer').addEventListener('click', e => { if (e.target.closest('a[href^="#"]')) closeNav(); });
  $('#fxToggle').addEventListener('click', toggleFx);
  document.addEventListener('keydown', onKeydown);

  /* privacy / 404 views */
  $('#privacyBack').addEventListener('click', () => { location.hash = ''; });
  $('#errHome').addEventListener('click', () => { location.hash = ''; });

  /* logo → homepage/top (sticky target can't anchor-scroll, so scroll manually) */
  $('#brandLink').addEventListener('click', e => {
    e.preventDefault();
    closeNav();
    if (location.hash && location.hash !== '#top') location.hash = '';
    if (history.replaceState) history.replaceState(null, '', ' ');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
});
"""
