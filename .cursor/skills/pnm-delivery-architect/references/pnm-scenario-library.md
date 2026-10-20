# PNM Scenario Library (Layer 2)

Generalised PNM scenarios across the provider lifecycle. Use them in STEP 1 to
select scope, carry edge cases into acceptance criteria, and decide which Org
Discovery dimensions must be resolved.

Every scenario has a card with exact evidence:

- **Core domains** (deep cards with a Pattern E seed): Intake & application,
  Credentialing, Network participation, Provider data maintenance,
  Recredentialing & ongoing monitoring, Roster & bulk intake —
  `references/scenario-cards-core.md`.
- **Other domains** (compact cards): `references/scenario-cards-extended.md`.

Read the index first, then load only the cards for the domains in scope. A
card is a starting point for discovery and acceptance criteria — never a
design.

## Rules

1. A scenario states **what the business needs and which options exist**. It
   never states "the" status values, stage names, record types, batch designs
   or downstream systems. Where those matter it names the discovery dimension
   (D-1…D-13, `references/org-discovery.md`).
2. Product objects named here are `[Product]` candidates, not a decision. The
   target's anchor (D-1), location model (D-3) and participation model (D-4)
   decide which objects are actually written.
3. "Volume rule" means the rule in `references/build-technology-guide.md` §2.

**Basis codes:** **P** = product documentation · **R** = accreditation or
regulatory standard · **F** = field pattern observed in at least one
implementation and generalised. Basis codes never name an organisation.

## Evidence codes

| Code | Meaning |
|---|---|
| S1–S14 | Official sources in the register, `references/pnm-product-baseline.md` §6 |
| CS-1 | Field pattern from a public payer case study (replacement of a legacy provider mainframe: guided build, network hierarchy, data-domain queues, licence strategy, migration practice) |
| CS-2 | Field pattern from private implementation research (a heavily customised PNM: staged credentialing, review loops, bulk intake, activation, termination variants) |

CS codes say a pattern **exists in the field**. They never supply names,
status values, stage models or defaults; the mapping from code to source is
held outside this package. A card with Basis **F** carries at least one CS
code; a card with Basis **P** or **R** carries at least one S code.

## Card format

```
### <ID> · <Name>
**Business need:** …
**Personas:** <role archetypes>
**Product objects that may be involved:** …   [Product]
**Design options:** product-first, then alternatives (ladder rungs)
**Discovery dimensions that change the design:** D-…
**Records typically written:** Pattern E seed using product objects or <discovered> placeholders
**Edge cases:** …
**Compliance hooks:** … (A-4, only when in the target's scope)
**Basis:** P | R | F
**Evidence:** <source IDs from pnm-product-baseline.md §6, regulatory clause/page, or field-pattern code>
```

---

## 1. Recruitment & network development

| ID | Scenario | Product objects / capabilities | Basis |
|---|---|---|---|
| RC-01 | Network adequacy analysis (access within N miles by specialty and region; gap forecast) | CRM Analytics over provider, location and participation data | P |
| RC-02 | Inbound provider registration from a public portal into a lead | Shipped recruitment OmniScript, Experience Cloud, reCAPTCHA, Lead | P |
| RC-03 | Lead segmentation and skill-based assignment by geography, type, specialty | Assignment rules, Omni-Channel | P |
| RC-04 | Recruitment campaigns and journeys | Campaigns, marketing journeys | P |
| RC-05 | Lead review, missing-information outreach, conversion to provider records and portal user | Lead conversion | P |

## 2. Intake & application

| ID | Scenario | Product objects / capabilities | Basis |
|---|---|---|---|
| IN-01 | Portal application with CAQH pre-fill, attestation and e-signature | IndividualApplication, ApplicationCase, CAQH integration, e-signature | P, F |
| IN-02 | Staff-entered participation request covering a practitioner, a group and their locations | Application/case record, provider anchor (D-1), locations (D-3), identifiers, credentials | F |
| IN-03 | Guided provider build: type and specialty → identity and tax ID → demographics → reason codes → networks → child networks → tier → affiliations → billing address → service location with hours and telehealth | Provider anchor, specialty, identifiers, participation (D-4), OperatingHours/TimeSlot | F |
| IN-04 | Detect and reuse existing, terminated or previously denied provider records at intake | Duplicate rules, NPI/tax-ID matching | F |
| IN-05 | Address standardisation and overlap detection at entry | Address-verification service, location model (D-3) | F |
| IN-06 | Validation severity matrix — which rules block and which only warn | Validation rules, guided-UI messaging | F |
| IN-07 | Bulk file intake of practitioners with rule validation, NPPES lookup and a fallout report | Bulk processing (volume rule), staging, error capture | F |
| IN-08 | Application withdrawal, closure and denial | Application/case status (D-5) | F, R |

## 3. Credentialing (initial)

| ID | Scenario | Product objects / capabilities | Basis |
|---|---|---|---|
| CR-01 | Route applications by provider attributes; balance workload; decide ownership on returns (D-6) | Case, queues, Omni-Channel | P, F |
| CR-02 | Combined application review and verification in one working session | Case, verification UI | F |
| CR-03 | Primary source verification: licence, DEA/CDS, education and training, board certification, work history, malpractice history, sanctions | BusinessLicense, BoardCertification, PersonEducation, PersonEmployment, CareProviderAdverseAction, InsurancePolicy | R, P |
| CR-04 | Hybrid verification — specialist first, then a verification organisation's API with real-time status | Work guide, Named Credential, external verification organisation | P |
| CR-05 | NPDB query and continuous query; adverse-action capture | CareProviderAdverseAction or a discovered equivalent | F, R |
| CR-06 | Service-area verification for practice locations | Location model (D-3) | F |
| CR-07 | Specialty credentialing programs (e.g. behavioural-health plus medical dual credentialing; program-specific indicators) | Specialty, program attributes (discovered) | F |
| CR-08 | Document capture and review, including size and type limits | ContentDocumentLink, CaseRelatedFile | P, F |

## 4. Quality review, committee & decision

| ID | Scenario | Product objects / capabilities | Basis |
|---|---|---|---|
| QC-01 | Quality review with outcomes "complete" or "needs correction", and return to the originating reviewer when configured | Case, verification status, work model (D-6) | F |
| QC-02 | Clean-file vs non-clean-file routing | Decision rules, case routing | R, F |
| QC-03 | Medical director review | Case, review outcome | R, F |
| QC-04 | Credentialing committee docket, decisions (approve / deny / defer), committee minutes and reports | Case, reports | R |
| QC-05 | Reporting to authorities and practitioner appeal / fair-hearing rights | Correspondence, case | R |

## 5. Network participation

| ID | Scenario | Product objects / capabilities | Basis |
|---|---|---|---|
| NW-01 | Assign base networks (participating / non-participating) with effective dates, including mandatory base networks and bulk row entry | HealthcareFacilityNetwork, HealthcarePayerNetwork | F, P |
| NW-02 | Child or limited networks scoped to a base network | HealthcarePayerNetwork plus a discovered hierarchy | F |
| NW-03 | Network tiers | ProviderNetworkTier | P |
| NW-04 | Participation through a contract (Network Participation component) | ProviderNetworkContract, Contract | P |
| NW-05 | Multi-grain participation (organisation, location, practitioner-location, taxonomy) and records derived by automation | Participation model (D-4) | F |
| NW-06 | Panel status, panel limit, accepting new patients | HealthcareFacilityNetwork PanelStatus / PanelLimit | P |
| NW-07 | Mass add or terminate participation by tax ID or NPI | Bulk processing (volume rule) | F |
| NW-08 | Participation attributes: capitation site, directory display indicators, participating-but-not-credentialed status | Discovered attributes; IsDirectoryPrint | F, P |

## 6. Contracting & reimbursement

| ID | Scenario | Product objects / capabilities | Basis |
|---|---|---|---|
| CT-01 | Apply a reimbursement template to generate payment agreements and term items | ContractPaymentAgreement, FeeScheduleDefinition | P |
| CT-02 | Fee-for-service fee schedule — facility vs non-facility price per procedure; percentage of a baseline | StandardCareFeeAgreement, CareFeeScheduleItem | P |
| CT-03 | Value-based agreements (capitation, shared savings, bundled, percentile, preventive, categorized) by line of business | Agreement objects | P |
| CT-04 | Contract generation from template, conditions and clauses with preview | Contract, guided UI, document generation | P |
| CT-05 | Internal approval, versioning and change review | Contract approval and versioning | P |
| CT-06 | E-signature and activation; signed document on the version | E-signature integration | P |
| CT-07 | Fee-arrangement maintenance with audit history | Field history / audit trail (D-7) | F |
| CT-08 | Rate-schedule assignment by provider type | Discovered rate model | F |

## 7. Onboarding & activation

| ID | Scenario | Product objects / capabilities | Basis |
|---|---|---|---|
| OB-01 | Go-live case with onboarding work guide or orchestration | Case, Flow Orchestration | P |
| OB-02 | Activate staged records after approval, following the discovered status model (D-5) | Provider, location and participation records | F |
| OB-03 | Synchronise provider data to downstream consumers (claims, data warehouse, directory, national/association feeds — D-12) | Events, change data capture, middleware, ETL | F |
| OB-04 | Portal activation, training and enablement content | Experience Cloud, Knowledge | P |

## 8. Provider data maintenance

| ID | Scenario | Product objects / capabilities | Basis |
|---|---|---|---|
| PD-01 | Provider change request (address, billing, phone, hours, telehealth) with review | Location model, work model | F |
| PD-02 | Add or change NPI; NPI history; automated NPI verification task | HealthcareProviderNpi, history (D-2, D-7) | P, F |
| PD-03 | Tax ID change; tax-ID history; re-pointing the billing organisation | Identifier model (D-2) | F |
| PD-04 | Specialty or taxonomy change with effective dates | HealthcareProviderTaxonomy, HealthcareProviderSpecialty | P, F |
| PD-05 | Add or remove a practice location; primary-location rules; secondary addresses | HealthcareFacility, HealthcarePractitionerFacility | P, F |
| PD-06 | Add or move affiliations, including mergers (move providers from one group to another) | HealthcarePractitionerFacility, AccountContactRelationship, Upsert Provider API | P, F |
| PD-07 | Data-domain work queues (e.g. NPI, taxonomy, priority, special handling) | Task or case queues, list views | F |
| PD-08 | Field-level audit trail and change-history view | Field history, Shield Field Audit Trail | P, F |
| PD-09 | Off-cycle events: name change, role change, new region or state | Work model, status model | F |

## 9. Recredentialing & ongoing monitoring

| ID | Scenario | Product objects / capabilities | Basis |
|---|---|---|---|
| RE-01 | Recredentialing cycle (at most 36 months) — scheduling, due-date batches, notices | Scheduled processing | R, F |
| RE-02 | CAQH access and re-attestation as a gate before recredentialing | CAQH integration | F |
| RE-03 | Recredentialing verification → review → committee, and conversion to initial credentialing when required | Case, work model | F, R |
| RE-04 | Ongoing monitoring of sanctions, licence expirations and complaints | CareProviderAdverseAction, BusinessLicense | R |
| RE-05 | Event-triggered off-cycle credentialing | Case | F |
| RE-06 | Automated reminders to providers (renewal, recredentialing) | Flows, notifications | P |

## 10. Roster & bulk intake

| ID | Scenario | Product objects / capabilities | Basis |
|---|---|---|---|
| RO-01 | Roster submitted by email into a roster case with one record per file | Email-to-Case, CaseRelatedFile | P |
| RO-02 | Roster upload on a provider portal with status tracking | Experience Cloud, CaseRelatedFile | P |
| RO-03 | Roster File Mapping with Data Processing Engine and GenAI field mapping | Data 360, Data Processing Engine | P |
| RO-04 | CAQH roster add, update, delete and status checks | MuleSoft CAQH Connector | P |
| RO-05 | Health-system roster reconciliation against existing participation | Bulk processing, staging | F |

## 11. Directory, search & consumption

| ID | Scenario | Product objects / capabilities | Basis |
|---|---|---|---|
| DS-01 | Internal provider search by NPI, tax ID, name, legacy ID, service address | Global search, custom search UI | F |
| DS-02 | Member- or agent-facing provider search | Provider Search API, CareProviderSearchableField, CareProviderSearchConfig | P |
| DS-03 | Search-index sync monitoring | ProviderSearchSyncLog | P |
| DS-04 | Directory accuracy feeds; print vs online directory indicators | IsDirectoryPrint, directory files | P, F |
| DS-05 | Read-only consumer access for view-only staff as a licence strategy | API to an external read-only app | F |
| DS-06 | Show code values with their definitions | Labels, reference objects (CareSpecialty and similar) | F |

## 12. Organisational & ancillary providers

| ID | Scenario | Product objects / capabilities | Basis |
|---|---|---|---|
| AN-01 | Site assessment and re-assessment of organisational providers | Assessment model (discovered or proposed) | F |
| AN-02 | Organisational service catalog: services, sub-services, billing type, provider type | CareService, HealthcareProviderService | P, F |
| AN-03 | Facility licences, Medicare/Medicaid numbers, accreditation | BusinessLicense, Accreditation, IdentityDocument | P, F |

## 13. Termination, reinstatement & exits

| ID | Scenario | Product objects / capabilities | Basis |
|---|---|---|---|
| TR-01 | Termination of a provider or location — full, partial, future-dated, extended | Effective dates, status model (D-5) | F |
| TR-02 | Provisional ("soft") termination and group-wide reinstatement | Status model (D-5) | F |
| TR-03 | Alert reviewers when an in-flight case references a terminated location | Case, location | F |
| TR-04 | Retain non-participating and out-of-area providers for downstream consumers | Status model, consumers (D-12) | F |

## 14. Delegated credentialing

| ID | Scenario | Product objects / capabilities | Basis |
|---|---|---|---|
| DG-01 | Delegated-entity roster intake that builds practitioner records at volume | Bulk processing (volume rule) | F |
| DG-02 | Delegation oversight — agreement, pre-delegation and annual audits, reporting | Contract or discovered model | R |

## 15. Provider service & contact center

| ID | Scenario | Product objects / capabilities | Basis |
|---|---|---|---|
| SV-01 | Provider inquiry (claims, contract terms) via portal messaging routed to a specialised queue | Messaging, Omni-Channel, Knowledge | P |
| SV-02 | Contact-centre agent grounded in provider-network data | Agentforce (payer contact center) | P |
| SV-03 | Credentialing assistant (expiry monitoring, CAQH/NPPES lookups, file assembly) | Custom agent topics/actions — `[Proposed]` | F |

## 16. Platform & migration

| ID | Scenario | Product objects / capabilities | Basis |
|---|---|---|---|
| PL-01 | Unique provider identifier strategy | External ID, SourceSystemIdentifier | P, F |
| PL-02 | Migration lanes, mapping validation, staged loads with sign-off | Data loading tools | F |
| PL-03 | Bridges that keep legacy downstream consumers working during transition | Middleware, ETL | F |
| PL-04 | Persona-based permission sets; event monitoring, field audit trail, encryption | Permission sets, Shield | P, F |
| PL-05 | Licence-tier strategy (full users vs read-only consumers) | Licensing, API | F |
| PL-06 | Re-platform declarative record-creation chains to bulk, testable services | Apex, asynchronous processing, Custom Metadata | F |
| PL-07 | Data-fix runbooks with validation queries and rollback | Scripts, queries | F |
| PL-08 | Change management — business champions, UAT entry/exit criteria, shadow and reverse-shadow support | — | F |

**Coverage:** 16 domains, 92 scenarios.

## Core domains

Intake & application · Credentialing · Network participation · Provider data
maintenance · Recredentialing & ongoing monitoring · Roster & bulk intake.
Their deep cards are in `references/scenario-cards-core.md`.
