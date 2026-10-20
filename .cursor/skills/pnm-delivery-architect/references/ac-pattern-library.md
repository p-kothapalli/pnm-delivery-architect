# Persona Contract + AC Pattern Library (PNM)

The two non-negotiables of every story: a concrete business persona, and
acceptance criteria in business language using one of the patterns below.

## Contents

- §A Persona contract — role archetypes, adapter mapping, the provider trap
- §B Given / When / Then contract
- Pattern A — Behavioural (default)
- Pattern B — Field / object / metadata definition
- Pattern C — Permission set / field-level security
- Pattern D — Field update rules
- Pattern E — Record & field specification (mandatory on writes)
- Pattern F — Lifecycle transition (optional)
- Pattern G — Routing and ownership (optional)
- Choosing a pattern

All names in examples are **illustrative placeholders**. `<Prefix>` stands for
the discovered or adapter-supplied prefix; nothing here is a default.

---

## §A Persona contract

The persona is the **Salesforce user doing the work**. Providers, groups,
facilities, delegated entities and members are the **subject** of the work.

### Role archetypes

If the adapter maps archetypes to organisation titles (`personas`), use the
organisation's title; otherwise use the archetype.

| Domain | Role archetypes |
|---|---|
| Recruitment | Provider Network Director · Provider Recruitment Specialist |
| Intake | Provider Enrollment Specialist · Provider Intake Specialist |
| Credentialing | Credentialing Specialist · Primary Source Verification Specialist · Organisational Provider Credentialing Specialist · Delegated Credentialing Analyst |
| Review & decision | Credentialing Quality Reviewer · Medical Director · Credentialing Committee Coordinator |
| Network | Network Configuration Specialist · Network Management Specialist |
| Contracting | Contracting Specialist · Contracting Manager · Reimbursement Analyst |
| Onboarding | Provider Relations Specialist |
| Data maintenance | Provider Data Specialist · Provider Data Steward |
| Roster | Roster Analyst |
| Service | Provider Services Representative · Claims Research Analyst (read-only) |
| Platform | PNM Administrator · Integration Engineer · Data Migration Lead |
| Portal only | Provider · Practice Office Manager · Delegated Entity Administrator |

**Banned:** "user", "business user", "system", "developer", an unqualified
"admin", and "provider" (or "practitioner", "group", "facility") as the
persona of an internal feature.

### The provider trap

| Don't write | Write instead |
|---|---|
| "As a provider, I want my address updated" (internal change) | "As a **Provider Data Specialist**, I want to update a practitioner's practice address…" |
| "As a user, I want to see expiring licences" | "As a **Credentialing Specialist**, I want…" |
| "As the system, I want to create participation rows" | Name the role whose action causes it; describe automation in Technical Implementation |
| "As an admin, I want a new field" | "As a **PNM Administrator**…" — or keep the business persona and put the field in Pattern B |

"As a **Provider**" or "As a **Practice Office Manager**" is correct only for a
genuine portal experience the provider's staff log into.

---

## §B Given / When / Then contract

```
**AC-N — Short business-language title**

**Given** <persona + business state>
**When** <one business action>
**Then** <observable, checkable outcome>
**And** <optional additional outcome, one per line>
```

- One **When** per AC; two actions → two ACs.
- The **Then** is observable — QA can see, query or read it. "It works" is not
  a Then.
- Compound outcomes use **And** lines.
- Edge cases get their own AC.
- More than ~6 lines under one Then → split the AC.
- **Validation severity (A-7):** every validation outcome says whether it
  *blocks* the action or only *warns*.
- **No** API names, `*__c` names, class names, step numbers, SOQL or picklist
  API values in any Given/When/Then/And line, and **no provenance labels** —
  those belong in Technical Implementation and Pattern E.

**Wrong:**

> When Save fires, `<Prefix>_ParticipationService` inserts a participation row
> with the active flag set and the network lookup populated.

**Right:**

```
**AC-1 — Practitioner joins a base network from a future date**

**Given** a Network Configuration Specialist is working a credentialed practitioner at an approved practice location,
**When** they add the practitioner to a base network with an effective date next month,
**Then** the practitioner's participation in that network is recorded for that location from that date,
**And** the participation does not appear in the provider directory before that date.
```

---

## Pattern A — Behavioural (default)

Use for any behaviour the persona can observe: records change, a message is
shown, work is routed, a document is generated. Format as §B.

**Negative example:**

```
**AC-2 — Duplicate NPI blocks the application**

**Given** a Provider Intake Specialist is entering a new practitioner application,
**When** they enter an NPI already held by an active practitioner,
**Then** the application cannot be submitted (blocks),
**And** the specialist sees the existing practitioner with a link to open the record.
```

---

## Pattern B — Field / object / metadata definition

Use when a field, object, metadata type, record type or picklist value is
**defined** or changed. Bullets, not GWT.

```
**AC-N — Create the following field on <Object label>**

- **API Name:** <Prefix>_<FieldName>__c        [Proposed]
- **Object:** <object label / API name>        [Product | Discovered]
- **Type:** Checkbox | Text(80) | Date | Lookup(<Target>) | Picklist | …
- **Label:** <user-facing label>
- **Values (picklist only):** <values — discovered or proposed, never borrowed>
- **Default:** <optional>
- **Help text:** <optional>
- **Track History:** true | false
- **Required:** true | false
- **Sensitive data (A-9):** <none | classification + encryption/FLS note>
```

For a new object add plural label, sharing model, name format, and its fields
in the same bullet style.

---

## Pattern C — Permission set / field-level security

```
**AC-N — Access**

- **<permission set — discovered or proposed>:**
  - Object: Read, Create, Edit
  - Fields: Read and Edit on <fields>
- **<read-only permission set>:**
  - Object: Read
  - Fields: Read on <fields>
```

Persona-based access sets are preferred (scenario PL-04). For sensitive fields
(A-9) state which personas may see the value and how it is masked for the rest.

---

## Pattern D — Field update rules

Use when one value depends on several conditions.

```
**Given** <precondition>,
**When** <action>,
**Then** the following are set per the rules below:

- **Directory display =**
  - When the location is the practitioner's primary location AND participation is active → shown
  - When participation is future-dated → hidden until the effective date
  - Else → hidden
```

Rule values use discovered or product values only.

---

## Pattern E — Record & field specification (mandatory on writes)

Whenever a Save, Submit, batch run, integration load or automation **creates or
updates records**, pair the Pattern A AC with one table per object, parents
before children, listing **every field written**.

```
**AC-N — Records written when <trigger> (branch: <branch>)**

**Given** <which branch this recipe applies to>,
**When** <the single trigger>,
**Then** the following records are written exactly as specified:

**Practitioner location — Create**   [Product: HealthcarePractitionerFacility]

| Field | Value | Provenance | Notes |
|---|---|---|---|
| Provider | {Selected practitioner} | [Product] | lookup |
| Facility | {Selected location} | [Product] | lookup |
| Effective From | {Entered effective date} | [Product] | A-2 |
| Effective To | blank | [Product] | open-ended |
| Active | false until Effective From, then true | [Product] | A-3 — rule, not a stored default |
| Primary Facility | {Primary? answer} | [Product] | |
| Directory Print | {Directory? answer} | [Product] | |

**Network participation — Create**   [Product: HealthcareFacilityNetwork]

| Field | Value | Provenance | Notes |
|---|---|---|---|
| … every field written … | | | |
```

Rules:

- **Every field** — never "etc." or "other fields as needed".
- One table per object, in write order.
- **Value** is a literal, a `{source}` placeholder, or a short formula; nest
  Pattern D rules for multi-branch values.
- Use business labels in the Field column; the object header and the
  Provenance column carry the API identity.
- **A-2:** state effective-from/to values or the rule that sets them whenever
  the object supports effective dating.
- **A-3:** state the status written whenever the discovered status model
  governs the record — discovered values only; if unknown, write
  `{status per D-5}` and raise a Clarification Question.
- A different recipe per branch → a separate Pattern E AC per branch.
- An audit note, task, case comment or file is a record write — spec it too.

---

## Pattern F — Lifecycle transition (optional)

Use when the outcome is a **status change across several records** (activate,
suspend, terminate, reinstate). Pair with a Pattern A AC.

```
**AC-N — Lifecycle on <event>**

| Record | Before | After | Effective-date rule |
|---|---|---|---|
| Practitioner location | {active value per D-5} | {terminated value per D-5} | Effective To = {termination date}; future-dated terminations stay active until then |
| Network participation (each, for that location) | … | … | … |
| Practitioner (anchor) | unchanged unless it was the last active location | … | … |
```

Use only discovered status values. If two status mechanisms exist (Org
Discovery §6), list both columns and raise the conflict.

---

## Pattern G — Routing and ownership (optional)

Use when work moves between queues, stages or owners. Pair with a Pattern A AC.

```
**AC-N — Routing on <event>**

| Trigger | From (stage / owner) | To (stage / owner) | Rule |
|---|---|---|---|
| Quality review returns the file for correction | {review stage per D-6} | {originating reviewer, if configured per D-6} | If the originating reviewer is inactive → their queue |
```

Use only the discovered work model; never assume a stage sequence.

---

## Choosing a pattern

| What the AC asserts | Pattern |
|---|---|
| Behaviour the persona observes | A |
| A field, object, metadata type or picklist being defined | B |
| Access, sharing or field-level security | C |
| A value computed from several conditions | D |
| The exact records and fields written by an action | E (always with an A) |
| Several records changing status together | F (with an A) |
| Work moving between queues, stages or owners | G (with an A) |
