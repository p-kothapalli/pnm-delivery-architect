# Evaluations

Sixteen evaluations that exercise every workflow mode, the neutrality rule and
the package's own integrity. Each runs against a **fixture** — a neutral
description of an org shape — never against a real organisation.

## Files

| File | Purpose |
|---|---|
| `eval-NN-<slug>.json` | One evaluation: prompt, fixture and rubric |
| `fixtures/*.md` | Org shapes: what each capability returns and what the user answers if asked |

Each evaluation holds:

| Key | Meaning |
|---|---|
| `skills` | Always `["pnm-delivery-architect"]` |
| `mode` | The workflow mode the skill should enter |
| `fixture` | The fixture file, or `none` |
| `scenarios` | Scenario IDs the output is expected to cite (informational) |
| `query` | The prompt — a string, or a list for multi-prompt evaluations |
| `expected_behavior` | Conditions that must all hold |
| `must_not` | Conditions that fail the evaluation outright |

## Index

| # | Mode | Fixture | What it proves |
|---|---|---|---|
| 01 | Plan + Prototype | unknown-org | Asks discovery questions; no defaults; grounded prototype |
| 02 | New Feature | product-anchored-greenfield | Product objects and product values; complete Pattern E |
| 03 | New Feature | custom-xyz | Discovered names and statuses only; Patterns E and F |
| 04 | New Feature | licence-absent | Licence-gated objects flagged; options offered |
| 05 | New Feature | conflicting-status | Conflict surfaced, never resolved silently |
| 06 | New Feature | file-scale-roster | Volume rule; no record-by-record chain |
| 07 | Migration | migration-source | Identifier strategy, cleansing, bridges, parity, rollback |
| 08 | New Feature | unknown-org | Persona trap rejected |
| 09 | Neutrality | none | Outputs of 01–08 carry no organisation terms |
| 10 | New Feature | credentialing-org | Compliance (A-4) and sensitive data (A-9) without asserting unsupplied rules |
| 11 | New Feature | adapter-bound | Adapter vs discovered provenance; capability use; no tool names |
| 12 | New Feature | no-tools | Free-text fallback; standalone package |
| 13 | Data Remediation | remediation-missing-npi | Plan only; bounded, reversible, validated |
| 14 | Refactor; Bug Fix | refactor-bugfix | Component-scoped discovery; behaviour preserved or fixed explicitly |
| 15 | Epic Breakdown | epic-credentialing | Decomposition first; at most ten stories without approval |
| 16 | Package integrity | none | The package validator passes |

## How to run

1. Start a fresh session with only the skill installed (no adapter unless the
   fixture supplies one).
2. Give the agent the fixture text as the state of the org: capability results
   are returned only when the agent invokes that capability; user answers only
   when the agent asks.
3. Send the `query`.
4. Lint every story, plan and prototype produced with the package validator in
   artifact mode. For evaluation 09, supply an organisation denylist.
5. Score against the rubric below.

## Scoring

| Result | Rule |
|---|---|
| **Pass** | Every `expected_behavior` holds, no `must_not` occurs, and the validator reports zero FAIL for the artifacts |
| **Partial** | No `must_not` occurs and the validator reports zero FAIL, but at least one `expected_behavior` is missing |
| **Fail** | Any `must_not` occurs, or the validator reports a FAIL |

The release gate is **Pass on all sixteen**. Record each run with the date,
the skill version and the result; a Partial needs a note naming the missing
behaviour.

## Writing a new evaluation

- Use the next free number; never reuse one.
- Describe the org through a fixture; keep fixtures neutral — product objects,
  `XYZ_` or `ABC_` placeholders, invented counts.
- Each `must_not` is a single observable failure, not a style preference.
