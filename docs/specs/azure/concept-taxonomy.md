# Azure category — concept taxonomy

The fixed journey order for the Azure category, written from a *developer-turned-architect*
perspective: what someone designing and operating real systems on Azure has to know, in the order each
need appears. The order and the "why it exists" reasoning are provider-neutral on purpose — the
Azure and AWS categories share the same 19-step shape (and the same journey-map layout), and only
the service names differ. Keep them in sync: if one reorders, discuss the other.

**Do not reorder these without discussion** — the journey map (`azure/index.html`), the concept list on that
same page, and this file must always agree on order.

Per `../../rules/accuracy.md`, when a page is actually written, verify its own "why did this need to
exist" box and every service name/capability independently — cloud services are renamed, merged
and retired often; check the provider's current docs rather than copying this table or trusting memory.

| # | Concept | Why it exists (what the previous concept couldn't do) |
|---|---|---|
| 1 | Tenants, Subscriptions & Resource Groups | Starting point — before anything is deployed you need a place for it to live, a unit that gets billed, and a boundary that permissions attach to. Nothing precedes it. |
| 2 | Regions & Availability Zones | A single datacenter is a single failure domain, and users far from it feel latency — where you place resources decides both resilience and speed. |
| 3 | Identity & Access | Once resources exist across places, the question becomes who or what is allowed to create, read or change each one — including the apps themselves, not just people. |
| 4 | Virtual Networks | Identity says who may call what; networking decides what can physically reach what. Resources need isolation and controlled paths before they hold real traffic or data. |
| 5 | Compute | Code needs somewhere to run — and how much of the machine you manage (VM → platform → container → function) is the first big trade-off. |
| 6 | Storage | Compute is disposable; data isn't. Files, blobs and disks need durable homes with different access shapes (object, file, block). |
| 7 | Databases | Structured, queryable, transactional data needs more than files — relational and NoSQL engines trade consistency, scale and query power differently. |
| 8 | Load Balancing & Traffic Routing | Compute, storage and a database make one working instance — but one instance is a single point of failure and a throughput ceiling, so traffic must be spread. |
| 9 | Scaling & Resilience | Load changes and components fail; fixed capacity is either wasted or overwhelmed — scaling and resilience (autoscale, redundancy, backup, DR) respond to both. |
| 10 | Caching & Edge Delivery | Scaling out everything is expensive; much of the load is repeat work or bursty — caching, queues and serverless each absorb spikes without scaling blindly. Grouped because they are three different answers to the same pressure. |
| 11 | Messaging & Events | Synchronous call chains fail together under load; a queue or event bus decouples producers from consumers so they can scale and fail independently. |
| 12 | Serverless & Orchestration | Some work is spiky or event-shaped — running it as functions/orchestrated workflows avoids paying for idle capacity. |
| 13 | Infrastructure as Code | By now the system is dozens of resources; clicking them together in a portal isn't repeatable, reviewable, or recoverable. |
| 14 | CI/CD & Deployment Strategies | Environments defined as code still need a safe, automated way to build and roll out changes — and to roll them back. |
| 15 | Secrets & Configuration | Pipelines and apps need credentials and configuration; hard-coding them in code or pipelines is the classic leak. |
| 16 | Security & Governance | Secrets are one slice of security — an architect also needs guardrails (policy), threat detection and protective layers applied consistently across every resource. |
| 17 | Monitoring & Observability | Controls say what should happen; you still need to see what actually did — metrics, logs, traces and alerts, including for the controls themselves. |
| 18 | Cost Management | Everything above is metered. Without visibility and levers on spend, a good design can still be an unaffordable one. |
| 19 | Well-Architected & Landing Zones | The capstone: every earlier concept is a trade-off between reliability, security, cost, operations and performance — the provider's Well-Architected Framework and landing zones are how architects reason about all of them together. |

## Branch structure

Concepts 5–7 (Compute / Storage / Databases) form one branch cluster — three building blocks that all sit inside the network from concept 4 — and concepts 10–12 (Caching & Edge / Messaging / Serverless) form a second, three different answers to load pressure. Both clusters rejoin the main spine. The shape deliberately mirrors the AI category's hub.

## Scope notes

- **Included:** the services/ideas a developer must know to *design* a sound system — not an
  exhaustive service catalogue.
- **Deliberately not in the first pass:** deep dives on analytics/data-warehouse platforms, ML
  platforms, IoT, hybrid/on-prem connectivity details, and multi-cloud. Any of these can be added
  as new concepts later following `../../rules/content-structure.md`'s "inserting a concept into an
  existing taxonomy" rule.
