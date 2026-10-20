# Fixture — Legacy migration source

**Shape:** a legacy provider system is being replaced by PNM.

Legacy side (user-supplied):

| Item | Fact |
|---|---|
| Provider records | ~120,000 practitioners, ~9,000 groups, ~30,000 locations |
| Identifiers | Legacy provider number per record; NPI present on 92 % of practitioners; tax ID on groups |
| Participation | Rows per provider, location and plan code, with start and end dates |
| History | Ten years of changes in an audit table |
| Consumers | Claims, the provider directory, a data warehouse and a capitation payment process read nightly extracts |

Target side (org query capability):

| Dimension | Returned fact |
|---|---|
| D-1 Provider anchor | HealthcareProvider; 0 records |
| D-10 Licences & features | PNM add-on; Shield licensed |
| D-8 Naming & conventions | Prefix `XYZ_` |
