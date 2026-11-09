/**
 * ELLA ESTETİK VE GÜZELLİK
 * Ana JavaScript Dosyası
 * Çok dilli (i18n), dinamik çalışma saatleri, lightbox, galeri ve mobil etkileşimler
 */

let currentLang = 'tr';

document.addEventListener('DOMContentLoaded', () => {
  initLanguage();
  initHeader();
  initMobileNav();
  initLiveHours();
  initGallery();
  initFaq();
  initYear();
});

/* 1. ÇOKLU DİL YÖNETİMİ (i18n) */
function initLanguage() {
  const savedLang = localStorage.getItem('ella_lang');
  const browserLang = (navigator.language || navigator.userLanguage || 'tr').substring(0, 2).toLowerCase();
  
  if (savedLang && ['tr', 'en', 'ru', 'uk'].includes(savedLang)) {
    currentLang = savedLang;
  } else if (['en', 'ru', 'uk'].includes(browserLang)) {
    currentLang = browserLang;
  } else {
    currentLang = 'tr';
  }

  // Dil butonları etkileşimi
  const langToggleBtn = document.querySelector('.lang-btn-current');
  const langDropdown = document.querySelector('.lang-dropdown');
  const langOptions = document.querySelectorAll('.lang-option');
  const mobileLangBtns = document.querySelectorAll('.mobile-lang-btn');

  if (langToggleBtn && langDropdown) {
    langToggleBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      langDropdown.classList.toggle('open');
      langToggleBtn.setAttribute('aria-expanded', langDropdown.classList.contains('open'));
    });

    document.addEventListener('click', () => {
      langDropdown.classList.remove('open');
      langToggleBtn.setAttribute('aria-expanded', 'false');
    });
  }

  langOptions.forEach(opt => {
    opt.addEventListener('click', () => {
      const selected = opt.getAttribute('data-lang');
      setLanguage(selected);
      if (langDropdown) langDropdown.classList.remove('open');
    });
  });

  mobileLangBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const selected = btn.getAttribute('data-lang');
      setLanguage(selected);
    });
  });

  // Başlangıç dilini uygula
  setLanguage(currentLang);
}

function setLanguage(lang) {
  if (!translations[lang]) lang = 'tr';
  currentLang = lang;
  localStorage.setItem('ella_lang', lang);
  document.documentElement.lang = lang;

  const t = translations[lang];

  // Title & Meta
  if (t.pageTitle) document.title = t.pageTitle;
  const metaDescEl = document.querySelector('meta[name="description"]');
  if (metaDescEl && t.metaDesc) metaDescEl.setAttribute('content', t.metaDesc);

  // Metin alanlarını güncelle (data-i18n)
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key]) {
      el.innerHTML = t[key];
    }
  });

  // Öznitelikleri güncelle (data-i18n-attr="attr:key,attr2:key2")
  document.querySelectorAll('[data-i18n-attr]').forEach(el => {
    const pairs = el.getAttribute('data-i18n-attr').split(',');
    pairs.forEach(pair => {
      const [attr, key] = pair.split(':').map(s => s.trim());
      if (attr && key && t[key]) {
        el.setAttribute(attr, t[key]);
      }
    });
  });

  // Butonlardaki bayrak ve yazıyı güncelle
  const flags = { tr: '🇹🇷', en: '🇬🇧', ru: '🇷🇺', uk: '🇺🇦' };
  const labels = { tr: 'TR', en: 'EN', ru: 'RU', uk: 'UK' };
  
  const currentFlagEl = document.querySelector('.lang-btn-current .lang-flag');
  const currentCodeEl = document.querySelector('.lang-btn-current .lang-code');
  if (currentFlagEl) currentFlagEl.textContent = flags[lang];
  if (currentCodeEl) currentCodeEl.textContent = labels[lang];

  // Aktif sınıfları güncelle
  document.querySelectorAll('.lang-option').forEach(opt => {
    opt.classList.toggle('active', opt.getAttribute('data-lang') === lang);
  });
  document.querySelectorAll('.mobile-lang-btn').forEach(btn => {
    btn.classList.toggle('active', btn.getAttribute('data-lang') === lang);
  });

  // WhatsApp bağlantılarını dile özel mesajla güncelle
  updateWhatsAppLinks(t);

  // Çalışma saatleri rozetini güncelle
  initLiveHours();
}

function updateWhatsAppLinks(t) {
  const defaultMsg = encodeURIComponent(t.whatsappDefaultMsg || "Merhaba Ella Estetik, randevu almak istiyorum.");
  const baseUrl = `https://wa.me/905433494980?text=${defaultMsg}`;

  document.querySelectorAll('a.btn-whatsapp, a.floating-whatsapp, a.act-wa').forEach(a => {
    // Özel hizmet linki değilse varsayılan mesajı ata
    if (!a.getAttribute('data-custom-service')) {
      a.href = baseUrl;
    }
  });

  // Hizmet kartlarındaki WhatsApp butonları
  document.querySelectorAll('.service-card').forEach(card => {
    const btn = card.querySelector('.service-btn');
    const serviceTitle = card.querySelector('.service-title');
    if (btn && serviceTitle) {
      let customText = "";
      if (currentLang === 'en') {
        customText = `Hello Ella Estetik, I would like to book an appointment for ${serviceTitle.textContent.trim()}.`;
      } else if (currentLang === 'ru') {
        customText = `Здравствуйте! Я хотела бы записаться в Ella Estetik на процедуру: ${serviceTitle.textContent.trim()}.`;
      } else if (currentLang === 'uk') {
        customText = `Доброго дня! Я хотіла б записатися в Ella Estetik на процедуру: ${serviceTitle.textContent.trim()}.`;
      } else {
        customText = `Merhaba Ella Estetik, ${serviceTitle.textContent.trim()} hakkında bilgi ve randevu almak istiyorum.`;
      }
      btn.href = `https://wa.me/905433494980?text=${encodeURIComponent(customText)}`;
      btn.setAttribute('data-custom-service', 'true');
    }
  });
}

/* 2. HEADER SCROLL ETKİSİ */
function initHeader() {
  const header = document.querySelector('.header');
  if (!header) return;

  const onScroll = () => {
    if (window.scrollY > 40) {
      header.classList.add('scrolled');
    } else {
      header.classList.remove('scrolled');
    }
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();
}

/* 3. MOBİL MENÜ ETKİLEŞİMİ */
function initMobileNav() {
  const toggleBtn = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav');
  const navLinks = document.querySelectorAll('.nav-link');

  if (!toggleBtn || !nav) return;

  const toggleMenu = (open) => {
    const isOpen = open !== undefined ? open : !nav.classList.contains('active');
    nav.classList.toggle('active', isOpen);
    document.body.classList.toggle('menu-open', isOpen);
    toggleBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    toggleBtn.innerHTML = isOpen
      ? `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>`
      : `<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg>`;
  };

  toggleBtn.addEventListener('click', () => toggleMenu());

  navLinks.forEach(link => {
    link.addEventListener('click', () => toggleMenu(false));
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && nav.classList.contains('active')) {
      toggleMenu(false);
    }
  });
}

/* 4. DİNAMİK ÇALIŞMA SAATİ DURUMU (TÜRKİYE YEREL SAATİ & ÇOKLU DİL) */
function initLiveHours() {
  const statusPill = document.querySelector('.live-status-pill');
  const rows = document.querySelectorAll('.hours-table tr[data-day]');
  if (!statusPill) return;

  const t = translations[currentLang] || translations.tr;

  const dayNames = {
    0: t.daySun,
    1: t.dayMon,
    2: t.dayTue,
    3: t.dayWed,
    4: t.dayThu,
    5: t.dayFri,
    6: t.daySat
  };

  // Tablodaki gün başlıklarını güncelle
  rows.forEach(row => {
    const dayIndex = parseInt(row.getAttribute('data-day'), 10);
    const labelCell = row.querySelector('.day-name');
    if (labelCell && dayNames[dayIndex]) {
      labelCell.textContent = dayNames[dayIndex];
    }
    const valCell = row.querySelector('.day-val');
    if (valCell && dayIndex === 0) {
      valCell.textContent = t.statusClosedDay;
    }
  });

  const schedule = {
    0: { open: false, start: 0, end: 0 },
    1: { open: true, start: 10 * 60, end: 18 * 60 + 30 },
    2: { open: true, start: 10 * 60, end: 18 * 60 + 30 },
    3: { open: true, start: 10 * 60, end: 18 * 60 + 30 },
    4: { open: true, start: 10 * 60, end: 19 * 60 },
    5: { open: true, start: 10 * 60, end: 19 * 60 },
    6: { open: true, start: 10 * 60, end: 18 * 60 + 30 }
  };

  const now = new Date();
  const trTimeStr = now.toLocaleString("en-US", { timeZone: "Europe/Istanbul" });
  const trDate = new Date(trTimeStr);

  const dayOfWeek = trDate.getDay();
  const currentMinutes = trDate.getHours() * 60 + trDate.getMinutes();

  rows.forEach(row => {
    row.classList.remove('today');
    if (parseInt(row.getAttribute('data-day'), 10) === dayOfWeek) {
      row.classList.add('today');
    }
  });

  const todaySchedule = schedule[dayOfWeek];
  let isOpen = false;
  let statusText = '';

  if (todaySchedule.open && currentMinutes >= todaySchedule.start && currentMinutes < todaySchedule.end) {
    isOpen = true;
    const closingHour = Math.floor(todaySchedule.end / 60);
    const closingMin = todaySchedule.end % 60;
    const minFormatted = closingMin === 0 ? '00' : closingMin;
    const closeTimeStr = `${closingHour}:${minFormatted}`;
    statusText = (t.statusOpenNow || "Şu Anda Açık • Bugün {time}'a kadar açığız").replace('{time}', closeTimeStr);
  } else {
    isOpen = false;
    let nextDay = (dayOfWeek + 1) % 7;
    let daysAhead = 1;
    while (!schedule[nextDay].open && daysAhead < 7) {
      nextDay = (nextDay + 1) % 7;
      daysAhead++;
    }
    const nextStartHour = Math.floor(schedule[nextDay].start / 60);
    const nextDayLabel = daysAhead === 1 ? (t.tomorrow || 'Yarın') : dayNames[nextDay];
    const openTimeStr = `${nextStartHour}:00`;
    statusText = (t.statusClosedNow || "Şu Anda Kapalı • Açılış: {nextDay} {time}")
      .replace('{nextDay}', nextDayLabel)
      .replace('{time}', openTimeStr);
  }

  statusPill.className = `live-status-pill ${isOpen ? 'open' : 'closed'}`;
  statusPill.innerHTML = `
    <span class="live-pulse" aria-hidden="true"></span>
    <span>${statusText}</span>
  `;
}

/* 5. GALERİ FİLTRELEME & LIGHTBOX (DOKUNMATİK KAYDIRMA DESTEĞİ) */
function initGallery() {
  const filterBtns = document.querySelectorAll('.gallery-filter-btn');
  const items = document.querySelectorAll('.gallery-item');
  const lightbox = document.querySelector('.lightbox');
  const lightboxImg = document.querySelector('.lightbox-img');
  const lightboxVideo = document.querySelector('.lightbox-video');
  const lightboxCaption = document.querySelector('.lightbox-caption');
  const closeBtn = document.querySelector('.lightbox-close');
  const prevBtn = document.querySelector('.lightbox-prev');
  const nextBtn = document.querySelector('.lightbox-next');

  if (!items.length) return;

  // Filtreleme
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      const filter = btn.getAttribute('data-filter');

      items.forEach(item => {
        const cat = item.getAttribute('data-category');
        if (filter === 'all' || cat === filter) {
          item.style.display = '';
        } else {
          item.style.display = 'none';
        }
      });
    });
  });

  // Lightbox Verisi
  let currentIndex = 0;
  const galleryData = Array.from(items).map((item, idx) => {
    const isVideo = item.classList.contains('gallery-item-video');
    const src = isVideo
      ? item.getAttribute('data-video-src')
      : item.querySelector('img').getAttribute('src');
    const caption = item.getAttribute('data-caption') || '';
    return { index: idx, isVideo, src, caption, element: item };
  });

  const openLightbox = (index) => {
    currentIndex = index;
    const current = galleryData[currentIndex];

    if (current.isVideo) {
      lightboxImg.style.display = 'none';
      lightboxVideo.style.display = 'block';
      lightboxVideo.src = current.src;
      lightboxVideo.play().catch(() => {});
    } else {
      lightboxVideo.pause();
      lightboxVideo.style.display = 'none';
      lightboxImg.style.display = 'block';
      lightboxImg.src = current.src;
      lightboxImg.alt = current.caption;
    }

    lightboxCaption.textContent = current.caption;
    lightbox.classList.add('active');
    document.body.style.overflow = 'hidden';
  };

  const closeLightbox = () => {
    lightbox.classList.remove('active');
    lightboxVideo.pause();
    lightboxVideo.src = '';
    document.body.style.overflow = '';
  };

  const navigateLightbox = (dir) => {
    const visibleData = galleryData.filter(d => d.element.style.display !== 'none');
    if (!visibleData.length) return;

    let currentVisiblePos = visibleData.findIndex(d => d.index === currentIndex);
    if (currentVisiblePos === -1) currentVisiblePos = 0;

    currentVisiblePos = (currentVisiblePos + dir + visibleData.length) % visibleData.length;
    openLightbox(visibleData[currentVisiblePos].index);
  };

  items.forEach((item, idx) => {
    item.addEventListener('click', () => openLightbox(idx));
    item.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openLightbox(idx);
      }
    });
  });

  if (closeBtn) closeBtn.addEventListener('click', closeLightbox);
  if (prevBtn) prevBtn.addEventListener('click', () => navigateLightbox(-1));
  if (nextBtn) nextBtn.addEventListener('click', () => navigateLightbox(1));

  if (lightbox) {
    lightbox.addEventListener('click', (e) => {
      if (e.target === lightbox || e.target.classList.contains('lightbox-content')) {
        closeLightbox();
      }
    });

    // Mobil dokunmatik kaydırma (Touch Swipe)
    let touchStartX = 0;
    let touchEndX = 0;

    lightbox.addEventListener('touchstart', (e) => {
      touchStartX = e.changedTouches[0].screenX;
    }, { passive: true });

    lightbox.addEventListener('touchend', (e) => {
      touchEndX = e.changedTouches[0].screenX;
      handleSwipe();
    }, { passive: true });

    const handleSwipe = () => {
      const diff = touchEndX - touchStartX;
      if (Math.abs(diff) > 45) {
        if (diff > 0) {
          navigateLightbox(-1); // Sağa kaydır -> Önceki
        } else {
          navigateLightbox(1);  // Sola kaydır -> Sonraki
        }
      }
    };
  }

  // Klavye desteği
  document.addEventListener('keydown', (e) => {
    if (!lightbox || !lightbox.classList.contains('active')) return;
    if (e.key === 'Escape') closeLightbox();
    if (e.key === 'ArrowLeft') navigateLightbox(-1);
    if (e.key === 'ArrowRight') navigateLightbox(1);
  });
}

/* 6. SSS (FAQ) AKORDİYON */
function initFaq() {
  const cards = document.querySelectorAll('.faq-card');
  cards.forEach(card => {
    const question = card.querySelector('.faq-question');
    if (!question) return;

    question.addEventListener('click', () => {
      const isOpen = card.classList.contains('open');
      cards.forEach(c => c.classList.remove('open'));
      if (!isOpen) {
        card.classList.add('open');
      }
    });
  });
}

/* 7. DİNAMİK YIL */
function initYear() {
  const yearEl = document.querySelector('.current-year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }
}
