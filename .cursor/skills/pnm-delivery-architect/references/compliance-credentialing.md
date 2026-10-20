# Compliance & Credentialing Reference

Use this when applicability check **A-4** (Compliance & Audit) or **A-9**
(sensitive data) holds. It lists the credentialing elements that an
accreditation programme or regulator *may* require, the product objects that
can hold the evidence, and the section format an artifact uses.

**Scope rule.** Apply only what the target has placed in scope through
discovery dimension D-13 (accreditation programmes, delegation agreements,
state or federal programme rules). Reference points here come from S10, S12
and S14 in `references/pnm-product-baseline.md` §6. Look-back periods, time
limits and thresholds that are not stated in those sources are the target's
to supply — write them as `{per D-13}` and raise a Clarification Question.
Never assert a requirement the target has not placed in scope.

## Contents

1. Verification elements
2. Review, committee and decision
3. Recredentialing
4. Ongoing monitoring
5. Delegation oversight
6. Reporting, notices and appeals
7. Sensitive data (A-9)
8. Compliance & Audit section — artifact format

---

## 1. Verification elements

Reference point: the primary source verification elements in S10.

| Element | Typical primary sources (confirm per D-12) | Product object that can hold the result | Evidence the artifact should name |
|---|---|---|---|
| Licence to practise | State licensing board | BusinessLicense (Status, VerificationStatus, VerifiedDate, PeriodEnd, JurisdictionState) | Source, result, verification date, expiry |
| DEA / CDS registration | Federal and state controlled-substance registries | No dedicated product object verified — `{per D-2}` | Source, registration number, expiry |
| Education and training | Institution, or a body that verifies on its behalf | PersonEducation (EducationLevel, CompletionDate, Status, VerificationStatus, VerifiedDate) | Programme, completion date, verification date |
| Board certification | The certifying board, or an approved display source | BoardCertification (BoardName, Status, CurrentCertificationDate, ExpirationDate) | Board, status, expiry, verification date |
| Work history | The application or curriculum vitae; explanation of gaps | PersonEmployment (StartDate, EndDate, Position, VerificationStatus) | Gaps above the target's threshold and their explanation |
| Malpractice history | The national data bank (S12) or the liability carrier | CareProviderAdverseAction (ActionType Malpractice Judgement), InsurancePolicy (EffectiveDate, ExpirationDate, TotalSumInsured) | Query history or carrier confirmation; coverage period |
| Sanctions | The national data bank (S12), the federal exclusion list (S14), state lists `{per D-13}` | CareProviderAdverseAction (ActionType, RegulatoryBody, Status) | List checked, date, result |

Rules:

- Every in-scope element has a **source, a result and a date** — the three
  things an auditor samples.
- An NPI from the national registry does **not** prove licensure or
  credentialing (S13). Never treat a registry match as a verification.
- A verification organisation's result counts only if the target accepts that
  organisation `{per D-13}`.

## 2. Review, committee and decision

Reference point: credentialing committee review in S10.

- **Quality review** (QC-01) — evidence: reviewer, date, outcome, any return
  reason.
- **Clean vs non-clean routing** (QC-02) — the criteria and who may approve a
  clean file are the target's `{per D-13}`.
- **Medical director review** (QC-03) — reviewer identity and date.
- **Committee** (QC-04) — docket, decision per practitioner (approve, deny,
  defer — use the target's values), meeting date, minutes.
- **Decision date** — participation must not become effective before it when
  D-13 requires that (NW-01, OB-02).

## 3. Recredentialing

Reference point: recredentialing at most every 36 months (S10).

- Re-verify the elements in §1 that the target re-verifies `{per D-13}`.
- Include monitoring findings since the last decision (§4).
- A lapsed cycle may require conversion to initial credentialing (RE-03) — the
  rule is the target's.

## 4. Ongoing monitoring

Reference point: ongoing monitoring of sanctions, complaints and adverse
events (S10).

| Source | Mechanism | Reference |
|---|---|---|
| National data bank | Continuous query: 12-month enrolment, notice within 24 hours of a new, revised, corrected or voided report | S12 |
| Federal exclusion list | Monthly supplement files or online search | S14 |
| Licence and certification expiry | Scheduled check of PeriodEnd, ExpirationDate | S5 |
| Complaints and quality events | The target's complaint process `{per D-12}` | — |

S12 also announces that one-time and continuous query services merge in
December 2026; an artifact that integrates with the data bank raises a
Clarification Question about the post-merger interface.

## 5. Delegation oversight

Reference point: delegation oversight in S10; delegated credentialing service
providers are a health-plan entity type in S12.

Elements an artifact may need: the delegation agreement and its scope,
pre-delegation evaluation, periodic audit, the delegate's reporting
obligations, corrective action, and revocation. Scenario cards DG-01 and
DG-02. The frequency of audits and reports is `{per D-13}`.

## 6. Reporting, notices and appeals

- Health plans must report to the national data bank when appropriate (S12);
  which actions are reportable is `{per D-13}`.
- Denials and adverse decisions may carry notice and appeal or fair-hearing
  rights (QC-05) — process and time limits are `{per D-13}`.

## 7. Sensitive data (A-9)

| Data | Why sensitive | Handling the artifact must state |
|---|---|---|
| Tax ID whose type is SSN | Personal identifier | Field-level security by persona; masking for read-only roles; encryption where licensed (D-10); audit of access |
| Date of birth, home address | PII | Field-level security; exclude from directory and search index |
| Data-bank query results | Confidential by statute; surveyors and auditors may not view them — the query history page is the evidence | Restricted storage; never copied into notes or emails; evidence = query history |
| Malpractice details, adverse actions | Sensitive professional data | Restricted to credentialing and committee personas |
| Uploaded documents | May contain PHI | File sharing limited to the case; retention `{per D-13}` |

## 8. Compliance & Audit section — artifact format

Every artifact for which A-4 applies includes this section after Technical
Implementation:

```
## Compliance & Audit

| Element in scope (D-13) | Where the evidence is recorded | Who can see it | Retention |
|---|---|---|---|
| <element> | <object · field — provenance label> | <personas> | <per D-13> |

**Out of scope:** <elements deliberately not covered, with the reason>
**Sensitive data (A-9):** <fields, FLS, encryption, audit handling — or "none">
**Open compliance questions:** <Clarification Question numbers>
```
