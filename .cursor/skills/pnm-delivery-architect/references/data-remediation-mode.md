# Data Remediation Mode

Use in **Data Remediation** mode ("plan a fix for practice locations missing
NPI", "backfill effective dates", "correct participation after a bad load").
Scenario card PL-07 applies.

**The skill plans; it never executes changes.** It does not run updates,
deletes or anonymous code against any org, even when a capability to do so
is bound. Read-only queries for discovery are allowed when the adapter binds
an org-query capability.

## Contents

1. Output structure
2. Root cause
3. Bounded selection
4. Dry run
5. Fix steps and volume
6. Validation queries
7. Partial failure and rollback
8. Prevention
9. Remediation story

---

## 1. Output structure

```
# Remediation Plan — <symptom in business words>

## Org Discovery Context            (component-scoped; A-1)
## Symptom and impact               (who sees what; downstream consumers — A-5)
## Root cause                       (with evidence)
## Bounded selection                (criteria and counts)
## Dry run
## Fix steps                        (ordered; volume strategy — A-6)
## Validation queries               (before and after)
## Partial-failure handling
## Rollback
## Prevention fix
## Remediation story                (Pattern A + Pattern E)
## Clarification Questions
## Estimated Effort
```

## 2. Root cause

State what produced the bad data — a load, an automation path, a missing
validation, a user process — and the evidence (records, history, logs,
component behaviour). If the cause is a component, run component-scoped
discovery on it (D-9). "Unknown" is acceptable only with a Clarification
Question and an investigation step.

## 3. Bounded selection

Describe the exact selection criteria in business terms and, where an
org-query capability is bound, the counts by meaningful slice (provider type,
network, created date, source). Exclude records that look affected but are
correct, and say why. Never propose "update all".

## 4. Dry run

Produce the would-be change set (record, field, old value, new value) for
review before any change. The business owner signs off the dry run.

## 5. Fix steps and volume

Ordered steps, parents before children. State the volume class (A-6); above
single-transaction volume use bulk tooling or batch processing. State how
automation is handled during the fix and how its side effects are reproduced
if bypassed. Every write is idempotent so a re-run is safe.

## 6. Validation queries

Describe each query by intent, object, filter and expected result — for
example "count of practitioner-location rows that are active and have no
NPI: before = the selection count, after = 0". When the adapter configures a
query archive, offer to save the concrete queries there (post-generation
offer 9).

## 7. Partial failure and rollback

Capture failures per record with the reason; define how failed records are
retried. Before the fix, export the affected fields so they can be restored;
state the rollback trigger and who decides.

## 8. Prevention

The change that stops recurrence — a validation (A-7: blocks or warns), a fix
to the automation, a load rule, or a process change — written as its own
story if non-trivial.

## 9. Remediation story

A story with Pattern A for the corrected outcome and Pattern E for the
records corrected (every field written, with A-2/A-3 where they apply), plus
Downstream Impact (A-5) because consumers may need a re-send.
