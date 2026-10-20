# Output Templates, Effort Sizing & Save Location (PNM)

The exact format of every artifact. `SKILL.md` STEP 4 links here.

## Contents

1. Story — canonical section order
2. Story template
3. Epic wrapper
4. Solution Plan template (Plan + Prototype mode)
5. Effort sizing
6. Where to save

---

## 1. Story — canonical section order

| # | Section | Required |
|---|---|---|
| 1 | Header | Yes |
| 2 | Org Discovery Context | Yes (A-1) |
| 3 | Story (As a / I want / So that) | Yes |
| 4 | Why it matters | Yes |
| 5 | Scope | When more than one component or provider type |
| 6 | Current State | Refactor, Bug Fix, Migration, Remediation; otherwise when something exists |
| 7 | Acceptance Criteria (Patterns A–G) | Yes |
| 8 | Technical Implementation (high-level) | Yes |
| 9 | Compliance & Audit | When A-4 applies |
| 10 | Definition of Done | Yes |
| 11 | Clarification Questions | When anything is unresolved |
| 12 | Impact Analysis, including Downstream Consumers | Yes for provider-data changes (A-5); otherwise when relevant |
| 13 | Estimated Effort | Yes |

Technical Implementation sits after the ACs so business reviewers can stop at
the end of the AC block.

---

## 2. Story template

```markdown
# USER STORY <N>: <Descriptive title>

**Persona:** <role archetype or adapter-mapped title>
**Priority:** P0 | P1 | P2
**Lifecycle domain(s):** <e.g. Network participation; Provider data maintenance>
**Scenario(s):** <scenario IDs from the library, e.g. NW-01, PD-05>
**Provider types in scope:** <practitioner | group | organisational/ancillary | delegated entity>
**Workflow mode:** <New Feature | Refactor | Bug Fix | Migration | Remediation>
**Build technology:** <rung(s) from the ladder, e.g. "Config + Flow"; OmniStudio runtime if used, as discovered>
**Volume class (A-6):** <single record | tens per day | file-scale (n rows)>
**Relevant requirements:** <IDs or "none found" / "overlap check not run — story index unbound">

---

## Org Discovery Context

<table from org-discovery.md §5>

---

## Story

**As a** <same persona>,
**I want** <capability in business terms>,
**So that** <measurable business outcome>.

**Why it matters:** <1–2 sentences>

---

## Scope

| Lifecycle step | Component | Change | Provider type |
|---|---|---|---|
| <step> | <component> [provenance] | <new / modified> | <type> |

---

## Current State

- **<component or behaviour>** [Discovered — <where>]: <current behaviour>

---

## Acceptance Criteria

> Patterns A–G (ac-pattern-library.md). Business language only inside
> Given/When/Then; every write outcome carries a Pattern E; each validation
> says *blocks* or *warns*.

**AC-1 — <title>**

**Given** …
**When** …
**Then** …

---

## Technical Implementation (high-level)

| Component | Provenance | Type | Change | Drives |
|---|---|---|---|---|
| <API name> | [Product] / [Discovered] / [Adapter] / [Proposed] | <object, field, Flow, OmniScript, Apex, LWC, config, integration> | <one line> | AC-1 |

**Governor / volume strategy (A-6):** <when a write path exists>
**Sensitive data handling (A-9):** <when applicable>

---

## Compliance & Audit

| Requirement element | Source (D-13) | How this story satisfies it | Audit evidence produced |
|---|---|---|---|
| <e.g. primary source verification of licence> | <in-scope standard, as stated by the target> | <behaviour> | <record, history, file, report> |

---

## Definition of Done

- [ ] Happy-path AC verified in the target org
- [ ] Negative / edge ACs verified
- [ ] Every Pattern E field verified by query or record inspection
- [ ] Access applied per Pattern C, if fields or objects changed
- [ ] Automated test coverage meets the target's threshold, including bulk and negative paths, if code changed
- [ ] Downstream consumers verified or notified (A-5)
- [ ] No regression in the components listed in Impact Analysis

---

## Clarification Questions

| # | Question | Impact if answered differently | Owner |
|---|---|---|---|
| 1 | <question — one per [Assumed — confirm] item> | <impact> | <role> |

---

## Impact Analysis

| Component / consumer | Type | Impact | Why |
|---|---|---|---|
| <name> [provenance] | <component / downstream consumer> | HIGH / MEDIUM / LOW | <reason> |

---

## Estimated Effort

| Component | Change type | Effort | Notes |
|---|---|---|---|
| <name> | <type> | S / M / L / XL / XXL | <context> |

**Total:** <sum> — <overall size> · AI-estimated — validate with the team.
```

---

## 3. Epic wrapper

```markdown
# EPIC: <title>

**Scope source:** <document or prompt>
**Lifecycle domains:** <list>
**Stories:** <n> (maximum 10 per epic; split into waves beyond that)

## Org Discovery Context
<shared table; individual stories reference it and add rows only for what differs>

## Decomposition

| # | Story | Persona | Scenarios | Depends on | Size |
|---|---|---|---|---|---|
| 1 | <title> | <role> | <IDs> | — | M |

## Dependency order
<Mermaid flowchart or ordered list>

<stories follow, each using the story template>
```

Present the decomposition for approval **before** writing the stories.

---

## 4. Solution Plan template (Plan + Prototype mode)

Skipped in this mode: Given/When/Then, Pattern E, the Technical Implementation
table and Definition of Done. Retained: persona, Org Discovery Context,
build-technology decision, provenance on every name, no invented names,
Clarification Questions, effort.

```markdown
# Solution Plan — <capability>

**Primary persona:** <role>
**Subjects:** <provider types the work is about>
**Priority:** P0 | P1 | P2
**Lifecycle domain(s):** <list> · **Scenarios:** <IDs>
**Build technology (decision):** <one line>
**Rejected alternative(s):** <one line each, with the reason>
**Volume class:** <class>
**Prototype:** <file name, if produced>
**Mode:** Plan + Prototype (no stories yet) · AI-estimated — validate with the team.

## Ask (verbatim)
> <original prompt>

## Org Discovery Context
<table>

## Goals and non-goals

## Scenario coverage
| Scenario | Covered | Notes / edge cases carried forward |
|---|---|---|

## Current State

## Proposed solution and alternatives
<2–4 sentences of solution shape in business language>

| # | Component | Provenance | Badge | Change | Effort | Why chosen |
|---|---|---|---|---|---|---|
| 1 | <name> | [Product] | OOTB | Config | S | <reason> |

**Badges** — one of: `OOTB`, `Config`, `Flow`, `OS`, `FC`, `IP`, `DM`, `LWC`, `Apex`, `DPE`, `Agentforce`, `Ext`.

## Data, lifecycle and integration impacts
- Records touched (objects only, with provenance)
- Lifecycle effect (discovered status model)
- Downstream consumers (A-5)

## Compliance and security
- A-4 elements in scope · A-9 sensitive data handling

## Delivery slices and dependencies
| Slice | Contents | Depends on |
|---|---|---|

## Risks and open questions
| # | Risk / question | Impact | Owner |
|---|---|---|---|

## Estimated Effort
| Bucket | Size |
|---|---|
| Declarative (product, config, Flow) | |
| OmniStudio | |
| Custom (LWC, Apex) | |
| Data / integration | |
| Testing and migration | |
| **Total** | |

## Next step
Promote to stories? (New Feature or Epic Breakdown mode, reusing this Org Discovery Context.)
```

---

## 5. Effort sizing

| Size | Hours | Points | Description | PNM examples |
|---|---|---|---|---|
| **S** | < 1 | 1 | Configuration, no code | Picklist value, list view, queue, permission set update, directory-display rule |
| **M** | 2–4 | 2 | Single component change | Screen Flow change, OmniScript element, validation rule set, Data Mapper field |
| **L** | 4–8 | 3 | New component or multi-element change | New Screen Flow, work-guide step set, new Data Mapper, record page with dynamic actions |
| **XL** | 1–2 days | 5 | Complex logic or cross-component | Apex service, LWC grid, participation multi-row edit, verification integration |
| **XXL** | 3+ days | 8+ | Multi-component or multi-system | Bulk intake with async processing, roster mapping, migration lane, downstream feed |

Add the test, data-migration and integration burden explicitly; they are
usually the larger share in PNM work.

---

## 6. Where to save

- If the adapter sets `outputs.location`, save there.
- Otherwise ask once per session and reuse the answer.
- File names: `<PascalCaseTitle>_UserStory.md`, `<Capability>_SolutionPlan.md`,
  `<Capability>_Prototype.html`, `<Title>_Epic.md`.
- Validation queries go to `outputs.queryArchive` when configured.
- Never overwrite an unrelated file; ask before appending to an existing one.
