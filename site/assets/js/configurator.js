// ============================================================
// ONEIRO PARIS — Configurateur de diamant
// ------------------------------------------------------------
// Le visiteur compose une pierre, le modele estime le prix.
//
// Trois principes de conception.
//
//  1. Il ne casse jamais la page. Si l'API ne repond pas, si le modele
//     n'est pas charge, si le reseau tombe : on retire le widget et on
//     retombe sur le contenu de repli. Un configurateur en panne est pire
//     que pas de configurateur.
//  2. Les echelles viennent de l'API, pas d'ici. Le jour ou le modele
//     apprend une forme de plus, elle apparait sans toucher a ce fichier.
//  3. Il montre ce que chaque arbitrage coute. C'est la ligne editoriale de
//     la maison rendue interactive : on explique comment depenser moins,
//     y compris quand ca nous fait vendre moins cher.
// ============================================================

(function () {
  const EN = (document.documentElement.getAttribute("lang") || "fr")
    .slice(0, 2).toLowerCase() === "en";

  const T = EN ? {
    origin: "Stone", natural: "Natural", lab: "Lab-grown",
    shape: "Shape", carat: "Carat weight", color: "Colour",
    clarity: "Clarity", cut: "Cut",
    estimate: "Estimated price", levers: "What each choice changes",
    leverHint: "Click a line to apply it.",
    cta: "Ask us to source this stone",
    ctaAlt: "Discuss it by video",
    demo: "Demonstration mode: the model is trained on test data, these prices are fictional.",
    reference: "Indicative levels, based on wholesale prices restated to today's index. A firm price is confirmed by quotation.",
    outOfRange: "This configuration is outside what the model has learned. Ask us directly.",
    loading: "Calculating…",
    error: "The estimator is unavailable at the moment.",
    mailSubject: "Diamond search — configuration",
    shapes: {
      Round: "Round", Oval: "Oval", Pear: "Pear", Emerald: "Emerald",
      Cushion: "Cushion", Princess: "Princess", Marquise: "Marquise",
      Radiant: "Radiant", Asscher: "Asscher", Heart: "Heart", Other: "Other",
    },
    cuts: { Excellent: "Excellent", "Very Good": "Very good", Good: "Good" },
  } : {
    origin: "La pierre", natural: "Naturel", lab: "Laboratoire",
    shape: "Forme", carat: "Poids en carats", color: "Couleur",
    clarity: "Pureté", cut: "Taille",
    estimate: "Prix estimé", levers: "Ce que chaque choix change",
    leverHint: "Cliquez une ligne pour l'appliquer.",
    cta: "Nous demander de sourcer cette pierre",
    ctaAlt: "En parler en visio",
    demo: "Mode démonstration : le modèle est entraîné sur des données de test, ces prix sont fictifs.",
    reference: "Ordres de grandeur, établis sur des prix de gros recalés sur l'indice du jour. Le prix ferme est confirmé par devis.",
    outOfRange: "Cette configuration sort de ce que le modèle a appris. Demandez-nous directement.",
    loading: "Calcul en cours…",
    error: "L'estimateur est indisponible pour le moment.",
    mailSubject: "Recherche de diamant — configuration",
    shapes: {
      Round: "Rond", Oval: "Ovale", Pear: "Poire", Emerald: "Émeraude",
      Cushion: "Coussin", Princess: "Princesse", Marquise: "Marquise",
      Radiant: "Radiant", Asscher: "Asscher", Heart: "Cœur", Other: "Autre",
    },
    cuts: { Excellent: "Excellent", "Very Good": "Très bon", Good: "Bon" },
  };

  const MAGIC = [0.30, 0.50, 0.70, 0.90, 1.00, 1.50, 2.00, 3.00];

  // La devise vient de l'API, pas d'une constante : le modele peut avoir
  // appris sur des prix en dollars, et afficher des dollars sous un symbole
  // euro serait une erreur silencieuse de l'ordre de 15 %.
  let DEVISE = "EUR";
  const money = n => (DEVISE === "EUR" && typeof O !== "undefined" && O.fmt)
    ? O.fmt(n)
    : new Intl.NumberFormat(EN ? "en-GB" : "fr-FR",
        { style: "currency", currency: DEVISE, maximumFractionDigits: 0 }).format(n);

  const signed = n => (n > 0 ? "+" : "−") + money(Math.abs(n)).replace(/^[-−]/, "");

  function esc(value) {
    return String(value).replace(/[<>&"]/g,
      c => ({ "<": "&lt;", ">": "&gt;", "&": "&amp;", '"': "&quot;" }[c]));
  }

  // ---------------------------------------------------------------
  const Configurator = {
    async mount(host, apiUrl) {
      this.api = String(apiUrl).replace(/\/+$/, "");
      this.host = host;
      // Compteur de requetes : garantit qu'une reponse lente arrivee apres
      // une plus recente ne vient pas ecraser l'affichage. Doit partir de 0,
      // sinon ++undefined vaut NaN et NaN !== NaN rejette toutes les reponses.
      this._token = 0;

      let options;
      try {
        const response = await fetch(this.api + "/options", { mode: "cors" });
        if (!response.ok) throw new Error("options " + response.status);
        options = await response.json();
      } catch (err) {
        console.warn("[configurateur] indisponible :", err.message);
        return false;                       // le repli de la page prend la main
      }

      this.options = options;
      if (options.devise) DEVISE = options.devise;
      this.state = {
        origin: options.origins.includes("natural") ? "natural" : options.origins[0],
        shape: options.shapes.includes("Round") ? "Round" : options.shapes[0],
        carat: 1.00,
        color: options.colors.includes("G") ? "G" : options.colors[0],
        clarity: options.clarities.includes("VS1") ? "VS1" : options.clarities[0],
        cut: "Excellent",
      };
      host.innerHTML = this.template();
      this.bind();
      this.refresh();
      return true;
    },

    template() {
      const o = this.options;
      const pills = (key, values, label) => `
        <div class="opt">
          <label>${esc(label)}</label>
          <div class="opt__values" data-cfg="${key}">
            ${values.map(v => `<button type="button" data-v="${esc(v.value)}"
              class="${this.state[key] === v.value ? "on" : ""}">${esc(v.label)}</button>`).join("")}
          </div>
        </div>`;

      return `
      ${o.demo ? `<p class="cfg__demo">${esc(T.demo)}</p>` : ""}
      ${(!o.demo && o.etat === "reference")
          ? `<p class="cfg__reference">${esc(T.reference)}</p>` : ""}
      <div class="cfg">
        <div class="cfg__controls">
          ${o.origins.length > 1
            ? pills("origin", o.origins.map(v => ({ value: v, label: v === "lab" ? T.lab : T.natural })), T.origin)
            : ""}
          ${pills("shape", o.shapes.map(v => ({ value: v, label: T.shapes[v] || v })), T.shape)}

          <div class="opt">
            <label for="cfg-carat">${esc(T.carat)}</label>
            <div class="cfg__carat">
              <input id="cfg-carat" type="range" min="${o.carat_min}" max="${Math.min(o.carat_max, 5)}"
                     step="0.01" value="${this.state.carat}">
              <output id="cfg-carat-out">${this.state.carat.toFixed(2).replace(".", EN ? "." : ",")} ct</output>
            </div>
            <div class="opt__values cfg__magic" data-cfg="carat">
              ${MAGIC.filter(m => m >= o.carat_min && m <= o.carat_max)
                .map(m => `<button type="button" data-v="${m}"
                  class="${Math.abs(this.state.carat - m) < 0.005 ? "on" : ""}">${m.toFixed(2).replace(".", EN ? "." : ",")}</button>`).join("")}
            </div>
          </div>

          ${pills("color", o.colors.map(v => ({ value: v, label: v })), T.color)}
          ${pills("clarity", o.clarities.map(v => ({ value: v, label: v })), T.clarity)}
          ${pills("cut", o.cuts.map(v => ({ value: v, label: T.cuts[v] || v })), T.cut)}
        </div>

        <aside class="cfg__result">
          <span class="kicker">${esc(T.estimate)}</span>
          <div class="cfg__price" id="cfg-price">${esc(T.loading)}</div>
          <p class="cfg__mention" id="cfg-mention"></p>
          <div class="cfg__levers" id="cfg-levers"></div>
          <div class="btn-row">
            <a class="btn btn--solid" id="cfg-cta" href="#">${esc(T.cta)}</a>
          </div>
        </aside>
      </div>`;
    },

    bind() {
      const host = this.host;

      host.querySelectorAll(".opt__values").forEach(group => {
        group.addEventListener("click", event => {
          const button = event.target.closest("button[data-v]");
          if (!button) return;
          const key = group.dataset.cfg;
          this.state[key] = key === "carat" ? parseFloat(button.dataset.v) : button.dataset.v;
          if (key === "carat") this.syncCarat();
          group.querySelectorAll("button").forEach(b => b.classList.remove("on"));
          button.classList.add("on");
          this.refresh();
        });
      });

      const slider = host.querySelector("#cfg-carat");
      slider.addEventListener("input", () => {
        this.state.carat = parseFloat(slider.value);
        this.syncCarat(false);
        this.refresh();
      });

      // Les arbitrages sont cliquables : on applique la variante proposee.
      host.querySelector("#cfg-levers").addEventListener("click", event => {
        const row = event.target.closest("[data-change]");
        if (!row) return;
        Object.assign(this.state, JSON.parse(row.dataset.change));
        this.syncAll();
        this.refresh();
      });
    },

    syncCarat(moveSlider = true) {
      const value = this.state.carat;
      this.host.querySelector("#cfg-carat-out").textContent =
        value.toFixed(2).replace(".", EN ? "." : ",") + " ct";
      if (moveSlider) this.host.querySelector("#cfg-carat").value = value;
      this.host.querySelectorAll('.cfg__magic button').forEach(b => {
        b.classList.toggle("on", Math.abs(parseFloat(b.dataset.v) - value) < 0.005);
      });
    },

    syncAll() {
      this.host.querySelectorAll(".opt__values").forEach(group => {
        const key = group.dataset.cfg;
        if (key === "carat") return;
        group.querySelectorAll("button").forEach(b => {
          b.classList.toggle("on", b.dataset.v === String(this.state[key]));
        });
      });
      this.syncCarat();
    },

    refresh() {
      clearTimeout(this._timer);
      this._timer = setTimeout(() => this.fetchQuote(), 220);
    },

    async fetchQuote() {
      const token = ++this._token;
      const body = { ...this.state, polish: this.state.cut, symmetry: this.state.cut };
      let data;
      try {
        const response = await fetch(`${this.api}/compare?lang=${EN ? "en" : "fr"}`, {
          method: "POST", mode: "cors",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(body),
        });
        if (!response.ok) throw new Error("compare " + response.status);
        data = await response.json();
      } catch (err) {
        if (token === this._token) this.renderError();
        return;
      }
      if (token !== this._token) return;    // une reponse plus recente est arrivee
      this.render(data);
    },

    render(data) {
      const base = data.base;
      const price = this.host.querySelector("#cfg-price");
      const mention = this.host.querySelector("#cfg-mention");
      const levers = this.host.querySelector("#cfg-levers");

      if (!base.fiable) {
        price.textContent = "—";
        mention.textContent = T.outOfRange;
        levers.innerHTML = "";
      } else {
        price.textContent = money(base.prix);
        mention.textContent = base.mention;
        levers.innerHTML = data.variantes.length ? `
          <span class="cfg__levers-title">${esc(T.levers)}</span>
          ${data.variantes.map(v => `
            <button type="button" class="cfg__lever" data-change='${esc(JSON.stringify(v.changement))}'>
              <span>${esc(v.libelle)}</span>
              <b class="${v.delta < 0 ? "down" : "up"}">${signed(v.delta)}</b>
            </button>`).join("")}
          <span class="cfg__levers-hint">${esc(T.leverHint)}</span>` : "";
      }

      const cta = this.host.querySelector("#cfg-cta");
      const spec = [
        `${EN ? "Shape" : "Forme"} : ${T.shapes[this.state.shape] || this.state.shape}`,
        `${EN ? "Weight" : "Poids"} : ${this.state.carat.toFixed(2)} ct`,
        `${EN ? "Colour" : "Couleur"} : ${this.state.color}`,
        `${EN ? "Clarity" : "Pureté"} : ${this.state.clarity}`,
        `${EN ? "Cut" : "Taille"} : ${this.state.cut}`,
        `${EN ? "Type" : "Type"} : ${this.state.origin === "lab" ? T.lab : T.natural}`,
      ].join("\n- ");
      const body = (EN
        ? "Hello,\n\nI configured this stone on your website:\n\n- "
        : "Bonjour,\n\nJ'ai configuré cette pierre sur votre site :\n\n- ")
        + spec
        + (base.fiable ? `\n\n${EN ? "Estimate shown" : "Estimation affichée"} : ${money(base.prix)}` : "")
        + (EN ? "\n\nCould you tell me what is actually available and at what price?\n"
              : "\n\nPourriez-vous me dire ce qui est réellement disponible, et à quel prix ?\n");
      cta.href = (typeof O !== "undefined" && O.mailto)
        ? O.mailto(T.mailSubject, body)
        : "mailto:?subject=" + encodeURIComponent(T.mailSubject) + "&body=" + encodeURIComponent(body);
    },

    renderError() {
      const price = this.host.querySelector("#cfg-price");
      if (price) price.textContent = "—";
      const mention = this.host.querySelector("#cfg-mention");
      if (mention) mention.textContent = T.error;
    },
  };

  window.OneiroConfigurator = Configurator;
})();
