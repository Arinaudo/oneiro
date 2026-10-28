# Registre du Journal.
# Deux sections : "actu" (actualites, datees, a rafraichir) et "guide"
# (intemporel, la colonne vertebrale SEO). Chaque article declare les pieces
# de la collection dont il parle : build.py en tire automatiquement le bloc
# « Les pieces dont on parle » en bas de l'article, dans les deux langues.
#
# Pour ajouter un article : une entree ici + le fichier source dans
# _build/articles/<slug-fr>.html et _build/articles-en/<slug-en>.html.

ONE = "https://oneiroparis.com/cdn/shop/files/"

ARTICLES = {

    # ---------------------------------------------------------------- ACTU --
    "or-record-2026": {
        "date": "2026-09-18", "section": "actu",
        "image": ONE + "Photoroom_20250203_113624.jpg",
        "products": ["bague-4", "lena", "bague-1"],
        "fr": {
            "slug": "prix-de-l-or-2026",
            "cat": "Actualité — Matières",
            "card": "L'or au plus haut : ce que ça change pour votre bijou",
            "teaser": "Pourquoi le cours de l'or pèse moins sur la facture qu'on ne le croit — et où regarder vraiment.",
            "title": "Prix de l'or en 2026 : l'impact réel sur un bijou | Oneiro",
            "desc": "L'or est au plus haut, mais il ne représente qu'une part du prix d'une bague. Ce qui bouge vraiment, ce qui ne bouge pas, et les trois arbitrages qui comptent en 2026.",
        },
        "en": {
            "slug": "gold-price-2026",
            "cat": "News — Materials",
            "card": "Gold at record levels: what it changes for your piece",
            "teaser": "Why the gold price weighs less on the bill than people think — and where to look instead.",
            "title": "Gold prices in 2026: the real impact on a piece | Oneiro",
            "desc": "Gold is at record levels, but it is only part of the price of a ring. What actually moves, what does not, and the three trade-offs that matter in 2026.",
        },
    },

    "diamant-labo-prix-2026": {
        "date": "2026-09-10", "section": "actu",
        "image": ONE + "9E02A374-D8BD-48A7-9834-DC248A59479C.jpg",
        "products": ["ami", "kyra", "selena"],
        "fr": {
            "slug": "prix-diamant-laboratoire-2026",
            "cat": "Actualité — Diamants",
            "card": "Diamant de laboratoire : où en sont les prix en 2026",
            "teaser": "La baisse continue, l'écart avec le naturel se stabilise. Ce que ça implique concrètement pour un budget.",
            "title": "Prix du diamant de laboratoire en 2026 | Oneiro Paris",
            "desc": "Où en sont vraiment les prix du diamant de laboratoire en 2026, pourquoi l'écart avec le naturel s'est stabilisé autour de 35-40 %, et comment en profiter sans se tromper.",
        },
        "en": {
            "slug": "lab-grown-diamond-prices-2026",
            "cat": "News — Diamonds",
            "card": "Lab-grown diamonds: where prices stand in 2026",
            "teaser": "Prices keep falling, the gap with natural has settled. What that means for a real budget.",
            "title": "Lab-grown diamond prices in 2026 | Oneiro Paris",
            "desc": "Where lab-grown diamond prices really stand in 2026, why the gap with natural stones has settled around 35-40 %, and how to take advantage of it wisely.",
        },
    },

    "tendances-fiancailles-2026": {
        "date": "2026-09-02", "section": "actu",
        "image": ONE + "731519C5-8E00-4E53-9C7A-A9F6A102A08C.jpg",
        "products": ["iris", "sofia", "mia", "daphne"],
        "fr": {
            "slug": "tendances-bague-de-fiancailles-2026",
            "cat": "Actualité — Tendances",
            "card": "Tendances fiançailles 2026 : ce qu'on nous demande vraiment",
            "teaser": "Poire à l'horizontale, serti clos, toi & moi, pierres de couleur : ce qui monte, vu de l'atelier.",
            "title": "Tendances bague de fiançailles 2026 | Oneiro Paris",
            "desc": "Les formes, les sertis et les couleurs qui reviennent en 2026, vus depuis l'atelier — et comment distinguer une tendance qui tiendra d'un effet de mode.",
        },
        "en": {
            "slug": "engagement-ring-trends-2026",
            "cat": "News — Trends",
            "card": "Engagement ring trends 2026: what people actually ask for",
            "teaser": "East-west pears, bezel settings, toi & moi, coloured stones: what is rising, seen from the bench.",
            "title": "Engagement ring trends 2026 | Oneiro Paris",
            "desc": "The shapes, settings and colours coming back in 2026, seen from the workshop — and how to tell a trend that will last from a passing fashion.",
        },
    },

    "se-fiancer-pendant-les-fetes": {
        "date": "2026-08-26", "section": "actu",
        "image": ONE + "IMG_5540.jpg",
        "products": ["bague-3", "bague-1", "ami"],
        "fr": {
            "slug": "demande-en-mariage-fetes-de-fin-d-annee",
            "cat": "Actualité — Calendrier",
            "card": "Demande à Noël ou au Nouvel An : le calendrier à tenir",
            "teaser": "Une bague sur-mesure demande 2 à 7 semaines. Voici la date limite pour ne pas courir.",
            "title": "Se fiancer pendant les fêtes : le rétroplanning | Oneiro",
            "desc": "Demande prévue à Noël ou au Nouvel An ? Le rétroplanning réaliste d'une bague sur-mesure, les dates limites, et ce qui reste faisable si vous vous y prenez tard.",
        },
        "en": {
            "slug": "proposing-over-the-holidays",
            "cat": "News — Timing",
            "card": "Proposing at Christmas or New Year: the timeline to hold",
            "teaser": "A bespoke ring takes 2 to 7 weeks. Here is the cut-off date, so you are not rushing.",
            "title": "Proposing over the holidays: the timeline | Oneiro",
            "desc": "Planning a proposal at Christmas or New Year? The realistic timeline for a bespoke ring, the cut-off dates, and what is still possible if you start late.",
        },
    },

    "bagues-de-stars-2026": {
        "date": "2026-09-22", "section": "actu",
        "image": ONE + "Bague_Mia.jpg",
        "products": ["sofia", "kyra", "selena", "iris", "bague-3", "mia"],
        "fr": {
            "slug": "bagues-de-fiancailles-des-stars-2026",
            "cat": "Actualité — Tendances",
            "card": "Les bagues de fiançailles des stars en 2026",
            "teaser": "Kravitz, Sabalenka, Sienna Miller : ce que leurs bagues disent vraiment, et ce que ça coûte.",
            "title": "Bagues de fiançailles des stars en 2026 | Oneiro Paris",
            "desc": "Zoë Kravitz, Aryna Sabalenka, Halle Berry, Sienna Miller, Madison Beer : les bagues de fiançailles marquantes de 2026 décryptées forme par forme, avec les prix réels et leurs équivalents accessibles.",
        },
        "en": {
            "slug": "celebrity-engagement-rings-2026",
            "cat": "News — Trends",
            "card": "The celebrity engagement rings of 2026",
            "teaser": "Kravitz, Sabalenka, Sienna Miller: what their rings actually say, and what it costs.",
            "title": "Celebrity engagement rings in 2026 | Oneiro Paris",
            "desc": "Zoë Kravitz, Aryna Sabalenka, Halle Berry, Sienna Miller, Madison Beer: the engagement rings that defined 2026, decoded shape by shape, with real prices and their attainable equivalents.",
        },
    },

    # --------------------------------------------------------------- GUIDES --
    "diamant-naturel-ou-laboratoire": {
        "date": "2026-06-12", "section": "guide",
        "image": ONE + "9E02A374-D8BD-48A7-9834-DC248A59479C.jpg",
        "products": ["ami", "kyra", "selena", "bague-3"],
        "fr": {
            "slug": "diamant-naturel-ou-laboratoire",
            "cat": "Guide — Diamants",
            "card": "Diamant naturel ou de laboratoire : le comparatif honnête",
            "teaser": "Prix, éthique, revente — ce que personne ne vous dit clairement.",
            "title": "Diamant naturel ou de laboratoire : le comparatif | Oneiro",
            "desc": "Mêmes pierres, deux histoires : 35-40 % d'écart de prix, nuances éthiques, valeur de revente. Le comparatif sans parti pris pour choisir en connaissance de cause.",
        },
        "en": {
            "slug": "natural-vs-lab-grown-diamond",
            "cat": "Guide — Diamonds",
            "card": "Natural or lab-grown diamond: the honest comparison",
            "teaser": "Price, ethics, resale — what nobody tells you plainly.",
            "title": "Natural or lab-grown diamond: the comparison | Oneiro",
            "desc": "Same stones, two stories: a 35-40 % price gap, ethical nuances, resale value. The unbiased comparison, so you can choose knowing exactly what you are choosing.",
        },
    },

    "comment-choisir-un-diamant-4c": {
        "date": "2026-06-12", "section": "guide",
        "image": ONE + "IMG_5540.jpg",
        "products": ["kyra", "bague-4", "sofia"],
        "fr": {
            "slug": "comment-choisir-un-diamant-4c",
            "cat": "Guide — Achat",
            "card": "Comment choisir un diamant : les 4C sans jargon",
            "teaser": "Carat, couleur, pureté, taille — et les astuces pour payer juste.",
            "title": "Comment choisir un diamant : le guide des 4C | Oneiro",
            "desc": "Carat, Cut, Color, Clarity : ce que chaque critère change vraiment, l'ordre de priorité pour arbitrer, et les astuces pour payer le juste prix d'un diamant certifié.",
        },
        "en": {
            "slug": "how-to-choose-a-diamond-4cs",
            "cat": "Guide — Buying",
            "card": "How to choose a diamond: the 4Cs without the jargon",
            "teaser": "Carat, colour, clarity, cut — and how to pay the right price.",
            "title": "How to choose a diamond: the 4Cs guide | Oneiro",
            "desc": "Carat, cut, colour, clarity: what each criterion really changes, the order of priority for trade-offs, and how to pay the right price for a certified diamond.",
        },
    },

    "prix-bague-fiancailles-ethique": {
        "date": "2026-06-12", "section": "guide",
        "image": ONE + "IMG_1941.jpg",
        "products": ["ami", "bague-4", "bague-8", "daphne"],
        "fr": {
            "slug": "prix-bague-fiancailles-ethique",
            "cat": "Guide — Budget",
            "card": "Bague de fiançailles éthique : combien ça coûte vraiment ?",
            "teaser": "Fourchettes réalistes, ce qui fait varier le prix, et où va votre argent.",
            "title": "Prix d'une bague de fiançailles éthique en 2026 | Oneiro",
            "desc": "Fourchettes réalistes (1 000 à 7 000 €), ce qui fait varier le prix, où va votre argent — et pourquoi l'éthique ne devrait jamais être facturée en supplément.",
        },
        "en": {
            "slug": "ethical-engagement-ring-price",
            "cat": "Guide — Budget",
            "card": "Ethical engagement ring: what does it really cost?",
            "teaser": "Realistic ranges, what moves the price, and where your money goes.",
            "title": "The price of an ethical engagement ring in 2026 | Oneiro",
            "desc": "Realistic ranges (€1,000 to €7,000), what moves the price, where your money goes — and why ethics should never be charged as an extra.",
        },
    },

    "formes-de-diamant": {
        "date": "2026-07-08", "section": "guide",
        "image": ONE + "Photoroom_20250310_204856.jpg",
        "products": ["kyra", "iris", "sofia", "selena", "bague-3", "bague-4"],
        "fr": {
            "slug": "formes-de-diamant-guide",
            "cat": "Guide — Diamants",
            "card": "Les formes de diamant, et ce que chacune change au doigt",
            "teaser": "Ovale, poire, émeraude, coussin, marquise : taille apparente, prix, entretien.",
            "title": "Formes de diamant : le guide complet | Oneiro Paris",
            "desc": "Rond, ovale, poire, émeraude, coussin, marquise, Asscher, radiant : ce que chaque forme change à la taille apparente, au prix et au porter quotidien.",
        },
        "en": {
            "slug": "diamond-shapes-guide",
            "cat": "Guide — Diamonds",
            "card": "Diamond shapes, and what each one changes on the finger",
            "teaser": "Oval, pear, emerald, cushion, marquise: apparent size, price, everyday wear.",
            "title": "Diamond shapes: the complete guide | Oneiro Paris",
            "desc": "Round, oval, pear, emerald, cushion, marquise, Asscher, radiant: what each shape changes in apparent size, in price and in everyday wear.",
        },
    },

    "taille-de-bague": {
        "date": "2026-07-22", "section": "guide",
        "image": ONE + "Photoroom_20250425_145931.jpg",
        "products": ["bague-1", "bague-4", "bague-8"],
        "fr": {
            "slug": "trouver-sa-taille-de-bague",
            "cat": "Guide — Pratique",
            "card": "Trouver la bonne taille de bague (sans vendre la mèche)",
            "teaser": "Les quatre méthodes qui marchent, celles qui trompent, et la marge de rattrapage.",
            "title": "Taille de bague : la trouver sans se tromper | Oneiro",
            "desc": "Mesurer un doigt sans éveiller les soupçons : les quatre méthodes fiables, les pièges classiques, les correspondances FR/US, et ce qui reste rattrapable après coup.",
        },
        "en": {
            "slug": "find-your-ring-size",
            "cat": "Guide — Practical",
            "card": "Finding the right ring size (without giving the game away)",
            "teaser": "The four methods that work, the ones that mislead, and the margin to fix it later.",
            "title": "Ring size: getting it right first time | Oneiro",
            "desc": "Measuring a finger without raising suspicion: the four reliable methods, the classic traps, the FR/US/UK conversions, and what can still be fixed afterwards.",
        },
    },

    "choisir-son-alliance": {
        "date": "2026-08-05", "section": "guide",
        "image": ONE + "Photoroom_20250612_230000.jpg",
        "products": ["bracelet-tennis-en-diamants", "bague-2", "bague-1"],
        "fr": {
            "slug": "alliance-epuree-pavee-ou-bandeau-infini",
            "cat": "Guide — Mariage",
            "card": "Alliance épurée, pavée ou bandeau infini : comment choisir",
            "teaser": "Trois familles, trois budgets, trois contraintes d'entretien — et l'empilage avec la bague.",
            "title": "Alliance : épurée, pavée ou bandeau infini | Oneiro Paris",
            "desc": "Anneau épuré, demi-tour pavé ou bandeau infini serti sur tout le tour : ce qui les sépare vraiment en prix, en confort, en entretien et en accord avec la bague de fiançailles.",
        },
        "en": {
            "slug": "plain-pave-or-full-eternity-band",
            "cat": "Guide — Wedding",
            "card": "Plain, pavé or full eternity band: how to choose",
            "teaser": "Three families, three budgets, three maintenance realities — and the stack with the ring.",
            "title": "Wedding bands: plain, pavé or full eternity | Oneiro Paris",
            "desc": "A plain band, a half-eternity pavé or a full eternity band set all the way round: what really separates them in price, comfort, upkeep and fit with the engagement ring.",
        },
    },

    "quelle-main-quel-doigt": {
        "date": "2026-08-19", "section": "guide",
        "image": ONE + "Photoroom_20250425_145200.jpg",
        "products": ["bague", "lena", "collier"],
        "fr": {
            "slug": "quelle-main-quel-doigt-bague-de-fiancailles",
            "cat": "Guide — Coutumes",
            "card": "Quelle main, quel doigt : les coutumes expliquées",
            "teaser": "Pourquoi la France porte à gauche, l'Allemagne à droite, et ce qu'on fait le jour du mariage.",
            "title": "Bague de fiançailles : quelle main, quel doigt ? | Oneiro",
            "desc": "Main gauche ou droite, annulaire ou autre doigt, ordre des anneaux le jour du mariage, gravure : les coutumes pays par pays, et la seule règle qui compte vraiment.",
        },
        "en": {
            "slug": "which-hand-which-finger",
            "cat": "Guide — Customs",
            "card": "Which hand, which finger: the customs explained",
            "teaser": "Why France wears it on the left, Germany on the right, and what happens on the wedding day.",
            "title": "Engagement ring: which hand, which finger? | Oneiro",
            "desc": "Left hand or right, ring finger or another, the order of the bands on the wedding day, engraving: the customs country by country, and the only rule that really matters.",
        },
    },

    "entretien-bijoux": {
        "date": "2026-09-01", "section": "guide",
        "image": ONE + "CA012D99-4A08-46BA-AA52-96069C7FF785.jpg",
        "products": ["bracelet-tennis-en-diamants", "creole-en-diamants", "pendentif-personnalisable"],
        "fr": {
            "slug": "entretenir-ses-bijoux-or-et-diamants",
            "cat": "Guide — Entretien",
            "card": "Entretenir son or et ses diamants : le guide simple",
            "teaser": "Cinq minutes par mois, trois gestes à éviter, et quand faire vérifier le sertissage.",
            "title": "Entretenir ses bijoux en or et diamants | Oneiro Paris",
            "desc": "Nettoyer un diamant chez soi sans l'abîmer, ce qu'il ne faut jamais faire, à quel rythme faire vérifier les griffes, et comment ranger ses pièces pour qu'elles durent.",
        },
        "en": {
            "slug": "caring-for-gold-and-diamond-jewellery",
            "cat": "Guide — Care",
            "card": "Caring for gold and diamonds: the simple guide",
            "teaser": "Five minutes a month, three things never to do, and when to have the setting checked.",
            "title": "Caring for gold and diamond jewellery | Oneiro Paris",
            "desc": "Cleaning a diamond at home without damaging it, what you should never do, how often to have the claws checked, and how to store your pieces so they last.",
        },
    },
}

# Libelles des deux sections du Journal
JOURNAL_SECTIONS = {
    "fr": {
        "actu": ("Actualités", "Ce qui bouge en ce moment",
                 "Prix des matières, tendances, calendrier : les sujets datés, revus régulièrement. Utiles maintenant, pas dans trois ans."),
        "guide": ("Guides intemporels", "Ce qui reste vrai",
                  "La colonne vertébrale du Journal : comprendre les pierres, les formes, les tailles et les coutumes. Écrit une fois, corrigé quand il le faut."),
    },
    "en": {
        "actu": ("News", "What is moving right now",
                 "Material prices, trends, timing: the dated subjects, reviewed regularly. Useful now, not in three years."),
        "guide": ("Timeless guides", "What stays true",
                  "The backbone of the Journal: understanding the stones, the shapes, the sizes and the customs. Written once, corrected when it needs to be."),
    },
}
