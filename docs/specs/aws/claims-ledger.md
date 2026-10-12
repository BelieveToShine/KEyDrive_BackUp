# AWS — claims ledger

Every factual claim on an AWS concept page, where it came from, and how sure we are. This is the
cross-check file for `docs/rules/fact-check-and-currency.md`. `scripts/check-site.js` warns when a
page contains a number, price, size, year or "retired/preview" word that is **not written in this
file** — so adding a number to a page without adding it here is caught.

**How the claims were checked (2026-10-12 session, written while the user was away):** direct fetches
of `docs.aws.amazon.com` are not available in the sandbox, so each risky claim was checked with web
searches restricted to `docs.aws.amazon.com` / `aws.amazon.com`; the result snippets quote AWS documentation pages
(URLs below). That is real but second-hand evidence — a human or a session with direct docs access should
still open the linked page for every row marked 🟨 and for anything you plan to quote in an interview.
Prices, discount percentages, quotas and retirement dates are deliberately left off the pages.

Legend: ✅ V verified against AWS documentation via search snippet · 🟨 K knowledge-based, not verified here ·
🟦 I illustrative (made-up names/numbers in examples and diagrams) · 👤 U user-supplied.

## Accounts & Organizations (`accounts-organizations.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| AC1 | An organization is a tree: root, OUs, accounts; a management account, zero or more member accounts; policies attached to a node flow down | ✅ V | `/organizations/latest/userguide/orgs_getting-started_concepts.html` |
| AC2 | The management account creates the organization (cannot be changed), pays all charges; AWS recommends keeping workloads out of it; SCPs do not apply to it | ✅ V | same page |
| AC3 | A member account belongs to one organization; an account is in exactly one OU; an OU has one parent | ✅ V | same page |
| AC4 | SCPs never grant; effective permissions are the overlap of SCPs and IAM policies | ✅ V | same page |
| AC5 | Consolidated billing: one bill, shared volume discounts, Reserved Instance discounts and Savings Plans; "All features" (default) adds policies and integrations | ✅ V | `/awsaccountbilling/latest/aboutv2/consolidated-billing.html` |
| AC6 | Separate accounts limit blast radius ("two levels"/"60 seconds" are reading-time or counting words, not claims) | 🟨 K | AWS multi-account whitepaper (`/whitepapers/latest/organizing-your-aws-environment/`) supports the practice; wording is ours |
| AC7 | `aws organizations create-account` flags | 🟨 K | |
| AC-I | OU and account names (Production, Dev, App A/B), e-mail example | 🟦 I | |

## Regions & Availability Zones (`regions-availability-zones.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| RG1 | A Region is a geographic area designed to be isolated from other Regions; resources are regional by default and cross-Region replication is not automatic | ✅ V | `/global-infrastructure/latest/regions/aws-regions.html`, global infrastructure page |
| RG2 | Each Region has a minimum of three AZs ("three zones" in the diagrams is the teaching example); each AZ has its own power, cooling, physical security, linked by redundant low-latency networks | ✅ V | `aws.amazon.com/about-aws/global-infrastructure/regions_az/` |
| RG3 | AZs are up to about 100 km apart: far enough to avoid common local disasters, close enough for synchronous replication | ✅ V | same page |
| RG4 | Regions launched after 2019 (after March 20, 2019) must be enabled before use; older Regions are on by default | ✅ V | AWS Regions docs |
| RG5 | Local Zones extend Regions closer to users; Wavelength Zones serve 5G devices | ✅ V | Regions/AZ user guide |
| RG6 | AZ letters map to physical zones per account; use zone IDs to line up accounts | 🟨 K | |
| RG7 | "At least two zones" as the resilience baseline | 🟦 I | our guidance, consistent with multi-AZ design docs |
| RG8 | `aws ec2 describe-availability-zones` flags; `eu-west-1` | 🟨 K | example Region |
| RG-I | AZ a/b/c diagram; scenarios | 🟦 I | |

## Identity & Access and IAM Roles (`identity-access.html`, `iam-roles.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| IM1 | Humans should use federation / temporary credentials; IAM Identity Center is the recommended way to manage access to accounts; workloads use roles with temporary credentials | ✅ V | `/IAM/latest/UserGuide/best-practices.html` |
| IM2 | Least privilege: start with AWS managed policies then customer managed; IAM Access Analyzer can generate policies; last-accessed data finds unused permissions | ✅ V | same page |
| IM3 | Root user: only for tasks that require it; MFA; no root access keys; remove root credentials from member accounts in an organization | ✅ V | `/IAM/latest/UserGuide/root-user-best-practices.html` |
| IM4 | Deny by default; explicit deny always wins | ✅ V | IAM policy evaluation logic docs |
| IM5 | A role needs a trust policy and a permissions policy; EC2 uses an instance profile that holds one role; credentials come from instance metadata and are renewed at least five minutes before expiry | ✅ V | `/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html`, `/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html` |
| IM6 | AssumeRole returns an access key ID, secret access key and session token; session permissions are the intersection of the role policy and session policies | ✅ V | `/STS/latest/APIReference/API_AssumeRole.html` |
| IM7 | Launching with a role needs iam:PassRole (scope with iam:PassedToService); replace the instance profile rather than removing the role; changes can take up to an hour | ✅ V | EC2 role docs |
| IM8 | EC2 workloads need not call AssumeRole for their own instance role | ✅ V | same docs |
| IM9 | Cross-account flow (caller → STS → role in other account trusting the caller) | ✅ V (concept), 🟦 I (drawing) | STS docs |
| IM10 | `aws sts get-caller-identity`, `aws sts assume-role` flags; account ID 111122223333 | 🟨 K / 🟦 I | |
| IM-I | Policy JSON example (`s3:GetObject`, bucket `reports`) | 🟦 I | |

## VPC Networking and VPC Endpoints (`vpc-networking.html`, `vpc-endpoints.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| VP1 | Public subnet has a direct route to an internet gateway; private subnet does not and needs a NAT device; route tables pair destinations with targets; a subnet lives in one AZ | ✅ V | `/vpc/latest/userguide/how-it-works.html`, `/configure-subnets.html` |
| VP2 | NAT gateway allows outbound connections from private subnets and blocks unsolicited inbound | ✅ V | VPC docs |
| VP3 | Security groups: resource level, stateful, allow rules only, all rules evaluated; network ACLs: subnet level, stateless, allow and deny, rules in ascending order; AWS suggests ACLs as a secondary control | ✅ V | `/vpc/latest/userguide/vpc-security-groups.html`, `/vpc-network-acls.html` |
| VP4 | VPC peering is point-to-point, not transitive; hybrid links on one VPC cannot be borrowed by a peer; Transit Gateway supports transitive routing and attaches VPNs and Direct Connect | ✅ V | `/vpc/latest/peering/vpc-peering-basics.html`, Transit Gateway docs |
| VP5 | Gateway endpoints: only S3 and DynamoDB, no PrivateLink, routes in route tables, no additional cost, not reachable from on-premises, other-Region peered VPCs or transit gateways | ✅ V | `/vpc/latest/privatelink/gateway-endpoints.html` |
| VP6 | Interface endpoints: PrivateLink, ENIs with private IPs, many services, reachable from on-premises and peered VPCs/transit gateways, hourly plus data charges | ✅ V | `/vpc/latest/privatelink/concepts.html` |
| VP7 | Both endpoint types can be used for S3 in one VPC; endpoint policies; security groups on interface endpoints | ✅ V (first), 🟨 K (rest) | |
| VP8 | NAT gateways and connectivity options are billed by hour and data | 🟨 K | no prices on the page |
| VP9 | `aws ec2 create-vpc` / `create-subnet` / `create-vpc-endpoint` flags; 10.0.0.0/16, 10.0.1.0/24; eu-west-1 | 🟦 I / 🟨 K | |
| VP-I | Diagrams, scenarios, "thirty VPCs" | 🟦 I | |

## Compute (`compute.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| CP1 | App Runner = simplest way to put a web app/API online from image or source; Elastic Beanstalk = web apps, manages the EC2 runtime and patching; ECS = AWS-native, more control over networking and security; EKS = managed Kubernetes; Fargate = serverless compute for ECS/EKS; EC2 = most control; Lambda = event-driven functions | ✅ V | `/decision-guides/latest/containers-on-aws-how-to-choose/choosing-aws-container-service.html`, `/compute-on-aws-how-to-choose/choosing-aws-compute-service.html` |
| CP2 | Start at the managed end (App Runner or Fargate) and move toward self-management only when needed | ✅ V | `/whitepapers/latest/containers-on-aws/containers-services-on-aws.html` |
| CP3 | ECS and EKS can run on Fargate or EC2 | ✅ V | AWS containers blog (ECS vs EKS) |
| CP4 | Fargate vs EC2 is mainly cost: Fargate for spiky, EC2 for steady highly utilised | ✅ V | AWS containers blog (cost optimisation by launch type) |
| CP5 | Lambda fits short, bursty tasks better than long-running services | ✅ V | `/decision-guides/latest/decision-guides/fargate-or-lambda.html` |
| CP6 | On EC2 you patch the guest OS | 🟨 K | shared-responsibility model |
| CP7 | `aws ec2 run-instances` flags; `t3.micro` instance type | 🟨 K | example type |
| CP-I | Scenarios, "ten services" | 🟦 I | |

## Illustrative phrases the checker flags (🟦 I — scenario wording, not claims)

Batch A: "Only two Regions" (scenario: a law allows two Regions) · "30 minutes" (scenario: temporary admin for half an hour) · "at least two zones" (our resilience baseline, see RG7) · "60 seconds" (reading-time label on every page).

## Storage and S3 in Depth (`storage.html`, `s3-in-depth.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| ST1 | Block (EBS) for a single host, file (EFS, FSx) for shared access, object (S3) for web-scale API access; S3 bucket = container for objects | ✅ V | `/decision-guides/latest/storage-on-aws-how-to-choose/choosing-aws-storage-service.html`, `/AWSEC2/latest/UserGuide/Storage.html` |
| ST2 | EBS data stored redundantly within a single AZ; EFS via NFSv4 with hierarchical directories; FSx offers Windows File Server, Lustre, NetApp ONTAP, OpenZFS; EFS has an archive class | ✅ V | same pages, EFS docs |
| ST3 | Object storage is not suited to active write-heavy file workloads (whole-object writes, no POSIX locking) | ✅ V (blog) | AWS gametech blog on storage backends |
| ST4 | Storage classes: Standard (frequent, ms), Intelligent-Tiering (unknown/changing; per-object monitoring fee; small objects not monitored), Infrequent Access, Glacier Instant/Flexible/Deep Archive; One Zone-IA is not resilient to loss of the AZ | ✅ V | `/AmazonS3/latest/userguide/storage-class-intro.html`, `aws.amazon.com/s3/storage-classes/` |
| ST5 | Minimum storage durations: Glacier Instant Retrieval 90 days, Deep Archive 180 days | ✅ V | storage classes page (check current values) |
| ST6 | Lifecycle rules transition/expire objects; versioning without lifecycle grows without bound | ✅ V | S3 lifecycle docs |
| ST7 | Presigned URLs: made with SDK/CLI, GET or PUT, valid up to seven days, reusable until expiry, work without making the bucket public, revoked if the signing role is deleted | ✅ V | `/AmazonS3/latest/userguide/using-presigned-url.html` and AWS security blog |
| ST8 | Block Public Access: buckets created since April 2023 block public access by default; keep all settings on | ✅ V | `/AmazonS3/latest/userguide/access-control-block-public-access.html` |
| ST9 | Durability design does not protect against deletion; versioning and Object Lock address it | ✅ V | S3 docs |
| ST10 | Very high durability design figures exist but are deliberately not quoted | 🟦 I | |
| ST11 | `aws s3 mb`, `aws s3 cp`, `aws s3 presign --expires-in 3600` (3600 seconds = one hour) flags; bucket name `my-example-bucket-12345`; eu-west-1 | 🟨 K / 🟦 I | |
| ST-I | Scenarios, diagrams | 🟦 I | |

## Databases and DynamoDB vs RDS/Aurora (`databases.html`, `dynamodb-vs-rds-aurora.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| DB1 | RDS Multi-AZ instance: synchronous standby in another AZ, cannot serve reads; read replicas: asynchronous, for scaling reads, not autoscaled by RDS, not automatic failover targets | ✅ V | `/AmazonRDS/latest/UserGuide/Concepts.MultiAZSingleStandby.html`, `/USER_ReadRepl.html` |
| DB2 | Multi-AZ DB cluster: a writer and two readers in three AZs; readers are failover targets | ✅ V | RDS Multi-AZ docs |
| DB3 | Aurora storage: six copies across three AZs ("six copies", "three Availability Zones"), independent of instance count; tolerates losing copies without losing write availability; asynchronous readers, failover priorities | ✅ V | `/AmazonRDS/latest/AuroraUserGuide/Concepts.AuroraHighAvailability.html`, Aurora FAQ |
| DB4 | RDS handles provisioning, patching and backups; Aurora is MySQL/PostgreSQL compatible | ✅ V (first), 🟨 K (compat.) | AWS overview whitepaper |
| DB5 | DynamoDB partition key: choose high cardinality; low-cardinality keys cause hot partitions; write sharding spreads writes but complicates reads; adaptive capacity | ✅ V | `/amazondynamodb/latest/developerguide/bp-partition-key-design.html` and related |
| DB6 | A read unit = one strongly consistent read/s or two eventually consistent reads/s for an item up to 4 KB; eventually consistent reads cost half; ~3,000 read and 1,000 write units per partition ("1001" in the sample key `u-1001` is an example value) | ✅ V (4 KB, 3,000/1,000 from the best-practices pages) | same pages |
| DB7 | GSI keys can distribute differently from the base table; low-variety index keys cause write throttling | ✅ V | same pages |
| DB8 | DynamoDB global tables replicate across Regions; on-demand and provisioned capacity modes | 🟨 K | not covered by the search |
| DB9 | RDS engines list (MySQL, PostgreSQL, MariaDB, SQL Server, Oracle) | 🟨 K | |
| DB10 | `aws rds create-db-instance` flags; `db.t3.micro`; `aws dynamodb get-item` | 🟨 K / 🟦 I | |
| DB-I | Scenarios, "Carts" table, `u-1001` | 🟦 I | |

## Load Balancing & Traffic Routing (`load-balancing.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| LB1 | ALB = layer 7, HTTP/HTTPS, path-based routing; NLB = layer 4 TCP/UDP, handles bursts, keeps client source IP, fixed IP for its life; GWLB = third-party virtual appliances, needs extra integration | ✅ V | `/elasticloadbalancing/latest/userguide/how-elastic-load-balancing-works.html` and guides |
| LB2 | Classic Load Balancer is the previous generation; AWS recommends migrating to ALB/NLB; the migration wizard creates an equivalent new load balancer and you redirect traffic (no end-of-life date stated) | ✅ V | `/elasticloadbalancing/latest/userguide/migrate-classic-load-balancer.html` |
| LB3 | Route 53 policies: failover, weighted (weight 0 stops routing), latency, geolocation, geoproximity, IP-based, multivalue; health checks; weighted-as-failover sends to zero-weight records only when all non-zero are unhealthy | ✅ V | `/Route53/latest/DeveloperGuide/routing-policy.html` |
| LB4 | DNS answers can be cached so failover is not instant | 🟨 K | general DNS behaviour (Azure analogue verified) |
| LB5 | `aws elbv2 create-load-balancer` flags | 🟨 K | |
| LB-I | Scenarios | 🟦 I | |

## Scaling & Resilience and Disaster Recovery (`scaling-resilience.html`, `disaster-recovery.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| SC1 | Dynamic scaling types: target tracking (strongly recommended), step, simple (discouraged, with cooldowns); conflicts between target tracking and step policies can cause bad behaviour | ✅ V | `/autoscaling/ec2/userguide/as-scale-based-on-demand.html`, `/as-scaling-simple-step.html` |
| SC2 | Default instance warm-up: strongly recommended, not enabled by default; policy-level warm-up overrides the default | ✅ V | `/autoscaling/ec2/userguide/ec2-auto-scaling-default-instance-warmup.html` |
| SC3 | Scheduled scaling can start an activity at its scheduled time | ✅ V | EC2 Auto Scaling docs |
| SC4 | Scale up = bigger machine, scale out = more copies | 🟨 K | general term |
| SC5 | Retry with exponential back-off and jitter, circuit breaker, idempotency | 🟨 K | analogue verified for Azure; AWS Builders Library not searched |
| DR1 | RPO = acceptable data loss; RTO = acceptable downtime | ✅ V | DR whitepaper |
| DR2 | Four strategies: backup and restore, pilot light, warm standby, multi-site active/active; pilot light cannot process requests without extra action, warm standby can handle reduced traffic immediately; active/active serves from all Regions and still needs backups for corruption | ✅ V | `/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-options-in-the-cloud.html`, Reliability Pillar REL13-BP02 |
| DR3 | All strategies need data backed up in-Region with copies in the recovery Region; AWS Backup gives central configuration, scheduling and monitoring | ✅ V | DR whitepaper |
| DR4 | Elastic Disaster Recovery uses a pilot-light approach with continuous data protection (targets deliberately not quoted; RTO/RPO ranges differ across AWS documents) | ✅ V | Reliability Pillar, DRS docs |
| DR5 | A replica copies deletions; a backup lets you go back in time | 🟨 K | general principle |
| DR6 | Drills and failback planning | 🟨 K | |
| SC-I | Group name `shop-asg`, scenarios, Copy 1/2/3 | 🟦 I | |

## Caching & Edge Delivery (`caching-edge.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| CE1 | Lazy loading: read cache first, on miss read the database and write to cache; weakness is staleness | ✅ V | `/AmazonElastiCache/latest/dg/Strategies.html` |
| CE2 | Write-through keeps cache fresh but missing data on new nodes and cache churn; combine with lazy loading and add a TTL | ✅ V | same page |
| CE3 | Invalidate (delete) on write rather than update; a narrow race remains | ✅ V (guide example) | ElastiCache Valkey e-commerce guide |
| CE4 | CloudFront serves from edge until expiry; Cache-Control from the origin; default/min/max TTL; regional edge caches; invalidation takes minutes and is charged beyond a free allowance; versioned names avoid it; cache-tag invalidation | ✅ V | `/AmazonCloudFront/latest/DeveloperGuide/Expiration.html`, `/Invalidation.html`, `/HowCloudFrontWorks.html` |
| CE5 | ElastiCache engines include Valkey and Memcached (names change; check docs) | ✅ V (names appear in current docs) | `/AmazonElastiCache/latest/dg/` |
| CE6 | Browser cache controlled by response headers | 🟨 K | |
| CE-I | Pseudo-code, scenarios | 🟦 I | |

Batch B illustrative phrases: "at least two zones" is not used here · "three zones" in diagrams is the teaching layout (RG2).

## Messaging & Events and its deep dives (`messaging.html`, `sqs-sns-eventbridge.html`, `kinesis.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| MS1 | SQS is pull-based, persists messages until processed or expired (up to a fixed maximum retention); SNS is push-based, does not persist, supports HTTP/S, email, SMS, mobile push, Lambda and SQS subscribers; EventBridge matches events by rules and delivers to targets | ✅ V | `/decision-guides/latest/sns-or-sqs-or-eventbridge/sns-or-sqs-or-eventbridge.html` |
| MS2 | FIFO queues and FIFO topics guarantee order; EventBridge does not; EventBridge delivery to targets is at least once (sources differ on wording — the safer reading is used) | ✅ V | same page |
| MS3 | SNS filters are per subscriber; EventBridge rules are central; SNS for many subscribers, EventBridge for many topics/filters between microservices; EventBridge or SNS into an SQS buffer is a common pattern | ✅ V | same guide, Prescriptive Guidance |
| MS4 | Dead-letter queue catches repeated failures; visibility timeout hides a message during processing | ✅ V (EventBridge Pipes doc), 🟨 K (general SQS) | `/eventbridge/latest/userguide/eb-pipes-sqs.html` |
| MS5 | Kinesis: partition key hashed to a shard; per-shard fixed limits (numbers not quoted); default retention 24 hours, extendable up to 365 days; on-demand and provisioned modes; hot shards split manually in provisioned mode; enhanced fan-out for registered consumers with a mode-dependent cap | ✅ V | `/streams/latest/dev/key-concepts.html`, `/how-do-i-size-a-stream.html` |
| MS6 | On-demand mode does not detect and isolate a hot key | ✅ V | same page |
| MS7 | `aws sqs send-message`; queue URL/account ID 111122223333, order_id 1001 | 🟨 K / 🟦 I | |
| MS-I | Scenarios, diagrams | 🟦 I | |

## Serverless & Orchestration (`serverless-orchestration.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| SV1 | Step Functions Standard: long-running, durable, auditable, exactly-once; Express: up to five minutes, at-least-once (async), suits idempotent actions; Standard fits non-repeatable actions like payments; Express history via CloudWatch Logs best-effort; the type cannot be changed after creation | ✅ V | `/step-functions/latest/dg/choosing-workflow-type.html`, `/bp-express.html` |
| SV2 | Lambda fits short, bursty tasks better than long-running services | ✅ V | `/decision-guides/latest/decision-guides/fargate-or-lambda.html` |
| SV3 | EventBridge: event routing without ordering guarantee | ✅ V | MS2 |
| SV4 | Lambda cold starts, execution role | 🟨 K | Lambda internals not searched |
| SV5 | `aws lambda create-function` flags; runtime `python3.12` | 🟨 K | example runtime |
| SV-I | Scenarios, "Step 1/2/3" | 🟦 I | |

## Infrastructure as Code (`infrastructure-as-code.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| IA1 | CDK is an open-source framework to define AWS resources in programming languages; synthesizing produces a CloudFormation template; a construct represents one or more CloudFormation resources; needs a bootstrapped environment per account | ✅ V | `/prescriptive-guidance/latest/choose-iac-tool/aws-cdk.html`, getting-started-terraform |
| IA2 | A stack is IaC deployed and tracked as a single unit; a template is one CloudFormation file | ✅ V | `/prescriptive-guidance/latest/getting-started-terraform/introduction.html` |
| IA3 | Terraform is not tied to one provider; CloudFormation change set ≈ Terraform plan; template ≈ configuration; CDK for Terraform exists | ✅ V | same guide |
| IA4 | Change sets preview changes; drift detection | 🟨 K | not returned by the search |
| IA5 | The sample template (`AWS::S3::Bucket`, versioning enabled) | 🟦 I | |
| IA-I | Scenarios | 🟦 I | |

## CI/CD & Deployment Strategies (`ci-cd-deployment.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| CD1 | CodeDeploy: in-place for EC2/on-premises only; blue/green on EC2, Lambda and ECS; Lambda and ECS cannot use in-place | ✅ V | `/codedeploy/latest/userguide/deployment-configurations.html` |
| CD2 | Traffic shifting for Lambda/ECS: all-at-once, canary, linear; predefined examples `CodeDeployDefault.ECSCanary10Percent5Minutes` (10 percent, then the rest five minutes later) | ✅ V | same page |
| CD3 | CodeDeploy tracks application health by rules you configure | ✅ V | CodeDeploy docs |
| CD4 | OIDC: add the provider to IAM, create a web-identity role with audience `sts.amazonaws.com`, restrict the trust policy to the repository/branch; match immutable IDs where possible; workflow needs `id-token: write` | ✅ V | `/IAM/latest/UserGuide/id_roles_create_for-idp_oidc.html`, condition-keys page |
| CD5 | CodePipeline orchestrates stages; CodeBuild builds and tests | 🟨 K | not returned by the search |
| CD6 | `aws deploy create-deployment` flags; `appspec-revision.json` | 🟨 K / 🟦 I | |
| CD-I | Pipeline picture, scenarios | 🟦 I | |

## Secrets & Configuration (`secrets-configuration.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| SX1 | Secrets Manager: automatic rotation, random secret generation, cross-account sharing, cross-Region replication; per-secret and per-API-call charges; database rotation expects the database secret JSON structure | ✅ V | `/secretsmanager/latest/userguide/integrating_parameterstore.html`, ECS sensitive-data guide |
| SX2 | Parameter Store has no automatic rotation; keep secrets in Secrets Manager and reference them from Parameter Store; standard-tier parameters up to a small size have no charge; both use KMS | ✅ V | same pages, `/systems-manager/latest/userguide/systems-manager-parameter-store.html` |
| SX3 | Environment variables carry a higher risk of leakage for containers; a sidecar reading Secrets Manager into a shared volume is described | ✅ V | `/AmazonECS/latest/developerguide/specifying-sensitive-data.html` |
| SX4 | AWS recommends ephemeral secrets or a secrets-management service | ✅ V | `/prescriptive-guidance/latest/aws-startup-security-baseline/wkld-03.html` |
| SX5 | KMS envelope encryption details | 🟨 K | not returned; the page only says both services encrypt with KMS |
| SX6 | `aws secretsmanager get-secret-value`; secret name `prod/shop/db` | 🟨 K / 🟦 I | |
| SX-I | Scenarios | 🟦 I | |

Batch C illustrative phrases: "365 days" and "24 hours" are Kinesis retention values (MS5) · "Preview" in CloudFormation text is the "change set preview" meaning, not a lifecycle state.

## Security & Governance (`security-governance.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| SG1 | SCPs/RCPs apply guardrails at organization, OU or account level; SCPs never grant; default Organizations setup supports SCPs as deny lists | ✅ V | `/prescriptive-guidance/latest/security-reference-architecture/security-services.html` |
| SG2 | Config is enabled for member accounts as a prerequisite for Security Hub CSPM; GuardDuty findings flow to Security Hub; Config rules can start in monitoring mode and move to enforcement | ✅ V | same page, Security Pillar |
| SG3 | Delegated administration of security services to a Security Tooling account, separate from the management account | ✅ V | same page |
| SG4 | WAF: use AWS managed rules in default mode so they update; Shield Advanced for ALB, Classic LB, Elastic IPs, CloudFront; Firewall Manager applies WAF, Shield and security group rules across accounts | ✅ V | `/prescriptive-guidance/latest/security-reference-architecture/perimeter-security.html` |
| SG5 | Findings can drive automation such as updating a WAF IP set | ✅ V | same page |
| SG6 | SCPs do not apply to the management account | ✅ V | AC2 |
| SG7 | Layer table (organization, identity, network and edge, detection) | 🟦 I | teaching model |
| SG8 | SCP JSON example (`aws:RequestedRegion`, "2012-10-17" policy version, two example Regions) | 🟦 I | real SCPs exempt global services |
| SG-I | Scenarios | 🟦 I | |

## Monitoring & Observability (`monitoring-observability.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| MO1 | Observability = logs, metrics, traces; CloudWatch for metrics, logs and alarms; Logs Insights to query logs; X-Ray distributed tracing with a map of components; Service Map | ✅ V | `/decision-guides/latest/monitoring-on-aws-how-to-choose/monitoring-on-aws-how-to-choose.html`, `/wellarchitected/latest/management-and-governance-guide/aws-observability-tools.html` |
| MO2 | CloudTrail records API activity (who, when, what); default event history covers recent management events (window not quoted) | ✅ V | `/decision-guides/latest/cloudtrail-or-cloudwatch/cloudtrail-or-cloudwatch.html` |
| MO3 | CloudTrail = audit and compliance; CloudWatch = operational health and performance | ✅ V | same guide |
| MO4 | Alarm → action (notify, automation, ticket) | 🟨 K | general CloudWatch behaviour |
| MO5 | `aws cloudwatch put-metric-alarm` flags; period 300, threshold 80, evaluation periods 2 | 🟨 K / 🟦 I | example values |
| MO-I | Scenarios | 🟦 I | |

## Cost Management (`cost-management.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| CO1 | Cost Explorer + cost allocation tags show spend by team/workload; Cost Categories group accounts and tags and appear in Cost Explorer, Budgets and Anomaly Detection | ✅ V | `/decision-guides/latest/cost-management-on-aws-how-to-choose/cost-management-on-aws-how-to-choose.html` |
| CO2 | AWS Budgets: custom cost and usage budgets with alerts; filter by tags; one budget for overall spend and one per workload | ✅ V | `/wellarchitected/latest/framework/cost_cloud_financial_management_budget_forecast.html` |
| CO3 | Savings Plans: commitment in $/hour for one or three years; Reserved Instances can be cheaper for steady workloads but less flexible; Well-Architected suggests working toward Savings Plans; Cost Explorer gives recommendations | ✅ V | `/wellarchitected/latest/framework/cost_pricing_model_analysis.html` |
| CO4 | Spot Instances: spare capacity at a discounted hourly rate, no upfront commitment, for non-critical workloads (discount percentage not quoted) | ✅ V | Cost Optimization pillar |
| CO5 | Compute Optimizer recommends compute resources; start generic and resize on CPU and memory use | ✅ V | same pillar |
| CO6 | Commitment fees cannot be tagged in advance; use amortized cost grouped by tag | ✅ V | tagging best practices |
| CO7 | Cost allocation tags must be activated in billing before they appear in cost reports | 🟨 K | |
| CO8 | `aws ec2 create-tags` flags; tag values | 🟨 K / 🟦 I | |
| CO-I | Scenarios | 🟦 I | |

## Well-Architected & Landing Zones (`well-architected.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| WA1 | Six pillars: operational excellence, security, reliability, performance efficiency, cost optimization, sustainability | ✅ V | `/wellarchitected/latest/framework/the-pillars-of-the-framework.html` |
| WA2 | Trade-offs between pillars depend on business needs; security and operational excellence are generally not traded off against the others | ✅ V | same page |
| WA3 | A landing zone is a well-architected multi-account environment based on security and compliance best practices | ✅ V | `/controltower/latest/userguide/what-is-control-tower.html` |
| WA4 | Control Tower orchestrates Organizations, Service Catalog and IAM Identity Center, applies preventive and detective guardrails, gives a dashboard; AWS recommends starting with it; a custom landing zone suits unusual requirements | ✅ V | same page |
| WA5 | Platform and workload account layout; pillar-to-concept mapping | 🟦 I | teaching model |
| WA-I | Scenarios | 🟦 I | |

Batch D illustrative phrases: "300" (seconds, example alarm period) · "2012" (the IAM policy language version string in the SCP example).

---

## Open verification list

Everything marked 🟨 K above, in priority order: **IM-series CLI flags and example IDs** (IM10), **ST11 / DB8 / DB9** (S3 CLI flags, DynamoDB global tables and RDS engine list were not covered by the searches), **LB4** (DNS caching), **SC4 / SC5 / DR5 / DR6** (general terms and Builders-Library patterns), **SV4** (Lambda internals and cold starts), **IA4** (change sets and drift detection), **CD5** (CodePipeline and CodeBuild descriptions), **SX5** (KMS envelope encryption), **MS4** (general SQS visibility timeout and dead-letter behaviour), **MO4 / MO5**, **CO7**, **RG6** (zone-name mapping per account), **CP6 / CP7**, and the CLI examples marked K on every page.
After checking a row against the official AWS page, change 🟨 K to ✅ V and add the exact URL. Also re-check any ✅ V row whose source was a search snippet from a page the search described as older.
