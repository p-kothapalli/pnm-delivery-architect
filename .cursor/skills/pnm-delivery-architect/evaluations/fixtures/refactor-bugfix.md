# Fixture — Existing component for Refactor and Bug Fix

**Shape:** one custom component implements practitioner-location creation.

| Item | Returned fact |
|---|---|
| Component | `XYZ_LocationSvc` (Apex) creates HealthcarePractitionerFacility rows for one practitioner at a time from a screen flow |
| Callers (metadata-dependency capability) | Screen flow "Add Location"; one test class |
| Behaviour | Sets EffectiveFrom from the entered date; sets IsPrimaryFacility from the user's answer; inserts rows one at a time inside a loop |
| Defect | When a practitioner has no existing locations, IsPrimaryFacility stays false even if the user answered Yes |
| D-8 Naming & conventions | Prefix `XYZ_` |
| D-11 Volumes | A new bulk caller is planned: up to 500 locations per run |
