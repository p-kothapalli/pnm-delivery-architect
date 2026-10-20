# Workspace Adapter (Layer 4)

An adapter is an **optional, workspace-owned** file that binds this skill's
capabilities to local reality: where artifacts go, which tools answer which
questions, local naming rules, and any organisation-specific overlay.

**Adapters are never shipped inside this skill package.** The package ships
only the schema and the blank template below. The skill works without an
adapter.

## Contents

1. Capability rule
2. Adapter keys
3. Precedence
4. Blank template
5. Overlay file guidance

---

## 1. Capability rule

The skill refers to **capabilities**, never to a specific script, server
identifier or repository path.

| Capability | Question it answers | Fallback when unbound |
|---|---|---|
| Metadata dependencies | Who uses this component; what does it use | Source search; then disclose the gap |
| Source search | Does this component exist in the workspace source | Org query; then ask the user |
| Org query | Describe objects and fields; read record types, picklists, licences | Ask the user; label results `[Assumed — confirm]` |
| Official docs | What the product documents | The links in `references/pnm-product-baseline.md` §6 |
| Structured questions | Present choices to the user | One grouped, numbered free-text question per phase |
| Story index | Which existing requirements overlap | Disclose that no overlap check was run |
| Work items, diagrams, knowledge base, test prompts | STEP 6 offers | Do not offer that step (Mermaid is always available for diagrams) |

If a capability is unbound, say so once and continue with the fallback. **A
missing tool is never evidence that a component or feature does not exist.**

---

## 2. Adapter keys

| Key | Purpose | Value shape |
|---|---|---|
| `outputs.location` | Where plans, prototypes and stories are saved | Folder |
| `outputs.queryArchive` | Where validation queries are saved, if the workspace keeps an archive | Folder, or none |
| `tools.metadataDependencies` | Binding for the metadata-dependency capability | Command or tool reference, with usage notes |
| `tools.sourceSearch` | Binding for source search | Search tool, index, or command |
| `tools.orgQuery` | Binding for describe/query against the target org | CLI or tool reference, plus the target org alias |
| `tools.officialDocs` | Binding for official documentation lookup | Tool reference or "direct fetch" |
| `tools.structuredQuestions` | Binding for structured choices | Tool reference, or none |
| `tools.storyIndex` | Where existing requirements live | Folder(s) |
| `conventions` | Prefix, naming patterns, layering rules for custom components | Free text |
| `overlay` | Organisation-specific knowledge: stage model, status flags, routing rules, downstream feeds | Path to an overlay file (§5) |
| `discovery.preanswers` | Answers to any D-1…D-13 dimension | Table |
| `personas` | Organisation role titles mapped to library role archetypes | Table |
| `neutrality.denylist` | Extra terms that must not leak into artifacts for *other* organisations | List, or path to a list |

All keys are optional.

---

## 3. Precedence

When sources disagree about the target org:

1. **Live org metadata** (`[Discovered]`) — what is actually deployed.
2. **Workspace source** (`[Discovered]`, noting it may not be deployed).
3. **Adapter pre-answers and overlay** (`[Adapter]`).
4. **User answers in this session** — recorded as `[Adapter]` if they confirm
   an adapter value, otherwise as the provenance the user states.
5. **Product baseline** (`[Product]`) — what the product offers, not what the
   org uses.

Flag every disagreement between levels 1–3 as a Clarification Question.

---

## 4. Blank template

Copy into the workspace (for example as an always-applied editor rule or a
markdown file the trigger rule points to). Fill only what applies.

```markdown
# PNM Delivery Architect — workspace adapter

> Workspace-owned. Not part of the skill package.

## outputs
- location: <folder for plans, prototypes and stories>
- queryArchive: <folder, or none>

## tools
- metadataDependencies: <binding + one-line usage, or none>
- sourceSearch: <binding, or none>
- orgQuery: <binding + target org alias, or none>
- officialDocs: <binding, or direct fetch>
- structuredQuestions: <binding, or none>
- storyIndex: <folder(s), or none>

## conventions
<prefix, naming patterns, layering rules — or "none (greenfield)">

## overlay
<path to the overlay file, or none>

## discovery.preanswers
| # | Dimension | Answer | Evidence |
|---|---|---|---|
| D-1 | Provider anchor | | |

## personas
| Library role archetype | Organisation title |
|---|---|
| Credentialing Specialist | |

## neutrality.denylist
- <term>
```

---

## 5. Overlay file guidance

An overlay holds knowledge that is true for one organisation and must never
enter the package: stage names and their order, status values and what they
mean, routing and return-to-owner rules, record types, derived-record
automation, downstream feeds and their triggers, known defects and workarounds.

- Keep it in the workspace, next to the adapter.
- Cite evidence for each statement (component, object or document).
- The skill labels overlay facts `[Adapter]` and still verifies them against
  the org when a capability is bound; a mismatch becomes a Clarification
  Question.
