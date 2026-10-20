# Integrations Reference

Use this when a scenario touches discovery dimension D-12 (integrations and
consumers) or applicability check A-5 (downstream impact). It describes
integration **archetypes**; the target's actual systems are always
`[Discovered]` or `[Adapter]` — never assume a vendor or a consumer.

## Contents

1. Integration archetypes
2. Platform patterns
3. Design rules
4. Downstream Impact table — artifact format

---

## 1. Integration archetypes

| Archetype | Direction | Scenarios | Product or public reference | Typical pattern |
|---|---|---|---|---|
| Credentialing data source (practitioner self-reported profile) | Inbound | IN-01, RE-02, RO-04 | S9 — MuleSoft CAQH Connector (ProView and DirectAssure operations) | Middleware connector; pre-fill on demand; roster operations in batches |
| National NPI registry | Inbound lookup | IN-07, PD-02 | S13 — read-only API v2.1, NPI-1 / NPI-2, up to 200 results per request | Callout per NPI, or bulk via downloaded files at volume |
| National practitioner data bank | Inbound | CR-05, RE-04 | S12 — one-time and continuous query; external application access | Middleware or manual with uploaded evidence |
| Exclusion lists | Inbound | CR-03, RE-04 | S14 — online search, CSV download, monthly supplements | Scheduled file match |
| Verification organisation | Inbound | CR-04 | — | Named Credential callout with asynchronous status |
| Address verification | Inbound lookup | IN-05 | — | Callout from the entry UI; standardised value stored |
| E-signature | Both | IN-01, CT-06 | S7 — DocuSign integration | Shipped integration |
| Roster files | Inbound | RO-01…RO-05, DG-01 | S7 — Roster File Mapping (Data 360) | Shipped mapping, or bulk staging |
| Claims platform | Outbound | OB-03, PD-03, TR-04 | — | Change events into middleware |
| Enterprise data warehouse | Outbound | OB-03 | — | Change data capture stream or scheduled extract |
| Provider directory | Outbound | DS-04, NW-06 | S8 — Provider Search API and index | Index sync, or file feed |
| National and association feeds | Outbound | OB-03 | — | Scheduled file |
| Banking and payment | Inbound or outbound | PD-03 | — | Middleware |

## 2. Platform patterns

| Need | Options (choose by volume and latency) |
|---|---|
| Call an external API from a user action | Named Credential + External Credential; Apex or Flow HTTP callout; asynchronous continuation when slow |
| Receive inbound records | REST or composite API for small volumes; Bulk API 2.0 for files; Upsert Provider API for business-level practitioner upserts (S8) |
| Publish changes outbound | Change Data Capture (change events exist on many provider objects — S5); Platform Events for business events; Pub/Sub API for subscribers |
| File-scale ingestion | Roster File Mapping on Data 360 (S7); middleware; bulk Apex with staging (volume rule) |
| Keep legacy consumers working | Bridge mappings in middleware, retired as consumers move (PL-03) |

## 3. Design rules

1. **Idempotency.** Every inbound write upserts on a stable external key —
   SourceSystem plus SourceSystemIdentifier on product objects, or the
   target's external ID (PL-01). Re-running a load must not duplicate records.
2. **Partial success.** Report success and failure per record; never fail a
   whole file for one bad row unless the business asks for it.
3. **Ordering.** Outbound consumers receive parents before children and
   changes in commit order; state how replays are handled.
4. **Error capture and retry.** Name where failures are recorded and who works
   them; retries are bounded and visible.
5. **Sensitive data.** State which fields leave the org and how they are
   protected in transit and at rest (A-9).
6. **Effective dating.** Say whether consumers receive future-dated changes
   immediately or on their effective date.
7. **No named tools.** An artifact names the target's systems only when
   `[Discovered]` or `[Adapter]`; otherwise it names the archetype.

## 4. Downstream Impact table — artifact format

Required when A-5 applies:

```
### Downstream Consumers (A-5)

| Consumer | What changes for it | Timing (immediate / effective date) | Mechanism | Provenance |
|---|---|---|---|---|
| <consumer from D-12> | <fields or records> | <timing> | <pattern> | [Discovered] / [Adapter] / [Assumed — confirm] |
```

If D-12 is unknown, the table has one row — "Consumers not yet identified" —
and a Clarification Question.
