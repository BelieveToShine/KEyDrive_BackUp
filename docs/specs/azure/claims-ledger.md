# Azure — claims ledger

Every factual claim on an Azure concept page, where it came from, and how sure we are. This is the
cross-check file for `docs/rules/fact-check-and-currency.md`. `scripts/check-site.js` warns when a
page contains a number, price, size, year or "retired/preview" word that is **not written in this
file** — so adding a number to a page without adding it here is caught.

**How the claims were checked (2026-10-12 session):** direct fetches of `learn.microsoft.com` were
blocked by the sandbox network policy, so each risky claim was checked with web searches restricted
to `learn.microsoft.com`; the result snippets quote Microsoft Learn pages (URLs below). That is
real but second-hand evidence — a human or a session with direct docs access should still open the
linked page for every row marked 🟨 and for anything you plan to quote in an interview.

| Status | Meaning |
|---|---|
| ✅ V | Verified — the claim matches text returned from the named Microsoft Learn page |
| 🟨 K | Knowledge-based — a well-established concept stated conservatively, **not re-verified** this session. Re-check before relying on specifics |
| 🟦 I | Illustrative — an example value or label (not a claim about Azure) |
| 👤 U | Taken from a screenshot the project owner supplied |

Doc roots (stable): [Storage](https://learn.microsoft.com/en-us/azure/storage/) ·
[Azure SQL](https://learn.microsoft.com/en-us/azure/azure-sql/) ·
[Cosmos DB](https://learn.microsoft.com/en-us/azure/cosmos-db/) ·
[Service Bus](https://learn.microsoft.com/en-us/azure/service-bus-messaging/) ·
[Event Hubs](https://learn.microsoft.com/en-us/azure/event-hubs/) ·
[Event Grid](https://learn.microsoft.com/en-us/azure/event-grid/) ·
[Architecture Center](https://learn.microsoft.com/en-us/azure/architecture/)

---

## Storage (`storage.html`)

| # | Claim on the page | Status | Source / note |
|---|---|---|---|
| S1 | A storage account offers Blob, Files, Queues and Tables | ✅ V | `/azure/storage/common/storage-account-overview` |
| S2 | Endpoints follow `<account>.blob/.file/.queue/.table.core.windows.net` | ✅ V | same page |
| S3 | Portal "Data storage" menu lists Containers, Classic file shares, Queues, Tables | 👤 U | owner's portal screenshot (the page says "File shares"; the portal currently labels it "Classic file shares") |
| S4 | Azure Files is a shared drive over SMB or NFS | ✅ V | `/azure/storage/files/storage-files-introduction` |
| S5 | A queue message can be up to **64 KB** | ✅ V | `/azure/storage/queues/storage-queues-introduction`; `/azure/service-bus-messaging/service-bus-azure-and-service-bus-queues-compared-contrasted` |
| S6 | Storage queues: no ordering guarantee, no built-in dead-lettering | ✅ V | queues-compared page above |
| S7 | Table storage is a simple key → value (NoSQL) store | 🟨 K | not returned by search; confirm on `/azure/storage/tables/` |
| S8 | Cosmos DB has a Table API | ✅ V | `/azure/cosmos-db/table/introduction` |
| S9 | LRS = copies in one datacenter; ZRS = copies across zones; GRS = + async copy to paired region (secondary kept as LRS); GZRS = ZRS primary + async copy; RA- variants allow reading the secondary | ✅ V | `/azure/storage/common/storage-redundancy` |
| S10 | LRS / ZRS keep **three** copies | 🟨 K | docs say "copies"; the count "three" is standard wording — confirm on the redundancy page |
| S11 | Redundancy is not a backup (a delete/overwrite is replicated) | 🟨 K | widely documented; soft delete & versioning are the documented protections |
| S12 | Entra ID + RBAC preferred; SAS = limited temporary access; account key = full access | ✅ V (Entra/user-delegation SAS recommendation) / 🟨 K (wording "avoid account key") | `/azure/storage/blobs/authorize-access-azure-active-directory` |
| S13 | General-purpose v2 is the standard type; Premium types exist | ✅ V | storage-account-overview |
| S14 | Data Lake Storage Gen2 = Blob service with hierarchical namespace on | ✅ V | search result on HNS (Blob Storage + Data Lake docs) |
| S15 | "10 minutes" (SAS example in the audience box) | 🟦 I | example value |
| S16 | "60 seconds" (reading-time label "Go one level deeper") | 🟦 I | UI label, not a claim |
| S17 | ZRS copies data across **three** zones (the docs say "three or more availability zones"); the page's "three zones" / "3 zones" follow that | ✅ V | `/azure/storage/common/storage-redundancy` |

## Blob Storage in depth (`blob-storage.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| B1 | Blob URL = `https://<account>.blob.core.windows.net/<container>/<blob>` | ✅ V | `/azure/storage/blobs/storage-blobs-introduction` |
| B2 | Three blob types: block (built from blocks), append (append operations, logging), page (random access, VM disks) | ✅ V | same page |
| B3 | A user delegation SAS is signed with Entra credentials and is the recommended kind of SAS | ✅ V | `/rest/api/storageservices/create-user-delegation-sas` |
| B4 | Upload pattern: API issues a short-lived SAS, browser uploads straight to Blob | 🟨 K | standard design pattern, not a quoted doc sentence |
| B5 | Blob Storage emits `BlobCreated` events via an Event Grid system topic | ✅ V | `/azure/event-grid/event-schema-blob-storage`, `/azure/event-grid/system-topics` |
| B6 | An Azure Function can handle the event | 🟨 K | Event Grid handlers include Functions (concepts page) — trigger details not re-read |
| B7 | Tiers Hot / Cool / Cold / Archive; minimum stay **30 days** (Cool), **90 days** (Cold), **180 days** (Archive); Hot none; Archive is offline (hours to rehydrate); early-deletion fees apply | ✅ V | `/azure/storage/blobs/access-tiers-overview`, `/azure/storage/blobs/archive-rehydrate-overview`. Note: minimums apply to GPv2 accounts |
| B8 | Cooler tiers cost less to store and more to read | 🟨 K | documented pricing principle — confirm on the access-tiers page |
| B9 | Lifecycle management rules move or delete blobs by age | ✅ V | `/azure/storage/blobs/lifecycle-management-overview` |
| B10 | Hierarchical namespace gives real directories, atomic rename, POSIX-style permissions | ✅ V | HNS / Data Lake docs |
| B11 | Without HNS the slash in a name is only part of the name; renaming a "folder" means copying blobs | 🟨 K | flat-namespace behaviour — confirm |
| B12 | Soft delete, versioning and immutable (WORM) storage exist | 🟨 K | features exist; immutable containers also block lifecycle delete (V in lifecycle docs) |
| B13 | Keep anonymous public access off unless needed | 🟨 K | security guidance |
| B14 | The 30 / 90 / 180-day lifecycle thresholds in the diagram are "an example rule" | 🟦 I | the minimum stays (B7) are real; the rule itself is an example |
| B15 | "2025/trip.jpg", "30 days online" (backup scenario), "15 / 10 minutes" in the code | 🟦 I | example names and values |
| B16 | Python SDK names `get_user_delegation_key`, `generate_blob_sas`, `BlobSasPermissions` | 🟨 K | verify against current `azure-storage-blob` reference |

## Databases (`databases.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| D1 | Azure SQL family = SQL Database, SQL Managed Instance, SQL Server on Azure VMs | ✅ V | `/azure/azure-sql/azure-sql-iaas-vs-paas-what-is-overview` |
| D2 | Managed Instance for SQL Agent, linked servers, cross-database queries, CLR, transactional replication | ✅ V | `/azure/azure-sql/azure-sql-decision-tree` |
| D3 | SQL Server on a VM for OS/file-system access or a pinned SQL version | ✅ V | `/azure/azure-sql/migration-guides/modernization` |
| D4 | SQL Database serverless can auto-pause when idle; Hyperscale tier exists; vCore vs DTU purchasing models | ✅ V | `/azure/azure-sql/database/serverless-tier-overview`, `.../purchasing-models` |
| D5 | PostgreSQL **Single Server has been retired**; use Flexible Server | ✅ V (secondary) | Microsoft Q&A threads citing the 28 March 2025 sunset; open the official retirement notice to quote a date |
| D6 | MySQL Flexible Server is the managed MySQL option | 🟨 K | not returned by search |
| D7 | Cosmos DB APIs: NoSQL (recommended for new apps), MongoDB, Cassandra, Gremlin, Table | ✅ V | `/azure/cosmos-db/overview` |
| D8 | Cosmos DB indexes all data by default; uses Request Units | ✅ V | same page |
| D9 | The partition key's hash decides the partition | 🟨 K | concept from `/azure/cosmos-db/partitioning`; "hash" wording not quoted |
| D10 | Relational: transactions across tables; Cosmos DB: transactions inside one partition key | ✅ V | `/azure/cosmos-db/transactional-batch` |
| D11 | Relational scales mostly up with readable copies | 🟨 K | general characteristic |
| D12 | "$100" ("orders over $100") | 🟦 I | example in a user story |
| D13 | "60 seconds" (label) | 🟦 I | UI label |
| D14 | "order-1001" (example order id in the code sample) | 🟦 I | example value |

## Cosmos DB vs Azure SQL (`cosmos-db-vs-azure-sql.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| C1 | JOIN in Cosmos DB works only inside one item | 🟨 K | confirm on the NoSQL query docs |
| C2 | Transactional batch needs one partition key | ✅ V | `/azure/cosmos-db/transactional-batch` |
| C3 | A logical partition holds up to about **20 GB** | ✅ V | `/azure/cosmos-db/partitioning` |
| C4 | Throughput: Request Units; manual, autoscale or serverless modes | ✅ V | `/azure/cosmos-db/partitioning`, `/azure/cosmos-db/concepts-limits` |
| C5 | Multi-region writes are available | ✅ V | `/azure/cosmos-db/overview` |
| C6 | Five consistency levels (Strong, Bounded staleness, Session = default, Consistent prefix, Eventual) and their meanings | ✅ V | `/azure/cosmos-db/consistency-levels` |
| C7 | Designed for single-digit-millisecond reads and writes | ✅ V | `/azure/cosmos-db/overview` ("promises single-digit millisecond response times") |
| C8 | Reading one small item by id + partition key is the cheapest operation | 🟨 K | |
| C9 | Each extra region adds to the bill | 🟨 K | |
| C10 | Azure SQL has one writable primary; geo copies are readable | 🟨 K | |
| C11 | Cross-partition queries fan out and cost more | 🟨 K | |
| C12 | Polyglot persistence (using both) is a documented pattern | ✅ V | Architecture Center: "Polyglot Persistence with Azure Cosmos DB and Azure SQL Database" |
| C13 | "30 seconds" (label "Decide in 30 seconds") | 🟦 I | UI label |
| C14 | SDK call `create_container_if_not_exists(id=, partition_key=PartitionKey(path=))` | 🟨 K | verify against current `azure-cosmos` reference |

## Messaging & Events (`messaging.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| M1 | Event Grid = discrete events; Event Hubs = streams; Service Bus = enterprise messages; Storage queues = basic work queues | ✅ V | `/azure/service-bus-messaging/compare-messaging-services` |
| M2 | Event Grid: no ordering guarantee, supports dead-lettering, pushes events | ✅ V | same page; `/azure/event-grid/overview` |
| M3 | Service Bus: FIFO via sessions, duplicate detection, transactions, dead-lettering; Storage queues lack dead-lettering | ✅ V | same page |
| M4 | Event Hubs: readers manage their own position; events can be replayed; Capture | ✅ V | same page; `/azure/event-hubs/event-hubs-features` |
| M5 | Service Bus peek-lock is at-least-once | ✅ V | `/azure/service-bus-messaging/service-bus-message-loss-and-duplicates` |
| M6 | Claim-check pattern recommended for big payloads | ✅ V | queues-compared page |
| M7 | Combination example: Service Bus for orders, Event Hubs for telemetry, Event Grid for shipped-item reactions | ✅ V | compare-messaging-services |
| M8 | Event Grid subscriptions filter by event type and subject; handlers include Azure services and webhooks | ✅ V | `/azure/event-grid/event-filtering`, `/azure/event-grid/concepts` |
| M9 | Event Grid retries delivery for a while, then drops or dead-letters | ✅ V | `/azure/event-grid/overview` (24-hour retry window; the page does not give a number except in this ledger) |
| M10 | "64 KB" message limit | ✅ V | = S5 |
| M11 | "10 seconds" / "60 seconds" (labels "Event Grid in 10 seconds", "Go one level deeper (60 seconds)") | 🟦 I | UI labels |
| M12 | SDK names `ServiceBusClient`, `get_queue_sender`, `ServiceBusMessage` | 🟨 K | verify against current `azure-servicebus` reference |
| M13 | "24 hours" appears only as the example reminder ("remind in 24 hours") on service-bus.html | 🟦 I | see SB-I |

## Service Bus (`service-bus.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| SB1 | Queue: one consumer per message; topic + subscriptions: one-to-many publish/subscribe | ✅ V | `/azure/service-bus-messaging/service-bus-queues-topics-subscriptions` |
| SB2 | A message is copied only to subscriptions whose filters match; no match → delivered to none | ✅ V | same page |
| SB3 | Peek-lock lifecycle: lock → Complete removes; abandon or lock expiry returns it and raises the delivery count; over the max delivery count (**10 by default**) → dead-letter queue | ✅ V | `/azure/service-bus-messaging/service-bus-dead-letter-queues` |
| SB4 | Every queue and every subscription has a dead-letter queue (also for expired / filter-failed messages) | ✅ V | same page |
| SB5 | Duplicate detection drops repeated MessageId within a window; protects the sending side only | ✅ V | service-bus-message-loss-and-duplicates (default window 10 minutes — not stated on the page) |
| SB6 | Sessions give FIFO ordering | ✅ V | compare-messaging-services |
| SB7 | Tiers: Basic = queues only; Standard adds topics, shared capacity billed per operation; Premium = dedicated resources, geo-replication, Private Link, much larger messages | ✅ V | `/azure/service-bus-messaging/service-bus-premium-messaging`, `.../service-bus-quotas` |
| SB8 | Scheduled messages, transactions, auto-forwarding exist | 🟨 K | auto-forwarding appears in DLQ docs; others from the "advanced features" overview |
| SB9 | Receive-and-delete is at-most-once | ✅ V | message-loss-and-duplicates |
| SB-I | "24 hours" (reminder scenario), SDK names `get_queue_receiver`, `complete_message` | 🟦 I / 🟨 K | |

## Event Hubs (`event-hubs.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| E1 | Partitions are ordered sequences; consumer groups give independent views | ✅ V | `/azure/event-hubs/event-hubs-features` |
| E2 | Events with the same key land in the same partition | 🟨 K | |
| E3 | Capture writes the stream to storage; not available on Basic | ✅ V | `/azure/event-hubs/compare-tiers` |
| E4 | Kafka endpoint on Standard and above; not on Basic | ✅ V | `/azure/event-hubs/compare-tiers` |
| E5 | Tiers: Basic (low-cost entry), Standard (general purpose), Premium (isolation + performance), Dedicated (single-tenant cluster) | ✅ V | same page |
| E6 | Partition count is set at creation; only Premium and Dedicated can increase it later | ✅ V | `/azure/event-hubs/dynamically-add-partitions` |
| E7 | Retention is a limited window that depends on the tier (page gives no numbers) | ✅ V | compare-tiers |
| E8 | Order is kept only inside a partition | ✅ V/K | features page |
| E9 | Namespace address ends `.servicebus.windows.net`; SDK names `EventHubProducerClient`, `create_batch`, `send_batch` | 🟨 K | verify against current `azure-eventhub` reference |
| E10 | Millions of tiny events per second scenario | ✅ V | compare-messaging-services ("millions of events per second") |

---

## Tenants, Subscriptions & Resource Groups (`resource-hierarchy.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| RH1 | Hierarchy: tenant → management groups → subscriptions → resource groups → resources | ✅ V | `/azure/governance/management-groups/overview`, `/azure/cloud-adoption-framework/ready/landing-zone/design-area/resource-org-subscriptions` |
| RH2 | A role or policy assigned at a higher scope is inherited by everything below | ✅ V | management-groups overview |
| RH3 | A subscription trusts one tenant; a tenant can trust many subscriptions | ✅ V | same page |
| RH4 | Management groups are optional folders; resources never sit directly in one (they live in resource groups) | 🟨 K | |
| RH5 | A subscription is the unit of billing and a boundary for access and limits | ✅ V (billing / access) · 🟨 K (limits) | Cloud Adoption Framework subscription guidance |
| RH6 | A resource group is a lifecycle container — keep resources with the same lifespan together | ✅ V | `/azure/azure-resource-manager/management/overview`, Entra "resource management fundamentals" |
| RH7 | A resource belongs to exactly one resource group (and can be moved) | ✅ V | ARM overview |
| RH8 | A resource group's location is where its metadata is stored; its resources can be in other regions | ✅ V | `/azure/azure-resource-manager/management/manage-resource-groups-portal` |
| RH9 | Deleting a resource group deletes every resource inside it | ✅ V | same page |
| RH10 | Every tool (portal, CLI, SDK, templates) sends REST requests to Azure Resource Manager, which routes to resource providers | 🟨 K | ARM overview confirms ARM is the management layer; the exact "all tools" wording was not quoted |
| RH11 | Provider names `Microsoft.Compute`, `Microsoft.Storage`, `Microsoft.Network` | 🟨 K | |
| RH12 | Tags for cost reporting; resource locks protect from deletion | 🟨 K | |
| RH13 | `az group create/delete` commands; "westeurope" region name | 🟨 K | |
| RH-I | Example names (rg-shop-prod, Prod/Dev, "Contoso"-style), "60 seconds" label | 🟦 I | |

## Regions & Availability Zones (`regions-availability-zones.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| RG1 | Zone-enabled regions have at least **three** zones | ✅ V | `/azure/reliability/regions-overview`, Well-Architected "Using availability zones and regions" |
| RG2 | Each zone has independent power, cooling and networking | ✅ V | Well-Architected page |
| RG3 | Zonal = pinned to one zone (you design resilience); zone-redundant = spread across zones, Azure handles failover; Microsoft recommends zone-redundant unless there is a strong reason | ✅ V | `/azure/reliability/availability-zones-zonal-resource-resiliency` |
| RG4 | Region pairs are assigned by Microsoft (you cannot choose); many regions are not paired and rely on zones | ✅ V | `/azure/reliability/regions-paired` |
| RG5 | Zone support differs by service (some zone-redundant by default, others need enabling) | ✅ V | reliability docs per service |
| RG6 | Logical zone numbers map to physical zones per subscription | ✅ V | `/azure/reliability/availability-zones-overview` |
| RG7 | Not every region supports zones; not every service/feature is in every region | ✅ V | feature-availability-by-region pages |
| RG8 | Prices can differ between regions | 🟨 K | |
| RG9 | Zones protect against a zone failure, not a whole-region failure | ✅ V | storage-redundancy ("ZRS … doesn't protect against a region-wide disaster") |
| RG10 | Zones are far enough apart to fail separately, close enough to stay fast | 🟨 K | design principle |
| RG11 | `az vm create --zone 1`, `az storage account create --sku Standard_ZRS` | 🟨 K | |
| RG-I | "Region A / Region B" and the three-zone picture are generic | 🟦 I | |

## Identity & Access (`identity-access.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| ID1 | A role assignment = security principal + role definition + scope | ✅ V | `/azure/role-based-access-control/role-assignments` |
| ID2 | Principals: users, groups, service principals, managed identities | ✅ V | same page |
| ID3 | Scopes: management group, subscription, resource group, resource | ✅ V | same page |
| ID4 | Owner can assign roles; Contributor manages everything but cannot assign roles; Reader views only | ✅ V | `/azure/role-based-access-control/built-in-roles` |
| ID5 | Permissions are additive; assignments are inherited by lower scopes | ✅ V | role-assignments / overview |
| ID6 | Entra roles manage the directory (scopes: tenant, administrative unit, object); Azure roles manage Azure resources; separate systems — permissions cannot be mixed in custom roles; Global Administrator is the top Entra role and not the same as Owner | ✅ V | `/azure/role-based-access-control/rbac-and-directory-admin-roles` |
| ID7 | Entra ID authenticates and issues tokens; Azure RBAC authorizes | ✅ V / 🟨 K | Entra + RBAC overview pages |
| ID8 | A service principal is the tenant-local identity of an app | ✅ V | `/entra/identity-platform/howto-create-service-principal-portal` |
| ID9 | A new identity has no access until a role is assigned | ✅ V | managed-identities docs |
| ID10 | Assign roles to groups; least privilege at the narrowest scope | 🟨 K | widely documented guidance |
| ID11 | `az role assignment create --assignee --role --scope` | 🟨 K | |
| ID-I | "Asha", "rg-shop-prod", "ten people" examples | 🟦 I | |

## Managed Identities (`managed-identities.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| MI1 | A managed identity is a special service principal, usable only with Azure resources; no credentials in code | ✅ V | `/entra/identity/managed-identities-azure-resources/overview` |
| MI2 | System-assigned: tied to one resource's lifecycle, deleted with it, cannot be shared | ✅ V | same page |
| MI3 | User-assigned: a standalone resource, shareable, independent lifecycle | ✅ V | same page |
| MI4 | Code gets a token from an Azure identity endpoint | ✅ V | `/entra/identity/managed-identities-azure-resources/how-managed-identities-work-vm` |
| MI5 | Identities have no access by default — assign RBAC roles | ✅ V | same page |
| MI6 | Azure Identity / MSAL libraries get the token; user-assigned needs client ID (or resource ID) passed | ✅ V | `/entra/identity/managed-identities-azure-resources/overview-for-developers` |
| MI7 | Secrets in config files are a common way accounts get compromised; tokens are short-lived | 🟨 K | security guidance |
| MI8 | `DefaultAzureCredential(managed_identity_client_id=...)` | 🟨 K | verify against current `azure-identity` reference |

## Virtual Networks (`virtual-networks.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| VN1 | A VNet is scoped to one region (can span zones) and to one subscription; networks in different regions connect through peering | ✅ V | `/azure/virtual-network/virtual-networks-faq`, `/azure/virtual-network/concepts-and-best-practices` |
| VN2 | Azure reserves **five addresses** in every subnet | ✅ V | virtual-networks-faq (wording of the five differs slightly between pages; the count agrees) |
| VN3 | Use private (RFC 1918) address ranges | ✅ V | same pages |
| VN4 | NSGs and route tables attach to subnets; associate an NSG with every subnet | ✅ V | `/azure/networking/design-guide/vnets-subnets`, `/azure/virtual-network/secure-virtual-network` |
| VN5 | NSG custom rules use priority **100** to **4096**; lower number wins; first match stops evaluation | ✅ V | `/azure/virtual-network/manage-network-security-group` |
| VN6 | Default rules sit at **65000** (allow inside the virtual network) and 65500 (deny all inbound); cannot be deleted, can be overridden | ✅ V | same page |
| VN7 | The default VNet allow rule covers connected networks too, so subnets can talk unless you add a deny | ✅ V (secondary) | Microsoft Q&A answer; behaviour consistent with the NSG docs |
| VN8 | Peering is not transitive; create explicit peerings per path | ✅ V | `/azure/virtual-network/secure-virtual-network` |
| VN9 | Peered networks must not have overlapping address spaces | 🟨 K | |
| VN10 | VPN gateway = encrypted tunnel; ExpressRoute = private connection through a provider | 🟨 K | |
| VN11 | Ports **443** (HTTPS), 1433 (SQL Server), **3389** (remote desktop) | 🟨 K | standard port numbers |
| VN12 | `az network vnet create` / `az network nsg rule create` flags | 🟨 K | |
| VN-I | Address ranges 10.x.x.x, subnet names, "200" priority in the example, the "no direct path" picture | 🟦 I | |

## Private Endpoints (`private-endpoints.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| PE1 | A private endpoint is a network interface with a private IP from your subnet, connecting you to a Private Link resource | ✅ V | `/azure/private-link/private-endpoint-overview` |
| PE2 | A service endpoint keeps the service's public IP; the service sees your subnet as the source | ✅ V | `/azure/virtual-network/vnet-integration-for-azure-services` |
| PE3 | Service endpoints apply to the whole service; private endpoints to an individual instance | ✅ V | Private Link FAQ + Q&A |
| PE4 | Private endpoints work from on-premises over VPN/ExpressRoute; service endpoints do not | ✅ V | same sources |
| PE5 | The service name must resolve to the private IP (usually a private DNS zone) | ✅ V | private-endpoint-overview |
| PE6 | A private endpoint lets you disable public access | ✅ V | same page |
| PE7 | Microsoft recommends Private Link | ✅ V | same sources |
| PE8 | Creating a private endpoint does not by itself close public access | 🟨 K | |
| PE9 | `az network private-endpoint create` flags | 🟨 K | |
| PE-I | "10.0.3.4", "mystorage…" | 🟦 I | |

## Compute (`compute.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| CP1 | VMs = full control / lift-and-shift / GPU or long batch; App Service = web apps and APIs; Functions = event-driven; Container Apps = containers without Kubernetes; AKS = Kubernetes API and control; Container Instances = a single container or one-off job | ✅ V | `/azure/architecture/guide/technology-choices/compute-decision-tree` |
| CP2 | Container Apps is built on Kubernetes but does not expose its API; Microsoft recommends considering it first for containers unless you need the Kubernetes API | ✅ V | `/azure/architecture/guide/choose-azure-container-service` |
| CP3 | AKS needs more operational effort and gives the most customisation | ✅ V | same page |
| CP4 | Container Instances does not scale beyond the container group | ✅ V | same page |
| CP5 | App Service: built-in autoscale, deployment slots, scaling per App Service plan, does not scale to zero | ✅ V | `/azure/architecture/microservices/design/compute-options` |
| CP6 | Container Apps scales with KEDA; most apps can scale to zero, not those scaling on CPU or memory | ✅ V | `/azure/container-apps/overview`, `/azure/container-apps/scale-app` |
| CP7 | On VMs you patch the guest OS; on App Service Azure patches the OS and runtime | ✅ V | `/azure/app-service/overview-patch-os-runtime`, VM updates docs |
| CP8 | Azure Update Manager helps patch VMs | ✅ V | `/azure/virtual-machines/updates-maintenance-overview` |
| CP9 | AKS node OS patching is a shared responsibility | ✅ V | `/azure/aks/support-policies` |
| CP10 | An App Service plan is a set of VM instances that its apps share | 🟨 K | |
| CP11 | Azure runs the AKS control plane | 🟨 K | |
| CP12 | `az containerapp create` flags and the quickstart image name | 🟨 K | |
| CP-I | "VM 1/2/3", "App A/B", "Ten small services" | 🟦 I | |

## Load Balancing & Traffic Routing (`load-balancing.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| LB1 | Load Balancer = layer 4 (TCP/UDP), regional, health probes, no TLS termination or URL routing | ✅ V | `/azure/load-balancer/load-balancer-overview`, `/azure/architecture/guide/technology-choices/load-balancing-overview` |
| LB2 | Application Gateway = layer 7, regional, TLS termination, URL path-based routing, multi-site hosting, cookie-based affinity, optional WAF (v2) | ✅ V | `/azure/application-gateway/overview` |
| LB3 | Front Door = layer 7, global, edge entry, WAF, caching, fast failover; Standard and Premium are current | ✅ V | `/azure/frontdoor/front-door-overview` |
| LB4 | Traffic Manager = DNS-based, global, any protocol; routing by priority, weight, performance, geography; failover lags because DNS answers are cached | ✅ V | `/azure/traffic-manager/traffic-manager-overview` |
| LB5 | Decision rule: web + one region → Application Gateway; web + global → Front Door; non-web + one region → Load Balancer; non-web + multi-region → Traffic Manager (a "two regions"-style setup is the multi-region case) | ✅ V | load-balancing-overview (Architecture Center) |
| LB6 | Basic Load Balancer was retired on 30 Sept 2025 — use Standard | ✅ V | `/azure/load-balancer/load-balancer-faqs` |
| LB7 | Application Gateway V1 retired (28 April 2026) — use V2 | ✅ V | `/azure/application-gateway/v1-retirement` |
| LB8 | Front Door stays in the request path, Traffic Manager does not (client connects directly after DNS) | ✅ V | follows from LB3/LB4 |
| LB9 | The layered diagram (Front Door → App Gateway → internal LB) is one common shape | 🟦 I | illustrative; Microsoft guidance on combining the tools varies, the page says "example, not a rule" |
| LB10 | `az network lb create` flags | 🟨 K | |
| LB-I | "Region 1/2", "Web VMs", scenario names | 🟦 I | |

## Scaling & Resilience (`scaling-resilience.html`) and Disaster Recovery (`disaster-recovery.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| SC1 | Autoscale is horizontal; metric-based (CPU, queue length, memory) or schedule-based | ✅ V | `/azure/azure-monitor/autoscale/autoscale-overview` |
| SC2 | Rules use a time window; always pair scale-out with scale-in; keep a margin between thresholds to avoid flapping | ✅ V | `/azure/azure-monitor/autoscale/autoscale-best-practices` |
| SC3 | Scale sets = a group of load-balanced VMs that can autoscale; Flexible orchestration mode is recommended | ✅ V | `/azure/virtual-machine-scale-sets/overview` |
| SC4 | Spreading across zones protects against datacenter failure but does not replicate data | ✅ V | scale-set / reliability docs |
| SC5 | Scale up = bigger machine, scale out = more copies; scale up has a ceiling | 🟨 K | general term |
| SC6 | Transient faults: retry with exponential back-off + jitter; add a circuit breaker | ✅ V | `/azure/well-architected/design-guides/handle-transient-faults` |
| SC7 | Layered redundancy, no single point of failure, failure-mode analysis first | ✅ V | `/azure/well-architected/reliability/principles`, `/checklist` |
| SC8 | Health checks should probe real dependencies (database, cache, messaging) | ✅ V | `/azure/well-architected/service-guides/app-service-web-apps` |
| SC9 | Design Functions for idempotency | ✅ V | `/azure/well-architected/service-guides/azure-functions` |
| SC10 | Three failure sizes (server / datacenter / region) and the matching protections ("two zones" = copies in zones) | 🟦 I | teaching model built on SC3, SC4, DR1 |
| SC11 | `az monitor autoscale rule create` flags; "CPU > 70 avg 10m" values | 🟨 K | example numbers are 🟦 illustrative |
| DR1 | RPO = acceptable data loss (time); RTO = acceptable downtime (time) | ✅ V | `/azure/well-architected/reliability/disaster-recovery` |
| DR2 | Three multi-region patterns: active-active (hot), active-passive warm standby, active-passive cold standby; active-active roughly doubles spend | ✅ V | `/azure/well-architected/design-guides/disaster-recovery` |
| DR3 | Failover = shifting traffic to the unaffected region; failback = shifting it back | ✅ V | same page |
| DR4 | Site Recovery = replication and failover for VMs; do not use it for databases (use native replication) | ✅ V | `/azure/site-recovery/` docs and Q&A guidance |
| DR5 | Azure Backup restores data (files, disks, databases, workloads); soft delete, immutable vaults, Cross Region Restore exist | ✅ V | `/azure/backup/backup-overview`, `/azure/backup/backup-azure-recovery-services-vault-overview` |
| DR6 | A replica copies deletions/corruption, a backup lets you go back in time | 🟨 K | general principle |
| DR7 | Regular DR drills find hidden region dependencies; define environments as code | ✅ V | WAF disaster-recovery pages |
| DR-I | Scenarios, "last good copy" timeline | 🟦 I | |

## Caching & Edge Delivery (`caching-edge.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| CE1 | Cache-aside: check cache, on miss read the store and add to cache; on update write to the store then invalidate the cached item | ✅ V | `/azure/architecture/patterns/cache-aside` |
| CE2 | Cache-aside does not guarantee consistency; expiry too early/late hurts; avoid sensitive data; poor fit when most requests miss | ✅ V | same page |
| CE3 | Per-instance in-memory caches are private; a distributed cache such as Azure Managed Redis suits shared data | ✅ V | same page |
| CE4 | A cache can act as a limited fallback if the origin store is briefly unavailable | ✅ V | `/azure/well-architected/reliability/design-patterns` |
| CE5 | Azure Managed Redis is Microsoft's recommended Redis cache; tiers Memory Optimized, Balanced, Compute Optimized, Flash Optimized (flash moves less-used data to NVMe) | ✅ V | `/azure/redis/overview`, `/azure/redis/plan-tiers-and-capacity` |
| CE6 | Older Azure Cache for Redis tiers are being retired; Microsoft recommends migrating to Azure Managed Redis (page gives no dates) | ✅ V | `/azure/redis/migrate/migrate-basic-standard-premium-understand` |
| CE7 | Front Door (classic) and Azure CDN Standard (classic) are being retired; Front Door Standard/Premium is current (page gives no dates) | ✅ V | Front Door / CDN retirement notices |
| CE8 | Front Door caching: expiry (TTL), purge, query-string caching, compression | ✅ V | `/azure/frontdoor/front-door-caching` |
| CE9 | Browser cache is controlled by response headers; the visitor's device holds it | 🟨 K | |
| CE10 | Moving a look-aside cache means create new → repoint app → let it refill | ✅ V | migration guidance |
| CE-I | Pseudo-code, "Visitor A/B", scenarios | 🟦 I | |

## Serverless & Orchestration (`serverless-orchestration.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| SV1 | Functions plans: Flex Consumption is the recommended serverless plan for new apps (scale to zero, optional always-ready instances, Linux-only code deployments); Premium has pre-warmed workers with at least one instance running; Dedicated does not scale on events; Consumption is legacy | ✅ V | `/azure/azure-functions/functions-scale`, `/flex-consumption-plan` |
| SV2 | Durable Functions: orchestrator coordinates, activities do single units of work; function chaining and fan-out/fan-in; orchestrator checkpoints progress | ✅ V | `/azure/azure-functions/durable/durable-functions-overview` and durable-task pattern pages |
| SV3 | Logic Apps = designer-first with many prebuilt connectors; Functions = code-first; a Logic App can call a Function and vice versa | ✅ V | `/azure/azure-functions/functions-compare-logic-apps-ms-flow-webjobs` |
| SV4 | Event Grid = event routing; no ordering guarantee, transactions or duplicate detection; Service Bus offers sessions, transactions, duplicate detection | ✅ V | `/azure/service-bus-messaging/compare-messaging-services` |
| SV5 | Functions triggers and bindings; cold start differs by plan; idempotency for retried work | ✅ V (idempotency), 🟨 K (binding wording) | WAF Functions guide; scale pages |
| SV6 | `az functionapp create` flags (flexconsumption-location, runtime, version) | 🟨 K | |
| SV7 | Steady heavy work may fit an always-on plan better than a burst-oriented one | 🟨 K | general guidance |
| SV-I | Scenario names, "Activity 1/2/3", file counts | 🟦 I | |

## Infrastructure as Code (`infrastructure-as-code.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| IA1 | Bicep is a declarative language for Azure resources; deployments are idempotent | ✅ V | `/azure/azure-resource-manager/bicep/overview` |
| IA2 | what-if previews changes (Create, Modify, Delete, NoChange…) without modifying resources; run it before complete mode | ✅ V | `/azure/azure-resource-manager/bicep/deploy-what-if` |
| IA3 | Incremental mode (default) leaves resources not in the template; complete mode deletes them | ✅ V | ARM deployment REST reference |
| IA4 | Bicep has no state file; Terraform keeps state and can manage non-Azure resources; azd uses Bicep by default | ✅ V | `/azure/developer/terraform/comparing-terraform-and-bicep` |
| IA5 | Azure Verified Modules: Microsoft-maintained, versioned modules for Bicep and Terraform | ✅ V | `/community/content/azure-verified-modules` |
| IA6 | Deployment scopes: resource group, subscription, management group, tenant | ✅ V | what-if docs |
| IA7 | Store Terraform state remotely and protect it | ✅ V | `/azure/developer/azure-developer-cli/use-terraform-for-azd` |
| IA8 | Bicep compiles to ARM templates | 🟨 K | |
| IA-I | Bicep sample (`Microsoft.Storage/storageAccounts@2023-05-01`, name `stshopprod001`, SKU) and scenarios; the API version "2023" is an example only | 🟦 I | |

## CI/CD & Deployment Strategies (`ci-cd-deployment.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| CD1 | Deployment slots exist on Standard, Premium and Isolated tiers; the target stays online while the source slot is warmed up | ✅ V | `/azure/app-service/deploy-staging-slots` |
| CD2 | Swap can run in Preview (apply the target's settings to the source, then complete or cancel) | ✅ V | same page |
| CD3 | Traffic can be split by percentage to a slot; a client routed to a slot stays pinned for a time | ✅ V | same page, `/cli/azure/webapp/traffic-routing` |
| CD4 | Deploy to a non-production slot and swap; rollback by swapping again | ✅ V | `/azure/app-service/deploy-continuous-deployment`, `/deploy-best-practices` |
| CD5 | Azure Pipelines tasks deploy to a slot and swap; workload identity federation is recommended; OIDC avoids stored publishing credentials | ✅ V | `/azure/app-service/deploy-azure-pipelines`, deploy-continuous-deployment |
| CD6 | Slots share the App Service plan with production | ✅ V (Q&A) | Microsoft Q&A answer; consistent with docs |
| CD7 | Slot-specific settings do not move on swap | ✅ V | deploy-staging-slots |
| CD8 | `az webapp deploy` / `slot swap` flags | 🟨 K | |
| CD-I | Pipeline picture, scenarios | 🟦 I | |

## Secrets & Configuration (`secrets-configuration.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| SX1 | Key Vault stores secrets, keys and certificates; HSM-backed keys on the Premium tier | ✅ V | `/azure/key-vault/general/overview` |
| SX2 | Data-plane access via Azure RBAC (roles such as Key Vault Secrets User) or legacy access policies | ✅ V | `/azure/key-vault/general/rbac-guide` |
| SX3 | Soft delete keeps deleted vaults and items recoverable for a retention period; purge protection blocks permanent deletion until it ends and cannot be disabled once on | ✅ V | `/azure/key-vault/general/key-vault-recovery` (retention numbers deliberately left off the page) |
| SX4 | App Configuration: central store for settings and feature flags; change without redeploy; point-in-time replay; managed identities; sentinel-key best practice | ✅ V | `/azure/azure-app-configuration/overview`, `/howto-best-practices` |
| SX5 | App Configuration can hold Key Vault references; App Service resolves Key Vault references; needs App Configuration Data Reader and vault access | ✅ V | `/azure/app-service/app-service-configuration-references`, `/app-service-key-vault-references` |
| SX6 | Rotate regularly; use two credentials for zero-downtime rotation; apps read the latest version and refresh cached values | ✅ V | `/azure/key-vault/general/autorotation`, `/secrets/tutorial-rotation-dual`, `/azure/security/fundamentals/secrets-best-practices` |
| SX7 | Prefer managed identity over stored secrets; where unavoidable fetch from Key Vault; for Storage prefer Entra ID over shared keys and disable shared-key access where allowed | ✅ V | Safe Secrets Standard (`/security/zero-trust/sfi/safe-secrets-standard`) |
| SX8 | `az keyvault create` / `az role assignment create` flags | 🟨 K | |
| SX-I | "10% of users" scenario, vault and app names | 🟦 I | |

## Security & Governance (`security-governance.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| SG1 | Zero Trust: verify explicitly, least privilege, assume breach | ✅ V | `/azure/security/fundamentals/zero-trust` |
| SG2 | Defense in depth layers (identity, network, compute, data); identity is the primary line, network supports it | ✅ V | `/azure/security/fundamentals/overview`, `/azure/well-architected/security/segmentation` |
| SG3 | Policy effects deny, audit, modify, deployIfNotExists; deny stops the request, audit logs it; modify changes resources on create/update and only marks existing ones non-compliant; DINE deploys a template; deny is evaluated before audit | ✅ V | `/azure/governance/policy/concepts/effect-basics`, `/effect-modify` |
| SG4 | Start with audit before enforcing | ✅ V | same pages |
| SG5 | Modify and deployIfNotExists need a managed identity with the minimum role; remediation tasks fix existing resources; initiatives need a task per policy | ✅ V | `/azure/governance/policy/how-to/remediate-resources` |
| SG6 | A policy assigned at a scope applies to resources beneath it (inheritance) | ✅ V (secondary) | policy overview + Q&A on child-scope inheritance |
| SG7 | Defender for Cloud: CSPM (free foundational plan, paid Defender CSPM), secure score, workload-protection plans for servers, containers, storage, databases | ✅ V | `/azure/defender-for-cloud/defender-for-cloud-introduction`, `/concept-cloud-security-posture-management` |
| SG8 | WAF is layer 7, OWASP-based rules, regional on Application Gateway and at the edge on Front Door; Front Door managed rule sets need Premium (Standard has custom rules); custom rules and rate limiting | ✅ V | `/azure/web-application-firewall/*` |
| SG9 | WAF does not mitigate volumetric network DDoS; use DDoS Protection together with a WAF | ✅ V | WAF docs |
| SG10 | Resource locks can protect against accidental deletion | 🟨 K | not searched |
| SG11 | `az policy assignment create` flags | 🟨 K | |
| SG-I | Scenario names, subscription A/B | 🟦 I | |

## Monitoring & Observability (`monitoring-observability.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| MO1 | Azure Monitor combines metrics, logs, traces and events | ✅ V | `/azure/azure-monitor/fundamentals/overview` |
| MO2 | Log Analytics workspaces hold logs/traces queried with KQL; Azure Monitor workspaces hold Prometheus/OpenTelemetry metrics queried with PromQL | ✅ V | same page |
| MO3 | Application Insights is the APM feature; instrument with OpenTelemetry (some OpenTelemetry paths are in Preview); distributed tracing; its data lands in a Log Analytics workspace | ✅ V | `/azure/azure-monitor/app/app-insights-overview` |
| MO4 | Platform metrics collected about every minute by default | ✅ V | `/azure/azure-monitor/metrics/data-platform-metrics` |
| MO5 | Platform metrics and the activity log are collected automatically; resource logs need a diagnostic setting; resource-specific tables recommended; diagnostic settings cannot filter within a category; built-in Policy can deploy them at scale | ✅ V | `/azure/azure-monitor/platform/diagnostic-settings`, `/diagnostic-settings-policy` |
| MO6 | Alert types: metric, log, activity-log; action groups can email, SMS, push, run automation runbooks, Functions, ITSM, Logic Apps, webhooks | ✅ V | `/azure/azure-monitor/alerts/alerts-overview` |
| MO7 | Every alert needs an owner / alert on symptoms | 🟨 K | operational guidance |
| MO8 | The KQL example (`requests`, `success`, `timestamp`) | 🟨 K | table names depend on setup |
| MO-I | Scenarios | 🟦 I | |

## Cost Management (`cost-management.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| CO1 | Budgets can be scoped to subscription, resource group or resource sets; use actual or forecast cost; can trigger action groups, including ones that stop VMs | ✅ V | `/azure/cost-management-billing/costs/tutorial-acm-create-budgets`, budget scenario |
| CO2 | Azure has no built-in hard cap for a whole subscription; alerts are the main defence | ✅ V | `/azure/cost-management-billing/manage/cost-management-budget-scenario` |
| CO3 | Tags are the way to add your own business context to cost; tag inheritance; allocation rules do not cover reservations or savings plans | ✅ V | `/azure/cost-management-billing/costs/allocate-costs` |
| CO4 | Reservations are prepaid one- or three-year commitments; the savings plan for compute is the most flexible commitment (discount percentages deliberately left off the page) | ✅ V | `/azure/cost-management-billing/costs/overview-cost-management`, savings docs |
| CO5 | Advisor flags VMs with little use over a week and suggests shutdown or a cheaper size; orphaned resources appear after a parent is deleted | ✅ V | `/azure/advisor/advisor-cost-recommendations` |
| CO6 | Spot VMs: spare capacity, can be evicted with a short warning (Scheduled Events), not checkpointed work is lost, choose deallocate or delete | ✅ V | `/azure/virtual-machines/spot-vms` |
| CO7 | Hybrid Benefit uses existing Windows Server or SQL Server licenses | ✅ V | Cost Management docs |
| CO8 | Cut waste before committing to discounts | 🟨 K | FinOps guidance |
| CO9 | `az group update --tags` flags | 🟨 K | |
| CO-I | Tag example (`cc-1042` is an example value); scenarios | 🟦 I | |

## Well-Architected & Landing Zones (`well-architected.html`)

| # | Claim | Status | Source / note |
|---|---|---|---|
| WA1 | Five pillars: Reliability, Security, Cost Optimization, Operational Excellence, Performance Efficiency | ✅ V | `/azure/well-architected/pillars` |
| WA2 | Design must be balanced across pillars; recommendations may mean trade-offs against others; document trade-offs | ✅ V | `/azure/well-architected/what-is-well-architected-framework`, CAF cloud-native planning |
| WA3 | Zone-redundant is often the best balance; multi-region raises reliability, cost and complexity | ✅ V | `/azure/well-architected/design-guides/regions-availability-zones` |
| WA4 | Landing zone = platform landing zone (shared services) + workload landing zones; design areas include identity, network, security, management, governance, automation | ✅ V | `/azure/cloud-adoption-framework/ready/landing-zone/`, `/design-areas` |
| WA5 | CAF renamed "application landing zones" to "workload landing zones" and dropped separate data landing zones; detailed architecture guidance now mainly in the Architecture Center and WAF | ✅ V | `/azure/cloud-adoption-framework/whats-new` (single search result; re-check) |
| WA6 | Advisor recommends across cost, performance, reliability, security, operational excellence | ✅ V | `/azure/advisor/advisor-overview` |
| WA7 | Mapping of pillars to earlier concepts | 🟦 I | teaching model |
| WA-I | Scenarios | 🟦 I | |

---

## Open verification list (do these with direct docs access)

Everything marked 🟨 K above, in priority order: **RH4 / RH10 / RH11** (management-group and ARM wording), **RG8 / RG10** (region price differences), **VN9 / VN10** (peering overlap; VPN vs ExpressRoute wording), **CP10 / CP11** (App Service plan and AKS control-plane wording), **PE8**, **ID10**, **MI7**, **S7** (Table storage wording), **S10** (three copies),
**SC5 / DR6 / CE9 / LB10 / SC11** (general terms and CLI flags), **MO7 / MO8 / CO8 / CO9 / WA5** (WA5: re-check the landing-zone rename), **SG10 / SX8 / SG11 / SV6 / SV7 / CD8 / IA8** (locks, CLI flags, general guidance), **D6** (MySQL Flexible Server), **C1** (JOIN inside one item), **B6** (Function trigger for blob events),
**E2** (same key → same partition), and the SDK method names (**B16, C14, M12, SB-I, E9**).
After checking a row, change 🟨 K to ✅ V and add the exact page URL.
