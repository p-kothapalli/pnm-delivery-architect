# Legacy → PNM Migration Playbook

Use in **Legacy → PNM Migration** mode. Output is a Solution Plan first, then
stories per lane. Scenario cards PL-01…PL-08 and the integrations reference
(`references/integrations.md`) apply. Downstream impact (A-5) is mandatory.

## Contents

1. Discovery for migration
2. Solution Plan sections
3. Identifier strategy
4. Mapping by anchor
5. Load lanes and order
6. Cleansing and standardisation
7. Bridges for legacy consumers
8. Parity, shadow run and cutover
9. Rollback
10. Change management
11. Stories that come out of the plan

---

## 1. Discovery for migration

Run full Org Discovery on the **target** (D-1…D-13) and an equivalent
inventory of the **source**: entities, keys, volumes per entity, history
depth, code sets, and every consumer of the source (D-12). Unknown consumers
are the most common cause of a failed cutover — ask for them explicitly.

## 2. Solution Plan sections

Use the Solution Plan template in `references/output-template.md`, with these
additions under *Proposed solution*: identifier strategy · mapping summary per
anchor · lanes and order · cleansing rules · bridges · parity and shadow
approach · cutover runbook outline · rollback · change management.

## 3. Identifier strategy (PL-01)

- One unique provider key replacing composite legacy keys; state its format
  source `[Proposed]` or `[Discovered]`.
- Carry the legacy key on every migrated record (SourceSystem and
  SourceSystemIdentifier on product objects, or the target's external ID) so
  loads are idempotent and consumers can cross-reference.
- Decide how legacy duplicates merge into one key, and who signs off merges.

## 4. Mapping by anchor (D-1…D-4)

Map source entities to the target's **discovered** anchor, identifier,
location and participation models — not to a default. For each mapping row:
source entity and field · target object and field with provenance label ·
transformation · effective-date rule (A-2) · status rule (A-3) · owner.
Fields on objects marked *Not verified* in the object catalog stay
`[Assumed — confirm]` until checked.

## 5. Load lanes and order (PL-02)

Each lane runs **mapping → mapping validation → test load → full stage load →
production load**, with business sign-off at each step. Load parents before
children. A product-anchored order, adapted to the discovered model:

1. Reference data — specialties, taxonomies, code sets, payer networks and their hierarchy
2. Organisations and people — Account, Contact
3. Provider anchor records
4. Identifiers — NPI and tax-ID history
5. Locations, then practitioner-location rows
6. Specialty and taxonomy assignments
7. Credentials — licences, certifications, education, employment, coverage, adverse actions
8. Network participation and tiers
9. Contracts, payment agreements, fee schedules
10. In-flight work — applications, cases, files

**Volume.** Use bulk loading; state how automation (triggers, flows,
duplicate rules) is handled during loads and how skipped side effects are
reproduced afterwards. Size storage before the full stage load — provider data
with history can approach purchased storage.

## 6. Cleansing and standardisation

Addresses to postal standards (IN-05) · NPI checked against the national
registry (S13) · tax ID and type validated · taxonomy and specialty codes
mapped to the target's reference lists · effective dates normalised (no open
overlaps) · status values mapped to the discovered model.

## 7. Bridges for legacy consumers (PL-03)

List every consumer from D-12 and, for each, whether it moves to the new
model at cutover or is fed through a bridge that reshapes new data into the
old form. Each bridge has an owner and a retirement condition.

## 8. Parity, shadow run and cutover

- **Record parity:** counts and field-by-field comparison per lane, sampled
  and full.
- **Process parity:** run the same business transactions in both systems for
  an agreed period and compare outcomes.
- **Cutover runbook:** freeze window, final delta load, validation queries,
  go/no-go criteria, communication.

## 9. Rollback

State the point of no return, what is restored, how deltas captured after
cutover are replayed to the legacy system if rollback happens, and who
decides.

## 10. Change management (PL-08)

Champions per affected team · learning material for UAT and production ·
UAT, integration and production-checkout entry and exit criteria · shadowing
and reverse shadowing for deployments and incident response · user
provisioning by persona (PL-04) · licence-tier decisions (PL-05).

## 11. Stories that come out of the plan

One story per lane, per bridge and per parity check, in dependency order; use
Epic Breakdown rules (at most ten per epic). Each load story carries Pattern E
for the records written and A-5 for consumers.
