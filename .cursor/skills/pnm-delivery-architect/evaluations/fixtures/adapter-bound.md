# Fixture — Workspace adapter with live discovery

**Shape:** an adapter supplies naming and pre-answers; an org query capability is bound and returns different facts for one dimension.

Adapter instance (as the workspace would provide it):

```markdown
## outputs
- location: out/stories
- queryArchive: out/queries

## tools
- orgQuery: fixture org-describe capability, target alias fixture-org
- sourceSearch: none
- structuredQuestions: none

## conventions
Prefix ABC_; services end in "Svc"; one trigger per object.

## discovery.preanswers
| # | Dimension | Answer | Evidence |
|---|---|---|---|
| D-1 | Provider anchor | HealthcareProvider | architecture note |
| D-5 | Status & temporal model | ABC_Stage__c picklist: Draft, Live, Ended | architecture note |

## personas
| Library role archetype | Organisation title |
|---|---|
| Network Configuration Specialist | Network Builder |
```

Org query capability returns, when invoked:

| Object | Fact |
|---|---|
| HealthcareProvider | 41,000 records; custom field ABC_Stage__c with values Draft, Live, Ended, **Suspended** |
| HealthcareFacilityNetwork | custom field ABC_TierCode__c (Text 10) |

The returned picklist has a value the adapter does not mention.
