# SLDS 2 + Cosmos Primer for PNM Prototypes

The styling contract for every grounded HTML prototype this skill produces
(SKILL.md §Prototype contract). A prototype uses the hooks, utilities and
recipes in this file — not generic web CSS, not SLDS 1 and not invented class
names — and then adds the PNM build-technology overlay (§8) that labels every
element with the Salesforce technology that will implement it.

**Scope.** Enough to hand-author a Salesforce-looking single-file HTML
walkthrough for a product owner. Not covered: LWC mechanics, full WCAG
conformance testing, dark mode, the complete icon library.

## Contents

1. File skeleton and root tokens
2. Colour rules
3. Spacing
4. Utility classes
5. SLDS building blocks
6. Icons
7. Component styles
8. PNM build-technology overlay — badges, banner, legend, provenance
9. PNM blueprints B1–B12
10. Ten-point self-check
11. What deliberately is not here
12. Provenance and update policy

---

## 1. File skeleton and root tokens

Every prototype is one self-contained file: the self-check comment, the
`:root` token block, the styles it uses, then SLDS 2 markup. No CDN, no
external stylesheet — product owners open, email and archive the file.

```html
<!--
  PNM prototype self-check (slds2-pnm-primer §10)
  passed: 10 / 10
  primer: v1.1
  notes:  none
-->
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<title><Capability> — PNM Prototype</title>
<style>
  :root {
    /* Surface (85 %) */
    --slds-g-color-surface-1: #ffffff;
    --slds-g-color-surface-2: #f3f3f3;
    --slds-g-color-surface-3: #e5e5e5;
    --slds-g-color-surface-container-1: #ffffff;
    --slds-g-color-surface-container-2: #f3f3f3;
    --slds-g-color-on-surface-1: #747474;
    --slds-g-color-on-surface-2: #181818;
    --slds-g-color-on-surface-3: #080707;
    /* Accent (5 %) */
    --slds-g-color-accent-1: #0176d3;
    --slds-g-color-accent-2: #014486;
    --slds-g-color-accent-container-1: #0176d3;
    --slds-g-color-on-accent-1: #ffffff;
    /* Feedback */
    --slds-g-color-success-1: #2e844a;
    --slds-g-color-on-success-1: #ffffff;
    --slds-g-color-warning-1: #fe9339;
    --slds-g-color-on-warning-1: #080707;
    --slds-g-color-error-1: #ba0517;
    --slds-g-color-on-error-1: #ffffff;
    /* Border */
    --slds-g-color-border-1: #c9c9c9;
    --slds-g-color-border-2: #aeaeae;
    /* Spacing (4-point grid) */
    --slds-g-spacing-1: 0.25rem;
    --slds-g-spacing-2: 0.5rem;
    --slds-g-spacing-3: 0.75rem;
    --slds-g-spacing-4: 1rem;
    --slds-g-spacing-5: 1.5rem;
    --slds-g-spacing-6: 2rem;
    --slds-g-spacing-8: 3rem;
    /* Typography */
    --slds-g-font-family-base: "Salesforce Sans", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --slds-g-font-size-base: 0.8125rem;
    --slds-g-font-scale-neg-2: 0.6875rem;
    --slds-g-font-scale-neg-1: 0.75rem;
    --slds-g-font-scale-1: 0.875rem;
    --slds-g-font-scale-2: 1rem;
    --slds-g-font-scale-4: 1.25rem;
    --slds-g-font-scale-6: 1.75rem;
    --slds-g-font-weight-4: 400;
    --slds-g-font-weight-5: 500;
    --slds-g-font-weight-7: 700;
    /* Radius, shadow, motion */
    --slds-g-radius-border-1: 0.125rem;
    --slds-g-radius-border-2: 0.25rem;
    --slds-g-radius-border-3: 0.5rem;
    --slds-g-radius-border-circle: 50%;
    --slds-g-shadow-1: 0 2px 4px rgba(0, 0, 0, 0.08);
    --slds-g-shadow-2: 0 2px 8px rgba(0, 0, 0, 0.16);
    --slds-g-duration-1: 150ms;
    /* PNM overlay tones (§8) */
    --pnm-tone-ootb: #2e844a;
    --pnm-tone-config: #0176d3;
    --pnm-tone-flow: #7f5cff;
    --pnm-tone-os: #b8256b;
    --pnm-tone-fc: #9b2fae;
    --pnm-tone-ip: #3c5b8b;
    --pnm-tone-dm: #06787a;
    --pnm-tone-lwc: #b95500;
    --pnm-tone-apex: #ba0517;
    --pnm-tone-dpe: #8c4b02;
    --pnm-tone-agentforce: #5a1ba9;
    --pnm-tone-ext: #514f4d;
  }
  html, body { margin: 0; padding: 0; }
  body {
    font-family: var(--slds-g-font-family-base);
    font-size: var(--slds-g-font-size-base);
    color: var(--slds-g-color-on-surface-2);
    background: var(--slds-g-color-surface-2);
    line-height: 1.4;
  }
  /* §4 utilities, §7 component styles and §8 overlay — paste only what is used */
</style>
</head>
<body>
  <!-- §6 icon sprite, then the §8 banner and legend, then the screen -->
</body>
</html>
```

The `--pnm-tone-*` variables are the only colours outside the `--slds-g-*`
family a prototype may use, and only inside the overlay (§8).

---

## 2. Colour rules (85 · 5 · 10)

| Share | Role | Hook family | PNM examples |
|---|---|---|---|
| 85 % | Surface, background, container | `--slds-g-color-surface-*`, `--slds-g-color-surface-container-*` | Page, cards, related lists, modals |
| 5 % | Accent — primary action, selected state | `--slds-g-color-accent-*` | "Submit for review", "Add network", active tab |
| 10 % | Feedback and data | `--slds-g-color-success-*`, `-warning-*`, `-error-*` | Verified tile, expiring licence, blocked validation |

Pair every surface with its on-surface colour: `surface-1`/`surface-2` with
`on-surface-2` for body text, `accent-1` with `on-accent-1`, `success-1`
with `on-success-1`, `error-1` with `on-error-1`. Numbered variants express
emphasis, not shade: `-1` low (captions), `-2` medium (body), `-3` high
(headings). There is no unnumbered form.

## 3. Spacing

| Hook | Value | Use |
|---|---|---|
| `--slds-g-spacing-1` | 0.25rem | Icon to label |
| `--slds-g-spacing-2` | 0.5rem | Between related items |
| `--slds-g-spacing-3` | 0.75rem | Compact padding |
| `--slds-g-spacing-4` | 1rem | Default padding and margin |
| `--slds-g-spacing-5` | 1.5rem | Between sections |
| `--slds-g-spacing-6` | 2rem | Between page regions |

Prefer the utility classes (§4); use the hooks in custom CSS.

## 4. Utility classes

Paste only the rules a prototype uses.

```css
.slds-grid { display: flex; flex-wrap: nowrap; }
.slds-wrap { flex-wrap: wrap; }
.slds-grid_vertical { display: flex; flex-direction: column; }
.slds-col { flex: 1 1 auto; min-width: 0; }
.slds-gutters > .slds-col { padding-left: var(--slds-g-spacing-3); padding-right: var(--slds-g-spacing-3); }
.slds-grid_align-spread { justify-content: space-between; }
.slds-grid_align-end { justify-content: flex-end; }
.slds-grid_vertical-align-center { align-items: center; }
.slds-size_1-of-1 { width: 100%; }
.slds-size_1-of-2 { width: 50%; }
.slds-size_1-of-3 { width: 33.333%; }
.slds-size_2-of-3 { width: 66.666%; }
.slds-size_1-of-4 { width: 25%; }
.slds-m-bottom_small { margin-bottom: var(--slds-g-spacing-3); }
.slds-m-bottom_medium { margin-bottom: var(--slds-g-spacing-4); }
.slds-m-top_medium { margin-top: var(--slds-g-spacing-4); }
.slds-m-right_x-small { margin-right: var(--slds-g-spacing-2); }
.slds-m-left_small { margin-left: var(--slds-g-spacing-3); }
.slds-p-around_small { padding: var(--slds-g-spacing-3); }
.slds-p-around_medium { padding: var(--slds-g-spacing-4); }
.slds-p-horizontal_medium { padding-left: var(--slds-g-spacing-4); padding-right: var(--slds-g-spacing-4); }
.slds-text-heading_small { font-size: var(--slds-g-font-scale-2); font-weight: var(--slds-g-font-weight-5); color: var(--slds-g-color-on-surface-3); }
.slds-text-heading_medium { font-size: var(--slds-g-font-scale-4); font-weight: var(--slds-g-font-weight-5); color: var(--slds-g-color-on-surface-3); }
.slds-text-body_small { font-size: var(--slds-g-font-scale-neg-1); color: var(--slds-g-color-on-surface-1); }
.slds-text-title { font-size: var(--slds-g-font-scale-neg-1); text-transform: uppercase; letter-spacing: 0.04em; color: var(--slds-g-color-on-surface-1); font-weight: var(--slds-g-font-weight-7); }
.slds-text-color_weak { color: var(--slds-g-color-on-surface-1); }
.slds-truncate { max-width: 100%; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.slds-assistive-text { position: absolute !important; margin: -1px !important; border: 0 !important; padding: 0 !important; width: 1px !important; height: 1px !important; overflow: hidden !important; clip: rect(0 0 0 0) !important; }
.slds-hide { display: none !important; }
```

## 5. SLDS building blocks

The blueprints in §9 compose these. Class names are SLDS 2; keep them.

| Block | Root markup |
|---|---|
| Global header | `<header class="slds-global-header">` with app name and running persona |
| Page header | `<header class="slds-page-header">` → `__row` → `__col-title` / `__col-actions` |
| Path | `<div class="slds-path"><ul class="slds-path__nav"><li class="slds-path__item slds-is-complete|slds-is-current|slds-is-incomplete">` |
| Tabs | `<div class="slds-tabs_default"><ul class="slds-tabs_default__nav" role="tablist">` |
| Card | `<article class="slds-card">` → `__header` / `__body` / `__footer` |
| Form element | `<div class="slds-form-element"><label class="slds-form-element__label">` + `__control` with `.slds-input`, `.slds-select`, `.slds-textarea` |
| Data table | `<table class="slds-table slds-table_bordered slds-table_cell-buffer">` |
| Buttons | `.slds-button` + `_brand` (primary) · `_neutral` (secondary) · `_destructive` |
| Modal | `<section role="dialog" class="slds-modal slds-fade-in-open">` + `.slds-backdrop` |
| Scoped notification | `<div class="slds-notify slds-notify_alert slds-theme_success|_warning|_error" role="alert">` |
| Vertical progress | `<ol class="slds-progress slds-progress_vertical">` with `.slds-progress__item` + `slds-is-completed|slds-is-active` |
| Badge (SLDS, for status) | `<span class="slds-badge">` — distinct from the PNM build badge |

## 6. Icons

Ship a small inline sprite. The glyphs are simplified placeholders; say so in
the banner.

```html
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="icon-provider" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4" fill="currentColor"/><path d="M4 21c0-4 4-7 8-7s8 3 8 7" fill="currentColor"/></symbol>
  <symbol id="icon-location" viewBox="0 0 24 24"><path d="M12 2a7 7 0 0 0-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 0 0-7-7z" fill="currentColor"/></symbol>
  <symbol id="icon-network" viewBox="0 0 24 24"><circle cx="5" cy="12" r="3" fill="currentColor"/><circle cx="19" cy="5" r="3" fill="currentColor"/><circle cx="19" cy="19" r="3" fill="currentColor"/><path d="M7.5 11l9-5M7.5 13l9 5" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="icon-credential" viewBox="0 0 24 24"><path d="M4 3h16v14l-8 4-8-4z" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8 10l3 3 5-5" fill="none" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="icon-contract" viewBox="0 0 24 24"><path d="M6 2h9l5 5v15H6z M14 2v6h6 M9 13h8 M9 17h8" fill="none" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="icon-case" viewBox="0 0 24 24"><path d="M3 7h18v13H3z M8 7V4h8v3" fill="none" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="icon-file" viewBox="0 0 24 24"><path d="M6 2h9l5 5v15H6z M14 2v6h6" fill="none" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="icon-history" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 7v5l3 3" fill="none" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="icon-search" viewBox="0 0 24 24"><circle cx="10" cy="10" r="6" fill="none" stroke="currentColor" stroke-width="2"/><path d="M15 15l6 6" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="icon-sync" viewBox="0 0 24 24"><path d="M4 12a8 8 0 0 1 14-5l2-2v6h-6l2-2a5 5 0 0 0-9 3z M20 12a8 8 0 0 1-14 5l-2 2v-6h6l-2 2a5 5 0 0 0 9-3z" fill="currentColor"/></symbol>
  <symbol id="icon-warning" viewBox="0 0 24 24"><path d="M12 3l10 18H2z M12 10v5 M12 17h.01" fill="none" stroke="currentColor" stroke-width="2"/></symbol>
  <symbol id="icon-user" viewBox="0 0 24 24"><circle cx="12" cy="8" r="4" fill="currentColor"/><path d="M4 20c0-4 4-6 8-6s8 2 8 6" fill="currentColor"/></symbol>
</svg>
```

| PNM noun | Icon | SLDS category it stands for |
|---|---|---|
| Practitioner, group, organisation | `#icon-provider` | standard:account / standard:avatar |
| Location, practice site | `#icon-location` | standard:location |
| Network, tier, participation | `#icon-network` | standard:hierarchy |
| Licence, certification, verification | `#icon-credential` | standard:entitlement |
| Contract, payment agreement | `#icon-contract` | standard:contract |
| Application, case, queue item | `#icon-case` | standard:case |
| Roster file, document | `#icon-file` | doctype:attachment |
| Field history, audit | `#icon-history` | utility:clock |
| Search | `#icon-search` | utility:search |
| Downstream sync | `#icon-sync` | utility:sync |
| Expiry, sanction, blocked rule | `#icon-warning` | utility:warning |
| Running persona | `#icon-user` | utility:user |

Every icon gets assistive text or an `aria-label`.

## 7. Component styles

```css
.slds-global-header { background: var(--slds-g-color-on-surface-3); color: var(--slds-g-color-on-accent-1);
  padding: var(--slds-g-spacing-2) var(--slds-g-spacing-4); display: flex; justify-content: space-between; align-items: center; }
.slds-button { display: inline-flex; align-items: center; justify-content: center; gap: var(--slds-g-spacing-1);
  border: 1px solid transparent; border-radius: var(--slds-g-radius-border-2); padding: 0 var(--slds-g-spacing-3);
  min-height: 2rem; font-family: inherit; font-size: var(--slds-g-font-scale-1); font-weight: var(--slds-g-font-weight-5);
  cursor: pointer; transition: background var(--slds-g-duration-1); }
.slds-button_brand { background: var(--slds-g-color-accent-1); color: var(--slds-g-color-on-accent-1); }
.slds-button_brand:hover { background: var(--slds-g-color-accent-2); }
.slds-button_neutral { background: var(--slds-g-color-surface-1); color: var(--slds-g-color-accent-1); border-color: var(--slds-g-color-border-2); }
.slds-button_destructive { background: var(--slds-g-color-error-1); color: var(--slds-g-color-on-error-1); }
.slds-card { background: var(--slds-g-color-surface-container-1); border: 1px solid var(--slds-g-color-border-1);
  border-radius: var(--slds-g-radius-border-2); box-shadow: var(--slds-g-shadow-1); margin-bottom: var(--slds-g-spacing-4); position: relative; }
.slds-card__header { padding: var(--slds-g-spacing-3) var(--slds-g-spacing-4); display: flex; align-items: center; justify-content: space-between; }
.slds-card__body { padding: 0 var(--slds-g-spacing-4) var(--slds-g-spacing-4); }
.slds-card__footer { padding: var(--slds-g-spacing-3) var(--slds-g-spacing-4); border-top: 1px solid var(--slds-g-color-border-1); text-align: center; }
.slds-page-header { background: var(--slds-g-color-surface-1); padding: var(--slds-g-spacing-4); border-bottom: 1px solid var(--slds-g-color-border-1); }
.slds-page-header__row { display: flex; align-items: center; justify-content: space-between; gap: var(--slds-g-spacing-4); }
.slds-path__nav { display: flex; list-style: none; margin: 0; padding: 0; gap: var(--slds-g-spacing-1); }
.slds-path__item { flex: 1 1 0; text-align: center; padding: var(--slds-g-spacing-2); background: var(--slds-g-color-surface-3);
  border-radius: var(--slds-g-radius-border-1); font-size: var(--slds-g-font-scale-neg-1); }
.slds-path__item.slds-is-complete { background: var(--slds-g-color-success-1); color: var(--slds-g-color-on-success-1); }
.slds-path__item.slds-is-current { background: var(--slds-g-color-accent-1); color: var(--slds-g-color-on-accent-1); font-weight: var(--slds-g-font-weight-5); }
.slds-tabs_default__nav { display: flex; list-style: none; margin: 0; padding: 0; border-bottom: 1px solid var(--slds-g-color-border-1); }
.slds-tabs_default__item { margin-right: var(--slds-g-spacing-4); padding: var(--slds-g-spacing-3) 0; color: var(--slds-g-color-on-surface-1); border-bottom: 2px solid transparent; }
.slds-tabs_default__item.slds-is-active { color: var(--slds-g-color-accent-1); border-bottom-color: var(--slds-g-color-accent-1); font-weight: var(--slds-g-font-weight-5); }
.slds-table { width: 100%; border-collapse: collapse; background: var(--slds-g-color-surface-1); font-size: var(--slds-g-font-scale-1); }
.slds-table th, .slds-table td { text-align: left; padding: var(--slds-g-spacing-2) var(--slds-g-spacing-3); border-bottom: 1px solid var(--slds-g-color-border-1); }
.slds-table thead th { background: var(--slds-g-color-surface-2); color: var(--slds-g-color-on-surface-1); font-weight: var(--slds-g-font-weight-7);
  text-transform: uppercase; letter-spacing: 0.04em; font-size: var(--slds-g-font-scale-neg-1); }
.slds-form-element { margin-bottom: var(--slds-g-spacing-3); }
.slds-form-element__label { display: block; font-size: var(--slds-g-font-scale-neg-1); color: var(--slds-g-color-on-surface-1); margin-bottom: var(--slds-g-spacing-1); }
.slds-input, .slds-select, .slds-textarea { width: 100%; box-sizing: border-box; padding: var(--slds-g-spacing-2) var(--slds-g-spacing-3);
  font: inherit; font-size: var(--slds-g-font-scale-1); color: var(--slds-g-color-on-surface-2); background: var(--slds-g-color-surface-1);
  border: 1px solid var(--slds-g-color-border-2); border-radius: var(--slds-g-radius-border-2); }
.slds-input:focus, .slds-select:focus { outline: 2px solid var(--slds-g-color-accent-1); outline-offset: 1px; }
.slds-notify_alert { padding: var(--slds-g-spacing-3) var(--slds-g-spacing-4); border-radius: var(--slds-g-radius-border-2); font-size: var(--slds-g-font-scale-1); margin-bottom: var(--slds-g-spacing-3); }
.slds-theme_success { background: var(--slds-g-color-success-1); color: var(--slds-g-color-on-success-1); }
.slds-theme_warning { background: var(--slds-g-color-warning-1); color: var(--slds-g-color-on-warning-1); }
.slds-theme_error { background: var(--slds-g-color-error-1); color: var(--slds-g-color-on-error-1); }
.slds-progress_vertical { list-style: none; margin: 0; padding: 0; }
.slds-progress__item { padding: var(--slds-g-spacing-2) var(--slds-g-spacing-3); border-left: 3px solid var(--slds-g-color-border-1); color: var(--slds-g-color-on-surface-1); }
.slds-progress__item.slds-is-completed { border-left-color: var(--slds-g-color-success-1); color: var(--slds-g-color-on-surface-2); }
.slds-progress__item.slds-is-active { border-left-color: var(--slds-g-color-accent-1); color: var(--slds-g-color-accent-1); font-weight: var(--slds-g-font-weight-5); }
.slds-badge { display: inline-block; padding: 0 var(--slds-g-spacing-2); border-radius: var(--slds-g-radius-border-3);
  background: var(--slds-g-color-surface-3); color: var(--slds-g-color-on-surface-2); font-size: var(--slds-g-font-scale-neg-1); }
.slds-modal { position: fixed; inset: 4rem 0 0 0; z-index: 9002; display: flex; justify-content: center; }
.slds-modal__container { background: var(--slds-g-color-surface-1); border-radius: var(--slds-g-radius-border-3); box-shadow: var(--slds-g-shadow-2);
  width: min(45rem, calc(100vw - 4rem)); max-height: calc(100vh - 8rem); display: flex; flex-direction: column; overflow: hidden; }
.slds-backdrop { position: fixed; inset: 0; background: rgba(0, 0, 0, 0.5); z-index: 9001; }
```

---

## 8. PNM build-technology overlay — badges, banner, legend, provenance

This layer is what makes a PNM prototype a delivery artifact rather than a
mockup: every interactive or data-bearing element names the technology that
will build it, and every custom element carries its provenance.

```css
.pnm-badge { display: inline-flex; align-items: center; margin-left: var(--slds-g-spacing-2); padding: 0 var(--slds-g-spacing-1);
  font-size: var(--slds-g-font-scale-neg-2); font-weight: var(--slds-g-font-weight-7); letter-spacing: 0.04em; text-transform: uppercase;
  border: 1px solid currentColor; border-radius: var(--slds-g-radius-border-1); background: var(--slds-g-color-surface-1); vertical-align: middle; }
.pnm-badge.ootb       { color: var(--pnm-tone-ootb); }
.pnm-badge.config     { color: var(--pnm-tone-config); }
.pnm-badge.flow       { color: var(--pnm-tone-flow); }
.pnm-badge.os         { color: var(--pnm-tone-os); }
.pnm-badge.fc         { color: var(--pnm-tone-fc); }
.pnm-badge.ip         { color: var(--pnm-tone-ip); }
.pnm-badge.dm         { color: var(--pnm-tone-dm); }
.pnm-badge.lwc        { color: var(--pnm-tone-lwc); }
.pnm-badge.apex       { color: var(--pnm-tone-apex); }
.pnm-badge.dpe        { color: var(--pnm-tone-dpe); }
.pnm-badge.agentforce { color: var(--pnm-tone-agentforce); }
.pnm-badge.ext        { color: var(--pnm-tone-ext); }
.pnm-prov { margin-left: var(--slds-g-spacing-1); font-size: var(--slds-g-font-scale-neg-2); color: var(--slds-g-color-on-surface-1); font-style: italic; }
.pnm-build-banner { background: var(--slds-g-color-accent-container-1); color: var(--slds-g-color-on-accent-1);
  padding: var(--slds-g-spacing-3) var(--slds-g-spacing-5); font-size: var(--slds-g-font-scale-1); }
.pnm-build-banner strong { font-weight: var(--slds-g-font-weight-7); }
.pnm-legend { display: flex; flex-wrap: wrap; gap: var(--slds-g-spacing-2); align-items: center; background: var(--slds-g-color-surface-1);
  padding: var(--slds-g-spacing-2) var(--slds-g-spacing-5); border-bottom: 1px solid var(--slds-g-color-border-1); font-size: var(--slds-g-font-scale-neg-1); }
.pnm-legend .pnm-badge { margin-left: 0; }
```

### Badge vocabulary

**Badges** — one of: `OOTB`, `Config`, `Flow`, `OS`, `FC`, `IP`, `DM`, `LWC`, `Apex`, `DPE`, `Agentforce`, `Ext`.

| Badge | Class | Meaning | PNM examples |
|---|---|---|---|
| OOTB | `pnm-badge ootb` | Shipped product capability, no change | PNM app record page; Network Participation component; Roster File Mapping UI; contract approval |
| Config | `pnm-badge config` | Declarative configuration | Dynamic Forms and Actions, list views, queues, validation rules, work guides, Path |
| Flow | `pnm-badge flow` | Screen, record-triggered, scheduled or orchestration Flow | Change-request wizard; reminder flow; go-live orchestration |
| OS | `pnm-badge os` | OmniScript (runtime per D-9) | Portal application; shipped Primary Source Verification OmniScript |
| FC | `pnm-badge fc` | FlexCard | Provider summary card |
| IP | `pnm-badge ip` | Integration Procedure | Server-side orchestration behind an OmniScript |
| DM | `pnm-badge dm` | Omnistudio Data Mapper | Read or write mapping behind an OmniScript |
| LWC | `pnm-badge lwc` | Custom Lightning Web Component | Build wizard stepper, participation grid, verification tiles |
| Apex | `pnm-badge apex` | Apex service, trigger or batch | Bulk activation; mass participation change |
| DPE | `pnm-badge dpe` | Data Processing Engine on Data 360 | Roster mapping and load |
| Agentforce | `pnm-badge agentforce` | Agentforce agent, topic or action | Contact-centre agent; proposed credentialing assistant |
| Ext | `pnm-badge ext` | External system or middleware | CAQH, NPI registry, data bank, address service, claims, warehouse |

A badge may carry a short qualifier after the code: `Flow · reminder`,
`Ext · address service`. A shipped product element shows its badge only; a
custom or proposed element also shows its provenance:

```html
<button class="slds-button slds-button_brand">Submit for review
  <span class="pnm-badge apex">Apex · bulk</span><span class="pnm-prov">[Proposed]</span></button>
```

### Banner and legend

Directly after `<body>` (and the sprite), before any screen chrome:

```html
<div class="pnm-build-banner">
  <strong>Build technology · Mixed</strong> — OOTB record page + Config list views + LWC participation grid + Apex bulk activation.
  Rejected: record-by-record Flow (file-scale volume — volume rule). Icons are simplified placeholders.
</div>
<div class="pnm-legend" aria-label="Component legend">
  <span class="pnm-badge ootb">OOTB</span> shipped
  <span class="pnm-badge config">Config</span> configuration
  <span class="pnm-badge lwc">LWC</span> custom component
  <span class="pnm-badge apex">Apex</span> custom service
  <span class="pnm-prov">[Proposed]</span> new in this design
</div>
```

The legend lists every badge used on the page and nothing else.

---

## 9. PNM blueprints B1–B12

Each blueprint uses product objects by default and `{discovered}`
placeholders otherwise. Status values are always `{status per D-5}` until
discovered. Data is fictitious. Copy, then adapt.

### B1 · Provider 360 record page
Header with identifiers and status; related lists for specialties, taxonomies,
identifier history, locations, networks, affiliations and field history.
Scenarios: IN-03, PD-01…PD-08.

```html
<header class="slds-page-header">
  <div class="slds-page-header__row">
    <div><p class="slds-text-title">Practitioner <span class="pnm-badge ootb">OOTB</span></p>
      <h1 class="slds-text-heading_medium">Dr. Jordan Example, MD</h1>
      <p class="slds-text-body_small">NPI 1234567893 · Tax ID ••••6789 · <span class="slds-badge">{status per D-5}</span></p></div>
    <div><button class="slds-button slds-button_neutral">Request change <span class="pnm-badge flow">Flow</span><span class="pnm-prov">[Proposed]</span></button></div>
  </div>
</header>
<div class="slds-grid slds-gutters slds-wrap slds-p-around_medium">
  <div class="slds-col slds-size_1-of-2"><article class="slds-card"><div class="slds-card__header"><h2 class="slds-text-heading_small">Specialties (2) <span class="pnm-badge ootb">OOTB</span></h2></div>
    <div class="slds-card__body"><table class="slds-table"><thead><tr><th>Specialty</th><th>Primary</th><th>Effective from</th><th>Effective to</th></tr></thead>
    <tbody><tr><td>Family Medicine</td><td>Yes</td><td>01 Jan 2025</td><td>—</td></tr></tbody></table></div></article></div>
  <div class="slds-col slds-size_1-of-2"><article class="slds-card"><div class="slds-card__header"><h2 class="slds-text-heading_small">NPI history <span class="pnm-badge ootb">OOTB</span></h2></div>
    <div class="slds-card__body"><!-- HealthcareProviderNpi rows: Npi, NpiType, EffectiveFrom, EffectiveTo --></div></article></div>
  <!-- Repeat for Taxonomies, Locations, Networks, Affiliations, Field history (B11) -->
</div>
```

### B2 · Build or change wizard with vertical stepper
Scenarios: IN-02, IN-03, PD-01, PD-05.

```html
<div class="slds-grid slds-p-around_medium">
  <div class="slds-col slds-size_1-of-4"><ol class="slds-progress slds-progress_vertical" aria-label="Build steps">
    <li class="slds-progress__item slds-is-completed">Type and specialty</li>
    <li class="slds-progress__item slds-is-completed">Identity and tax ID</li>
    <li class="slds-progress__item slds-is-active">Base networks</li>
    <li class="slds-progress__item">Child networks</li><li class="slds-progress__item">Tier</li>
    <li class="slds-progress__item">Affiliations</li><li class="slds-progress__item">Billing address</li>
    <li class="slds-progress__item">Service location and hours</li></ol>
    <span class="pnm-badge lwc">LWC · stepper</span><span class="pnm-prov">[Proposed]</span></div>
  <div class="slds-col slds-p-horizontal_medium"><article class="slds-card"><div class="slds-card__header"><h2 class="slds-text-heading_small">Base networks</h2></div>
    <div class="slds-card__body"><div class="slds-notify slds-notify_alert slds-theme_warning" role="alert">NPI missing — you can continue (warns).</div>
    <!-- B7 grid here --></div></article>
    <div class="slds-grid slds-grid_align-end"><button class="slds-button slds-button_neutral slds-m-right_x-small">Back</button>
      <button class="slds-button slds-button_brand">Save and continue <span class="pnm-badge apex">Apex</span><span class="pnm-prov">[Proposed]</span></button></div></div>
</div>
```

### B3 · Work-queue home with list views per queue
Scenarios: CR-01, PD-07, QC-01.

```html
<div class="slds-tabs_default slds-p-around_medium"><ul class="slds-tabs_default__nav" role="tablist">
  <li class="slds-tabs_default__item slds-is-active" role="tab">My open items</li>
  <li class="slds-tabs_default__item" role="tab">{Queue per D-6}</li>
  <li class="slds-tabs_default__item" role="tab">{Queue per D-6}</li></ul>
  <span class="pnm-badge config">Config · list views + queues</span>
  <table class="slds-table"><thead><tr><th>Subject</th><th>Provider</th><th>Due</th><th>Owner</th></tr></thead>
  <tbody><tr><td>Verify NPI</td><td>Dr. Jordan Example</td><td>24 Oct 2026</td><td>{queue}</td></tr></tbody></table></div>
```

### B4 · Verification tiles
Element → source → result → verified date. Scenarios: CR-02, CR-03, CR-04.

```html
<div class="slds-grid slds-gutters slds-wrap slds-p-around_medium">
  <div class="slds-col slds-size_1-of-3"><article class="slds-card"><div class="slds-card__header"><h2 class="slds-text-heading_small">State licence</h2>
    <span class="pnm-badge lwc">LWC · tile</span><span class="pnm-prov">[Proposed]</span></div>
    <div class="slds-card__body"><p>Source: state licensing board <span class="pnm-badge ext">Ext</span></p>
      <p><span class="slds-badge">Verified</span> · 18 Oct 2026 · expires 31 Mar 2028</p></div></article></div>
  <div class="slds-col slds-size_1-of-3"><article class="slds-card"><div class="slds-card__header"><h2 class="slds-text-heading_small">Malpractice history</h2></div>
    <div class="slds-card__body"><div class="slds-notify slds-notify_alert slds-theme_warning" role="alert">Query pending</div></div></article></div>
</div>
```

### B5 · Quality review with return-for-correction action
Scenarios: QC-01, QC-02.

```html
<article class="slds-card slds-m-top_medium"><div class="slds-card__header"><h2 class="slds-text-heading_small">Quality review</h2>
  <div><button class="slds-button slds-button_neutral slds-m-right_x-small">Return for correction <span class="pnm-badge flow">Flow · routing</span><span class="pnm-prov">[Proposed]</span></button>
  <button class="slds-button slds-button_brand">Complete review <span class="pnm-badge config">Config</span></button></div></div>
  <div class="slds-card__body"><div class="slds-form-element"><label class="slds-form-element__label" for="rr">Return reason</label>
  <select id="rr" class="slds-select"><option>{reason values per D-5}</option></select></div>
  <p class="slds-text-body_small">Returns to: {originating reviewer if configured per D-6}</p></div></article>
```

### B6 · Committee docket and decision capture
Scenarios: QC-04, RE-03.

```html
<article class="slds-card"><div class="slds-card__header"><h2 class="slds-text-heading_small">Committee docket — 12 Nov 2026 <span class="pnm-badge lwc">LWC</span><span class="pnm-prov">[Proposed]</span></h2></div>
  <div class="slds-card__body"><table class="slds-table"><thead><tr><th>Practitioner</th><th>Type</th><th>File</th><th>Decision</th></tr></thead>
  <tbody><tr><td>Dr. Jordan Example</td><td>Initial</td><td>Non-clean</td>
    <td><select class="slds-select" aria-label="Decision"><option>{decision values per D-5}</option></select></td></tr></tbody></table></div>
  <div class="slds-card__footer"><button class="slds-button slds-button_brand">Record decisions <span class="pnm-badge apex">Apex</span><span class="pnm-prov">[Proposed]</span></button></div></article>
```

### B7 · Network participation grid
Base and child networks, tier, effective dates, participation status.
Scenarios: NW-01…NW-03, NW-06, NW-08.

```html
<article class="slds-card"><div class="slds-card__header"><h2 class="slds-text-heading_small">Network participation <span class="pnm-badge lwc">LWC · grid</span><span class="pnm-prov">[Proposed]</span></h2>
  <button class="slds-button slds-button_neutral">Add rows</button></div>
  <div class="slds-card__body"><table class="slds-table"><thead><tr><th>Network</th><th>Parent network</th><th>Tier</th><th>Location</th><th>Effective from</th><th>Effective to</th><th>Panel</th><th>Status</th></tr></thead>
  <tbody><tr><td>Commercial PPO</td><td>—</td><td>Tier 1</td><td>Main St Clinic</td><td>01 Dec 2026</td><td>—</td><td>Open</td><td>{status per D-5}</td></tr>
    <tr><td>Narrow PPO</td><td>Commercial PPO</td><td>—</td><td>Main St Clinic</td><td>01 Dec 2026</td><td>—</td><td>Open</td><td>{status per D-5}</td></tr></tbody></table></div></article>
```

### B8 · Payment agreement and fee schedule table
Facility vs non-facility. Scenarios: CT-01…CT-03.

```html
<article class="slds-card"><div class="slds-card__header"><h2 class="slds-text-heading_small">Payment agreement — Standard care fee · Medicaid <span class="pnm-badge ootb">OOTB</span></h2></div>
  <div class="slds-card__body"><table class="slds-table"><thead><tr><th>Procedure</th><th>Description</th><th>Facility price</th><th>Non-facility price</th></tr></thead>
  <tbody><tr><td>99213</td><td>Office visit, established patient</td><td>$62.00</td><td>$88.00</td></tr></tbody></table></div></article>
```

### B9 · Roster upload portal page with case status
Scenarios: RO-01, RO-02, RO-03, DG-01.

```html
<article class="slds-card slds-p-around_medium"><div class="slds-card__header"><h2 class="slds-text-heading_small">Upload roster <span class="pnm-badge ootb">OOTB · Experience Cloud</span></h2></div>
  <div class="slds-card__body"><input class="slds-input" type="file" aria-label="Roster file" />
  <table class="slds-table slds-m-top_medium"><thead><tr><th>File</th><th>Stage</th><th>Status</th><th>Rows</th></tr></thead>
  <tbody><tr><td>roster_october.csv</td><td>Mapping</td><td>InReview</td><td>1,240</td></tr></tbody></table>
  <span class="pnm-badge dpe">DPE · Roster File Mapping</span></div></article>
```

### B10 · Provider search with filters
Scenarios: DS-01, DS-02.

```html
<div class="slds-grid slds-p-around_medium">
  <div class="slds-col slds-size_1-of-4"><div class="slds-form-element"><label class="slds-form-element__label" for="sp">Specialty</label><select id="sp" class="slds-select"><option>Family Medicine</option></select></div>
    <div class="slds-form-element"><label class="slds-form-element__label" for="an">Accepting new patients</label><select id="an" class="slds-select"><option>Yes</option></select></div>
    <span class="pnm-badge ootb">OOTB · Provider Search</span></div>
  <div class="slds-col slds-p-horizontal_medium"><input class="slds-input" placeholder="Search by name, NPI, tax ID or address" aria-label="Search" />
    <!-- result cards: name, specialty, location, networks, panel --></div>
</div>
```

### B11 · Change-history timeline
Scenarios: PD-08, CT-07.

```html
<article class="slds-card"><div class="slds-card__header"><h2 class="slds-text-heading_small">Change history <span class="pnm-badge lwc">LWC · timeline</span><span class="pnm-prov">[Proposed]</span></h2></div>
  <div class="slds-card__body"><ol class="slds-progress slds-progress_vertical">
    <li class="slds-progress__item slds-is-completed">18 Oct 2026 · Site phone changed · by Provider Data Specialist</li>
    <li class="slds-progress__item slds-is-completed">02 Oct 2026 · Primary specialty set · by integration</li></ol></div></article>
```

### B12 · Downstream sync status panel
Scenarios: OB-03, DS-03.

```html
<article class="slds-card"><div class="slds-card__header"><h2 class="slds-text-heading_small">Downstream sync <span class="pnm-badge ext">Ext · middleware</span></h2></div>
  <div class="slds-card__body"><table class="slds-table"><thead><tr><th>Consumer</th><th>Last sent</th><th>Result</th></tr></thead>
  <tbody><tr><td>{consumer per D-12}</td><td>20 Oct 2026 09:14</td><td><span class="slds-badge">Success</span></td></tr>
    <tr><td>Provider search index</td><td>20 Oct 2026 09:15</td><td><span class="slds-badge">Failure</span> <span class="pnm-badge ootb">OOTB · sync log</span></td></tr></tbody></table></div></article>
```

---

## 10. Ten-point self-check

Record the result in the comment at the top of the file as `passed: X / 10`.
Score honestly — a noted failure is acceptable; a false clean score is not.

| # | Contract point | Passed if… |
|---|---|---|
| 1 | Single self-contained file | No external stylesheet, script or font link |
| 2 | SLDS 2 styling | `:root` block with `--slds-g-*` hooks; colours, spacing and font sizes come from hooks or §4 utilities; no pixel font sizes |
| 3 | Banner and legend | `.pnm-build-banner` and `.pnm-legend` present before the screen |
| 4 | Every element badged | Every button, input, grid, card and action bar carries a `.pnm-badge` |
| 5 | Product vs config vs custom | OOTB, Config and custom badges are used truthfully |
| 6 | Provenance on custom elements | Every custom or proposed element has a `.pnm-prov` label |
| 7 | Matches the approved scope | Screens, fields and records match the plan, ACs and Pattern E |
| 8 | Verified or proposed names only | No invented component names; unresolved values shown as `{… per D-n}` |
| 9 | Realistic but fictitious data | No real provider, member or organisation data |
| 10 | Accessibility basics | Icons have assistive text; inputs have labels; colour is never the only signal |

The package validator checks points 2, 3 and 4 mechanically and rejects a
clean score when they fail.

## 11. What deliberately is not here

Full WCAG conformance testing, the SLDS linter, dark mode, LWC behaviour
(placeholders carry an `LWC` badge) and the full icon library.

## 12. Provenance and update policy

Hook names, utility classes and component class names follow the public
Salesforce Lightning Design System 2 documentation
([lightningdesignsystem.com](https://www.lightningdesignsystem.com/)) and the
Cosmos theme defaults. Snapshot 2026-10-20. Refresh when SLDS 2 publishes a
new major version; re-check any hook used here that the documentation no
longer lists.
