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

  // Reveal on scroll: fade-up, line drawing, process line expansion
  var targets = document.querySelectorAll(
    '.hero-copy, .hero-plate, .sec-head, .statement-top, .disc li, .spec-grid li, .row, .cap, .steps, .steps li, .pmc, .ind li, .about-grid > *, .matrix li, .tally div, .grp, .details, .contact-copy'
  );
  var drawn = document.querySelectorAll('.row-art, .hero-plate');
  targets.forEach(function (el) { el.classList.add('rv'); });

  if (!('IntersectionObserver' in window)) {
    targets.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) {
      if (en.isIntersecting) { en.target.classList.add('in'); io.unobserve(en.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  targets.forEach(function (el) { io.observe(el); });
  drawn.forEach(function (el) { io.observe(el); });

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
