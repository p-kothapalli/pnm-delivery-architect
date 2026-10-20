# Fixture — Credentialing org with sensitive data

**Shape:** practitioners are credentialed in the org; some solo practitioners bill under their personal tax number.

| Dimension | Returned fact |
|---|---|
| D-1 Provider anchor | HealthcareProvider |
| D-2 Identifier model | Tax ID stored as text on the provider anchor; no masking or encryption detected |
| D-7 History & audit | Field history on; Shield not licensed |
| D-10 Licences & features | PNM add-on |
| Credentials | InsurancePolicy present and unused; BusinessLicense in use |
| D-13 Compliance scope | **Not supplied** — the user has not named an accreditation program or regulation |
