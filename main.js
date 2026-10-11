(function () {
  var header = document.getElementById('top');
  var burger = document.querySelector('.burger');
  var menu = document.getElementById('menu');

  function onScroll() { header.classList.toggle('scrolled', window.scrollY > 24); }
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  function setMenu(open) {
    menu.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', open);
    burger.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
  }
  burger.addEventListener('click', function () { setMenu(!menu.classList.contains('open')); });
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) setMenu(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') setMenu(false); });
  window.addEventListener('resize', function () { if (window.innerWidth > 860) setMenu(false); });

  // Building types: tabs
  var tabs = Array.prototype.slice.call(document.querySelectorAll('.bt-list [role=tab]'));
  function select(tab, focus) {
    tabs.forEach(function (t) {
      var on = t === tab;
      t.setAttribute('aria-selected', on);
      t.tabIndex = on ? 0 : -1;
      var p = document.getElementById(t.getAttribute('aria-controls'));
      p.hidden = !on;
      p.classList.toggle('on', on);
    });
    if (focus) tab.focus();
  }
  tabs.forEach(function (t, i) {
    t.addEventListener('click', function () { select(t); });
    t.addEventListener('mouseenter', function () {
      if (window.matchMedia('(hover:hover) and (min-width:981px)').matches) select(t);
    });
    t.addEventListener('keydown', function (e) {
      var n = null;
      if (e.key === 'ArrowDown' || e.key === 'ArrowRight') n = tabs[(i + 1) % tabs.length];
      if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') n = tabs[(i - 1 + tabs.length) % tabs.length];
      if (e.key === 'Home') n = tabs[0];
      if (e.key === 'End') n = tabs[tabs.length - 1];
      if (n) { e.preventDefault(); select(n, true); }
    });
  });

  // Reveal on scroll
  var fade = document.querySelectorAll(
    '.hero-copy, .sec-top, .sec-label, .practice-grid > *, .svc, .feat-panel > *, .pf-info > *, .pf-meta, .pf-s > :not(figure), .steps li, .matrix li, .senior li, .grp, .why-list li, .details, .contact-grid > div:first-child > *, .cred-grid li, .bt-view'
  );
  var media = document.querySelectorAll('.reveal-img');
  var steps = document.querySelector('.steps');
  fade.forEach(function (el) { el.classList.add('rv'); });

  if (!('IntersectionObserver' in window)) {
    fade.forEach(function (el) { el.classList.add('in'); });
    media.forEach(function (el) { el.classList.add('in'); });
    if (steps) steps.classList.add('in');
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); if (en.target.classList.contains('cred-grid')) count(); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.06 });
  fade.forEach(function (el) { io.observe(el); });
  media.forEach(function (el) { io.observe(el); });
  if (steps) io.observe(steps);

  // Number counters (final values are in the HTML for no-JS / reduced motion)
  var counted = false;
  function count() {
    if (counted) return; counted = true;
    if (window.matchMedia('(prefers-reduced-motion:reduce)').matches) return;
    document.querySelectorAll('[data-to]').forEach(function (el) {
      var to = parseFloat(el.getAttribute('data-to')), dec = +el.getAttribute('data-dec') || 0;
      var t0 = null, dur = 1400;
      function tick(t) {
        if (!t0) t0 = t;
        var k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3);
        el.textContent = (to * e).toFixed(dec);
        if (k < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    });
  }
  var cred = document.querySelector('.cred-grid');
  if (cred) {
    new IntersectionObserver(function (en, ob) {
      if (en[0].isIntersecting) { count(); ob.disconnect(); }
    }, { threshold: 0.4 }).observe(cred);
  }

  // Active nav state
  var links = {};
  menu.querySelectorAll('a[href^="#"]').forEach(function (a) { links[a.getAttribute('href')] = a; });
  var spy = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      var a = links['#' + en.target.id];
      if (a && !a.classList.contains('btn')) a.classList.toggle('on', en.isIntersecting);
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  ['services', 'projects', 'expertise', 'team', 'contact'].forEach(function (id) {
    var s = document.getElementById(id); if (s) spy.observe(s);
  });
})();
