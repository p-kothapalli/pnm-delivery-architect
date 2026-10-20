# PNM Object Catalog (Layer 1 detail)

Field-level facts for the product objects a PNM artifact is likely to write or
read. This file extends `references/pnm-product-baseline.md` §3; the baseline
stays the summary and the licence authority.

Verified 2026-10-20 against the individual object reference pages (source S5
in the baseline register). Each entry lists the object's purpose, the API
version it appeared in, its licence gate, the fields documented on its page
(system fields such as Id, CreatedDate, LastViewedDate and LastReferencedDate
are omitted) and the documented picklist values.

## How to use this catalog

- A field listed here may be labelled `[Product]` in Pattern E and Technical
  Implementation. A field **not** listed here is `[Assumed — confirm]` until
  it is checked against official documentation or `[Discovered]` in the target.
- Picklist values are the **product** values. The target org may restrict or
  extend them; once `[Discovered]`, the target's values win.
- Fields marked *pilot* belong to a pilot feature (for example Site
  Management) and must not be used unless the target has the feature
  `[Discovered]`.
- Objects marked **Not verified** have a documented name but their reference
  page could not be read on the verification date. Name the object; label
  every field `[Assumed — confirm]`.

## Contents

1. Identifiers
2. Locations
3. Specialty and taxonomy
4. Services and conditions
5. Credentials
6. Networks
7. Contracting and reimbursement
8. Application, case and files
9. Search
10. Not verified
11. Reference page URLs

---

## 1. Identifiers

### HealthcareProviderNpi
A National Provider Identifier held by a practitioner or an organisation.

| Field | Notes |
|---|---|
| Npi | the 10-digit identifier |
| NpiType | picklist: Individual, Organization |
| PractitionerId | lookup to the practitioner (Contact) |
| AccountId | lookup to the organisation or person account |
| IsActive | |
| EffectiveFrom, EffectiveTo | effective dating — A-2 applies |
| SourceSystem, SourceSystemIdentifier | origin and external key (PL-01) |
| Name, OwnerId | |

Gate: none beyond Health Cloud.

## 2. Locations

HealthcarePractitionerFacility is verified in the baseline §3.2.
HealthcareFacility is listed in §10 (not verified).

## 3. Specialty and taxonomy

### CareSpecialty
Reference list of specialties.

| Field | Notes |
|---|---|
| Name, Description | |
| SpecialtyCode | code value |
| SpecialtyType | |
| SpecialtyUsage | whether it applies to practitioners, organisations or both |
| IsActive, EffectiveFrom, EffectiveTo | |
| OwnerId | |

### CareTaxonomy
Reference list of provider taxonomy codes, with a parent hierarchy.

| Field | Notes |
|---|---|
| Name, Description | |
| TaxonomyCode, TaxonomyType | |
| ParentTaxonomyId | self-lookup — taxonomy hierarchy |
| IsActive, EffectiveFrom, EffectiveTo | |
| OwnerId | |

### CareSpecialtyTaxonomy
Junction between a specialty and a taxonomy. Available from API 52.0.

| Field | Notes |
|---|---|
| CareSpecialtyId, CareTaxonomyId | the two sides of the junction |
| Name | autonumber |

### HealthcareProviderSpecialty
A specialty held by a provider.

| Field | Notes |
|---|---|
| SpecialtyId | lookup to CareSpecialty |
| PractitionerId | lookup to the practitioner (Contact) |
| AccountId | |
| IsPrimarySpecialty | |
| SpecialtyRole | picklist |
| IsActive, EffectiveFrom, EffectiveTo | A-2 |
| SourceSystem, SourceSystemIdentifier | |
| Name, OwnerId | |

Field history and change events are available. Research-related fields on the
page belong to the Site Management pilot — *pilot*.

### HealthcareProviderTaxonomy
A taxonomy held by a provider.

| Field | Notes |
|---|---|
| TaxonomyId | lookup to CareTaxonomy |
| PractitionerId | lookup to the practitioner (Contact) |
| AccountId | |
| HealthcareProviderId | API 62.0 — *pilot* |
| IsPrimaryTaxonomy | |
| IsActive, EffectiveFrom, EffectiveTo | A-2 |
| SourceSystem, SourceSystemIdentifier | |
| Name, OwnerId | |

### CareProviderFacilitySpecialty
A specialty offered by a practitioner at a specific location.

| Field | Notes |
|---|---|
| PractitionerFacilityId | lookup to HealthcarePractitionerFacility |
| SpecialtyId | lookup to CareSpecialty |
| AccountId | |
| HealthcareFacilityId | API 62.0 — *pilot* |
| IsPrimarySpecialty, SpecialtyRole | |
| IsActive, EffectiveFrom, EffectiveTo | A-2 |
| SourceSystem, SourceSystemIdentifier | |
| Name, OwnerId | |

## 4. Services and conditions

### CareService
A treatment, service or procedure offered by a provider, practitioner or
facility. Available from API 59.0.

| Field | Notes |
|---|---|
| Name | required |
| Description | |
| IsAppointmentRequired | default false |
| ReferralMethods | multi-select picklist |
| ServiceProvision | multi-select picklist: Free, Discount Available, Fees Apply |
| OwnerId | |

### HealthcareServiceDetail
Junction between a CareService and a code (CodeSet or CodeSetBundle).
Available from API 59.0.

| Field | Notes |
|---|---|
| CareServiceId | required |
| DetailCodeId | required; polymorphic: CodeSet, CodeSetBundle |
| DetailType | restricted picklist: Service_Category (default), Service_Type |
| Name | autonumber |
| OwnerId | |

### HealthcareProviderService
A service offered by a provider. Available from API 59.0.

| Field | Notes |
|---|---|
| CareServiceId | required; lookup to CareService |
| ProviderId | required; polymorphic: HealthcareFacility, HealthcarePractitionerFacility, HealthcareProvider |
| IsActive | default false |
| EffectiveFrom, EffectiveTo | A-2 |
| Name, OwnerId | |

### HlthCareProvTreatedCondition
A condition a provider treats. Available from API 59.0.

| Field | Notes |
|---|---|
| ConditionId | required; lookup to ProblemDefinition |
| HealthcareProviderId | required |
| IsActive, EffectiveFrom, EffectiveTo | |
| Name, OwnerId | |

## 5. Credentials

### BusinessLicense
A licence held by a person or organisation. Health Cloud from API 46.0.

| Field | Notes |
|---|---|
| LicenseNumber, Name | |
| Identifier | unique identifier |
| ContactId, AccountId, UserId, HealthcareProviderId | holder lookups — the target decides which is populated (D-1) |
| Issuer, IssueDate | |
| PeriodStart, PeriodEnd | date-times — the licence validity window |
| JurisdictionType | picklist: Country, County, Province, State (default State) |
| JurisdictionState, JurisdictionCountry, JurisdictionOther | |
| LicenseClass | picklist (API 48.0+): APN, LPN, MD, PC, PT |
| IsPrimaryLicense | added by the PNM add-on |
| IsActive | default false |
| Status | picklist: Draft, Inactive (default), Revoked, Verified |
| VerificationStatus | picklist: Authorized (default) |
| VerifiedDate | |
| SourceSystemUpdateDate | |
| Description, OwnerId | |

### BoardCertification
A board certification held by a practitioner.

| Field | Notes |
|---|---|
| BoardName | |
| CertificationType | picklist |
| PractitionerId, AccountId | |
| CurrentCertificationDate, ExpirationDate | |
| EffectiveFrom, EffectiveTo | A-2 |
| Status | picklist |
| TerminationDate, TerminationReason | |
| SourceSystem, SourceSystemIdentifier | |
| Name, OwnerId | |

Field history is available; change events from API 60.0.

### PersonEducation
Education and training of a person.

| Field | Notes |
|---|---|
| Name | |
| ContactId, IndividualId, UserId | person lookups |
| EducationLevel | picklist; values include Undergraduate, Medical School, Internship, Residency, Fellowship |
| StartDate, CompletionDate, GraduationDate | |
| Identifier, IdentifierIssuer | |
| IsActive | |
| Status | picklist: Draft, Inactive (default), Revoked, Verified |
| VerificationStatus | picklist: Authorized, None (default) |
| VerifiedDate | |
| InstitutionAddress, ProgramName, CertificateIdentifier | added by the PNM add-on |
| OwnerId | |

### PersonEmployment
Employment history of a person. **Requires the PNM add-on.**

| Field | Notes |
|---|---|
| Name, Position, Description | |
| RelatedPersonId | the person (Account or Contact) |
| HealthcareProviderId | |
| StartDate, EndDate | gaps between rows are the work-history gap check (CR-03) |
| EmploymentStatus | picklist: Employed, Home Maker, Retired, Self-Employed, Student, Unemployed with Income, Unemployed without Income |
| EmploymentType | picklist: Contract, Full-Time, Part-Time, Self-Employed, Temporary |
| Occupation | picklist of occupations |
| Employer address fields, EmployerPhone | |
| AnnualIncome | sensitive — A-9 |
| VerificationStatus | picklist: Authorized, Confirmed, Expired, In Progress, Submitted, Verified |
| VerificationDate | |
| OwnerId | |

### CareProviderAdverseAction
An adverse action against a provider. Available from API 47.0.

| Field | Notes |
|---|---|
| ActionType | picklist: Administrative Disciplinary Action, Court Order, Felony Conviction, Malpractice Judgement, Misdemeanor Conviction, Probationary License |
| PractitionerId, AccountId, HealthcareProviderId | subject lookups |
| BusinessLicenseId, BoardCertificationId, AccreditationId | the credential the action concerns |
| CaseNumber, CourtSentence, Description, Jurisdiction | |
| IncidentDate, IncidentReportedDate, ActionIssueDate | added by the PNM add-on |
| PenaltyAmount, InsurancePolicyNumber, InsuranceProviderName | added by the PNM add-on |
| RegulatoryBody, RegulatoryBodyType, ReportingEntity | |
| Status | picklist: Active, Revoked, Suspended |
| EffectiveFrom, EffectiveTo | |
| SourceSystem, SourceSystemIdentifier | |
| Name, OwnerId | |

### Accreditation
An accreditation held by a practitioner or organisation.

| Field | Notes |
|---|---|
| AccreditingBody, AccreditationRating | |
| Type, SubType, Status | |
| PractitionerId, AccountId | |
| HealthcareFacilityId | API 62.0 — *pilot* |
| LastFullSurveyDate, LastOnsiteSurveyDate | site-assessment evidence (AN-01, AN-03) |
| EffectiveFrom, EffectiveTo | |
| SourceSystem, SourceSystemIdentifier | |
| Name, OwnerId | |

### InsurancePolicy
An insurance policy — in PNM, typically the practitioner's professional
liability coverage. **Requires the PNM add-on.** The object is shared with
insurance products, so most of its fields are not meaningful for
credentialing; use the fields below and treat others as out of scope.

| Field | Notes |
|---|---|
| Name | the policy number |
| PolicyName, PolicyDescription, PolicyType | PolicyType values are insurance-product values; confirm the target's use |
| NameInsuredId | lookup to Account — the insured |
| EffectiveDate, ExpirationDate | coverage period — CR-03, RE-04 |
| CancellationDate, CancellationReason, CancellationReasonType | |
| IsActive | read-only; default false |
| Status, Substatus | picklists; default Initial and Draft |
| TotalSumInsured | coverage amount |
| UniversalPolicyNumber | |
| SourceSystem, SourceSystemIdentifier | |
| OwnerId | |

## 6. Networks

ProviderNetworkTier, HealthcareFacilityNetwork and ProviderNetworkContract are
verified in the baseline §3.2.

### HealthcarePayerNetwork
A payer's network or plan product.

| Field | Notes |
|---|---|
| Name, Code, Description | |
| PayerId | lookup to the payer Account |
| ParentPayerNetworkId | self-lookup — the product-network hierarchy (NW-02) |
| NetworkType | picklist: HMO, PPO, EPO |
| LineofBusiness | restricted picklist: Commercial for Groups, Commercial for Individuals, Exchange, Medicaid, Medicare |
| IsActive, EffectiveFrom, EffectiveTo | |
| SourceSystem, SourceSystemIdentifier | |
| OwnerId | |

## 7. Contracting and reimbursement

ContractPaymentAgreement and StandardCareFeeAgreement are verified in the
baseline §3.2. Every agreement object below is a **master-detail child of
ContractPaymentAgreement**, available from API 54.0 with the **PNM permission
set licence**, and has feed, history and (API 61.0+) change events.

### FeeScheduleDefinition
A fee schedule used as the baseline for fee-for-service agreements.

| Field | Notes |
|---|---|
| Name, Description | |
| FeeScheduleDefinitionKey | unique key |
| EffectiveStartDateTime, EffectiveEndDateTime | |
| OwnerId | |

### CareFeeScheduleItem
One procedure price in a fee schedule.

| Field | Notes |
|---|---|
| FeeScheduleDefinitionId | master-detail to FeeScheduleDefinition |
| ProcedureCodeId | lookup to CodeSetBundle |
| ProcedureCodeDescription | |
| FacilityPrice, NonFacilityPrice | CT-02 |
| CareFeeScheduleItemKey | unique key |
| Name | autonumber |

### CapitationCareFeeAgreement

| Field | Notes |
|---|---|
| ContractPaymentAgreementId | master-detail |
| MonthlyFee | per member per month |
| MonthlyWithheldPercentage | share withheld for performance |
| MonthlyBalanceFee | calculated |
| MemberAgeRangeLowerLimit, MemberAgeRangeUpperLimit | |
| Name | autonumber |

### CategorizedCareFeeAgreement

| Field | Notes |
|---|---|
| ContractPaymentAgreementId | master-detail |
| ProcedureCategory | for example immunisation |
| PricingInformation | agreed fee for the category |
| LineofBusiness | picklist: Commercial, Medi-Cal, Medicare |
| Description | |
| CategorizedCareFeeAgreeKey | unique key |
| Name | autonumber |

### BundledCareFeeAgreement

| Field | Notes |
|---|---|
| ContractPaymentAgreementId | master-detail |
| ProcedureBundleCodeId | lookup to CodeSetBundle |
| ProcedureBundleDescription, ProcedureBundleItemList | |
| BasicTierPrice, MidTierPrice, PremiumTierPrice | |
| Name | autonumber |

### SharedSavingPaymentAgreement

| Field | Notes |
|---|---|
| ContractPaymentAgreementId | master-detail |
| BenchmarkStartDateTime, BenchmarkEndDateTime | benchmark period |
| BenchmarkedExpenditureAmount, ForecastedExpenditureAmount | |
| QualifyingProfitPercentage | minimum profit before sharing |
| ProfitPlanDescription, LossPlanDescription | |
| Name | autonumber |

Percentile-based and preventive care-fee agreements are listed in §10.

## 8. Application, case and files

### ApplicationCase
Junction between an IndividualApplication and a Case. Available from API
52.0. **Requires the PNM add-on.**

| Field | Notes |
|---|---|
| ApplicationId | lookup to IndividualApplication |
| CaseId | lookup to Case |
| Name | autonumber |

### CaseRelatedFile
A file attached to a case, with processing details — the roster-file record
created by Roster File Mapping. Available from API 62.0.

| Field | Notes |
|---|---|
| CaseId | master-detail to Case |
| ContentDocumentId | the uploaded file |
| ProcessDefinitionReferenceId | the Data Processing Engine definition that processed it |
| ProcessStage | restricted picklist: Mapping, Processing, Staging |
| ProcessStatus | restricted picklist: Complete, Failed, InProgress, InReview |
| SourceDatasetName, TargetDatasetName | |
| Name | autonumber |

Field history and change events are available — use them for roster status
tracking (RO-01, RO-02) before proposing custom status fields.

## 9. Search

ProviderSearchSyncLog is verified in the baseline §3.2.

### CareProviderSearchableField
The denormalised search index row behind the Provider Search API. Available
from API 47.0. **Read and delete only** — rows are maintained by the platform's
sync job, so an artifact never writes them directly.

| Field | Notes |
|---|---|
| ProviderId, ProviderName, ProviderType, ProviderGender | |
| NationalProviderIdentifier | |
| FacilityId, FacilityName, FacilityPhone, Address | |
| Specialty, SubSpecialty, Service, ServiceCode, Condition | |
| LanguagesSpoken, PlanType, PhotoUrl | |
| IsAcceptingNewPatients | derived from the participation row's panel status being open |
| CertificationType, EducationLevel | |
| LicenseName, LicenseStatus (API 57.0+), LicenseJurisdictionState, LicenseJurisdictionCountry, LicenseJurisdictionRegion | |
| OperatingHoursId | |
| IsUpdateNeeded, SyncLogRecord | sync bookkeeping (DS-03) |

### CareProviderSearchConfig
Maps a source field on another object to a target field on the search index.
Available from API 48.0.

| Field | Notes |
|---|---|
| DeveloperName, MasterLabel | |
| MappedObject | restricted picklist: HealthcarePractitionerFacility, HealthcareProvider |
| SourceField, TargetField | API names of the copied and the receiving field |
| Language | restricted picklist of supported languages |
| IsActive | |

## 10. Not verified

Reference pages for these objects returned no content on 2026-10-20 (two
attempts, two documentation guides). Name the object; label every field
`[Assumed — confirm]`; re-check at the next verification.

| Object | What is known from the data-model pages (S1, S2) |
|---|---|
| HealthcareFacility | A location where care is delivered; the parent of practitioner-location rows and a participation grain |
| IndividualApplication | The application record used for provider applications; licence-gated by the PNM add-on |
| IdentityDocument | An identity document such as a government or programme identifier |
| Award | An award or recognition held by a practitioner |
| Percentile-based care-fee agreement | A ContractPaymentAgreement child; exact API name to confirm |
| PreventiveCareFeeAgreement | A ContractPaymentAgreement child |

## 11. Reference page URLs

All pages share the base
`https://developer.salesforce.com/docs/atlas.en-us.health_cloud_object_reference.meta/health_cloud_object_reference/`
followed by `sforce_api_objects_<object name in lower case>.htm` — for example
[HealthcareProviderNpi](https://developer.salesforce.com/docs/atlas.en-us.health_cloud_object_reference.meta/health_cloud_object_reference/sforce_api_objects_healthcareprovidernpi.htm),
[BusinessLicense](https://developer.salesforce.com/docs/atlas.en-us.health_cloud_object_reference.meta/health_cloud_object_reference/sforce_api_objects_businesslicense.htm),
[CaseRelatedFile](https://developer.salesforce.com/docs/atlas.en-us.health_cloud_object_reference.meta/health_cloud_object_reference/sforce_api_objects_caserelatedfile.htm)
and
[CareProviderSearchableField](https://developer.salesforce.com/docs/atlas.en-us.health_cloud_object_reference.meta/health_cloud_object_reference/sforce_api_objects_careprovidersearchablefield.htm).
