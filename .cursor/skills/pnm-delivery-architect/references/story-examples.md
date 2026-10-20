# Story Examples (PNM)

Worked examples of the delivery contract. **Every name, value and finding in
this file is illustrative.** Discovery findings shown here describe a
fictional target; never copy them into an artifact for a real one (Org
Discovery §5). `XYZ_` is a deliberately arbitrary prefix; `<Prefix>` stands
for whatever the target's discovered convention is.

## Contents

1. Example 1 — product-anchored org: add a practitioner to networks at a location (Patterns A, D, E)
2. Example 2 — custom-anchored org: terminate a practice location (Patterns A, E, F, G, Compliance & Audit)
3. Pattern gallery — B, C and G in isolation
4. Solution Plan excerpt — Plan + Prototype mode
5. Bad → good rewrites

---

## 1. Example 1 — product-anchored org

```markdown
# USER STORY 1: Add a practitioner to base and child networks at an approved location

**Persona:** Network Configuration Specialist
**Priority:** P1
**Lifecycle domain(s):** Network participation
**Scenario(s):** NW-01, NW-02, NW-08
**Provider types in scope:** practitioner
**Workflow mode:** New Feature
**Build technology:** Config + LWC (participation grid) + Apex (bulk write)
**Volume class (A-6):** tens per day; up to 40 rows per save
**Relevant requirements:** none found

---

## Org Discovery Context

**Archetype:** Product-anchored
**Discovery depth:** Full · **Capabilities used:** org query, source search

| # | Dimension | Finding | Provenance | Evidence |
|---|---|---|---|---|
| D-1 | Provider anchor | HealthcareProvider, one per practitioner | [Discovered] | object describe; 18,400 records |
| D-3 | Location model | HealthcarePractitionerFacility per practitioner and practice site | [Discovered] | object describe |
| D-4 | Participation model | HealthcareFacilityNetwork per practitioner-location-network; child networks via the payer network's parent | [Discovered] | object describe; payer network records |
| D-5 | Status & temporal model | IsActive + EffectiveFrom / EffectiveTo; a scheduled job activates future-dated rows | [Discovered] | scheduled job inventory |
| D-8 | Naming & conventions | Prefix `XYZ_` | [Discovered] | custom metadata inventory |
| D-10 | Licences & features | PNM add-on enabled | [Discovered] | permission set licences |
| D-11 | Volumes | 30–60 participation saves per day; peak 40 rows per save | [Discovered] | record counts; user statement |
| D-12 | Integrations & consumers | Provider directory and claims read participation nightly | [Assumed — confirm] | Clarification Q1 |

---

## Story

**As a** Network Configuration Specialist,
**I want** to add a credentialed practitioner to a base network and its child networks at an approved location in one action,
**So that** participation is complete and correct before the effective date and the directory and claims see it on time.

**Why it matters:** Adding networks one row at a time leaves child networks missing, which surfaces later as claim denials and directory gaps.

---

## Acceptance Criteria

**AC-1 — Practitioner joins a base network and its child networks from a future date**

**Given** a Network Configuration Specialist is working a credentialed practitioner at an approved practice location,
**When** they add the practitioner to a base network with an effective date next month,
**Then** participation is recorded for that location in the base network and in each of its child networks from that date,
**And** none of the new participation is shown in the provider directory before that date.

**AC-2 — Overlapping participation is blocked**

**Given** the practitioner already participates in a network at that location for an overlapping period,
**When** the specialist adds the same network and location again,
**Then** the save is blocked (blocks),
**And** the specialist sees the existing participation and its dates.

**AC-3 — Participation outside the location's active period warns**

**Given** the practitioner's time at the location ends before the requested participation would end,
**When** the specialist saves the participation,
**Then** the save completes with a warning (warns) that participation ends with the location,
**And** the participation end date is set to the location's end date.

**AC-4 — Directory display rule**

**Given** a participation row is being written,
**When** the specialist saves,
**Then** the directory display value is set per the rules below:

- **Directory display =**
  - When the location is the practitioner's primary location AND the participation is in effect today → shown
  - When the participation starts in the future → hidden until the effective date
  - Else → hidden

**AC-5 — Records written when participation is saved (branch: base network with child networks)**

**Given** the specialist selected one base network that has child networks,
**When** they save,
**Then** the following records are written exactly as specified:

**Network participation (base) — Create**   [Product: HealthcareFacilityNetwork]

| Field | Value | Provenance | Notes |
|---|---|---|---|
| Payer Network | {Selected base network} | [Product] | lookup |
| Practitioner Facility | {Selected practitioner location} | [Product] | lookup |
| Healthcare Facility | {Location of the practitioner facility} | [Product] | lookup, copied from the practitioner facility |
| Healthcare Provider | {Selected practitioner} | [Product] | lookup |
| Account | {Practitioner's account} | [Product] | lookup |
| Effective From | {Entered effective date} | [Product] | A-2 |
| Effective To | {Earlier of the entered end date and the location's Effective To}; blank when both are blank | [Product] | A-2, AC-3 |
| Active | false until Effective From, then true | [Product] | A-3 — set by the scheduled activation job |
| Panel Status | {Entered panel status} | [Product] | discovered values only |
| Panel Limit | {Entered panel limit}; blank when not entered | [Product] | |
| Directory Display | per AC-4 | [Proposed] | `XYZ_DirectoryDisplay__c` |

**Network participation (child) — Create, one per child network**   [Product: HealthcareFacilityNetwork]

| Field | Value | Provenance | Notes |
|---|---|---|---|
| Payer Network | {Child network} | [Product] | one row per child of the base network |
| Practitioner Facility | same as base row | [Product] | |
| Healthcare Facility | same as base row | [Product] | |
| Healthcare Provider | same as base row | [Product] | |
| Account | same as base row | [Product] | |
| Effective From | same as base row | [Product] | A-2 |
| Effective To | same as base row | [Product] | A-2 |
| Active | same rule as base row | [Product] | A-3 |
| Panel Status | same as base row | [Product] | |
| Panel Limit | same as base row | [Product] | |
| Directory Display | per AC-4 | [Proposed] | |

---

## Technical Implementation (high-level)

| Component | Provenance | Type | Change | Drives |
|---|---|---|---|---|
| HealthcareFacilityNetwork | [Product] | object | written | AC-1, AC-5 |
| HealthcarePayerNetwork (parent/child) | [Product] | object | read to expand child networks | AC-1 |
| `XYZ_DirectoryDisplay__c` on HealthcareFacilityNetwork | [Proposed] | field | new | AC-4 |
| `xyzParticipationGrid` | [Proposed] | LWC | multi-row entry on the practitioner record page | AC-1 |
| `XYZ_ParticipationService` | [Proposed] | Apex | bulk insert; overlap check; end-date clamp | AC-2, AC-3, AC-5 |
| Overlap validation | [Proposed] | Apex | blocks; one query per save | AC-2 |
| Scheduled activation job | [Discovered] | scheduled job | unchanged; flips Active on Effective From | AC-1 |

**Governor / volume strategy (A-6):** one query for existing participation and one bulk insert per save; 40 rows is well within one transaction.

---

## Definition of Done

- [ ] Happy-path AC verified in the target org
- [ ] Negative / edge ACs verified
- [ ] Every Pattern E field verified by query or record inspection
- [ ] Access applied per Pattern C
- [ ] Automated test coverage meets the target's threshold, including bulk and negative paths
- [ ] Downstream consumers verified or notified (A-5)
- [ ] No regression in the components listed in Impact Analysis

---

## Clarification Questions

| # | Question | Impact if answered differently | Owner |
|---|---|---|---|
| 1 | Do the directory and claims feeds read participation nightly, and do they honour future-dated rows? | A feed that ignores dates would expose future participation early | Integration Engineer |

---

## Impact Analysis

| Component / consumer | Type | Impact | Why |
|---|---|---|---|
| Provider directory feed [Assumed — confirm] | downstream consumer | HIGH | New field drives display |
| Claims participation feed [Assumed — confirm] | downstream consumer | MEDIUM | New rows per child network |
| Scheduled activation job [Discovered] | component | LOW | Unchanged; more rows to process |

---

## Estimated Effort

| Component | Change type | Effort | Notes |
|---|---|---|---|
| Directory display field + access | Config | S | |
| Participation grid | LWC | XL | multi-row entry, child expansion preview |
| Participation service + overlap rule | Apex | XL | bulk, negative and boundary tests |
| Testing (bulk, negative, feeds) | Test | L | |

**Total:** ~4–5 days — XXL · AI-estimated — validate with the team.
```

---

## 2. Example 2 — custom-anchored org: terminate a practice location

Only the sections that differ from Example 1 are shown.

```markdown
# USER STORY 2: Terminate a practitioner's practice location and its participation

**Persona:** Provider Data Specialist
**Lifecycle domain(s):** Provider data maintenance; Network participation; Termination
**Scenario(s):** PD-05, TR-01
**Workflow mode:** New Feature
**Build technology:** Flow (single provider) — Apex rejected at this volume
**Volume class (A-6):** single record; up to 15 participation rows per location

## Org Discovery Context

**Archetype:** Custom-anchored
**Discovery depth:** Full · **Capabilities used:** source search; user answers

| # | Dimension | Finding | Provenance | Evidence |
|---|---|---|---|---|
| D-1 | Provider anchor | Person account with `XYZ_ProviderType__c` | [Discovered] | source metadata |
| D-3 | Location model | `XYZ_PracticeLocation__c` child of the provider account | [Discovered] | source metadata |
| D-4 | Participation model | `XYZ_Participation__c` per location and network | [Discovered] | source metadata |
| D-5 | Status & temporal model | Picklist `XYZ_Status__c` with Active, Pending Termination, Terminated; plus an end date | [Discovered] | picklist values |
| D-6 | Work model | Termination case per request; returns go to the originating specialist's queue | [Discovered] | queues; case record types |
| D-13 | Compliance scope | Termination notice to members and the state program within the target's stated window | [Adapter] | adapter pre-answer |

## Acceptance Criteria

**AC-1 — Location terminated from a future date**

**Given** a Provider Data Specialist is working a termination request for one of a practitioner's practice locations,
**When** they terminate the location with a termination date at the end of next month,
**Then** the location and every participation at that location stay in effect until that date and end on it,
**And** the practitioner's other locations and their participation are unchanged.

**AC-2 — Last active location cannot be terminated without confirming the practitioner's end**

**Given** the location is the practitioner's only active location,
**When** the specialist submits the termination,
**Then** the submission is blocked (blocks) until the specialist confirms whether the practitioner is leaving the network entirely.

**AC-3 — Lifecycle on termination**

| Record | Before | After | Effective-date rule |
|---|---|---|---|
| Practice location | Active | Pending Termination, then Terminated on the termination date | End date = {termination date} |
| Participation (each, at that location) | Active | Pending Termination, then Terminated on the termination date | End date = {termination date}, unless an earlier end date exists |
| Provider account (anchor) | unchanged | unchanged | Only changes through AC-2's confirmation |

**AC-4 — Records written when the termination is submitted**

**Given** the location is not the practitioner's last active location,
**When** the specialist submits,
**Then** the following records are written exactly as specified:

**Practice location — Update**   [Discovered: `XYZ_PracticeLocation__c`]

| Field | Value | Provenance | Notes |
|---|---|---|---|
| Status | Pending Termination | [Discovered] | A-3; becomes Terminated on the date |
| End Date | {Termination date} | [Discovered] | A-2 |
| Termination Reason | {Selected reason} | [Discovered] | discovered values only |

**Participation — Update, each at that location**   [Discovered: `XYZ_Participation__c`]

| Field | Value | Provenance | Notes |
|---|---|---|---|
| Status | Pending Termination | [Discovered] | A-3 |
| End Date | {Earlier of the existing end date and the termination date} | [Discovered] | A-2 |

**Termination case — Update**   [Discovered: Case, termination record type]

| Field | Value | Provenance | Notes |
|---|---|---|---|
| Status | {submitted value per D-6} | [Discovered] | |
| Notice Due Date | {Termination date minus the notice window per D-13} | [Adapter] | Compliance |

**AC-5 — Routing on return for correction**

| Trigger | From (stage / owner) | To (stage / owner) | Rule |
|---|---|---|---|
| Quality review returns the termination | Quality review queue | Originating specialist | If the specialist is inactive → their queue |

## Compliance & Audit

| Requirement element | Source (D-13) | How this story satisfies it | Audit evidence produced |
|---|---|---|---|
| Member and state-program notice of termination | The target's stated program rule | Notice due date computed and shown on the case | Case field history; notice task |
| Termination reason recorded | The target's stated policy | Reason required at submit | Location field history |
```

---

## 3. Pattern gallery — B, C and G in isolation

**Pattern B — new field**

```markdown
**AC-6 — Create the following field on Network participation**

- **API Name:** <Prefix>_DirectoryDisplay__c        [Proposed]
- **Object:** HealthcareFacilityNetwork        [Product]
- **Type:** Checkbox
- **Label:** Show in Directory
- **Default:** false
- **Help text:** Set automatically from the primary-location and effective-date rule.
- **Track History:** true
- **Required:** false
- **Sensitive data (A-9):** none
```

**Pattern C — access with a sensitive field**

```markdown
**AC-7 — Access**

- **Provider Data Specialist access set** [Proposed]:
  - Object: Read, Edit on the provider anchor
  - Fields: Read and Edit on tax ID; Read on date of birth
- **Provider Services Representative access set** [Proposed]:
  - Object: Read
  - Fields: tax ID shown masked except the last four digits; date of birth hidden
```

**Pattern G — routing between credentialing stages**

```markdown
**AC-8 — Routing on verification complete**

| Trigger | From (stage / owner) | To (stage / owner) | Rule |
|---|---|---|---|
| All verification elements complete and clean | {verification stage per D-6} | {quality review stage per D-6} | Clean files skip committee if the target's policy allows (D-13) |
| Any element non-clean | {verification stage per D-6} | {committee preparation per D-6} | Medical director review first |
```

---

## 4. Solution Plan excerpt — Plan + Prototype mode

```markdown
# Solution Plan — Roster intake for delegated groups

**Primary persona:** Roster Analyst
**Subjects:** delegated groups and their practitioners
**Build technology (decision):** OOTB Roster File Mapping + DPE load + Config review queue
**Rejected alternative(s):** record-by-record Flow — file-scale volume (volume rule)
**Volume class:** file-scale (2,000–20,000 rows per file)
**Prototype:** RosterIntake_Prototype.html

## Proposed solution and alternatives

| # | Component | Provenance | Badge | Change | Effort | Why chosen |
|---|---|---|---|---|---|---|
| 1 | Roster File Mapping | [Product] | OOTB | Config | M | Shipped mapping and staging |
| 2 | Roster load definition | [Product] | DPE | Config | L | Bulk load at file scale |
| 3 | Exception review queue | [Proposed] | Config | New | S | Rows failing validation |
| 4 | Upload portal page | [Product] | OOTB | Config | M | Delegated entities upload directly |
```

---

## 5. Bad → good rewrites

| Don't write | Write instead | Rule |
|---|---|---|
| "As a provider, I want my address updated" | "As a Provider Data Specialist, I want to update a practitioner's practice address…" | Persona trap |
| "When Save fires, the participation service inserts rows" | "When they save the participation, …" | No class names in Given/When/Then |
| "Then the record is created with the status set" | "Then participation is recorded from the effective date" + a Pattern E table | Observable Then; Pattern E on writes |
| "Status = Active" (no discovery) | "Status = {status per D-5}" + Clarification Question | Discovered values only |
| "Other fields as needed" | Every field, one row each | Pattern E completeness |
| "Then an error appears" | "Then the save is blocked (blocks), and the specialist sees…" | A-7 severity |
| "Query the participation object for active rows" in an AC | Describe the check in Definition of Done; keep queries out of ACs | Business language |
