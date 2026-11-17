// Fiche produit - hydratation (galerie, variantes, prix, CTA).
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
    priceOnRequest: "Price on request",
    buy: "Buy this piece",
    reserve: "Contact us for this piece",
    reserveNote: "Reserving commits you to nothing: we come back to you within 24 working hours with full guidance and bespoke options.",
    video: "See this piece by video",
    videoHref: "book-appointment.html",
    soldOut: c => `This piece is currently unavailable: <a href="${c}">contact us</a> for an equivalent creation.`,
    variantOut: "This configuration is momentarily unavailable: a bespoke equivalent can be crafted on request.",
    contactHref: "contact.html",
    customisable: " - customisable",
    defaultDesc: "An Oneiro creation in 14k gold, 18k gold or platinum set with GIA, IGI or HRD certified diamonds. Further details and photographs on request: we answer within 24 working hours.",
    barBuy: "Buy",
    barReserve: "Contact us",
    barChosen: "chosen configuration",
    barFrom: "from",
    accMaterials: "Materials &amp; certification",
    accMaterialsText: '14k gold, 18k gold or platinum. GIA, IGI or HRD certified diamonds: untreated natural stones from conflict-free sources, or lab-grown diamonds. The certificate of the centre stone is handed over with the piece.',
    accDelivery: "Timing &amp; delivery",
    accDeliveryText: c => `Every piece is made to order in our French workshop: allow 4 to 6 weeks on average depending on complexity. Free, tracked delivery in France and internationally. A date you cannot miss? <a href="${c}">Tell us before you order.</a>`,
    accReturns: "Returns, warranty &amp; care",
    accReturnsText: g => `In accordance with article L221-28, every bespoke creation approved in 3D is crafted exclusively for you and cannot be returned. Statutory warranty covering manufacturing defects, resizing on request depending on feasibility and model structure. <a href="${g}">All our guarantees.</a>`,
    accCustom: "Personalise this model",
    accCustomText: s => `Another stone, another shape, other proportions, an engraving: this model can serve as the starting point for a bespoke creation. <a href="${s}">See how it works.</a>`,
    guaranteesHref: "guarantees.html",
    customHref: "custom-made.html",
  } : {
    notFound: "Cr\u00e9ation introuvable",
    notFoundText: "Cette pi\u00e8ce n'existe pas ou n'est plus au catalogue.",
    seeCollection: "Voir la collection",
    collectionHref: "collection.html",
    titleSuffix: " | Oneiro Paris",
    from: "\u00c0 partir de ",
    priceOnRequest: "Prix sur demande",
    buy: "Acheter cette pi\u00e8ce",
    reserve: "Nous contacter pour cette pi\u00e8ce",
    reserveNote: "La demande d'information est sans engagement : nous revenons vers vous sous 24 h ouvr\u00e9es avec les d\u00e9tails et les options sur-mesure.",
    video: "Voir cette pi\u00e8ce en visio",
    videoHref: "rendez-vous.html",
    soldOut: c => `Cette pi\u00e8ce est actuellement indisponible : <a href="${c}">contactez-nous</a> pour une cr\u00e9ation \u00e9quivalente.`,
    variantOut: "Cette configuration est momentan\u00e9ment indisponible : une r\u00e9alisation sur-mesure \u00e9quivalente est possible.",
    contactHref: "contact.html",
    customisable: " - personnalisable",
    defaultDesc: "Cr\u00e9ation Oneiro en or 14k, 18k ou platine et diamants certifi\u00e9s GIA, IGI ou HRD. D\u00e9tails et photos compl\u00e9mentaires sur demande : nous r\u00e9pondons sous 24 h ouvr\u00e9es.",
    barBuy: "Acheter",
    barReserve: "Nous contacter",
    barChosen: "configuration choisie",
    barFrom: "\u00e0 partir de",
    accMaterials: "Mati\u00e8res &amp; certification",
    accMaterialsText: "Or 14k, 18k ou platine. Diamants certifi\u00e9s GIA, IGI ou HRD : naturels non trait\u00e9s issus de zones sans conflit, ou diamants de laboratoire. Le certificat de la pierre centrale est remis avec le bijou.",
    accDelivery: "D\u00e9lais &amp; livraison",
    accDeliveryText: c => `Chaque pi\u00e8ce est r\u00e9alis\u00e9e \u00e0 la demande dans notre atelier fran\u00e7ais : comptez en moyenne 4 \u00e0 6 semaines selon la complexit\u00e9. Livraison offerte et suivie, en France et \u00e0 l'international. Une date imp\u00e9rative ? <a href="${c}">Dites-le nous avant de commander.</a>`,
    accReturns: "Retours, garantie &amp; entretien",
    accReturnsText: g => `Conform\u00e9ment \u00e0 l'article L221-28, chaque cr\u00e9ation sur-mesure valid\u00e9e en 3D est confectionn\u00e9e exclusivement pour vous et ne fait l'objet d'aucun retour. Garantie l\u00e9gale contre tout d\u00e9faut de fabrication, mise \u00e0 taille sur demande selon faisabilit\u00e9 et structure du mod\u00e8le. <a href="${g}">Toutes nos garanties.</a>`,
    accCustom: "Personnaliser ce mod\u00e8le",
    accCustomText: s => `Autre pierre, autre forme, autres proportions, gravure : ce mod\u00e8le peut servir de point de d\u00e9part \u00e0 une cr\u00e9ation sur-mesure. <a href="${s}">Voir comment \u00e7a marche.</a>`,
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
  document.title = TITLE + " - " + O.catLabel(p.category) + P.titleSuffix;

  // --- État de sélection
  const sel = {};
  p.options.forEach(o => sel[o.name] = o.values[0]);

  function currentVariant() {
    const want = p.options.map(o => sel[o.name]).join(" / ");
    return p.variants.find(v => v.title === want) || null;
  }

  function contactLink() {
    const lines = Object.entries(sel).map(([k, val]) => tr(k) + ": " + tr(val)).join(", ");
    const sp = new URLSearchParams();
    sp.set("piece", TITLE);
    if (lines) sp.set("config", lines);
    return `${P.contactHref}?${sp.toString()}`;
  }

  function priceBlock() {
    return `<div class="pinfo__price">${P.priceOnRequest}</div>`;
  }

  function ctaBlock() {
    const cfg = ONEIRO_CONFIG.shopify;
    let html = `<div class="pinfo__cta">`;
    if (cfg.enabled && cfg.domain) {
      html += `<a class="btn btn--solid" href="https://${cfg.domain}/products/${p.handle}" target="_blank" rel="noopener">${P.buy}</a>`;
    } else {
      html += `<a class="btn btn--solid" href="${contactLink()}">${P.reserve}</a>`;
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
        <div class="gallery__main" style="position:relative"><img id="gmain" src="${O.img(imgs[0], 1100)}" alt="${TITLE} - Oneiro Paris"></div>
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
    const cfg = ONEIRO_CONFIG.shopify;
    const label = (cfg.enabled && cfg.domain) ? P.barBuy : P.barReserve;
    const href = (cfg.enabled && cfg.domain)
      ? `https://${cfg.domain}/products/${p.handle}`
      : contactLink();
    bar.innerHTML = `
      <span class="pbar__price">${P.priceOnRequest}</span>
      <a class="btn btn--solid" href="${href}">${label}</a>`;
  }
  paintBar();

  // Suggestions : même catégorie d'abord, puis le reste
  const rel = ONEIRO_PRODUCTS.filter(x => x.handle !== p.handle)
    .sort((a, b) => (b.category === p.category) - (a.category === p.category))
    .slice(0, 4);
  O.renderCards(document.getElementById("related"), rel);
});

  // Suggestions : même catégorie d'abord, puis le reste
  const rel = ONEIRO_PRODUCTS.filter(x => x.handle !== p.handle)
    .sort((a, b) => (b.category === p.category) - (a.category === p.category))
    .slice(0, 4);
  O.renderCards(document.getElementById("related"), rel);
});
