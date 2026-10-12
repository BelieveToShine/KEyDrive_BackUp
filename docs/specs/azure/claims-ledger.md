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

## Open verification list (do these with direct docs access)

Everything marked 🟨 K above, in priority order: **S7** (Table storage wording), **S10** (three copies),
**D6** (MySQL Flexible Server), **C1** (JOIN inside one item), **B6** (Function trigger for blob events),
**E2** (same key → same partition), and the SDK method names (**B16, C14, M12, SB-I, E9**).
After checking a row, change 🟨 K to ✅ V and add the exact page URL.
