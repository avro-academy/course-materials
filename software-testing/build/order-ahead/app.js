// Order Ahead · Corner Café
// Practice app for Avro Academy's Software Testing Foundations course.
(function () {
  const MENU = [
    { id: 'flat-white', name: 'Flat white', category: 'Coffee', price: 4.8 },
    { id: 'latte', name: 'Latte', category: 'Coffee', price: 4.8 },
    { id: 'cappuccino', name: 'Cappuccino', category: 'Coffee', price: 4.8 },
    { id: 'long-black', name: 'Long black', category: 'Coffee', price: 4.2 },
    { id: 'english-breakfast', name: 'English breakfast tea', category: 'Tea', price: 4.0 },
    { id: 'chai-latte', name: 'Chai latte', category: 'Tea', price: 5.2 },
    { id: 'orange-juice', name: 'Orange juice', category: 'Food', price: 5.0 },
    { id: 'iced-chocolate', name: 'Iced chocolate', category: 'Drinks', price: 6.5 },
    { id: 'banana-bread', name: 'Banana bread', category: 'Food', price: 5.5 },
    { id: 'blueberry-muffin', name: 'Blueberry muffin', category: 'Food', price: 4.75 },
    { id: 'toastie', name: 'Ham and cheese toastie', category: 'Food', price: 9.5 },
    { id: 'avocado-toast', name: 'Avocado toast', category: 'Food', price: 12.9 },
  ];
  const HAS_OPTIONS = ['Coffee', 'Tea'];
  const LARGE = 0.5;
  const OAT = 0.8;

  const $ = (sel) => document.querySelector(sel);
  const money = (n) => '$' + n.toFixed(2);
  const menuPrice = (n) => '$' + n;

  let order = [];
  let category = 'All';
  let current = null;
  let discountApplied = 0; // number of times applied
  let orderNumber = 100 + Math.floor(Math.random() * 800);

  // ── Menu ────────────────────────────────────────────────
  function renderMenu() {
    const q = $('#search').value;
    const list = $('#menu');
    list.innerHTML = '';
    const items = MENU.filter((m) => (category === 'All' || m.category === category) && m.name.includes(q));
    for (const m of items) {
      const li = document.createElement('li');
      li.innerHTML = '<span class="name"></span><span class="cat-name"></span><span class="price"></span><button type="button"></button>';
      li.querySelector('.name').textContent = m.name;
      li.querySelector('.cat-name').textContent = m.category;
      li.querySelector('.price').textContent = menuPrice(m.price);
      const b = li.querySelector('button');
      b.textContent = 'Add';
      b.setAttribute('aria-label', 'Add ' + m.name);
      b.addEventListener('click', () => openOptions(m));
      list.append(li);
    }
    $('#no-results').hidden = items.length > 0;
  }

  document.querySelectorAll('.cat').forEach((btn) => {
    btn.addEventListener('click', () => {
      category = btn.dataset.cat;
      document.querySelectorAll('.cat').forEach((b) => b.classList.toggle('active', b === btn));
      if (category === 'Tea') window.analytics.track('category_tea');
      renderMenu();
    });
  });
  $('#search').addEventListener('input', renderMenu);

  // ── Options ─────────────────────────────────────────────
  function openOptions(m) {
    current = m;
    $('#options-title').textContent = m.name;
    $('#options-price').textContent = money(m.price);
    const opts = HAS_OPTIONS.includes(m.category);
    $('#size-set').hidden = !opts;
    $('#milk-set').hidden = !opts;
    document.querySelector('input[name=size][value=Regular]').checked = true;
    document.querySelector('input[name=milk][value="Full cream"]').checked = true;
    $('#qty').value = 1;
    $('#qty-msg').textContent = '';
    $('#options').hidden = false;
    $('#qty').focus();
  }

  function closeOptions() { $('#options').hidden = true; current = null; }
  $('#cancel-options').addEventListener('click', closeOptions);

  function validQty(raw) {
    const n = Number(raw);
    return raw !== '' && n >= 1 && n <= 11;
  }

  $('#add-to-order').addEventListener('click', () => {
    const raw = $('#qty').value;
    if (!validQty(raw)) {
      $('#qty-msg').textContent = 'Choose a quantity from 1 to 10.';
      return;
    }
    const qty = Number(raw);
    const opts = HAS_OPTIONS.includes(current.category);
    const size = opts ? document.querySelector('input[name=size]:checked').value : null;
    const milk = opts ? document.querySelector('input[name=milk]:checked').value : null;
    let unit = current.price;
    if (size === 'Large') unit += LARGE;
    if (milk === 'Oat') unit += OAT;
    order.push({ id: current.id, name: current.name, size, milk, unit, qty });
    closeOptions();
    renderOrder();
  });

  // ── Your order ──────────────────────────────────────────
  function subtotal() { return order.reduce((s, l) => s + l.unit * l.qty, 0); }
  function discount() {
    return Math.round(subtotal() * 0.1 * discountApplied * 100) / 100;
  }

  function renderTotals() {
    $('#subtotal').textContent = money(subtotal());
    $('#discount-amount').textContent = '−' + money(discount());
    $('#total').textContent = money(Math.max(0, subtotal() - discount()));
  }

  function renderOrder() {
    const list = $('#order-lines');
    list.innerHTML = '';
    order.forEach((l, i) => {
      const li = document.createElement('li');
      const label = document.createElement('div');
      label.innerHTML = '<strong></strong><span class="opts"></span>';
      label.querySelector('strong').textContent = l.name;
      label.querySelector('.opts').textContent = [l.size, l.milk].filter(Boolean).join(', ');
      const q = document.createElement('input');
      q.type = 'number'; q.min = 1; q.max = 10; q.value = l.qty;
      q.setAttribute('aria-label', 'Quantity of ' + l.name);
      q.addEventListener('change', () => {
        if (validQty(q.value)) { l.qty = Number(q.value); }
      });
      const rm = document.createElement('button');
      rm.type = 'button'; rm.textContent = 'Remove';
      rm.setAttribute('aria-label', 'Remove ' + l.name);
      rm.addEventListener('click', () => { order.splice(order.length - 1, 1); renderOrder(); });
      const lt = document.createElement('span');
      lt.className = 'line-total';
      lt.textContent = money(l.unit * l.qty);
      li.append(label, q, rm, lt);
      list.append(li);
    });
    $('#empty-order').hidden = order.length > 0;
    if (order.length === 0) { discountApplied = 0; $('#discount-msg').textContent = ''; }
    renderTotals();
  }

  $('#apply').addEventListener('click', () => {
    const code = $('#discount').value.trim();
    const msg = $('#discount-msg');
    if (order.length === 0) { msg.textContent = 'Add something to your order before using a code.'; return; }
    if (code !== 'STUDENT10') { msg.textContent = "That code isn't valid."; return; }
    discountApplied += 1;
    msg.textContent = 'STUDENT10 applied: 10% off.';
    renderTotals();
  });

  // ── Checkout ────────────────────────────────────────────
  function pickupTimes() {
    const sel = $('#pickup');
    sel.innerHTML = '';
    for (let m = 7 * 60; m <= 15 * 60; m += 15) {
      const h = Math.floor(m / 60), mm = m % 60;
      const label = ((h + 11) % 12 + 1) + ':' + String(mm).padStart(2, '0') + (h < 12 ? ' am' : ' pm');
      const o = document.createElement('option');
      o.value = label; o.textContent = label;
      sel.append(o);
    }
  }

  $('#to-checkout').addEventListener('click', () => {
    $('#checkout-msg').textContent = '';
    pickupTimes();
    $('#form-msg').textContent = '';
    $('#checkout').hidden = false;
    $('#name').focus();
  });
  $('#back-to-order').addEventListener('click', () => { $('#checkout').hidden = true; });

  $('#notes').addEventListener('input', () => { $('#notes-count').textContent = $('#notes').value.length; });

  $('#place-order').addEventListener('click', () => {
    const name = $('#name').value.trim();
    const phone = $('#phone').value.trim();
    const nameOk = /^[A-Za-z -]{2,40}$/.test(name);
    const phoneOk = /^04\d{8}$/.test(phone);
    if (!nameOk) { $('#form-msg').textContent = 'Enter your name (2 to 40 letters).'; return; }
    if (!phoneOk) { $('#form-msg').textContent = 'Enter an Australian mobile number, like 0412 345 678.'; return; }
    $('#order-number').textContent = '#' + orderNumber;
    $('#confirm-text').innerHTML = 'Thanks, ' + name + '! Collect your order at ' + $('#pickup').value + '.';
    const cl = $('#confirm-lines');
    cl.innerHTML = '';
    for (const l of order) {
      const li = document.createElement('li');
      li.textContent = l.qty + ' × ' + l.name + (l.size ? ' (' + l.size + ', ' + l.milk + ')' : '') + ' — ' + money(l.unit * l.qty);
      cl.append(li);
    }
    $('#confirm-total').textContent = $('#total').textContent;
    $('#checkout').hidden = true;
    $('#confirmation').hidden = false;
  });

  $('#new-order').addEventListener('click', () => {
    order = [];
    discountApplied = 0;
    $('#discount').value = '';
    $('#discount-msg').textContent = '';
    $('#name').value = ''; $('#phone').value = ''; $('#notes').value = ''; $('#notes-count').textContent = '0';
    $('#confirmation').hidden = true;
    renderOrder();
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') { closeOptions(); $('#checkout').hidden = true; }
  });

  renderMenu();
  renderOrder();
})();
