# Scenario Cards — Extended Domains (Layer 2 detail)

Compact cards for Recruitment (RC), Quality review & committee (QC),
Contracting (CT), Onboarding (OB), Directory & search (DS), Organisational &
ancillary providers (AN), Termination (TR), Delegated credentialing (DG),
Provider service (SV) and Platform & migration (PL). The index, card rules and
evidence codes are in `references/pnm-scenario-library.md`; deep cards for the
core domains are in `references/scenario-cards-core.md`.

A compact card omits the Pattern E seed. When a story writes records, build
the Pattern E table from the object catalog (`references/pnm-object-catalog.md`)
and the discovered model.

---

## 1. Recruitment & network development

### RC-01 · Network adequacy analysis
**Business need:** Measure access by specialty and region (for example members within a distance of a provider) and forecast gaps to drive recruitment.
**Personas:** Provider Network Director.
**Product objects / capabilities:** CRM Analytics over provider, location and participation data.
**Design options:** rung 0 — CRM Analytics dashboards; rung 1 — standard reports; rung 6 — external geo-access tooling if `[Discovered]`.
**Discovery dimensions:** D-3 (geolocation present?), D-4, D-10 (analytics licence), D-13 (adequacy standards).
**Edge cases:** telehealth counted or not · providers at several locations.
**Compliance hooks:** state or federal adequacy standards when D-13 includes them.
**Basis:** P
**Evidence:** S6 (network adequacy and recruiting dashboards)

### RC-02 · Inbound provider registration from a public portal into a lead
**Business need:** Capture interest from providers who want to join, protected against bots.
**Personas:** Provider Recruitment Specialist; Provider (portal).
**Product objects / capabilities:** shipped recruitment OmniScript, Experience Cloud, reCAPTCHA, Lead.
**Design options:** rung 0 — shipped OmniScript on an Experience Cloud site.
**Discovery dimensions:** D-9, D-10.
**Edge cases:** duplicate lead for an existing provider (IN-04).
**Basis:** P
**Evidence:** S7 (shipped recruitment OmniScript; reCAPTCHA; Experience Cloud prerequisites)

### RC-03 · Lead segmentation and skill-based assignment
**Business need:** Assign recruitment leads by geography, provider type and specialty.
**Personas:** Provider Recruitment Specialist.
**Product objects / capabilities:** lead assignment rules, Omni-Channel.
**Design options:** rung 1 — assignment rules; rung 1 — Omni-Channel skills.
**Discovery dimensions:** D-6.
**Edge cases:** no matching recruiter.
**Basis:** P
**Evidence:** S6 (routing by provider attributes)

### RC-04 · Recruitment campaigns and journeys
**Business need:** Run targeted campaigns to recruit providers into gap areas.
**Personas:** Provider Recruitment Specialist.
**Product objects / capabilities:** Campaign, marketing journeys.
**Design options:** rung 1 — campaigns; rung 6 — marketing platform if `[Discovered]`.
**Discovery dimensions:** D-10, D-12.
**Edge cases:** opt-outs and contact consent.
**Basis:** P
**Evidence:** S6 (recruiting in the reference lifecycle)

### RC-05 · Lead review, outreach and conversion
**Business need:** Review a lead, chase missing information and convert it to provider records and a portal user.
**Personas:** Provider Recruitment Specialist.
**Product objects / capabilities:** Lead conversion; Experience Cloud user creation.
**Design options:** rung 1 — lead conversion with mapping; rung 2 — Flow that creates the portal user.
**Discovery dimensions:** D-1 (what conversion creates), D-10.
**Edge cases:** conversion into an existing account.
**Basis:** P
**Evidence:** S7 (Experience Cloud user for PNM) · S6 (recruitment to application)

---

## 4. Quality review, committee & decision

### QC-01 · Quality review with return for correction
**Business need:** A reviewer checks the credentialing file and either completes it or returns it for correction, to the originating reviewer when the target is configured that way.
**Personas:** Credentialing Quality Reviewer, Credentialing Specialist.
**Product objects / capabilities:** Case, verification status, the work model.
**Design options:** rung 1 — case stage with return action; rung 2 — Flow for ownership on return; primer blueprint 5.
**Discovery dimensions:** D-5, D-6 (**return rules**), D-7.
**Edge cases:** repeated returns · returning one element only · the originating reviewer is unavailable.
**Compliance hooks:** review evidence (A-4).
**Basis:** F
**Evidence:** CS-2 (quality review loop with return to the originating reviewer)

### QC-02 · Clean-file vs non-clean-file routing
**Business need:** Send files with no issues for streamlined approval and files with issues to full review.
**Personas:** Credentialing Quality Reviewer, Medical Director.
**Product objects / capabilities:** decision rules, case routing.
**Design options:** rung 1 — criteria-based routing; rung 2 — Flow decision.
**Discovery dimensions:** D-6, D-13 (clean-file criteria and who may sign off).
**Edge cases:** criteria changing after routing.
**Compliance hooks:** clean-file criteria and sign-off authority (A-4).
**Basis:** R, F
**Evidence:** S10 (committee and designee review) · CS-2 (clean and non-clean routing)

### QC-03 · Medical director review
**Business need:** A medical director reviews non-clean files and records an outcome.
**Personas:** Medical Director.
**Product objects / capabilities:** Case, review outcome.
**Design options:** rung 1 — approval process or case stage; rung 4 — review panel.
**Discovery dimensions:** D-6, D-13.
**Edge cases:** conflict of interest with the practitioner.
**Compliance hooks:** reviewer identity and date (A-4).
**Basis:** R, F
**Evidence:** S10 (medical director role in credentialing decisions) · CS-2

### QC-04 · Credentialing committee docket, decisions and minutes
**Business need:** Build a docket, capture approve, deny or defer decisions per practitioner, and produce minutes and reports.
**Personas:** Credentialing Committee Coordinator, Medical Director.
**Product objects / capabilities:** Case, reports, document generation.
**Design options:** rung 1 — list views and reports; rung 4 — docket UI (primer blueprint 6); rung 3 — document generation.
**Discovery dimensions:** D-5, D-6, D-13.
**Edge cases:** deferred decision carried to the next meeting · quorum not met.
**Compliance hooks:** committee decision evidence and minutes (A-4).
**Basis:** R
**Evidence:** S10 (credentialing committee review)

### QC-05 · Reporting to authorities and appeal rights
**Business need:** Report adverse decisions where required and offer the practitioner appeal or fair-hearing rights.
**Personas:** Credentialing Committee Coordinator.
**Product objects / capabilities:** correspondence, Case.
**Design options:** rung 2 — Flow-driven notices; rung 1 — appeal case type.
**Discovery dimensions:** D-13 (**reporting obligations and appeal process**), D-6.
**Edge cases:** appeal upheld — reverse the decision across records.
**Compliance hooks:** reporting obligations (S12 — health plans must report when appropriate) and appeal evidence (A-4).
**Basis:** R
**Evidence:** S12 (health-plan reporting and querying obligations) · S10

---

## 6. Contracting & reimbursement

### CT-01 · Apply a reimbursement template
**Business need:** Generate payment agreements and their term items from a template.
**Personas:** Contracting Specialist, Reimbursement Analyst.
**Product objects / capabilities:** ContractPaymentAgreement, FeeScheduleDefinition.
**Design options:** rung 0 — PNM contract lifecycle; rung 2 — Flow that clones template agreements.
**Discovery dimensions:** D-10 (**licence-gated**), D-12 (payment systems).
**Edge cases:** template changes after agreements were generated.
**Basis:** P
**Evidence:** S4 (ContractPaymentAgreement fields) · S5 (FeeScheduleDefinition) · S7 (contract lifecycle)

### CT-02 · Fee-for-service fee schedule
**Business need:** Price procedures with facility and non-facility prices, or as a percentage of a baseline schedule.
**Personas:** Reimbursement Analyst.
**Product objects / capabilities:** StandardCareFeeAgreement, CareFeeScheduleItem.
**Design options:** rung 1 — related lists; rung 4 — fee grid (primer blueprint 8); rung 5 — bulk load for large schedules.
**Discovery dimensions:** D-10, D-11.
**Edge cases:** missing procedure code · percentage and explicit price both present.
**Basis:** P
**Evidence:** S4 (StandardCareFeeAgreement; StandardFeeCalculationPercentage) · S5 (CareFeeScheduleItem prices)

### CT-03 · Value-based agreements by line of business
**Business need:** Model capitation, shared savings, bundled, percentile, preventive and categorized agreements.
**Personas:** Reimbursement Analyst, Contracting Manager.
**Product objects / capabilities:** the agreement child objects of ContractPaymentAgreement.
**Design options:** rung 0 — product agreement objects; rung 1 — layouts per agreement type.
**Discovery dimensions:** D-10, D-12.
**Edge cases:** line-of-business values differ between objects (check each object's values).
**Basis:** P
**Evidence:** S4 (AgreementType values) · S5 (capitation, categorized, bundled and shared-savings fields)

### CT-04 · Contract generation from template with preview
**Business need:** Generate a contract from a template with conditions and clauses, previewed before sending.
**Personas:** Contracting Specialist.
**Product objects / capabilities:** Contract, guided UI, document generation.
**Design options:** rung 0 — PNM contract lifecycle; rung 3 — OmniStudio document generation.
**Discovery dimensions:** D-9, D-10.
**Edge cases:** clause conflicts.
**Basis:** P
**Evidence:** S7 (contract lifecycle)

### CT-05 · Internal approval, versioning and change review
**Business need:** Approve contracts internally and keep versions.
**Personas:** Contracting Manager.
**Product objects / capabilities:** contract approval and versioning.
**Design options:** rung 0 — shipped approval and versioning.
**Discovery dimensions:** D-6.
**Edge cases:** approval withdrawn after signature request.
**Basis:** P
**Evidence:** S7 (approval workflow, version management)

### CT-06 · E-signature and activation
**Business need:** Send for signature, store the signed document on the version, and activate.
**Personas:** Contracting Specialist.
**Product objects / capabilities:** e-signature integration.
**Design options:** rung 0 — shipped e-signature integration.
**Discovery dimensions:** D-12, D-5.
**Edge cases:** declined signature · expired envelope.
**Basis:** P
**Evidence:** S7 (e-signature integration; DocuSign)

### CT-07 · Fee-arrangement maintenance with audit history
**Business need:** Update fee arrangements and see who changed what.
**Personas:** Reimbursement Analyst.
**Product objects / capabilities:** field history; agreement history objects.
**Design options:** rung 1 — field history; rung 4 — change timeline.
**Discovery dimensions:** D-7.
**Edge cases:** retroactive rate change.
**Basis:** F
**Evidence:** CS-1 (fee-arrangement updates with clear audit history) · S5 (agreement history objects)

### CT-08 · Rate-schedule assignment by provider type
**Business need:** Assign a rate schedule automatically from the provider's type.
**Personas:** Reimbursement Analyst.
**Product objects / capabilities:** discovered rate model.
**Design options:** rung 1 — Custom Metadata mapping; rung 2 — Flow.
**Discovery dimensions:** D-1, D-12.
**Edge cases:** provider type changes after assignment.
**Basis:** F
**Evidence:** CS-2 (rate schedule by provider type)

---

## 7. Onboarding & activation

### OB-01 · Go-live case with onboarding work guide or orchestration
**Business need:** Coordinate the tasks between approval and go-live.
**Personas:** Provider Relations Specialist.
**Product objects / capabilities:** Case, work guides, Flow Orchestration.
**Design options:** rung 0 — work guide; rung 2 — Flow Orchestration.
**Discovery dimensions:** D-6.
**Edge cases:** a dependent task blocked by a downstream system.
**Basis:** P
**Evidence:** S6 (work guides and orchestration for go-live)

### OB-02 · Activate staged records after approval
**Business need:** Flip staged provider, location and participation records to active, following the discovered status model.
**Personas:** Provider Data Specialist, Network Configuration Specialist.
**Product objects / capabilities:** provider, location and participation records.
**Design options:** rung 2 — Flow at single-provider volume; rung 5 — bulk Apex when activation spans many records (volume rule). Pattern F applies.
**Discovery dimensions:** D-5 (**critical**; watch for two status mechanisms — Org Discovery §6), D-4, D-11.
**Edge cases:** partial activation · future effective date · activation failure on one record.
**Compliance hooks:** not active before the decision date (A-4).
**Basis:** F
**Evidence:** CS-2 (activation of staged records after approval)

### OB-03 · Synchronise provider data to downstream consumers
**Business need:** Send changes to claims, warehouse, directory and association feeds reliably.
**Personas:** Integration Engineer.
**Product objects / capabilities:** platform events, change data capture, middleware, ETL.
**Design options:** rung 6 — change data capture into middleware; rung 5 — outbound Apex at low volume; see `references/integrations.md`.
**Discovery dimensions:** D-12 (**critical**), D-11.
**Edge cases:** consumer down · ordering of dependent changes · replays.
**Basis:** F
**Evidence:** CS-1 (outbound chain to enterprise consumers; real-time feed to the data warehouse) · S5 (change events on provider objects)

### OB-04 · Portal activation, training and enablement content
**Business need:** Give newly active providers portal access and learning content.
**Personas:** Provider Relations Specialist.
**Product objects / capabilities:** Experience Cloud, Knowledge.
**Design options:** rung 0 — Experience Cloud and Knowledge.
**Discovery dimensions:** D-10.
**Edge cases:** office staff needing their own access.
**Basis:** P
**Evidence:** S7 (Experience Cloud user for PNM)

---

## 11. Directory, search & consumption

### DS-01 · Internal provider search
**Business need:** Find providers by NPI, tax ID, name, legacy ID or service address without result caps.
**Personas:** Provider Data Specialist, Provider Services Representative.
**Product objects / capabilities:** global search, custom search UI.
**Design options:** rung 1 — global search with searchable fields; rung 4 — LWC search (primer blueprint 10).
**Discovery dimensions:** D-2, D-3.
**Edge cases:** tax ID search restricted for sensitive values (A-9).
**Basis:** F
**Evidence:** CS-1 (search by NPI, tax ID, site address and name)

### DS-02 · Member- or agent-facing provider search
**Business need:** Let members or agents search by specialty, plan, location, language and more.
**Personas:** Provider Services Representative; member (portal).
**Product objects / capabilities:** Provider Search API, CareProviderSearchableField, CareProviderSearchConfig.
**Design options:** rung 0 — Provider Search API and index; rung 1 — search configuration for extra fields.
**Discovery dimensions:** D-4, D-10, D-12.
**Edge cases:** a field needed by search but not in the index (add via search configuration).
**Basis:** P
**Evidence:** S8 (Provider Search criteria) · S5 (search index and configuration fields)

### DS-03 · Search-index sync monitoring
**Business need:** Detect and fix providers whose search index rows failed to sync.
**Personas:** PNM Administrator.
**Product objects / capabilities:** ProviderSearchSyncLog; IsUpdateNeeded on the index.
**Design options:** rung 1 — reports on the sync log; rung 2 — alert Flow.
**Discovery dimensions:** D-11.
**Edge cases:** repeated failures for one provider.
**Basis:** P
**Evidence:** S4 (ProviderSearchSyncLog) · S5 (IsUpdateNeeded, SyncLogRecord)

### DS-04 · Directory accuracy feeds; print vs online indicators
**Business need:** Feed directories accurately and control what prints vs what appears online.
**Personas:** Provider Data Specialist, Integration Engineer.
**Product objects / capabilities:** IsDirectoryPrint; directory files.
**Design options:** rung 6 — outbound file or API; rung 1 — indicator fields.
**Discovery dimensions:** D-12, D-13.
**Edge cases:** future-dated changes leaking into the directory.
**Compliance hooks:** directory accuracy rules when D-13 includes them.
**Basis:** P, F
**Evidence:** S4 (IsDirectoryPrint) · CS-1 (directory files to the public directory)

### DS-05 · Read-only consumer access as a licence strategy
**Business need:** Give view-only staff provider data without a full licence each.
**Personas:** Claims Research Analyst (read-only), PNM Administrator.
**Product objects / capabilities:** API to an external read-only app.
**Design options:** rung 6 — external app over the API; rung 1 — lower-tier licences if they fit.
**Discovery dimensions:** D-10, D-12.
**Edge cases:** sensitive fields exposed through the API (A-9).
**Basis:** F
**Evidence:** CS-1 (read-only consumer app roughly halving licence count)

### DS-06 · Show code values with their definitions
**Business need:** Display codes (specialty, reason, taxonomy) together with their descriptions.
**Personas:** Provider Services Representative, Claims Research Analyst.
**Product objects / capabilities:** CareSpecialty, CareTaxonomy descriptions; labels.
**Design options:** rung 1 — formula or lookup display; rung 4 — LWC.
**Discovery dimensions:** D-8.
**Edge cases:** retired codes.
**Basis:** F
**Evidence:** CS-1 (code values shown with definitions) · S5 (Description on CareSpecialty and CareTaxonomy)

---

## 12. Organisational & ancillary providers

### AN-01 · Site assessment and re-assessment of organisational providers
**Business need:** Assess organisational sites before approval and on a cycle, or accept an accreditation in lieu.
**Personas:** Organisational Provider Credentialing Specialist.
**Product objects / capabilities:** assessment model (discovered or proposed); Accreditation survey dates.
**Design options:** rung 1 — case plus checklist; rung 3 — guided assessment; rung 4 — mobile-friendly form.
**Discovery dimensions:** D-1, D-6, D-13.
**Edge cases:** accreditation accepted in lieu of a site visit.
**Compliance hooks:** organisational assessment evidence (A-4).
**Basis:** F
**Evidence:** CS-2 (organisational site assessment) · S5 (LastFullSurveyDate, LastOnsiteSurveyDate)

### AN-02 · Organisational service catalog
**Business need:** Record which services and sub-services an organisation offers, with billing and provider type.
**Personas:** Organisational Provider Credentialing Specialist, Provider Data Specialist.
**Product objects / capabilities:** CareService, HealthcareProviderService, HealthcareServiceDetail.
**Design options:** rung 0 — product service objects; rung 1 — reference data load.
**Discovery dimensions:** D-1, D-8.
**Edge cases:** a service offered at some locations only (ProviderId may be a practitioner-location).
**Basis:** P, F
**Evidence:** S5 (CareService, HealthcareProviderService, HealthcareServiceDetail) · CS-2 (ancillary service catalog)

### AN-03 · Facility licences, programme numbers and accreditation
**Business need:** Track facility licences, Medicare and Medicaid numbers and accreditation.
**Personas:** Organisational Provider Credentialing Specialist.
**Product objects / capabilities:** BusinessLicense, Accreditation, IdentityDocument.
**Design options:** rung 1 — related lists; rung 2 — expiry monitoring Flow.
**Discovery dimensions:** D-2 (where programme numbers live — IdentityDocument fields are unverified).
**Edge cases:** one accreditation covering several sites.
**Compliance hooks:** organisational credentialing elements (A-4).
**Basis:** P, F
**Evidence:** S5 (BusinessLicense, Accreditation fields; IdentityDocument not verified) · CS-2

---

## 13. Termination, reinstatement & exits

### TR-01 · Termination — full, partial, future-dated, extended
**Business need:** End a provider's or location's participation entirely, for some networks only, from a future date, or extend an end date.
**Personas:** Network Management Specialist, Provider Data Specialist.
**Product objects / capabilities:** effective dates, the status model.
**Design options:** rung 2 — Flow at single-provider volume; rung 5 — bulk Apex for groups. Pattern F applies.
**Discovery dimensions:** D-5 (**critical**), D-4, D-12.
**Edge cases:** termination before effective start · reversing a future termination.
**Compliance hooks:** termination notices and reasons (A-4).
**Basis:** F
**Evidence:** CS-2 (termination variants)

### TR-02 · Provisional termination and group-wide reinstatement
**Business need:** Suspend provisionally, then reinstate everyone in a group together.
**Personas:** Network Management Specialist.
**Product objects / capabilities:** status model.
**Design options:** rung 5 — bulk reinstatement; Pattern F.
**Discovery dimensions:** D-5, D-11.
**Edge cases:** one practitioner terminated for cause within a reinstated group.
**Compliance hooks:** reason codes (A-4).
**Basis:** F
**Evidence:** CS-2 (provisional termination and reinstatement)

### TR-03 · Alert reviewers when an in-flight case references a terminated location
**Business need:** Warn reviewers working a case when a location it relies on has been terminated.
**Personas:** Credentialing Specialist.
**Product objects / capabilities:** Case, location.
**Design options:** rung 2 — record-triggered Flow posting an alert; rung 1 — highlights panel.
**Discovery dimensions:** D-3, D-6.
**Edge cases:** location reinstated before the case closes.
**Basis:** F
**Evidence:** CS-2 (terminated-location alert)

### TR-04 · Retain non-participating and out-of-area providers
**Business need:** Keep non-participating and out-of-area providers so downstream consumers can still pay or reference them.
**Personas:** Provider Data Steward.
**Product objects / capabilities:** status model, consumers (D-12).
**Design options:** rung 1 — status values and filters.
**Discovery dimensions:** D-5, D-12.
**Edge cases:** directory must exclude them.
**Basis:** F
**Evidence:** CS-1 (non-participating and out-of-state providers retained for downstream use)

---

## 14. Delegated credentialing

### DG-01 · Delegated-entity roster intake at volume
**Business need:** Accept a delegated entity's roster of already-credentialed practitioners and build their records at volume.
**Personas:** Delegated Credentialing Analyst, Roster Analyst; Delegated Entity Administrator (portal).
**Product objects / capabilities:** bulk processing (volume rule); Roster File Mapping.
**Design options:** **volume rule applies.** Rung 0 — Roster File Mapping (D-10); rung 5 — bulk Apex with async; rung 6 — middleware.
**Discovery dimensions:** D-11, D-1, D-4, D-9 (existing async framework — reuse only if `[Discovered]`).
**Edge cases:** practitioner already credentialed directly by the plan · rows failing validation.
**Compliance hooks:** delegation agreement scope (DG-02; A-4).
**Basis:** F
**Evidence:** CS-2 (delegated roster intake building practitioner records at volume) · S7 (Roster File Mapping)

### DG-02 · Delegation oversight
**Business need:** Manage the delegation agreement, pre-delegation and annual audits, and reporting from the delegate.
**Personas:** Delegated Credentialing Analyst.
**Product objects / capabilities:** Contract or a discovered model.
**Design options:** rung 1 — contract plus audit case type; rung 2 — scheduled audit Flow.
**Discovery dimensions:** D-13 (**critical**), D-6.
**Edge cases:** audit failure and corrective action.
**Compliance hooks:** delegation oversight (A-4).
**Basis:** R
**Evidence:** S10 (delegation oversight) · S12 (delegated credentialing service providers are health-plan entity types)

---

## 15. Provider service & contact center

### SV-01 · Provider inquiry routed to a specialised queue
**Business need:** Providers ask about claims or contract terms through portal messaging and reach the right team.
**Personas:** Provider Services Representative.
**Product objects / capabilities:** Messaging, Omni-Channel, Knowledge.
**Design options:** rung 0 — Messaging with Omni-Channel.
**Discovery dimensions:** D-6, D-10.
**Edge cases:** inquiry about a provider the agent cannot see.
**Basis:** P
**Evidence:** S6 · S11 (payer contact centre)

### SV-02 · Contact-centre agent grounded in provider-network data
**Business need:** An AI agent answers contact-centre questions using provider-network data.
**Personas:** Provider Services Representative.
**Product objects / capabilities:** Agentforce in the payer contact center.
**Design options:** rung 6a — Agentforce with human review.
**Discovery dimensions:** D-10 (**licence**), D-12.
**Edge cases:** answer about a future-dated change.
**Basis:** P
**Evidence:** S11 (payer contact center with Agentforce)

### SV-03 · Credentialing assistant
**Business need:** An assistant that watches expiries, performs CAQH and registry lookups and assembles files.
**Personas:** Credentialing Specialist.
**Product objects / capabilities:** custom agent topics and actions — `[Proposed]`; no shipped credentialing agent.
**Design options:** rung 6a — custom Agentforce topics and actions over the credential objects.
**Discovery dimensions:** D-10, D-12, D-13.
**Edge cases:** the assistant must not record a verification without human confirmation.
**Compliance hooks:** human sign-off on verification (A-4).
**Basis:** F
**Evidence:** CS-2 (proposed verification-review and CAQH-match assistants) · S11 (no shipped credentialing agent found in release notes, checked 2026-10-20) · S13 · S9

---

## 16. Platform & migration

### PL-01 · Unique provider identifier strategy
**Business need:** One unique provider key replacing composite legacy keys, used by every load and consumer.
**Personas:** Data Migration Lead, Provider Data Steward.
**Product objects / capabilities:** External ID, SourceSystemIdentifier.
**Design options:** rung 1 — external ID field plus SourceSystem and SourceSystemIdentifier on product objects.
**Discovery dimensions:** D-2, D-12.
**Edge cases:** legacy duplicates mapping to one key.
**Basis:** P, F
**Evidence:** CS-1 (single unique provider identifier replacing a composite legacy key) · S5 (SourceSystem and SourceSystemIdentifier on product objects)

### PL-02 · Migration lanes, mapping validation and staged loads with sign-off
**Business need:** Move data through mapping, validation, test, stage and production loads with sign-off per lane.
**Personas:** Data Migration Lead.
**Product objects / capabilities:** data-loading tools.
**Design options:** see `references/legacy-to-pnm-migration.md`.
**Discovery dimensions:** D-1 to D-4, D-11.
**Edge cases:** a lane fails sign-off after downstream lanes started.
**Basis:** F
**Evidence:** CS-1 (migration swimlanes and phase sign-offs)

### PL-03 · Bridges that keep legacy consumers working
**Business need:** Keep legacy downstream systems fed while they still expect the old shapes.
**Personas:** Integration Engineer.
**Product objects / capabilities:** middleware, ETL.
**Design options:** rung 6 — bridge mappings retired as consumers move.
**Discovery dimensions:** D-12.
**Edge cases:** a consumer that cannot accept new identifiers.
**Basis:** F
**Evidence:** CS-1 (bridging procedures between the product data model and legacy consumers)

### PL-04 · Persona-based permission sets; monitoring, audit trail and encryption
**Business need:** Grant access by persona and protect sensitive data with monitoring, audit trail and encryption.
**Personas:** PNM Administrator.
**Product objects / capabilities:** permission sets, Shield.
**Design options:** rung 1 — permission set groups per persona; Shield features when licensed (D-10).
**Discovery dimensions:** D-10, D-7.
**Edge cases:** encrypted fields that must stay searchable.
**Basis:** P, F
**Evidence:** CS-1 (persona-based permission sets; event monitoring, field audit trail, encryption) · S3 (PNM permission sets)

### PL-05 · Licence-tier strategy
**Business need:** Decide who needs a full licence and who can consume read-only.
**Personas:** PNM Administrator, Provider Network Director.
**Product objects / capabilities:** licensing, API.
**Design options:** see DS-05.
**Discovery dimensions:** D-10.
**Edge cases:** read-only users who occasionally need to edit.
**Basis:** F
**Evidence:** CS-1 (persona and licence analysis)

### PL-06 · Re-platform declarative record-creation chains to bulk services
**Business need:** Replace chains of declarative record creation that fail at volume with bulk, testable services.
**Personas:** PNM Administrator, Integration Engineer.
**Product objects / capabilities:** Apex, asynchronous processing, Custom Metadata.
**Design options:** rung 5 — bulk services with async sequencing; keep the UI and replace its write path.
**Discovery dimensions:** D-9 (**critical** — inventory the active chain), D-11.
**Edge cases:** parity with the old chain's side effects.
**Basis:** F
**Evidence:** CS-2 (re-platforming a declarative record-creation chain to bulk services)

### PL-07 · Data-fix runbooks with validation queries and rollback
**Business need:** Fix bad data safely with a repeatable runbook.
**Personas:** Provider Data Steward, PNM Administrator.
**Product objects / capabilities:** scripts, queries.
**Design options:** see `references/data-remediation-mode.md`.
**Discovery dimensions:** D-7, D-11.
**Edge cases:** fix interacts with automation (bypass or not).
**Basis:** F
**Evidence:** CS-2 (data-fix runbooks)

### PL-08 · Change management
**Business need:** Prepare teams for the change with champions, UAT criteria and shadowing.
**Personas:** Provider Network Director, Data Migration Lead.
**Product objects / capabilities:** none.
**Design options:** champions per team, learning material, entry and exit criteria, shadow and reverse-shadow support.
**Discovery dimensions:** D-12 (teams affected).
**Edge cases:** a team without a champion.
**Basis:** F
**Evidence:** CS-1 (change champions, UAT and production entry and exit criteria, shadowing)
