# P2 design — Scaffold binka-lab: app shell, design system, data layer, CI & deploy (2026-09-29)

**Parent:** [SHOWCASE_plan.md](SHOWCASE_plan.md) §4. **Consumes:** the P1 bundle contract
(`bundle/v1/`: manifest, parquet tables, text JSON, JSON Schemas, resolved `claims.json`).
**Feeds:** P3/P4, which only add module content and charts on top of this shell.

P2 builds everything **except the modules themselves**: the repo, the page skeleton for
the four acts, the design tokens, the chart kit, the claim and provenance components, the
typed data layer, CI and a gated production deploy on `lab.gridchyn.ai`. Exit criterion
(plan §4): **a "hello bundle" page renders the real manifest in production.**

---

## 1. Context that shapes the design

- **igor-web** (`gridchyn.ai`) is Astro 4, has light mode only, and uses a Distill-style
  editorial skin. It has a token set in `astro/src/styles/global.css` `:root` (bg `#FAF8F5`,
  petrol `--accent #1E4C5C`, crimson `--accent-warm #B8443A` reserved for *live/interactive*,
  Fraunces / Source Serif 4 / IBM Plex Sans / IBM Plex Mono), is hosted on Netlify from a
  `production` branch, and has en/de i18n.
- The zone `gridchyn.ai` is on **Cloudflare DNS**. It already holds the records
  of the operator's other services.
- The lab is a **sibling product** of igor-web. It should look like the same author (tokens,
  type, voice) while being denser and more app-like (dashboards, explorers). A visitor
  moving between `/algo` and the lab should feel continuity, not a theme change.

## 2. Stack

| Concern | Choice | Why |
|---|---|---|
| Framework | **Astro 5**, static output | Same mental model as igor-web; pages are HTML by default and JS only where a module is interactive. A new repo starts on the current major, and tokens are plain CSS, so no coupling to igor-web's version |
| Interactivity | **React 19 islands**, `client:visible` | Explorers hydrate only when scrolled into view; the 60-second layer ships no JS |
| Language | TypeScript `strict` | The bundle schema is typed end to end (§5.2) |
| Charts | **Own thin kit on `d3-scale` / `d3-shape` / `d3-array` + SVG in React** (§4) | The mark specs (rounded data-ends, 2px surface gaps, hover layer, table view) are easier to own than to fight a library's defaults. Observable Plot was considered and rejected for that reason |
| Parquet on pages | **`hyparquet`** (~10 KB, pure JS) | v0.1 tables are ≤ a few thousand rows. Reading and transforming in JS is instant, and a page doesn't pay for a WASM engine |
| SQL in the browser | **DuckDB-WASM, lazy, only on `/about/data`** (the data console, §5.4) | Serves the poke test: an expert can run each claim's verification SQL (P1 §6) against the same parquet. Kept off every other page because the engine is several MB |
| Content | **MDX in Astro content collections**, one file per module | Prose is authored (P1 §11); the collection schema enforces the P0 §3.2 outline fields |
| Fonts | **Fontsource**, self-hosted, same four families as igor-web | No third-party font request, preloadable subsets. Visually identical to igor-web's Google Fonts |
| Tests | Vitest (units) + **Playwright** (smoke, a11y, screenshots) | igor-web's `/algo` shipped without browser verification (its follow-ups note it). The lab doesn't repeat that |
| Hosting | **Cloudflare Pages** + Cloudflare Access (pre-launch) + Web Analytics (cookieless) | DNS is already there, Access gating is free and native, preview deploys per branch |

**Plan correction (D4):** "DuckDB-WASM over exported parquet" becomes *hyparquet for pages,
DuckDB-WASM for the data console only*. The P1 bundle format is unchanged; plan D4 is updated.

## 3. Repository layout

```
binka-lab/
  data/bundle/v1/            committed bundle from P1 (manifest, tables/, text/, schema/, claims.json)
  content/                   authored, public: narrative sources, claims.yaml, glossary.yaml, epics.yaml, …
  docs/                      planning docs (moved from binka at E9.P2.0), per-phase design/impl/summary
  src/
    content/modules/*.mdx    one MDX per module (collection schema in src/content/config.ts)
    pages/                   index, system, science, verdicts, operating-model, lessons, about/{index,data,manifest}
                             + verdicts/sd/[id].astro   (one public page per SD entry, from text/sd_entries.json)
    layouts/                 Base, Act
    components/
      shell/                 SiteHeader, ActNav, LensSwitch, ThemeToggle, Footer, Glossary tooltip
      module/                Module, Depth (60s / explore / method), LensNote, Handoff
      claim/                 Claim, ProvenanceChip, ProvenancePopover
      chart/                 the kit (§4)
    data/                    bundle loader, generated types, claim lookup (§5)
    styles/                  tokens.css, base.css, chart.css
  tools/
    scan.py                  vendored P1 scanner (stdlib-only)
    verify-bundle.mjs        manifest ↔ file hashes, schema major, dirty flag
    gen-types.mjs            JSON Schema → src/data/types.gen.ts
    check-tokens.mjs         token sync vs igor-web snapshot (§4.1)
    check-palette.mjs        OKLab validator over chart tokens, both modes (§4.2)
    remark-claims.mjs        unbound-number lint for MDX (§5.3)
  vendor/igor-web-tokens.css pinned snapshot of igor-web :root (source commit in header)
  tests/                     vitest units + playwright specs
  .github/workflows/ci.yml
  public/_headers, public/_redirects
```

## 4. Design system

### 4.1 Tokens

- `src/styles/tokens.css` = **igor-web `:root` tokens copied verbatim**, plus three additions:
  a **dark theme** (igor-web has none), **chart roles** (§4.2) and **app-density** spacing.
- `check-tokens.mjs` diffs the shared token names against `vendor/igor-web-tokens.css`. That
  is a pinned snapshot, refreshed by hand when igor-web changes, with the source commit in
  its header. CI fails on silent divergence. There is no shared npm package (SD-SC-03).
- **Dark theme** follows the artifact convention: `@media (prefers-color-scheme: dark)`
  guarded by `:root:not([data-theme="light"])`, repeated under `:root[data-theme="dark"]`.
  The toggle wins both ways. Dark surfaces: `--bg #17191A`, `--bg-deep #1F2224`, and ink/muted
  stepped for ≥ 4.5:1 body contrast. Petrol and crimson get their own dark steps rather than
  inversion.
- **Reading widths are inherited** (`38rem` / `56rem` / `72rem`), plus one lab-only width,
  `--col-app: 80rem`, for explorer panels (ledger, SD explorer, console).
- **Editorial furniture is reused by name** (`.lede`, `.aside`, `.pullquote`, `§` dividers)
  in Act prose. Explorers use a quieter UI register (Plex Sans, Plex Mono numerics).

### 4.2 Chart palette (validated 2026-09-29 with the dataviz validator, OKLab ΔE×100)

Categorical: fixed order, never cycled. Slot 1 is a chroma-lifted step of the site petrol,
and slot 2 is a clay derived from the warm accents.

| Slot | Hue | Light (on `#FAF8F5`) | Dark (on `#17191A`) |
|---|---|---|---|
| 1 | petrol | `#007A9E` | `#1591B8` |
| 2 | clay | `#C4622D` | `#CF6A34` |
| 3 | violet | `#6A4FB0` | `#8872D8` |
| 4 | green | `#3C8F4E` | `#2A7A3C` |
| 5 | ochre | `#D09A00` | `#BA8800` |
| 6 | rose | `#C2457A` | `#D2568C` |

Validator results:
- **Light:** every check PASSes on the adjacent pairlist (worst CVD ΔE 9.9, normal-vision
  ΔE 20.1). Contrast WARNs only for ochre (2.39:1), so the **relief rule** applies: ochre
  series always carry direct labels or the table view.
- **Dark:** every check PASSes (worst CVD 10.1, normal-vision 20.0, all ≥ 3:1).
- **All-pairs forms** (scatter, dot strips, small multiples in one frame) are capped at
  **2 series, petrol + clay** (all-pairs CVD ΔE 16.2 light / 18.2 dark). A third slot fails
  the normal-vision floor, so beyond two, facet or use "highlight one, gray the rest".

Roles built on the palette:

| Role | Encoding | Used for |
|---|---|---|
| **Binary contrast** | petrol vs clay | *causal* (petrol) vs *as built* (clay) in the leakage autopsy; val vs test; buy vs sell |
| **Diverging** | clay (−) ← neutral gray at 0 → petrol (+) | Sharpe / EV around zero: cost wall, ledger heat cells |
| **Sequential** | petrol ramp, light → dark, one hue | Magnitudes: cost, counts, $ per item |
| **Status (verdicts)** | Own reserved steps, **always glyph + label**: ✓ ADVANCE/GO, ✗ KILL/NO-GO, ⛔ NO-READING, ⏸ PAUSE | Ledger, timeline, gates. Never reused as a series color |
| **Live** | igor-web crimson `#B8443A`, pulse dot | **Nothing since E9-G0 Q6**: I.6 shows a dated snapshot, not a live feed (SD-SC-07). Crimson stays reserved, so igor-web's rule that crimson means live still holds |

Status steps and the diverging neutral are validated in P2 implementation by
`check-palette.mjs`, which runs in CI on every token change. A future token edit can't
quietly break colour-blind safety.

### 4.3 Chart kit (`src/components/chart/`)

The kit follows the dataviz method as written: form first, colour by job, thin marks,
hover by default, table view always, no dual axes, legend for ≥ 2 series plus direct
labels for ≤ 4, text in ink tokens and never the series colour.

| Component | Form | First user |
|---|---|---|
| `StatTile` | Hero number + qualifier + provenance chip; no plot | Front-door tiles |
| `LineChart` | Crosshair + tooltip | Cost-wall EV curve |
| `BarChart` | Grouped / diverging, 4px rounded data-ends at the baseline, 2px gaps | Leakage per-coin as-built vs causal |
| `DotStrip` | 1-D dots with a reference line (e.g. zero, null median) | Per-coin Sharpe; S3 null percentile (P4) |
| `Histogram` | Binned bars + marker line | Cost-wall per-trade gross return |
| `SmallMultiples` | Shared scales, one panel per coin | 9-coin views (never 9 colours) |
| `Timeline` | Swim lanes, epochs as bands, events as glyph marks | Program timeline, "how it was found" strip |
| `LedgerTable` | Filterable/sortable table, status cells with glyph + label | Verdict ledger, autorun items |
| `StepDiagram` | Static SVG with keyed steps, highlighted by scroll/click | Loop lifecycle (IV.15) |
| `Controls` | One filter row above the chart: `Toggle`, `Slider`, `Select` | Substrate toggle, cost slider |

Every chart component takes `claimIds` and a `table` prop, which provides two things:
- a **"Table" toggle** that renders the underlying rows accessibly;
- a **provenance chip** in the chart footer.

A chart can't be rendered without data provenance: the TypeScript props require it.

## 5. Data layer

### 5.1 Two paths, one source

- **Build time (static, no JS):** Astro reads `claims.json`, `text/*.json` and the manifest.
  Tiles, headlines, the ledger's initial state and every SD page are pre-rendered HTML.
- **Runtime (islands):** `loadTable(name)` fetches `/data/v1/<sha8>/tables/<name>.parquet`
  and decodes it with hyparquet into typed rows. The path includes the table's sha, so
  assets are immutable and cache forever (§7.3).

### 5.2 Typed contract

- `gen-types.mjs` turns `data/bundle/v1/schema/*.json` into `src/data/types.gen.ts`, run on
  `prebuild`. `loadTable<'leak_autopsy_coin'>()` returns `LeakAutopsyCoinRow[]`.
- The app declares `EXPECTED_BUNDLE_MAJOR = 1`. The build fails on a mismatch with
  `manifest.bundle_version`, on `binka_dirty: true`, or on any file whose sha256 ≠ manifest
  (`verify-bundle.mjs`).

### 5.3 Claims in prose: the "no unbound number" rule

- In MDX, a number the reader should believe is written as `<Claim id="C-E4-024-collapse"
  field="causal_strict_median" />`. That renders the formatted value, unit and chip.
- `remark-claims.mjs` flags any **decimal number, percentage, bps value, currency amount or
  Sharpe/AUC-like value** in MDX prose that is outside a `<Claim>`. An allow-list covers
  years, dates, epic/SD/section identifiers and small counting words in plain prose
  ("three depths"). In `release` builds a flag is an error; in dev it's a warning.
- *Amended at E9.P0.5 (P0 §15):* it flags any digit outside a `<Claim>` or a name (dates, section marks, ids
  that start with a capital letter, release tags, code, and a numbered part of a source such as "point 8"), as
  [`narrative.md`](../content/narrative.md) §1.1 does. An unbound count, such as a tile's, is a number too.
- It also checks that every referenced `id` exists in `claims.json` and, in release builds,
  has `status: verified`.
- This is the mechanical half of plan D6. The human half, P0 verification, still stands.

### 5.4 The data console (`/about/data`)

- It lists the manifest tables with row counts, tiers and schemas.
- It lazy-loads DuckDB-WASM, registers the parquet files, and offers:
  - each claim's verification SQL, prefilled, with a "Run" button that shows the value next
    to the claimed value;
  - a free SQL box.
- It is read-only and local. The data is already public, so nothing is sent anywhere.
- The provenance popover's "verify this" link deep-links here with the claim's query loaded.
  This is what makes the **poke test** (P0 §8) a 30-second click, not a trust exercise.

## 6. Page shell and module anatomy

### 6.1 Shell

- **Header:** wordmark "Binka Lab" · act nav (System · Science · Verdicts · Operating model ·
  Lessons) · lens switch · theme toggle.
- **Front door `/`:**
  - the spine sentence;
  - the timeline strip;
  - six `StatTile`s;
  - "Choose your path": three cards (IC / Lead / Manager), each a curated route through the
    acts with a stated reading time;
  - the cross-link to igor-web `/algo` ("the narrative version").
- **Act page:** act intro (the P0 §3.1 hand-off copy), a module list with depth indicators,
  then the modules in order, and a hand-off footer to the next act.
- **Lens:** a `?lens=ic|lead|manager` URL param, also remembered in `localStorage` wrapped
  in try/catch (a per-viewer convenience only). The lens reorders and reveals `LensNote`
  callouts; it never hides content. P2 builds the mechanism, and P5 fills the copy.

### 6.2 `<Module>`

```
┌ Module n · Title ───────────────────────────── [act anchor] ┐
│ Headline (≤ 15 words)                                        │  ← 60 s: static HTML
│ [the one figure / tile]                         ⓘ provenance │
│ ▸ Explore  — the interactive island (client:visible)          │  ← 5 min
│ ▸ Method   — deep write-up, caveats, excerpts, links          │  ← deep (disclosure)
│ LensNote (per active lens)                                    │
└ Hand-off to next module ───────────────────────────────────┘
```

The collection schema (`src/content/config.ts`) requires `id`, `act`, `title`, `headline`,
`claims[]`, `tables[]`, `lens.{ic,lead,manager}`, `release` (`v0.1` | `p4`). A module whose
`release` is later than the build target is excluded, so v0.1 can ship without P4 stubs.

### 6.3 The provenance chip and popover

- **Chip** (Plex Mono, muted, one line): `SD-E4-24 · 68c917e · fp 38dcdfdc`. It shows whichever
  of doc anchor / commit / fingerprint the claim has.
- **Popover:**
  - claim text, value and unit;
  - the **qualifier**, always shown;
  - its kind (recorded / recomputed / illustrative, with the illustrative badge);
  - the source doc and section (as text, since binka is private);
  - **a link to the public SD page** when the anchor is an SD entry
    (`/verdicts/sd/SD-E4-24`);
  - the commit SHA, the table name, and "Verify in data console →".

SD entries become first-class public pages, so most chips resolve **inside the site**.

## 7. CI, deploy, environments

### 7.1 CI (`.github/workflows/ci.yml`, on every push and PR)

| Job | Checks | Blocking |
|---|---|---|
| `bundle` | `verify-bundle.mjs` (hashes, schema major, not dirty) · `python tools/scan.py data/bundle` | yes |
| `static` | `tsc --noEmit`, eslint, prettier, `check-tokens`, `check-palette` | yes |
| `content` | `astro build` with `remark-claims` (release mode on `production`, dev mode on other branches) · content-collection schema | yes |
| `unit` | vitest: data loader, formatting, claim lookup, lens logic | yes |
| `e2e` | Playwright on the built site: every route 200, no console errors, islands hydrate, axe-core a11y (WCAG 2.2 AA) on each route, screenshots light/dark × 390 px/1440 px (as artifacts, not diffed in P2) | yes (except screenshots) |
| `links` | lychee over the built site (internal links hard-fail; external links warn) | internal only |
| `lighthouse` | Lighthouse CI against the Pages preview URL, with the budgets in §7.4 | warn in P2, block from P5 |

### 7.2 Branches and environments

It mirrors igor-web's habit:
- **`main`** → Cloudflare Pages *preview* (`<hash>.binka-lab.pages.dev`).
- **`production`** → **`lab.gridchyn.ai`**.

To ship: merge `main` → `production`.

**Pre-launch gate:** a Cloudflare Access application covers `lab.gridchyn.ai` **and**
`*.binka-lab.pages.dev`, using email one-time PIN with an allow-list of the operator plus
named reviewers (the 60-second testers). Removing the Access policy is the launch step in P3,
together with flipping the GitHub repo public.

DNS: `lab` CNAME → the Pages project (proxied), added in the existing `gridchyn.ai` zone.
It doesn't touch the Netlify apex records or the zone's other records.

### 7.3 Headers (`public/_headers`)

- `/_astro/*` and `/data/v1/*`: `Cache-Control: public, max-age=31536000, immutable`. They
  are content-addressed.
- HTML: short cache (`max-age=300, must-revalidate`).
- **CSP:** `default-src 'self'; script-src 'self' 'wasm-unsafe-eval'` (DuckDB-WASM on the
  console only); `connect-src 'self'` (no feed origin: since E9-G0 Q6, I.6 is a snapshot in the
  bundle, SD-SC-07); `img-src 'self' data:`; `frame-ancestors 'none'`. The Cloudflare Web
  Analytics beacon is added explicitly.
- `Referrer-Policy: strict-origin-when-cross-origin`, `X-Content-Type-Options: nosniff`.

### 7.4 Performance budgets

| Budget | Value |
|---|---|
| JS on a route before any island hydrates | ≤ 30 KB gz |
| Largest single island (excluding the console) | ≤ 90 KB gz |
| Parquet fetched per act | ≤ 4 MB (P1 §3.3), lazy on first explore |
| Fonts | ≤ 4 files preloaded, Latin subsets |
| First contentful paint (mid-range phone, 4G) | < 1.5 s (P0 §8) |
| Lighthouse (all four) | ≥ 95, blocking from P5 |

## 8. SEO and sharing basics (minimal in P2)

- Canonical URLs and `sitemap.xml` (excluding `/about/data`).
- A `robots.txt` that **disallows everything while Access is on**, flipped at launch.
- Per-page title and description; a single default OG image. Per-act generated OG images are P5.
- JSON-LD `CreativeWork` with author "Igor Gridchyn" linking to `gridchyn.ai`.

## 9. The "hello bundle" slice (P2's proof)

1. `/about/manifest` renders the manifest: bundle version, export date, binka commit, and a
   table list (name, tier, rows, sha8, release). Every row is fetched and decoded through
   `loadTable` in an island.
2. One `StatTile` on `/` bound to a real claim (for example `C-E5-screens`) with a working chip
   and popover.
3. `/about/data` runs one claim's verification SQL in DuckDB-WASM and shows it matching.
4. One SD page (`/verdicts/sd/SD-E4-24`) rendered from `text/sd_entries.json`.

If P1's full v0.1 export isn't ready when P2 starts, a **fixture bundle** built by the P1
exporter on its test fixtures stands in. The app only ever reads a real exporter's output,
never a hand-written mock.

## 10. Work steps

1. (E9.P2.0, the operator's setup card.) `git init ~/dev/binka-lab` and move the docs in from binka
   (SD-SC-06). Create the GitHub repo `binka-lab` (**private**) and push. Connect Cloudflare
   Pages. Create the Access app **before** the first deploy.
2. Astro 5 + React + TS strict + Fontsource scaffold; tokens.css (copy + dark + chart roles);
   `check-tokens`, `check-palette`.
3. Data layer: `verify-bundle`, `gen-types`, `loadTable`, claim lookup; vitest.
4. Shell: Base/Act layouts, header, act nav, theme toggle, lens mechanism, footer.
5. Claim + ProvenanceChip + popover; `remark-claims`; content-collection schema; one stub MDX
   module per v0.1 module (headline only, `release: v0.1`).
6. Chart kit: `StatTile`, `BarChart`, `LineChart`, `LedgerTable`, `Timeline` first (these are
   what v0.1 needs); the rest in P4 as needed. Each gets a table view and a hover layer.
7. `/about/manifest`, `/about/data` (DuckDB-WASM), the SD page route.
8. CI workflow, `_headers`, `robots.txt`, DNS `lab` CNAME; the first production deploy
   behind Access.
9. Playwright suite green; screenshots reviewed by eye (light/dark, phone/desktop).

## 11. Exit criteria

1. `https://lab.gridchyn.ai/about/manifest` (behind Access) shows the real (or P1-fixture)
   manifest, with every table decoded in the browser.
2. The front-door claim tile shows the correct value, and its chip → popover → "verify" →
   console reproduces the value.
3. CI is green on `production`: bundle verified, scanner clean, palette checks pass in both
   modes, a11y clean on every route, no console errors.
4. JS budget on `/` ≤ 30 KB gz measured. The theme toggle and OS dark mode both work, and
   the phone layout has no horizontal scroll at 390 px.
5. Nothing is reachable without Access: the preview and production URLs were checked from a
   logged-out browser.

## 12. Scope decisions and open points

Logged in SHOWCASE_scope_decisions.md:
- **SD-SC-02:** English only; igor-web's de locale is not mirrored.
- **SD-SC-03:** tokens are a vendored snapshot with a CI diff, not a shared package.

**Operator answers (2026-09-30):**
1. **Hosting split:** accepted. Cloudflare Pages for the lab; igor-web stays on Netlify.
2. **Analytics:** accepted. Cloudflare Web Analytics (cookieless).
3. **Wordmark:** "Binka Lab".

## 13. Amendments from E9-G0 (2026-10-15)

Applied by E9.P0.1 from [E9](E9_2026-10-15.md) §2 and §8. The rows are in-place fixes.

| Change | Why |
|---|---|
| The CSP's `connect-src` drops the feed origin (§7.3) | E9-G0 Q6: I.6 is a dated snapshot read from the bundle, with no polling; SD-SC-07 |
| The **Live** colour role has no user. Crimson stays reserved for "live" (§4.2) | E9-G0 Q6 |
| The repo is created and the docs moved in at E9.P2.0, the operator's setup card, not at P0 (§3, §10 step 1) | E9 §2 row 10; SD-SC-06 |
