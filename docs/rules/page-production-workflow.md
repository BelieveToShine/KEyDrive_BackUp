# Page production workflow — how to write a concept page, start to finish

The step-by-step a session follows for **any** concept page in **any** category (Azure was the first
cloud category written this way; AWS and others should follow it exactly). Each step names the file
that has the detail. Do the steps in order — skipping research or verification is how wrong facts and
broken diagrams shipped before.

> **Read first, every session:** `CLAUDE.md` → `docs/rules/accuracy.md` →
> `docs/rules/fact-check-and-currency.md` → this file → `docs/rules/cloud-category-playbook.md`
> (if it is a cloud category) → `docs/rules/content-writing.md` + `diagram-style.md`.

## Step 0 — Make sure you are allowed to start

- The user must have asked for these pages (`CLAUDE.md` "Explicitly deferred" list still applies).
- Open the category's `docs/specs/<cat>/roadmap.md` and `concept-taxonomy.md`: which concept is next,
  and why it exists. Do not reorder concepts without discussion.
- If the user names topics out of order (Azure: Storage, Databases, Messaging first), write them —
  the navigation supports unwritten neighbours (locked "coming soon" cells) — but record it in the roadmap.

## Step 1 — Decide the page set (main page + deep dives)

- **One main page per taxonomy concept.** It answers "why does this exist, and which option do I
  pick?" with a decision diagram.
- **Add a deep-dive sub page** when (a) a concept holds two or more things people confuse
  (Cosmos DB vs Azure SQL), or (b) one service has its own vocabulary worth a page (Service Bus
  queues/topics, Event Hubs partitions). Sub pages are registered in `journeys.json` → `"sub"`.
- Keep each page to one idea a learner can finish in ~10 minutes. Split before you bloat.
- Write the page list into the roadmap before building.

## Step 2 — Research and build the claims ledger (BEFORE writing prose)

Follow `fact-check-and-currency.md`. In short:
1. Search the provider's own documentation (see the file for the exact method and domains).
2. For every claim you intend to make, write a row in `docs/specs/<cat>/claims-ledger.md`
   (✅ V verified with URL / 🟨 K knowledge-based / 🟦 I illustrative / 👤 U from the user).
3. Drop or soften any claim you cannot support. Never state prices, SLA percentages, quotas or
   preview features unless verified from the official page — and then still prefer wording that
   survives change ("a limited window that depends on the tier").
4. Record conflicts between sources and **leave the contested claim out** (Hyperscale auto-pause was
   described both as preview and as unsupported — it was left out).

## Step 3 — Outline with the standard template

Main concept page, in this order (details: `content-writing.md`):

| # | Section | Notes |
|---|---|---|
| 1 | Hero: eyebrow `Concept N of T · <group>`, one-sentence H1 with a `.grad-text` phrase, plain-English sub, ❓ interview question | H1 states the idea; it does not just name the topic |
| 2 | 👁 **See it first** — the primary diagram | must teach in 5–10 seconds; caption starts "What you're seeing:" |
| 3 | 🎯 One-sentence takeaway (`.one-sentence`) | |
| 4 | 📖 **Why did this need to exist?** (`#why`) | starts from the limit of the previous concept |
| 5 | Core body (cloud decision pages): 🧰 **pick-cards** per option (use / look elsewhere) → 🧭 **decision-tree diagram** → 📊 comparison table → 🎬 **real-world scenarios** → ⚖️ pros/cons → 🔬 **Go deeper** cards to sub pages | skip blocks that would not teach something specific |
| 6 | `<details class="zoom">` "Go one level deeper" | closed by default |
| 7 | 🔥 Recall (`#recall`) · 🎤 Say this in an interview · ⚠️ Common trap (`#trap`) · `.confuse-pair` | |
| 8 | 💻 Tiny illustrative example (zoom) — labelled illustrative | verify API names; mark K in the ledger |
| 9 | ➡️ Where this leads (`#next`) — real link if the next concept is written, `.next-box.locked` if not | `check-site.js` enforces this |
| 10 | 📌 `.fact-note` — "check the official docs" with links to **stable section roots** | never deep-link a URL you did not see |

Sub pages: same skeleton, eyebrow `Deep dive · <Parent> · <icon> <topic>`, crumbs include the parent
concept, `#next` points back to the parent (the bottom bar handles "next deep dive").

## Step 4 — Design the diagrams

Follow `diagram-style.md` (highest-priority rule). For cloud pages the standard set is:
- **Primary**: the system picture (what the service *is*, e.g. the four doors of a storage account).
- **Decision tree**: ordered yes/no questions → answer boxes, with the upgrade path shown.
- **Mechanism / lifecycle**: how it actually behaves (peek-lock lifecycle, partition log, tiers).
- **Contrast**: two panels side by side (message vs event, mailbox vs log, good key vs bad key).
- **Use both**: a polyglot picture when several services belong in one system.

Rules of thumb that the linter enforces: every arrow ends on a box or container edge; every arrow has
a pill label; pills never touch boxes and sit ≥14 units from an arrow tip; text fits its box with
3 px to spare; nothing leaves the viewBox; no arrow runs through a box or text. Put long labels
**beside** a vertical line, not on it. Use plain numerals in pills.

Use `scripts/page-kit` (optional) to write them — see its README.

## Step 5 — Write the copy in simple English

- Short sentences (aim ≤ 20 words). One idea per sentence. Active voice, "you".
- Define a term the first time it appears, in the same sentence, with a picture-able comparison
  (a post office, a doorbell, a tape recorder). Analogies **support** the technical model; never
  replace it (`diagram-style.md` "Type A vs Type B").
- Headings promise something ("Decide in 30 seconds", "Keep it locked down") — not "Overview".
- Use real scenarios with named situations, not abstractions.
- Say what each option is **not** good for. Honest trade-offs build trust.
- Emoji are signposts (one per heading / card), not decoration in running text.
- Never write "always/never/best" unless the docs do.

## Step 6 — Build, lint, and LOOK

```bash
python3 scripts/page-kit/build.py <cat> <module>:<name>          # or hand-write the HTML
python3 -m http.server 5900 &                                    # always serve over http
NODE_PATH=$(npm root -g) node scripts/diagram-lint.js http://localhost:5900 <cat>/concepts/<page>.html
NODE_PATH=$(npm root -g) node scripts/shoot-diagrams.js http://localhost:5900 <cat>/concepts/<page>.html /tmp/shot
```
Open **every** screenshot and check each junction, label and caption. The linter catches geometry; only
eyes catch "this arrow means something different from what the label says". Fix → re-lint → re-look.

## Step 7 — Wire the page into the site (same commit)

| Where | What |
|---|---|
| `assets/journeys.json` | add the slug to `written` (main page) or `sub` + `subTitles` (deep dive); new category → full entry |
| `assets/concepts-index.json` | three entries per page: top-level, `#recall`, `#trap` (`search-index.md`) |
| `<cat>/index.html` hub | flip the journey node to `done` + `<a class="jm-hit">`; flip the concept row to `done` with links (deep dives in `.cr-subs`); update the hub note and footer counts |
| Previous written concept's `#next` box | link to this page if it is now the next written concept |
| `docs/specs/<cat>/roadmap.md`, `overview.md`, `docs/keydrive-overview.md`, `CLAUDE.md` "Current state" | status |
| `docs/specs/<cat>/claims-ledger.md` | every claim + every number on the page |

## Step 8 — Verify (all must pass before you say "done")

1. `node scripts/check-site.js <cat>` → **0 errors**, and every warning understood (volatile-claim
   warnings are cleared by adding the claim to the ledger — not by deleting the check).
2. `scripts/diagram-lint.js` → 0 issues on every changed page.
3. Every diagram viewed at 2× (Step 6). Hover/press states for any new clickable element screenshotted.
4. Page read top to bottom at desktop width and at 390 px; bottom bar and Back pill tested
   (`navigation.md` verification list).
5. `docs/checklists/concept-page-qa.md` ticked item by item.
6. `scripts/layout-check.js` → "layout OK" and a phone-width look (see `lessons-learned.md`).

## Step 9 — Commit and push

- One commit per logical change, message says what and why; pages + wiring + docs together.
- Branch rules: follow the session's instructions; this project is also deployed from `main` and the
  baseline branch — if the user asks for "push to main", push to both (fast-forward only).
- Do **not** open a PR unless asked.

## Step 10 — Report honestly

Tell the user: what was written, how facts were verified (and what could **not** be verified —
list the 🟨 K rows), what the linter and checker reported, and anything you left out and why.
Never say "verified against the docs" for a claim you only recalled.

## Kick-off prompt for a fresh session (copy/paste)

> Read CLAUDE.md, then docs/rules/page-production-workflow.md and follow it exactly. Category: `<aws>`.
> Write the pages listed in docs/rules/cloud-category-playbook.md → "AWS page set". Use the Azure
> pages as the quality bar, scripts/page-kit/azure as the working example, and docs/specs/azure/
> claims-ledger.md as the ledger format. Verify facts only against official AWS documentation;
> list anything unverified. Run scripts/check-site.js and scripts/diagram-lint.js; view every diagram.
