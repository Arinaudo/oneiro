#!/usr/bin/env python3
"""Journal Oneiro : veille et brouillons d'articles sur les fiançailles de célébrités.

Principe : l'outil lit l'actualité, rédige un brouillon FR + EN À PARTIR DES SEULES
SOURCES RÉCUPÉRÉES (jamais de mémoire du modèle), vérifie le brouillon, puis le
publie dans le registre du Journal et relance build.py.

Commandes (depuis la racine du projet) :
    python site/_build/journal_auto.py scan                     liste l'actualité récente
    python site/_build/journal_auto.py draft --pick 1,3         brouillon depuis des résultats du scan
    python site/_build/journal_auto.py draft --url URL1 --url URL2 --topic "Charles Leclerc, mariage"
    python site/_build/journal_auto.py draft --query "Charles Leclerc mariage bague"
    python site/_build/journal_auto.py auto                     scan + meilleur sujet + brouillon
    python site/_build/journal_auto.py auto --publish            idem, publie si TOUS les contrôles passent
    python site/_build/journal_auto.py list                     brouillons en attente
    python site/_build/journal_auto.py publish CLE               publie un brouillon relu

Configuration (variables d'environnement, ou fichier journal.env à la racine du projet,
jamais versionné) :
    ONEIRO_LLM=gemini | anthropic      (défaut : gemini)
    GEMINI_API_KEY=...   ou   ANTHROPIC_API_KEY=...
    ONEIRO_LLM_MODEL=...               (facultatif, remplace le modèle par défaut)

Aucune dépendance : bibliothèque standard uniquement.
"""
import argparse, datetime, email.utils, html, json, math, os, re, shutil, subprocess, sys
import urllib.parse, urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))           # site/_build
PROJECT = os.path.dirname(os.path.dirname(HERE))            # racine du projet (hors site/)
DRAFTS = os.path.join(PROJECT, "journal_drafts")
STATE = os.path.join(PROJECT, "journal_state.json")
ENVFILE = os.path.join(PROJECT, "journal.env")
REGISTRY = os.path.join(HERE, "_articles_registry.py")
ONE = "https://oneiroparis.com/cdn/shop/files/"

QUERIES = [
    ("fr", "bague de fiançailles célébrité"),
    ("fr", "fiançailles star bague diamant"),
    ("fr", "mariage célébrité bague de fiançailles"),
    ("en", "celebrity engagement ring"),
    ("en", "celebrity engaged ring carat designer"),
]
UA = "Mozilla/5.0 (compatible; OneiroJournalBot/1.0)"
MONTHS = {
    "fr": ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
           "septembre", "octobre", "novembre", "décembre"],
    "en": ["January", "February", "March", "April", "May", "June", "July", "August",
           "September", "October", "November", "December"],
}
DISCLAIMER = {
    "fr": "<p><em>Précision utile&nbsp;: Oneiro n'a aucun lien avec les personnes et les maisons citées ici. "
          "Nous commentons des informations rendues publiques par la presse, et nous ne reproduisons le dessin de personne. "
          "Ce qui se transpose, ce sont des choix génériques, une forme de pierre, un type de serti, une couleur d'or.</em></p>",
    "en": "<p><em>A useful note: Oneiro has no connection with the people and houses mentioned here. "
          "We comment on information made public by the press, and we do not reproduce anyone's design. "
          "What carries over are generic choices: a stone shape, a type of setting, a colour of gold.</em></p>",
}
ALLOWED_TAGS = {"p", "h2", "h3", "strong", "em", "a", "ul", "ol", "li", "br", "blockquote"}


# ------------------------------------------------------------------ utilitaires
def load_env():
    if os.path.exists(ENVFILE):
        for line in open(ENVFILE, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

def load_state():
    try:
        return json.load(open(STATE, encoding="utf-8"))
    except Exception:
        return {"seen_links": [], "published": []}

def save_state(st):
    json.dump(st, open(STATE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

def http_get(url, timeout=20):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "fr,en;q=0.8"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
        m = re.search(r"charset=([\w-]+)", r.headers.get("Content-Type", ""))
    enc = m.group(1) if m else "utf-8"
    try:
        return raw.decode(enc, errors="replace")
    except LookupError:
        return raw.decode("utf-8", errors="replace")

def norm(s):
    s = html.unescape(s).lower().replace("’", "'").replace(" ", " ")
    return re.sub(r"\s+", " ", re.sub(r"[^\w' ]+", " ", s)).strip()

def strip_dashes(s):
    """Pas de tiret long dans les textes publiés (règle éditoriale de la maison)."""
    return re.sub(r"\s*[—–]\s*", ", ", s)

def slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", norm(s).replace("'", "-")).strip("-")
    return s[:80].strip("-")

def load_registry_module():
    import importlib.util
    spec = importlib.util.spec_from_file_location("_articles_registry_live", REGISTRY)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod

def load_products():
    return json.load(open(os.path.join(HERE, "products.json"), encoding="utf-8"))


# ------------------------------------------------------------------ veille
def parse_rss(xml_text):
    out = []
    root = ET.fromstring(xml_text)
    for it in root.iter("item"):
        link = (it.findtext("link") or "").strip()
        if "bing.com" in link and "url=" in link:
            q = urllib.parse.parse_qs(urllib.parse.urlparse(link).query)
            link = q.get("url", [link])[0]
        src = ""
        for child in it:
            if child.tag.endswith("Source") or child.tag == "source":
                src = (child.text or "").strip()
        try:
            dt = email.utils.parsedate_to_datetime(it.findtext("pubDate"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=datetime.timezone.utc)
        except Exception:
            dt = datetime.datetime.now(datetime.timezone.utc)
        out.append({"title": html.unescape((it.findtext("title") or "").strip()), "link": link,
                    "source": src, "date": dt.isoformat()})
    return out

def search_news(query, lang):
    q = urllib.parse.quote(query)
    urls = [f"https://www.bing.com/news/search?q={q}&format=rss&setlang={lang}",
            f"https://news.google.com/rss/search?q={q}&hl={lang}&gl={'FR' if lang == 'fr' else 'US'}&ceid={'FR:fr' if lang == 'fr' else 'US:en'}"]
    for u in urls:
        try:
            items = parse_rss(http_get(u))
            if items:
                return items
        except Exception as e:
            print(f"  (flux indisponible : {u.split('/')[2]} : {e})", file=sys.stderr)
    return []

def scan(days=10, extra_query=None):
    st = load_state()
    qs = [("fr", extra_query), ("en", extra_query)] if extra_query else QUERIES
    seen, items = set(), []
    cutoff = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=days)
    for lang, q in qs:
        for it in search_news(q, lang):
            key = norm(it["title"])[:60]
            if key in seen or it["link"] in st["seen_links"]:
                continue
            if datetime.datetime.fromisoformat(it["date"]) < cutoff:
                continue
            seen.add(key); items.append(it)
    items.sort(key=lambda x: x["date"], reverse=True)
    os.makedirs(DRAFTS, exist_ok=True)
    json.dump(items, open(os.path.join(DRAFTS, "_last_scan.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return items

def related(item, items):
    """Articles qui parlent du même événement : au moins 2 mots en majuscule en commun."""
    def caps(t): return {w for w in re.findall(r"\b[A-ZÉÈÀ][\w'-]{3,}", t)}
    base = caps(item["title"])
    return [x for x in items if x is item or len(base & caps(x["title"])) >= 2][:4]


# ------------------------------------------------------------------ lecture des sources
def article_text(url, limit=7000):
    try:
        page = http_get(url)
    except Exception as e:
        return "", f"inaccessible ({e})"
    page = re.sub(r"(?is)<(script|style|nav|footer|header|aside|form|noscript)[^>]*>.*?</\1>", " ", page)
    paras = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", p))).strip()
             for p in re.findall(r"(?is)<p[^>]*>(.*?)</p>", page)]
    text = "\n".join(p for p in paras if len(p) > 50)
    return text[:limit], ""

def collect_sources(items_or_urls):
    sources = []
    for i, x in enumerate(items_or_urls, 1):
        url = x if isinstance(x, str) else x["link"]
        title = "" if isinstance(x, str) else x["title"]
        text, err = article_text(url)
        if len(text) < 800:
            print(f"  source ignorée (texte trop court ou {err or 'protégé'}) : {url}")
            continue
        sources.append({"id": f"S{len(sources) + 1}", "url": url, "title": title,
                        "domain": urllib.parse.urlparse(url).netloc.replace("www.", ""), "text": text})
    return sources


# ------------------------------------------------------------------ modèle de langage
def llm(prompt):
    prov = os.environ.get("ONEIRO_LLM", "gemini").lower()
    if prov == "fake":                      # pour tester la chaîne sans clé
        return open(os.environ["ONEIRO_FAKE_JSON"], encoding="utf-8").read()
    if prov == "anthropic":
        key = os.environ.get("ANTHROPIC_API_KEY") or sys.exit("ANTHROPIC_API_KEY manquante")
        body = {"model": os.environ.get("ONEIRO_LLM_MODEL", "claude-sonnet-5-5"), "max_tokens": 8000,
                "temperature": 0.3, "messages": [{"role": "user", "content": prompt}]}
        req = urllib.request.Request("https://api.anthropic.com/v1/messages", json.dumps(body).encode(),
                                     {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
        data = json.load(urllib.request.urlopen(req, timeout=180))
        return "".join(b.get("text", "") for b in data["content"])
    key = os.environ.get("GEMINI_API_KEY") or sys.exit("GEMINI_API_KEY manquante")
    model = os.environ.get("ONEIRO_LLM_MODEL", "gemini-2.5-flash")
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.3, "responseMimeType": "application/json"}}
    req = urllib.request.Request(f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
                                 json.dumps(body).encode(), {"x-goog-api-key": key, "content-type": "application/json"})
    data = json.load(urllib.request.urlopen(req, timeout=180))
    return "".join(p.get("text", "") for p in data["candidates"][0]["content"]["parts"])

def extract_json(txt):
    m = re.search(r"\{.*\}", txt, re.S)
    if not m:
        raise ValueError("réponse sans JSON")
    return json.loads(m.group(0))

def build_prompt(topic, sources, products, reg):
    style = open(os.path.join(HERE, "articles", "bagues-de-fiancailles-des-stars-2026.html"), encoding="utf-8").read()
    style = re.sub(r"(?s)^.*?<div class=\"wrap prose\">", "", style)[:2200]
    plist = "\n".join(f"- {p['handle']} | {p['title']} | {p['category']} | des {p.get('priceFrom')} EUR" for p in products)
    existing = "\n".join(f"- journal/{a['fr']['slug']}.html (FR) | journal/{a['en']['slug']}.html (EN) | {a['fr']['card']}"
                         for a in reg.ARTICLES.values())
    src = "\n\n".join(f"[{s['id']}] {s['domain']} | {s['title']}\n{s['text']}" for s in sources)
    return f"""Tu rédiges un article du Journal d'Oneiro Paris, maison parisienne de joaillerie sur-mesure 100 % en ligne
(bagues de fiançailles, diamants certifiés GIA/IGI, naturels et de laboratoire, or 18 carats).
Sujet : {topic}

RÈGLES NON NÉGOCIABLES
1. N'utilise QUE les faits présents dans les SOURCES ci-dessous. Aucune connaissance extérieure sur les personnes, leurs bijoux, leurs prix.
2. Aucune citation inventée. Une citation entre guillemets doit être recopiée mot pour mot d'une source, sinon n'en mets pas.
3. Les carats, prix et origines de pierre rapportés par la presse sont des ESTIMATIONS : dis-le, et signale quand les sources divergent.
4. Aucun lien suggéré entre Oneiro et les personnes citées. Aucune rumeur, aucun détail de vie privée au-delà de l'événement public.
5. Si les sources ne disent rien sur la bague, ne l'invente pas : écris sur ce que l'événement dit des goûts (forme, serti, or) de façon générique, et reconnais ce qu'on ignore.
6. Ne reproduis le dessin de personne. Propose des choix génériques transposables et rattache-les à 3 pièces de la collection.
7. Ton : sobre, honnête, concret, comme les articles existants (exemple ci-dessous). Pas de superlatifs creux, pas d'appel d'achat agressif.
8. JAMAIS de tiret long (— ou –). Utilise virgule, deux-points ou parenthèses. Espace insécable (&nbsp;) avant : ; ! ? et « » en français.
9. Corps en HTML restreint : p, h2, h3, strong, em, a, ul, li. Pas de h1. 650 à 1100 mots par langue. Commence par un paragraphe d'accroche en <strong>. Termine par une section « Ce qu'on en retient » (EN : "What to take from it").
10. Liens internes autorisés uniquement : produits/HANDLE.html (FR) ou products/HANDLE.html (EN) avec un HANDLE de la liste, et les pages journal/... listées. Aucun autre lien.
11. Ne mets PAS de bloc « sources » ni d'avertissement « Oneiro n'a aucun lien » : ils sont ajoutés automatiquement.

PIÈCES DE LA COLLECTION (choisis exactement 3 handles pertinents) :
{plist}

ARTICLES DÉJÀ PUBLIÉS (pour les liens internes) :
{existing}

EXEMPLE DE STYLE (extrait d'un article existant) :
{style}

SOURCES :
{src}

RÉPONDS UNIQUEMENT PAR UN OBJET JSON :
{{"key": "kebab-case court et unique", "products": ["h1","h2","h3"],
 "claims": [{{"text": "fait précis utilisé", "source": "S1"}}],
 "fr": {{"slug": "...", "cat": "Actualité, Célébrités", "card": "titre de carte (max 70 car.)", "teaser": "accroche (max 140 car.)",
        "title": "titre SEO | Oneiro", "desc": "meta description 140-160 car.", "h1": "titre de l'article", "body": "<p>...</p>"}},
 "en": {{"slug": "...", "cat": "News, Celebrities", "card": "...", "teaser": "...", "title": "...", "desc": "...", "h1": "...", "body": "<p>...</p>"}}}}"""


# ------------------------------------------------------------------ contrôles
def check_draft(d, sources, products, reg):
    errors, warnings = [], []
    handles = {p["handle"] for p in products}
    corpus = norm(" ".join(s["text"] for s in sources))
    for k in ("key", "products", "fr", "en"):
        if k not in d:
            errors.append(f"champ manquant : {k}")
    if errors:
        return errors, warnings
    if not re.fullmatch(r"[a-z0-9-]{3,80}", d["key"]) or d["key"] in reg.ARTICLES:
        errors.append("clé invalide ou déjà utilisée")
    if len(d["products"]) != 3 or not set(d["products"]) <= handles:
        errors.append(f"produits invalides : {d['products']}")
    slugs = {a[l]["slug"] for a in reg.ARTICLES.values() for l in ("fr", "en")}
    for lang in ("fr", "en"):
        a = d[lang]
        for f in ("slug", "cat", "card", "teaser", "title", "desc", "h1", "body"):
            if not a.get(f):
                errors.append(f"{lang}.{f} manquant")
        if errors:
            continue
        if not re.fullmatch(r"[a-z0-9-]{3,90}", a["slug"]) or a["slug"] in slugs:
            errors.append(f"{lang}: slug invalide ou déjà utilisé ({a['slug']})")
        body = a["body"]
        for tag in re.findall(r"</?([a-zA-Z0-9]+)", body):
            if tag.lower() not in ALLOWED_TAGS:
                errors.append(f"{lang}: balise interdite <{tag}>")
        for href in re.findall(r'href="([^"]+)"', body):
            if href.startswith("http"):
                errors.append(f"{lang}: lien externe interdit dans le corps ({href})")
                continue
            m = re.fullmatch(r"(?:produits|products)/([\w-]+)\.html", href)
            j = re.fullmatch(r"journal/([\w-]+)\.html", href)
            if m and m.group(1) in handles and ((lang == "fr") == href.startswith("produits/")):
                continue
            if j and j.group(1) in slugs:
                continue
            errors.append(f"{lang}: lien interne inconnu ({href})")
        words = len(re.sub(r"<[^>]+>", " ", body).split())
        if not 450 <= words <= 1500:
            warnings.append(f"{lang}: {words} mots (attendu 650 à 1100)")
        text = html.unescape(re.sub(r"<[^>]+>", " ", body))
        for q in re.findall(r"«\s*([^»]{12,})»|“([^”]{12,})”|\"([^\"]{12,})\"", text):
            q = norm(next(x for x in q if x))
            if len(q.split()) >= 4 and q not in corpus:
                errors.append(f"{lang}: citation absente des sources : « {q[:80]} »")
        for n in set(re.findall(r"\b\d[\d\s.,]*\s?(?:carats?|ct|€|%|euros?)", text)):
            digits = re.sub(r"\D", "", n)
            if digits and digits not in re.sub(r"\D", "", " ".join(s["text"] for s in sources)):
                warnings.append(f"{lang}: chiffre à vérifier (absent des sources) : {n.strip()}")
    return errors, warnings


# ------------------------------------------------------------------ brouillon
def page_source(a, lang, date, body, sources):
    d = datetime.date.fromisoformat(date)
    words = len(re.sub(r"<[^>]+>", " ", body).split())
    mins = max(3, math.ceil(words / 200))
    if lang == "fr":
        meta = f"Publié le {d.day} {MONTHS['fr'][d.month - 1]} {d.year} · {mins} min de lecture · par la maison Oneiro"
        kick, lab = "Journal, Actualité, célébrités", "Sources consultées"
    else:
        meta = f"Published {d.day} {MONTHS['en'][d.month - 1]} {d.year} · {mins} min read · by the Oneiro house"
        kick, lab = "Journal, News, celebrities", "Sources consulted"
    parts = body.split("</p>", 1)
    body = parts[0] + "</p>\n    " + DISCLAIMER[lang] + (parts[1] if len(parts) > 1 else "")
    srcs = " · ".join(f'<a href="{html.escape(s["url"])}" rel="nofollow noopener" target="_blank">{html.escape(s["domain"])}</a>' for s in sources)
    body += f'\n    <p class="form__hint">{lab}&nbsp;: {srcs}</p>' if lang == "fr" else f'\n    <p class="form__hint">{lab}: {srcs}</p>'
    return f"""<section class="page-head section--cream">
  <div class="wrap">
    <span class="kicker">{kick}</span>
    <h1>{a['h1']}</h1>
    <p class="section-sub">{meta}</p>
  </div>
</section>

<section class="section">
  <div class="wrap prose">
    {body}
  </div>
</section>
"""

def make_draft(topic, sources):
    if len(sources) < 2:
        sys.exit("Moins de 2 sources exploitables : brouillon annulé (pour éviter d'écrire sans base factuelle).\n"
                 "Astuce : fournissez vous-même des URLs avec --url.")
    products, reg = load_products(), load_registry_module()
    raw = llm(build_prompt(topic, sources, products, reg))
    d = extract_json(raw)
    for lang in ("fr", "en"):                       # nettoyage des tirets longs
        for k, v in list(d.get(lang, {}).items()):
            if isinstance(v, str):
                d[lang][k] = strip_dashes(v)
    errors, warnings = check_draft(d, sources, products, reg)
    date = datetime.date.today().isoformat()
    folder = os.path.join(DRAFTS, d.get("key", "sans-cle"))
    os.makedirs(folder, exist_ok=True)
    if not errors or all(not e.startswith("champ manquant") for e in errors):
        for lang in ("fr", "en"):
            if d.get(lang, {}).get("body"):
                open(os.path.join(folder, f"{lang}.html"), "w", encoding="utf-8").write(
                    page_source(d[lang], lang, date, d[lang]["body"], sources))
    json.dump({"draft": d, "date": date, "errors": errors, "warnings": warnings, "topic": topic,
               "sources": [{k: s[k] for k in ("id", "url", "title", "domain")} for s in sources]},
              open(os.path.join(folder, "meta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rev = [f"# Relecture : {d.get('key')}", "", f"Sujet : {topic}", "",
           "## Contrôles automatiques", *(f"- ERREUR : {e}" for e in errors), *(f"- à vérifier : {w}" for w in warnings),
           "" if (errors or warnings) else "- aucun problème détecté", "",
           "## Faits utilisés (à confronter aux sources)",
           *(f"- [{c.get('source')}] {c.get('text')}" for c in d.get("claims", [])), "",
           "## Sources", *(f"- [{s['id']}] {s['url']}" for s in sources)]
    open(os.path.join(folder, "RELECTURE.md"), "w", encoding="utf-8").write("\n".join(rev))
    return d.get("key", "sans-cle"), folder, errors, warnings

def list_drafts():
    out = []
    if os.path.isdir(DRAFTS):
        for k in sorted(os.listdir(DRAFTS)):
            m = os.path.join(DRAFTS, k, "meta.json")
            if os.path.exists(m):
                j = json.load(open(m, encoding="utf-8"))
                out.append((k, j["date"], len(j["errors"]), len(j["warnings"])))
    return out


# ------------------------------------------------------------------ publication
def product_image(handle):
    for p in load_products():
        if p["handle"] == handle and p.get("images"):
            name = p["images"][0].split("/files/")[-1].split("?")[0]
            return ONE + name
    return None

def publish(key, force=False):
    folder = os.path.join(DRAFTS, key)
    meta = json.load(open(os.path.join(folder, "meta.json"), encoding="utf-8"))
    if meta["errors"] and not force:
        sys.exit("Brouillon refusé, erreurs à corriger dans RELECTURE.md :\n- " + "\n- ".join(meta["errors"]))
    d = meta["draft"]
    img = product_image(d["products"][0])
    if not img:
        sys.exit("Aucune image de carte trouvée pour le premier produit.")
    for lang, sub in (("fr", "articles"), ("en", "articles-en")):
        shutil.copyfile(os.path.join(folder, f"{lang}.html"), os.path.join(HERE, sub, d[lang]["slug"] + ".html"))
    def entry(lang):
        a = d[lang]
        rows = "".join(f'            "{f}": {json.dumps(a[f], ensure_ascii=False)},\n' for f in ("slug", "cat", "card", "teaser", "title", "desc"))
        return f'        "{lang}": {{\n{rows}        }},\n'
    block = (f'\n    {json.dumps(d["key"])}: {{\n        "date": "{meta["date"]}", "section": "actu",\n'
             f'        "image": ONE + {json.dumps(img[len(ONE):])},\n'
             f'        "products": {json.dumps(d["products"])},\n{entry("fr")}{entry("en")}    }},\n')
    src = open(REGISTRY, encoding="utf-8").read()
    m = re.search(r"^ARTICLES = \{\n", src, re.M)
    end = re.search(r"^\}\n", src[m.end():], re.M)
    pos = m.end() + end.start()
    shutil.copyfile(REGISTRY, REGISTRY + ".bak")
    open(REGISTRY, "w", encoding="utf-8", newline="").write(src[:pos] + block + src[pos:])
    r = subprocess.run([sys.executable, os.path.join(HERE, "build.py")], capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())
    if r.returncode != 0:
        shutil.copyfile(REGISTRY + ".bak", REGISTRY)
        sys.exit("Le build a échoué : registre restauré.")
    st = load_state()
    st["published"].append({"key": key, "date": meta["date"]})
    st["seen_links"] += [s["url"] for s in meta["sources"]]
    save_state(st)
    shutil.move(folder, os.path.join(DRAFTS, "_publies_" + key))
    print(f"Publié : journal/{d['fr']['slug']}.html  et  en/journal/{d['en']['slug']}.html")


# ------------------------------------------------------------------ commande
def main():
    load_env()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = ap.add_subparsers(dest="cmd", required=True)
    s = sp.add_parser("scan"); s.add_argument("--days", type=int, default=10); s.add_argument("--query")
    d = sp.add_parser("draft"); d.add_argument("--pick"); d.add_argument("--url", action="append"); d.add_argument("--query"); d.add_argument("--topic")
    a = sp.add_parser("auto"); a.add_argument("--publish", action="store_true"); a.add_argument("--days", type=int, default=10)
    sp.add_parser("list")
    p = sp.add_parser("publish"); p.add_argument("key"); p.add_argument("--force", action="store_true")
    args = ap.parse_args()

    if args.cmd == "scan":
        items = scan(args.days, args.query)
        for i, x in enumerate(items, 1):
            print(f"{i:2}. {x['date'][:10]}  {x['title']}  ({x['source']})\n      {x['link']}")
        print(f"\n{len(items)} résultat(s). Ensuite : draft --pick 1,2")
    elif args.cmd == "list":
        for k, dt, e, w in list_drafts():
            print(f"{k}  {dt}  erreurs={e}  à vérifier={w}")
    elif args.cmd == "publish":
        publish(args.key, args.force)
    elif args.cmd == "draft":
        if args.url:
            chosen, topic = args.url, args.topic or "actualité fiançailles"
        elif args.pick:
            last = json.load(open(os.path.join(DRAFTS, "_last_scan.json"), encoding="utf-8"))
            chosen = [last[int(i) - 1] for i in args.pick.split(",")]
            topic = args.topic or chosen[0]["title"]
        elif args.query:
            chosen = scan(21, args.query)[:4]; topic = args.topic or args.query
        else:
            sys.exit("Précisez --pick, --url ou --query")
        key, folder, err, warn = make_draft(topic, collect_sources(chosen))
        print(f"\nBrouillon : {folder}\nErreurs : {len(err)}  À vérifier : {len(warn)}\nLisez RELECTURE.md puis : publish {key}")
    elif args.cmd == "auto":
        items = scan(args.days)
        if not items:
            sys.exit("Rien de nouveau à traiter.")
        group = related(items[0], items)
        print("Sujet retenu :", items[0]["title"])
        key, folder, err, warn = make_draft(items[0]["title"], collect_sources(group))
        print(f"Brouillon : {folder}  erreurs={len(err)}  à vérifier={len(warn)}")
        if args.publish:
            if err or warn:
                print("Publication automatique refusée (erreurs ou points à vérifier). Relisez RELECTURE.md.")
            else:
                publish(key)

if __name__ == "__main__":
    main()
