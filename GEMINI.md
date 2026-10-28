# Contexte du projet pour l'assistant (Gemini ou autre)

Ce fichier remplace la mémoire de projet : lis-le en entier avant de modifier
quoi que ce soit.

## Le projet

Site de **Oneiro Paris**, joaillerie sur-mesure et diamants certifiés, maison
parisienne 100 % en ligne. Site **statique bilingue** : français à la racine,
anglais sous `site/en/`. Hébergé sur un home server (Docker, nginx, Cloudflare
Tunnel).

## Règles de travail (préférences du propriétaire)

- Langage : **Python** pour tout script ou outil.
- Donner des **blocs de code complets**, jamais des morceaux à replacer.
- **Jamais de tirets longs** (le caractère em dash ou en dash) dans les textes,
  le code et les commentaires. Utiliser une virgule, deux points ou un tiret court.
- Chaînes françaises dans le JavaScript : écrire les accents en échappements
  Unicode (`é`), sinon ils se perdent au transfert vers Windows.
- Procéder étape par étape, avec une confirmation brève entre les étapes.
- Les commandes shell ou PowerShell se donnent directement dans la réponse.
- Sobriété graphique : pas d'habillage décoratif superflu.

## Architecture

- **Les pages HTML de `site/` sont générées. Ne jamais les éditer à la main.**
  Éditer les sources dans `site/_build/` puis lancer `python site/_build/build.py`.
- `_build/build.py` génère FR et EN en un passage (environ 104 pages) et produit
  `sitemap.xml` et `robots.txt`. Les dictionnaires `SLUGS`, `META`, `CHROME`,
  `CAT`, `PSTR`, `JSTR`, `OPTION_TR` en tête du fichier contiennent tout le texte
  d'interface des deux langues.
- Sources : `_build/pages/` et `_build/articles/` (FR), `_build/pages-en/` et
  `_build/articles-en/` (EN). `head.tpl`, `header.html`, `footer.html` sont
  communs, les libellés y sont des jetons `{{...}}`.
- Fiches produit : 22 produits dans `assets/js/products-data.js` (FR) et
  `_build/products-en.json` (titres et descriptions EN). Les handles produit sont
  **identiques dans les deux langues** (volontaire : les liens de sélection `?s=`
  doivent marcher d'une langue à l'autre). Ne pas les traduire.
- `OPTION_TR` (dans `build.py`) et `OPT` (dans `assets/js/product-page.js`)
  doivent rester **synchronisées**.
- Le Journal (13 articles par langue) est piloté par
  `_build/_articles_registry.py`. Ajouter un article = une entrée dans le registre
  plus un fichier source par langue. Le corps d'un article ne contient que de la
  prose : le build ajoute cartes, bloc "pièces dont on parle", "à lire ensuite",
  bandeau final et JSON-LD.
- Les chemins d'assets dans `head.tpl` sont **absolus** (`/assets/...`).
- Réglages centraux (contact, société, services branchés) dans
  `site/assets/js/config.js`.

## Configurateur de diamant

`site/assets/js/configurator.js` appelle une API externe (`pricer.apiUrl` dans
`config.js`). Cette API et le modèle de prix ne sont **pas** dans ce dépôt. Si
l'API ne répond pas, la page Diamants retombe silencieusement sur du contenu de
repli : ne jamais casser ce comportement. Initialiser les compteurs à 0
(`this._token = 0`), sinon `NaN !== NaN` rejette toutes les réponses.

## Pièges connus

- **Avant de lancer `build.py`**, vérifier que les fichiers sources édités sont
  complets (présence de `</html>`, `</header>`, taille cohérente). Un build sur
  des sources tronquées produit des pages HTML invalides sur tout le site.
  **Après** le build, vérifier que toutes les pages générées se terminent par
  `</body></html>`.
- `deploy/nginx.conf` : le bloc `location /en/` a son propre `error_page 404`.
  Ne jamais y ajouter de `add_header` (cela annulerait ceux du bloc `server`).
- Le header tient à peine dans 1200 px depuis le sélecteur FR/EN : une entrée de
  nav en plus oblige à resserrer `.nav { gap }` ou les libellés.
- Les cartes générées (Journal, produits) n'ont volontairement pas la classe
  `reveal`, qui masque tant que le JS n'a pas tourné.
- Vérifier le rendu en **390 px** et pas seulement en 1280 px.
- Les textes anglais des pages légales portent une mention : la version française
  fait foi.
- Ne jamais commiter `deploy/.env` (token du tunnel Cloudflare).
- Ne jamais afficher d'adresse Gmail publique : le contact passe par
  `contact@oneiroparis.com`.
- Contenu éditorial : aucun avis ni citation inventés, aucun lien suggéré entre
  la marque et des personnes citées.
