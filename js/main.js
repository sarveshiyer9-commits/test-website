// Boston Shawarma — site behaviour. The page reads fine without this file; it adds the
// popups, mobile menu, menu tabs, scroll reveals, rotating offers and live "Open now" badges.

// Where inquiry + newsletter forms are sent. Leave empty for the pitch demo (forms show a
// "demo" confirmation). For launch, paste a form endpoint here, e.g. from Formspree.
const FORM_ENDPOINT = '';

const DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)').matches;
const store = {                                   // localStorage can throw (private mode, blocked storage)
  get(key) { try { return localStorage.getItem(key); } catch { return null; } },
  set(key, value) { try { localStorage.setItem(key, value); } catch { /* not important */ } },
};
let refreshStatuses = () => {};

/* ------------------------------------------------------------------ popups */
// Any element with data-popup="x" opens <template id="tpl-x"> in the shared dialog.
// Visiting the page with #x in the URL opens it too, so deals and partner pages can be linked
// from Instagram, flyers or emails (e.g. boston-shawarma.com/#deal-student).
function initPopups() {
  const dialog = document.getElementById('popup');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  const body = dialog.querySelector('.popup-body');
  const formTemplate = document.getElementById('tpl-inquiry-form');
  let current = null;

  const open = (key) => {
    const tpl = document.getElementById(`tpl-${key}`);
    if (!tpl) return false;
    body.replaceChildren(tpl.content.cloneNode(true));

    // partnership and event popups share one inquiry form, pre-set to the right topic
    for (const slot of body.querySelectorAll('.popup-form')) {
      const form = formTemplate.content.cloneNode(true);
      const type = form.querySelector('[name="type"]');
      if (slot.dataset.formType) type.value = slot.dataset.formType;
      if (slot.dataset.formTopic) form.querySelector('[name="message"]').value = `Re: ${slot.dataset.formTopic}\n`;
      slot.replaceWith(form);
    }
    current = key;
    refreshStatuses();
    history.replaceState(null, '', `#${key}`);
    if (!dialog.open) dialog.showModal();
    dialog.scrollTop = 0;
    return true;
  };

  const close = () => { if (dialog.open) dialog.close(); };
  dialog.addEventListener('close', () => {
    current = null;
    history.replaceState(null, '', location.pathname + location.search);
  });

  document.addEventListener('click', (e) => {
    const trigger = e.target.closest('[data-popup]');
    if (trigger && open(trigger.dataset.popup)) {
      e.preventDefault();
      closeNudge();
      return;
    }
    if (e.target === dialog || e.target.closest('[data-close-popup]')) close();   // backdrop, × or "Full menu" links

    const share = e.target.closest('[data-share]');
    if (share && current) {
      const url = `${location.origin}${location.pathname}#${current}`;
      const title = body.querySelector('h2')?.textContent ?? 'Boston Shawarma';
      if (navigator.share) navigator.share({ title, url }).catch(() => {});
      else navigator.clipboard?.writeText(url).then(() => { share.textContent = 'Link copied!'; });
    }
  });

  const openFromHash = () => {
    const key = decodeURIComponent(location.hash.slice(1));
    if (key && document.getElementById(`tpl-${key}`)) open(key);
  };
  openFromHash();
  addEventListener('hashchange', openFromHash);
}

/* ------------------------------------------------------------------ forms (demo until FORM_ENDPOINT is set) */
function initForms() {
  document.addEventListener('submit', async (e) => {
    const form = e.target.closest('[data-demo-form]');
    if (!form) return;
    e.preventDefault();
    const status = form.querySelector('.form-status') ?? form.parentElement.querySelector('.form-status');
    const data = new FormData(form);
    const name = (data.get('name') || '').toString().split(' ')[0];
    const button = form.querySelector('[type="submit"]');
    button.disabled = true;

    let message;
    if (FORM_ENDPOINT) {
      try {
        const res = await fetch(FORM_ENDPOINT, { method: 'POST', body: data, headers: { Accept: 'application/json' } });
        if (!res.ok) throw new Error(res.statusText);
        message = form.dataset.demoForm === 'newsletter' ? "You're on the list — see you in your inbox." : `Thanks${name ? `, ${name}` : ''}! We'll get back to you within a day.`;
        form.reset();
      } catch {
        message = 'Something went wrong — please call us at (617) 670-0460.';
        button.disabled = false;
      }
    } else {
      message = form.dataset.demoForm === 'newsletter'
        ? "You're on the list! (Demo — connect a mailing tool to go live.)"
        : `Thanks${name ? `, ${name}` : ''}! (Demo — on the live site this goes straight to the Boston Shawarma team.)`;
    }
    status.textContent = message;
    status.hidden = false;
  });
}

/* ------------------------------------------------------------------ deal nudge */
let closeNudge = () => {};
function initNudge() {
  const nudge = document.querySelector('.nudge');
  if (!nudge || store.get('bs-nudge') === 'done') return;
  const dismiss = () => { nudge.hidden = true; store.set('bs-nudge', 'done'); };
  closeNudge = dismiss;
  nudge.querySelector('.nudge-close').addEventListener('click', dismiss);

  // show once the visitor has scrolled past the deals, never on top of an open popup
  const deals = document.getElementById('deals');
  const io = new IntersectionObserver(([entry]) => {
    if (entry.boundingClientRect.top < 0 && !entry.isIntersecting && !document.getElementById('popup')?.open) {
      nudge.hidden = false;
      io.disconnect();
    }
  });
  if (deals) io.observe(deals);
}

/* ------------------------------------------------------------------ rotating offers in the top bar */
function initPromos() {
  const promos = [...document.querySelectorAll('.promo')];
  if (promos.length < 2) return;
  let i = 0;
  let paused = false;
  const bar = promos[0].parentElement;
  bar.addEventListener('mouseenter', () => { paused = true; });
  bar.addEventListener('mouseleave', () => { paused = false; });
  bar.addEventListener('focusin', () => { paused = true; });
  bar.addEventListener('focusout', () => { paused = false; });
  setInterval(() => {
    if (paused || document.hidden) return;
    promos[i].classList.remove('is-current');
    i = (i + 1) % promos.length;
    promos[i].classList.add('is-current');
  }, 4500);
}

/* ------------------------------------------------------------------ scroll reveals, hand-drawn marks, spinning plate */
function initReveals() {
  const items = document.querySelectorAll('.reveal, .mark');
  if (!('IntersectionObserver' in window)) {
    items.forEach((el) => el.classList.add('is-visible', 'is-drawn'));
    return;
  }
  const io = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (!entry.isIntersecting) continue;
      entry.target.classList.add(entry.target.classList.contains('mark') ? 'is-drawn' : 'is-visible');
      io.unobserve(entry.target);
    }
  }, { rootMargin: '0px 0px -12% 0px' });
  items.forEach((el) => io.observe(el));

  if (reducedMotion) return;
  // the big plate turns slowly as it scrolls past
  const spinners = [...document.querySelectorAll('.spinner')];
  let ticking = false;
  const spin = () => {
    for (const el of spinners) {
      const r = el.getBoundingClientRect();
      const progress = (innerHeight - r.top) / (innerHeight + r.height);
      if (progress > -0.1 && progress < 1.1) el.style.setProperty('--spin', `${(progress - 0.5) * 70}deg`);
    }
    ticking = false;
  };
  addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(spin); } }, { passive: true });
  spin();
}

/* ------------------------------------------------------------------ navigation + menu tabs */
function initNav() {
  const toggle = document.querySelector('.nav-toggle');
  const nav = document.getElementById('site-nav');
  if (!toggle || !nav) return;
  const setOpen = (open) => {
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  };
  toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
  nav.addEventListener('click', (e) => { if (e.target.closest('a')) setOpen(false); });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setOpen(false); });
}

function initMenuTabs() {
  const tabs = [...document.querySelectorAll('.menu-tabs [role="tab"]')];
  if (!tabs.length) return;
  const select = (tab, { focus = false, scroll = true } = {}) => {
    for (const t of tabs) {
      const selected = t === tab;
      t.setAttribute('aria-selected', String(selected));
      t.tabIndex = selected ? 0 : -1;
      document.getElementById(t.getAttribute('aria-controls')).hidden = !selected;
    }
    if (focus) tab.focus();
    else if (scroll) tab.scrollIntoView({ block: 'nearest', inline: 'nearest' });
  };
  tabs.forEach((tab, i) => {
    tab.addEventListener('click', () => select(tab));
    tab.addEventListener('keydown', (e) => {
      const next = { ArrowRight: i + 1, ArrowLeft: i - 1, Home: 0, End: tabs.length - 1 }[e.key];
      if (next === undefined) return;
      e.preventDefault();
      select(tabs[(next + tabs.length) % tabs.length], { focus: true });
    });
  });
  select(tabs[0], { scroll: false });
}

/* ------------------------------------------------------------------ opening hours */
const toMinutes = (hhmm) => {
  const [h, m] = hhmm.split(':').map(Number);
  return h * 60 + m;
};

// 1350 -> "10:30 pm", 1380 -> "11 pm"
const formatTime = (minutes) => {
  const h = Math.floor(minutes / 60) % 24;
  const m = minutes % 60;
  return `${h % 12 || 12}${m ? `:${String(m).padStart(2, '0')}` : ''} ${h < 12 ? 'am' : 'pm'}`;
};

// Hours come from the HTML: data-open / data-close on the [data-hours] element apply
// every day; optional children like <span data-day="0" data-open="12:00" data-close="20:00">
// override single days (data-day="0" is Sunday). Omit open/close on a child to mark a day closed.
function readSchedule(el) {
  const daily = el.dataset.open && el.dataset.close
    ? { open: toMinutes(el.dataset.open), close: toMinutes(el.dataset.close) }
    : null;
  const schedule = new Map(DAYS.map((_, d) => [d, daily]));
  for (const override of el.querySelectorAll('[data-day]')) {
    const { day, open, close } = override.dataset;
    schedule.set(Number(day), open && close ? { open: toMinutes(open), close: toMinutes(close) } : null);
  }
  return schedule;
}

function openStatus(schedule, timeZone, date = new Date()) {
  // Day and time *at the restaurant*, not wherever the visitor's device is set to
  const parts = Object.fromEntries(
    new Intl.DateTimeFormat('en-US', {
      timeZone, weekday: 'long', hour: 'numeric', minute: 'numeric', hourCycle: 'h23',
    }).formatToParts(date).map((p) => [p.type, p.value]),
  );
  const today = DAYS.indexOf(parts.weekday);
  const now = Number(parts.hour) * 60 + Number(parts.minute);
  const pastMidnight = (h) => h && h.close <= h.open;

  const t = schedule.get(today);
  const y = schedule.get((today + 6) % 7);
  let closesAt = null;
  if (t && now >= t.open && (pastMidnight(t) || now < t.close)) closesAt = t.close;
  else if (pastMidnight(y) && now < y.close) closesAt = y.close;

  if (closesAt !== null) {
    const minutesLeft = (closesAt - now + 1440) % 1440;
    return minutesLeft <= 45
      ? { state: 'soon', text: `Closing soon · ${formatTime(closesAt)}` }
      : { state: 'open', text: `Open now · until ${formatTime(closesAt)}` };
  }
  for (let i = 0; i <= 7; i++) {
    const h = schedule.get((today + i) % 7);
    if (!h || (i === 0 && now >= h.open)) continue;
    const when = i === 0 ? 'today' : i === 1 ? 'tomorrow' : i === 7 ? `next ${DAYS[today]}` : DAYS[(today + i) % 7];
    return { state: 'closed', text: `Closed · opens ${when} at ${formatTime(h.open)}` };
  }
  return { state: 'closed', text: 'Closed' };
}

function initOpenStatus() {
  const locations = [...document.querySelectorAll('[data-hours]')].map((el) => ({
    key: el.dataset.hours,
    timeZone: el.dataset.timezone,
    schedule: readSchedule(el),
  }));
  if (!locations.length) return;
  refreshStatuses = () => {
    for (const { key, timeZone, schedule } of locations) {
      const { state, text } = openStatus(schedule, timeZone);
      for (const badge of document.querySelectorAll(`[data-open-status="${key}"]`)) {
        badge.textContent = text;
        badge.dataset.state = state;
        badge.hidden = false;
      }
    }
  };
  refreshStatuses();
  setInterval(refreshStatuses, 60_000);
}

/* ------------------------------------------------------------------ font lab */
// Add ?fontlab to the URL for a switcher that swaps the site between type pairings
// (?font=poster jumps straight to one). Each theme's fonts load only when it's picked.
const GF = 'https://fonts.googleapis.com/css2?display=swap&family=';
const FONT_THEMES = {
  grotesk: { label: 'Bricolage Grotesque (default)', href: `${GF}Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,200..800` },
  fraunces: { label: 'Fraunces', href: `${GF}Fraunces:opsz,wght,SOFT,WONK@9..144,400..900,0..100,0..1&family=Figtree:wght@400;500;600;700;800` },
  serif: { label: 'DM Serif Display', href: `${GF}DM+Serif+Display:ital@0;1&family=Figtree:wght@400;500;600;700;800` },
  poster: { label: 'Anton', href: `${GF}Anton&family=DM+Sans:opsz,wght@9..40,400..800` },
  beirut: { label: 'Lalezar', href: `${GF}Lalezar&family=Figtree:wght@400;500;600;700;800` },
  elegant: { label: 'Instrument Serif', href: `${GF}Instrument+Serif:ital@0;1&family=Instrument+Sans:wght@400..700` },
  playful: { label: 'Bagel Fat One', href: `${GF}Bagel+Fat+One&family=DM+Sans:opsz,wght@9..40,400..800` },
};

function initFontLab() {
  const params = new URLSearchParams(location.search);
  const requested = params.get('font');
  if (!params.has('fontlab') && !FONT_THEMES[requested]) return;

  const apply = (name) => {
    document.documentElement.dataset.font = name;
    let link = document.getElementById('font-theme');
    if (!link) {
      link = Object.assign(document.createElement('link'), { id: 'font-theme', rel: 'stylesheet' });
      document.head.append(link);
    }
    link.href = FONT_THEMES[name].href;
    params.set('font', name);
    history.replaceState(null, '', `?${params}${location.hash}`);
    for (const b of document.querySelectorAll('.font-lab button')) b.setAttribute('aria-pressed', String(b.value === name));
  };

  if (params.has('fontlab')) {
    const panel = document.createElement('div');
    panel.className = 'font-lab';
    panel.innerHTML = '<p>Font lab</p>' + Object.entries(FONT_THEMES)
      .map(([key, t]) => `<button type="button" value="${key}" aria-pressed="false">${t.label}</button>`).join('');
    panel.addEventListener('click', (e) => { const b = e.target.closest('button'); if (b) apply(b.value); });
    document.body.append(panel);
  }
  apply(FONT_THEMES[requested] ? requested : 'grotesk');
}

initFontLab();
initNav();
initMenuTabs();
initOpenStatus();
initPopups();
initForms();
initNudge();
initPromos();
initReveals();
document.querySelectorAll('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
