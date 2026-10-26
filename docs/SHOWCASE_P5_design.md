# P5 design — Explainability & polish: v1.0 (2026-10-15)

**Parent:** [SHOWCASE_plan.md](SHOWCASE_plan.md) §4. **Builds on:** v0.9 (every P4 module shipped), the P2 shell
(the lens mechanism, theme toggle and CI) and the P0 glossary seed and lens lines. **Feeds:** P6 (distribution),
which needs a finished v1.0 to record, print and link to. **Program wrapper:** [E9](E9_2026-10-15.md) §5 P5.

P5 adds no modules and no numbers. It makes what P4 shipped **easier to understand** (glossary, lenses, tours) and
**sound for every reader and device** (mobile, a11y, dark mode, performance, sharing). It is done when the CI budgets
that warned until now block, and a manual audit finds nothing left to fix.

---

## 1. What ships

| Area | v1.0 deliverable | § |
|---|---|---|
| Glossary | A tooltip on the first use of each marked term in each module, plus a `/glossary` page | 2 |
| Lenses | All 21 modules × 3 lenses of "why it matters" copy, the act-page route markers, and the no-lens default | 3 |
| Guided tours | Three tours (IC · Lead · Manager), driven by the URL, with a tour bar | 4 |
| Mobile, a11y and dark mode | A full pass to a written checklist, axe + a manual keyboard and screen-reader audit, and visual regression on key pages | 5 |
| Performance | Lighthouse ≥ 95 on all four categories, **blocking**, on every route template | 6 |
| Sharing | Per-act and per-SD OG images generated at build time from claims | 7 |
| Small polish | A 404 page, copy-link anchors, an "as of" export date in the footer, and reduced motion | 8 |

v1.0 = this list on `production`. It is still a soft launch. The announcement is P6, after the human 60-second test.

## 2. Glossary tooltips

### 2.1 Data

`content/glossary.yaml` (P0 §7), extended:

```yaml
- id: psi
  term: PSI
  aliases: [population stability index]
  short: "How far a quantity's spread of values moved between two periods; large values mean the inputs changed."  # ≤ 20 words, no number
  long: "…"            # optional, shown on /glossary only
  link: /science#m10   # the module that explains it best
  acts: [II]           # where it appears (validated at build)
```

The seed's terms (P0 §7, with E6 and E7's added by E9.P0.1) grow with P4's modules: QLIKE, VRP, HAR-RV,
walk-forward fold, Optuna, freeze record, seal, NO-READING, skeptic, dossier, supervisor, guard hook, and so on.
Every `short` is written for the recruiter persona: no term in it may itself need a tooltip, and it holds no
number, since nothing in it is bound to a claim (narrative §1.1). The seed is binka's `glossary.yaml` (E9.P0.6).

### 2.2 Marking

P3 and P4 already mark terms in MDX: `<Term id="psi">PSI</Term>`. P5 adds a `remark-glossary` lint, not
auto-marking. Auto-marking would underline every "fold" and "seal" in running prose, so the marks stay authored, and
the lint checks them:
- every `id` exists in the glossary;
- the first use of a glossary term in each module is marked, and later uses aren't (a warning, not an error, since
  sometimes the first use sits in a heading);
- no glossary entry is unused (a warning, so orphans get cut).

### 2.3 Component

`<Term>` renders a `<button class="term" popovertarget="g-psi-m10">` with a dotted underline, and a
`<div popover id="g-psi-m10" role="tooltip">` holding `short` and "More in the glossary →".
- **Zero JS for tap, click and keyboard**, using the native Popover API: Enter or Space opens it, Esc closes it, and
  light-dismiss is built in.
- **Hover** (fine pointers only, `@media (hover: hover)`) opens it after 300 ms through one shared ≤ 2 KB script, and
  CSS anchor positioning places it. Where the browser lacks anchor positioning, it falls back to a fixed bottom sheet
  on phones and below the term on desktop.
- The button's accessible name is the term itself. The popover is linked with `aria-describedby` while it is open.
- In a chart's table view and inside `<Claim>` popovers, terms aren't marked (no nested popovers).

### 2.4 `/glossary`

One static page listing every term alphabetically, with `short` and `long`, a "where it's used" list of module links,
and a filter box built on the P4 `SearchIndex`. It is linked from the footer and from every tooltip.

## 3. The per-role lens

### 3.1 What exists

P2 §6.1 built the mechanism: `?lens=ic|lead|manager` beats `localStorage` (try/catch), which beats no lens. The lens
reorders and reveals `LensNote` callouts and never hides content. P0 wrote one draft line per module per lens. The
schema requires `lens.{ic,lead,manager}` on every module.

### 3.2 The copy (63 notes)

Each note answers *"why would someone hiring for this role care about this module?"*

| Rule | Why |
|---|---|
| ≤ 35 words, first person, one point | It sits under a module the reader has just read |
| Never restates the headline; says what it **shows about how I work** | The headline says what happened; the lens says why it matters |
| Numbers only through `<Claim>`, and at most one | The no-unbound-number rule (P2 §5.3) |
| IC: method and evidence. Lead: judgement, trade-offs, the team pattern. Manager: risk, cost, governance, delegation | The three P0 §2 personas |
| No superlatives, and no claims about the reader ("you'll love…") | Copy rules (P3 §2) |

Claude drafts all 63 notes in one item from the module text and P0's lines. The operator reviews a **sample of 9**
(one per act per lens, picked by the operator) and edits those. The rest follow the edited sample's pattern, and the
operator does a final skim.

### 3.3 Behaviour

- **No lens chosen:** each module shows a compact `Why it matters: IC · Lead · Manager` switcher, collapsed, with
  one click to expand. Choosing one sets the lens site-wide.
- **Lens chosen:** the `LensNote` for that lens shows expanded under each module, and the others are one click away.
  On act pages, the modules on that lens's tour (§4) get a small "on your path" marker in the module list. Nothing
  moves position: the "reordering" P2 described is limited to which note is expanded, so anchors and screenshots
  stay stable.
- **The header lens switch** shows the current lens and lets the reader clear it.
- The front door's three path cards set the lens and start the matching tour (§4).

### 3.4 Tests

Vitest: lens precedence (URL > storage > none) and storage failing safely. Playwright: lens persists across act
navigation, the URL wins over storage, the no-lens switcher works by keyboard, and axe passes in all four states.
A content lint checks the word counts and that every module has all three notes.

## 4. Guided tours

### 4.1 Model

A tour is **a route through module anchors**, not a coach-mark overlay. Overlays trap focus, fight screen readers and
break on phones. A tour stop is the module itself, with a tour bar.

`content/tours.yaml`:

```yaml
- id: lead
  title: "The tech lead's path"
  minutes: 12            # computed at build from word counts at 230 wpm + 20 s per figure; the authored value must match ±2
  stops:
    - {module: III.11, note: "Start with the shape of the program: each research epic ended at a gate I signed."}
    - {module: II.9,  note: "The story I'd tell in an interview: the agent found the leak, and the rules decided what happened next."}
    - …
```

| Tour | Stops (draft) | ≈ minutes |
|---|---|---|
| **IC / Staff** | II.9 Leakage autopsy → II.7 Cost wall → II.8 Bake-off → IV.17 Pre-registration as code → `/about/data` ("try to break a number") | 30 |
| **Lead** | III.11 Timeline & gates → II.9 Leakage autopsy → IV.15 Loop → IV.18 Case replays → III.13 SD explorer → `/lessons` | 12 |
| **Manager** | III.11 Timeline & gates → IV.16 Boundaries → IV.19 Throughput & compute → IV.20 Division of labour → III.12 Verdict ledger | 6 |

These extend P3 §3.1's three v0.1 paths to the full site. P3's paths stay as each tour's first stops, so links
already shared still work.

### 4.2 Tour bar

- State lives in the URL (`?tour=lead&stop=2`). It's shareable, survives reloads, and needs no storage.
- A sticky bottom bar, ≤ 56 px, shows `Lead path · 2 of 6 · ← Prev · Next → · ✕`. Its stop note shows above the
  module heading at the stop, not in the bar.
- Keyboard: the bar is a `<nav aria-label="Guided tour">` landmark with real links. No global shortcuts, which would
  collide with the replay player's ← →.
- The last stop offers the other two tours and the CV link.
- Leaving the route (any other link) ends the tour quietly. The bar never reappears unless a tour URL is opened.

### 4.3 Checks

At build: every stop's module exists and is released, the computed minutes match the authored ones, and each note is
≤ 25 words. Playwright walks each tour end to end at 390 px and 1440 px.

## 5. Mobile, accessibility and dark mode

### 5.1 The checklist (each row is a test or an audit line)

| # | Check | How |
|---|---|---|
| 1 | No horizontal page scroll at 320, 390, 768 and 1440 px on every route. Wide tables and charts scroll **inside** their frame, with a visible edge fade | Playwright (`scrollWidth ≤ clientWidth`) |
| 2 | Touch targets ≥ 24 × 24 px (WCAG 2.2 2.5.8), and ≥ 44 px for the tour bar, the lens switch and the replay controls | axe + a CSS lint on interactive classes |
| 3 | Every island is fully usable by keyboard: toggles, sliders (the II.9 shift scrubber), the replay player, search and the data console | Playwright keyboard scripts per island |
| 4 | Visible focus on every focusable element, in both themes (a 2 px outline at ≥ 3:1 against both surfaces) | the palette validator, extended to focus tokens |
| 5 | Every chart: an SVG `role="img"` with an `aria-label` built from its headline claim, a table view reachable by keyboard, and no information carried by colour alone (glyphs ✓ ✗ ⛔ ⏸ carry text equivalents) | axe + a component test |
| 6 | `prefers-reduced-motion`: the touch-label animation (I.3) shows its final frame, and scroll-linked effects become instant | Playwright with reduced motion emulated |
| 7 | I.6's feed snapshot is static: no polling and no live region, and its date is part of its accessible label (E9-G0 Q6, SD-SC-07) | component test |
| 8 | Headings: one `h1` per page and no skipped levels. Landmarks: header, nav, main, footer. A skip link. `lang="en"` | axe + a heading-outline test |
| 9 | Dark mode: every diagram is inline SVG on tokens (`currentColor`, CSS variables), so none is a raster with a baked-in background. Code excerpts use a dual Shiki theme | the visual regression below |
| 10 | Contrast ≥ 4.5:1 for body text and ≥ 3:1 for chart marks and UI, in both themes. Already validated for the palette (P2 §4.2); P5 extends the validator to every token pair actually used, not just the palette | `check-palette` extended |
| 11 | Zoom to 200 % and text spacing (WCAG 1.4.12) without loss: popovers reposition, and tables stay scrollable | manual |

### 5.2 Manual audit (one sitting, recorded in the P5 summary)

- A keyboard-only walk through every route, including each tour.
- A screen-reader spot check of one module per act plus the front door, with Orca + Firefox (Linux). VoiceOver on
  an iPhone for the front door and II.9 if a device is at hand.
- A real-phone pass: one Android and one iPhone if available, both themes, portrait and landscape.

Findings go in a table in the P5 summary. Each is fixed, or logged as an SD-SC entry with its reason.

### 5.3 Visual regression

P2 captured screenshots as artifacts without diffing them. P5 turns on Playwright `toHaveScreenshot` for **eight
pages** (`/`, the four act pages, `/lessons`, one SD page, `/glossary`) × light/dark × 390/1440 px, with a 0.2 %
pixel tolerance. The export date is masked. Only eight pages are covered because snapshot
upkeep across all ~200 pages (SD pages included) would cost more than the regressions it catches.

## 6. Performance: Lighthouse becomes blocking

P2 §7.4's budgets stand. P5 flips the `lighthouse` CI job from warn to **block**:
- **Where:** each route template: `/`, the four act pages, `/lessons`, `/glossary`, `/about`, `/about/manifest`,
  one SD page. `/about/data` is measured *before* the console is opened; its WASM loads only on demand.
- **How:** Lighthouse CI with mobile emulation (the default), the median of 3 runs, against the Pages preview URL.
- **Bar:** ≥ 95 on Performance, Accessibility, Best Practices and SEO, on every template.

The known risks, and the fixes planned for them:

| Risk | Fix |
|---|---|
| Act pages with 5–6 islands (Act IV) | Everything `client:visible`. Parquet loads on the first Explore, not on scroll |
| CLS from charts sizing after load | A fixed aspect-ratio box per figure, sized from the spec, so nothing reflows |
| LCP on `/` | The spine is the LCP element: text, a preloaded font subset, no hero image |
| Font weight | ≤ 4 preloaded Latin subsets (P2). The mono face loads lazily, since it's only used in chips and code |
| Third parties | Only the Cloudflare beacon. Nothing else external (no YouTube embed; P6 links the video instead) |

## 7. Per-act OG images

- **Generated at build** with Satori → resvg (no browser, no runtime): a PNG of 1200 × 630, in the light theme.
- **Templates:** the front door, each act, `/lessons`, `/glossary` and SD pages. Each shows the wordmark, the
  act or page title, its headline, and **at most one number**, rendered from the same `<Claim>` value the page uses,
  so the image can't disagree with the page. SD pages show the SD id and title.
- **Size:** ≤ 150 KB each, written to `dist/og/`. Content-hashed, so the immutable cache applies.
- **Tags:** `og:image`, `og:image:alt` (the headline as text), `twitter:card=summary_large_image`.
- **Disclosure:** the image's text is generated from strings already in the scanned bundle or content, and a test
  asserts that every OG string also appears on its page, so nothing reaches an image that wasn't scanned.
- **Check:** every page has an `og:image` that exists and is within budget, and LinkedIn's Post Inspector preview
  of `/` and one act is checked by hand once, before P6.

## 8. Small polish

- **404:** a plain page with the act nav and "Try the glossary or the tours".
- **Copy-link anchors** on every module heading (`#m9`) and SD page section, with a "Link copied" toast. No
  `alert()`.
- **The footer** shows "Data as of <export date> · bundle <sha8>", from the manifest. The site is a dated
  snapshot by design (plan §6).
- **Print:** Method sections print legibly (light theme, no islands, URLs after links). It costs a dozen CSS lines,
  and P6's one-pager reuses it.

## 9. Work steps

1. Glossary: grow `glossary.yaml` to cover every marked term. `remark-glossary` lint. The `<Term>` component. The
   `/glossary` page.
2. Lens copy: draft all 63 notes. **The operator reviews the 9-note sample** (a lens-copy PAUSE). Finish the rest to
   the sample's pattern, plus the no-lens switcher and the act-page markers.
3. Tours: `tours.yaml`, the tour bar, the build checks, the Playwright walks.
4. The a11y/mobile/dark checklist (§5.1) as tests, then the fixes.
5. Performance: the fixes in §6, then Lighthouse flipped to blocking.
6. OG images and the small polish (§7, §8).
7. The manual audit (§5.2), whose findings are fixed or logged.
8. The P5 summary, then the v1.0 release card for the operator: the full-site disclosure read on the changed
   surfaces (lens notes, glossary, tour notes and OG text are all new public text), then the merge to `production`.

## 10. Exit criteria

1. Lighthouse ≥ 95 on all four categories on every template, with the job **blocking** and green on `production`.
2. axe clean on every route in both themes and every lens state. The manual audit's findings are all fixed or logged.
3. Every module has three lens notes within the rules, and the operator has edited the sample.
4. All three tours walk end to end on phone and desktop.
5. Every marked term has a tooltip and a `/glossary` entry, and the glossary lint is clean.
6. Every page has an OG image within budget, and the preview has been checked by hand.
7. The operator has signed the disclosure read of the new public text, and v1.0 is on `production`.

## 11. Decisions I've taken (flag if you disagree)

- **Tours are routes, not overlays** (§4.1), for accessibility and phones.
- **Lens "reordering" is limited to which note is expanded** (§3.3), so anchors and screenshots stay stable. This is
  narrower than P2 §6.1's wording, and doesn't change P2's mechanism.
- **Glossary marks stay authored, with a lint**, not auto-linking (§2.2).
- **Visual regression covers eight pages, not all of them** (§5.3).
- **No video embed on the site** (§6). P6 links the walkthrough instead of embedding it, to keep the CSP and
  performance intact.
- **Lens copy is reviewed by sample** (§3.2): 9 of 63 notes edited by the operator, the rest written to match.

## 12. Amendments from E9-G0 (2026-10-15)

Applied by E9.P0.1 from [E9](E9_2026-10-15.md) §2 and §8. The rows are in-place fixes.

| Change | Why |
|---|---|
| I.6 has no live ticker to pause, poll or mask. Checklist rows 6–7 and the visual-regression masks change (§5.1, §5.3) | E9-G0 Q6; SD-SC-07 |
| The glossary seed already carries E6 and E7's terms (§2.1) | E9-G0 Q3; P0 §7 |
| The lead tour's first note counts no epics (§4.1) | E9-G0 Q3: the timeline runs E0–E7 |
