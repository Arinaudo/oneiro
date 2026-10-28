// ============================================================
// ONEIRO PARIS — Comportements partagés + rendu produits
// Bilingue : la langue est lue sur <html lang="...">.
// ============================================================

const ONEIRO_LANG = (document.documentElement.getAttribute("lang") || "fr").slice(0, 2).toLowerCase() === "en" ? "en" : "fr";

const ONEIRO_I18N = {
  fr: {
    locale: "fr-FR",
    productDir: "produits/",
    onRequest: "Sur demande",
    cat: { "bagues": "Bague", "boucles-oreilles": "Boucles d'oreilles", "colliers": "Collier", "bracelets": "Bracelet", "default": "Bijou" },
    orLab: p => `ou ${p} en diamant de laboratoire`,
    customizable: "Personnalisable",
    from: "À partir de ",
    wishAdd: "Ajouter à ma sélection",
    wishRemove: "Retirer de ma sélection",
    starsAria: n => `${n} étoiles sur 5`,
    reviewPhoto: a => `Photo du bijou par ${a}`,
    waDefault: "Bonjour, j'ai une question sur une création Oneiro.",
    videoFallback: "Votre navigateur ne lit pas cette vidéo.",
    videoTitle: "Vidéo de l'atelier Oneiro",
    heroDots: "Choisir le visuel",
    heroDot: (i, n) => `Visuel ${i} sur ${n}`,
    heroPrev: "Visuel précédent",
    heroNext: "Visuel suivant",
  },
  en: {
    locale: "en-GB",
    productDir: "products/",
    onRequest: "On request",
    cat: { "bagues": "Ring", "boucles-oreilles": "Earrings", "colliers": "Necklace", "bracelets": "Bracelet", "default": "Jewellery" },
    orLab: p => `or ${p} with a lab-grown diamond`,
    customizable: "Customisable",
    from: "From ",
    wishAdd: "Add to my selection",
    wishRemove: "Remove from my selection",
    starsAria: n => `${n} out of 5 stars`,
    reviewPhoto: a => `Photo of the piece by ${a}`,
    waDefault: "Hello, I have a question about an Oneiro piece.",
    videoFallback: "Your browser cannot play this video.",
    videoTitle: "Oneiro workshop video",
    heroDots: "Choose a visual",
    heroDot: (i, n) => `Visual ${i} of ${n}`,
    heroPrev: "Previous visual",
    heroNext: "Next visual",
  },
};

const T = ONEIRO_I18N[ONEIRO_LANG];

const O = {
  lang: ONEIRO_LANG,
  t: T,

  fmt(n) {
    if (n == null) return T.onRequest;
    return new Intl.NumberFormat(T.locale, { style: "currency", currency: "EUR", maximumFractionDigits: 0 }).format(n);
  },

  catLabel(c) {
    return T.cat[c] || T.cat.default;
  },

  img(src, w) {
    if (!src) return "";
    return src + (src.includes("?") ? "&" : "?") + "width=" + (w || 900);
  },

  product(handle) {
    return (typeof ONEIRO_PRODUCTS !== "undefined" ? ONEIRO_PRODUCTS : []).find(p => p.handle === handle);
  },

  // Titre et description traduits si le catalogue anglais est chargé
  title(p) {
    return (ONEIRO_LANG === "en" && p.titleEn) ? p.titleEn : p.title;
  },

  desc(p) {
    return (ONEIRO_LANG === "en" && p.descriptionEn) ? p.descriptionEn : p.description;
  },

  // Carte produit (collection, suggestions, accueil)
  card(p) {
    const lab = p.priceLab ? `<small>${T.orLab(this.fmt(p.priceLab))}</small>` : "";
    const badge = p.customizable ? `<span class="card__badge">${T.customizable}</span>` : "";
    const title = this.title(p);
    const img = p.images && p.images[0] ? `<img src="${this.img(p.images[0], 720)}" alt="${title} — Oneiro Paris" loading="lazy">` : "";
    const from = (p.priceNatural && p.priceLab && p.priceNatural !== p.priceLab) || p.variants.length > 1 ? T.from : "";
    return `
      <a class="card reveal" href="${T.productDir}${p.handle}.html">
        <div class="card__img">${img}${badge}${this.wishBtn(p.handle)}</div>
        <div class="card__body">
          <span class="card__cat">${this.catLabel(p.category)}</span>
          <span class="card__title">${title}</span>
          <span class="card__price">${from}${this.fmt(p.priceNatural || p.priceFrom)}${lab}</span>
        </div>
      </a>`;
  },

  renderCards(el, products) {
    el.innerHTML = products.map(p => this.card(p)).join("");
    this.observeReveals(el);
    this.wish.paint();
  },

  // Étoiles pleines / demie / vides à partir d'une note sur 5
  stars(n) {
    const full = Math.floor(n), half = n - full >= .25 && n - full < .75, up = n - full >= .75;
    return "★".repeat(full + (up ? 1 : 0)) + (half ? "⯨" : "") + "☆".repeat(Math.max(0, 5 - full - (up ? 1 : 0) - (half ? 1 : 0)));
  },

  reviewCard(r) {
    const esc = t => String(t == null ? "" : t).replace(/[<>&]/g, c => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;" }[c]));
    const rating = r.rating || 5;
    const when = r.date ? new Date(r.date).toLocaleDateString(T.locale, { month: "long", year: "numeric" }) : "";
    const meta = [r.context, when, r.source].filter(Boolean).map(esc).join(" — ");
    const photo = r.photo ? `<div class="review__photo"><img src="${esc(r.photo)}" alt="${esc(T.reviewPhoto(r.author))}" loading="lazy"></div>` : "";
    const quote = ONEIRO_LANG === "en" ? `“${esc(r.text)}”` : `«&nbsp;${esc(r.text)}&nbsp;»`;
    return `
      <div class="review reveal">
        <div class="review__stars" aria-label="${esc(T.starsAria(rating))}">${this.stars(rating)}</div>
        <p class="review__text">${quote}</p>
        ${photo}
        <p class="review__author"><b>${esc(r.author)}</b>${meta}</p>
      </div>`;
  },

  // ---------- Sélection partageable ----------
  // Stockée en local, et encodable dans l'URL pour être envoyée à quelqu'un.
  wish: {
    KEY: "oneiro_selection",
    get() {
      try { return JSON.parse(localStorage.getItem(this.KEY)) || []; }
      catch (e) { return []; }
    },
    set(list) {
      try { localStorage.setItem(this.KEY, JSON.stringify(list)); } catch (e) {}
      O.wish.paint();
    },
    has(handle) { return this.get().includes(handle); },
    toggle(handle) {
      const l = this.get();
      const i = l.indexOf(handle);
      if (i >= 0) l.splice(i, 1); else l.push(handle);
      this.set(l);
      return i < 0;
    },
    // Sélection affichée : celle de l'URL (lien reçu) sinon la sienne
    shared() {
      const q = new URLSearchParams(location.search).get("s");
      return q ? q.split(",").filter(Boolean) : null;
    },
    shareUrl() {
      const l = this.get();
      return location.origin + location.pathname + "?s=" + l.join(",");
    },
    // Met à jour les cœurs et le compteur du menu
    paint() {
      const l = O.wish.get();
      document.querySelectorAll("[data-wish]").forEach(b => {
        const on = l.includes(b.dataset.wish);
        b.classList.toggle("on", on);
        b.setAttribute("aria-pressed", on ? "true" : "false");
        b.setAttribute("title", on ? T.wishRemove : T.wishAdd);
      });
      document.querySelectorAll("[data-wish-count]").forEach(el => {
        el.textContent = l.length ? " (" + l.length + ")" : "";
      });
      document.querySelectorAll("[data-wish-count-badge]").forEach(el => {
        el.textContent = l.length;
        el.hidden = !l.length;
      });
    },
  },

  wishBtn(handle) {
    return `<button type="button" class="wish-btn" data-wish="${handle}" aria-pressed="false" aria-label="${T.wishAdd}">
      <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.5 3.8 12.3a5 5 0 0 1 7.1-7.1l1.1 1.1 1.1-1.1a5 5 0 1 1 7.1 7.1z"/></svg>
    </button>`;
  },

  mailto(subject, body) {
    const e = ONEIRO_CONFIG.contactEmail;
    return `mailto:${e}?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body || "")}`;
  },

  whatsapp(text) {
    const n = ONEIRO_CONFIG.whatsappNumber;
    if (!n) return null;
    return `https://wa.me/${n}?text=${encodeURIComponent(text || T.waDefault)}`;
  },

  observeReveals(scope) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(en => { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { threshold: .08 });
    (scope || document).querySelectorAll(".reveal:not(.in)").forEach(el => io.observe(el));
  },

  // ---------- Carrousel du hero ----------
  // Fondu enchaîné entre plusieurs visuels. Sans JavaScript, le premier
  // visuel reste affiché : le hero ne dépend pas du script pour exister.
  heroCarousel() {
    const box = document.querySelector("[data-hero-carousel]");
    if (!box) return;
    const slides = Array.from(box.querySelectorAll(".hero__slide"));
    if (slides.length < 2) return;

    const delay = Math.max(2500, parseInt(box.dataset.interval, 10) || 6000);
    const reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let i = slides.findIndex(s => s.classList.contains("is-active"));
    if (i < 0) i = 0;
    let timer = null;

    // Préchargement : évite le flash gris au premier changement
    slides.forEach(s => {
      const m = /url\(['"]?(.+?)['"]?\)/.exec(s.style.backgroundImage || "");
      if (m) { const im = new Image(); im.src = m[1]; }
    });

    const nav = document.createElement("div");
    nav.className = "hero__dots";
    nav.setAttribute("role", "group");
    nav.setAttribute("aria-label", T.heroDots);
    const dots = slides.map((_, n) => {
      const b = document.createElement("button");
      b.type = "button";
      b.className = "hero__dot" + (n === i ? " on" : "");
      b.setAttribute("aria-label", T.heroDot(n + 1, slides.length));
      b.setAttribute("aria-current", n === i ? "true" : "false");
      b.addEventListener("click", () => { go(n); restart(); });
      nav.appendChild(b);
      return b;
    });
    box.parentElement.appendChild(nav);

    function go(n) {
      i = (n + slides.length) % slides.length;
      slides.forEach((s, k) => s.classList.toggle("is-active", k === i));
      dots.forEach((d, k) => {
        d.classList.toggle("on", k === i);
        d.setAttribute("aria-current", k === i ? "true" : "false");
      });
    }
    function stop() { if (timer) { clearInterval(timer); timer = null; } }
    function start() { if (!reduce && !timer) timer = setInterval(() => go(i + 1), delay); }
    function restart() { stop(); start(); }

    const hero = box.closest(".hero") || box;
    hero.addEventListener("mouseenter", stop);
    hero.addEventListener("mouseleave", start);
    hero.addEventListener("focusin", stop);
    hero.addEventListener("focusout", start);
    document.addEventListener("visibilitychange", () => document.hidden ? stop() : start());

    // Balayage tactile
    let x0 = null;
    hero.addEventListener("touchstart", e => { x0 = e.changedTouches[0].clientX; stop(); }, { passive: true });
    hero.addEventListener("touchend", e => {
      if (x0 === null) return;
      const dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 45) go(i + (dx < 0 ? 1 : -1));
      x0 = null;
      start();
    }, { passive: true });

    start();
  },
};

document.addEventListener("DOMContentLoaded", () => {
  // Menu mobile
  const burger = document.querySelector(".burger");
  const nav = document.querySelector(".nav");
  if (burger && nav) burger.addEventListener("click", () => nav.classList.toggle("open"));

  // Lien actif
  const here = location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".nav a").forEach(a => {
    const href = (a.getAttribute("href") || "").split("/").pop();
    if (href === here) a.classList.add("active");
  });

  // Accordéons
  document.querySelectorAll(".acc__item > button").forEach(btn => {
    btn.addEventListener("click", () => btn.parentElement.classList.toggle("open"));
  });

  // Email de contact injecté partout où [data-email] est présent
  document.querySelectorAll("[data-email]").forEach(el => {
    el.textContent = ONEIRO_CONFIG.contactEmail;
    if (el.tagName === "A") el.href = "mailto:" + ONEIRO_CONFIG.contactEmail;
  });

  // Boutons WhatsApp (masqués si pas de numéro configuré)
  document.querySelectorAll("[data-whatsapp]").forEach(el => {
    const url = O.whatsapp(el.dataset.whatsapp);
    if (url) { el.href = url; el.target = "_blank"; el.rel = "noopener"; }
    else el.style.display = "none";
  });

  // CTA rendez-vous flottant (masqué sur la page rendez-vous elle-même)
  const rdvFloat = document.querySelector(".rdv-float");
  if (rdvFloat && (rdvFloat.getAttribute("href") || "").split("/").pop() === here) rdvFloat.style.display = "none";

  // Carrousel du hero
  O.heroCarousel();

  // Avis clients (accueil) — s'affiche dès que ONEIRO_CONFIG.reviews est rempli
  const reviewsZone = document.getElementById("reviews-zone");
  if (reviewsZone && Array.isArray(ONEIRO_CONFIG.reviews) && ONEIRO_CONFIG.reviews.length) {
    reviewsZone.innerHTML = ONEIRO_CONFIG.reviews.slice(0, 3).map(r => O.reviewCard(r)).join("");
    document.getElementById("reviews-section").style.display = "";
    O.observeReveals(reviewsZone);
  }

  // Vidéos de l'atelier (page À propos) — s'affiche dès que config.atelierVideos est rempli
  const videosZone = document.getElementById("videos-zone");
  if (videosZone && Array.isArray(ONEIRO_CONFIG.atelierVideos) && ONEIRO_CONFIG.atelierVideos.length) {
    const vids = ONEIRO_CONFIG.atelierVideos.slice(0, 3);
    if (vids.length === 1) videosZone.classList.add("videos--single");
    videosZone.innerHTML = vids.map(v => {
      const media = v.type === "youtube"
        ? `<iframe src="https://www.youtube-nocookie.com/embed/${v.id}?rel=0&modestbranding=1" title="${v.title || T.videoTitle}" loading="lazy" allow="fullscreen; picture-in-picture" allowfullscreen></iframe>`
        : `<video controls preload="metadata"${v.poster ? ` poster="${v.poster}"` : ""}><source src="${v.src}" type="video/mp4">${T.videoFallback}</video>`;
      return `
      <div class="video-card reveal">
        <div class="video-card__media">${media}</div>
        ${v.title ? `<span class="video-card__title">${v.title}</span>` : ""}
      </div>`;
    }).join("");
    document.getElementById("videos-section").style.display = "";
    O.observeReveals(videosZone);
  }

  // Sélection partageable : clic sur un cœur (délégation, marche aussi sur le contenu rendu en JS)
  document.addEventListener("click", e => {
    const b = e.target.closest("[data-wish]");
    if (!b) return;
    e.preventDefault();
    e.stopPropagation();
    O.wish.toggle(b.dataset.wish);
  });
  O.wish.paint();

  // Année courante
  document.querySelectorAll("[data-year]").forEach(el => el.textContent = new Date().getFullYear());

  // Animations d'apparition
  O.observeReveals(document);
});
