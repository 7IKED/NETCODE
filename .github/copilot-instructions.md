````instructions
## Kurzanleitung für KI-Coding-Agenten

Dieses Projekt enthält aktuell nur minimale Metadaten (z. B. `README.md`, `LICENSE`). Es liegen keine Quellcode-Dateien, Build- oder CI-Konfigurationen vor. Verwende die folgenden, konkreten Schritte, um produktiv zu starten, Entscheidungen nachzuweisen und sinnvolle PR-Vorschläge zu machen.

1) Schnelle Repo-Discovery

- Öffne und lese `README.md` und die Projekt-Root (bereits vorhanden).
- Prüfe systematisch auf typische Build-/Sprach-Indikatoren (Beispiele):

```bash
# prüfe nach Node/Python/Go/Rust/Java/Gradle/Maven/Elterndateien
git ls-files | grep -E "package.json|pyproject.toml|requirements.txt|setup.py|go.mod|Cargo.toml|pom.xml|build.gradle|Makefile|Dockerfile" -n || true
```

- Falls keine der Dateien vorhanden ist (wie aktuell), dokumentiere das kurz in deinem PR und schlage eine sinnvolle erste Aufgabe vor (z. B. Projekt-Scaffold, README-Erweiterung, CI-Workflow).

2) Architektur & "Big Picture"

- In diesem Repository sind keine Komponenten oder Services gefunden. Wenn du neue Code-Dateien hinzufügst, beschreibe in der PR-Beschreibung immer:
  - Ziel und Verantwortlichkeit der Komponente (Input/Output, Fehlerfälle)
  - Wo Code leben soll (z. B. `src/`, `cmd/`, `pkg/` oder `lib/` je nach Sprache)
  - Minimale Lauf-/Test-Schritte zum Verifizieren

3) Projekt-spezifische Workflows (aktuell keine vorhanden)

- Da kein Build/Test definiert ist, liefere in deinem Vorschlag eindeutige, automatisierte Schritte:
  - Beispiel für Node.js: `npm install && npm test`
  - Beispiel für Python: `python -m venv .venv && .venv/bin/pip install -r requirements.txt && pytest`

- Wenn du CI hinzufügen willst, erstelle eine einfache GitHub Actions Workflow-Datei in `.github/workflows/` mit einem sehr schlanken Job (checkout + Setup + test). Verweise in der PR auf die minimalen Erfolgskriterien.

4) Konventionen & Patterns (was du hier finden/setzen sollst)

- Namenskonvention: Falls du ein Sprach-Scaffold anlegst, folge den üblichen Konventionen der Sprache (z. B. `src/` für Python/TS, `cmd/` + `pkg/` für Go). Dokumentiere die gewählte Konvention in `README.md`.
- Commit/PR-Nachrichten: kurze Titelzeile, 1–2 Zeilen Beschreibung, ein Abschnitt "How to test" mit den minimalen Schritten.

5) Integration & externe Abhängigkeiten

- Es sind keine Integration-Punkte (APIs, DBs, cloud infra) detektierbar. Wenn du solche hinzufügst, nenne in der PR:
  - Endpunkte/Umgebungsvariablen (nur Namen, keine Geheimnisse)
  - Minimal reproduzierbare Local-Run-Anleitung

6) Beispiele & Templates (benutze diese Vorlagen in PRs)

- PR-Beschreibung (kurz):
  - Was wurde geändert
  - Warum (Motivation)
  - Wie zu testen (copy-paste Befehle)

- Commit-Beispiel-Titel: `chore: scaffold project (language)` oder `feat: add initial CI workflow`

7) Wenn du unsicher bist

- Stelle eine präzise Frage in der PR-Description (z. B. "Welche Sprache bevorzugst du für dieses Projekt?") und biete 2-3 vorgeschlagene Optionen (z. B. Node.js scaffold, Python package, minimal Go module).

8) Files to reference

- `README.md` — aktuell die einzige inhaltliche Datei; erweitere sie bei allen größeren Änderungen.

---
Wenn du möchtest, kann ich sofort ein erstes Scaffolding vorschlagen (z. B. `node` oder `python`) und eine PR mit README-, CI- und Minimal-Test hinzufügen — nenne kurz welche Sprache/Stack du bevorzugst oder lass mich Vorschläge machen.

## Versionierung & Releases

Dieses Repository verwendet aktuell noch kein automatisches Release-System. Lege folgenden, einfachen Workflow an, damit Änderungen nachvollziehbar und reproduzierbar sind:

- Datei `VERSION`: enthält die aktuelle Release-Version (SemVer), z. B. `0.1.0`.
- Datei `CHANGELOG.md`: chronologische Liste von Releases mit kurzen Beschreibungen.
- Release-Prozess (manuell für Start):

```bash
# 1. Inkrementiere VERSION (z. B. 0.1.0 -> 0.1.1)
echo "0.1.1" > VERSION
# 2. Ergänze CHANGELOG.md mit Einträgen für die neue Version
# 3. Commit + Tag
git add VERSION CHANGELOG.md
git commit -m "chore(release): bump version to 0.1.1"
git tag -a v0.1.1 -m "Release v0.1.1"
git push --follow-tags
```

Hinweis für Agenten: Verwende SemVer (MAJOR.MINOR.PATCH). Schreibe in Pull Requests kurz in den Titel oder das Release-Issue, welche SemVer-Schritte erforderlich sind (z. B. `patch` für Bugfixes, `minor` für neue Features, `major` für breaking changes).

Automatisierungsempfehlung: Später kann eine GitHub Actions-Workflowdatei (z. B. `.github/workflows/release.yml`) hinzugefügt werden, die bei Merge in `main` automatisch die Version taggt und ein GitHub Release erstellt.

## Issue-Vorlage für Releases

Im Ordner `.github/ISSUE_TEMPLATE/` liegt eine Vorlage, die verwendet werden soll, um Release/Version-Requests einheitlich zu erfassen. Nutze diese Vorlage, wenn du ein Release anstößt oder eine Versionserhöhung vorschlägst.

---

## NETMASTER WIKI (lokal)

Ich habe ein kleines lokales Wiki unter `netmaster_wiki/` hinzugefügt. Es ist ein Minimal‑Flask-Service, der folgende Funktionen bietet:

- Web-UI zum Einfügen von Markdown (`/`)
- Seiten werden als `.md` in `netmaster_wiki/pages/` gespeichert (Front-Matter: title/date/tags)
- Button "Tags generieren" erzeugt Vorschläge per einfacher Heuristik (`/autotags`)
- Feedback/Autoupdater-Einträge werden in `netmaster_wiki/feedback.json` gesammelt (`/feedback`)

Schnellstart:

```bash
cd netmaster_wiki
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python app.py
# Öffne http://127.0.0.1:5000
```

Use-cases für Agenten:
- Beim Scaffolding: fülle `pages/` mit initialen HowTo‑Markdowns.
- Nach Änderungen an `VERSION`/`CHANGELOG.md`: erstelle optional einen Release-Eintrag im Wiki.
- Autoupdater-Feedback kann via UI oder POST an `/feedback` eingereicht werden.

Dateien:
- `netmaster_wiki/app.py` — Hauptserver
- `netmaster_wiki/templates/` — UI-Templates
- `netmaster_wiki/static/` — CSS
- `netmaster_wiki/pages/` — gespeicherte Seiten (werden bei Bedarf angelegt)
- `netmaster_wiki/feedback.json` — gespeichertes Feedback (JSON-Array)

````
## Kurzanleitung für KI-Coding-Agenten

Dieses Projekt enthält aktuell nur minimale Metadaten (z. B. `README.md`, `LICENSE`). Es liegen keine Quellcode-Dateien, Build- oder CI-Konfigurationen vor. Verwende die folgenden, konkreten Schritte, um produktiv zu starten, Entscheidungen nachzuweisen und sinnvolle PR-Vorschläge zu machen.

1) Schnelle Repo-Discovery

- Öffne und lese `README.md` und die Projekt-Root (bereits vorhanden).
- Prüfe systematisch auf typische Build-/Sprach-Indikatoren (Beispiele):

```bash
# prüfe nach Node/Python/Go/Rust/Java/Gradle/Maven/Elterndateien
git ls-files | grep -E "package.json|pyproject.toml|requirements.txt|setup.py|go.mod|Cargo.toml|pom.xml|build.gradle|Makefile|Dockerfile" -n || true
```

- Falls keine der Dateien vorhanden ist (wie aktuell), dokumentiere das kurz in deinem PR und schlage eine sinnvolle erste Aufgabe vor (z. B. Projekt-Scaffold, README-Erweiterung, CI-Workflow).

2) Architektur & "Big Picture"

- In diesem Repository sind keine Komponenten oder Services gefunden. Wenn du neue Code-Dateien hinzufügst, beschreibe in der PR-Beschreibung immer:
  - Ziel und Verantwortlichkeit der Komponente (Input/Output, Fehlerfälle)
  - Wo Code leben soll (z. B. `src/`, `cmd/`, `pkg/` oder `lib/` je nach Sprache)
  - Minimale Lauf-/Test-Schritte zum Verifizieren

3) Projekt-spezifische Workflows (aktuell keine vorhanden)

- Da kein Build/Test definiert ist, liefere in deinem Vorschlag eindeutige, automatisierte Schritte:
  - Beispiel für Node.js: `npm install && npm test`
  - Beispiel für Python: `python -m venv .venv && .venv/bin/pip install -r requirements.txt && pytest`

- Wenn du CI hinzufügen willst, erstelle eine einfache GitHub Actions Workflow-Datei in `.github/workflows/` mit einem sehr schlanken Job (checkout + Setup + test). Verweise in der PR auf die minimalen Erfolgskriterien.

4) Konventionen & Patterns (was du hier finden/setzen sollst)

- Namenskonvention: Falls du ein Sprach-Scaffold anlegst, folge den üblichen Konventionen der Sprache (z. B. `src/` für Python/TS, `cmd/` + `pkg/` für Go). Dokumentiere die gewählte Konvention in `README.md`.
- Commit/PR-Nachrichten: kurze Titelzeile, 1–2 Zeilen Beschreibung, ein Abschnitt "How to test" mit den minimalen Schritten.

5) Integration & externe Abhängigkeiten

- Es sind keine Integration-Punkte (APIs, DBs, cloud infra) detektierbar. Wenn du solche hinzufügst, nenne in der PR:
  - Endpunkte/Umgebungsvariablen (nur Namen, keine Geheimnisse)
  - Minimal reproduzierbare Local-Run-Anleitung

6) Beispiele & Templates (benutze diese Vorlagen in PRs)

- PR-Beschreibung (kurz):
  - Was wurde geändert
  - Warum (Motivation)
  - Wie zu testen (copy-paste Befehle)

- Commit-Beispiel-Titel: `chore: scaffold project (language)` oder `feat: add initial CI workflow`

7) Wenn du unsicher bist

- Stelle eine präzise Frage in der PR-Description (z. B. "Welche Sprache bevorzugst du für dieses Projekt?") und biete 2-3 vorgeschlagene Optionen (z. B. Node.js scaffold, Python package, minimal Go module).

8) Files to reference

- `README.md` — aktuell die einzige inhaltliche Datei; erweitere sie bei allen größeren Änderungen.

---
Wenn du möchtest, kann ich sofort ein erstes Scaffolding vorschlagen (z. B. `node` oder `python`) und eine PR mit README-, CI- und Minimal-Test hinzufügen — nenne kurz welche Sprache/Stack du bevorzugst oder lass mich Vorschläge machen.

## Versionierung & Releases

Dieses Repository verwendet aktuell noch kein automatisches Release-System. Lege folgenden, einfachen Workflow an, damit Änderungen nachvollziehbar und reproduzierbar sind:

- Datei `VERSION`: enthält die aktuelle Release-Version (SemVer), z. B. `0.1.0`.
- Datei `CHANGELOG.md`: chronologische Liste von Releases mit kurzen Beschreibungen.
- Release-Prozess (manuell für Start):

```bash
# 1. Inkrementiere VERSION (z. B. 0.1.0 -> 0.1.1)
echo "0.1.1" > VERSION
# 2. Ergänze CHANGELOG.md mit Einträgen für die neue Version
# 3. Commit + Tag
git add VERSION CHANGELOG.md
git commit -m "chore(release): bump version to 0.1.1"
git tag -a v0.1.1 -m "Release v0.1.1"
git push --follow-tags
```

Hinweis für Agenten: Verwende SemVer (MAJOR.MINOR.PATCH). Schreibe in Pull Requests kurz in den Titel oder das Release-Issue, welche SemVer-Schritte erforderlich sind (z. B. `patch` für Bugfixes, `minor` für neue Features, `major` für breaking changes).

Automatisierungsempfehlung: Später kann eine GitHub Actions-Workflowdatei (z. B. `.github/workflows/release.yml`) hinzugefügt werden, die bei Merge in `main` automatisch die Version taggt und ein GitHub Release erstellt.

## Issue-Vorlage für Releases

Im Ordner `.github/ISSUE_TEMPLATE/` liegt eine Vorlage, die verwendet werden soll, um Release/Version-Requests einheitlich zu erfassen. Nutze diese Vorlage, wenn du ein Release anstößt oder eine Versionserhöhung vorschlägst.

---

