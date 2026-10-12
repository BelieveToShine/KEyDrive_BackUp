# Azure category — overview

## Status

Hub page, full roadmap and the **first batch of pages** are done: 3 / 19 concepts (Storage, Databases,
Messaging & Events) + 4 deep dives (Blob Storage in depth, Cosmos DB vs Azure SQL, Service Bus, Event Hubs). Added at the user's
explicit request (2026-10-12), which lifts the platform-wide "don't start a new category without
being asked" rule for this category only.

## What's built

- `azure/concepts/*.html` — 7 pages (see `roadmap.md`), each with decision-first content: pick-cards, decision tree, comparison table, scenarios, strengths/watch-outs, 21 diagrams in total. Facts are logged in `claims-ledger.md`.
- `azure/index.html` — category hub: hero, the 19-node journey-map diagram (written nodes are links, the rest locked) (every connector
  labeled with the limit that made the next concept necessary, two grouping containers, legend)
  and the full concept list with 🔒 planned badges. Nodes and rows are not links yet.
- A "Roadmap" tile on the platform home (`index.html`), directly after the Cloud Systems placeholder.
- This spec folder.

## Decisions

- **Perspective:** developer growing into architect — the journey follows one app from first
  deployment to a well-architected system, not a service-by-service catalogue.
- **Shared shape with the sister category** (AWS): identical 19-step order and hub layout, only service
  names differ, so a learner can carry the mental model between clouds.
- **Hub generated once, then hand-maintained.** The SVG was laid out from a script for consistent
  spacing, but the committed HTML is the source of truth (no build step). When a concept ships,
  edit the hub by hand per `../../rules/content-structure.md` (node → `.done` + `<a class="jm-hit">`,
  row → `.done` with a real link, connector → `.done`).

## Deferred (category-specific, on top of the platform-wide list)

Concept pages themselves; per-service deep dives; pricing figures (change often — never hard-code);
certification-exam mapping.

## Verification done on the hub

Rendered in headless Chromium at 3× and every connector junction zoomed (both splits, both
merges, spine arrows): arrowheads meet box edges, pills clear all boxes/containers.

## First-batch decisions (2026-10-12)

- **Order**: Storage, Databases and Messaging were written first because the user asked for them; the rest of the
  journey is unchanged.
- **Verification**: direct fetches of Microsoft Learn were blocked in the sandbox; claims were checked with
  searches restricted to `learn.microsoft.com` and logged in `claims-ledger.md`. 🟨 K rows (listed at the bottom
  of the ledger) still need a human or docs-enabled session.
- **Left out on purpose** (sources conflicted or volatile): prices, SLA percentages, quotas, Hyperscale auto-pause,
  retirement dates, Event Hubs retention numbers.
- **Tooling added** for this and future categories: `scripts/check-site.js`, `scripts/diagram-lint.js`,
  `scripts/shoot-diagrams.js`, `scripts/page-kit/` — see `docs/rules/verification.md`.
