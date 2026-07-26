/* FEELY the Traveler — interactions */

(function () {
  'use strict';

  /* ---------- Footer year ---------- */
  const yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  /* ---------- Sticky nav ---------- */
  const nav = document.getElementById('nav');
  const onScroll = () => {
    nav.classList.toggle('is-stuck', window.scrollY > 40);
    // Prevent sideways jump from overflow / focus scroll-into-view
    if (window.scrollX !== 0) {
      window.scrollTo(0, window.scrollY);
    }
  };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
  window.addEventListener('resize', () => {
    if (window.scrollX !== 0) window.scrollTo(0, window.scrollY);
  }, { passive: true });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'PageDown' || e.key === 'PageUp' || e.key === ' ' || e.key === 'Home' || e.key === 'End') {
      requestAnimationFrame(() => {
        if (window.scrollX !== 0) window.scrollTo(0, window.scrollY);
      });
    }
  });

  /* ---------- Reveal on scroll ---------- */
  const io = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (!entry.isIntersecting) return;
      const delay = Math.min(i, 6) * 70;
      setTimeout(() => entry.target.classList.add('is-in'), delay);
      io.unobserve(entry.target);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });

  document.querySelectorAll('.reveal').forEach((el) => io.observe(el));

  /* ---------- Gallery ---------- */
  const tabsEl = document.getElementById('tabs');
  const chaptersEl = document.getElementById('chapters');

  // Flat list of every work, in display order, for lightbox navigation.
  const flat = [];

  const epLabel = (file) => {
    const match = file.match(/([^/\\]+)\.[^.]+$/);
    return match ? match[1].toUpperCase() : file;
  };

  if (tabsEl && chaptersEl && typeof GALLERY !== 'undefined') {
    const viewAllBtn = document.getElementById('viewAll');
    let viewAll = false;
    let activeChapter = GALLERY[0] ? GALLERY[0].id : null;

    const applyView = () => {
      chaptersEl.classList.toggle('is-view-all', viewAll);
      chaptersEl.querySelectorAll('.chapter').forEach((c) => {
        c.classList.toggle('is-active', viewAll || c.id === activeChapter);
      });
      tabsEl.querySelectorAll('.tab').forEach((t) => {
        const active = !viewAll && t.dataset.target === activeChapter;
        t.classList.toggle('is-active', active);
        t.setAttribute('aria-selected', active ? 'true' : 'false');
      });
      if (viewAllBtn) {
        viewAllBtn.classList.toggle('is-active', viewAll);
        viewAllBtn.setAttribute('aria-pressed', viewAll ? 'true' : 'false');
        viewAllBtn.textContent = viewAll ? 'By chapter' : 'View all';
      }
    };

    GALLERY.forEach((chapter, ci) => {
      const tab = document.createElement('button');
      tab.className = 'tab' + (ci === 0 ? ' is-active' : '');
      tab.type = 'button';
      tab.textContent = chapter.label;
      tab.setAttribute('role', 'tab');
      tab.setAttribute('aria-selected', ci === 0 ? 'true' : 'false');
      tab.dataset.target = chapter.id;
      tabsEl.appendChild(tab);

      const section = document.createElement('div');
      section.className = 'chapter' + (ci === 0 ? ' is-active' : '');
      section.id = chapter.id;

      const head = document.createElement('div');
      head.className = 'chapter__head';
      head.innerHTML =
        '<span class="chapter__label">' + chapter.label +
        (chapter.title ? '. ' + chapter.title : '') + '</span>' +
        '<span class="chapter__count">' + chapter.works.length +
        (chapter.works.length === 1 ? ' piece' : ' pieces') + '</span>';
      section.appendChild(head);

      const grid = document.createElement('div');
      grid.className = 'grid';

      chapter.works.forEach((work) => {
        const index = flat.length;
        flat.push({ ...work, chapter: chapter.label, ep: epLabel(work.file) });

        const tile = document.createElement('button');
        tile.className = 'tile';
        tile.type = 'button';
        tile.dataset.index = index;

        const colors = [work.primary, ...(work.support || [])].filter(Boolean);

        tile.innerHTML =
          '<span class="tile__imgwrap">' +
            '<span class="tile__ep">' + epLabel(work.file) + '</span>' +
            '<img src="' + work.file + '" alt="' +
              (work.emotion ? work.emotion + ' — ' : '') +
              chapter.label + ' ' + epLabel(work.file) +
              ' by Feely the Traveler" loading="lazy">' +
          '</span>' +
          ((work.emotion || colors.length)
            ? '<span class="tile__meta">' +
                (work.emotion ? '<span class="tile__emotion">' + work.emotion + '</span>' : '') +
                (colors.length
                  ? '<span class="tile__dots">' +
                      colors.map((c) => '<span style="background:' + c + '"></span>').join('') +
                    '</span>'
                  : '') +
              '</span>'
            : '');

        grid.appendChild(tile);
      });

      section.appendChild(grid);
      chaptersEl.appendChild(section);
    });

    tabsEl.addEventListener('click', (e) => {
      const tab = e.target.closest('.tab');
      if (!tab) return;
      viewAll = false;
      activeChapter = tab.dataset.target;
      applyView();
    });

    if (viewAllBtn) {
      viewAllBtn.addEventListener('click', () => {
        viewAll = !viewAll;
        applyView();
      });
    }
  }

  /* ---------- Lightbox ---------- */
  const lb = document.getElementById('lb');
  const lbImg = document.getElementById('lbImg');
  const lbMeta = document.getElementById('lbMeta');
  const lbEmotion = document.getElementById('lbEmotion');
  const lbNote = document.getElementById('lbNote');
  const lbStory = document.getElementById('lbStory');
  let current = 0;

  const render = (i) => {
    const item = flat[i];
    if (!item) return;
    current = i;
    lbImg.src = item.file;
    lbImg.alt = (item.emotion ? item.emotion + ' — ' : '') + item.chapter + ' ' + item.ep;

    lbMeta.textContent = item.chapter + ' · ' + item.ep;

    if (item.emotion) {
      lbEmotion.hidden = false;
      lbEmotion.textContent = item.emotion;
    } else {
      lbEmotion.hidden = true;
      lbEmotion.textContent = '';
    }

    if (item.note) {
      lbNote.hidden = false;
      lbNote.textContent = item.note;
      lbStory.classList.remove('is-empty');
    } else {
      lbNote.hidden = true;
      lbNote.textContent = '';
      lbStory.classList.add('is-empty');
    }
  };

  const open = (i) => {
    render(i);
    lb.hidden = false;
    document.body.style.overflow = 'hidden';
  };

  const close = () => {
    lb.hidden = true;
    lbImg.src = '';
    document.body.style.overflow = '';
  };

  const step = (dir) => {
    if (!flat.length) return;
    render((current + dir + flat.length) % flat.length);
  };

  document.addEventListener('click', (e) => {
    const tile = e.target.closest('.tile');
    if (tile) open(Number(tile.dataset.index));
  });

  document.getElementById('lbClose').addEventListener('click', close);
  document.getElementById('lbPrev').addEventListener('click', () => step(-1));
  document.getElementById('lbNext').addEventListener('click', () => step(1));

  lb.addEventListener('click', (e) => {
    if (e.target === lb) close();
  });

  document.addEventListener('keydown', (e) => {
    if (lb.hidden) return;
    if (e.key === 'Escape') close();
    if (e.key === 'ArrowLeft') step(-1);
    if (e.key === 'ArrowRight') step(1);
  });
})();
