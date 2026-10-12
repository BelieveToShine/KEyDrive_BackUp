# Azure category — roadmap

Status of all 19 planned concepts. **Update this table in the same commit that flips a concept's
journey-map node and concept-list row from locked to written** (and adds its slug to
`assets/journeys.json` and its entries to `assets/concepts-index.json`, and its claims to
`claims-ledger.md`) — never a follow-up task, per `../../rules/content-structure.md`,
`../../rules/navigation.md` and `../../rules/page-production-workflow.md`.

| # | Concept | Status | Page(s) |
|---|---|---|---|
| 1 | Tenants, Subscriptions & Resource Groups | ✅ Written | `azure/concepts/resource-hierarchy.html` |
| 2 | Regions & Availability Zones | ✅ Written | `azure/concepts/regions-availability-zones.html` |
| 3 | Identity & Access | ✅ Written | `azure/concepts/identity-access.html`, `azure/concepts/managed-identities.html` (Managed Identities) |
| 4 | Virtual Networks | ✅ Written | `azure/concepts/virtual-networks.html`, `azure/concepts/private-endpoints.html` (Private Endpoints) |
| 5 | Compute | ✅ Written | `azure/concepts/compute.html` |
| 6 | Storage | ✅ Written | `azure/concepts/storage.html`, `azure/concepts/blob-storage.html` (Blob Storage in Depth) |
| 7 | Databases | ✅ Written | `azure/concepts/databases.html`, `azure/concepts/cosmos-db-vs-azure-sql.html` (Cosmos DB vs Azure SQL) |
| 8 | Load Balancing & Traffic Routing | ✅ Written | `azure/concepts/load-balancing.html` |
| 9 | Scaling & Resilience | ✅ Written | `azure/concepts/scaling-resilience.html`, `azure/concepts/disaster-recovery.html` (Disaster Recovery) |
| 10 | Caching & Edge Delivery | ✅ Written | `azure/concepts/caching-edge.html` |
| 11 | Messaging & Events | ✅ Written | `azure/concepts/messaging.html`, `azure/concepts/service-bus.html` (Service Bus: Queues & Topics), `azure/concepts/event-hubs.html` (Event Hubs) |
| 12 | Serverless & Orchestration | ✅ Written | `azure/concepts/serverless-orchestration.html` |
| 13 | Infrastructure as Code | ✅ Written | `azure/concepts/infrastructure-as-code.html` |
| 14 | CI/CD & Deployment Strategies | ✅ Written | `azure/concepts/ci-cd-deployment.html` |
| 15 | Secrets & Configuration | ✅ Written | `azure/concepts/secrets-configuration.html` |
| 16 | Security & Governance | ✅ Written | `azure/concepts/security-governance.html` |
| 17 | Monitoring & Observability | ✅ Written | `azure/concepts/monitoring-observability.html` |
| 18 | Cost Management | ✅ Written | `azure/concepts/cost-management.html` |
| 19 | Well-Architected & Landing Zones | ✅ Written | `azure/concepts/well-architected.html` |

**19 / 19 written (journey complete), plus 7 deep-dive pages** (2026-10-12). Batch 1 (written first, out of order, at the user's
request): Storage, Databases, Messaging & Events. Batch 2 (roadmap order): concepts 1–5 — the whole foundation
(hierarchy, regions, identity, networking, compute). Batch 3 (roadmap order): 8 Load Balancing, 9 Scaling & Resilience (+ Disaster Recovery), 10 Caching & Edge. Batch 4 (roadmap order): 12 Serverless, 13 Infrastructure as Code, 14 CI/CD. Batch 5 (roadmap order): 15 Secrets & Configuration, 16 Security & Governance. Batch 6 (roadmap order): 17 Monitoring & Observability, 18 Cost Management, 19 Well-Architected & Landing Zones.

Slug convention: kebab-case of the concept name (the slugs for all 19 are fixed in `assets/journeys.json`).

**Next:** none planned. Open items: verify the 🟨 rows in `claims-ledger.md` (see its "Open verification list"), apply user corrections from production review, then the AWS category.
Verify every fact first (`../../rules/fact-check-and-currency.md`).
