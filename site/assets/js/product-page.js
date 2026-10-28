// Fiche produit — hydratation (gallerie, variantes, prix, CTA).
// Handle via window.PRODUCT_HANDLE (pages statiques) ou ?p= (produit.html).
// Bilingue : les libelles suivent <html lang="...">, lu par app.js (O.lang).
document.addEventListener("DOMContentLoaded", () => {
  const EN = O.lang === "en";

  const P = EN ? {
    notFound: "Piece not found",
    notFoundText: "This piece does not exist or is no longer in the catalogue.",
    seeCollection: "See the collection",
    collectionHref: "collection.html",
    titleSuffix: " | Oneiro Paris",
    from: "From ",
    klarnaSplit: t => `or <b>3 × ${t}</b> with Klarna — interest free`,
    buy: "Buy this piece",
    reserve: "Reserve this piece",
    reserveNote: "Online purchase is coming soon. In the meantime, reserving by email commits you to nothing — we come back to you within 24 working hours with the exact quote and the secure payment options (card, bank transfer, Klarna in 3).",
    video: "See this piece by video",
    videoHref: "book-appointment.html",
    soldOut: c => `This piece is currently sold out — <a href="${c}">contact us</a> to be told when it returns, or for an equivalent creation.`,
    variantOut: "This configuration is momentarily unavailable — a close configuration can be made on request.",
    contactHref: "contact.html",
    customisable: " — customisable",
    defaultDesc: "An Oneiro creation in 18 carat gold set with certified diamonds. Further details and photographs on request — we answer within 24 working hours.",
    mailSubject: t => "Reservation — " + t,
    mailBody: (t, lines) => "Hello,\n\nI would like to reserve the creation “" + t + "” in the following configuration:\n" + lines + "\n\nPlease come back to me to finalise the order.\n",
    barBuy: "Buy",
    barReserve: "Reserve this piece",
    barChosen: "chosen configuration",
    barFrom: "from",
    accMaterials: "Materials &amp; certification",
    accMaterialsText: '18 carat gold (yellow, white or rose depending on the configuration). GIA or IGI certified diamonds — untreated natural stones from conflict-free sources, or lab-grown diamonds. The certificate of the centre stone is handed over with the piece.',
    accDelivery: "Timing &amp; delivery",
    accDeliveryText: c => `Every piece is made to order in our French workshop: allow 2 to 7 weeks depending on complexity. Free, tracked delivery in France and internationally. A date you cannot miss? <a href="${c}">Tell us before you order.</a>`,
    accReturns: "Returns, warranty &amp; care",
    accReturnsText: g => `15 day returns on fine jewellery (unworn, in its original condition). Personalised creations and loose stones cannot be returned or exchanged. Manufacturing warranty, resizing possible depending on the model. <a href="${g}">All our guarantees.</a>`,
    accCustom: "Personalise this model",
    accCustomText: s => `Another stone, another shape, other proportions, an engraving: this model can serve as the starting point for a bespoke creation. <a href="${s}">See how it works.</a>`,
    guaranteesHref: "guarantees.html",
    customHref: "custom-made.html",
  } : {
    notFound: "Création introuvable",
    notFoundText: "Cette pièce n'existe pas ou n'est plus au catalogue.",
    seeCollection: "Voir la collection",
    collectionHref: "collection.html",
    titleSuffix: " | Oneiro Paris",
    from: "À partir de ",
    klarnaSplit: t => `ou <b>3 × ${t}</b> avec Klarna — sans frais`,
    buy: "Acheter cette pièce",
    reserve: "Réserver cette pièce",
    reserveNote: "L'achat en ligne arrive bientôt. En attendant, la réservation par email est sans engagement — nous revenons vers vous sous 24 h ouvrées avec le devis exact et les modalités de paiement sécurisé (CB, virement, Klarna 3×).",
    video: "Voir cette pièce en visio",
    videoHref: "rendez-vous.html",
    soldOut: c => `Cette pièce est actuellement épuisée — <a href="${c}">contactez-nous</a> pour être prévenu·e de son retour ou pour une création équivalente.`,
    variantOut: "Cette configuration est momentanément indisponible — une configuration proche peut être réalisée sur demande.",
    contactHref: "contact.html",
    customisable: " — personnalisable",
    defaultDesc: "Création Oneiro en or 18 carats et diamants certifiés. Détails et photos complémentaires sur demande — nous répondons sous 24 h ouvrées.",
    mailSubject: t => "Réservation — " + t,
    mailBody: (t, lines) => "Bonjour,\n\nJe souhaite réserver la création « " + t + " » dans la configuration suivante :\n" + lines + "\n\nMerci de me recontacter pour finaliser la commande.\n",
    barBuy: "Acheter",
    barReserve: "Réserver cette pièce",
    barChosen: "configuration choisie",
    barFrom: "à partir de",
    accMaterials: "Matières &amp; certification",
    accMaterialsText: "Or 18 carats (jaune, blanc ou rose selon configuration). Diamants certifiés GIA ou IGI — naturels non traités issus de zones sans conflit, ou diamants de laboratoire. Le certificat de la pierre centrale est remis avec le bijou.",
    accDelivery: "Délais &amp; livraison",
    accDeliveryText: c => `Chaque pièce est réalisée à la demande dans notre atelier français : comptez 2 à 7 semaines selon la complexité. Livraison offerte et suivie, en France et à l'international. Une date impérative ? <a href="${c}">Dites-le nous avant de commander.</a>`,
    accReturns: "Retours, garantie &amp; entretien",
    accReturnsText: g => `Retour sous 15 jours pour la joaillerie fine (pièce non portée, dans son état d'origine). Les créations personnalisées et pierres seules ne sont ni reprises ni échangées. Garantie fabrication, mise à taille possible selon modèle. <a href="${g}">Toutes nos garanties.</a>`,
    accCustom: "Personnaliser ce modèle",
    accCustomText: s => `Autre pierre, autre forme, autres proportions, gravure : ce modèle peut servir de point de départ à une création sur-mesure. <a href="${s}">Voir comment ça marche.</a>`,
    guaranteesHref: "garanties.html",
    customHref: "sur-mesure.html",
  };

  // Traduction des noms et valeurs d'options (le catalogue source est en français)
  const OPT = EN ? {
    "Couleur": "Colour", "Taille diamants": "Diamond size", "Type de diamants": "Diamond type",
    "Type de diamant": "Diamond type", "Type de Diamant": "Diamond type", "Type de Diamants": "Diamond type",
    "Pierre Centrale": "Centre stone", "Sertissage": "Setting", "Taille de l’anneau": "Ring size",
    "Or": "Yellow gold", "Or blanc": "White gold", "Or rose": "Rose gold", "Platine": "Platinum",
    "Naturel": "Natural", "Naturels": "Natural", "Laboratoire": "Lab-grown", "Laboratoires": "Lab-grown",
    "Avec griffes": "Claw set", "Avec Halo": "With halo",
  } : {};
  const tr = v => OPT[v] || v;

  const handle = window.PRODUCT_HANDLE || new URLSearchParams(location.search).get("p");
  const p = O.product(handle);
  const root = document.getElementById("product");

  if (!p) {
    root.innerHTML = `<div><h1>${P.notFound}</h1><p class='pinfo__desc'>${P.notFoundText}</p><a class='btn' href='${P.collectionHref}'>${P.seeCollection}</a></div>`;
    return;
  }

  const TITLE = O.title(p);
  document.title = TITLE + " — " + O.catLabel(p.category) + P.titleSuffix;

  // --- État de sélection
  const sel = {};
  p.options.forEach(o => sel[o.name] = o.values[0]);

  function currentVariant() {
    const want = p.options.map(o => sel[o.name]).join(" / ");
    return p.variants.find(v => v.title === want) || null;
  }

  function mailtoLink() {
    const lines = Object.entries(sel).map(([k, val]) => "- " + tr(k) + ": " + tr(val)).join("\n");
    return O.mailto(P.mailSubject(TITLE), P.mailBody(TITLE, lines));
  }

  function priceBlock() {
    const v = currentVariant();
    const price = v ? v.price : (p.priceFrom || null);
    const prefix = v ? "" : P.from;
    let html = `<div class="pinfo__price">${prefix}${O.fmt(price)}</div>`;
    if (price) {
      const third = Math.round(price / 3);
      html += `<div class="pinfo__klarna">${P.klarnaSplit(O.fmt(third))}</div>`;
    }
    return html;
  }

  function ctaBlock() {
    const cfg = ONEIRO_CONFIG.shopify;
    let html = `<div class="pinfo__cta">`;
    if (cfg.enabled && cfg.domain) {
      html += `<a class="btn btn--solid" href="https://${cfg.domain}/products/${p.handle}" target="_blank" rel="noopener">${P.buy}</a>`;
    } else {
      html += `<a class="btn btn--solid" href="${mailtoLink()}">${P.reserve}</a>`;
      html += `<span class="pinfo__note">${P.reserveNote}</span>`;
    }
    html += `<a class="btn" href="${P.videoHref}">${P.video}</a></div>`;
    return html;
  }

  function avail() {
    const v = currentVariant();
    if (p.variants.length && !p.variants.some(x => x.available)) {
      return `<p class="pinfo__note" style="color:var(--danger)">${P.soldOut(P.contactHref)}</p>`;
    }
    if (v && !v.available) {
      return `<p class="pinfo__note" style="color:var(--danger)">${P.variantOut}</p>`;
    }
    return "";
  }

  function optionsBlock() {
    return p.options.map(o => `
      <div class="opt" data-opt="${o.name}">
        <label>${tr(o.name)}</label>
        <div class="opt__values">
          ${o.values.map(v => `<button type="button" data-v="${v}" class="${sel[o.name] === v ? "on" : ""}">${tr(v)}</button>`).join("")}
        </div>
      </div>`).join("");
  }

  function render() {
    const imgs = p.images && p.images.length ? p.images : [];
    root.innerHTML = `
      <div class="gallery">
        <div class="gallery__main" style="position:relative"><img id="gmain" src="${O.img(imgs[0], 1100)}" alt="${TITLE} — Oneiro Paris"></div>
        ${imgs.length > 1 ? `<div class="gallery__thumbs">${imgs.map((s, i) =>
          `<button type="button" class="${i === 0 ? "on" : ""}" data-i="${i}"><img src="${O.img(s, 200)}" alt=""></button>`).join("")}</div>` : ""}
      </div>
      <div class="pinfo">
        <span class="kicker">${O.catLabel(p.category)}${p.customizable ? P.customisable : ""}</span>
        <h1 class="has-wish">${TITLE} ${O.wishBtn(p.handle)}</h1>
        <div id="price-zone">${priceBlock()}</div>
        <p class="pinfo__desc">${O.desc(p) || P.defaultDesc}</p>
        <div id="opts">${optionsBlock()}</div>
        <div id="avail-zone">${avail()}</div>
        <div id="cta-zone">${ctaBlock()}</div>
        <div class="acc">
          <div class="acc__item">
            <button type="button">${P.accMaterials}</button>
            <div class="acc__panel"><p>${P.accMaterialsText}</p></div>
          </div>
          <div class="acc__item">
            <button type="button">${P.accDelivery}</button>
            <div class="acc__panel"><p>${P.accDeliveryText(P.contactHref)}</p></div>
          </div>
          <div class="acc__item">
            <button type="button">${P.accReturns}</button>
            <div class="acc__panel"><p>${P.accReturnsText(P.guaranteesHref)}</p></div>
          </div>
          <div class="acc__item">
            <button type="button">${P.accCustom}</button>
            <div class="acc__panel"><p>${P.accCustomText(P.customHref)}</p></div>
          </div>
        </div>
      </div>`;

    // interactions
    root.querySelectorAll(".gallery__thumbs button").forEach(b => {
      b.addEventListener("click", () => {
        root.querySelectorAll(".gallery__thumbs button").forEach(x => x.classList.remove("on"));
        b.classList.add("on");
        document.getElementById("gmain").src = O.img(p.images[+b.dataset.i], 1100);
      });
    });
    root.querySelectorAll(".opt").forEach(optEl => {
      optEl.querySelectorAll("button").forEach(b => {
        b.addEventListener("click", () => {
          sel[optEl.dataset.opt] = b.dataset.v;
          optEl.querySelectorAll("button").forEach(x => x.classList.remove("on"));
          b.classList.add("on");
          document.getElementById("price-zone").innerHTML = priceBlock();
          document.getElementById("avail-zone").innerHTML = avail();
          document.getElementById("cta-zone").innerHTML = ctaBlock();
          paintBar();
        });
      });
    });
    root.querySelectorAll(".acc__item > button").forEach(btn => {
      btn.addEventListener("click", () => btn.parentElement.classList.toggle("open"));
    });
  }

  render();

  // --- Barre d'action fixe en bas d'écran (mobile) ---
  const bar = document.createElement("div");
  bar.className = "pbar";
  document.body.appendChild(bar);
  document.body.classList.add("has-pbar");

  function paintBar() {
    const v = currentVariant();
    const price = v ? v.price : (p.priceFrom || null);
    const cfg = ONEIRO_CONFIG.shopify;
    const label = (cfg.enabled && cfg.domain) ? P.barBuy : P.barReserve;
    const href = (cfg.enabled && cfg.domain)
      ? `https://${cfg.domain}/products/${p.handle}`
      : mailtoLink();
    bar.innerHTML = `
      <span class="pbar__price">${O.fmt(price)}<small>${v ? P.barChosen : P.barFrom}</small></span>
      <a class="btn btn--solid" href="${href}">${label}</a>`;
  }
  paintBar();

  // Suggestions : même catégorie d'abord, puis le reste
  const rel = ONEIRO_PRODUCTS.filter(x => x.handle !== p.handle)
    .sort((a, b) => (b.category === p.category) - (a.category === p.category))
    .slice(0, 4);
  O.renderCards(document.getElementById("related"), rel);
});
