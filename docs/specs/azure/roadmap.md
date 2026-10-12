# Azure category — roadmap

Status of all 19 planned concepts. **Update this table in the same commit that flips a concept's
journey-map node and concept-list row from locked to written** (and adds its slug to
`assets/journeys.json` and its entries to `assets/concepts-index.json`, and its claims to
`claims-ledger.md`) — never a follow-up task, per `../../rules/content-structure.md`,
`../../rules/navigation.md` and `../../rules/page-production-workflow.md`.

| # | Concept | Status | Page(s) |
|---|---|---|---|
| 1 | Tenants, Subscriptions & Resource Groups | 🔒 Planned | — |
| 2 | Regions & Availability Zones | 🔒 Planned | — |
| 3 | Identity & Access | 🔒 Planned | — |
| 4 | Virtual Networks | 🔒 Planned | — |
| 5 | Compute | 🔒 Planned | — |
| 6 | Storage | ✅ Written | `azure/concepts/storage.html`, `azure/concepts/blob-storage.html` (Blob Storage in Depth) |
| 7 | Databases | ✅ Written | `azure/concepts/databases.html`, `azure/concepts/cosmos-db-vs-azure-sql.html` (Cosmos DB vs Azure SQL) |
| 8 | Load Balancing & Traffic Routing | 🔒 Planned | — |
| 9 | Scaling & Resilience | 🔒 Planned | — |
| 10 | Caching & Edge Delivery | 🔒 Planned | — |
| 11 | Messaging & Events | ✅ Written | `azure/concepts/messaging.html`, `azure/concepts/service-bus.html` (Service Bus: Queues & Topics), `azure/concepts/event-hubs.html` (Event Hubs) |
| 12 | Serverless & Orchestration | 🔒 Planned | — |
| 13 | Infrastructure as Code | 🔒 Planned | — |
| 14 | CI/CD & Deployment Strategies | 🔒 Planned | — |
| 15 | Secrets & Configuration | 🔒 Planned | — |
| 16 | Security & Governance | 🔒 Planned | — |
| 17 | Monitoring & Observability | 🔒 Planned | — |
| 18 | Cost Management | 🔒 Planned | — |
| 19 | Well-Architected & Landing Zones | 🔒 Planned | — |

**3 / 19 written, plus 4 deep-dive pages** (2026-10-12). The first batch was written out of order at the
user's request (they asked for Storage, Databases and Messaging first); the bottom bar and the previous
concepts' "next" boxes show unwritten neighbours as locked "coming soon" until they ship.

Slug convention: kebab-case of the concept name, e.g. `azure/concepts/regions-availability-zones.html`
(the slugs for all 19 are fixed in `assets/journeys.json`).

**Next in order when asked:** 1 Resource Hierarchy → 2 Regions & Zones → 3 Identity & Access → 4 Virtual
Networks → 5 Compute, then 8 onward. Verify every fact first (`../../rules/fact-check-and-currency.md`).
