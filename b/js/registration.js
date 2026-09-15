(() => {
  'use strict';
  const config = window.LAUNCH_CONFIG || {};
  const dialog = document.querySelector('#registrationModal');
  const form = document.querySelector('#registrationForm');
  const fieldset = form.querySelector('fieldset');
  const nameInput = form.elements.name;
  const phoneInput = form.elements.phone;
  const status = document.querySelector('#registration-status');
  let pending = false;
  let submission = null;

  function setStatus(text, state) { status.textContent = text; status.dataset.state = state; }
  function makeId() {
    if (crypto.randomUUID) return crypto.randomUUID();
    return Array.from(crypto.getRandomValues(new Uint8Array(16)), b => b.toString(16).padStart(2, '0')).join('');
  }
  function endpointUrl() {
    try {
      const url = new URL(config.sheetUrl);
      return url.protocol === 'https:' && url.hostname === 'script.google.com' && /^\/macros\/s\/[\w-]+\/exec$/.test(url.pathname) ? url.href : null;
    } catch { return null; }
  }
  function invalid(input, text) {
    document.getElementById(input===nameInput?'nameError':'phoneError').hidden=false;
    input.setAttribute('aria-invalid', 'true');
    setStatus(text, 'error'); input.focus();
  }
  for (const input of [nameInput, phoneInput]) {
    input.addEventListener('input', () => {
      document.getElementById(input===nameInput?'nameError':'phoneError').hidden=true;
      input.removeAttribute('aria-invalid');
      if (status.dataset.state === 'error') setStatus('', '');
    });
  }
  let opener = null;
  const main = document.querySelector('main');
  function closeModal() {
    window.phoneFormatter.closeDropdown(); dialog.hidden = true; main.inert = false;
    if (opener) opener.focus({preventScroll:true});
  }
  document.querySelectorAll('[data-register]').forEach(button => {
    button.classList.add('registerBtn');
    button.addEventListener('click', () => {
      opener = button; dialog.hidden = false; main.inert = true;
      if (!pending) nameInput.focus();
      else dialog.querySelector('#closeModalBtn').focus();
    });
  });
  dialog.querySelector('#closeModalBtn').addEventListener('click', closeModal);
  dialog.querySelector('.homeModalOverlay').addEventListener('click', closeModal);
  dialog.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      event.preventDefault();
      if (window.phoneFormatter.isDropdownOpen()) { window.phoneFormatter.closeDropdown(); document.getElementById('selectedCountry').focus(); }
      else closeModal();
    }
    if (event.key === 'Tab') {
      const elements = [...dialog.querySelectorAll('button,input,a[href]')].filter(e=>!e.disabled && e.tabIndex>=0 && e.getClientRects().length);
      const first=elements[0], last=elements[elements.length-1];
      if (event.shiftKey && document.activeElement===first) {event.preventDefault();last.focus();}
      else if (!event.shiftKey && document.activeElement===last) {event.preventDefault();first.focus();}
    }
  });
  form.addEventListener('submit', event => {
    event.preventDefault();
    if (pending) return;
    const name = nameInput.value.trim().replace(/\s+/g, ' ');
    const formatter = window.phoneFormatter;
    const phone = formatter.validate(phoneInput.value) ? formatter.getNumber() : null;
    if (name.length < 2 || name.length > 80 || !/\p{L}/u.test(name)) return invalid(nameInput, 'Ismingizni to‘liq kiriting.');
    if (!phone) return invalid(phoneInput, 'Tanlangan mamlakatga mos telefon raqamini to‘liq kiriting.');
    const endpoint = endpointUrl();
    if (!endpoint) { setStatus('Ro‘yxatdan o‘tish hozircha mavjud emas. Iltimos, keyinroq qayta urinib ko‘ring.', 'error'); return; }
    const variant = document.body.dataset.variant;
    const signature = JSON.stringify([name, phone, variant]);
    if (!submission || submission.signature !== signature) submission = { signature, id: makeId() };
    const utm = new URLSearchParams(location.search);
    let referrer = '';
    try { referrer = new URL(document.referrer).origin; } catch { /* Direct visit. */ }
    const data = {
      requestId: submission.id, name, phone, variant,
      page: location.origin + location.pathname,
      referrer,
      website: form.elements.website.value,
      utmSource: (utm.get('utm_source') || '').slice(0, 200),
      utmMedium: (utm.get('utm_medium') || '').slice(0, 200),
      utmCampaign: (utm.get('utm_campaign') || '').slice(0, 200),
      utmTerm: (utm.get('utm_term') || '').slice(0, 200),
      utmContent: (utm.get('utm_content') || '').slice(0, 200)
    };
    let body = data;
    const transport = config.sheetTransport === 'form-data' ? 'form-data' : 'json';
    if (config.sheetTransport === 'form-data') {
      const payload = new FormData();
      payload.append('sheetName', config.sheetName || 'Lead');
      payload.append('Ism', name);
      payload.append('Telefon raqam', formatter.getCurrentCode() + ' ' + phoneInput.value.trim());
      payload.append("Royhatdan o'tgan vaqti", new Intl.DateTimeFormat('uz-UZ', { timeZone:'Asia/Tashkent', dateStyle:'short', timeStyle:'medium' }).format(new Date()));
      if (config.sheetMetadata === true) {
        payload.append('Variant', variant);
        payload.append('Ariza ID', submission.id);
        payload.append('Sahifa', data.page);
        payload.append('Manba', data.referrer);
        for (const key of ['utmSource','utmMedium','utmCampaign','utmTerm','utmContent']) payload.append(key, data[key]);
      }
      body = Object.fromEntries(payload.entries());
    }
    try {
      const key = 'bir.pendingLead:' + new URL('.', location.href).pathname;
      sessionStorage.setItem(key, JSON.stringify({
        requestId: submission.id, variant, transport, body, createdAt: Date.now()
      }));
      pending = true; fieldset.disabled = true;
      window.location.assign(new URL('./thankYou.html', location.href).href);
    } catch {
      pending = false; fieldset.disabled = false;
      setStatus('Davom etish uchun brauzerda sayt ma’lumotlarini saqlashga ruxsat bering.', 'error');
    }
  });
  window.addEventListener('pageshow', () => { pending = false; fieldset.disabled = false; });
})();
