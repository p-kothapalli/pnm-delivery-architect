# PNM Delivery Architect

A portable Cursor skill that acts as a Salesforce Delivery / Solution Architect
for **Health Cloud Provider Network Management (PNM)**. It produces three
artifacts, on demand and independently:

1. **Solution Plan** — Org Discovery summary, scenario coverage,
   build-technology decision, component inventory, effort.
2. **Grounded HTML prototype** — every element labelled with the Salesforce
   technology that will implement it.
3. **Implementation-ready user story or epic** — business persona,
   Given/When/Then, Pattern E record specifications, Technical
   Implementation, Compliance & Audit, effort.

## Client-neutral by design

The skill carries Salesforce product knowledge and generalised PNM scenarios.
It ships **no organisation's** names, prefixes, stage models, status values,
paths or tool bindings. Those are discovered at run time (Org Discovery) or
supplied by an optional, workspace-owned adapter that is never committed here.

| Layer | Ships here | Per organisation |
|---|---|---|
| 1 Product baseline | Yes | — |
| 2 Scenario library (92 scenarios, 16 domains) | Yes | — |
| 3 Org Discovery | Procedure | Results |
| 4 Workspace adapter | Blank template | Instance |
| 5 Delivery contract | Yes | — |

## Install

Copy `.cursor/skills/pnm-delivery-architect/` and
`.cursor/rules/use-pnm-delivery-architect.mdc` into a workspace (or into
`~/.cursor/` for all workspaces). Nothing needs to be installed: there are no
MCP or tool prerequisites. If the workspace has tools for org queries, source
search or structured questions, bind them in an adapter
(`references/workspace-adapter.md`); otherwise the skill falls back to asking.

## Validate

```bash
python3 .cursor/skills/pnm-delivery-architect/tools/validate.py
python3 .cursor/skills/pnm-delivery-architect/tools/validate.py --denylist my-org-terms.txt
python3 .cursor/skills/pnm-delivery-architect/tools/validate.py --artifacts path/to/Story.md path/to/Prototype.html
```

The validator checks package integrity (references, links, scenario index and
cards with their evidence, AC patterns, badges, primer blueprints, object
catalog, evaluations, verification dates), runs the neutrality scan (built-in
rules plus an optional denylist), and lints generated artifacts. CI runs the
same command.

## Status — v1.1

| Area | Contents |
|---|---|
| Entry point | `SKILL.md`, trigger rule |
| Product | Baseline (licences, verified fields, capabilities, dated source register), object catalog (29 objects with field entries; unavailable pages marked not verified), reference lifecycle |
| Scenarios | Index of 92 scenarios across 16 domains; deep cards for the six core domains, compact cards for the other ten; every card has a Basis and an exact Evidence line |
| Org | Org Discovery procedure, workspace adapter template |
| Delivery | Persona contract and AC Patterns A–G, output templates, story examples, build-technology guide, SLDS 2 primer with badge overlay and 12 blueprints, post-generation offers |
| Specialist references | Compliance and credentialing, integrations, legacy migration, data remediation |
| Quality | Validator, neutrality baseline, evaluations 01–16 with neutral fixtures |

Not yet run: the evaluations themselves (they need a live agent session per
fixture; see `evaluations/README.md`). The CI workflow file must be added by
hand.

## Lineage

Structurally modelled on the [LSC Delivery Architect](https://github.com/p-kothapalli/lsc-delivery-architect);
the package itself has no dependency on it.
