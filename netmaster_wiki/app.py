#!/usr/bin/env python3
"""Ein kleines, lokales Wiki für NETMASTER.

Funktionen:
- Web-UI zum Einfügen von Markdown (Formular)
- Seiten als Markdown-Dateien in `pages/` speichern
- Automatische Schlagwort-Generierung (einfaches Heuristik-Counter)
- Feedback/Autoupdater-Einträge in `feedback.json` speichern

Minimal abhängig von: Flask, markdown
"""
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
import os
import json
import re
from datetime import datetime
from collections import Counter
import urllib.parse
import requests

# load config
CONFIG_PATH = os.path.join(BASE_DIR, "config.json")
if os.path.exists(CONFIG_PATH):
    try:
        with open(CONFIG_PATH, encoding='utf-8') as cf:
            CONFIG = json.load(cf)
    except Exception:
        CONFIG = {}
else:
    CONFIG = {}

ADMIN_TOKEN = CONFIG.get('admin_token')
ALLOW_INSECURE_GLOBAL = bool(CONFIG.get('allow_insecure_global', False))
TRUSTED_HOSTS = CONFIG.get('trusted_hosts', [])

BASE_DIR = os.path.dirname(__file__)
PAGES_DIR = os.path.join(BASE_DIR, "pages")
FEEDBACK_FILE = os.path.join(BASE_DIR, "feedback.json")

os.makedirs(PAGES_DIR, exist_ok=True)

app = Flask(__name__, template_folder="templates", static_folder="static")

# very small stopword list for tag extraction
STOPWORDS = set([
    "und","oder","der","die","das","ein","eine","in","auf","zu","mit",
    "ist","sind","auch","von","für","als","an","bei","nach","als",
    "the","a","of","and","to","is"
])


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    s = re.sub(r"-+", "-", s)
    return s or "untitled"


def extract_tags(text: str, top_n: int = 6):
    words = re.findall(r"[a-zA-ZäöüÄÖÜß0-9]{3,}", text.lower())
    words = [w for w in words if w not in STOPWORDS]
    cnt = Counter(words)
    tags = [w for w, _ in cnt.most_common(top_n)]
    return tags


def is_trusted_host(url: str) -> bool:
    try:
        p = urllib.parse.urlparse(url)
        host = p.hostname or ''
        for th in TRUSTED_HOSTS:
            if host == th or host.endswith('.' + th):
                return True
    except Exception:
        return False
    return False


@app.route('/fetch', methods=['POST'])
def fetch_url():
    """Fetch a URL server-side. Allows insecure TLS only when explicitly authorized.

    JSON body: { "url": "...", "insecure": true/false }
    Header or json field: 'X-Admin-Token' or 'token' must match CONFIG.admin_token to allow insecure fetches.
    Only hosts listed in `trusted_hosts` may be fetched with insecure TLS when requested.
    """
    data = request.get_json(force=True) or {}
    url = data.get('url') or request.form.get('url')
    if not url:
        return jsonify({'ok': False, 'error': 'url required'}), 400
    insecure_req = bool(data.get('insecure', False) or request.form.get('insecure', False))
    token = request.headers.get('X-Admin-Token') or data.get('token') or request.form.get('token')

    # authorize insecure only if token matches admin and host is trusted or global flag set
    if insecure_req:
        if not ADMIN_TOKEN:
            return jsonify({'ok': False, 'error': 'server not configured for insecure fetches'}), 403
        if token != ADMIN_TOKEN:
            return jsonify({'ok': False, 'error': 'invalid admin token'}), 403
        if not (ALLOW_INSECURE_GLOBAL or is_trusted_host(url)):
            return jsonify({'ok': False, 'error': 'host not allowed for insecure fetch'}), 403

    try:
        resp = requests.get(url, timeout=10, verify=not insecure_req)
        return (resp.content, resp.status_code, {'Content-Type': resp.headers.get('Content-Type', 'application/octet-stream')})
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 502



def page_path(slug: str) -> str:
    return os.path.join(PAGES_DIR, f"{slug}.md")


@app.route("/")
def index():
    # simple form to create pages and submit feedback
    pages = []
    for fn in sorted(os.listdir(PAGES_DIR)):
        if fn.endswith('.md'):
            pages.append(fn[:-3])
    return render_template("index.html", pages=pages)


@app.route("/autotags", methods=["POST"])
def autotags():
    data = request.get_json(force=True) or {}
    text = data.get("text", "")
    tags = extract_tags(text)
    return jsonify({"tags": tags})


@app.route("/save", methods=["POST"])
def save():
    title = request.form.get("title", "Untitled").strip()
    content = request.form.get("content", "").strip()
    tags_in = request.form.get("tags", "").strip()
    if not title and not content:
        abort(400, "Title or content required")
    slug = slugify(title or content[:40])
    if tags_in:
        tags = [t.strip() for t in tags_in.split(',') if t.strip()]
    else:
        tags = extract_tags(title + "\n" + content)
    meta = {
        "title": title or slug,
        "date": datetime.utcnow().isoformat() + "Z",
        "tags": tags,
    }
    md = "---\n"
    md += f"title: {meta['title']}\n"
    md += f"date: {meta['date']}\n"
    md += f"tags: {json.dumps(meta['tags'])}\n"
    md += "---\n\n"
    md += content + "\n"
    with open(page_path(slug), "w", encoding="utf-8") as f:
        f.write(md)
    return redirect(url_for('view_page', slug=slug))


@app.route("/pages")
def pages_list():
    pages = []
    for fn in sorted(os.listdir(PAGES_DIR)):
        if fn.endswith('.md'):
            pages.append(fn[:-3])
    return render_template("pages.html", pages=pages)


@app.route("/page/<slug>")
def view_page(slug):
    path = page_path(slug)
    if not os.path.exists(path):
        abort(404)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # naive split frontmatter
    parts = text.split('---', 2)
    if len(parts) >= 3:
        _, meta_raw, body = parts
    else:
        meta_raw = ""
        body = text
    # try to parse tags from meta
    tags = []
    m = re.search(r"tags:\s*(\[.*\])", meta_raw)
    if m:
        try:
            tags = json.loads(m.group(1))
        except Exception:
            tags = []
    # render markdown (if markdown lib is available)
    try:
        import markdown as md
        html = md.markdown(body)
    except Exception:
        # fallback: show raw markdown in pre
        html = f"<pre>{body}</pre>"
    return render_template("page.html", title=slug, content=html, tags=tags)


@app.route("/feedback", methods=["POST"])
def feedback():
    data = request.get_json(force=True) or {}
    msg = data.get('message') or data.get('msg') or ''
    source = data.get('source') or 'web'
    who = data.get('who') or ''
    if not msg:
        return jsonify({"ok": False, "error": "message required"}), 400
    entry = {
        "message": msg,
        "who": who,
        "source": source,
        "ts": datetime.utcnow().isoformat() + 'Z'
    }
    if os.path.exists(FEEDBACK_FILE):
        with open(FEEDBACK_FILE, encoding='utf-8') as f:
            try:
                arr = json.load(f)
            except Exception:
                arr = []
    else:
        arr = []
    arr.append(entry)
    with open(FEEDBACK_FILE, 'w', encoding='utf-8') as f:
        json.dump(arr, f, indent=2, ensure_ascii=False)
    return jsonify({"ok": True})


if __name__ == '__main__':
    # simple dev server
    app.run(host='127.0.0.1', port=5000, debug=True)
