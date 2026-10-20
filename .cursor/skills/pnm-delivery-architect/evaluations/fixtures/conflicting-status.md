# Fixture — Conflicting lifecycle models

**Shape:** two status mechanisms drive the same record.

Org query and source search capabilities return:

| Dimension | Returned fact |
|---|---|
| D-1 Provider anchor | HealthcareProvider |
| D-5 Status & temporal model | Product IsActive and EffectiveFrom on HealthcareProvider **and** a custom picklist `XYZ_ProviderStatus__c` (Pending, Approved, Active, Inactive) on the same object |
| Automation | One flow sets IsActive when `XYZ_ProviderStatus__c` becomes Active; a separate scheduled job sets IsActive from EffectiveFrom regardless of the picklist |
| D-8 Naming & conventions | Prefix `XYZ_` |
| D-11 Volumes | 20–80 approvals per week |

Neither the documentation nor the user has said which mechanism governs.
