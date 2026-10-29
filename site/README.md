# Site Oneiro Paris — refonte (juin 2026), version bilingue (septembre 2026)

Site statique multi-pages, **bilingue français / anglais**, sans dépendance serveur.
Ouvrez `index.html` dans un navigateur pour le voir immédiatement.
Le français vit à la racine, l'anglais sous `en/`.

## Ce qui a changé par rapport au site Shopify actuel

- **Nouveau message** : « le sur-mesure d'exception, accessible et accompagné » —
  l'éthique devient un standard de production, plus l'argument principal.
- **Pure player assumé** : l'absence de boutique est un argument de vente
  (accueil, à-propos), pas une chose qu'on cache.
- **Split d'activité** : La Maison (sur-mesure + collection, émotionnel) /
  Oneiro Diamants (transactionnel, page dédiée à l'univers sombre distinct).
- **Hero refait** : titre fort, promesse claire, double CTA, barre de réassurance.
- **Confiance renforcée** : certificats GIA/IGI mis en avant, page Garanties
  complète, mentions légales étoffées,
  plus de Gmail public, plus de « propulsé par Shopify », plus de prix à 0 €.
- **Données conservées** : les 22 produits (prix, variantes naturel/labo, photos),
  délais 2-7 semaines, politiques de retour/livraison réelles, SIRET.

## Structure

| Fichier | Rôle |
|---|---|
| `index.html` | Accueil — hero, modèle pure player, split Maison/Diamants, parcours, confiance |
| `sur-mesure.html` | Parcours sur-mesure (fiançailles, alliance, pièce unique) |
| `collection.html` | Catalogue filtrable (généré depuis `products-data.js`) |
| `produits/<handle>.html` | **22 fiches produit statiques** (SEO : contenu indexable + JSON-LD Product), hydratées en interactif par JS |
| `produit.html?p=<handle>` | Ancienne version dynamique, conservée en fallback (exclue du sitemap) |
| `bague-de-fiancailles.html` | Landing SEO « bague de fiançailles sur-mesure éthique » |
| `alliance.html` | Landing SEO « alliance sur-mesure or 18 carats » |
| `journal.html` + `journal/<slug>.html` | Le Journal — 12 articles en deux sections (actualités / guides intemporels), voir plus bas |
| `diamants.html` | Section Oneiro Diamants — emplacement Nivoda + guide 4C + devis |
| `sitemap.xml` / `robots.txt` | Générés par le build (98 URL, FR + EN avec alternates `hreflang`) — à soumettre dans Google Search Console |
| `a-propos.html` | Histoire, atelier, engagements (anonyme pour l'instant) |
| `garanties.html` | Livraison, retours, garantie, certificats, paiement, FAQ |
| `rendez-vous.html` | Prise de RDV (emplacement Calendly + formulaire email) |
| `contact.html` | Contact (email, WhatsApp, formulaire) |
| `mentions-legales.html` / `cgv.html` / `confidentialite.html` | Légal |
| `en/…` | **Version anglaise complète** : mêmes pages, slugs traduits (voir table ci-dessous), fiches produit sous `en/products/`, articles sous `en/journal/` |

## Version anglaise

L'anglais est généré par le même build, depuis `_build/pages-en/` et
`_build/articles-en/`. Chaque page FR a exactement une page EN, reliées par des
balises `hreflang` réciproques et par le sélecteur **FR / EN** du header (et du
pied de page). Le sélecteur pointe toujours vers la page équivalente, pas vers
l'accueil.

| FR | EN |
|---|---|
| `/` | `/en/` |
| `sur-mesure.html` | `en/custom-made.html` |
| `bague-de-fiancailles.html` | `en/engagement-rings.html` |
| `alliance.html` | `en/wedding-bands.html` |
| `collection.html` | `en/collection.html` |
| `diamants.html` | `en/diamonds.html` |
| `journal.html` | `en/journal.html` |
| `a-propos.html` | `en/about.html` |
| `garanties.html` | `en/guarantees.html` |
| `avis.html` | `en/reviews.html` |
| `selection.html` | `en/wishlist.html` |
| `rendez-vous.html` | `en/book-appointment.html` |
| `contact.html` | `en/contact.html` |
| `produits/<handle>.html` | `en/products/<handle>.html` |
| `mentions-legales.html` / `cgv.html` / `confidentialite.html` | `en/legal-notice.html` / `en/terms.html` / `en/privacy.html` |

Les *handles* produit restent identiques dans les deux langues : une sélection
partagée par lien (`?s=…`) fonctionne donc d'une langue à l'autre.

Le JavaScript se traduit tout seul : `app.js` et `product-page.js` lisent
`<html lang="…">` et basculent leurs libellés, le format de prix (`3 300 €`
contre `€3,300`) et le dossier des fiches produit. Les titres et descriptions
anglais des 22 produits vivent dans **`_build/products-en.json`** ; le build en
tire `assets/js/products-en.js`, chargé uniquement par les pages `/en/`.

Les pages légales anglaises portent une mention indiquant que la version
française fait foi.

**Pour modifier un texte anglais** : éditez le fichier correspondant dans
`_build/pages-en/` (ou `_build/articles-en/`, ou `_build/products-en.json` pour
les fiches produit), puis relancez `python3 _build/build.py`. Les titres et
meta-descriptions des deux langues sont dans les dictionnaires `META` et
`ARTICLE_META` en tête de `build.py`.

## Le Journal

Le Journal compte **12 articles par langue**, répartis en deux sections&nbsp;:

- **Actualités** — sujets datés, à relire régulièrement&nbsp;: prix de l'or, prix du
  diamant de laboratoire, tendances de la saison, rétroplanning des fêtes.
- **Guides intemporels** — la colonne vertébrale SEO&nbsp;: 4C, naturel vs laboratoire,
  budget, formes de diamant, taille de bague, alliances, coutumes, entretien.

Tout est piloté par **`_build/_articles_registry.py`**, un seul fichier qui
contient, pour chaque article&nbsp;: la date, la section, le visuel de la carte, les
**handles des pièces dont l'article parle**, et — pour chaque langue — le slug, le
titre SEO, la meta-description, le libellé de catégorie, le titre de carte et
l'accroche.

À partir de ce registre, `build.py` génère automatiquement&nbsp;:

1. les **cartes des deux grilles** de `journal.html` (les balises
   `<div class="grid grid--3" id="journal-actu">` et `id="journal-guide">` des
   sources sont remplies au build, triées par date décroissante)&nbsp;;
2. le bloc **« Les pièces dont on parle »** en bas de chaque article, avec les
   vraies fiches produit et leurs prix&nbsp;;
3. le bloc **« À lire ensuite »** (3 articles, même section d'abord)&nbsp;;
4. le **bandeau d'appel final**, identique pour tous les articles&nbsp;;
5. le JSON-LD `Article` (image, `articleSection`, dates) et la priorité de
   sitemap (les guides pèsent plus que les actualités).

**Ajouter un article** : une entrée dans `_articles_registry.py` + le fichier
source `_build/articles/<slug-fr>.html` et `_build/articles-en/<slug-en>.html`.
Le corps de l'article ne contient que la prose — pas de bandeau final, pas de
grille produit&nbsp;: le build les ajoute.

**Liens contextuels** : dans le corps d'un article, les liens vers les fiches
produit s'écrivent `produits/<handle>.html` en français et `products/<handle>.html`
en anglais (les pages du Journal posent un `<base href="../">`). Quand un article
parle d'un type de pièce, il pointe vers la pièce correspondante — par exemple le
guide des alliances renvoie au bracelet tennis pour l'esprit « serti sur tout le
tour », faute de bandeau infini au catalogue pour l'instant.

## Rendez-vous et inspirations

- Le formulaire de `rendez-vous.html` demande le **format du rendez-vous**
  (visio ou en personne à Paris). Le choix part dans l'objet et le corps de
  l'email pré-rempli. Le lieu exact d'un rendez-vous en personne se convient par
  email&nbsp;: une note apparaît sous le champ quand l'option est sélectionnée.
- Les pages `rendez-vous.html` et `contact.html` portent un bloc
  **« Vos inspirations »** (ancre `#inspirations`) avec deux boutons&nbsp;: un email
  pré-rempli prêt à recevoir les pièces jointes, et WhatsApp (masqué tant que
  `whatsappNumber` est vide dans `config.js`). Le site étant statique, il n'y a
  pas d'upload serveur&nbsp;: c'est volontaire, et annoncé clairement au visiteur.

## Carrousel du hero

L'accueil (FR et EN) affiche un carrousel de 5 visuels en fondu enchaîné au lieu
d'une image fixe. Le markup se trouve dans `_build/pages/index.html` et
`_build/pages-en/index.html` :

```html
<div class="hero__carousel" data-hero-carousel data-interval="6000">
  <div class="hero__slide is-active" style="background-image:url('…')"></div>
  <div class="hero__slide" style="background-image:url('…')"></div>
  …
</div>
```

Pour changer les photos : remplacez les URL, dans le même ordre, dans les deux
fichiers, puis relancez le build. `data-interval` règle la durée d'affichage en
millisecondes. Les puces de navigation sont ajoutées par `app.js`
(`O.heroCarousel`), qui précharge les images, met le défilement en pause au
survol et quand l'onglet est en arrière-plan, gère le balayage tactile et
respecte `prefers-reduced-motion`. Sans JavaScript, la première diapositive
(`is-active`) reste affichée : le hero ne dépend pas du script pour exister.

## Fichiers à connaître

- **`assets/js/config.js`** — LE fichier de branchement : email, WhatsApp,
  Shopify (achat en ligne), Nivoda (sélecteur diamants), Calendly (RDV), avis clients.
  Tout est livré désactivé avec des solutions de repli propres (email pré-rempli).
- **`assets/js/products-data.js`** — le catalogue (22 produits extraits du site
  actuel, prix à 0 € corrigés, fautes corrigées). Pour modifier un prix ou un
  texte produit, c'est ici.
- **`_build/`** — sources des pages (`pages/`, `pages-en/`, `articles/`,
  `articles-en/`) et templates partagés (`head.tpl`, `header.html`,
  `footer.html`, communs aux deux langues : les libellés y sont des jetons
  `{{…}}` remplis par le dictionnaire `CHROME` de `build.py`). Pour toute
  modification : éditez la source puis exécutez `python3 _build/build.py` —
  régénère les 104 pages des deux langues, le sitemap.xml (avec les alternates
  `hreflang`), le robots.txt, les balises canonical et les données structurées
  schema.org (Organization, Product, Article, BreadcrumbList, FAQ). La variable
  `SITE_URL` en tête de `build.py` définit le domaine canonique : à ajuster si
  vous choisissez un autre domaine que oneiroparis.com. Pour ajouter un article :
  voir la section « Le Journal » ci-dessus.
- **`_source/policies.md`** — textes légaux du site actuel (référence).

## Images

Les images sont actuellement **hotlinkées depuis le CDN Shopify** (le site actuel).
Ça marche tant que la boutique Shopify existe. Avant de fermer Shopify :
téléchargez les photos (clic droit → enregistrer, ou export Shopify), placez-les
dans `assets/img/` et remplacez les URL dans `products-data.js`, `_build/` et
régénérez. Liste des URL utilisées : chercher `cdn.shopify.com` et `oneiroparis.com/cdn`.

## Contenus volontairement en attente

- **Fondateurs anonymes** : le storytelling incarné (visages, prénoms, vidéo)
  est prévu par la stratégie mais laissé neutre à votre demande. Les pages
  À propos / Accueil l'accueilleront sans refonte le jour venu.
- **Avis clients** : aucun faux avis. La section s'activera via `config.js`
  quand vous aurez de vrais avis.
- **Blog / Journal** : 12 articles en ligne dans les deux langues. Les articles
  de la section Actualités sont datés et doivent être relus une à deux fois par
  an (prix, tendances, dates limites des fêtes).

## Déploiement

Voir `../deploy/README-DEPLOIEMENT.md` (Cloudflare Tunnel, domaine à brancher plus tard).
