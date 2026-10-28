# Déploiement du site Oneiro — Cloudflare Tunnel

Le site est 100 % statique (`../site`). Il se sert depuis n'importe quelle machine
(votre serveur maison, un PC qui reste allumé) et s'expose sur votre nom de domaine
via un Cloudflare Tunnel — sans ouvrir de port sur votre box, sans IP fixe.

Le domaine n'est pas encore choisi : toutes les étapes ci-dessous marchent avec
n'importe quel domaine géré par Cloudflare. Notez juste que **tant que
oneiroparis.com pointe vers Shopify, le site actuel reste en ligne** — vous pouvez
préparer le tunnel sur un sous-domaine de test (ex. `preview.votredomaine.com`)
puis basculer le domaine principal le jour J.

---

## Option A — Docker (recommandé)

### 1. Préparer le domaine chez Cloudflare
1. Créez un compte sur https://dash.cloudflare.com (gratuit).
2. « Add a site » → votre domaine → plan Free.
3. Chez votre registrar (OVH, Gandi…), remplacez les serveurs DNS par ceux
   indiqués par Cloudflare. (Si le domaine est déjà chez Cloudflare, rien à faire.)

### 2. Créer le tunnel
1. Dans le dashboard : **Zero Trust → Networks → Tunnels → Create a tunnel**.
2. Type « Cloudflared », donnez-lui un nom (ex. `oneiro-site`).
3. Copiez le **token** affiché (longue chaîne commençant par `eyJ…`).
4. Dans ce dossier : copiez `.env.example` vers `.env` et collez le token.

### 3. Déclarer le nom d'hôte public
Toujours dans la config du tunnel, onglet **Public Hostnames → Add** :
- Subdomain/Domain : ce que vous voulez (ex. `preview` + `votredomaine.com`,
  ou vide + `oneiroparis.com` pour le jour de la bascule)
- Service : **HTTP** → `web:80`  ← (nom du conteneur nginx du docker-compose)

### 4. Lancer
```bash
cd deploy
docker compose up -d
```
C'est en ligne. Vérifiez sur votre nom d'hôte. Les mises à jour du site sont
instantanées (le dossier `site/` est monté en direct) ; après modification des
fichiers `_build/`, relancez `python3 _build/build.py`.

Pour tester en local sans tunnel : décommentez les lignes `ports` du
docker-compose puis ouvrez http://localhost:8080.

---

## Option B — Sans Docker (cloudflared seul)

1. Installez cloudflared : https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
2. Servez le dossier `site/` avec n'importe quoi (IIS, nginx, ou pour tester :
   `python -m http.server 8080` dans le dossier `site/`).
3. Créez le tunnel comme en Option A, puis :
   ```bash
   cloudflared service install <TOKEN>
   ```
   et pointez le Public Hostname vers `http://localhost:8080`.

---

## Le jour de la bascule (quand vous quitterez Shopify)

1. Ajoutez un Public Hostname `oneiroparis.com` (et `www`) sur le tunnel.
2. Dans Cloudflare DNS, supprimez les enregistrements qui pointent vers Shopify.
3. Gardez Shopify actif en parallèle quelques semaines si vous voulez conserver
   le checkout (le site renvoie vers les fiches Shopify si vous activez
   `shopify.enabled` dans `site/assets/js/config.js`).

## Email professionnel (recommandé avant la mise en ligne)

Le site affiche `contact@oneiroparis.com` (configurable dans
`site/assets/js/config.js`). Pour créer cette adresse gratuitement :
Cloudflare → votre domaine → **Email → Email Routing** → créer l'adresse et la
rediriger vers votre Gmail. Pour pouvoir *répondre* depuis cette adresse,
ajoutez-la ensuite dans Gmail (Paramètres → Comptes → « Envoyer des emails en
tant que »).

---

## Check-list avant mise en ligne publique

- [ ] `config.js` : email de contact réel, numéro WhatsApp (ou laisser vide)
- [ ] Mentions légales : capital social, RCS, TVA, directeur de publication, hébergeur
- [ ] CGV : désigner un médiateur de la consommation ; faire relire rétractation/retours par un conseil
- [ ] Remplacer les images hotlinkées du CDN Shopify par des copies locales
      (dossier `site/assets/img/` — voir `site/README.md`) **avant** de fermer Shopify
- [ ] Quand prêts : activer `shopify` / `nivoda` / `calendly` dans `config.js`
- [ ] Si le domaine final n'est pas oneiroparis.com : ajuster `SITE_URL` dans
      `site/_build/build.py` et relancer le build (canonical + sitemap)
- [ ] Dès la mise en ligne : créer la propriété dans Google Search Console et
      soumettre `https://votredomaine/sitemap.xml` ; créer la fiche Google
      Business Profile
- [ ] Tester sur mobile
