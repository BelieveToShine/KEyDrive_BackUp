# AWS category — roadmap

Status of all 19 planned concepts. **Update this table in the same commit that flips a concept's
journey-map node and concept-list row from locked to written** (and adds its slug to
`assets/journeys.json` and its entries to `assets/concepts-index.json`) — never a follow-up task,
per `../../rules/content-structure.md` and `../../rules/navigation.md`.

| # | Concept | Status | Page |
|---|---|---|---|
| 1 | Accounts & Organizations | ✅ Written | `aws/concepts/accounts-organizations.html` |
| 2 | Regions & Availability Zones | ✅ Written | `aws/concepts/regions-availability-zones.html` |
| 3 | Identity & Access (IAM) | ✅ Written | `aws/concepts/identity-access.html`, `aws/concepts/iam-roles.html` (IAM Roles) |
| 4 | VPC Networking | ✅ Written | `aws/concepts/vpc-networking.html`, `aws/concepts/vpc-endpoints.html` (VPC Endpoints) |
| 5 | Compute | ✅ Written | `aws/concepts/compute.html` |
| 6 | Storage | ✅ Written | `aws/concepts/storage.html`, `aws/concepts/s3-in-depth.html` (S3 in Depth) |
| 7 | Databases | ✅ Written | `aws/concepts/databases.html`, `aws/concepts/dynamodb-vs-rds-aurora.html` (DynamoDB vs RDS and Aurora) |
| 8 | Load Balancing & Traffic Routing | ✅ Written | `aws/concepts/load-balancing.html` |
| 9 | Scaling & Resilience | ✅ Written | `aws/concepts/scaling-resilience.html`, `aws/concepts/disaster-recovery.html` (Disaster Recovery) |
| 10 | Caching & Edge Delivery | ✅ Written | `aws/concepts/caching-edge.html` |
| 11 | Messaging & Events | ✅ Written | `aws/concepts/messaging.html`, `aws/concepts/sqs-sns-eventbridge.html`, `aws/concepts/kinesis.html` |
| 12 | Serverless & Orchestration | ✅ Written | `aws/concepts/serverless-orchestration.html` |
| 13 | Infrastructure as Code | ✅ Written | `aws/concepts/infrastructure-as-code.html` |
| 14 | CI/CD & Deployment Strategies | ✅ Written | `aws/concepts/ci-cd-deployment.html` |
| 15 | Secrets & Configuration | ✅ Written | `aws/concepts/secrets-configuration.html` |
| 16 | Security & Governance | 🔒 Planned | — |
| 17 | Monitoring & Observability | 🔒 Planned | — |
| 18 | Cost Management | 🔒 Planned | — |
| 19 | Well-Architected & Landing Zones | 🔒 Planned | — |

**15 / 19 written (batches A–C, written 2026-10-12 while the user was away).** The hub page (`aws/index.html`) is built with the full locked roadmap;
concept pages come next, in the order fixed in `concept-taxonomy.md`. Slug convention: kebab-case
of the concept name, e.g. `aws/concepts/regions-availability-zones.html`.
