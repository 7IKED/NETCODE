---
name: Release / Version bump
about: Verwende diese Vorlage, um eine neue Version oder Release anzufragen.
title: "chore(release): bump version to <new-version>"
labels: release
assignees: ''
---

## Ziel

Welche Version soll veröffentlicht werden? (SemVer)

- Neue Version: `0.1.1`

## Änderungen

Kurze Liste der Änderungen, die in diesem Release enthalten sind (linke PRs oder Commits):

- PR #12 — Fix: something
- PR #11 — Feat: add scaffold

## Risiko und Rollback

Gibt es breaking changes? Wie kann man zurückrollen?

## Release-Steps (für Maintainer)

1. Update `VERSION` auf die neue SemVer
2. Ergänze `CHANGELOG.md` mit einem Abschnitt für die Version
3. Commit, Tag und Push (siehe `.github/copilot-instructions.md`)
