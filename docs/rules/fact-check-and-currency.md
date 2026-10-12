# Fact-check and currency rule — never hallucinate, never ship stale

Extends `accuracy.md` (read it first). Cloud services are renamed, merged, retired and re-priced
constantly, and a confident-but-wrong sentence on a learning site is worse than a missing one.
This file turns "be accurate" into a repeatable procedure with files you can audit.

## The four rules

1. **Official docs only.** The source for a technical claim is the provider's own documentation
   (Azure: `learn.microsoft.com`; AWS: `docs.aws.amazon.com`, plus the official pricing/"what's new"
   pages for retirements). Blogs, forums, Q&A threads and training sites are leads, never sources.
   If only a secondary source supports a claim, mark it as such in the ledger and keep the wording soft.
2. **Nothing volatile unless verified and necessary.** Prices, SLA percentages, quotas/limits,
   instance sizes, regional availability, version numbers, preview features and retirement dates
   change. Prefer a durable wording ("a limited window that depends on the tier", "the older Single
   Server has been retired") over a number. When a number teaches something (30/90/180-day minimum
   stay), verify it **and** put it in the ledger.
3. **Every claim has a ledger row.** `docs/specs/<cat>/claims-ledger.md`. `scripts/check-site.js`
   scans each page for numbers, sizes, years, percentages, prices and words like preview/retired and
   **warns for every one that is not in the ledger** — a number cannot reach a page unnoticed.
4. **If sources disagree, leave it out.** Say the general pattern instead. (Example from the Azure
   run: one Microsoft page called Hyperscale serverless auto-pause a preview, another said it was
   unsupported → the page says only "serverless can pause when idle" for the tier where it is documented.)

## How to verify in a sandboxed session

Direct page fetches may be blocked by the network policy (they were in the Azure session). Use the
search tool restricted to the docs domain — it returns snippets quoted from the real pages:

```
WebSearch(query="Azure Service Bus tiers Basic Standard Premium topics supported",
          allowed_domains=["learn.microsoft.com"], mode="standard")
```
- Search per claim cluster, in parallel, with the service name and the exact thing you will assert.
- Write down the **page URL** the snippet came from. Only URLs you actually saw go in the ledger.
- Quotes that mention dates ("updated within the last 6 months") are a freshness signal; old
  Q&A/archive/blog results are not.
- If the tool cannot reach the docs at all, do not fall back to memory silently: mark every claim 🟨 K,
  keep wording conservative, and tell the user.

## Ledger format

| Status | Meaning | Allowed on a page? |
|---|---|---|
| ✅ V | text from an official page supports it; URL recorded | yes |
| 🟨 K | well-established, from knowledge, not re-verified | yes, if conservative; **must be listed in the "Open verification list"** and reported to the user |
| 🟦 I | illustrative example / UI label (not a claim) | yes, labelled "illustrative" on the page where it could be mistaken for fact |
| 👤 U | from a screenshot/text the user supplied | yes |

A row: `| id | claim as written | status | source URL or note |`. Keep ids stable (S1, B7 …) so reviews
can cite them. When a claim changes, change the page and the row in the same commit.

## What to double-check even though it feels obvious

- **Names**: product names change (Azure AD → Microsoft Entra ID; "Classic file shares" label;
  Cosmos DB "in Azure and Fabric"). Use the current name and, if the old one is still widely used,
  mention it once.
- **Retired / replaced services**: PostgreSQL Single Server → Flexible Server. Keep a watch list in
  the category playbook and check each service you name against the provider's retirement pages.
- **Defaults**: say "by default" only for documented defaults (Service Bus max delivery count 10;
  Cosmos DB default consistency Session).
- **Absolutes**: "always", "never", "only", "unlimited" — remove unless the docs say it.
- **SDK/CLI/API names** in code samples: mark K unless checked; label examples "illustrative shape only".
- **Diagrams are claims too**: every box, arrow label and caption goes through the same ledger.

## Page-level currency markers

- Each concept page ends with a `.fact-note` linking the **stable doc roots** for the services it covers.
  Only link roots you have seen (`/azure/storage/`, `/azure/service-bus-messaging/`, …). Never invent a deep URL.
- The ledger header records the verification date and method. Re-verify a category's ledger when
  (a) you touch the page, (b) a service on it is announced as renamed/retired, or (c) every ~6 months.

## Review questions before you push

1. Could I show the doc sentence behind every number and every "only/always" on this page?
2. Is any service, tier, feature or API name on the page possibly retired or renamed?
3. Does a diagram label say something the caption or ledger does not support?
4. Did I tell the user which claims are 🟨 K?
