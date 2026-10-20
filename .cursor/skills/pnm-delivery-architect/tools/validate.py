#!/usr/bin/env python3
"""
PNM Delivery Architect — package, neutrality and artifact validator.

Three groups of checks:

  PACKAGE     the skill is internally consistent and standalone: references
              cited and present, links resolve, scenario index complete,
              AC patterns defined, badge lists agree, verification dates fresh
  NEUTRALITY  no organisation-specific names, prefixes, paths or tool
              identifiers in the package (built-in baseline + optional denylist)
  ARTIFACT    a generated story, Solution Plan or prototype satisfies the
              blockers that can be checked deterministically

Stdlib only, no network. Exit 1 on any FAIL, or on WARN under --strict.

    validate.py                                   # package + neutrality
    validate.py --denylist terms.txt              # add organisation terms
    validate.py --artifacts out/*.md out/*.html   # lint generated artifacts
    validate.py --json                            # machine-readable
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys
from dataclasses import dataclass, field

FAIL, WARN, INFO = "FAIL", "WARN", "INFO"
STALE_AFTER_DAYS = 180
EXPECTED_DOMAINS = 16
PATTERNS_REQUIRED = list("ABCDEFG")
PROVENANCE = ("[Product]", "[Discovered]", "[Adapter]", "[Proposed]", "[Assumed — confirm]")


@dataclass
class Finding:
    level: str
    code: str
    message: str
    where: str = ""


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)

    def add(self, level: str, code: str, message: str, where: str = "") -> None:
        self.findings.append(Finding(level, code, message, where))

    def ok(self, code: str, message: str) -> None:
        self.add(INFO, code, message)

    def counts(self) -> dict[str, int]:
        return {lv: sum(1 for f in self.findings if f.level == lv) for lv in (FAIL, WARN, INFO)}


def read(p: pathlib.Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def line_of(text: str, index: int) -> int:
    return text[:index].count("\n") + 1


def before_version_history(text: str) -> str:
    """Changelog rows record what past versions claimed; they are not live claims."""
    marker = re.search(r"^#+\s*Version [Hh]istory", text, re.M)
    return text[: marker.start()] if marker else text


# ---------------------------------------------------------------- package ----

def package_files(skill_dir: pathlib.Path, rule_file: pathlib.Path | None) -> list[pathlib.Path]:
    files = [skill_dir / "SKILL.md", *sorted((skill_dir / "references").glob("*.md"))]
    ev = skill_dir / "evaluations"
    if ev.is_dir():
        files += sorted(p for p in ev.rglob("*") if p.is_file() and p.suffix in (".md", ".json"))
    if rule_file and rule_file.is_file():
        files.append(rule_file)
    return [f for f in files if f.is_file()]


def check_package(skill_dir: pathlib.Path, rule_file: pathlib.Path | None, rep: Report) -> dict:
    facts: dict = {}
    skill_md = skill_dir / "SKILL.md"
    refs_dir = skill_dir / "references"
    if not skill_md.is_file():
        rep.add(FAIL, "P01", "SKILL.md not found", str(skill_md))
        return facts
    skill_text = read(skill_md)

    m = re.search(r"^#\s*PNM Delivery Architect\s*\(v([\d.]+)\)", skill_text, re.M)
    if m:
        facts["version"] = m.group(1)
        rep.ok("P01", f"skill version v{m.group(1)}")
    else:
        rep.add(FAIL, "P01", "cannot parse the version from SKILL.md's H1")
    fm = re.match(r"^---\n(.*?)\n---\n", skill_text, re.S)
    if not fm or not re.search(r"^name:\s*pnm-delivery-architect\s*$", fm.group(1), re.M):
        rep.add(FAIL, "P01", "SKILL.md front matter missing or name is not pnm-delivery-architect")

    # Reference wiring, both directions.
    on_disk = {p.name for p in refs_dir.glob("*.md")} if refs_dir.is_dir() else set()
    cited = set(re.findall(r"references/([a-z0-9._-]+\.md)", skill_text))
    facts["reference_count"] = len(on_disk)
    for orphan in sorted(on_disk - cited):
        rep.add(WARN, "P02", "reference exists but SKILL.md never cites it — unreachable", f"references/{orphan}")
    for dangling in sorted(cited - on_disk):
        rep.add(FAIL, "P03", "SKILL.md cites a reference that does not exist", f"references/{dangling}")
    if on_disk and on_disk == cited:
        rep.ok("P02", f"all {len(on_disk)} references cited and present")

    # Cross-reference citations inside references.
    for ref in sorted(refs_dir.glob("*.md")):
        for name in set(re.findall(r"references/([a-z0-9._-]+\.md)", read(ref))):
            if name not in on_disk:
                rep.add(FAIL, "P03", f"cites references/{name}, which does not exist", ref.name)

    # Relative markdown links resolve inside the package.
    broken = 0
    for f in package_files(skill_dir, rule_file):
        text = read(f)
        for lm in re.finditer(r"\]\(([^)\s]+)\)", text):
            target = lm.group(1).split("#")[0]
            if not target or re.match(r"^[a-z]+:", target):
                continue
            if not (f.parent / target).resolve().exists():
                broken += 1
                rep.add(FAIL, "P08", f"relative link does not resolve: {target}", f"{f.name}:{line_of(text, lm.start())}")
    if not broken:
        rep.ok("P08", "all relative links resolve inside the package")

    check_scenarios(refs_dir / "pnm-scenario-library.md", skill_dir, rep, facts)
    check_patterns(refs_dir / "ac-pattern-library.md", rep, facts)
    check_badges(skill_dir, rep, facts)
    check_primer(refs_dir / "slds2-pnm-primer.md", rep, facts)
    check_catalog(refs_dir, rep, facts)
    check_evaluations(skill_dir / "evaluations", rep, facts)
    check_rule_file(rule_file, rep)
    check_dates(skill_dir, rep, facts)
    return facts


EXPECTED_BLUEPRINTS = 12
EXPECTED_EVALS = 16
EVAL_KEYS = ("skills", "mode", "fixture", "query", "expected_behavior", "must_not")


def check_primer(primer: pathlib.Path, rep: Report, facts: dict) -> None:
    if not primer.is_file():
        rep.add(WARN, "P10", "SLDS 2 primer not shipped — prototypes record 'primer: pending'")
        return
    text = read(primer)
    blueprints = re.findall(r"^###\s+B(\d{1,2})\s+·", text, re.M)
    facts["blueprint_count"] = len(blueprints)
    if len(set(blueprints)) != EXPECTED_BLUEPRINTS:
        rep.add(FAIL, "P10", f"{len(set(blueprints))} PNM blueprints in the primer; {EXPECTED_BLUEPRINTS} expected",
                primer.name)
    for hook in ("pnm-build-banner", "pnm-legend", "pnm-badge"):
        if f".{hook}" not in text:
            rep.add(FAIL, "P10", f"primer defines no style for .{hook}", primer.name)
    if re.search(r"font-size:\s*\d+px", text):
        rep.add(FAIL, "P10", "primer uses a hard-coded pixel font size", primer.name)
    if len(set(blueprints)) == EXPECTED_BLUEPRINTS:
        rep.ok("P10", f"primer: {EXPECTED_BLUEPRINTS} blueprints, banner, legend and badge styles present")


def check_catalog(refs_dir: pathlib.Path, rep: Report, facts: dict) -> None:
    cat, base = refs_dir / "pnm-object-catalog.md", refs_dir / "pnm-product-baseline.md"
    if not cat.is_file():
        rep.add(WARN, "P11", "object catalog not shipped")
        return
    objects = set(re.findall(r"^###\s+([A-Z][A-Za-z]+)\s*$", read(cat), re.M))
    facts["catalog_objects"] = len(objects)
    if base.is_file():
        rows = [r for r in read(base).splitlines() if re.match(r"^\|[^|]+\|[^|]+\|\s*Verified \([^)]*S5", r)]
        for r in rows:
            for name in re.findall(r"\b([A-Z][a-z]+[A-Z][A-Za-z]+)\b", r.split("|")[2].split("(")[0]):
                if name not in objects:
                    rep.add(FAIL, "P11", f"baseline marks {name} verified (S5) but the catalog has no entry", base.name)
    rep.ok("P11", f"object catalog: {len(objects)} object entries")


def check_evaluations(ev_dir: pathlib.Path, rep: Report, facts: dict) -> None:
    if not ev_dir.is_dir():
        rep.add(WARN, "P12", "no evaluations folder")
        return
    files = sorted(ev_dir.glob("eval-*.json"))
    numbers: list[int] = []
    for f in files:
        m = re.match(r"eval-(\d{2})-", f.name)
        if not m:
            rep.add(FAIL, "P12", "evaluation file name must be eval-NN-<slug>.json", f.name)
            continue
        numbers.append(int(m.group(1)))
        try:
            data = json.loads(read(f))
        except json.JSONDecodeError as e:
            rep.add(FAIL, "P12", f"invalid JSON: {e}", f.name)
            continue
        for key in EVAL_KEYS:
            if key not in data:
                rep.add(FAIL, "P12", f"missing key '{key}'", f.name)
        if data.get("skills") != ["pnm-delivery-architect"]:
            rep.add(FAIL, "P12", "skills must be [\"pnm-delivery-architect\"]", f.name)
        for key in ("expected_behavior", "must_not"):
            if key in data and (not isinstance(data[key], list) or not data[key]):
                rep.add(FAIL, "P12", f"'{key}' must be a non-empty list", f.name)
        fixture = data.get("fixture")
        if fixture and fixture != "none" and not (ev_dir / "fixtures" / fixture).is_file():
            rep.add(FAIL, "P12", f"fixture not found: fixtures/{fixture}", f.name)
    facts["evaluation_count"] = len(files)
    wanted = set(range(1, EXPECTED_EVALS + 1))
    if set(numbers) != wanted or len(numbers) != len(set(numbers)):
        missing = sorted(wanted - set(numbers))
        rep.add(FAIL, "P12", f"evaluations must be numbered 01–{EXPECTED_EVALS} once each"
                             + (f" (missing: {', '.join(f'{n:02d}' for n in missing)})" if missing else ""))
    else:
        rep.ok("P12", f"{EXPECTED_EVALS} evaluations, all with fixtures and rubric keys")


def check_scenarios(lib: pathlib.Path, skill_dir: pathlib.Path, rep: Report, facts: dict) -> None:
    if not lib.is_file():
        rep.add(FAIL, "P04", "scenario library missing", lib.name)
        return
    text = read(lib)
    ids = re.findall(r"^\|\s*([A-Z]{2}-\d{2})\s*\|", text, re.M)
    domains = re.findall(r"^##\s+\d+\.\s+\S", text, re.M)
    facts["scenario_count"] = len(ids)
    facts["domain_count"] = len(domains)
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    for d in dupes:
        rep.add(FAIL, "P04", f"duplicate scenario ID {d}", lib.name)
    if len(domains) != EXPECTED_DOMAINS:
        rep.add(FAIL, "P04", f"{len(domains)} domains in the index; {EXPECTED_DOMAINS} expected", lib.name)

    # Every live claim of "N scenarios" / "N domains" must match the index.
    for src in [skill_dir / "SKILL.md", *sorted((skill_dir / "references").glob("*.md"))]:
        body = before_version_history(read(src))
        for cm in re.finditer(r"\b(\d{2,3})\s+scenarios\b", body):
            if int(cm.group(1)) != len(ids):
                rep.add(FAIL, "P04", f"claims {cm.group(1)} scenarios; the index holds {len(ids)}",
                        f"{src.name}:{line_of(body, cm.start())}")
        for cm in re.finditer(r"\b(\d{1,2})\s+(?:lifecycle\s+)?domains\b", body):
            if int(cm.group(1)) != len(domains):
                rep.add(FAIL, "P04", f"claims {cm.group(1)} domains; the index holds {len(domains)}",
                        f"{src.name}:{line_of(body, cm.start())}")
    if not dupes:
        rep.ok("P04", f"scenario index: {len(ids)} unique IDs across {len(domains)} domains")

    # Cards live in the library and in references/scenario-cards-*.md. Each carries
    # exact evidence, not only a basis code, and the evidence must fit the basis.
    card_files = [lib, *sorted(lib.parent.glob("scenario-cards-*.md"))]
    seen: list[str] = []
    for cf in card_files:
        ctext = read(cf)
        cards = list(re.finditer(r"^###\s+([A-Z]{2}-\d{2})\s+·", ctext, re.M))
        for i, cm in enumerate(cards):
            cid = cm.group(1)
            seen.append(cid)
            block = ctext[cm.start(): cards[i + 1].start() if i + 1 < len(cards) else len(ctext)]
            ev = re.search(r"^\*\*Evidence:\*\*\s*(.+)$", block, re.M)
            basis = re.search(r"^\*\*Basis:\*\*\s*(.+)$", block, re.M)
            if not ev or not re.search(r"\bS\d{1,2}\b|\bCS-\d\b|§|clause|page", ev.group(1)):
                rep.add(FAIL, "P04", f"card {cid} has no exact evidence reference", cf.name)
            elif basis:
                codes = set(re.findall(r"\b([PRF])\b", basis.group(1)))
                if "F" in codes and not re.search(r"\bCS-\d\b", ev.group(1)):
                    rep.add(FAIL, "P04", f"card {cid} has Basis F but no CS evidence code", cf.name)
                if codes & {"P", "R"} and not re.search(r"\bS\d{1,2}\b", ev.group(1)):
                    rep.add(FAIL, "P04", f"card {cid} has Basis P/R but no S source", cf.name)
            if not basis:
                rep.add(FAIL, "P04", f"card {cid} has no Basis line", cf.name)
            if cid not in ids:
                rep.add(FAIL, "P04", f"card {cid} is not in the index", cf.name)
    facts["card_count"] = len(seen)
    for d in sorted({c for c in seen if seen.count(c) > 1}):
        rep.add(FAIL, "P04", f"scenario {d} has more than one card")
    missing_cards = [i for i in ids if i not in seen]
    if missing_cards:
        rep.add(WARN, "P04", f"{len(set(seen))} of {len(ids)} scenario cards authored — release gate requires all "
                             f"(missing: {', '.join(missing_cards[:8])}{'…' if len(missing_cards) > 8 else ''})")
    elif ids:
        rep.ok("P04", f"all {len(ids)} scenarios have a card with exact evidence across {len(card_files)} file(s)")


def check_patterns(acs: pathlib.Path, rep: Report, facts: dict) -> None:
    if not acs.is_file():
        rep.add(FAIL, "P05", "AC pattern library missing")
        return
    letters = sorted(set(re.findall(r"^#+\s*Pattern ([A-Z])\b", read(acs), re.M)))
    facts["ac_patterns"] = letters
    missing = [p for p in PATTERNS_REQUIRED if p not in letters]
    if missing:
        rep.add(FAIL, "P05", f"AC patterns not defined: {', '.join(missing)}", acs.name)
    else:
        rep.ok("P05", f"AC patterns defined: {letters[0]}–{letters[-1]}")


def check_badges(skill_dir: pathlib.Path, rep: Report, facts: dict) -> None:
    lists = {}
    for f in [skill_dir / "SKILL.md", *sorted((skill_dir / "references").glob("*.md"))]:
        for bm in re.finditer(r"\*\*Badges\*\*\s*—\s*one of:(.*)$", read(f), re.M):
            lists[f.name] = tuple(re.findall(r"`([A-Za-z]{2,12})`", bm.group(1)))
    facts["badge_lists"] = {k: list(v) for k, v in lists.items()}
    if not lists:
        rep.add(FAIL, "P06", "no authorised badge list found")
        return
    if len(set(lists.values())) > 1:
        rep.add(FAIL, "P06", f"badge lists disagree across files: {sorted(lists)}")
    else:
        rep.ok("P06", f"badge list consistent across {len(lists)} file(s): {', '.join(next(iter(lists.values())))}")
    primer = skill_dir / "references" / "slds2-pnm-primer.md"
    if primer.is_file():
        styled = {s.lower() for s in re.findall(r"\.pnm-badge\.([a-z0-9]+)", read(primer))}
        for b in sorted({b.lower() for b in next(iter(lists.values()))} - styled):
            rep.add(FAIL, "P06", f"badge '{b}' is authorised but has no style in the primer", primer.name)


def check_rule_file(rule_file: pathlib.Path | None, rep: Report) -> None:
    if not rule_file or not rule_file.is_file():
        rep.add(WARN, "P09", "trigger rule not found next to the skill")
        return
    text = read(rule_file)
    if "pnm-delivery-architect/SKILL.md" not in text:
        rep.add(FAIL, "P09", "trigger rule does not point at the skill's SKILL.md", rule_file.name)
    else:
        rep.ok("P09", "trigger rule points at the skill")


def check_dates(skill_dir: pathlib.Path, rep: Report, facts: dict) -> None:
    today = dt.date.today()
    dated = 0
    for src in [skill_dir / "SKILL.md", *sorted((skill_dir / "references").glob("*.md"))]:
        body = before_version_history(read(src))
        notes = r"(?:[Vv]erified|checked)[^\n]{0,80}?(\d{4}-\d{2}-\d{2})"
        register_rows = r"^\|\s*S\d{1,2}\s*\|.*\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*$"
        for vm in re.finditer(f"{notes}|{register_rows}", body, re.M):
            dated += 1
            try:
                age = (today - dt.date.fromisoformat(vm.group(1) or vm.group(2))).days
            except ValueError:
                continue
            if age > STALE_AFTER_DAYS:
                rep.add(WARN, "P07", f"verification is {age} days old — re-check against current docs",
                        f"{src.name}:{line_of(body, vm.start())}")
    facts["dated_verifications"] = dated
    if dated < 5:
        rep.add(WARN, "P07", f"only {dated} dated verification note(s) — product claims cannot be re-audited")
    else:
        rep.ok("P07", f"{dated} dated verification note(s)")


# ------------------------------------------------------------- neutrality ----

def load_baseline(skill_dir: pathlib.Path) -> dict:
    path = skill_dir / "tools" / "neutrality-baseline.json"
    return json.loads(read(path)) if path.is_file() else {"rules": [], "allow": []}


def load_denylist(path: pathlib.Path | None) -> list[str]:
    candidates = [path] if path else []
    env = os.environ.get("PNM_NEUTRALITY_DENYLIST")
    if env:
        candidates.append(pathlib.Path(env))
    terms: list[str] = []
    for c in candidates:
        if c and c.is_file():
            terms += [t.strip() for t in read(c).splitlines() if t.strip() and not t.startswith("#")]
    return terms


def scan_text(text: str, where: str, baseline: dict, denylist: list[str], rep: Report,
              level_override: str | None = None, deny_code: str = "N10") -> int:
    allow = [re.compile(a) for a in baseline.get("allow", [])]
    hits = 0
    for rule in baseline.get("rules", []):
        for m in re.finditer(rule["pattern"], text):
            if any(a.search(m.group(0)) for a in allow):
                continue
            hits += 1
            rep.add(level_override or rule["level"], rule["id"], f"{rule['label']}: '{m.group(0)}' — {rule['why']}",
                    f"{where}:{line_of(text, m.start())}")
    for term in denylist:
        for m in re.finditer(rf"(?<![A-Za-z0-9]){re.escape(term)}(?![A-Za-z0-9])", text, re.I):
            hits += 1
            rep.add(FAIL, deny_code, f"denylisted organisation term '{m.group(0)}'", f"{where}:{line_of(text, m.start())}")
    return hits


def check_neutrality(skill_dir: pathlib.Path, rule_file: pathlib.Path | None, denylist: list[str],
                     rep: Report) -> None:
    baseline = load_baseline(skill_dir)
    if not baseline.get("rules"):
        rep.add(FAIL, "N00", "neutrality baseline missing or empty")
        return
    files = package_files(skill_dir, rule_file)
    hits = sum(scan_text(read(f), f.name, baseline, denylist, rep) for f in files)
    if not hits:
        extra = f" + {len(denylist)} denylist term(s)" if denylist else " (no denylist supplied)"
        rep.ok("N00", f"{len(files)} package file(s) clean against {len(baseline['rules'])} baseline rule(s){extra}")


# --------------------------------------------------------------- artifacts ----

GENERIC_PERSONA = re.compile(
    r"\bas an?(?:\*\*)?\s+(?:the\s+)?(?:user|business user|developer|admin|administrator|system)\b(?!\s+[A-Z])", re.I)
# "Provider" alone is the subject trap; "Provider Data Specialist" is a role archetype.
PROVIDER_PERSONA = re.compile(
    r"^\s*\*\*As an?\*\*\s+(?:provider|practitioner|group|facility)\s*,?\s*$", re.I | re.M)
GWT_LINE = re.compile(r"^\s*(?:\*\*)?(Given|When|Then|And)(?:\*\*)?\s+(.*)$")
IMPL_IN_AC = [
    (r"\b\w+__(?:c|r|mdt|e|x)\b", "custom API name"),
    (r"\b[A-Z][A-Za-z0-9]*(?:Service|Controller|Handler|Helper|Batch|Trigger|Selector|Queueable)\b", "Apex class name"),
    (r"\bSELECT\b.+\bFROM\b", "SOQL"),
    (r"\bStep\s*\d+\b", "step number"),
    (r"\bIntegration Procedure\b|\bDataRaptor\b|\bData Mapper\b", "OmniStudio component"),
    (r"\[(?:Product|Discovered|Adapter|Proposed|Assumed — confirm)\]", "provenance label"),
]
# "credentialed" describes a precondition (a credentialed practitioner), not credentialing scope.
A4_TRIGGER = re.compile(r"credential(?!ed\b)|committee|delegat|sanction|monitoring|terminat", re.I)


def section_index(text: str, title: str) -> int:
    m = re.search(rf"^##\s+{re.escape(title)}\b", text, re.M | re.I)
    return m.start() if m else -1


def section_body(text: str, title: str) -> str:
    start = section_index(text, title)
    if start < 0:
        return ""
    nxt = re.search(r"^##\s+\S", text[start + 3:], re.M)
    return text[start: start + 3 + nxt.start()] if nxt else text[start:]


def lint_story(path: pathlib.Path, rep: Report, baseline: dict, denylist: list[str]) -> None:
    text = read(path)
    loc = path.name
    plan_mode = bool(re.search(r"^#\s*Solution Plan\b", text, re.M))

    if not re.search(r"^\*\*(?:Persona|Primary persona):\*\*\s*\S", text, re.M):
        rep.add(FAIL, "A01", "missing **Persona:** header", loc)
    if GENERIC_PERSONA.search(text) or PROVIDER_PERSONA.search(text):
        rep.add(FAIL, "A02", "generic or subject persona — use a role archetype (portal stories excepted)", loc)
    if section_index(text, "Org Discovery Context") < 0:
        rep.add(FAIL, "A03", "no Org Discovery Context section (A-1)", loc)
    if not re.search(r"Estimated Effort", text):
        rep.add(FAIL, "A04", "no Estimated Effort section", loc)

    for m in re.finditer(r"^\|.*\betc\.?(?:\s|\|).*$", text, re.M | re.I):
        rep.add(FAIL, "A05", "'etc.' inside a table — Pattern E requires every field enumerated",
                f"{loc}:{line_of(text, m.start())}")

    for i, line in enumerate(text.splitlines(), 1):
        gm = GWT_LINE.match(line)
        if not gm:
            continue
        for pat, label in IMPL_IN_AC:
            if re.search(pat, gm.group(2)):
                rep.add(FAIL, "A06", f"{label} inside a Given/When/Then line", f"{loc}:{i}")
                break

    if not plan_mode:
        ac, ti = section_index(text, "Acceptance Criteria"), section_index(text, "Technical Implementation")
        if ac < 0:
            rep.add(FAIL, "A07", "no Acceptance Criteria section", loc)
        if ti < 0:
            rep.add(FAIL, "A07", "no Technical Implementation section", loc)
        elif ac >= 0 and ti < ac:
            rep.add(FAIL, "A07", "Technical Implementation appears before the Acceptance Criteria", loc)
        if ti >= 0 and not any(p in section_body(text, "Technical Implementation") for p in PROVENANCE):
            rep.add(FAIL, "A08", "Technical Implementation carries no provenance labels", loc)
        if A4_TRIGGER.search(section_body(text, "Story") + section_body(text, "Acceptance Criteria")) \
                and section_index(text, "Compliance & Audit") < 0:
            rep.add(FAIL, "A09", "credentialing, committee, delegation, monitoring or termination scope "
                                 "without a Compliance & Audit section (A-4)", loc)

    odc = section_body(text, "Org Discovery Context")
    if odc and not any(p in odc for p in PROVENANCE):
        rep.add(FAIL, "A08", "Org Discovery Context rows carry no provenance labels", loc)

    if denylist:
        scan_text(text, loc, {"rules": [], "allow": []}, denylist, rep, deny_code="A10")


def lint_prototype(path: pathlib.Path, rep: Report, denylist: list[str]) -> None:
    raw = read(path)
    loc = path.name
    body = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    markup = re.sub(r"<(style|script)\b.*?</\1>", "", body, flags=re.S | re.I)

    checks = {
        "SLDS 2 root token block": ":root" in body and "--slds-g-" in body,
        "build-technology banner": re.search(r'class="[^"]*\bpnm-build-banner\b', markup) is not None,
        "component legend": re.search(r'class="[^"]*\bpnm-legend\b', markup) is not None,
        "badged elements (at least three)": len(re.findall(r'class="[^"]*\bpnm-badge\b', markup)) >= 3,
        "no hard-coded font sizes": not re.search(r"font-size:\s*\d+px", body),
    }
    for desc, passed in checks.items():
        if not passed:
            rep.add(FAIL, "A20", f"prototype fails: {desc}", loc)
    declared = re.search(r"passed:\s*(\d+)\s*/\s*(\d+)", raw[:6000])
    if not declared:
        rep.add(FAIL, "A21", "no 'passed: X / 10' self-check comment", loc)
    elif int(declared.group(1)) == int(declared.group(2)) and not all(checks.values()):
        rep.add(FAIL, "A21", "self-check claims a clean score but mechanical checks fail", loc)
    if denylist:
        scan_text(markup, loc, {"rules": [], "allow": []}, denylist, rep, deny_code="A10")


# ------------------------------------------------------------------- main ----

def main() -> int:
    here = pathlib.Path(__file__).resolve().parent.parent
    ap = argparse.ArgumentParser(description="Validate the PNM Delivery Architect package and artifacts.")
    ap.add_argument("--skill", type=pathlib.Path, default=here, help="skill directory (default: this script's parent)")
    ap.add_argument("--rule", type=pathlib.Path, default=None, help="trigger rule file (default: ../../rules/)")
    ap.add_argument("--denylist", type=pathlib.Path, default=None,
                    help="optional file of organisation terms, one per line (or env PNM_NEUTRALITY_DENYLIST)")
    ap.add_argument("--artifacts", type=pathlib.Path, nargs="*", default=[], help="stories/plans (.md), prototypes (.html)")
    ap.add_argument("--strict", action="store_true", help="treat WARN as failure")
    ap.add_argument("--json", action="store_true", dest="as_json")
    args = ap.parse_args()

    skill = args.skill.resolve()
    rule = args.rule or skill.parent.parent / "rules" / "use-pnm-delivery-architect.mdc"
    denylist = load_denylist(args.denylist)

    rep = Report()
    facts = check_package(skill, rule, rep)
    check_neutrality(skill, rule, denylist, rep)
    baseline = load_baseline(skill)
    for p in args.artifacts:
        if not p.is_file():
            rep.add(WARN, "A00", "artifact not found", str(p))
        elif p.suffix.lower() == ".html":
            lint_prototype(p, rep, denylist)
        else:
            lint_story(p, rep, baseline, denylist)

    counts = rep.counts()
    if args.as_json:
        print(json.dumps({"facts": facts, "counts": counts, "findings": [f.__dict__ for f in rep.findings]}, indent=2))
    else:
        for prefix, label in (("P", "PACKAGE"), ("N", "NEUTRALITY"), ("A", "ARTIFACT")):
            rows = [f for f in rep.findings if f.code.startswith(prefix)]
            if rows:
                print(f"\n{label}")
                for f in rows:
                    mark = {FAIL: "FAIL", WARN: "warn", INFO: "  ok"}[f.level]
                    print(f"  {mark}  {f.code}  {f.message}" + (f"  [{f.where}]" if f.where else ""))
        print(f"\n{counts[FAIL]} fail · {counts[WARN]} warn · {counts[INFO]} ok")
    return 1 if counts[FAIL] or (args.strict and counts[WARN]) else 0


if __name__ == "__main__":
    sys.exit(main())
