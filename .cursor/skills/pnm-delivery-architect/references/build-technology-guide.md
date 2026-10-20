# Build-Technology Decision Guide (PNM)

Declarative-first, product-first — and in PNM the **volume class decides
early**. Walk the ladder from rung 0 and stop at the first rung that meets the
requirement; state the rejected rungs and why.

## Contents

1. The ladder
2. Volume rule
3. Runtime rule (OmniStudio)
4. Reuse rule
5. Decision record format

---

## 1. The ladder

| Rung | Technology | Use when | Examples |
|---|---|---|---|
| 0 | **Shipped PNM capability** | A product component, app, OmniScript or API already does it | Network Participation component; PNM app; shipped recruitment and PSV OmniScripts; Roster File Mapping; contract approval and versioning; Upsert Provider API; Provider Search API |
| 1 | **Configuration** | Layout, visibility, simple automation | Dynamic Forms and Actions, related lists, list views and queues, record types, validation rules, duplicate rules, work guides, Path, field history |
| 2 | **Flow** | Guided or record-triggered work at single-record volume | Screen Flow wizards, Flow Orchestration for go-live, scheduled reminder flows |
| 3 | **OmniStudio** (runtime discovered) | Branching guided interactions, portal forms, reusable server orchestration | Portal application, contract generation, provider 360 cards |
| 4 | **LWC** | UI the rungs above cannot give | Dense multi-row edit grids, steppers with complex state, change-history timelines |
| 5 | **Apex services and async processing** | Multi-record or multi-provider writes, complex validation, cross-object bulk writes | Bulk intake, mass network changes, activation across many records |
| 6 | **Data 360 / Data Processing Engine / middleware / external** | File-scale ingestion, enterprise integration, verification services | Roster mapping, CAQH, claims and data-warehouse feeds, address verification |
| 6a | **Agentforce** | Conversational or autonomous assistance with human review | Payer contact-centre agent; a proposed credentialing assistant |

Product facts for rung 0 are in `references/pnm-product-baseline.md` §5.
Licence-gated capabilities follow the licence rule (§1 of that file).

---

## 2. Volume rule

Determine the volume class (D-11) for **every write path** (A-6):

| Class | Typical signal |
|---|---|
| Single record | One provider, one save |
| Small batch | Tens of records per action — e.g. one practitioner with many locations and networks |
| Multi-provider | One submission covering many providers |
| File-scale | A roster or file of hundreds to tens of thousands of rows |

When a path is **multi-provider or file-scale**, or one transaction cannot
safely hold its writes:

1. **Do not** propose a record-by-record declarative chain (Flow loops, chained
   Omnistudio Data Mapper loads per record) for that path.
2. **Present the viable options with trade-offs:**
   - shipped bulk capability (rung 0 — e.g. Roster File Mapping, Upsert
     Provider API);
   - Data 360 / Data Processing Engine or middleware (rung 6);
   - bulk Apex with asynchronous processing (rung 5).
3. **State the governor strategy** for the chosen option: one bulk write per
   object type per transaction, a fresh set of limits per asynchronous unit,
   idempotent upserts on stable external identifiers, error capture per
   record, a fallout report, and retry that does not duplicate completed work.
4. **State partial-failure behaviour**: what is kept, what is retried, what the
   persona sees.

---

## 3. Runtime rule (OmniStudio)

- Discover the OmniStudio runtime in use (D-9). Never assume one.
- For greenfield work, compare the currently supported runtimes from current
  official guidance and the target's constraints (installed packages,
  existing components, deployment tooling), then recommend one with the
  reason.
- Ground every existing OmniStudio component against its **active** version.
- Prose uses **Omnistudio Data Mapper**; "DataRaptor" appears only as an alias.

---

## 4. Reuse rule

- Reuse an in-org framework (async engine, logging, selector layer, trigger
  framework) **only if it is `[Discovered]`** — and name where it was found.
- Otherwise any framework is `[Proposed]` and sized in Estimated Effort.
- Never import a framework design from an example, a scenario card or another
  organisation.

---

## 5. Decision record format

Place in Technical Implementation (stories) or "Proposed solution and
alternatives" (Solution Plans):

```
**Build technology:** <chosen rung(s)> — <one-line reason>
**Rejected:** <rung> — <reason>; <rung> — <reason>
**Volume class:** <class> → <volume rule applied: option + governor strategy | not triggered>
**OmniStudio runtime:** <discovered value | recommended for greenfield + reason | not used>
```
