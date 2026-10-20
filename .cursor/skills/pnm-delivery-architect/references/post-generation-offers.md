# Post-Generation Offers (STEP 6)

After an artifact passes the validator, offer the actions below — **only those
whose capability is bound** (by the adapter or the environment). Name the
capability, never a specific tool. If a capability is unbound, say so and,
where one exists, give the fallback.

| # | Offer | Capability needed | Input | Output | Fallback when unbound |
|---|---|---|---|---|---|
| 1 | Convert ACs into test-automation prompts | none | The ACs and Pattern E tables | One prompt per AC: preconditions, steps, expected records and fields | — always available |
| 2 | Dependency, lifecycle or data-flow diagram | diagram rendering (optional) | Technical Implementation, Pattern E | Diagram | Mermaid in the artifact |
| 3 | Create or update a work item | work-item tracking | Story, effort, AC count | Work item with link back to the artifact | Paste-ready summary |
| 4 | Re-verify product claims | official-documentation lookup | Every `[Product]` name in the artifact | List of claims re-checked, with date and any change | List of claims to check by hand, with source IDs |
| 5 | Add the artifact to a knowledge base | knowledge-base ingestion | Saved artifact | Ingestion confirmation | — |
| 6 | Overlap and dependency check | story-index search | Story title, objects, components | Overlapping or conflicting stories with links | Disclose the check was not run (validator item 8) |
| 7 | Create or refine the grounded prototype | none | Approved plan or story | Single-file HTML per `references/slds2-pnm-primer.md` | — always available |
| 8 | Record-lifecycle diagram | none | Discovered status model (D-5) | State diagram per record type; stages labelled with provenance | — always available; unknown states shown as `[Assumed — confirm]` |
| 9 | Validation-query pack | org-query capability (optional); query archive (optional) | Pattern E outcomes | One query per outcome, described by intent, object, filter and expected result; saved to the adapter's archive when configured | Query intents in the artifact |
| 10 | Parity checklist | none | Migration or refactor scope | Field-by-field before/after checklist per record type | — always available |

Rules:

- Offer at most the top four most useful for the artifact; list the rest in
  one line.
- Never perform a write to an org as part of an offer.
- When an offer produces queries for the person to run and the adapter names
  a query archive, save them there.
