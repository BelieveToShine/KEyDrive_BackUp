# Verification — what the tools check, how to run them, and what they cannot see

Two scripts and one habit. Run all three before you call any page done.
(Requirements: Node 18+, `playwright` + a Chromium — in the cloud sandbox `NODE_PATH=$(npm root -g)`
and `/opt/pw-browsers/chromium` already work. The site must be served over **http**: the bottom bar
and search `fetch()` JSON, which fails on `file://`.)

```bash
python3 -m http.server 5900 &                                  # from the repo root
node scripts/check-site.js [category]                          # structure + facts cross-check (no browser)
NODE_PATH=$(npm root -g) node scripts/diagram-lint.js http://localhost:5900 azure/concepts/storage.html …
NODE_PATH=$(npm root -g) node scripts/shoot-diagrams.js http://localhost:5900 azure/concepts/storage.html /tmp/st
```
Do **not** `pkill -f "http.server 5900"` from the same shell command that started it — the pattern
matches your own command line and kills the shell. Use a unique port per session and leave it running.

## 1. `scripts/check-site.js` — wiring and the claims cross-check

| Check | Fails (ERROR) when |
|---|---|
| Links | an `href`/`xlink:href` points at a missing file, or `#id` is missing in the target page |
| Search index | a page/anchor in `concepts-index.json` does not exist; duplicate ids; a concept page lacks its top-level, `#recall` or `#trap` entry |
| Journeys | `written` ⊄ `order`; a written slug has no file; a file is in neither `order` nor `sub`; a sub page lacks `subTitles`; a title is missing |
| Concept pages | missing `#why/#recall/#trap/#next`; wrong `data-root`; missing `site.js`; `<title>` not ending "— KeyDrive"; eyebrow number ≠ position in `order`; next box is not a real link to the next **written** concept / not `.next-box.locked` when the next one is unwritten; undefined SVG marker; duplicate marker ids; figcaption not starting "What you're seeing:"; placeholder text |
| Hubs | node/row counts ≠ `order`; `done` counts ≠ `written`; no link to a written concept; footer count wrong (WARN) |
| **Volatile claims (WARN)** | a number+unit, price, year, percentage, "N by default/tries", or a word like preview/deprecated/retired appears in page text but **not** in `docs/specs/<cat>/claims-ledger.md` |

Treat every WARN as a to-do: add the claim to the ledger with a status (and fix the page if the
claim cannot be supported). Do not silence the scanner.

## 2. `scripts/diagram-lint.js` — geometry of every SVG

Runs in a real browser (real fonts), opens every `<details>`, and measures each `svg.concept-diagram`:

| Issue | Meaning |
|---|---|
| `bounds` | something leaves the viewBox |
| `text-overflow` | text does not fit inside its box with a 3 px margin |
| `text-on-box` / `text-overlap` | free text overlaps a box / other text |
| `box-overlap`, `zone-straddle` | boxes overlap, or a box crosses a dashed container's border |
| `pill-text`, `pill-on-box`, `pill-on-text`, `pill-overlap` | a label capsule is too small, touches a box/text, or collides with another label |
| `pill-near-tip`, `pill-on-tip` | a label sits within 14 units of an arrowhead (the "arrow does not read as arriving" bug) or covers it |
| `arrow-end` | an arrowhead does not touch a box or container edge (the "arrows not touched" bug that shipped twice) |
| `arrow-start` | an arrow starts in empty space |
| `arrow-through-box`, `arrow-through-text` | a connector runs across a node or label |

**Prove the linter works** (do this after changing it): `node scripts/diagram-lint.js
http://localhost:5900 scripts/fixtures/broken-diagram.html` must report ~12 issues and exit 1.
A clean run on a *good* page plus a loud run on the fixture is the acceptance test.

Conventions it depends on: `rect.bx` node, `rect.zone` container, `g.arrow-pill` label, arrows are
`path[marker-end]`. Hand-written diagrams must use the same classes (see `diagram-style.md`).

## 3. The habit — look at it

`scripts/shoot-diagrams.js` writes one 2× PNG per figure. Open each and check, with your own eyes:
- every arrowhead meets a box; every label names the relationship the arrow shows;
- a reader could get the idea in 5–10 s; nothing relies on the caption to make sense;
- colours carry meaning consistently (cyan core, violet processing, emerald success, rose failure, amber events/warnings).

Tools cannot judge *meaning*: an arrow can be perfectly drawn and still say the wrong thing. The
Azure SAS-flow diagram, for example, first had a box ("SAS link") floating with no arrow — the
linter had nothing to flag, the eyes did.

## 4. Navigation test (Playwright, ~2 minutes)

1. Hub scrolled down → click a written concept → Back pill present ("Back to <Hub>").
2. Click Back → same scroll position, no Back pill, clean URL.
3. Concept → bottom-bar Next (real page) → Back returns to the first page.
4. A neighbour that is not written yet shows a 🔒 "Coming soon" cell (not a dead link).
5. Sub page: bar shows Main concept / Previous or Next deep dive / ↑ hub.
6. 390 px width: bar stays one row.

## What the tools cannot check (human duties)

Truth of the facts (ledger + official docs), clarity of the prose, whether the page's story fits the
journey, accessibility of colour contrast beyond the project palette, and mobile feel. The QA
checklist (`docs/checklists/concept-page-qa.md`) covers these.
