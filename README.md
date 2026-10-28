# Oneiro Paris

Site vitrine de la maison de joaillerie Oneiro Paris : site statique bilingue
(français à la racine, anglais sous `site/en/`), sans dépendance serveur.

## Contenu du dépôt

| Dossier | Rôle |
|---|---|
| `site/` | Le site : pages HTML générées, CSS, JavaScript, images |
| `site/_build/` | Sources et générateur (`build.py`) qui produit les pages FR et EN |
| `deploy/` | Hébergement : nginx + Cloudflare Tunnel via Docker Compose |
| `favicon/` | Icônes et manifeste |

Le modèle de prix des diamants et son API ne font pas partie de ce dépôt.

## Voir le site en local

```bash
cd site
python -m http.server 8080
```

Puis ouvrir http://localhost:8080

## Modifier le site

Les pages à la racine de `site/` sont **générées**. On édite les sources dans
`site/_build/` puis on relance le build :

```bash
cd site/_build
python build.py
```

Voir `GEMINI.md` pour l'architecture détaillée et les règles de travail.

## Déploiement

Voir `deploy/README-DEPLOIEMENT.md`. Le fichier `deploy/.env` (token du tunnel
Cloudflare) n'est jamais versionné : copier `deploy/.env.example`.
