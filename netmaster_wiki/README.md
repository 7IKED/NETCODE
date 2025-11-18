# NETMASTER WIKI

Ein kleines, lokales Wiki für das NETCODE-Repository. Ziel ist ein schneller, lokaler Editor, mit dem Markdown-Seiten erstellt werden können, sowie eine einfache Feedback-Schnittstelle (z. B. für Autoupdater-Feedback).

Start (lokal, Entwicklung):

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
# dann im Browser öffnen: http://127.0.0.1:5000
```

Konzept
- Seiten werden unter `pages/` als Markdown-Dateien mit einfacher Front-Matter (title/date/tags) gespeichert.
- Tags werden automatisch per Heuristik aus dem Inhalt vorgeschlagen; es gibt ein UI-Button "Tags generieren".
- Feedback wird in `feedback.json` gesammelt.

Hinweis: Dieses Tool ist minimal und für lokale Nutzung gedacht. Für produktive Nutzung sollte man Authentifizierung, Validation, Versionskontrolle und robuste Tagging-Logik ergänzen.

Unsichere Quellen
-----------------
Das Wiki unterstützt optionales server-seitiges Abrufen externer URLs über den Endpoint `/fetch`.
Unsichere TLS-Verbindungen (z. B. verify=False) werden nur zugelassen, wenn:

- Du einen `admin_token` in `netmaster_wiki/config.json` gesetzt hast (ändert `CHANGE_ME_TOKEN`).
- Der Request das Token in Header `X-Admin-Token` oder im JSON-Feld `token` liefert.
- Und entweder `allow_insecure_global` in `config.json` auf `true` gesetzt ist oder der Zielhost in `trusted_hosts` gelistet ist.

Beispiel (curl) — sicherer Fetch:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"url":"https://example.com"}' http://127.0.0.1:5000/fetch
```

Beispiel (curl) — unsicherer Fetch erlaubt (nur wenn token & trusted host konfiguriert sind):

```bash
curl -X POST -H "Content-Type: application/json" -H "X-Admin-Token: CHANGE_ME_TOKEN" -d '{"url":"https://self-signed.example.local","insecure":true}' http://127.0.0.1:5000/fetch
```

Warnung: Diese Funktion ist mächtig und kann Sicherheitsrisiken bergen. Aktiviere sie nur in kontrollierten, lokalen oder vertrauenswürdigen Umgebungen.

Browser-Admin-UI
----------------
Im Wiki findest du jetzt eine Admin-Sektion auf der Index-Seite, in der du dein `admin_token` lokal im Browser (localStorage) speichern und serverseitige Fetches ausführen kannst. Das Token wird nicht an anderen Stellen im Repo gespeichert.

Hinweis: Das Speichern des Tokens im Browser ist praktisch für lokale Betreiber, aber nicht so sicher wie ein serverseitig verwalteter Secret-Store. Nutze es nur lokal.

Siehe auch die öffentliche Dokumentation zur Index-UI: `netmaster_wiki/docs/index.md` — dort sind UI‑Abläufe, Beispiele und Sicherheits‑Hinweise zusammengefasst.
