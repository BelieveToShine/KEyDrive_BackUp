# Concept page QA checklist

Tick every box before reporting a page done. Copy the list into your working notes; do not skip
items because "it looks fine". Tools referenced live in `scripts/` — see `docs/rules/verification.md`.

## Content
- [ ] H1 is one crisp sentence stating the idea (not a topic label); sub-line is plain English.
- [ ] "Why did this need to exist?" starts from the limit of the previous concept; not generic.
- [ ] Simple English: sentences mostly ≤ 20 words; every term defined where first used; no unexplained acronym.
- [ ] Each option says when to pick it **and** when to look elsewhere; trade-offs are honest.
- [ ] Real-world scenarios are concrete (a named situation → the answer), 4–6 of them.
- [ ] Recall, "Say this in an interview", Common trap and confuse-pair all teach something specific to this page.
- [ ] Code example is labelled illustrative; API names recorded in the ledger as K or V.
- [ ] No unsupported absolute ("always", "never", "only", "unlimited", "best").

## Facts
- [ ] Every claim is in `docs/specs/<cat>/claims-ledger.md` with a status; V rows have a URL.
- [ ] No price, SLA %, quota or preview feature unless verified; retired/renamed services checked.
- [ ] 🟨 K rows added to the ledger's "Open verification list" and mentioned in the report to the user.
- [ ] `.fact-note` present with stable doc-root links only.

## Diagrams (each one)
- [ ] Teaches the idea in 5–10 s without the prose; Type A (real model) first.
- [ ] Every arrow has a pill label naming the real relationship; arrows end on a box/container edge.
- [ ] `node scripts/diagram-lint.js …` → 0 issues.
- [ ] Viewed at 2× via `scripts/shoot-diagrams.js`; every junction, label and arrowhead looked at.
- [ ] Caption begins "What you're seeing:" and matches what is drawn.
- [ ] No circled digits in labels; no text below 8.5 px; contrast readable on the dark background.

## Navigation and wiring
- [ ] `journeys.json` (written / sub / subTitles), `concepts-index.json` (3 entries), hub node + row, previous page's `#next`.
- [ ] Bottom bar shows correct Previous / Next (locked cell for unwritten); Back pill appears after a click-through and returns to the same scroll position.
- [ ] `node scripts/check-site.js <cat>` → 0 errors, warnings understood.
- [ ] Roadmap, overview, `docs/keydrive-overview.md` and `CLAUDE.md` status updated in the same commit.

## Look and feel
- [ ] Desktop and 390 px widths: no horizontal scroll except tables/diagrams that scroll by design.
- [ ] Hover/press states of any new clickable element screenshotted (`interaction-style.md`).
- [ ] Reduced-motion respected (no new animation without it).

## Report
- [ ] Told the user what was verified how, what was **not** verified, and what was left out.
