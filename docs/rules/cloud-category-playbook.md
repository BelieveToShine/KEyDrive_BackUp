# Cloud category playbook — Azure and AWS (and any future cloud)

Azure and AWS share **one 19-concept journey** (see `docs/specs/azure/concept-taxonomy.md`); only the
service names differ. This file is the hand-over for writing the second cloud (AWS) the way the
first (Azure) was written, so nobody has to re-explain the approach. Read
`page-production-workflow.md` first — this file adds the cloud-specific parts.

## What stays identical between clouds

- Concept order, "why it exists" reasoning, hub layout and journey map (the AWS hub already exists with the full locked roadmap — flip nodes/rows to `done` as pages ship).
- Page skeleton and the **decision-first** shape: pick-cards → decision tree → comparison table → scenarios → pros/cons → deep dives.
- The diagram types (primary / decision tree / mechanism / contrast / use-both) and the colour language.
- Simple-English voice, scenarios, honest trade-offs, the fact-check procedure and ledger.
- Navigation wiring (`journeys.json`, hub rows, search index).

## What changes per cloud

- Service names, defaults, tiers and limits — **every one re-verified** against that cloud's own docs.
- The deep-dive pages (which confusions are classic in that cloud).
- The ledger (`docs/specs/<cat>/claims-ledger.md`) and the doc-root links in each `.fact-note`.
- The category folder: `<cat>/index.html`, `<cat>/concepts/`, `docs/specs/<cat>/`, `scripts/page-kit/<cat>/` (copy `azure/`).

## Parity map — Azure page ↔ AWS page set (starting points to verify, not facts to copy)

| Concept | Azure pages written | AWS pages to write | AWS services to cover (verify names/tiers/limits in AWS docs) |
|---|---|---|---|
| 6 Storage | `storage` + `blob-storage` | `storage` + `s3-in-depth` | S3, EBS, EFS (and FSx) as the "doors"; S3 storage classes + lifecycle rules; presigned URLs ≈ SAS; S3 event notifications / EventBridge; redundancy = the S3 durability model + Multi-AZ / cross-Region replication; access = IAM + bucket policies, Block Public Access |
| 7 Databases | `databases` + `cosmos-db-vs-azure-sql` | `databases` + `dynamodb-vs-rds-aurora` | RDS engines, Aurora, DynamoDB (+ ElastiCache pointer); partition key / capacity modes / consistency choices in DynamoDB; Multi-AZ vs read replicas vs global tables; "use both" picture |
| 11 Messaging & Events | `messaging` + `service-bus` + `event-hubs` | `messaging` + `sqs-sns-eventbridge` + `kinesis` | SQS (standard/FIFO, DLQ, visibility timeout ≈ peek-lock), SNS (topics/fan-out), EventBridge (event bus/rules), Kinesis Data Streams (shards ≈ partitions), Amazon MQ pointer; message vs event vs stream idea is identical |
| 1–5, 8–10, 12–19 | not yet written | follow the taxonomy | Organizations/accounts, Regions/AZs, IAM, VPC, EC2/ECS/EKS/Lambda, ELB/Route 53/CloudFront, Auto Scaling, ElastiCache/CloudFront, Step Functions, CloudFormation/CDK, CodePipeline, Secrets Manager/Parameter Store/KMS, Security Hub/GuardDuty/Config, CloudWatch/X-Ray/CloudTrail, Cost Explorer/Budgets/Savings Plans, Well-Architected |

**AWS page set for the first batch** (mirror Azure): `storage`, `s3-in-depth`, `databases`,
`dynamodb-vs-rds-aurora`, `messaging`, `sqs-sns-eventbridge`, `kinesis`. Slugs are kebab-case of the
page title; sub pages go in `journeys.json` → `sub`/`subTitles`.

Terminology bridge worth teaching (one line each, verified): SAS ↔ presigned URL · peek-lock ↔ SQS
visibility timeout · partition ↔ shard · consumer group ↔ (Kinesis) consumer / enhanced fan-out ·
Event Grid ↔ EventBridge · resource group ↔ (no direct equivalent — tags / CloudFormation stacks) ·
Entra ID/RBAC ↔ IAM. State where the analogy breaks, not just where it holds.

## Writing "when to use what" pages (the user's emphasis)

1. Start from the **question the learner has** ("Cosmos DB or Azure SQL?"), not the service list.
2. Give the answer as a **picture first** (decision tree or side-by-side shapes), then words.
3. Give each option a pick-card: ✅ pick it when… / ⛔ look elsewhere when… (honest, specific).
4. Add a comparison table (≤ 9 rows) and **real-world scenarios** (6) that each end in a verdict.
5. Show **strengths and watch-outs** for both sides — the watch-outs matter more.
6. Show "use both" when real systems do (polyglot persistence; the messaging combo example).
7. Finish with recall bullets, an interview sentence, and the classic trap.
8. Put the single most important design decision in its own block with a good/bad picture
   (Cosmos partition key; for DynamoDB it will be the partition key too — draw its own version).

## Retirement / rename watch list (check before naming a service)

- Azure: PostgreSQL *Single Server* (retired → Flexible Server); Azure AD → Microsoft Entra ID; Cosmos DB branding
  ("in Azure and Fabric"); portal label "Classic file shares". Re-check Azure Cache for Redis / CDN
  product lines before writing Caching & Edge.
- AWS: start a list in `docs/specs/aws/overview.md` from AWS's own "what's new"/deprecation pages; do not
  rely on memory for any service that has been announced as closing to new customers.

## Voice samples (match this)

> "A storage account is four doors. You pick the door by the shape of your data."
> "Do not make parts of your app wait for each other — put a message in between."
> "Reading does not delete. That is a feature (replay) — but it means *you* must remember where you stopped."
