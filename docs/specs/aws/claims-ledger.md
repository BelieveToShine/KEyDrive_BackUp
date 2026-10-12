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

---

## Open verification list

(Filled at the end of the AWS run: every 🟨 K row, in priority order.)
