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

---

## Open verification list (do these with direct docs access)

Everything marked 🟨 K above, in priority order: **RH4 / RH10 / RH11** (management-group and ARM wording), **RG8 / RG10** (region price differences), **VN9 / VN10** (peering overlap; VPN vs ExpressRoute wording), **CP10 / CP11** (App Service plan and AKS control-plane wording), **PE8**, **ID10**, **MI7**, **S7** (Table storage wording), **S10** (three copies),
**D6** (MySQL Flexible Server), **C1** (JOIN inside one item), **B6** (Function trigger for blob events),
**E2** (same key → same partition), and the SDK method names (**B16, C14, M12, SB-I, E9**).
After checking a row, change 🟨 K to ✅ V and add the exact page URL.
