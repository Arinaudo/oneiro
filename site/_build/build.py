#!/usr/bin/env python3
# Assemble le site bilingue : FR a la racine, EN sous /en/.
# Pages racine, articles du Journal (journal/), pages produit (produits/ | products/),
# + canonical, hreflang, JSON-LD (Organization, Product, Article), sitemap.xml et robots.txt.
# Usage : python3 build.py
# Si vous modifiez assets/js/products-data.js et que Node est installe, products.json
# est regenere automatiquement ; sinon le cache _build/products.json est utilise.
# Les traductions anglaises des fiches produit vivent dans _build/products-en.json.
import os, json, html, re, subprocess, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.dirname(ROOT)

# Domaine canonique du futur site — a ajuster si vous choisissez un autre domaine.
# Surchargeable sans toucher au code :
#   ONEIRO_SITE_URL=https://mon-domaine.fr python3 build.py
SITE_URL = os.environ.get("ONEIRO_SITE_URL", "https://oneiroparis.com").rstrip("/")
TODAY = datetime.date.today().isoformat()

# ============================================================================
# 1. Pages : cle logique -> slug FR, slug EN, titre/description par langue
# ============================================================================

# cle : (slug_fr, slug_en)
SLUGS = {
    "index": ("index", "index"),
    "sur-mesure": ("sur-mesure", "custom-made"),
    "bague-de-fiancailles": ("bague-de-fiancailles", "engagement-rings"),
    "alliance": ("alliance", "wedding-bands"),
    "collection": ("collection", "collection"),
    "produit": ("produit", "product"),
    "diamants": ("diamants", "diamonds"),
    "journal": ("journal", "journal"),
    "a-propos": ("a-propos", "about"),
    "garanties": ("garanties", "guarantees"),
    "avis": ("avis", "reviews"),
    "selection": ("selection", "wishlist"),
    "rendez-vous": ("rendez-vous", "book-appointment"),
    "contact": ("contact", "contact"),
    "404": ("404", "404"),
    "mentions-legales": ("mentions-legales", "legal-notice"),
    "cgv": ("cgv", "terms"),
    "confidentialite": ("confidentialite", "privacy"),
}

META = {
    "fr": {
        "index": (
            "Joaillerie sur-mesure & diamants certifiés | Oneiro Paris",
            "Bagues de fiançailles et joaillerie sur-mesure en or 18 carats, diamants naturels ou de laboratoire certifiés. Maison parisienne 100 % en ligne : prix d'atelier, accompagnement personnel de l'idée à la livraison.",
        ),
        "sur-mesure": (
            "Bijoux sur-mesure : bague, alliance, pièce unique | Oneiro",
            "Créez votre bijou sur-mesure avec un conseiller dédié : choix du diamant, design 3D, fabrication française en or 18 carats. De 1 000 à 7 000 €, délai 2 à 7 semaines.",
        ),
        "bague-de-fiancailles": (
            "Bague de fiançailles sur-mesure & éthique | Oneiro Paris",
            "Créez sa bague de fiançailles sur-mesure : diamant certifié GIA/IGI naturel ou de laboratoire, or 18 carats, fabrication française. De 1 000 à 7 000 €, conseil visio offert, validation 3D avant fabrication.",
        ),
        "alliance": (
            "Alliance sur-mesure en or 18 carats | Oneiro Paris",
            "Alliances de mariage sur-mesure : or 18 carats jaune, blanc ou rose, diamants certifiés, gravure offerte. Accordées à votre bague de fiançailles, façonnées en France. Devis gratuit sous 48 h.",
        ),
        "collection": (
            "Collection : bagues, colliers, boucles | Oneiro Paris",
            "La collection signature Oneiro Paris : créations en or 18 carats serties de diamants naturels ou de laboratoire certifiés. Chaque pièce est personnalisable.",
        ),
        "produit": (
            "Création Oneiro Paris",
            "Création en or 18 carats et diamants certifiés — Oneiro Paris, joaillerie sur-mesure en ligne.",
        ),
        "diamants": (
            "Diamants certifiés GIA/IGI au prix direct | Oneiro Paris",
            "Diamants naturels et de laboratoire, certifiés GIA/IGI, au prix direct négociant. Choisissez forme, carat, couleur et pureté — avec un expert pour vous guider.",
        ),
        "journal": (
            "Le Journal : actualités & guides joaillerie | Oneiro Paris",
            "Deux sections : l'actualité des prix, des tendances et du calendrier, et des guides intemporels sur les diamants, les formes, les tailles et les coutumes. Par la maison Oneiro.",
        ),
        "a-propos": (
            "À propos — la maison Oneiro | Oneiro Paris",
            "Oneiro est une jeune maison de joaillerie parisienne, 100 % en ligne par choix : ce que nous ne dépensons pas en vitrine, nous l'investissons dans l'or, les pierres et le temps passé avec vous.",
        ),
        "garanties": (
            "Garanties, livraison & retours | Oneiro Paris",
            "Livraison offerte et suivie, retours sous 15 jours sur la joaillerie fine, garantie fabrication, certificats GIA/IGI, paiement sécurisé et en 3 fois. Tout ce qui protège votre achat.",
        ),
        "avis": (
            "Avis clients vérifiés | Oneiro Paris",
            "Les avis authentiques des clients Oneiro Paris : accompagnement, qualité des pierres, délais et finition. Publiés tels quels, après réception de la pièce.",
        ),
        "selection": (
            "Ma sélection | Oneiro Paris",
            "Les créations Oneiro Paris que vous avez retenues — à comparer, à garder sous la main ou à partager par un simple lien.",
        ),
        "rendez-vous": (
            "Rendez-vous conseil : en visio ou à Paris | Oneiro Paris",
            "30 minutes avec un conseiller Oneiro, en visio ou en personne à Paris : votre projet, votre budget, les bonnes questions à se poser. Gratuit et sans engagement.",
        ),
        "contact": (
            "Contact | Oneiro Paris",
            "Une question, un projet sur-mesure ? Écrivez-nous — réponse sous 24 h ouvrées.",
        ),
        "404": (
            "Page introuvable | Oneiro Paris",
            "Cette page n'existe pas ou plus. Retrouvez la collection, le sur-mesure et les guides diamants d'Oneiro Paris.",
        ),
        "mentions-legales": ("Mentions légales | Oneiro Paris", "Mentions légales du site Oneiro Paris — ONEIRO SAS, Paris."),
        "cgv": ("Conditions générales de vente | Oneiro Paris", "Conditions générales de vente d'Oneiro Paris : prix, paiement, livraison, retours, garanties."),
        "confidentialite": ("Politique de confidentialité | Oneiro Paris", "Politique de confidentialité et données personnelles — Oneiro Paris."),
    },
    "en": {
        "index": (
            "Bespoke fine jewellery & certified diamonds | Oneiro Paris",
            "Engagement rings and bespoke fine jewellery in 18 carat gold, set with certified natural or lab-grown diamonds. A Parisian house, entirely online: workshop prices, personal guidance from the idea to the delivery.",
        ),
        "sur-mesure": (
            "Bespoke jewellery: rings, wedding bands, one-off pieces | Oneiro",
            "Create your bespoke piece with a dedicated adviser: choice of diamond, 3D design, French craftsmanship in 18 carat gold. From €1,000 to €7,000, ready in 2 to 7 weeks.",
        ),
        "bague-de-fiancailles": (
            "Bespoke & ethical engagement rings | Oneiro Paris",
            "Create a bespoke engagement ring: GIA/IGI certified natural or lab-grown diamond, 18 carat gold, made in France. From €1,000 to €7,000, free video advice, 3D sign-off before production.",
        ),
        "alliance": (
            "Bespoke wedding bands in 18 carat gold | Oneiro Paris",
            "Bespoke wedding bands: 18 carat yellow, white or rose gold, certified diamonds, engraving included. Matched to your engagement ring, made in France. Free quote within 48 hours.",
        ),
        "collection": (
            "Collection: rings, necklaces, earrings | Oneiro Paris",
            "The Oneiro Paris signature collection: creations in 18 carat gold set with certified natural or lab-grown diamonds. Every piece can be personalised.",
        ),
        "produit": (
            "An Oneiro Paris creation",
            "A creation in 18 carat gold set with certified diamonds — Oneiro Paris, bespoke fine jewellery online.",
        ),
        "diamants": (
            "GIA/IGI certified diamonds at direct prices | Oneiro Paris",
            "Natural and lab-grown diamonds, GIA/IGI certified, at direct dealer prices. Choose the shape, carat, colour and clarity — with an expert to guide you.",
        ),
        "journal": (
            "The Journal: jewellery news & guides | Oneiro Paris",
            "Two sections: news on prices, trends and timing, and timeless guides to diamonds, shapes, sizes and customs. By the Oneiro house.",
        ),
        "a-propos": (
            "About — the Oneiro house | Oneiro Paris",
            "Oneiro is a young Parisian jewellery house, entirely online by choice: what we do not spend on a shop window, we invest in the gold, the stones and the time we spend with you.",
        ),
        "garanties": (
            "Guarantees, delivery & returns | Oneiro Paris",
            "Free tracked delivery, 15 day returns on fine jewellery, manufacturing warranty, GIA/IGI certificates, secure payment and payment in 3. Everything that protects your purchase.",
        ),
        "avis": (
            "Verified client reviews | Oneiro Paris",
            "Authentic reviews from Oneiro Paris clients: guidance, quality of the stones, timing and finish. Published as written, after the piece has been received.",
        ),
        "selection": (
            "My selection | Oneiro Paris",
            "The Oneiro Paris creations you have kept — to compare, to keep to hand or to share through a single link.",
        ),
        "rendez-vous": (
            "Book an appointment: by video or in Paris | Oneiro Paris",
            "30 minutes with an Oneiro adviser, by video or in person in Paris: your project, your budget, the right questions to ask. Free and with no obligation.",
        ),
        "contact": (
            "Contact | Oneiro Paris",
            "A question, a bespoke project? Write to us — an answer within 24 working hours.",
        ),
        "404": (
            "Page not found | Oneiro Paris",
            "This page does not exist, or no longer does. Find the collection, bespoke creations and the diamond guides of Oneiro Paris.",
        ),
        "mentions-legales": ("Legal notice | Oneiro Paris", "Legal notice for the Oneiro Paris website — ONEIRO SAS, Paris."),
        "cgv": ("Terms and conditions of sale | Oneiro Paris", "Oneiro Paris terms and conditions of sale: prices, payment, delivery, returns, warranties."),
        "confidentialite": ("Privacy policy | Oneiro Paris", "Privacy policy and personal data — Oneiro Paris."),
    },
}

# Le Journal (articles, sections, pieces recommandees) vit dans son propre
# fichier pour rester lisible : _build/_articles_registry.py
import sys as _sys, importlib.util as _ilu
_sys.dont_write_bytecode = True   # pas de dossier __pycache__ dans _build/
_spec = _ilu.spec_from_file_location("_articles_registry", os.path.join(ROOT, "_articles_registry.py"))
_reg = _ilu.module_from_spec(_spec)
_spec.loader.exec_module(_reg)
ARTICLES = _reg.ARTICLES
JOURNAL_SECTIONS = _reg.JOURNAL_SECTIONS

# Ordre d'affichage : le plus recent d'abord, dans chaque section
def articles_in(section):
    return sorted([k for k, a in ARTICLES.items() if a["section"] == section],
                  key=lambda k: ARTICLES[k]["date"], reverse=True)

# ============================================================================
# 2. Chaines d'interface (header, footer) par langue
# ============================================================================

CHROME = {
    "fr": {
        "TOPBAR": "Maison de joaillerie 100&nbsp;% en ligne — livraison offerte, en France et à l'international",
        "L_HOME": "Accueil", "L_NAV": "Navigation principale", "L_MENU": "Menu",
        "L_SURMESURE": "Sur-Mesure", "L_COLLECTION": "Collection", "L_DIAMANTS": "Diamants",
        "L_JOURNAL": "Journal", "L_APROPOS": "À propos", "L_AVIS": "Avis",
        "L_GARANTIES": "Garanties", "L_CONTACT": "Contact",
        "L_SELECTION": "Ma sélection", "L_RDV": "Prendre rendez-vous",
        "L_WA_MSG": "Bonjour, j'ai une question sur une création Oneiro.",
        "L_WA_ARIA": "Nous écrire sur WhatsApp",
        "F_BASELINE": "Joaillerie sur-mesure en or 18 carats et diamants certifiés, dessinée à Paris et façonnée en France. Sans boutique — et c'est un choix.",
        "F_WIRE": "Virement",
        "F_H_MAISON": "La Maison", "F_H_AIDE": "Aide &amp; garanties", "F_H_CONTACT": "Contact",
        "F_SURMESURE": "Le sur-mesure", "F_FIANCAILLES": "Bague de fiançailles", "F_ALLIANCE": "Alliance",
        "F_COLLECTION": "La collection", "F_DIAMANTS": "Oneiro Diamants", "F_JOURNAL": "Le Journal",
        "F_APROPOS": "À propos", "F_SELECTION": "Ma sélection", "F_RDV": "Prendre rendez-vous",
        "F_LIVRAISON": "Livraison &amp; délais", "F_RETOURS": "Retours &amp; échanges",
        "F_GARANTIE": "Garantie &amp; entretien", "F_AVIS": "Avis clients",
        "F_FAQ": "Questions fréquentes", "F_CONTACT": "Nous contacter",
        "F_RDV_ONLY": "sur rendez-vous", "F_REPONSE": "Réponse sous 24&nbsp;h ouvrées",
        "F_MENTIONS": "Mentions légales", "F_CGV": "CGV", "F_CONFIDENTIALITE": "Confidentialité",
        "LANG_ARIA": "Choix de la langue",
    },
    "en": {
        "TOPBAR": "A jewellery house entirely online — free delivery, in France and worldwide",
        "L_HOME": "Home", "L_NAV": "Main navigation", "L_MENU": "Menu",
        "L_SURMESURE": "Bespoke", "L_COLLECTION": "Collection", "L_DIAMANTS": "Diamonds",
        "L_JOURNAL": "Journal", "L_APROPOS": "About", "L_AVIS": "Reviews",
        "L_GARANTIES": "Guarantees", "L_CONTACT": "Contact",
        "L_SELECTION": "My selection", "L_RDV": "Book an appointment",
        "L_WA_MSG": "Hello, I have a question about an Oneiro piece.",
        "L_WA_ARIA": "Message us on WhatsApp",
        "F_BASELINE": "Bespoke fine jewellery in 18 carat gold set with certified diamonds, designed in Paris and made in France. No boutique — and that is a choice.",
        "F_WIRE": "Bank&nbsp;transfer",
        "F_H_MAISON": "The House", "F_H_AIDE": "Help &amp; guarantees", "F_H_CONTACT": "Contact",
        "F_SURMESURE": "Bespoke", "F_FIANCAILLES": "Engagement rings", "F_ALLIANCE": "Wedding bands",
        "F_COLLECTION": "The collection", "F_DIAMANTS": "Oneiro Diamonds", "F_JOURNAL": "The Journal",
        "F_APROPOS": "About", "F_SELECTION": "My selection", "F_RDV": "Book an appointment",
        "F_LIVRAISON": "Delivery &amp; timing", "F_RETOURS": "Returns &amp; exchanges",
        "F_GARANTIE": "Warranty &amp; care", "F_AVIS": "Client reviews",
        "F_FAQ": "Frequently asked questions", "F_CONTACT": "Contact us",
        "F_RDV_ONLY": "by appointment", "F_REPONSE": "An answer within 24&nbsp;working hours",
        "F_MENTIONS": "Legal notice", "F_CGV": "Terms of sale", "F_CONFIDENTIALITE": "Privacy",
        "LANG_ARIA": "Language selection",
    },
}

OG_ALT = {
    "fr": "Bague de fiançailles Oneiro Paris — solitaire marquise en or 18 carats",
    "en": "Oneiro Paris engagement ring — marquise solitaire in 18 carat gold",
}
OG_LOCALE = {"fr": "fr_FR", "en": "en_GB"}

CAT = {
    "fr": {"bagues": "Bague", "boucles-oreilles": "Boucles d'oreilles", "colliers": "Collier", "bracelets": "Bracelet", "default": "Bijou"},
    "en": {"bagues": "Ring", "boucles-oreilles": "Earrings", "colliers": "Necklace", "bracelets": "Bracelet", "default": "Jewellery"},
}

PRODUCT_DIR = {"fr": "produits", "en": "products"}

# Traduction des noms et valeurs d'options : le catalogue source
# (assets/js/products-data.js) est en francais. Miroir de la table OPT de
# assets/js/product-page.js — les deux doivent rester synchronisees, sinon la
# version statique (moteurs de recherche, visiteurs sans JS) et la version
# hydratee par le JS ne diraient pas la meme chose.
OPTION_TR = {
    "Couleur": "Colour", "Taille diamants": "Diamond size",
    "Type de diamants": "Diamond type", "Type de diamant": "Diamond type",
    "Type de Diamant": "Diamond type", "Type de Diamants": "Diamond type",
    "Pierre Centrale": "Centre stone", "Sertissage": "Setting",
    "Taille de l\u2019anneau": "Ring size",
    "Or": "Yellow gold", "Or blanc": "White gold", "Or rose": "Rose gold",
    "Platine": "Platinum", "Naturel": "Natural", "Naturels": "Natural",
    "Laboratoire": "Lab-grown", "Laboratoires": "Lab-grown",
    "Avec griffes": "Claw set", "Avec Halo": "With halo",
}

def opt_tr(v, lang):
    return OPTION_TR.get(v, v) if lang == "en" else v

# Libelles des fiches produit generees en statique
PSTR = {
    "fr": {
        "crumbs_aria": "Fil d'Ariane", "home": "Accueil", "collection": "Collection",
        "from": "À partir de ",
        "lab": lambda p: f'ou <b>{p}</b> en diamant de laboratoire — et paiement en 3× avec Klarna',
        "klarna": "Paiement en <b>3×</b> possible avec Klarna",
        "reserve": "Réserver cette pièce", "video": "Voir cette pièce en visio",
        "note": "Or 18 carats — diamants certifiés GIA/IGI — façonné en France — livraison offerte — délai 2 à 7 semaines.",
        "note_link": "Toutes nos garanties",
        "also": "Vous aimerez aussi", "also_kicker": "Pour continuer",
        "customizable": " — personnalisable",
        "badge": "Personnalisable",
        "card_lab": lambda p: f"ou {p} en diamant de laboratoire",
        "default_desc": "Création Oneiro en or 18 carats et diamants certifiés. Détails et photos complémentaires sur demande.",
        "alt": lambda t, c: f"{t}, {c.lower()} en or 18 carats sertie de diamants certifies, Oneiro Paris",
        "wish_aria": "Ajouter a ma selection",
        "title_tpl": lambda t, c: f"{t} — {c} or 18 carats | Oneiro",
        "title_tpl2": lambda t, c: f"{t} — {c} | Oneiro Paris",
        "title_tpl3": lambda t: f"{t} | Oneiro Paris",
        "fallback_desc": lambda t, c: f"{t}, {c.lower()} Oneiro Paris en or 18 carats et diamants certifiés.",
        "material": "Or 18 carats",
        "natural_suffix": " en diamant naturel", "lab_suffix": " en diamant de laboratoire",
        "sku_natural": "-naturel", "sku_lab": "-laboratoire",
    },
    "en": {
        "crumbs_aria": "Breadcrumb", "home": "Home", "collection": "Collection",
        "from": "From ",
        "lab": lambda p: f'or <b>{p}</b> with a lab-grown diamond — and payment in 3 with Klarna',
        "klarna": "Payment in <b>3 instalments</b> available with Klarna",
        "reserve": "Reserve this piece", "video": "See this piece by video",
        "note": "18 carat gold — GIA/IGI certified diamonds — made in France — free delivery — ready in 2 to 7 weeks.",
        "note_link": "All our guarantees",
        "also": "You may also like", "also_kicker": "To continue",
        "customizable": " — customisable",
        "badge": "Customisable",
        "card_lab": lambda p: f"or {p} with a lab-grown diamond",
        "default_desc": "An Oneiro creation in 18 carat gold set with certified diamonds. Further details and photographs on request.",
        "alt": lambda t, c: f"{t}, {c.lower()} in 18 carat gold set with certified diamonds, Oneiro Paris",
        "wish_aria": "Add to my selection",
        "title_tpl": lambda t, c: f"{t} — {c} in 18ct gold | Oneiro",
        "title_tpl2": lambda t, c: f"{t} — {c} | Oneiro Paris",
        "title_tpl3": lambda t: f"{t} | Oneiro Paris",
        "fallback_desc": lambda t, c: f"{t}, an Oneiro Paris {c.lower()} in 18 carat gold with certified diamonds.",
        "material": "18 carat gold",
        "natural_suffix": " with a natural diamond", "lab_suffix": " with a lab-grown diamond",
        "sku_natural": "-natural", "sku_lab": "-lab-grown",
    },
}

# ============================================================================
# 3. Donnees structurees
# ============================================================================

def org_jsonld(lang):
    return {
        "@context": "https://schema.org",
        "@type": "JewelryStore",
        "name": "Oneiro Paris",
        "url": SITE_URL + ("/en/" if lang == "en" else ""),
        "logo": SITE_URL + "/assets/img/logo-oneiro.svg",
        "image": SITE_URL + "/assets/img/og-oneiro.jpg",
        "description": (
            "Bespoke fine jewellery in 18 carat gold and GIA/IGI certified diamonds, designed in Paris and made in France. An entirely online house."
            if lang == "en" else
            "Joaillerie sur-mesure en or 18 carats et diamants certifiés GIA/IGI, dessinée à Paris et façonnée en France. Maison 100 % en ligne."
        ),
        "priceRange": "€1,000 to €7,000" if lang == "en" else "1 000 € à 7 000 €",
        "email": "contact@oneiroparis.com",
        "sameAs": ["https://www.instagram.com/oneiro_paris"],
        "address": {"@type": "PostalAddress", "streetAddress": "3 rue de la Faisanderie", "postalCode": "75016", "addressLocality": "Paris", "addressCountry": "FR"},
        "contactPoint": {"@type": "ContactPoint", "contactType": "customer service", "email": "contact@oneiroparis.com", "availableLanguage": ["fr", "en"]},
    }

def website_jsonld(lang):
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Oneiro Paris",
        "url": SITE_URL + ("/en/" if lang == "en" else ""),
        "inLanguage": "en" if lang == "en" else "fr",
    }

# FAQ de la page garanties (doit rester synchronisee avec pages/garanties.html
# et pages-en/guarantees.html)
FAQ = {
    "fr": [
        ("Puis-je voir le bijou avant d'acheter, sans boutique ?",
         "Oui, autrement. En visio, nous vous montrons la pièce ou des pièces équivalentes sous toutes les coutures, en lumière naturelle, avec les certificats. Pour le sur-mesure, vous validez une modélisation 3D fidèle avant fabrication. La joaillerie fine bénéficie de 15 jours de retour après réception."),
        ("Comment être sûr que le diamant vaut son prix ?",
         "Chaque pierre est décrite par un certificat indépendant (GIA/IGI) remis avant l'achat. Nos prix s'entendent sans la marge d'une boutique physique, comparez à caractéristiques égales."),
        ("Que se passe-t-il si le colis est perdu ou endommagé ?",
         "Les envois sont suivis et remis contre signature. En cas de problème de transport, nous gérons le dossier avec le transporteur."),
        ("Faites-vous les alliances assorties ?",
         "Oui. Parlez-en dès la bague de fiançailles pour penser l'empilage : nous gardons les plans de votre pièce."),
        ("Proposez-vous un paiement en plusieurs fois ?",
         "Oui, en 3 fois via Klarna, en plus du paiement comptant par carte, PayPal, Apple Pay ou virement."),
        ("Livrez-vous à l'étranger ?",
         "Oui, la livraison est offerte à l'international. Hors UE, les droits et taxes d'importation locaux restent à votre charge."),
    ],
    "en": [
        ("Can I see the piece before buying, with no boutique?",
         "Yes, differently. By video we show you the piece or equivalent pieces from every angle, in natural light, with the certificates. For bespoke, you approve a faithful 3D model before production. Fine jewellery comes with 15 days to return it after delivery."),
        ("How can I be sure the diamond is worth its price?",
         "Every stone is described by an independent certificate (GIA/IGI) handed over before the purchase. Our prices carry no physical boutique's margin, so compare like for like."),
        ("What happens if the parcel is lost or damaged?",
         "Shipments are tracked and handed over against signature. If there is a transport problem, we handle the claim with the carrier."),
        ("Do you make matching wedding bands?",
         "Yes. Mention it as early as the engagement ring so we can think about the stack: we keep the files for your piece."),
        ("Do you offer payment in instalments?",
         "Yes, in 3 instalments via Klarna, alongside payment in full by card, PayPal, Apple Pay or bank transfer."),
        ("Do you deliver abroad?",
         "Yes, delivery is free internationally. Outside the EU, local import duties and taxes are payable by you."),
    ],
}

def faq_jsonld(lang):
    return {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in FAQ[lang]
        ],
    }

# ============================================================================
# 4. Utilitaires
# ============================================================================

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(s)

def jsonld(obj):
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>"

def fmt_money(n, lang):
    if lang == "en":
        return "€" + f"{n:,.0f}"
    return f"{n:,.0f}".replace(",", " ") + " €"

def page_url(key, lang):
    """URL relative au domaine (sans slash initial) d'une page racine."""
    slug = SLUGS[key][0 if lang == "fr" else 1]
    if lang == "fr":
        return "" if key == "index" else slug + ".html"
    return "en/" if key == "index" else "en/" + slug + ".html"

def article_url(key, lang):
    slug = ARTICLES[key][lang]["slug"]
    return ("journal/" if lang == "fr" else "en/journal/") + slug + ".html"

def product_url(handle, lang):
    return ("" if lang == "fr" else "en/") + PRODUCT_DIR[lang] + "/" + handle + ".html"

# ============================================================================
# 5. Cartes produit en HTML statique
# ============================================================================
# Miroir de O.card() dans assets/js/app.js. Le JS re-rend ces grilles a
# l'identique au chargement (avec l'animation reveal) ; cette version statique
# existe pour les moteurs de recherche, qui ne suivaient jusqu'ici aucun lien
# vers les fiches produit, et pour les visiteurs sans JavaScript.

def img_url(src, w=720):
    return src + ("&" if "?" in src else "?") + "width=" + str(w)

def p_title(p, lang):
    if lang == "en":
        return PRODUCTS_EN.get(p["handle"], {}).get("title") or p["title"]
    return p["title"]

def p_desc(p, lang):
    if lang == "en":
        return (PRODUCTS_EN.get(p["handle"], {}).get("description") or "").strip()
    return (p.get("description") or "").strip()

def card_html(p, lang):
    e = html.escape
    S = PSTR[lang]
    cat = CAT[lang].get(p["category"], CAT[lang]["default"])
    title = p_title(p, lang)
    lab = f'<small>{S["card_lab"](fmt_money(p["priceLab"], lang))}</small>' if p.get("priceLab") else ""
    badge = f'<span class="card__badge">{S["badge"]}</span>' if p.get("customizable") else ""
    imgs = p.get("images") or []
    alt = S["alt"](title, cat)
    img = f'<img src="{e(img_url(imgs[0], 720))}" alt="{e(alt)}" loading="lazy" width="720" height="720">' if imgs else ""
    wish = (f'<button type="button" class="wish-btn" data-wish="{e(p["handle"])}" aria-pressed="false" aria-label="{e(S["wish_aria"])}">'
            '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20.5 3.8 12.3a5 5 0 0 1 7.1-7.1l1.1 1.1 1.1-1.1a5 5 0 1 1 7.1 7.1z"/></svg></button>')
    multi = (p.get("priceNatural") and p.get("priceLab") and p["priceNatural"] != p["priceLab"]) or len(p.get("variants") or []) > 1
    frm = S["from"] if multi else ""
    return (f'<a class="card" href="{PRODUCT_DIR[lang]}/{e(p["handle"])}.html">'
            f'<div class="card__img">{img}{badge}{wish}</div>'
            f'<div class="card__body">'
            f'<span class="card__cat">{e(cat)}</span>'
            f'<span class="card__title">{e(title)}</span>'
            f'<span class="card__price">{frm}{fmt_money(p.get("priceNatural") or p["priceFrom"], lang)}{lab}</span>'
            f'</div></a>')

def grid_html(products, lang):
    return "".join(card_html(p, lang) for p in products)

def inject_grids(body, lang):
    """Remplit les <div class="grid" id="..."></div> vides des pages sources."""
    order = {"bagues": 1, "boucles-oreilles": 2, "colliers": 3, "bracelets": 4}
    tout = sorted(PRODUCTS, key=lambda p: order.get(p["category"], 9))
    bagues_perso = [p for p in tout if p.get("customizable") and p["category"] == "bagues"][:8]
    accueil = [p for p in (next((x for x in PRODUCTS if x["handle"] == h), None)
               for h in ["ami", "creole-en-diamants", "pendentif-personnalisable", "elya"]) if p]
    for gid, sel in (("catalog", tout), ("home-products", accueil),
                     ("engagement-products", bagues_perso), ("custom-products", bagues_perso)):
        vide = f'<div class="grid" id="{gid}"></div>'
        if vide in body:
            body = body.replace(vide, f'<div class="grid" id="{gid}">{grid_html(sel, lang)}</div>')
    return body

# --- Journal : cartes d'index, pieces recommandees, articles lies ------------

JSTR = {
    "fr": {
        "pieces_kicker": "Dans la collection",
        "pieces_title": "Les pièces dont on parle",
        "pieces_sub": "Les créations Oneiro citées dans cet article — toutes personnalisables : autre pierre, autre or, autres proportions.",
        "see_all": "Voir toute la collection",
        "next_kicker": "Pour continuer",
        "next_title": "À lire ensuite",
        "all_articles": "Tous les articles du Journal",
        "published": "Publié le",
        "months": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet",
                   "août", "septembre", "octobre", "novembre", "décembre"],
    },
    "en": {
        "pieces_kicker": "In the collection",
        "pieces_title": "The pieces we mention",
        "pieces_sub": "The Oneiro creations cited in this article — all of them customisable: another stone, another gold, other proportions.",
        "see_all": "See the whole collection",
        "next_kicker": "To continue",
        "next_title": "Read next",
        "all_articles": "All the articles in the Journal",
        "published": "Published",
        "months": ["January", "February", "March", "April", "May", "June", "July",
                   "August", "September", "October", "November", "December"],
    },
}

def pretty_date(iso, lang):
    y, m, d = (int(x) for x in iso.split("-"))
    mon = JSTR[lang]["months"][m - 1]
    return f"{d} {mon} {y}" if lang == "fr" else f"{d} {mon} {y}"

def journal_card(key, lang):
    """Carte d'article pour l'index du Journal — meme habillage que les produits."""
    e = html.escape
    a = ARTICLES[key]
    L = a[lang]
    href = article_url(key, lang)
    # Les pages du Journal posent <base href="../"> : on vise depuis la racine.
    href_rel = href[len("en/"):] if lang == "en" else href
    img = a["image"] + ("&" if "?" in a["image"] else "?") + "width=720"
    # Pas de classe « reveal » : ces cartes sont du HTML statique, lisible par
    # les moteurs et par les visiteurs sans JavaScript (comme les cartes produit).
    return (f'<a class="card" href="{e(href_rel)}">'
            f'<div class="card__img"><img src="{e(img)}" alt="{e(L["card"])}" loading="lazy" width="720" height="720"></div>'
            f'<div class="card__body">'
            f'<span class="card__cat">{e(L["cat"])}</span>'
            f'<span class="card__title">{e(L["card"])}</span>'
            f'<span class="card__price">{e(L["teaser"])}</span>'
            f'</div></a>')

def inject_journal(body, lang):
    """Remplit les grilles vides de la page Journal, section par section."""
    for section in ("actu", "guide"):
        vide = f'<div class="grid grid--3" id="journal-{section}"></div>'
        if vide in body:
            cards = "".join(journal_card(k, lang) for k in articles_in(section))
            body = body.replace(vide, f'<div class="grid grid--3" id="journal-{section}">{cards}</div>')
    return body

def article_products_block(key, lang):
    """« Les pieces dont on parle » : la passerelle article -> fiche produit."""
    handles = ARTICLES[key].get("products") or []
    prods = [p for h in handles for p in PRODUCTS if p["handle"] == h]
    if not prods:
        return ""
    S = JSTR[lang]
    e = html.escape
    return f'''
<section class="section section--cream">
  <div class="wrap">
    <span class="kicker reveal">{e(S["pieces_kicker"])}</span>
    <h2 class="section-title reveal">{e(S["pieces_title"])}</h2>
    <p class="section-sub reveal">{e(S["pieces_sub"])}</p>
    <div class="grid" id="article-products">{grid_html(prods, lang)}</div>
    <div class="btn-row" style="margin-top:44px"><a class="btn" href="{nav_href("collection", lang)}">{e(S["see_all"])}</a></div>
  </div>
</section>
'''

def article_cta_block(lang):
    """Meme pied de page pour tous les articles : une conversation, pas un formulaire."""
    if lang == "en":
        return f'''
<section class="cta-band">
  <h2 class="reveal">The most useful guide is still a conversation.</h2>
  <p class="reveal">Thirty minutes, by video or in person in Paris, free and with no obligation. Bring your questions — and your inspiration photographs if you have any.</p>
  <div class="btn-row reveal"><a class="btn btn--gold" href="{nav_href("rendez-vous", "en")}">Book an appointment</a><a class="btn btn--light" href="{nav_href("collection", "en")}">See the collection</a></div>
</section>
'''
    return f'''
<section class="cta-band">
  <h2 class="reveal">Le guide le plus utile reste une conversation.</h2>
  <p class="reveal">Trente minutes, en visio ou en personne à Paris, offertes et sans engagement. Venez avec vos questions — et vos photos d'inspiration si vous en avez.</p>
  <div class="btn-row reveal"><a class="btn btn--gold" href="{nav_href("rendez-vous", "fr")}">Prendre rendez-vous</a><a class="btn btn--light" href="{nav_href("collection", "fr")}">Voir la collection</a></div>
</section>
'''

def article_related_block(key, lang):
    """Trois autres articles : d'abord la meme section, puis le reste."""
    same = [k for k in articles_in(ARTICLES[key]["section"]) if k != key]
    other = [k for k in ARTICLES if k != key and k not in same]
    picks = (same + sorted(other, key=lambda k: ARTICLES[k]["date"], reverse=True))[:3]
    if not picks:
        return ""
    S = JSTR[lang]
    e = html.escape
    cards = "".join(journal_card(k, lang) for k in picks)
    return f'''
<section class="section">
  <div class="wrap">
    <span class="kicker reveal">{e(S["next_kicker"])}</span>
    <h2 class="section-title reveal">{e(S["next_title"])}</h2>
    <div class="grid grid--3">{cards}</div>
    <div class="btn-row" style="margin-top:44px"><a class="btn" href="{nav_href("journal", lang)}">{e(S["all_articles"])}</a></div>
  </div>
</section>
'''

# ============================================================================
# 6. Politiques commerciales pour les donnees structurees Offer
# ============================================================================

SHIPPING_JSONLD = {
    "@type": "OfferShippingDetails",
    "shippingRate": {"@type": "MonetaryAmount", "value": 0, "currency": "EUR"},
    "shippingDestination": [{"@type": "DefinedRegion", "addressCountry": c}
                            for c in ("FR", "BE", "LU", "CH", "DE", "IT", "ES")],
    "deliveryTime": {
        "@type": "ShippingDeliveryTime",
        "handlingTime": {"@type": "QuantitativeValue", "minValue": 14, "maxValue": 49, "unitCode": "DAY"},
        "transitTime": {"@type": "QuantitativeValue", "minValue": 1, "maxValue": 3, "unitCode": "DAY"},
    },
}
PRICE_VALID_UNTIL = (datetime.date.today() + datetime.timedelta(days=365)).isoformat()

def offers_jsonld(p, lang):
    """Un Offer par type de pierre plutot qu'un AggregateOffer : les fiches
    marchandes Google demandent un prix ferme, un identifiant et la livraison."""
    S = PSTR[lang]
    url = f'{SITE_URL}/{product_url(p["handle"], lang)}'
    title = p_title(p, lang)
    base = {
        "@type": "Offer", "priceCurrency": "EUR", "url": url,
        "availability": "https://schema.org/InStock" if p.get("available") else "https://schema.org/OutOfStock",
        "itemCondition": "https://schema.org/NewCondition",
        "priceValidUntil": PRICE_VALID_UNTIL,
        "seller": {"@type": "Organization", "name": "Oneiro Paris"},
        "shippingDetails": SHIPPING_JSONLD,
    }
    out = []
    if p.get("priceNatural"):
        out.append({**base, "name": title + S["natural_suffix"],
                    "sku": p["handle"] + S["sku_natural"], "price": p["priceNatural"]})
    if p.get("priceLab") and p.get("priceLab") != p.get("priceNatural"):
        out.append({**base, "name": title + S["lab_suffix"],
                    "sku": p["handle"] + S["sku_lab"], "price": p["priceLab"]})
    if not out:
        out.append({**base, "sku": p["handle"], "price": p["priceFrom"]})
    return out

def source_lastmod(key, kind, lang):
    """Date de derniere modification reelle de la source d'une URL."""
    pages_dir = "pages" if lang == "fr" else "pages-en"
    arts_dir = "articles" if lang == "fr" else "articles-en"
    if kind == "page":
        cand = os.path.join(ROOT, pages_dir, SLUGS[key][0 if lang == "fr" else 1] + ".html")
    elif kind == "article":
        cand = os.path.join(ROOT, arts_dir, ARTICLES[key][lang]["slug"] + ".html")
    else:
        cand = os.path.join(SITE, "assets", "js", "products-data.js")
    try:
        return datetime.date.fromtimestamp(os.path.getmtime(cand)).isoformat()
    except OSError:
        return TODAY

# ============================================================================
# 7. Assemblage
# ============================================================================

def langswitch(fr_url, en_url, lang):
    cur_fr = "true" if lang == "fr" else "false"
    cur_en = "true" if lang == "en" else "false"
    aria = CHROME[lang]["LANG_ARIA"]
    return (f'<span class="langswitch" role="group" aria-label="{aria}">'
            f'<a href="/{fr_url}" hreflang="fr" lang="fr" aria-current="{cur_fr}">FR</a>'
            f'<span aria-hidden="true">/</span>'
            f'<a href="/{en_url}" hreflang="en" lang="en" aria-current="{cur_en}">EN</a>'
            f'</span>')

def chrome(lang, fr_url, en_url):
    """Header et footer traduits, avec le selecteur de langue de cette page."""
    C = dict(CHROME[lang])
    urls = {
        "U_INDEX": nav_href("index", lang),
        "U_SURMESURE": nav_href("sur-mesure", lang),
        "U_FIANCAILLES": nav_href("bague-de-fiancailles", lang),
        "U_ALLIANCE": nav_href("alliance", lang),
        "U_COLLECTION": nav_href("collection", lang),
        "U_DIAMANTS": nav_href("diamants", lang),
        "U_JOURNAL": nav_href("journal", lang),
        "U_APROPOS": nav_href("a-propos", lang),
        "U_AVIS": nav_href("avis", lang),
        "U_GARANTIES": nav_href("garanties", lang),
        "U_CONTACT": nav_href("contact", lang),
        "U_SELECTION": nav_href("selection", lang),
        "U_RDV": nav_href("rendez-vous", lang),
        "U_MENTIONS": nav_href("mentions-legales", lang),
        "U_CGV": nav_href("cgv", lang),
        "U_CONFIDENTIALITE": nav_href("confidentialite", lang),
    }
    C.update(urls)
    C["LANGSWITCH"] = langswitch(fr_url, en_url, lang)
    h, f = HEADER_TPL, FOOTER_TPL
    for k, v in C.items():
        h = h.replace("{{" + k + "}}", str(v))
        f = f.replace("{{" + k + "}}", str(v))
    return h, f

def nav_href(key, lang):
    """Lien de navigation, relatif (les pages profondes posent un <base>)."""
    slug = SLUGS[key][0 if lang == "fr" else 1]
    return "index.html" if key == "index" else slug + ".html"

def assemble(lang, title, desc, body, canonical, fr_url, en_url, extra_head="", base=""):
    h = HEAD_TPL.replace("{{TITLE}}", html.escape(title)).replace("{{DESC}}", html.escape(desc))
    h = h.replace("{{V}}", ASSET_V)
    h = h.replace("{{LANG}}", "en" if lang == "en" else "fr")
    h = h.replace("{{OGLOCALE}}", OG_LOCALE[lang])
    h = h.replace("{{OGALT}}", html.escape(OG_ALT[lang]))
    h = h.replace("{{OG}}", SITE_URL + "/assets/img/og-oneiro.jpg")
    h = h.replace("{{I18N_SCRIPT}}",
                  f'  <script src="/assets/js/products-en.js?v={ASSET_V}" defer></script>\n' if lang == "en" else "")
    inject = (
        f'<link rel="canonical" href="{SITE_URL}/{canonical}">\n'
        f'<link rel="alternate" hreflang="fr" href="{SITE_URL}/{fr_url}">\n'
        f'<link rel="alternate" hreflang="en" href="{SITE_URL}/{en_url}">\n'
        f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}/{fr_url}">\n'
        + extra_head
    )
    if base:
        inject = f'<base href="{base}">\n' + inject
    h = h.replace("<head>", "<head>\n  " + inject.rstrip())
    header, footer = chrome(lang, fr_url, en_url)
    return h + header + body.replace("{{V}}", ASSET_V) + footer

# ============================================================================
# 8. Donnees
# ============================================================================

# --- produits.json (regenere via Node si possible, sinon cache) -------------
pj = os.path.join(ROOT, "products.json")
try:
    out = subprocess.run(
        ["node", "-e", "console.log(JSON.stringify(require(process.argv[1]).ONEIRO_PRODUCTS))",
         os.path.join(SITE, "assets", "js", "products-data.js")],
        capture_output=True, text=True, timeout=20)
    if out.returncode == 0 and out.stdout.strip().startswith("["):
        write(pj, out.stdout.strip())
except Exception:
    pass
PRODUCTS = json.loads(read(pj))

# --- traductions anglaises des fiches produit --------------------------------
try:
    PRODUCTS_EN = json.loads(read(os.path.join(ROOT, "products-en.json")))
except Exception:
    PRODUCTS_EN = {}

# --- avis clients lus depuis assets/js/config.js (pour les donnees structurees) ---
REVIEWS = []
try:
    _out = subprocess.run(
        ["node", "-e",
         "const fs=require('fs');eval(fs.readFileSync(process.argv[1],'utf8')"
         ".replace('const ONEIRO_CONFIG','globalThis.ONEIRO_CONFIG'));"
         "console.log(JSON.stringify(ONEIRO_CONFIG.reviews||[]))",
         os.path.join(SITE, "assets", "js", "config.js")],
        capture_output=True, text=True, timeout=20)
    if _out.returncode == 0 and _out.stdout.strip().startswith("["):
        REVIEWS = json.loads(_out.stdout.strip())
except Exception:
    pass

def reviews_jsonld(lang):
    """Donnees structurees d'avis — uniquement si de vrais avis sont configures."""
    if not REVIEWS:
        return ""
    rated = [r for r in REVIEWS if r.get("rating")]
    if not rated:
        return ""
    avg = round(sum(r["rating"] for r in rated) / len(rated), 1)
    obj = {
        "@context": "https://schema.org", "@type": "JewelryStore",
        "name": "Oneiro Paris", "url": SITE_URL + ("/en/" if lang == "en" else ""),
        "aggregateRating": {
            "@type": "AggregateRating", "ratingValue": avg,
            "reviewCount": len(REVIEWS), "bestRating": 5, "worstRating": 1,
        },
        "review": [{
            "@type": "Review",
            "reviewRating": {"@type": "Rating", "ratingValue": r.get("rating", 5), "bestRating": 5},
            "author": {"@type": "Person", "name": r.get("author", "Client Oneiro")},
            "reviewBody": r.get("text", ""),
            **({"datePublished": r["date"]} if r.get("date") else {}),
        } for r in REVIEWS[:20]],
    }
    return jsonld(obj) + "\n"

# --- Anti-cache : suffixe de version calcule sur le contenu des assets --------
# Le navigateur recharge automatiquement CSS et JS des qu'ils changent,
# sans que personne ait a vider son cache.
import hashlib

def asset_version():
    h = hashlib.md5()
    for rel in ["assets/css/style.css", "assets/js/config.js",
                "assets/js/products-data.js", "assets/js/app.js",
                "assets/js/product-page.js", "assets/js/configurator.js"]:
        fp = os.path.join(SITE, rel)
        if os.path.exists(fp):
            with open(fp, "rb") as fh:
                h.update(fh.read())
    h.update(json.dumps(PRODUCTS_EN, sort_keys=True, ensure_ascii=False).encode("utf-8"))
    return h.hexdigest()[:8]

ASSET_V = asset_version()

HEAD_TPL = read(os.path.join(ROOT, "head.tpl"))
HEADER_TPL = read(os.path.join(ROOT, "header.html"))
FOOTER_TPL = read(os.path.join(ROOT, "footer.html"))

# --- assets/js/products-en.js : titres et descriptions anglais ----------------
# Charge uniquement par les pages /en/, juste apres products-data.js : les
# champs titleEn / descriptionEn sont poses sur ONEIRO_PRODUCTS avant app.js.
def write_products_en_js():
    payload = {h: {"title": v.get("title", ""), "description": v.get("description", "")}
               for h, v in PRODUCTS_EN.items()}
    js = (
        "// Genere par _build/build.py depuis _build/products-en.json — ne pas editer a la main.\n"
        "(function () {\n"
        "  var M = " + json.dumps(payload, ensure_ascii=False, indent=2) + ";\n"
        "  if (typeof ONEIRO_PRODUCTS === 'undefined') return;\n"
        "  ONEIRO_PRODUCTS.forEach(function (p) {\n"
        "    var m = M[p.handle];\n"
        "    if (!m) return;\n"
        "    if (m.title) p.titleEn = m.title;\n"
        "    if (m.description) p.descriptionEn = m.description;\n"
        "  });\n"
        "})();\n"
    )
    write(os.path.join(SITE, "assets", "js", "products-en.js"), js)

write_products_en_js()

# ============================================================================
# 9. Generation
# ============================================================================

built = []
urls = []   # (url, lang, kind, key)

NO_SITEMAP = ("produit", "selection", "404")  # pages personnelles/dynamiques

for lang in ("fr", "en"):
    pages_dir = os.path.join(ROOT, "pages" if lang == "fr" else "pages-en")

    # --- 1. Pages racine ------------------------------------------------------
    for key in SLUGS:
        slug = SLUGS[key][0 if lang == "fr" else 1]
        src = os.path.join(pages_dir, slug + ".html")
        if not os.path.exists(src):
            print(f"  ! source manquante, page ignoree : {os.path.relpath(src, SITE)}")
            continue
        title, desc = META[lang][key]
        body = inject_journal(inject_grids(read(src), lang), lang)
        extra = ""
        if key == "index":
            extra = jsonld(org_jsonld(lang)) + "\n" + jsonld(website_jsonld(lang)) + "\n"
        elif key == "avis":
            extra = reviews_jsonld(lang)
        elif key == "garanties":
            extra = jsonld(faq_jsonld(lang)) + "\n"
        rel = page_url(key, lang)
        fr_url, en_url = page_url(key, "fr"), page_url(key, "en")
        # Les pages racine de chaque langue sont a la racine de leur dossier :
        # aucun <base> n'est necessaire, les liens relatifs tombent juste.
        out = os.path.join(SITE, "en", "index.html") if rel == "en/" else (
              os.path.join(SITE, "index.html") if rel == "" else os.path.join(SITE, *rel.split("/")))
        write(out, assemble(lang, title, desc, body, rel, fr_url, en_url, extra))
        built.append(rel or "index.html")
        if key not in NO_SITEMAP:
            urls.append((rel, lang, "page", key))

    # --- 2. Articles du Journal ----------------------------------------------
    arts_dir = os.path.join(ROOT, "articles" if lang == "fr" else "articles-en")
    for key in sorted(ARTICLES, key=lambda k: ARTICLES[k]["date"], reverse=True):
        a = ARTICLES[key]
        date = a["date"]
        slug = a[lang]["slug"]
        src = os.path.join(arts_dir, slug + ".html")
        if not os.path.exists(src):
            print(f"  ! source manquante, article ignore : {os.path.relpath(src, SITE)}")
            continue
        title, desc = a[lang]["title"], a[lang]["desc"]
        body = (read(src) + article_products_block(key, lang)
                + article_related_block(key, lang) + article_cta_block(lang))
        rel = article_url(key, lang)
        fr_url, en_url = article_url(key, "fr"), article_url(key, "en")
        art = {
            "@context": "https://schema.org", "@type": "Article",
            "headline": title.split(" | ")[0], "description": desc,
            "datePublished": date, "dateModified": TODAY,
            "image": [a["image"]],
            "articleSection": JOURNAL_SECTIONS[lang][a["section"]][0],
            "inLanguage": "en" if lang == "en" else "fr",
            "author": {"@type": "Organization", "name": "Oneiro Paris"},
            "publisher": {"@type": "Organization", "name": "Oneiro Paris",
                          "logo": {"@type": "ImageObject", "url": SITE_URL + "/assets/img/logo-oneiro.svg"}},
            "mainEntityOfPage": f"{SITE_URL}/{rel}",
        }
        write(os.path.join(SITE, *rel.split("/")),
              assemble(lang, title, desc, body, rel, fr_url, en_url, jsonld(art) + "\n", base="../"))
        built.append(rel)
        urls.append((rel, lang, "article", key))

    # --- 3. Pages produit statiques -------------------------------------------
    for p in PRODUCTS:
        S = PSTR[lang]
        e = html.escape
        cat = CAT[lang].get(p["category"], CAT[lang]["default"])
        title_p = p_title(p, lang)
        imgs = p.get("images") or []
        prices = [v["price"] for v in p["variants"] if v.get("price")]
        d = p_desc(p, lang)
        desc_body = d or S["default_desc"]
        multi = len(set(prices)) > 1
        price_line = (S["from"] if multi else "") + fmt_money(p.get("priceNatural") or p["priceFrom"], lang)
        if p.get("priceLab") and p.get("priceNatural") != p.get("priceLab"):
            lab_line = f'<div class="pinfo__klarna">{S["lab"](fmt_money(p["priceLab"], lang))}</div>'
        else:
            lab_line = f'<div class="pinfo__klarna">{S["klarna"]}</div>'
        gallery = "".join(
            f'<div class="gallery__main" style="margin-bottom:12px"><img src="{e(src)}{"&" if "?" in src else "?"}width=1100" '
            f'alt="{e(title_p)} — {e(cat)} Oneiro Paris" loading="{"eager" if i == 0 else "lazy"}"></div>'
            for i, src in enumerate(imgs[:2]))
        opts = "".join(
            f'<div class="opt"><label>{e(opt_tr(o["name"], lang))}</label><div class="opt__values">'
            + "".join(f'<button type="button" disabled style="cursor:default">{e(opt_tr(v, lang))}</button>' for v in o["values"])
            + "</div></div>" for o in p.get("options", []))

        rel = product_url(p["handle"], lang)
        fr_url, en_url = product_url(p["handle"], "fr"), product_url(p["handle"], "en")
        h_index = nav_href("index", lang)
        h_collection = nav_href("collection", lang)
        h_contact = nav_href("contact", lang)
        h_rdv = nav_href("rendez-vous", lang)
        h_garanties = nav_href("garanties", lang)

        related = sorted([x for x in PRODUCTS if x["handle"] != p["handle"]],
                         key=lambda x: x["category"] != p["category"])[:4]

        body = f'''<section class="section" id="product-root">
  <div class="wrap">
    <nav class="crumbs" aria-label="{e(S["crumbs_aria"])}" style="margin-bottom:28px"><a class="textlink" href="{h_index}">{e(S["home"])}</a> <span aria-hidden="true">›</span> <a class="textlink" href="{h_collection}">{e(S["collection"])}</a> <span aria-hidden="true">›</span> <span>{e(title_p)}</span></nav>
    <div class="product" id="product">
      <div class="gallery">{gallery}</div>
      <div class="pinfo">
        <span class="kicker">{e(cat)}{S["customizable"] if p.get("customizable") else ""}</span>
        <h1>{e(title_p)}</h1>
        <div class="pinfo__price">{price_line}</div>
        {lab_line}
        <p class="pinfo__desc">{e(desc_body)}</p>
        {opts}
        <div class="pinfo__cta">
          <a class="btn btn--solid" href="{h_contact}">{e(S["reserve"])}</a>
          <a class="btn" href="{h_rdv}">{e(S["video"])}</a>
        </div>
        <p class="pinfo__note">{S["note"]} <a href="{h_garanties}">{e(S["note_link"])}</a>.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section--cream">
  <div class="wrap">
    <span class="kicker reveal">{e(S["also_kicker"])}</span>
    <h2 class="section-title reveal">{e(S["also"])}</h2>
    <div class="grid" id="related">{grid_html(related, lang)}</div>
  </div>
</section>

<script>window.PRODUCT_HANDLE = "{p["handle"]}";</script>
<script src="/assets/js/product-page.js?v={ASSET_V}"></script>
'''

        # Google tronque les titres vers 600 px de large (~58 caracteres) :
        # sur les noms longs, on abrege plutot que de se faire couper.
        title = S["title_tpl"](title_p, cat)
        if len(title) > 58:
            title = S["title_tpl2"](title_p, cat)
        if len(title) > 58:
            title = S["title_tpl3"](title_p)
        desc = (d[:150] + "…" if len(d) > 152 else d) or S["fallback_desc"](title_p, cat)

        prod_ld = {
            "@context": "https://schema.org", "@type": "Product",
            "name": title_p, "description": desc,
            "image": imgs[:3],
            "brand": {"@type": "Brand", "name": "Oneiro Paris"},
            "url": f"{SITE_URL}/{rel}",
            "sku": p["handle"],
            "material": S["material"],
            "category": cat,
            "offers": offers_jsonld(p, lang),
        }
        crumbs = {
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": S["home"], "item": SITE_URL + "/" + page_url("index", lang)},
                {"@type": "ListItem", "position": 2, "name": S["collection"], "item": SITE_URL + "/" + page_url("collection", lang)},
                {"@type": "ListItem", "position": 3, "name": title_p},
            ],
        }
        write(os.path.join(SITE, *rel.split("/")),
              assemble(lang, title, desc, body, rel, fr_url, en_url,
                       jsonld(prod_ld) + "\n" + jsonld(crumbs) + "\n", base="../"))
        built.append(rel)
        urls.append((rel, lang, "product", p["handle"]))

# ============================================================================
# 10. sitemap.xml + robots.txt
# ============================================================================

PRIORITY = {
    "index": "1.0", "bague-de-fiancailles": "0.9", "sur-mesure": "0.9", "diamants": "0.9",
    "collection": "0.8", "alliance": "0.8", "journal": "0.7", "avis": "0.7",
}

sm = ['<?xml version="1.0" encoding="UTF-8"?>',
      '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
for rel, lang, kind, key in urls:
    if kind == "page":
        pr = PRIORITY.get(key, "0.5")
        alts = [("fr", page_url(key, "fr")), ("en", page_url(key, "en"))]
    elif kind == "article":
        pr = "0.7" if ARTICLES[key]["section"] == "guide" else "0.6"
        alts = [("fr", article_url(key, "fr")), ("en", article_url(key, "en"))]
    else:
        pr = "0.6"
        alts = [("fr", product_url(key, "fr")), ("en", product_url(key, "en"))]
    # L'anglais reste secondaire dans la hierarchie du site
    if lang == "en":
        pr = f"{max(0.4, float(pr) - 0.1):.1f}"
    sm.append(f"  <url><loc>{SITE_URL}/{rel}</loc><lastmod>{source_lastmod(key, kind, lang)}</lastmod><priority>{pr}</priority>"
              + "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{SITE_URL}/{u}"/>' for l, u in alts)
              + "</url>")
sm.append("</urlset>")
write(os.path.join(SITE, "sitemap.xml"), "\n".join(sm) + "\n")

write(os.path.join(SITE, "robots.txt"),
      "User-agent: *\nAllow: /\nDisallow: /_build/\nDisallow: /_source/\n"
      "Disallow: /produit.html\nDisallow: /selection.html\n"
      "Disallow: /en/product.html\nDisallow: /en/wishlist.html\n"
      f"\nSitemap: {SITE_URL}/sitemap.xml\n")

print(f"OK — {len(built)} pages générées en 2 langues "
      f"({len(PRODUCTS)} produits, {len(ARTICLES)} articles par langue) "
      f"+ sitemap.xml ({len(urls)} URL) + robots.txt")
# v3 — bilingue FR / EN
