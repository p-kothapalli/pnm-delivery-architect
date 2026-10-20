# Scenario Cards — Core Domains (Layer 2 detail)

Deep cards for the core domains: Intake & application (IN), Credentialing
(CR), Network participation (NW), Provider data maintenance (PD),
Recredentialing & ongoing monitoring (RE) and Roster & bulk intake (RO).
The index, the card rules and the evidence codes are in
`references/pnm-scenario-library.md`; cards for the other domains are in
`references/scenario-cards-extended.md`.

**How to read a card.** Product objects are `[Product]` candidates only — the
discovered anchor (D-1), location model (D-3) and participation model (D-4)
decide what is written. Field names in *Records typically written* are product
fields verified in the baseline or the object catalog; anything shown as
`{…per D-n}` must be discovered. A card never supplies status values, stage
names, record types or downstream systems.

---

## 2. Intake & application

### IN-01 · Portal application with CAQH pre-fill, attestation and e-signature
**Business need:** Let practitioners or their office staff apply online, pre-fill from the practitioner's CAQH profile to avoid rekeying, and capture a signed attestation before review starts.
**Personas:** Provider and Practice Office Manager (portal — the genuine portal exception); Provider Intake Specialist (internal review).
**Product objects that may be involved:** IndividualApplication, ApplicationCase, Case, ContentDocumentLink; shipped provider registration OmniScript; Experience Cloud; DocuSign and reCAPTCHA.
**Design options:** rung 0 — shipped registration OmniScript on an Experience Cloud site; rung 3 — extend it (runtime per D-9); rung 4 — LWC for multi-row sections the OmniScript cannot render; CAQH pre-fill at rung 6 through middleware.
**Discovery dimensions that change the design:** D-1 (is the application record the anchor or a staging record?), D-9 (OmniStudio runtime), D-10 (PNM add-on, Experience Cloud, portal permission sets), D-12 (CAQH binding), D-13 (attestation requirements).
**Records typically written:** Application — Create [Product: IndividualApplication; fields `[Assumed — confirm]`] · Case — Create · ApplicationCase — Create (ApplicationId, CaseId) · signed attestation file — Create (ContentDocumentLink to the case) · status per D-5.
**Edge cases:** the CAQH profile is not authorised for this plan or its attestation has lapsed · pre-filled data conflicts with typed data (which wins) · save and resume across sessions · signature declined or expired envelope · an application already exists for the same NPI (IN-04).
**Compliance hooks:** attestation currency and signed-application evidence when D-13 includes accreditation (A-4); tax IDs and dates of birth on the form (A-9).
**Basis:** P, F
**Evidence:** S3 (IndividualApplication and ApplicationCase are licence-gated) · S5 (ApplicationCase fields) · S7 (Experience Cloud prerequisites, DocuSign, reCAPTCHA) · S9 (CAQH connector) · S10 (application and attestation as credentialing elements) · CS-2 (portal application with pre-fill)

### IN-02 · Staff-entered participation request covering a practitioner, a group and their locations
**Business need:** Intake staff capture one request that names a practitioner, the group they join and the locations they will practise at, so one submission drives credentialing and participation.
**Personas:** Provider Intake Specialist, Provider Enrollment Specialist.
**Product objects that may be involved:** the provider anchor (D-1), HealthcareProvider or Account/Contact, HealthcareFacility, HealthcarePractitionerFacility, HealthcareProviderNpi, BusinessLicense, Case.
**Design options:** rung 2 — Screen Flow for a single practitioner; rung 3 — OmniScript for branching sections; rung 4 — LWC for multi-row location grids; rung 5 — Apex service when one request writes several practitioners or many locations (volume rule).
**Discovery dimensions that change the design:** D-1, D-2, D-3, D-5 (which records start staged), D-6 (what case or task the request creates), D-11 (practitioners and locations per request).
**Records typically written:** request/case — Create · practitioner anchor — Create or Update · practitioner location — Create per location (HealthcareProviderId, HealthcareFacilityId, EffectiveFrom, IsPrimaryFacility, IsActive per D-5) · identifier rows — Create (Npi, NpiType, EffectiveFrom).
**Edge cases:** the group or location already exists (link, do not duplicate) · a practitioner joins several groups in one request · one location is out of the service area (CR-06) · partial save when one section fails validation.
**Compliance hooks:** none on intake itself; the request starts the credentialing clock where D-13 measures turnaround.
**Basis:** F
**Evidence:** CS-2 (staff-entered request spanning practitioner, group and locations) · S4 (HealthcarePractitionerFacility fields) · S5 (HealthcareProviderNpi, BusinessLicense fields)

### IN-03 · Guided provider build wizard
**Business need:** Build a complete provider profile in one guided session: type and specialty → identity and tax ID → demographics → reason codes → base networks → child networks → tier → affiliations → billing address → service location with hours and telehealth.
**Personas:** Provider Enrollment Specialist, Provider Data Specialist.
**Product objects that may be involved:** HealthcareProvider, HealthcareProviderSpecialty, HealthcareProviderNpi, HealthcarePayerNetwork, HealthcareFacilityNetwork, ProviderNetworkTier, HealthcareFacility, HealthcarePractitionerFacility, OperatingHours, TimeSlot.
**Design options:** rung 4 — LWC stepper when steps need multi-row grids and search; rung 3 — OmniScript (runtime per D-9); rung 2 — Screen Flow when each step is a simple form. Save per step or once at the end is a design decision — state it.
**Discovery dimensions that change the design:** D-1 (anchor), D-2 (where tax ID and its type live; identifier history), D-3 (billing vs service location), D-4 (participation grain), D-5 (setup status while the build is incomplete), D-8 (reason-code model).
**Records typically written:** provider anchor — Create · specialty — Create (SpecialtyId, IsPrimarySpecialty, EffectiveFrom) · NPI — Create · participation — Create per network (PayerNetworkId, EffectiveFrom, EffectiveTo, IsActive) · location and practitioner location — Create · operating hours — Create · setup status per D-5.
**Edge cases:** a base network is mandatory for the provider type · NPI missing (warn or block per A-7) · copy the service address from the affiliated group · end date optional at initial build · abandon the wizard mid-way (draft remains, or not).
**Compliance hooks:** none; tax ID type may make the value an SSN (A-9).
**Basis:** F
**Evidence:** CS-1 (guided build wizard; step list and behaviours) · S4 (HealthcareProvider, HealthcareFacilityNetwork, ProviderNetworkTier) · S5 (HealthcareProviderSpecialty, HealthcarePayerNetwork)

### IN-04 · Detect and reuse existing, terminated or previously denied provider records
**Business need:** Before creating anything, find the provider if they already exist — active, terminated or denied — and reuse or reactivate rather than duplicate.
**Personas:** Provider Intake Specialist, Provider Data Steward.
**Product objects that may be involved:** HealthcareProviderNpi, the provider anchor, Account, Contact; duplicate and matching rules; global search.
**Design options:** rung 1 — matching and duplicate rules on the anchor; rung 2 — Flow lookup step at intake; rung 5 — Apex matching across NPI, tax ID, licence and name when rules cannot express the logic; rung 6 — enterprise matching service if one is `[Discovered]`.
**Discovery dimensions that change the design:** D-1, D-2 (which identifiers are unique, and at what grain), D-5 (what terminated and denied look like), D-7 (history to show the reviewer).
**Records typically written:** none on detection · on reuse: the existing anchor — Update (status per D-5) and a note or task recording the match decision.
**Edge cases:** same NPI on two records · a group NPI shared by several practitioners · denied within a waiting period the target enforces · name change since the last record · match found but owned by another team.
**Compliance hooks:** a previous denial or termination for cause must be visible to the reviewer (A-4) when D-13 covers it.
**Basis:** F
**Evidence:** CS-2 (reuse of terminated or denied records at intake) · CS-1 (search by NPI, tax ID, name and legacy identifier) · S5 (HealthcareProviderNpi)

### IN-05 · Address standardisation and overlap detection at entry
**Business need:** Standardise addresses as they are entered and detect when a new location overlaps an existing one, so downstream consumers get one clean address.
**Personas:** Provider Intake Specialist, Provider Data Specialist.
**Product objects that may be involved:** HealthcareFacility, Location, AssociatedLocation, the location model (D-3).
**Design options:** rung 6 — external address-verification service called from the entry UI; rung 5 — Apex callout with retry; rung 1 — validation rules only for format. Decide whether the standardised value replaces or sits beside the entered one.
**Discovery dimensions that change the design:** D-3, D-12 (address service and consumers that need the standard form), D-7 (keep the entered value?).
**Records typically written:** location — Create or Update with the standardised address and a verification marker `{per D-3}`.
**Edge cases:** the service is unavailable (save with a warning or block — A-7) · a rural address the service cannot resolve · a suite number that makes two addresses distinct · several practitioners sharing one location.
**Compliance hooks:** none.
**Basis:** F
**Evidence:** CS-1 (address standardisation to postal standards before propagation) · CS-2 (overlapping-location detection)

### IN-06 · Validation severity matrix — which rules block and which only warn
**Business need:** Agree, per rule, whether it stops the action or only warns, so intake is strict where it matters and does not stall on optional data.
**Personas:** Provider Enrollment Specialist (owner of the rule set), PNM Administrator.
**Product objects that may be involved:** validation rules, guided-UI messages.
**Design options:** rung 1 — validation rules for blocking checks; rung 2/3/4 — in-UI soft warnings; rung 5 — a rule service when rules depend on provider type and many records.
**Discovery dimensions that change the design:** D-8 (where rules live today), D-9 (UI technology), D-1 (which object owns the field).
**Records typically written:** none, or a warning acknowledgement `{per D-7}` when the target audits overrides.
**Edge cases:** a warning acknowledged at intake must not block a later stage · the same rule warns at intake and blocks at activation · rules differ by provider type or line of business.
**Compliance hooks:** none.
**Basis:** F
**Evidence:** CS-1 (missing NPI as a soft warning; tax ID and type mandatory) · CS-2 (blocking vs warning rules by stage)

### IN-07 · Bulk file intake of practitioners with rule validation, NPPES lookup and a fallout report
**Business need:** Accept a file of many practitioners, validate each row, check NPIs against the national registry and return a clear fallout report while good rows proceed.
**Personas:** Roster Analyst, Provider Intake Specialist.
**Product objects that may be involved:** Case, CaseRelatedFile, the provider anchor, HealthcareProviderNpi; Roster File Mapping (RO-03).
**Design options:** **volume rule applies.** Rung 0 — Roster File Mapping when the target has Data 360 (D-10); rung 5 — bulk Apex with asynchronous processing and staging; rung 6 — middleware. Never a record-by-record declarative chain.
**Discovery dimensions that change the design:** D-10 (Data 360), D-11 (rows per file, files per day), D-12 (registry access), D-1 and D-2 (what each row writes), D-9 (any in-org async framework — reuse only if `[Discovered]`).
**Records typically written:** intake case — Create · file record — Create (CaseId, ContentDocumentId, ProcessStage, ProcessStatus) · per row: anchor and identifiers — Create or Update · fallout rows `{per D-7 or [Proposed]}` with row number, rule and message.
**Edge cases:** the registry returns a different name or deactivated NPI · duplicate rows in the file · partial success and re-submission of failed rows only · the registry's results-per-request limit · a file with an unexpected column layout.
**Compliance hooks:** an NPI does not prove licensure — rows still need credentialing (A-4).
**Basis:** F
**Evidence:** S13 (registry API, NPI types, results limit, NPI is not proof of licensure) · S5 (CaseRelatedFile fields) · S7 (Roster File Mapping) · CS-2 (bulk practitioner intake with fallout report)

### IN-08 · Application withdrawal, closure and denial
**Business need:** Close applications that are withdrawn, abandoned or denied, with a recorded reason and the right notice to the applicant.
**Personas:** Credentialing Specialist, Provider Intake Specialist, Credentialing Committee Coordinator (for denials).
**Product objects that may be involved:** IndividualApplication, Case, ApplicationCase.
**Design options:** rung 1 — case closure with reason fields; rung 2 — Flow that closes related records and sends notice; rung 5 — Apex when closure cascades across many staged records.
**Discovery dimensions that change the design:** D-5 (closure statuses and what happens to staged records), D-6 (who may close), D-13 (notice and appeal rules).
**Records typically written:** application and case — Update (status per D-5, closure reason) · staged provider, location and participation rows — Update or delete per D-5 · notice — Create (correspondence record or file).
**Edge cases:** withdrawal after committee approval · a group application where one practitioner withdraws · re-application within a waiting period · abandoned for missing information after outreach.
**Compliance hooks:** denial notice and appeal rights (QC-05) when D-13 includes them (A-4).
**Basis:** F, R
**Evidence:** CS-2 (withdrawal, closure and denial paths) · S10 (decision notification) · S3 (application objects licence-gated)

---

## 3. Credentialing (initial)

### CR-01 · Route applications by provider attributes; balance workload; decide ownership on returns
**Business need:** Send each application to the right team by provider type, specialty or region, keep queues balanced, and decide who owns it when it comes back.
**Personas:** Credentialing Specialist, Credentialing Quality Reviewer, PNM Administrator.
**Product objects that may be involved:** Case, queues, assignment rules, Omni-Channel.
**Design options:** rung 1 — assignment rules and queues; rung 1 — Omni-Channel skills-based routing; rung 2 — Flow for ownership-on-return rules; rung 5 — Apex only when rules exceed declarative limits.
**Discovery dimensions that change the design:** D-6 (case per stage, queue model, owner rules on returns), D-1 (which attributes are reliably populated at routing time).
**Records typically written:** case — Update (owner, queue, stage per D-6).
**Edge cases:** the originating reviewer is inactive · a specialty with no queue · urgent applications jump the queue · reassignment during leave.
**Compliance hooks:** turnaround measurement from routing timestamps when D-13 tracks it.
**Basis:** P, F
**Evidence:** S6 (work guides, queues, routing by provider attributes) · CS-2 (return-to-originating-reviewer ownership rules)

### CR-02 · Combined application review and verification in one working session
**Business need:** Let the credentialer review the application and record verification results in one session instead of switching between records.
**Personas:** Credentialing Specialist, Primary Source Verification Specialist.
**Product objects that may be involved:** Case, the credential objects (BusinessLicense, BoardCertification, PersonEducation, PersonEmployment, CareProviderAdverseAction, InsurancePolicy).
**Design options:** rung 1 — Dynamic Forms and related lists on the case; rung 0 — work guide; rung 4 — LWC verification tiles (primer blueprint 4) when many elements are verified at once.
**Discovery dimensions that change the design:** D-1, D-6 (one case or several), D-9 (existing UI).
**Records typically written:** each credential — Update (Status, VerificationStatus, VerifiedDate where the object has them) · case — Update (stage per D-6).
**Edge cases:** a verification source is down · the element was verified under another application still within its validity window · partial save.
**Compliance hooks:** verification date and source per element (A-4).
**Basis:** F
**Evidence:** CS-2 (combined review and verification session) · S5 (credential object status and verification fields)

### CR-03 · Primary source verification of credentials
**Business need:** Verify each credential with its primary source — licence, DEA/CDS, education and training, board certification, work history, malpractice history and sanctions — and record source, result and date.
**Personas:** Primary Source Verification Specialist, Credentialing Specialist.
**Product objects that may be involved:** BusinessLicense, BoardCertification, PersonEducation, PersonEmployment, CareProviderAdverseAction, InsurancePolicy; shipped Primary Source Verification OmniScript.
**Design options:** rung 0 — shipped Primary Source Verification OmniScript; rung 1 — work guide per element; rung 6 — verification services through Named Credentials (CR-04).
**Discovery dimensions that change the design:** D-2 (how DEA/CDS is stored — no dedicated product object is verified), D-12 (bound verification services), D-13 (which elements and look-back periods apply).
**Records typically written:** licence — Update (Status, VerificationStatus, VerifiedDate, PeriodEnd) · board certification — Update (Status, ExpirationDate) · education — Update (Status, VerificationStatus, VerifiedDate) · employment — Create per position (StartDate, EndDate, VerificationStatus) · liability coverage — Create (Name, EffectiveDate, ExpirationDate, TotalSumInsured) · adverse action — Create when found.
**Edge cases:** a work-history gap above the target's threshold needs an explanation · a licence in another state · board certification pending · coverage expiring before the decision date.
**Compliance hooks:** every in-scope element has a source, a result and a date inside the allowed window (A-4); sanctions checked against the exclusion list (S14).
**Basis:** R, P
**Evidence:** S10 (verification elements) · S5 (credential object fields) · S7 (shipped Primary Source Verification OmniScript) · S12 (malpractice history via NPDB) · S14 (exclusion list)

### CR-04 · Hybrid verification — specialist first, then a verification organisation's API
**Business need:** A specialist verifies what needs judgement while a verification organisation's API returns the rest with real-time status.
**Personas:** Primary Source Verification Specialist, Integration Engineer.
**Product objects that may be involved:** work guide, Named Credential, the credential objects.
**Design options:** rung 6 — external verification service through Named Credential and middleware; rung 5 — Apex callouts with asynchronous status polling; rung 1 — work guide for the manual steps.
**Discovery dimensions that change the design:** D-12 (which organisation and API), D-9 (callout pattern in use), D-11 (verifications per day).
**Records typically written:** credential — Update (VerificationStatus, VerifiedDate) · request log `{per D-7 or [Proposed]}` with request time, response status and reference.
**Edge cases:** the API times out · results conflict with the specialist's findings · the organisation returns a partial result.
**Compliance hooks:** the verification organisation's own accreditation status, when D-13 requires it.
**Basis:** P
**Evidence:** S6 (work guides) · S7 (Primary Source Verification OmniScript) · S9 (MuleSoft connector pattern)

### CR-05 · NPDB query and continuous query; adverse-action capture
**Business need:** Query the national practitioner data bank at credentialing, optionally enrol practitioners for continuous monitoring, and capture any reported actions.
**Personas:** Primary Source Verification Specialist, Credentialing Specialist.
**Product objects that may be involved:** CareProviderAdverseAction or a discovered equivalent.
**Design options:** rung 6 — external query through middleware where the data bank's external application interface is in use; rung 1 — manual query with result upload; continuous-query alerts feed RE-04.
**Discovery dimensions that change the design:** D-12 (query method), D-13 (query obligations), D-7 (where query history is kept).
**Records typically written:** adverse action — Create per report (ActionType, IncidentDate, ActionIssueDate, RegulatoryBody, Status, PractitionerId) · query evidence file — Create.
**Edge cases:** a report revised or voided after capture · a practitioner enrolled by another entity · enrolment renewal at 12 months · the announced merger of one-time and continuous query services.
**Compliance hooks:** the query response is confidential — store and restrict accordingly (A-9); query history is the audit evidence (A-4).
**Basis:** F, R
**Evidence:** S12 (query types, 12-month enrolment, 24-hour notice, confidentiality, query history as evidence, December 2026 merger) · S5 (CareProviderAdverseAction fields) · CS-2 (data-bank query step in verification)

### CR-06 · Service-area verification for practice locations
**Business need:** Confirm each practice location lies inside an area the plan serves before it is credentialed into a network.
**Personas:** Credentialing Specialist, Network Management Specialist.
**Product objects that may be involved:** HealthcareFacility, Location (geolocation), the location model (D-3).
**Design options:** rung 1 — validation against a state or county list; rung 5 — Apex geographic check; rung 6 — external geocoding.
**Discovery dimensions that change the design:** D-3, D-13 (state programme rules), D-4 (out-of-area participation allowed?).
**Records typically written:** practitioner location — Update (service-area result `{per D-3 or [Proposed]}`).
**Edge cases:** telehealth-only location · a location on a state border · a service area that changed after the location was approved.
**Compliance hooks:** state programme network rules when D-13 includes them.
**Basis:** F
**Evidence:** CS-2 (service-area verification step)

### CR-07 · Specialty credentialing programmes
**Business need:** Run programme-specific credentialing — for example behavioural-health plus medical dual credentialing — with programme indicators that change the checklist.
**Personas:** Credentialing Specialist, Organisational Provider Credentialing Specialist.
**Product objects that may be involved:** HealthcareProviderSpecialty, CareSpecialty, programme attributes (discovered).
**Design options:** rung 1 — record types or picklist-driven checklists; rung 2 — Flow that adds programme steps; rung 3 — OmniScript branches.
**Discovery dimensions that change the design:** D-1, D-6 (separate cases per programme?), D-13 (programme rules).
**Records typically written:** programme indicator — Update `{per D-1}` · specialty — Create.
**Edge cases:** a practitioner credentialed in one programme and not the other · programme added after initial approval.
**Compliance hooks:** programme-specific elements (A-4).
**Basis:** F
**Evidence:** CS-2 (dual behavioural-health and medical credentialing) · S5 (HealthcareProviderSpecialty, CareSpecialty)

### CR-08 · Document capture and review
**Business need:** Collect and review supporting documents with enforced size and type limits, linked to the right credential.
**Personas:** Credentialing Specialist, Provider (portal upload).
**Product objects that may be involved:** ContentDocumentLink, CaseRelatedFile.
**Design options:** rung 1 — Files related list; rung 4 — LWC upload with type and size checks; rung 3 — OmniScript file step on the portal.
**Discovery dimensions that change the design:** D-6 (which record owns documents), D-7 (retention), D-10 (Experience Cloud file access).
**Records typically written:** file link — Create (to case or credential) · file record on the case — Create when processing status matters (CaseId, ContentDocumentId, ProcessStatus).
**Edge cases:** oversize or wrong type (block) · a document that covers several credentials · re-upload replacing an earlier version.
**Compliance hooks:** retention of verification evidence (A-4); PHI in uploads (A-9).
**Basis:** P, F
**Evidence:** S5 (CaseRelatedFile fields) · CS-2 (document size and type limits)

---

## 5. Network participation

### NW-01 · Assign base networks with effective dates
**Business need:** Place a provider into the plan's base networks as participating or non-participating from an effective date, including networks that are mandatory for the provider type, and add many rows at once.
**Personas:** Network Configuration Specialist, Network Management Specialist.
**Product objects that may be involved:** HealthcareFacilityNetwork, HealthcarePayerNetwork.
**Design options:** rung 1 — related list with quick action; rung 4 — LWC multi-row grid (primer blueprint 7); rung 0 — Network Participation component when participation is contract-based (NW-04); rung 5 for bulk (NW-07).
**Discovery dimensions that change the design:** D-4 (grain and any derived rows), D-5 (how participating vs non-participating is expressed), D-8.
**Records typically written:** participation — Create per network (PayerNetworkId, the grain lookup per D-4, EffectiveFrom, EffectiveTo, IsActive) · participation status per D-5.
**Edge cases:** a mandatory base network missing · overlapping date ranges for the same network · back-dated effective date · end date before start date (block).
**Compliance hooks:** participation must not be effective before the credentialing decision when D-13 requires it (A-4).
**Basis:** F, P
**Evidence:** CS-1 (main network mandatory, participating or non-participating, bulk row entry) · S4 (HealthcareFacilityNetwork fields) · S5 (HealthcarePayerNetwork fields)

### NW-02 · Child or limited networks scoped to a base network
**Business need:** Offer limited or custom networks that are only available under a chosen base network.
**Personas:** Network Configuration Specialist.
**Product objects that may be involved:** HealthcarePayerNetwork (ParentPayerNetworkId), HealthcareFacilityNetwork.
**Design options:** rung 1 — the product network hierarchy plus a filtered lookup; rung 4 — LWC dependent picker; rung 1 — validation rule enforcing the parent.
**Discovery dimensions that change the design:** D-4 (whether the target uses the product hierarchy or its own), D-5.
**Records typically written:** child participation — Create (PayerNetworkId of the child, EffectiveFrom within the parent's range).
**Edge cases:** the parent participation ends — what happens to children · a child shared by two base networks.
**Compliance hooks:** none.
**Basis:** F, P
**Evidence:** S5 (ParentPayerNetworkId on HealthcarePayerNetwork) · CS-1 (custom or limited networks scoped to a main network)

### NW-03 · Network tiers
**Business need:** Assign a provider to a tier within a network for benefit design and steerage.
**Personas:** Network Configuration Specialist.
**Product objects that may be involved:** ProviderNetworkTier.
**Design options:** rung 1 — related list; rung 4 — tier column in the participation grid.
**Discovery dimensions that change the design:** D-10 (**licence-gated**: PNM add-on), D-4.
**Records typically written:** tier — Create (ProviderNetworkId, IsActive).
**Edge cases:** tier changes mid-year · a tier defined for a network the provider does not participate in (block).
**Compliance hooks:** none.
**Basis:** P
**Evidence:** S4 (ProviderNetworkTier fields) · S3 (licence gate) · CS-1 (optional tier step)

### NW-04 · Participation through a contract
**Business need:** Record that a provider participates in a network because a contract binds them, using the shipped component.
**Personas:** Contracting Specialist, Network Configuration Specialist.
**Product objects that may be involved:** ProviderNetworkContract, Contract; Network Participation component.
**Design options:** rung 0 — Network Participation component; rung 2 — Flow on contract activation.
**Discovery dimensions that change the design:** D-4 (contract-based vs location-based participation, or both), D-10 (licence), D-5.
**Records typically written:** provider–network–contract — Create (StartDate, EndDate) · contract — Update.
**Edge cases:** contract amended mid-term · provider leaves the group that signed the contract · both a contract row and a location row exist — which governs.
**Compliance hooks:** none.
**Basis:** P
**Evidence:** S4 (ProviderNetworkContract; Network Participation component) · S3 (licence gate)

### NW-05 · Multi-grain participation and records derived by automation
**Business need:** Record participation at the grain the business needs — organisation, location, practitioner-location or taxonomy — and keep any automatically derived rows consistent.
**Personas:** Network Configuration Specialist, PNM Administrator.
**Product objects that may be involved:** HealthcareFacilityNetwork (lookups to facility, practitioner facility, practitioner and provider).
**Design options:** rung 1 — record types per grain; rung 5 — Apex that derives lower-grain rows (bulk-safe); rung 2 — record-triggered Flow at low volume only.
**Discovery dimensions that change the design:** D-4 (**critical**: which grains exist and which rows automation creates), D-9 (existing automation), D-11.
**Records typically written:** participation — Create per grain (record type per D-4, the grain's lookup, EffectiveFrom, IsActive) · derived rows — described as automation side effects in Technical Implementation.
**Edge cases:** a derived row edited by hand and later overwritten · deleting a parent row · grain changes during migration.
**Compliance hooks:** none.
**Basis:** F
**Evidence:** S4 (HealthcareFacilityNetwork lookups) · CS-2 (participation rows derived by automation at several grains)

### NW-06 · Panel status, panel limit and accepting new patients
**Business need:** Show whether a practitioner at a location accepts new patients and cap their panel.
**Personas:** Network Management Specialist, Provider Data Specialist.
**Product objects that may be involved:** HealthcareFacilityNetwork (PanelStatus, PanelLimit), CareProviderSearchableField (IsAcceptingNewPatients).
**Design options:** rung 1 — fields on the participation row; rung 2 — Flow that closes the panel at the limit.
**Discovery dimensions that change the design:** D-4, D-12 (directory consumers).
**Records typically written:** participation — Update (PanelStatus, PanelLimit).
**Edge cases:** panel closed for one network but open for another · the search index lagging behind the change (DS-03).
**Compliance hooks:** directory accuracy rules when D-13 includes them.
**Basis:** P
**Evidence:** S4 (PanelStatus, PanelLimit) · S5 (IsAcceptingNewPatients derived from an open panel status)

### NW-07 · Mass add or terminate participation by tax ID or NPI
**Business need:** Add or end participation for every provider under a tax ID or NPI in one operation.
**Personas:** Network Management Specialist, Roster Analyst.
**Product objects that may be involved:** HealthcareFacilityNetwork, HealthcareProviderNpi.
**Design options:** **volume rule applies.** Rung 5 — bulk Apex with asynchronous processing; rung 6 — data-loading tool with a reviewed file; never a looping Flow.
**Discovery dimensions that change the design:** D-2 (tax ID storage), D-4, D-5, D-11.
**Records typically written:** participation — Create or Update per affected row (EffectiveFrom or EffectiveTo, IsActive per D-5) · run log `{[Proposed]}` with counts and failures.
**Edge cases:** some providers already terminated · a future-dated termination overlapping a new addition · partial failure and re-run (idempotent).
**Compliance hooks:** termination notices when D-13 requires them (A-4).
**Basis:** F
**Evidence:** CS-2 (mass add or terminate by tax ID or NPI) · CS-1 (bulk row entry)

### NW-08 · Participation attributes
**Business need:** Carry participation attributes such as capitation site, print vs online directory display, and "participating but not credentialed".
**Personas:** Network Configuration Specialist.
**Product objects that may be involved:** HealthcarePractitionerFacility (IsDirectoryPrint), HealthcareFacilityNetwork; discovered attributes.
**Design options:** rung 1 — fields and record types; rung 4 — attribute columns in the participation grid.
**Discovery dimensions that change the design:** D-4, D-5 (is "not credentialed" a status or an attribute?), D-12 (directory and capitation consumers).
**Records typically written:** practitioner location — Update (IsDirectoryPrint) · participation — Update (attributes per D-4).
**Edge cases:** directory flag set on a future-dated row · a capitation site changing mid-month.
**Compliance hooks:** none.
**Basis:** F, P
**Evidence:** S4 (IsDirectoryPrint on HealthcarePractitionerFacility) · CS-2 (capitation site and participating-not-credentialed attributes)

---

## 8. Provider data maintenance

### PD-01 · Provider change request with review
**Business need:** Accept changes to address, billing, phone, hours or telehealth from the provider or staff, review them, and apply them.
**Personas:** Provider Data Specialist; Provider and Practice Office Manager (portal submission).
**Product objects that may be involved:** Case, HealthcareFacility, HealthcarePractitionerFacility, OperatingHours.
**Design options:** rung 2 — Screen Flow request plus approval; rung 3 — portal OmniScript; rung 6 — feeds from CAQH or survey tools when they are upstream.
**Discovery dimensions that change the design:** D-3, D-6 (review queue), D-7, D-12 (consumers of the change).
**Records typically written:** change case — Create · location — Update · operating hours — Update · history per D-7.
**Edge cases:** change effective in the future · change affecting several practitioners at one site · conflicting changes from two sources.
**Compliance hooks:** directory accuracy timelines when D-13 includes them.
**Basis:** F
**Evidence:** CS-1 (upstream updates via survey and CAQH; address and phone changes in field history) · CS-2 (change request review)

### PD-02 · Add or change NPI; NPI history; automated verification task
**Business need:** Maintain NPIs with history and automatically create a task to verify each new or changed NPI.
**Personas:** Provider Data Specialist.
**Product objects that may be involved:** HealthcareProviderNpi, Task.
**Design options:** rung 1 — effective-dated identifier rows; rung 2 — record-triggered Flow creates the task; rung 6 — registry lookup (S13).
**Discovery dimensions that change the design:** D-2 (product NPI object or custom history), D-6 (NPI queue), D-7.
**Records typically written:** NPI — Create (Npi, NpiType, EffectiveFrom, IsActive) · previous NPI — Update (EffectiveTo, IsActive) · verification task — Create.
**Edge cases:** NPI already on another provider · organisation vs individual NPI type · registry shows deactivation.
**Compliance hooks:** none.
**Basis:** P, F
**Evidence:** S5 (HealthcareProviderNpi fields) · S13 (registry lookup) · CS-1 (NPI history; automated NPI verification task)

### PD-03 · Tax ID change; tax-ID history; re-pointing the billing organisation
**Business need:** Change a provider's tax ID with history and move billing relationships to the new organisation.
**Personas:** Provider Data Specialist, Provider Data Steward.
**Product objects that may be involved:** the identifier model (D-2), Account.
**Design options:** rung 2 — Flow for a single provider; rung 5 — bulk Apex when a group's tax ID changes for many providers.
**Discovery dimensions that change the design:** D-2 (where tax ID and type live), D-12 (claims and payment consumers), D-11.
**Records typically written:** tax-ID history row — Create `{per D-2}` (value, type, effective from) · previous row — Update (effective to) · affiliation — Update.
**Edge cases:** tax ID type is SSN · future-dated change · claims in flight under the old tax ID.
**Compliance hooks:** none; the value may be an SSN (A-9).
**Basis:** F
**Evidence:** CS-1 (tax-ID history with type SSN or EIN)

### PD-04 · Specialty or taxonomy change with effective dates
**Business need:** Add, end or change a provider's specialty or taxonomy without losing history.
**Personas:** Provider Data Specialist.
**Product objects that may be involved:** HealthcareProviderSpecialty, HealthcareProviderTaxonomy, CareSpecialty, CareTaxonomy, CareSpecialtyTaxonomy.
**Design options:** rung 1 — effective-dated rows; rung 2 — Flow keeping one primary.
**Discovery dimensions that change the design:** D-1, D-5, D-12.
**Records typically written:** specialty — Create (SpecialtyId, IsPrimarySpecialty, EffectiveFrom) · taxonomy — Create (TaxonomyId, IsPrimaryTaxonomy, EffectiveFrom) · previous primary — Update (EffectiveTo).
**Edge cases:** two primaries · a new specialty needing credentialing first (CR-07) · code shown without its description (DS-06).
**Compliance hooks:** specialty-based board certification check when D-13 requires it.
**Basis:** P, F
**Evidence:** S5 (specialty and taxonomy fields) · CS-1 (type and specialty code with description)

### PD-05 · Add or remove a practice location; primary-location rules; secondary addresses
**Business need:** Maintain where a practitioner practises, keep exactly one primary location, and hold secondary addresses.
**Personas:** Provider Data Specialist.
**Product objects that may be involved:** HealthcareFacility, HealthcarePractitionerFacility.
**Design options:** rung 1 — related list with validation; rung 4 — LWC copying the address from the affiliated group; rung 5 — bulk when a site closes.
**Discovery dimensions that change the design:** D-3, D-4 (participation follows the location?), D-5.
**Records typically written:** practitioner location — Create or Update (HealthcareFacilityId, IsPrimaryFacility, EffectiveFrom, EffectiveTo, IsActive) · participation — Update when it follows the location.
**Edge cases:** removing the only primary location · location used by an in-flight case (TR-03) · secondary address for directory only.
**Compliance hooks:** none.
**Basis:** P, F
**Evidence:** S4 (HealthcarePractitionerFacility fields) · CS-1 (secondary addresses; copy address from affiliated group) · CS-2 (location removal effects)

### PD-06 · Add or move affiliations, including mergers
**Business need:** Affiliate practitioners with groups and move many practitioners when groups merge.
**Personas:** Provider Data Specialist, Network Management Specialist.
**Product objects that may be involved:** HealthcarePractitionerFacility, AccountContactRelationship; Upsert Provider API.
**Design options:** rung 1 — related list for single changes; rung 0 — Upsert Provider API for business-level bulk upserts; rung 5 — bulk Apex.
**Discovery dimensions that change the design:** D-1, D-3, D-11, D-12.
**Records typically written:** affiliation — Create (effective from, primary flag) · old affiliation — Update (effective to).
**Edge cases:** primary affiliation conflict · participation tied to the old group · per-provider partial success from the API.
**Compliance hooks:** none.
**Basis:** P, F
**Evidence:** S8 (Upsert Provider API, per-provider partial success) · CS-1 (individual-to-group affiliations with a primary flag)

### PD-07 · Data-domain work queues
**Business need:** Route data work into queues by domain — NPI, taxonomy, priority, special handling — so specialists work one kind of change at a time.
**Personas:** Provider Data Specialist, Provider Data Steward.
**Product objects that may be involved:** Task or Case, queues, list views.
**Design options:** rung 1 — queues and list views; rung 2 — Flow that creates the task in the right queue.
**Discovery dimensions that change the design:** D-6.
**Records typically written:** task — Create (subject, queue owner per D-6, related provider).
**Edge cases:** a change spanning two domains · priority escalation.
**Compliance hooks:** none.
**Basis:** F
**Evidence:** CS-1 (home page with NPI, taxonomy, priority and special-handling task queues) · S6 (queues)

### PD-08 · Field-level audit trail and change-history view
**Business need:** Show who changed which field, when, and keep that history as long as the business needs.
**Personas:** Provider Data Steward, Credentialing Quality Reviewer.
**Product objects that may be involved:** field history tracking; Shield Field Audit Trail; history related lists.
**Design options:** rung 1 — field history; rung 1 — Shield Field Audit Trail for longer retention (D-10); rung 4 — LWC timeline (primer blueprint 11).
**Discovery dimensions that change the design:** D-7, D-10.
**Records typically written:** none — history is platform-written.
**Edge cases:** history limits per object · changes made by integrations attributed to an integration user.
**Compliance hooks:** audit evidence for credentialing files (A-4).
**Basis:** P, F
**Evidence:** CS-1 (audit trail of field changes; field audit trail and event monitoring) · S5 (history on BoardCertification, HealthcareProviderSpecialty, CaseRelatedFile)

### PD-09 · Off-cycle events: name change, role change, new region or state
**Business need:** Handle life events that change the provider record outside the normal cycle.
**Personas:** Provider Data Specialist, Credentialing Specialist.
**Product objects that may be involved:** the provider anchor, BusinessLicense (new state).
**Design options:** rung 2 — Flow per event type; rung 1 — case types.
**Discovery dimensions that change the design:** D-5, D-6, D-13 (does a new state need credentialing?).
**Records typically written:** anchor — Update · licence — Create for a new state (JurisdictionState, LicenseNumber, PeriodStart, PeriodEnd).
**Edge cases:** name change mismatching the licence · new state without a licence yet.
**Compliance hooks:** licence verification for the new state (A-4).
**Basis:** F
**Evidence:** CS-2 (off-cycle event handling) · S5 (BusinessLicense jurisdiction fields)

---

## 9. Recredentialing & ongoing monitoring

### RE-01 · Recredentialing cycle — scheduling, due-date batches, notices
**Business need:** Recredential every practitioner within the cycle the target follows, by grouping due dates into batches and notifying in advance.
**Personas:** Credentialing Specialist, Credentialing Committee Coordinator.
**Product objects that may be involved:** Case; scheduled processing.
**Design options:** rung 2 — scheduled Flow at low volume; rung 5 — scheduled batch Apex at volume; rung 1 — report-driven work lists.
**Discovery dimensions that change the design:** D-5 (where the last decision date lives), D-6, D-11, D-13 (cycle length).
**Records typically written:** recredentialing case — Create per practitioner (due date, stage per D-6) · notice — Create.
**Edge cases:** a practitioner credentialed mid-cycle by an off-cycle event · leave of absence · cycle length shorter for some programmes.
**Compliance hooks:** cycle no longer than the target's standard — at most 36 months under the accreditation reference (A-4).
**Basis:** R, F
**Evidence:** S10 (recredentialing at most every 36 months) · CS-2 (due-date batches)

### RE-02 · CAQH access and re-attestation as a gate
**Business need:** Before recredentialing starts, confirm the plan still has CAQH access and the practitioner has re-attested.
**Personas:** Credentialing Specialist.
**Product objects that may be involved:** CAQH connector operations.
**Design options:** rung 6 — CAQH connector status checks; rung 1 — manual check recorded on the case.
**Discovery dimensions that change the design:** D-12, D-6.
**Records typically written:** case — Update (gate result `{per D-6}`) · outreach task — Create.
**Edge cases:** access revoked · attestation older than the target's limit · CAQH unavailable.
**Compliance hooks:** current attestation (A-4).
**Basis:** F
**Evidence:** S9 (CAQH connector operations) · CS-2 (access and re-attestation gate)

### RE-03 · Recredentialing verification → review → committee, and conversion to initial
**Business need:** Run recredentialing through verification, quality review and committee, and convert to initial credentialing when the gap or change requires it.
**Personas:** Credentialing Specialist, Credentialing Quality Reviewer, Credentialing Committee Coordinator.
**Product objects that may be involved:** Case, credential objects.
**Design options:** rung 1 — case stages; rung 2 — Flow Orchestration; rung 5 — Apex for bulk conversion.
**Discovery dimensions that change the design:** D-5, D-6 (**conversion rules**), D-13.
**Records typically written:** case — Update (stage per D-6) · on conversion: new initial case — Create, recredentialing case — Update (closure reason).
**Edge cases:** conversion after committee scheduling · a lapsed cycle · history to carry across.
**Compliance hooks:** committee decision evidence; conversion reason (A-4).
**Basis:** F, R
**Evidence:** S10 (committee review; recredentialing) · CS-2 (conversion of recredentialing to initial credentialing)

### RE-04 · Ongoing monitoring of sanctions, licence expirations and complaints
**Business need:** Between cycles, watch for sanctions, expiring licences and complaints, and act on them.
**Personas:** Credentialing Specialist, Medical Director.
**Product objects that may be involved:** CareProviderAdverseAction, BusinessLicense (PeriodEnd), BoardCertification (ExpirationDate), InsurancePolicy (ExpirationDate).
**Design options:** rung 2 — scheduled Flow on expirations; rung 6 — monthly exclusion-list supplements and continuous-query alerts; rung 5 — batch matching at volume.
**Discovery dimensions that change the design:** D-12 (monitoring sources), D-13, D-11.
**Records typically written:** adverse action — Create · monitoring task or case — Create · licence — Update (Status).
**Edge cases:** name-only match against the exclusion list · reinstated licence · complaint threshold reached.
**Compliance hooks:** monitoring frequency and evidence (A-4).
**Basis:** R
**Evidence:** S10 (ongoing monitoring of sanctions, complaints, adverse events) · S12 (continuous query) · S14 (monthly supplements) · S5 (expiry fields)

### RE-05 · Event-triggered off-cycle credentialing
**Business need:** Start a credentialing review outside the cycle when an event — a sanction, a new specialty, a complaint — requires it.
**Personas:** Credentialing Specialist.
**Product objects that may be involved:** Case.
**Design options:** rung 2 — record-triggered Flow; rung 1 — manual case type.
**Discovery dimensions that change the design:** D-6, D-13.
**Records typically written:** off-cycle case — Create (trigger reason).
**Edge cases:** an event during an open cycle case · several events for one practitioner.
**Compliance hooks:** reason and outcome recorded (A-4).
**Basis:** F
**Evidence:** CS-2 (off-cycle credentialing triggers) · S12 (alerts within 24 hours)

### RE-06 · Automated reminders to providers
**Business need:** Remind providers ahead of renewals and recredentialing deadlines.
**Personas:** Provider Relations Specialist, Credentialing Specialist.
**Product objects that may be involved:** Flow, email and notifications; Experience Cloud.
**Design options:** rung 2 — scheduled Flow; rung 6 — marketing or communication platform if `[Discovered]`.
**Discovery dimensions that change the design:** D-12, D-6.
**Records typically written:** reminder log — Create (email message or task).
**Edge cases:** bounced email · reminder after the item is already renewed.
**Compliance hooks:** none.
**Basis:** P
**Evidence:** S6 (reference lifecycle and automation) · CS-2 (renewal and recredentialing reminders)

---

## 10. Roster & bulk intake

### RO-01 · Roster submitted by email into a roster case
**Business need:** Turn each emailed roster into a case with one record per attached file.
**Personas:** Roster Analyst.
**Product objects that may be involved:** Email-to-Case, Case, CaseRelatedFile.
**Design options:** rung 0 — Email-to-Case plus Roster File Mapping file records.
**Discovery dimensions that change the design:** D-6, D-10, D-12.
**Records typically written:** case — Create · file record — Create per file (CaseId, ContentDocumentId, ProcessStage, ProcessStatus).
**Edge cases:** several files in one email · an unsupported file type · a re-sent roster.
**Compliance hooks:** delegated rosters (DG-01).
**Basis:** P
**Evidence:** S7 (Email-to-Case intake; one file record per file) · S5 (CaseRelatedFile)

### RO-02 · Roster upload on a provider portal with status tracking
**Business need:** Let groups upload rosters on the portal and watch processing status.
**Personas:** Practice Office Manager or Delegated Entity Administrator (portal); Roster Analyst.
**Product objects that may be involved:** Experience Cloud, Case, CaseRelatedFile.
**Design options:** rung 0 — Experience Cloud intake for Roster File Mapping; rung 4 — LWC status view (primer blueprint 9).
**Discovery dimensions that change the design:** D-10, D-6.
**Records typically written:** case — Create · file record — Create; status read from ProcessStatus.
**Edge cases:** upload succeeds but processing fails · large file timeouts.
**Compliance hooks:** none.
**Basis:** P
**Evidence:** S7 (Experience Cloud intake) · S5 (ProcessStage, ProcessStatus values)

### RO-03 · Roster File Mapping with Data Processing Engine and GenAI field mapping
**Business need:** Map arbitrary roster layouts to PNM objects with suggested field mappings and confidence scores.
**Personas:** Roster Analyst, PNM Administrator.
**Product objects that may be involved:** Data 360, Data Processing Engine, CaseRelatedFile; canonical roster template.
**Design options:** rung 0 — Roster File Mapping (requires Data 360; GenAI suggestions require the generative AI add-ons).
**Discovery dimensions that change the design:** D-10 (**licence-gated**), D-11, D-1.
**Records typically written:** provider records per mapping; file record — Update (ProcessStage, ProcessStatus, TargetDatasetName).
**Edge cases:** low-confidence suggestions · a new layout from the same submitter · failed rows.
**Compliance hooks:** none.
**Basis:** P
**Evidence:** S7 (Roster File Mapping; GenAI mapping suggestions; prerequisites)

### RO-04 · CAQH roster add, update, delete and status checks
**Business need:** Keep the plan's CAQH roster aligned with participating practitioners.
**Personas:** Roster Analyst, Integration Engineer.
**Product objects that may be involved:** MuleSoft CAQH Connector.
**Design options:** rung 6 — connector operations from middleware.
**Discovery dimensions that change the design:** D-12, D-11.
**Records typically written:** sync log `{[Proposed]}` per operation.
**Edge cases:** CAQH rejects a row · status check lag.
**Compliance hooks:** none.
**Basis:** P
**Evidence:** S9 (roster operations)

### RO-05 · Health-system roster reconciliation
**Business need:** Compare a health system's full roster against current participation and produce adds, changes and terminations.
**Personas:** Roster Analyst, Network Management Specialist.
**Product objects that may be involved:** HealthcareFacilityNetwork, HealthcarePractitionerFacility; staging.
**Design options:** **volume rule applies.** Rung 5 — bulk Apex comparison with staging; rung 6 — middleware or Data 360.
**Discovery dimensions that change the design:** D-4, D-11, D-2 (matching keys).
**Records typically written:** staged differences `{[Proposed]}` · after approval: participation and location rows — Create or Update.
**Edge cases:** providers missing from the roster (terminate or ask?) · intake channels other than files (fax, mail).
**Compliance hooks:** termination notice (A-4) when D-13 requires it.
**Basis:** F
**Evidence:** CS-2 (roster reconciliation) · CS-1 (roster intake by file, fax, email and mail)
