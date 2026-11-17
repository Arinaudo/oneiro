// ============================================================
// ONEIRO PARIS - Configurateur de diamant d'exception
// Selecteur visuel, echelles 4C completes, couleurs Fancy rares,
// rendu 3D holographique anime, certifications GIA, IGI ou HRD.
// ============================================================

(function () {
  const EN = (document.documentElement.getAttribute("lang") || "fr")
    .slice(0, 2).toLowerCase() === "en";

  const SHAPE_SVGS = {
    Round: '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9.5"/><polygon points="12,5.5 16.5,8.5 16.5,15.5 12,18.5 7.5,15.5 7.5,8.5"/><line x1="12" y1="2.5" x2="12" y2="5.5"/><line x1="12" y1="18.5" x2="12" y2="21.5"/><line x1="2.5" y1="12" x2="7.5" y2="12"/><line x1="16.5" y1="12" x2="21.5" y2="12"/></svg>',
    Oval: '<svg viewBox="0 0 24 24"><ellipse cx="12" cy="12" rx="7" ry="9.5"/><ellipse cx="12" cy="12" rx="4" ry="6"/><line x1="12" y1="2.5" x2="12" y2="6"/><line x1="12" y1="18" x2="12" y2="21.5"/><line x1="5" y1="12" x2="8" y2="12"/><line x1="16" y1="12" x2="19" y2="12"/></svg>',
    Pear: '<svg viewBox="0 0 24 24"><path d="M12,2.5 C16,9 18.5,14 18.5,16.5 A6.5,6.5 0 0,1 5.5,16.5 C5.5,14 8,9 12,2.5 Z"/><ellipse cx="12" cy="15" rx="3.5" ry="4"/><line x1="12" y1="2.5" x2="12" y2="11"/></svg>',
    Emerald: '<svg viewBox="0 0 24 24"><polygon points="6,3.5 18,3.5 20.5,6 20.5,18 18,20.5 6,20.5 3.5,18 3.5,6"/><polygon points="8,6 16,6 17.5,7.5 17.5,16.5 16,18 8,18 6.5,16.5 6.5,7.5"/><line x1="3.5" y1="6" x2="6.5" y2="7.5"/><line x1="20.5" y1="6" x2="17.5" y2="7.5"/><line x1="3.5" y1="18" x2="6.5" y2="16.5"/><line x1="20.5" y1="18" x2="17.5" y2="16.5"/></svg>',
    Cushion: '<svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16" rx="4.5"/><polygon points="12,7 17,12 12,17 7,12"/><line x1="4" y1="4" x2="7" y2="12"/><line x1="20" y1="4" x2="17" y2="12"/><line x1="4" y1="20" x2="7" y2="12"/><line x1="20" y1="20" x2="17" y2="12"/></svg>',
    Radiant: '<svg viewBox="0 0 24 24"><polygon points="6,3.5 18,3.5 20.5,6 20.5,18 18,20.5 6,20.5 3.5,18 3.5,6"/><polygon points="12,6.5 17.5,12 12,17.5 6.5,12"/><line x1="6" y1="3.5" x2="12" y2="6.5"/><line x1="18" y1="3.5" x2="12" y2="6.5"/><line x1="6" y1="20.5" x2="12" y2="17.5"/><line x1="18" y1="20.5" x2="12" y2="17.5"/></svg>',
    Marquise: '<svg viewBox="0 0 24 24"><path d="M12,2.5 C17.5,7 19.5,12 12,21.5 C4.5,12 6.5,7 12,2.5 Z"/><polygon points="12,6 15.5,12 12,18 8.5,12"/></svg>',
    Princess: '<svg viewBox="0 0 24 24"><rect x="4" y="4" width="16" height="16"/><line x1="4" y1="4" x2="20" y2="20"/><line x1="20" y1="4" x2="4" y2="20"/><rect x="8" y="8" width="8" height="8"/></svg>',
    Asscher: '<svg viewBox="0 0 24 24"><polygon points="7,3.5 17,3.5 20.5,7 20.5,17 17,20.5 7,20.5 3.5,17 3.5,7"/><polygon points="8.5,6 15.5,6 18,8.5 18,15.5 15.5,18 8.5,18 6,15.5 6,8.5"/><rect x="9" y="9" width="6" height="6"/></svg>',
  };

  // SVGs facettes 3D pour la scene holographique animee
  function buildFacetSvg(shape, fillGradId, strokeColor) {
    const stroke = strokeColor || "rgba(255,255,255,0.75)";
    const fill = `url(#${fillGradId})`;

    switch (shape) {
      case "Oval":
        return `<svg viewBox="0 0 100 100">
          <ellipse cx="50" cy="50" rx="36" ry="46" fill="${fill}" stroke="${stroke}" stroke-width="1.5"/>
          <ellipse cx="50" cy="50" rx="20" ry="26" fill="rgba(255,255,255,0.18)" stroke="${stroke}" stroke-width="1.2"/>
          <line x1="50" y1="4" x2="50" y2="24" stroke="${stroke}" stroke-width="1.2"/>
          <line x1="50" y1="76" x2="50" y2="96" stroke="${stroke}" stroke-width="1.2"/>
          <line x1="14" y1="50" x2="30" y2="50" stroke="${stroke}" stroke-width="1.2"/>
          <line x1="70" y1="50" x2="86" y2="50" stroke="${stroke}" stroke-width="1.2"/>
          <polygon points="50,24 64,36 64,64 50,76 36,64 36,36" fill="rgba(255,255,255,0.12)" stroke="${stroke}" stroke-width="1"/>
        </svg>`;
      case "Pear":
        return `<svg viewBox="0 0 100 100">
          <path d="M50,8 C68,36 82,60 82,72 A32,32 0 0,1 18,72 C18,60 32,36 50,8 Z" fill="${fill}" stroke="${stroke}" stroke-width="1.5"/>
          <ellipse cx="50" cy="66" rx="16" ry="18" fill="rgba(255,255,255,0.18)" stroke="${stroke}" stroke-width="1.2"/>
          <line x1="50" y1="8" x2="50" y2="48" stroke="${stroke}" stroke-width="1.2"/>
          <line x1="50" y1="84" x2="50" y2="98" stroke="${stroke}" stroke-width="1.2"/>
          <polygon points="50,48 64,60 50,80 36,60" fill="rgba(255,255,255,0.15)" stroke="${stroke}" stroke-width="1"/>
        </svg>`;
      case "Emerald":
        return `<svg viewBox="0 0 100 100">
          <polygon points="26,12 74,12 86,24 86,76 74,88 26,88 14,76 14,24" fill="${fill}" stroke="${stroke}" stroke-width="1.5"/>
          <polygon points="34,22 66,22 76,32 76,68 66,78 34,78 24,68 24,32" fill="rgba(255,255,255,0.16)" stroke="${stroke}" stroke-width="1.2"/>
          <polygon points="40,30 60,30 68,38 68,62 60,70 40,70 32,62 32,38" fill="rgba(255,255,255,0.22)" stroke="${stroke}" stroke-width="1"/>
          <line x1="14" y1="24" x2="32" y2="38" stroke="${stroke}" stroke-width="1"/>
          <line x1="86" y1="24" x2="68" y2="38" stroke="${stroke}" stroke-width="1"/>
          <line x1="14" y1="76" x2="32" y2="62" stroke="${stroke}" stroke-width="1"/>
          <line x1="86" y1="76" x2="68" y2="62" stroke="${stroke}" stroke-width="1"/>
        </svg>`;
      case "Cushion":
        return `<svg viewBox="0 0 100 100">
          <rect x="15" y="15" width="70" height="70" rx="20" fill="${fill}" stroke="${stroke}" stroke-width="1.5"/>
          <polygon points="50,26 74,50 50,74 26,50" fill="rgba(255,255,255,0.2)" stroke="${stroke}" stroke-width="1.2"/>
          <line x1="15" y1="15" x2="32" y2="32" stroke="${stroke}" stroke-width="1"/>
          <line x1="85" y1="15" x2="68" y2="32" stroke="${stroke}" stroke-width="1"/>
          <line x1="15" y1="85" x2="32" y2="68" stroke="${stroke}" stroke-width="1"/>
          <line x1="85" y1="85" x2="68" y2="68" stroke="${stroke}" stroke-width="1"/>
        </svg>`;
      case "Radiant":
        return `<svg viewBox="0 0 100 100">
          <polygon points="26,12 74,12 86,24 86,76 74,88 26,88 14,76 14,24" fill="${fill}" stroke="${stroke}" stroke-width="1.5"/>
          <polygon points="50,26 72,50 50,74 28,50" fill="rgba(255,255,255,0.2)" stroke="${stroke}" stroke-width="1.2"/>
          <line x1="26" y1="12" x2="50" y2="26" stroke="${stroke}" stroke-width="1"/>
          <line x1="74" y1="12" x2="50" y2="26" stroke="${stroke}" stroke-width="1"/>
          <line x1="86" y1="24" x2="72" y2="50" stroke="${stroke}" stroke-width="1"/>
          <line x1="86" y1="76" x2="72" y2="50" stroke="${stroke}" stroke-width="1"/>
          <line x1="74" y1="88" x2="50" y2="74" stroke="${stroke}" stroke-width="1"/>
          <line x1="26" y1="88" x2="50" y2="74" stroke="${stroke}" stroke-width="1"/>
        </svg>`;
      case "Marquise":
        return `<svg viewBox="0 0 100 100">
          <path d="M50,6 C78,32 86,50 50,94 C14,50 22,32 50,6 Z" fill="${fill}" stroke="${stroke}" stroke-width="1.5"/>
          <polygon points="50,22 68,50 50,78 32,50" fill="rgba(255,255,255,0.22)" stroke="${stroke}" stroke-width="1.2"/>
          <line x1="50" y1="6" x2="50" y2="22" stroke="${stroke}" stroke-width="1.2"/>
          <line x1="50" y1="78" x2="50" y2="94" stroke="${stroke}" stroke-width="1.2"/>
        </svg>`;
      case "Princess":
        return `<svg viewBox="0 0 100 100">
          <rect x="16" y="16" width="68" height="68" fill="${fill}" stroke="${stroke}" stroke-width="1.5"/>
          <polygon points="50,24 76,50 50,76 24,50" fill="rgba(255,255,255,0.2)" stroke="${stroke}" stroke-width="1.2"/>
          <line x1="16" y1="16" x2="84" y2="84" stroke="${stroke}" stroke-width="1"/>
          <line x1="84" y1="16" x2="16" y2="84" stroke="${stroke}" stroke-width="1"/>
          <rect x="36" y="36" width="28" height="28" fill="rgba(255,255,255,0.18)" stroke="${stroke}" stroke-width="1"/>
        </svg>`;
      case "Asscher":
        return `<svg viewBox="0 0 100 100">
          <polygon points="28,14 72,14 86,28 86,72 72,86 28,86 14,72 14,28" fill="${fill}" stroke="${stroke}" stroke-width="1.5"/>
          <polygon points="35,24 65,24 76,35 76,65 65,76 35,76 24,65 24,35" fill="rgba(255,255,255,0.18)" stroke="${stroke}" stroke-width="1.2"/>
          <polygon points="42,34 58,34 66,42 66,58 58,66 42,66 34,58 34,42" fill="rgba(255,255,255,0.24)" stroke="${stroke}" stroke-width="1"/>
          <line x1="14" y1="14" x2="34" y2="34" stroke="${stroke}" stroke-width="1"/>
          <line x1="86" y1="14" x2="66" y2="34" stroke="${stroke}" stroke-width="1"/>
          <line x1="14" y1="86" x2="34" y2="66" stroke="${stroke}" stroke-width="1"/>
          <line x1="86" y1="86" x2="66" y2="66" stroke="${stroke}" stroke-width="1"/>
        </svg>`;
      case "Round":
      default:
        return `<svg viewBox="0 0 100 100">
          <circle cx="50" cy="50" r="44" fill="${fill}" stroke="${stroke}" stroke-width="1.5"/>
          <polygon points="50,18 72,32 72,68 50,82 28,68 28,32" fill="rgba(255,255,255,0.18)" stroke="${stroke}" stroke-width="1.2"/>
          <polygon points="50,28 64,38 64,62 50,72 36,62 36,38" fill="rgba(255,255,255,0.22)" stroke="${stroke}" stroke-width="1"/>
          <line x1="50" y1="6" x2="50" y2="18" stroke="${stroke}" stroke-width="1.2"/>
          <line x1="50" y1="82" x2="50" y2="94" stroke="${stroke}" stroke-width="1.2"/>
          <line x1="6" y1="50" x2="28" y2="50" stroke="${stroke}" stroke-width="1.2"/>
          <line x1="72" y1="50" x2="94" y2="50" stroke="${stroke}" stroke-width="1.2"/>
        </svg>`;
    }
  }

  const FANCY_COLORS = [
    { id: "Yellow", fr: "Jaune", en: "Yellow", hex: "#facc15", factor: 1.15, glow: "rgba(250, 204, 21, 0.55)", stops: ["#fef08a", "#facc15", "#eab308"] },
    { id: "Pink", fr: "Rose", en: "Pink", hex: "#f472b6", factor: 2.10, glow: "rgba(244, 114, 182, 0.55)", stops: ["#fbcfe8", "#f472b6", "#db2777"] },
    { id: "Blue", fr: "Bleu", en: "Blue", hex: "#38bdf8", factor: 2.25, glow: "rgba(56, 189, 248, 0.55)", stops: ["#bae6fd", "#38bdf8", "#0284c7"] },
    { id: "Champagne", fr: "Champagne", en: "Champagne", hex: "#d4af37", factor: 0.88, glow: "rgba(212, 175, 55, 0.55)", stops: ["#fef3c7", "#d4af37", "#b45309"] },
    { id: "Green", fr: "Vert", en: "Green", hex: "#4ade80", factor: 1.95, glow: "rgba(74, 222, 128, 0.55)", stops: ["#bbf7d0", "#4ade80", "#16a34a"] }
  ];

  const T = EN ? {
    originLabel: "Stone Origin",
    naturalTitle: "Natural Diamond",
    naturalSub: "GIA / IGI / HRD certified - Geological treasure",
    labTitle: "Lab-grown Diamond",
    labSub: "GIA / IGI / HRD certified - Sustainable & ethical",
    shape: "Diamond Shape",
    carat: "Carat Weight",
    color: "Colour (D to Z)",
    colorDesc: "D-F: Colorless | G-J: Near Colorless | K-Z: Warm & solar hues",
    fancyLabel: "Rare Fancy Colours",
    clarity: "Clarity (FL to SI2)",
    clarityDesc: "FL: Flawless (purest in the world) | IF-VVS: Exceptional | VS-SI: Eye-clean",
    cut: "Cut Grade",
    cutNotice: "High Jewellery Exclusive: We exclusively source 'Excellent' cut diamonds to ensure optimum light performance, brilliance, and fire.",
    polishSym: "Polish & Symmetry",
    fluorescence: "Fluorescence",
    certificate: "Certificate",
    certNotice: "Delivered with an independent laboratory certificate GIA, IGI or HRD (laser inscribed on girdle).",
    estimateRange: "Indicative Range",
    estimateSub: "Indicative market range (incl. VAT). Firm quote and bespoke HD video selection within 24 to 48 hours.",
    ctaSource: "Request this stone from our workshop",
    ctaVideo: "Book a video appointment",
    summaryTitle: "Gemmological Profile",
    mailSubject: "Bespoke diamond sourcing request",
    shapes: {
      Round: "Round", Oval: "Oval", Pear: "Pear", Emerald: "Emerald",
      Cushion: "Cushion", Radiant: "Radiant", Marquise: "Marquise",
      Princess: "Princess", Asscher: "Asscher"
    },
    cuts: { Excellent: "Excellent" },
    polishOpts: { Excellent: "Excellent", VeryGood: "Very Good" },
    fluoOpts: { None: "None", Faint: "Faint", Medium: "Medium" }
  } : {
    originLabel: "Origine de la pierre",
    naturalTitle: "Diamant Naturel",
    naturalSub: "Certifi\u00e9 GIA / IGI / HRD - Tr\u00e9sor g\u00e9ologique",
    labTitle: "Diamant de Laboratoire",
    labSub: "Certifi\u00e9 GIA / IGI / HRD - \u00c9co-con\u00e7u & contemporain",
    shape: "Forme de taille",
    carat: "Poids en carats",
    color: "Couleur (D \u00e0 Z)",
    colorDesc: "D-F : Incolore parfait | G-J : Quasi incolore | K-Z : Nuances solaires",
    fancyLabel: "Couleurs Fancy rares",
    clarity: "Puret\u00e9 (FL \u00e0 SI2)",
    clarityDesc: "FL : Flawless (puret\u00e9 supr\u00eame) | IF-VVS : Exceptionnel | VS-SI : Pur \u00e0 l'oeil nu",
    cut: "Qualit\u00e9 de taille",
    cutNotice: "Exclusivit\u00e9 Haute Joaillerie : nous s\u00e9lectionnons exclusivement la taille \u00ab Excellent \u00bb pour garantir une r\u00e9fraction maximale de la lumi\u00e8re et un feu parfait.",
    polishSym: "Poli & Sym\u00e9trie",
    fluorescence: "Fluorescence",
    certificate: "Certification",
    certNotice: "Chaque pierre est accompagn\u00e9e de son certificat officiel GIA, IGI ou HRD avec gravure laser sur le rondiste.",
    estimateRange: "Fourchette indicative",
    estimateSub: "Fourchette de march\u00e9 indicative TTC. Devis d'atelier ferme et s\u00e9lection vid\u00e9o sous 24 \u00e0 48 h ouvr\u00e9es.",
    ctaSource: "Demander cette pierre \u00e0 l'atelier",
    ctaVideo: "Prendre rendez-vous en visio",
    summaryTitle: "Profil gemmologique",
    mailSubject: "Demande de sourcing diamant sur-mesure",
    shapes: {
      Round: "Rond", Oval: "Ovale", Pear: "Poire", Emerald: "\u00c9meraude",
      Cushion: "Coussin", Radiant: "Radiant", Marquise: "Marquise",
      Princess: "Princesse", Asscher: "Asscher"
    },
    cuts: { Excellent: "Excellent" },
    polishOpts: { Excellent: "Excellent", VeryGood: "Tr\u00e8s bon" },
    fluoOpts: { None: "Aucune", Faint: "Faible", Medium: "Moyenne" }
  };

  const SHAPES = ["Round", "Oval", "Pear", "Emerald", "Cushion", "Radiant", "Marquise", "Princess", "Asscher"];
  const COLORS = ["D", "E", "F", "G", "H", "I", "J", "K-L", "M-N", "O-P", "Q-R", "S-Z"];
  const CLARITIES = ["FL", "IF", "VVS1", "VVS2", "VS1", "VS2", "SI1", "SI2"];
  const CARAT_QUICKS = [0.50, 0.70, 1.00, 1.50, 2.00, 3.00];

  function esc(s) {
    return String(s || "").replace(/[<>&"]/g, c => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;" }[c]));
  }

  function fmtMoney(n) {
    return new Intl.NumberFormat(EN ? "en-GB" : "fr-FR", {
      style: "currency", currency: "EUR", maximumFractionDigits: 0
    }).format(n);
  }

  // Grille officielle des marges boutique Oneiro (extraite des reglages Nivoda / Boutique)
  function getBoutiqueMultiplier(origin, carat) {
    if (origin === "lab") {
      if (carat <= 0.50) return 6.00;       // +500 %
      if (carat <= 0.70) return 7.00;       // +600 %
      if (carat <= 1.00) return 8.00;       // +700 %
      if (carat <= 2.00) return 11.00;      // +1000 %
      return 9.00;                          // +800 %
    } else {
      if (carat <= 0.50) return 1.80;       // +80 %
      if (carat <= 0.70) return 1.70;       // +70 %
      if (carat <= 1.00) return 1.65;       // +65 %
      if (carat <= 1.10) return 1.50;       // +50 %
      if (carat <= 1.50) return 1.45;       // +45 %
      if (carat <= 2.00) return 1.40;       // +40 %
      if (carat <= 3.00) return 1.30;       // +30 %
      if (carat <= 5.00) return 1.25;       // +25 %
      return 1.18;                          // +18 %
    }
  }

  // Estimation locale de reference en appliquant la marge de la boutique
  function computeMarketRange(st) {
    const isLab = st.origin === "lab";
    const carat = Math.max(0.3, Math.min(st.carat, 5.0));

    // Base carat de gros (marche mondial)
    const baseNaturalWholesale = 1450 * Math.pow(carat, 1.95);
    const baseLabWholesale = 85 * Math.pow(carat, 1.45);
    let wholesale = isLab ? baseLabWholesale : baseNaturalWholesale;

    // Facteur forme
    const shapeFactors = {
      Round: 1.0, Oval: 0.92, Pear: 0.90, Emerald: 0.88,
      Cushion: 0.89, Radiant: 0.86, Marquise: 0.90, Princess: 0.85, Asscher: 0.88
    };
    wholesale *= (shapeFactors[st.shape] || 0.90);

    // Facteur couleur
    if (st.colorMode === "fancy") {
      const fc = FANCY_COLORS.find(x => x.id === st.fancyColor) || FANCY_COLORS[0];
      const factor = isLab ? (1 + (fc.factor - 1) * 0.4) : fc.factor;
      wholesale *= factor;
    } else {
      const colorFactors = {
        "D": 1.25, "E": 1.15, "F": 1.05,
        "G": 0.96, "H": 0.88, "I": 0.78, "J": 0.70,
        "K-L": 0.60, "M-N": 0.52, "O-P": 0.45, "Q-R": 0.40, "S-Z": 0.35
      };
      wholesale *= (colorFactors[st.color] || 0.90);
    }

    // Facteur purete
    const clarityFactors = {
      "FL": 1.45, "IF": 1.30, "VVS1": 1.18, "VVS2": 1.08,
      "VS1": 0.98, "VS2": 0.88, "SI1": 0.75, "SI2": 0.65
    };
    wholesale *= (clarityFactors[st.clarity] || 0.95);

    // Facteur fluorescence
    if (st.fluorescence === "Faint") wholesale *= 0.97;
    if (st.fluorescence === "Medium") wholesale *= 0.92;

    // Application de la marge boutique Oneiro + frais fixes (180 EUR) + TVA francaise (20 %)
    const mult = getBoutiqueMultiplier(st.origin, carat);
    const retailHT = wholesale * mult + 180;
    const retailTTC = retailHT * 1.20;

    // Calcul de la fourchette indicative [-5 %, +8 %]
    const low = Math.round((retailTTC * 0.95) / 50) * 50;
    const high = Math.round((retailTTC * 1.08) / 50) * 50;
    return { low: Math.max(low, isLab ? 350 : 800), high: Math.max(high, isLab ? 450 : 950) };
  }

  const Configurator = {
    async mount(host, apiUrl) {
      this.host = host;
      this.api = apiUrl ? String(apiUrl).replace(/\/+$/, "") : null;
      this._token = 0;

      this.state = {
        origin: "natural",
        shape: "Round",
        carat: 1.00,
        colorMode: "white",
        color: "G",
        fancyColor: "Yellow",
        clarity: "VS1",
        cut: "Excellent",
        polish: "Excellent",
        symmetry: "Excellent",
        fluorescence: "None",
      };

      this.host.innerHTML = this.template();
      this.bind();
      this.refresh();
      return true;
    },

    template() {
      const st = this.state;
      return `
        <div class="cfg">
          <div class="cfg__controls">
            <!-- 1. Origine de la pierre -->
            <div class="opt">
              <label>${esc(T.originLabel)}</label>
              <div class="cfg__origins">
                <button type="button" class="cfg__origin-btn ${st.origin === "natural" ? "on" : ""}" data-origin="natural">
                  <span class="cfg__origin-title">${esc(T.naturalTitle)}</span>
                  <span class="cfg__origin-sub">${esc(T.naturalSub)}</span>
                </button>
                <button type="button" class="cfg__origin-btn ${st.origin === "lab" ? "on" : ""}" data-origin="lab">
                  <span class="cfg__origin-title">${esc(T.labTitle)}</span>
                  <span class="cfg__origin-sub">${esc(T.labSub)}</span>
                </button>
              </div>
            </div>

            <!-- 2. Forme de la pierre -->
            <div class="opt">
              <label>${esc(T.shape)}</label>
              <div class="cfg__shapes" id="cfg-shapes">
                ${SHAPES.map(s => `
                  <button type="button" class="cfg__shape-btn ${st.shape === s ? "on" : ""}" data-shape="${s}">
                    ${SHAPE_SVGS[s] || ""}
                    <span class="cfg__shape-name">${esc(T.shapes[s] || s)}</span>
                  </button>
                `).join("")}
              </div>
            </div>

            <!-- 3. Poids en carats -->
            <div class="opt">
              <label for="cfg-carat">${esc(T.carat)}</label>
              <div class="cfg__carat">
                <input id="cfg-carat" type="range" min="0.30" max="3.50" step="0.01" value="${st.carat}">
                <output id="cfg-carat-out">${st.carat.toFixed(2).replace(".", EN ? "." : ",")} ct</output>
              </div>
              <div class="opt__values cfg__magic" id="cfg-carat-quicks">
                ${CARAT_QUICKS.map(m => `
                  <button type="button" data-carat="${m}" class="${Math.abs(st.carat - m) < 0.005 ? "on" : ""}">
                    ${m.toFixed(2).replace(".", EN ? "." : ",")} ct
                  </button>
                `).join("")}
              </div>
            </div>

            <!-- 4. Couleur (D a Z) et Couleurs Fancy -->
            <div class="opt">
              <label>${esc(T.color)} <span style="text-transform:none;letter-spacing:0;color:var(--taupe);font-size:11px;margin-left:6px">(${esc(T.colorDesc)})</span></label>
              <div class="opt__values" id="cfg-colors">
                ${COLORS.map(c => `<button type="button" data-color="${c}" class="${st.colorMode === "white" && st.color === c ? "on" : ""}">${c}</button>`).join("")}
              </div>

              <!-- Section Couleurs Fancy -->
              <div class="cfg__fancy-group">
                <span class="cfg__fancy-label">${esc(T.fancyLabel)}</span>
                <div class="opt__values" id="cfg-fancy-colors">
                  ${FANCY_COLORS.map(fc => `
                    <button type="button" class="cfg__fancy-chip ${st.colorMode === "fancy" && st.fancyColor === fc.id ? "on" : ""}" data-fancy="${fc.id}">
                      <span class="cfg__fancy-dot" style="background:${fc.hex}"></span>
                      <span>${esc(EN ? fc.en : fc.fr)}</span>
                    </button>
                  `).join("")}
                </div>
              </div>
            </div>

            <!-- 5. Purete (FL a SI2) -->
            <div class="opt">
              <label>${esc(T.clarity)} <span style="text-transform:none;letter-spacing:0;color:var(--taupe);font-size:11px;margin-left:6px">(${esc(T.clarityDesc)})</span></label>
              <div class="opt__values" id="cfg-clarities">
                ${CLARITIES.map(cl => `<button type="button" data-clarity="${cl}" class="${st.clarity === cl ? "on" : ""}">${cl}</button>`).join("")}
              </div>
            </div>

            <!-- 6. Coupe (Cut) -->
            <div class="opt">
              <label>${esc(T.cut)}</label>
              <div class="opt__values">
                <button type="button" class="on" style="cursor:default">${esc(T.cuts.Excellent)}</button>
              </div>
              <p class="cfg__cut-notice">${esc(T.cutNotice)}</p>
            </div>

            <!-- 7. Criteres de certificat additionnels -->
            <div class="opt">
              <label>${esc(T.polishSym)}</label>
              <div class="opt__values" id="cfg-polish">
                <button type="button" data-pol="Excellent" class="${st.polish === "Excellent" ? "on" : ""}">Excellent</button>
                <button type="button" data-pol="VeryGood" class="${st.polish === "VeryGood" ? "on" : ""}">${esc(T.polishOpts.VeryGood)}</button>
              </div>
            </div>

            <div class="opt">
              <label>${esc(T.fluorescence)}</label>
              <div class="opt__values" id="cfg-fluo">
                <button type="button" data-fluo="None" class="${st.fluorescence === "None" ? "on" : ""}">${esc(T.fluoOpts.None)}</button>
                <button type="button" data-fluo="Faint" class="${st.fluorescence === "Faint" ? "on" : ""}">${esc(T.fluoOpts.Faint)}</button>
                <button type="button" data-fluo="Medium" class="${st.fluorescence === "Medium" ? "on" : ""}">${esc(T.fluoOpts.Medium)}</button>
              </div>
            </div>
          </div>

          <!-- Panneau Synthese & Fourchette Indicative -->
          <aside class="cfg__result">
            <!-- Scene 3D / Visuel holographique anime -->
            <div class="cfg__stage" id="cfg-stage">
              <div class="cfg__stage-hologram">
                <div class="cfg__stage-gem" id="cfg-stage-gem"></div>
                <div class="cfg__stage-glint"></div>
              </div>
              <span class="cfg__stage-tag" id="cfg-stage-tag">...</span>
            </div>

            <span class="kicker">${esc(T.summaryTitle)}</span>
            <div class="cfg__summary" id="cfg-summary"></div>

            <span class="kicker" style="margin-top:20px;display:block">${esc(T.estimateRange)}</span>
            <div class="cfg__price-range" id="cfg-range">...</div>
            <p class="cfg__price-sub">${esc(T.estimateSub)}</p>

            <div class="btn-row">
              <button type="button" class="btn btn--solid" id="cfg-cta-source">${esc(T.ctaSource)}</button>
              <a class="btn" href="${EN ? "book-appointment.html" : "rendez-vous.html"}">${esc(T.ctaVideo)}</a>
            </div>
          </aside>
        </div>
      `;
    },

    bind() {
      const host = this.host;

      // Origine
      host.querySelectorAll(".cfg__origin-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          this.state.origin = btn.dataset.origin;
          host.querySelectorAll(".cfg__origin-btn").forEach(b => b.classList.remove("on"));
          btn.classList.add("on");
          this.refresh();
        });
      });

      // Formes
      host.querySelectorAll(".cfg__shape-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          this.state.shape = btn.dataset.shape;
          host.querySelectorAll(".cfg__shape-btn").forEach(b => b.classList.remove("on"));
          btn.classList.add("on");
          this.refresh();
        });
      });

      // Carat slider & quick buttons
      const slider = host.querySelector("#cfg-carat");
      slider.addEventListener("input", () => {
        this.state.carat = parseFloat(slider.value);
        host.querySelector("#cfg-carat-out").textContent =
          this.state.carat.toFixed(2).replace(".", EN ? "." : ",") + " ct";
        host.querySelectorAll("#cfg-carat-quicks button").forEach(b => {
          b.classList.toggle("on", Math.abs(parseFloat(b.dataset.carat) - this.state.carat) < 0.005);
        });
        this.refresh();
      });

      host.querySelectorAll("#cfg-carat-quicks button").forEach(btn => {
        btn.addEventListener("click", () => {
          this.state.carat = parseFloat(btn.dataset.carat);
          slider.value = this.state.carat;
          host.querySelector("#cfg-carat-out").textContent =
            this.state.carat.toFixed(2).replace(".", EN ? "." : ",") + " ct";
          host.querySelectorAll("#cfg-carat-quicks button").forEach(b => b.classList.remove("on"));
          btn.classList.add("on");
          this.refresh();
        });
      });

      // Couleurs D a Z
      host.querySelectorAll("#cfg-colors button").forEach(btn => {
        btn.addEventListener("click", () => {
          this.state.colorMode = "white";
          this.state.color = btn.dataset.color;
          host.querySelectorAll("#cfg-colors button").forEach(b => b.classList.remove("on"));
          host.querySelectorAll("#cfg-fancy-colors button").forEach(b => b.classList.remove("on"));
          btn.classList.add("on");
          this.refresh();
        });
      });

      // Couleurs Fancy
      host.querySelectorAll("#cfg-fancy-colors button").forEach(btn => {
        btn.addEventListener("click", () => {
          this.state.colorMode = "fancy";
          this.state.fancyColor = btn.dataset.fancy;
          host.querySelectorAll("#cfg-colors button").forEach(b => b.classList.remove("on"));
          host.querySelectorAll("#cfg-fancy-colors button").forEach(b => b.classList.remove("on"));
          btn.classList.add("on");
          this.refresh();
        });
      });

      // Puretes
      host.querySelectorAll("#cfg-clarities button").forEach(btn => {
        btn.addEventListener("click", () => {
          this.state.clarity = btn.dataset.clarity;
          host.querySelectorAll("#cfg-clarities button").forEach(b => b.classList.remove("on"));
          btn.classList.add("on");
          this.refresh();
        });
      });

      // Poli
      host.querySelectorAll("#cfg-polish button").forEach(btn => {
        btn.addEventListener("click", () => {
          this.state.polish = btn.dataset.pol;
          this.state.symmetry = btn.dataset.pol;
          host.querySelectorAll("#cfg-polish button").forEach(b => b.classList.remove("on"));
          btn.classList.add("on");
          this.refresh();
        });
      });

      // Fluorescence
      host.querySelectorAll("#cfg-fluo button").forEach(btn => {
        btn.addEventListener("click", () => {
          this.state.fluorescence = btn.dataset.fluo;
          host.querySelectorAll("#cfg-fluo button").forEach(b => b.classList.remove("on"));
          btn.classList.add("on");
          this.refresh();
        });
      });

      // Bouton CTA -> Remplir formulaire devis avec upload et defiler
      host.querySelector("#cfg-cta-source").addEventListener("click", () => {
        this.fillDevisForm();
      });
    },

    refresh() {
      const st = this.state;
      const range = computeMarketRange(st);

      // Calcul libelle couleur et parametres visuels
      let colorLabel = "";
      let glowColor = "rgba(255, 255, 255, 0.45)";
      let stops = ["#ffffff", "#e0f2fe", "#bfdbfe"];

      if (st.colorMode === "fancy") {
        const fc = FANCY_COLORS.find(x => x.id === st.fancyColor) || FANCY_COLORS[0];
        colorLabel = EN ? `Fancy ${fc.en}` : `Fancy ${fc.fr}`;
        glowColor = fc.glow;
        stops = fc.stops;
      } else {
        colorLabel = st.color;
        if (["D", "E", "F"].includes(st.color)) {
          glowColor = "rgba(224, 242, 254, 0.6)";
          stops = ["#ffffff", "#f0f9ff", "#e0f2fe"];
        } else if (["G", "H", "I", "J"].includes(st.color)) {
          glowColor = "rgba(254, 240, 138, 0.35)";
          stops = ["#ffffff", "#fef9c3", "#fef08a"];
        } else {
          glowColor = "rgba(253, 224, 71, 0.45)";
          stops = ["#ffffff", "#fde047", "#eab308"];
        }
      }

      // Mise a jour du visuel 3D anime
      const stageGemEl = this.host.querySelector("#cfg-stage-gem");
      const stageTagEl = this.host.querySelector("#cfg-stage-tag");
      if (stageGemEl) {
        stageGemEl.style.setProperty("--gem-glow", glowColor);
        const gradId = `gem-grad-${Date.now()}`;
        const gradDef = `
          <svg style="position:absolute;width:0;height:0">
            <defs>
              <linearGradient id="${gradId}" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="${stops[0]}" stop-opacity="0.9"/>
                <stop offset="50%" stop-color="${stops[1]}" stop-opacity="0.75"/>
                <stop offset="100%" stop-color="${stops[2]}" stop-opacity="0.85"/>
              </linearGradient>
            </defs>
          </svg>`;
        stageGemEl.innerHTML = gradDef + buildFacetSvg(st.shape, gradId, "rgba(255,255,255,0.8)");
      }
      if (stageTagEl) {
        const shapeName = T.shapes[st.shape] || st.shape;
        stageTagEl.textContent = `${shapeName} \u2022 ${st.carat.toFixed(2)} ct \u2022 ${colorLabel}`;
      }

      // Rendu synthese
      const summaryEl = this.host.querySelector("#cfg-summary");
      if (summaryEl) {
        summaryEl.innerHTML = `
          <div class="cfg__summary-item"><span>${esc(T.shape)} :</span> <strong>${esc(T.shapes[st.shape] || st.shape)}</strong></div>
          <div class="cfg__summary-item"><span>${esc(T.carat)} :</span> <strong>${st.carat.toFixed(2)} ct</strong></div>
          <div class="cfg__summary-item"><span>${esc(T.color)} :</span> <strong>${esc(colorLabel)}</strong></div>
          <div class="cfg__summary-item"><span>${esc(T.clarity)} :</span> <strong>${st.clarity}</strong></div>
          <div class="cfg__summary-item"><span>${esc(T.cut)} :</span> <strong>Excellent</strong></div>
          <div class="cfg__summary-item"><span>${esc(T.originLabel)} :</span> <strong>${st.origin === "lab" ? esc(T.labTitle) : esc(T.naturalTitle)}</strong></div>
          <div class="cfg__summary-item"><span>${esc(T.certificate)} :</span> <strong>GIA, IGI ou HRD</strong></div>
        `;
      }

      // Rendu fourchette indicative
      const rangeEl = this.host.querySelector("#cfg-range");
      if (rangeEl) {
        rangeEl.textContent = `${fmtMoney(range.low)} - ${fmtMoney(range.high)}`;
      }
    },

    fillDevisForm() {
      const st = this.state;
      const devisSection = document.getElementById("devis");
      if (!devisSection) return;

      const fForme = document.getElementById("d-forme");
      const fType = document.getElementById("d-type");
      const fNotes = document.getElementById("d-notes");
      const fCouleur = document.getElementById("d-couleur");

      if (fForme) {
        const shapeName = T.shapes[st.shape] || st.shape;
        for (let i = 0; i < fForme.options.length; i++) {
          if (fForme.options[i].text.toLowerCase().includes(shapeName.toLowerCase())) {
            fForme.selectedIndex = i;
            break;
          }
        }
      }

      if (fType) {
        fType.selectedIndex = st.origin === "lab" ? 1 : 0;
      }

      let colorLabel = st.color;
      if (st.colorMode === "fancy") {
        const fc = FANCY_COLORS.find(x => x.id === st.fancyColor) || FANCY_COLORS[0];
        colorLabel = EN ? `Fancy ${fc.en}` : `Fancy ${fc.fr}`;
      }

      if (fCouleur) {
        fCouleur.value = `${colorLabel} (${st.clarity}, taille Excellent)`;
      }

      if (fNotes) {
        const specSummary = (EN ? "Configured stone: " : "Pierre configur\u00e9e : ") +
          `${T.shapes[st.shape] || st.shape} ${st.carat.toFixed(2)}ct, couleur ${colorLabel}, puret\u00e9 ${st.clarity}, cut Excellent, sym\u00e9trie/poli ${st.polish}, fluorescence ${st.fluorescence}.`;
        if (!fNotes.value.includes(st.shape)) {
          fNotes.value = specSummary + "\n" + fNotes.value;
        }
      }

      devisSection.scrollIntoView({ behavior: "smooth" });
    }
  };

  window.OneiroConfigurator = Configurator;
})();
