# Org Discovery (Layer 3)

Before naming any custom object, field, prefix, record type, status value,
stage or downstream system, determine how the **target org** actually works.
Org Discovery replaces any notion of a default organisation: **nothing is
selected until discovery runs or the user confirms.**

## Contents

1. Discovery dimensions D-1…D-13
2. Depth by workflow mode
3. Procedure
4. Archetypes (vocabulary only)
5. Org Discovery Context table (artifact format)
6. Conflicts and unknowns

---

## 1. Discovery dimensions

| # | Dimension | Question to answer | Example outcomes (never defaults) | Evidence to look for |
|---|---|---|---|---|
| D-1 | Provider anchor | Where does a provider's identity live? | HealthcareProvider; Account/Contact; an application record; a custom object; a mix | Which objects hold NPI, name, provider type; where lookups point |
| D-2 | Identifier model | How are NPI, tax ID, licence and legacy IDs stored and historised? | Product identifier objects; custom history objects; fields on the anchor | Identifier objects, external IDs, history objects, duplicate rules |
| D-3 | Location model | How are practice and billing locations represented? | HealthcareFacility + HealthcarePractitionerFacility; Account hierarchy; custom | Location-type records, address storage, primary-location flags |
| D-4 | Participation model | At what grain is network participation recorded, and is anything derived automatically? | Practitioner-location-network rows; contract-based rows; parent/child networks; tiers; rows created by automation | Participation objects, record types, triggers or flows that create participation rows |
| D-5 | Status & temporal model | How does a record become effective, active, suspended or terminated? | IsActive + effective dates; staged flags; status picklists; several at once; none | Status picklists and their values, effective-date fields, automation that flips them |
| D-6 | Work model | How is work routed and owned? | Case per stage; tasks per data-domain queue; work guides; Omni-Channel; owner rules on returns | Queues, assignment rules, case record types, stage fields, routing configuration |
| D-7 | History & audit | How are changes tracked? | Field history; Shield Field Audit Trail; custom history objects; change-history UI | History tracking settings, history objects, audit components |
| D-8 | Naming & conventions | What prefix, naming and layering rules apply to custom components? | A discovered prefix; none (greenfield) | Recurring prefixes in custom metadata; documented conventions |
| D-9 | Build technology in use | What already implements PNM behaviour? | OmniStudio (which runtime), Flow, LWC, Apex services, Data 360, middleware | Component inventories; active versions only |
| D-10 | Licences & features | Which PNM-related licences and features are enabled? | PNM add-on, Data 360, Shield, Experience Cloud, Agentforce | Licences, permission set licences, enabled features |
| D-11 | Volumes | Typical and peak submissions, roster sizes, rows per transaction | Single records; tens per day; files of thousands of rows | Record counts, file sizes, user statements |
| D-12 | Integrations & consumers | What feeds in and what consumes provider data? | Credentialing data sources, verification services, address services, claims, data warehouse, directory, national/association feeds | Named credentials, external services, events, outbound jobs, user statements |
| D-13 | Compliance scope | Which accreditation, delegation and state/federal rules apply? | Accreditation programs, delegation agreements, state or federal program rules | User statements, existing policy documents |

---

## 2. Depth by workflow mode

| Mode | Depth | Dimensions that must be resolved or flagged before generating |
|---|---|---|
| New Feature, Plan + Prototype, Epic Breakdown | Full | All that the selected scenarios name; always D-1, D-5, D-8, D-10, D-11 |
| Legacy → PNM Migration | Full, plus the legacy side | All thirteen, and the legacy equivalents of D-1…D-5 and D-12 |
| Refactor, Bug Fix | Component-scoped | Dimensions the component reads or writes; D-8 and D-9 for the component |
| Data Remediation | Component- and data-scoped | The dimensions of the affected records; D-7, D-11, D-12 |

A dimension may stay unresolved only if it does not change the artifact; say so
in the context table.

---

## 3. Procedure

1. **Adapter first.** If a workspace adapter is present, read its
   `discovery.preanswers`, `conventions` and `overlay`
   (`references/workspace-adapter.md`). Pre-answers are `[Adapter]`, not
   `[Discovered]`.
2. **Inspect the target**, in this order, using whatever capabilities are bound:
   - org metadata — object and field describes, record types, picklist
     values, licences, permission sets, queues;
   - source metadata in the workspace — objects, fields, Apex, OmniStudio,
     Flows, LWC (active versions only);
   - the metadata-dependency capability, if bound, for who-uses-what. Its
     edges are deploy-time references; dynamic dispatch configured in data
     or metadata is invisible to it and must be read separately;
   - existing requirement documents, if the story-index capability is bound.
3. **Ask the user** for every dimension still unknown that changes the
   artifact. Use the structured-question capability when bound; otherwise ask
   one grouped, numbered free-text question, offering the outcomes detected so
   far as choices.
4. **Record the result** in the Org Discovery Context table (§5) at the top of
   every artifact.

If no capability is bound and the user cannot answer, proceed with product
baseline objects labelled `[Assumed — confirm]` and say plainly that the design
is unverified against the target.

---

## 4. Archetypes (vocabulary only)

Use these to *describe* what was found. **An archetype never selects a
default** — not a prefix, a status model, a stage sequence or an object.

| Archetype | Signature |
|---|---|
| **Product-anchored** | Provider identity on HealthcareProvider; participation on product objects |
| **Custom-anchored** | Provider identity on Account/Contact, an application record or a custom object; product objects used selectively and extended |
| **Hybrid** | Both patterns in use — flag every place they meet, because writes may need to land in both |
| **Greenfield** | PNM licensed but little or nothing built — propose the product baseline first |

---

## 5. Org Discovery Context table (artifact format)

Place directly after the header of every story, epic and Solution Plan.

```
## Org Discovery Context

**Archetype:** <Product-anchored | Custom-anchored | Hybrid | Greenfield | Unknown>
**Discovery depth:** <Full | Component-scoped | Data-scoped> · **Capabilities used:** <e.g. org query, source search — or "none bound">

| # | Dimension | Finding | Provenance | Evidence |
|---|---|---|---|---|
| D-1 | Provider anchor | <finding> | [Discovered] | <where it was found> |
| D-5 | Status & temporal model | <values and fields, or "unknown"> | [Assumed — confirm] | Clarification Q1 |
| … | … | … | … | … |
```

Rules:

- Include every dimension the artifact depends on; omit the others or mark
  them "not relevant to this change".
- `[Discovered]` rows must name where the fact was seen (object, component or
  file — whatever the capability returned).
- Every `[Assumed — confirm]` row has a matching Clarification Question.
- Never copy a finding from another organisation, an example or a scenario
  card into this table.

---

## 6. Conflicts and unknowns

- **Two mechanisms for one concept** (for example, both a status picklist and
  an active flag driving the same record): list both, ask which governs, and
  make the choice a Clarification Question. Never pick one silently.
- **Product object present but unused**: note it; do not write to it unless
  the user confirms.
- **Licence not confirmed**: apply the licence rule in
  `references/pnm-product-baseline.md` §1.
- **Discovered names that look organisation-specific** are fine to use for
  that target — they are `[Discovered]`. They must never appear in an artifact
  for any other target.
