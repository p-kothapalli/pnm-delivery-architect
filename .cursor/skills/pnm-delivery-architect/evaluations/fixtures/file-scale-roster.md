# Fixture — File-scale roster

**Shape:** delegated groups send monthly rosters of about 20,000 rows.

| Dimension | Returned fact |
|---|---|
| D-1 Provider anchor | HealthcareProvider |
| D-4 Participation model | HealthcareFacilityNetwork |
| D-9 Build technology in use | No in-org async framework; no middleware |
| D-10 Licences & features | PNM add-on; Data 360 licensed; Experience Cloud licensed |
| D-11 Volumes | 20,000 rows per file; 12 delegated groups; files arrive in the first week of the month |
| D-12 Integrations & consumers | Directory and claims read provider data nightly |

The user states: "Today the team keys these in by hand."
