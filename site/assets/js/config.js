// ============================================================
// ONEIRO PARIS — Configuration centrale
// C'est LE fichier à éditer quand vous branchez un service.
// Tant qu'un service est "enabled: false", le site affiche
// automatiquement une alternative propre (formulaire, email…).
// ============================================================

const ONEIRO_CONFIG = {

  // --- Coordonnées ---------------------------------------------------------
  // TODO: créer l'adresse pro (ex. via Cloudflare Email Routing -> redirection
  // vers votre Gmail), puis remplacer ici. Ne plus exposer le Gmail public.
  contactEmail: "contact@oneiroparis.com",

  // TODO: numéro WhatsApp Business au format international, sans + ni espaces.
  // Ex: "33612345678". Laisser vide pour masquer les boutons WhatsApp.
  whatsappNumber: "",

  instagramUrl: "https://www.instagram.com/oneiro_paris",

  // --- Société (mentions légales / footer) ---------------------------------
  company: {
    name: "ONEIRO, SAS",
    siret: "94136575100010",
    address: "3 rue de la Faisanderie, 75016 Paris",
  },

  // --- Shopify (achat en ligne) — NON CONNECTÉ pour l'instant ---------------
  // Quand votre boutique Shopify sera prête :
  //   1. passer enabled à true
  //   2. renseigner domain (ex: "oneiroparis.myshopify.com" ou le domaine final)
  // Les boutons « Acheter » des fiches produit redirigeront alors vers
  // https://<domain>/products/<handle> (la fiche Shopify avec panier/paiement).
  shopify: {
    enabled: false,
    domain: "",
  },

  // --- Configurateur de diamant (modèle de prix Oneiro) ---------------------
  // Estimateur maison : le visiteur compose une pierre, l'API du home server
  // renvoie une estimation. Voir pricing/ pour le modèle et son déploiement.
  //   1. déployer l'API (pricing/deploy), vérifier https://<url>/health
  //   2. passer enabled à true et renseigner apiUrl
  // Tant que c'est désactivé, la page Diamants affiche le contenu de repli.
  // ATTENTION : tant que le modèle est entraîné sur des données de test,
  // l'API renvoie demo=true et le configurateur affiche un bandeau qui le dit.
  // Ne pas mettre en ligne sans un modèle entraîné sur des données réelles.
  pricer: {
    // BRANCHE POUR TESTS le 23/09/2026. Le configurateur affiche des
    // ordres de grandeur en DOLLARS, naturel uniquement, avec la mention
    // qui le dit. Pour le couper : enabled a false, puis rebuild.
    enabled: true,
    apiUrl: "https://api-diamant.arinaudo.fr",
  },

  // --- Nivoda (sélecteur de diamants) — emplacement prêt --------------------
  // Quand votre compte/widget Nivoda sera opérationnel :
  //   1. passer enabled à true
  //   2. renseigner embedUrl avec l'URL d'embed fournie par Nivoda
  // L'iframe s'affichera sur la page Diamants à la place du formulaire devis.
  nivoda: {
    enabled: false,
    embedUrl: "",
  },

  // --- Prise de rendez-vous : vos disponibilités -----------------------------
  // Le widget de la page Rendez-vous génère les créneaux à partir d'ici.
  // availability : jours de la semaine (0=dimanche, 1=lundi ... 6=samedi),
  // chacun avec une ou plusieurs plages ["début", "fin"].
  // Le client choisit son créneau ; vous recevez la demande par email
  // et confirmez. Ajoutez vos absences dans exceptions ("AAAA-MM-JJ").
  booking: {
    enabled: true,
    slotMinutes: 30,   // durée d'un rendez-vous
    weeksAhead: 3,     // nombre de semaines de créneaux proposés
    leadHours: 24,     // délai minimum avant le premier créneau
    availability: {
      2: [["18:00", "20:00"]],   // mardi
      4: [["18:00", "20:00"]],   // jeudi
      6: [["10:00", "13:00"]],   // samedi
    },
    exceptions: [],    // ex. ["2026-08-15", "2026-08-22"]
  },

  // --- Réservation en ligne (Calendly, Cal.com ou équivalent) ---------------
  // Les visiteurs choisissent un créneau directement, sans envoyer d'email.
  // Marche à suivre :
  //   1. créer un compte gratuit sur calendly.com ou cal.com
  //   2. définir un événement "Rendez-vous conseil" de 30 min, brancher Google
  //      Agenda (les créneaux déjà pris disparaissent tout seuls) et activer
  //      la visio (Google Meet) dans l'événement
  //   3. coller ici l'adresse publique de l'événement, par exemple
  //        "https://calendly.com/oneiroparis/conseil-30min"
  //        "https://cal.com/oneiroparis/conseil-30min"
  //   4. relancer le build : python site/_build/build.py
  // Tant que url est vide, le site garde le widget de créneaux ci-dessous
  // (booking), qui, lui, passe encore par un email pré-rempli.
  calendly: {
    enabled: true,
    url: "",
  },

  // --- Vidéos de l'atelier ---------------------------------------------------
  // 1 à 3 vidéos affichées sur la page À propos (section « L'atelier en images »).
  // Deux formats acceptés :
  //   { type: "file", src: "assets/video/atelier-1.mp4", poster: "assets/video/atelier-1.jpg", title: "Le sertissage" }
  //     -> déposez le fichier .mp4 (et une image d'aperçu .jpg optionnelle) dans site/assets/video/
  //   { type: "youtube", id: "dQw4w9WgXcQ", title: "La fonte de l'or" }
  //     -> id = ce qui suit "watch?v=" dans l'URL YouTube
  // La section n'apparaît que si la liste n'est pas vide.
  atelierVideos: [],

  // --- Avis clients ----------------------------------------------------------
  // Alimente la section avis de l'accueil ET la page Avis (avis.html).
  // Champs : rating (1-5), text, author, context (pièce concernée), date (AAAA-MM-JJ),
  //          source ("Google", "Trustpilot"… facultatif), photo (URL facultative).
  // Exemple :
  // reviews: [
  //   { rating: 5, text: "Accompagnement remarquable du premier appel a la livraison.",
  //     author: "Camille D.", context: "Bague de fiancailles sur-mesure",
  //     date: "2026-05-14", source: "Google" },
  // ],
  // IMPORTANT : n'y mettez que de vrais avis recus. Les etoiles affichees dans
  // Google (donnees structurees) doivent correspondre a des avis authentiques.
  reviews: [],

  // Lien public vers votre fiche d'avis (Google Business, Trustpilot...).
  // Sert au bouton "Deposer un avis" de la page Avis. Vide = formulaire email.
  reviewUrl: "",
};
