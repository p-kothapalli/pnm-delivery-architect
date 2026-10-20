# Fixture — Custom-anchored org, arbitrary prefix XYZ_

**Shape:** provider identity and locations live on custom objects; product PNM objects exist but are unused.

Source search and org query capabilities return:

| Dimension | Returned fact |
|---|---|
| D-1 Provider anchor | Person account with `XYZ_ProviderType__c`; HealthcareProvider has 0 records |
| D-3 Location model | `XYZ_PracticeLocation__c` (lookup to the provider account); fields `XYZ_Status__c`, `XYZ_EndDate__c`, `XYZ_TerminationReason__c` |
| D-4 Participation model | `XYZ_Participation__c` per location and network; fields `XYZ_Status__c`, `XYZ_EndDate__c`, `XYZ_Network__c` |
| D-5 Status & temporal model | `XYZ_Status__c` picklist values: Active, Pending Termination, Terminated; a nightly job sets Terminated when the end date passes |
| D-6 Work model | Case record type "Location Change"; queue "Location Maintenance" |
| D-8 Naming & conventions | Prefix `XYZ_` on every custom component |
| D-11 Volumes | Single-location terminations; at most 15 participation rows per location |

HealthcarePractitionerFacility and HealthcareFacilityNetwork exist (product licence) with 0 records.
