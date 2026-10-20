# Fixture — Remediation: practitioners missing NPI

**Shape:** a defect left practitioner records without an NPI identifier.

| Dimension | Returned fact |
|---|---|
| D-1 Provider anchor | HealthcareProvider |
| D-2 Identifier model | HealthcareProviderNpi per practitioner; intake creates it after the provider record |
| D-7 History & audit | Field history on HealthcareProvider; none on HealthcareProviderNpi |
| D-11 Volumes | 3,400 practitioners have no HealthcareProviderNpi row; 2,950 of them have an NPI on the original intake file |
| D-12 Integrations & consumers | Claims and the directory reject providers without an NPI |
| Root-cause evidence | Intake error log shows a validation failure on the identifier step for a two-week window; the provider record was still committed |
