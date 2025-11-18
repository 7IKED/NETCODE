# NETMASTER WIKI — Public Docs (Index UI)

Diese Seite dokumentiert die öffentliche Benutzeroberfläche, die in `netmaster_wiki/templates/index.html` liegt. Sie beschreibt die Funktionalitäten, typische Abläufe und Sicherheits-Hinweise für Betreiber.

Kurzüberblick

- Editor: Ein einfaches Formular zum Anlegen von Markdown-Seiten (Titel + Inhalt). Beim Speichern wird die Seite unter `netmaster_wiki/pages/<slug>.md` abgelegt.
- Tags generieren: Button "Tags generieren" ruft `/autotags` auf und füllt das Tag-Feld mit Vorschlägen.
- Seitenliste: Unterhalb des Formulars werden vorhandene Seiten verlinkt.
- Autoupdater-Feedback: Formular sendet JSON an `/feedback` und speichert Einträge in `netmaster_wiki/feedback.json`.
- Admin-Fetch (nur Betreiber): Ein kleiner Admin‑Bereich erlaubt das Speichern eines Admin-Tokens im Browser (localStorage) und das Ausführen serverseitiger Fetches an `/fetch` (optional: unsichere TLS-Verbindungen, nur mit Token).

How-to (quick)

1. Lokalen Server starten (im Ordner `netmaster_wiki`):

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
# Öffne http://127.0.0.1:5000
```

2. Neue Seite erstellen
- Titel und Markdown eingeben → Speichern.
- Tags: entweder manuell eingeben (kommagetrennt) oder "Tags generieren" klicken.

3. Feedback absenden
- Nachricht in "Autoupdater Feedback" eingeben → Senden (POST `/feedback`).

Admin-Fetch (Schritt-für-Schritt)

1. Konfig: Lege `netmaster_wiki/config.json` an und setze `admin_token` (nicht `CHANGE_ME_TOKEN`), füge vertrauenswürdige Hosts zu `trusted_hosts` oder setze `allow_insecure_global` auf `true` (vorsichtig!).
2. In der Index-UI: Token eingeben → "Token speichern" (wird in localStorage gehalten).
3. URL eingeben, ggf. "Unsichere TLS zulassen" wählen und "Fetch ausführen" klicken.

Beispiel: Server-seitiger Fetch (curl)

Sicherer Fetch (kein Token nötig):

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"url":"https://example.com"}' \
  http://127.0.0.1:5000/fetch
```

Unsicherer Fetch (nur mit Token und Trusted Host):

```bash
curl -X POST -H "Content-Type: application/json" -H "X-Admin-Token: <DEIN_TOKEN>" \
  -d '{"url":"https://self-signed.local","insecure":true}' \
  http://127.0.0.1:5000/fetch
```

Wichtige Sicherheits-Hinweise

- Das Admin-Token, das in der UI gespeichert wird, liegt lokal im Browser (localStorage). Es wird nicht serverseitig geschützt; verwende diese Funktion nur lokal oder in einem vertrauenswürdigen Umfeld.
- Aktivieren von `allow_insecure_global` oder das Zulassen unsicherer TLS-Verbindungen öffnet Angriffsflächen. Nutze stattdessen `trusted_hosts` und setze dort explizit interne Domains.
- Für produktive Nutzung: HTTPS für das Wiki, serverseitige Secrets (Umgebungsvariablen), Authentifizierung, CSRF-Schutz und Ratenbegrenzung implementieren.

Wichtige Dateipfade

- `netmaster_wiki/templates/index.html` — die UI-Quelle.
- `netmaster_wiki/app.py` — Endpoints: `/`, `/save`, `/autotags`, `/pages`, `/page/<slug>`, `/feedback`, `/fetch`.
- `netmaster_wiki/pages/` — gespeicherte Markdown-Seiten.
- `netmaster_wiki/feedback.json` — gesammeltes Feedback.
- `netmaster_wiki/config.json` — (optional) Admin-Token, trusted hosts, flags.

Wenn du möchtest, kann ich diese Docs als HTML-Seite rendern oder eine kleine Navigation im Repo-Root ergänzen (z. B. `docs/netmaster_index.md`), damit sie leichter öffentlich erreichbar ist. Sag Bescheid, wie du die Docs veröffentlichen willst.
