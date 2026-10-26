# P4 design — Full build-out: the remaining 15 modules and the lessons coda (2026-09-30)

**Parent:** [SHOWCASE_plan.md](SHOWCASE_plan.md) §4. **Builds on:** v0.1 (P3), the P2 shell and
chart kit, and the P1 exporter, which gains its P4 tables here (§10). **Feeds:** P5
(explainability polish), which starts once every module exists.

P4 is breadth. Every module follows the v0.1 pattern (60 s / Explore / Method, claims only,
a provenance chip on every figure, a table view on every chart), so this doc specifies
**what each module shows and why**, plus the few new mechanisms (replay player, SD search,
pre-registration proofs, the MLflow and feed snapshots). It doesn't restate the shared rules.

*Since E9.P0.5:* the headlines, captions, intros, hand-offs and lens lines below are seeds. [`narrative.md`](../content/narrative.md) holds
the copy, and its §9 lists what changed and why (P0 §15).

---

## 1. Release trains

The order is fixed by how much each act differentiates (plan §4): Science → Operating model →
Verdicts → System → Lessons. Every train is a normal `main` → `production` release. A module
ships when its `release` flag flips (P2 §6.2), so a train can go out partially.

| Train | Modules | Why in this position |
|---|---|---|
| **v0.2** | II.8 Bake-off · II.10 Null models & the strategy-class screens, E5–E7 | Completes the Science act, the strongest act for IC interviews |
| **v0.5** | IV.17 Pre-registration as code · IV.18 Case replays · IV.19 Throughput & compute · IV.20 Human/AI division of labour · IV.21 Project → plugin | Completes the Operating model, the strongest act for lead/manager roles (plan: v0.5 = II + IV) |
| **v0.7** | III.13 SD explorer · III.14 Learned / not learned | Completes Verdicts; the explorer needs the most text tooling |
| **v0.9** | I.1 Data & collector · I.2 Features · I.3 Labels · I.4 Models & training · I.5 MLOps · I.6 Live inference · `/lessons` | Completes the System act, replacing the v0.1 stub; the lessons coda closes the arc |

v1.0 is P5's polish on top of v0.9.

## 2. New shared components (added to the P2 kit when their first user lands)

| Component | Purpose | First user |
|---|---|---|
| `Heatmap` | 2-D cell grid with a **diverging** scale around 0 or a **sequential** scale. Cell text in ink tokens; hover shows the cell's full row | I.3 label geometry |
| `ReplayPlayer` | Steps through a replay (§6.2): a progress rail, keyboard ← →, deep-linkable `#step-n` | IV.18 |
| `CodeExcerpt` | Syntax-highlighted excerpt (build-time Shiki, no runtime JS), with file path, commit chip and line range. Source must be a reviewed bundle excerpt | IV.17, I.2 (IV.21 shows no plugin code while the plugin is private, SD-SC-05) |
| `CommitOrder` | Two commit marks on a time axis ("declared" → "first result"), with the gap labelled. Proves ordering, not duration | IV.17 |
| `SearchIndex` | Client-side full-text search (MiniSearch, ~7 KB gz) over a prebuilt index shipped in the bundle | III.13 |
| `Matrix` | Row × column grid of glyph cells (✓ / ◐ / —) with a legend. Not a heatmap: categorical states | IV.20, III.14 |
| `FeedSnapshot` | A static, dated panel: when the prediction feed last published, and the coins it covered, labelled "snapshot · <newest point's timestamp>". By default it shows none of the feed's values (SD-SC-12). No polling, no pulse and no crimson (SD-SC-07) | I.6 |

## 3. Act II — The science (v0.2)

### II.8 Model bake-off & tabular saturation

**Job:** show ML breadth, and the finding that the ceiling was the *information*, not the model.

- **60 s.** Headline: *"Six model families, one answer: the features, not the learner, set the ceiling."* (The
  count is `C-arch-families`: six on the record; §12 point 1 found no MLP arm; SD-SC-15, SD-SC-19.)
  The figure is a `DotStrip`, one row per model family (logistic, LightGBM, XGBoost arch-#0
  control, AutoGluon, TabM, TabICL; no MLP arm, §12 point 1), with each dot a coin × fold median test Sharpe, a
  zero line and the control's median as a reference line.
- **Explore.**
  - **Selectors:** metric (test Sharpe · val→test gap · dir-AUC where logged); head variant
    (base · flipped · val-quantile rate head); coin (dev quartet / all).
  - **Second chart:** "How much of the lift is volatility timing?" A `BarChart` of AP-lift
    reproduced by a pure volatility timer (~93 %, Stage-0) next to the model's own.
  - **What to notice:** logistic reaches ~98.8 % of XGBoost's Sharpe, and the spread between
    families is smaller than the spread between folds.
- **Method.**
  - The bake-off protocol: arch-#0 as the mandatory control, Bar A (paired-bootstrap Δ-CI
    above 0 against the control) and Bar B (a positive median on traded folds).
  - The two priors: saturation, and threshold transfer beating ranking.
  - The "dead list" entries this closed.
  - The external deep-search survey that produced the shortlist, 13 ranked candidates → 6.
- **Claims:** C-arch-families, C-E2-logistic-ratio, C-E2-stage0-voltimer, C-E2-auc, C-E2-barA
  (all new except the first).
- **Data:** `arch_bakeoff` (the p16/p18/p23/p25/p26 eval parquets share one schema: arch,
  coin, fold, evaluable, val/test Sharpe, threshold, n_trades, gap), `stage0_diag` (p32).

### II.10 Null models & the strategy-class screens, E5–E7

**Job:** show hypothesis design with explicit nulls. It also covers the strategy change.
After E2–E4 had each closed NO-GO, E5 changed the strategy class itself, on a $0, two-day,
kill-bar-first budget per screen. After the family closed, E6 and E7 each screened one more class the same way:
$0, a bar closed in code before the first cell, and a gate (E9-G0 Q3).

- **60 s.** Headline: *"Each new strategy class was held to a bar written before its data."*
  The figure is eight screen cards, grouped by epic:
  - E5's six: carry, cross-sectional rank, short volatility, pairs, seconds-level lead-lag and
    regime, each marked "$0 · ≤ 2 days";
  - E6's BTC short variance (an iron fly priced from Deribit's trade tape);
  - E7's slow trend rule, on two verdict vehicles (perp and EU spot).

  Each card shows its verdict glyph and the deciding number vs the bar, read from `verdict_ledger`.
- **Explore.**
  1. **The null that mattered (S3):** a `Histogram` of the randomised-entry null distribution
     for the short-vol book, with the real book marked at the **40.8th percentile**.
     Caption: "What the book earned came from the unconditional premium, not from the
     forecast."
  2. **The drift limb (P3 escalation):** a toggle between *pooled* and *per currency*. The
     PSI bars show pooled 0.204 (it would pass the < 0.25 bar) against BTC 2.455 and ETH 0.722
     (both fail). A note explains that the per-currency reading was pinned in code before any
     number existed. This links to replay R4.
  3. **Unreachable limbs (S1, S2):** why a null limb can be *unreachable*, which makes the
     verdict NO-READING. The recorded counterfactuals are shown as *recorded, not decided*.
  4. **E6: a NO-READING held as NO-READING.** The coverage limb shows how much of the
     construction the free trade tape could mark and fill, against its pre-registered bars.
     Both fell short, so the screen couldn't read. Beside it are limbs (a) and (b), which would
     KILL by a wide margin, labelled as reported, not decided. The gate closed E6 without
     relabelling the verdict. Next to it sits the report-only DVOL-implied book: the premium
     shows at index level, not at the prices a seller gets.
  5. **E7: a KILL on both vehicles, accepted at the gate.** This is the limb table per vehicle,
     as `reading()` read it, with each limb's reachability stated first. K3 was near one-way on
     BTC's 2020–21 run, so the two-sided evidence is K4 (the timed book against its untimed,
     vol-scaled basket) and K5 (where the timing sat among random entries). On the perp, K4 did
     not hold. It also shows the funding-by-momentum table the plan promised either way.
- **Method.**
  - The screen template: class, hypothesis, economic limb, null limb, kill bar in code, and
    the seal.
  - Why each null was built the way it was: randomised entry, prevalence-matched, and so on.
  - The close-outs' scope-honesty clauses, verbatim (E5, E6 and E7, each §1).
  - What was *not* screened: C6, C8, C9, C10 (E5), and what E6 and E7 left open (their
    close-outs §4.2).
- **Claims:** C-E5-screens, C-E5-S3-null, C-E5-S3-R, C-E5-S3-D, C-E5-S1-counterfactual,
  C-E5-S2-counterfactual, C-E5-unscreened, C-E6-P2, C-E6-coverage, C-E6-dvol-book, C-E7-P2,
  C-E7-limbs, C-E7-funding (new where not in P0).
- **Data:**
  - `e5_screens` (parsed from the close-out §2.1);
  - `s3_drift` (the PSI per limb, from `p3_drift.pkl`, with its footer fingerprint `38dcdfdc`);
  - `null_dist`: the binned random-entry nulls of S3, E6 and E7, keyed by epic, screen and
    vehicle (§10);
  - `screen_limbs`: E6 and E7's limbs per vehicle, and `e7_funding`, the funding-by-momentum
    table (§10);
  - `verdict_ledger` (P1) for every card's verdict and deciding number.

## 4. Act IV — The operating model (v0.5)

### IV.17 Pre-registration as code

**Job:** turn "we pre-registered" from a claim into something the reader can check.

- **60 s.** Headline: *"Every reading was committed before its first result. The commits prove the order."*
  The figure is a `CommitOrder` strip, one row per pre-registered item, showing the
  declaration commit → the first-result commit.

  | Item | Declaration commit | First-result commit |
  |---|---|---|
  | E4.P6.8 | `c973274` "reading declared BEFORE the first re-cut cell" | `88ec6dc` |
  | E4.P7 | `64aa7b6` | `e176bcb` |
  | E5.P3 | `02b5c53` | `afa1f4f` |
  | … | | |

  Every row reads left-to-right; none is reversed. E6.P2 and E7.P2 join the list (E9-G0 Q3).
  Both bars were closed in code before the first cell (E7's at `71bf890`), and
  `content/prereg_pairs.yaml` curates their pairs.
- **Explore.**
  1. **The seal:**
     - a timeline of the seals through E7. E5's INTERIOR and FUTURE show "reads: 0" (E6's
       `e6_seal.py` sealed them again). E7's holdout (`e7_seal.py`) is unspent by E7 but not
       unseen: outside E5's windows, its months were dev data for E5 and E6 (E7 close-out §1
       point 5);
     - every disclosed contact, shown rather than hidden, in its close-out's own words. That
       covers E5's ~2 h count-only touch by an aborted attempt (SD-E5-26), the one DVOL bar an
       E6 skeptic printed at the seal's edge (SD-E6-24), and E7's contacts with holdout-dated
       information (its close-out §1 point 5);
     - a `CodeExcerpt` of `ml/e5_seal.py`: `strip_sealed`, `assert_unsealed` and the single
       `gate_unseal("E5-G2")` exception that raises `SealViolation`.
  2. **Hashed bars:** a bar is a number in code whose digest was pinned at pre-registration.
     A `CodeExcerpt` of one bar and its test shows how changing the bar after the fact would
     fail the suite, which is the supervisor's `CHECK_CMD`.
  3. **Freeze records:** a named configuration is content-hashed, so the confirmation runs
     are provably the same configuration. This links to the leakage autopsy, where the freeze
     is why the leak was recorded rather than quietly fixed.
- **Method.**
  - Why the order is proven by commits: binka is private, but the SHAs and timestamps are
    public, and the declared-reading commit messages are quoted verbatim.
  - Limits: a commit proves the order in *this* repo's history. It doesn't prove nothing was
    peeked at before. The seal and the loader guards are the defence there, and the doc says
    so plainly.
- **Claims:** C-prereg-pairs (`recomputed`: every pair ordered), C-seal-reads, C-seal-contacts,
  C-seal-rule.
- **Data:** `prereg_pairs` (git log search for "declared" / "pre-registration" / "BEFORE the
  first" commits paired with the next result commit on the same item, **curated**: the pairing
  file `content/prereg_pairs.yaml` is authored, and the exporter only resolves timestamps),
  plus excerpts `seal_core`, `bar_example`.

### IV.18 Case replays

**Job:** the operating model in motion. Real episodes (the ones P0.3 picks; R1–R4 at design
time), each showing the agent working inside the rules and me deciding at the edges.

- **60 s.** Headline: *"Moments where the rules, not the agent's judgement, decided what happened next."*
  The figure is one replay card per chosen replay, each with a one-line hook:

  | Replay | Hook |
  |---|---|
  | R1 The look-ahead | "The agent found a one-minute leak in the flagship, and was not allowed to fix it quietly." |
  | R2 The gate pause | "Dossier built, recommendation written, loop stopped: a program gate is mine." |
  | R3 The lost GPU | "The null control failed. The loop paused, the cause was found, the fix was committed, and the run resumed." |
  | R4 The easy pass | "A pooled reading would have passed. The per-currency reading had been fixed in code first." |

- **Explore:** the `ReplayPlayer` (§6), 5–8 steps per replay.
- **Method.** Where each step's evidence comes from (commit, SD entry, supervisor log line,
  transcript excerpt), and what was cut and why (P0 §5.3 redaction).
- **Claims:** replay-specific (`C-R1-*`, and so on), each a `recorded` claim against the SD entry or card.

### IV.19 Throughput & compute

**Job:** the manager's view: how much work the loop did, how often it needed me, and what it cost.

- **60 s.** Headline: *"N items, M gates, one flat subscription. The limit on autonomy was my sign-off, not the budget."*
  The figure is three `StatTile`s: items worked, PAUSEs at a boundary, and **median
  PAUSE → sign-off latency** (the human-in-the-loop delay, from PAUSE to my recorded decision).
  Under "items worked", one line covers a tooling epic, not shown, the one place the site describes it (E9-G0 Q5,
  SD-SC-08): *"one tooling epic, not shown: personal data"*, with its item count. Elsewhere a
  reference to it reads "a tooling epic, not shown" (SD-SC-09).
- **Explore.**
  1. Items per week, stacked by reading (✓ / ✗ / ⛔ / ⏸), from `autorun_items`.
  2. PAUSE → sign-off latency per gate (`DotStrip`). This shows where I, not the agent, was the
     bottleneck. E5-G1 is the long one: its screens finished 2026-08-19, and the gate was decided
     2026-09-27. The exact latency is computed from the PAUSE line, not from these dates.
  3. **API-equivalent compute per item** (`Histogram`), labelled *API-equivalent, as reported
     by Claude Code; the real cost was a flat subscription*. Unknown values are counted,
     not imputed.
  4. Recovery events: nudges, infra retries, repairs, limit waits, halts. They are counted from
     the supervisor log where it was retained, and shown as partial.
- **Method.** The loop as of the export; its values are claims checked against `config.env`
  (E9 §2 row 6, P1 §6):
  - The notional budgets per item and per run (C-loop-budget) as a runaway guard, not spend.
  - The usage limits pace the loop (P3 §8, C-loop-limit).
  - Per-kind model and effort routing: Opus throughout, `max` effort for design and dossier
    items.
  - What a metered team would do differently.
- **Claims:** C-loop-items, C-loop-sub, C-loop-cost (API-equivalent), C-loop-limit,
  C-pause-latency (new, `recomputed`), C-recovery-counts (new, partial-flagged),
  C-loop-items-hidden (new, `recomputed` from `autorun_withheld`, the count P1 §2's filter keeps).
- **Data:** `autorun_items`, `autorun_pauses`, `gate_events` (P3 delta), `autorun_recovery`
  (new, from `.autorun/state/logs/supervisor.log`), `autorun_withheld` (P1 §2).

### IV.20 Human/AI division of labour

**Job:** the delegation charter. Who does what in an AI-native research team of one.

- **60 s.** Headline: *"I framed the questions and signed the gates. The agents did almost everything in between."*
  The figure is a `Matrix` with activities as rows and actors as columns:
  - **Activities:** frame the question · external literature search · plan drafting ·
    pre-registration · implementation · code review · running jobs · skeptic check ·
    verdict analysis · gate decision · spend · live changes.
  - **Actors:** me · Claude Code agent (autorun) · claude.ai deep research · skeptic subagent,
    plus, as of the export, the supervisor's read-only verifier (E9 §2 row 6).
  - **Cells:** ● owns · ◐ contributes · — never.
- **Explore.**
  - Click a row to see the evidence for that cell: the policy line that assigns it, plus one
    real instance (a commit or SD entry).
  - The **research loop** as a `StepDiagram`, retrospective (agent, directed by me) → DR prompt
    (agent drafts, I edit) → deep research (claude.ai) → plan drafted from the results (agent)
    → ratification (me, verbatim sign-off). Real artifacts at each step: the E5 retrospective,
    the prompt, the results and the §12 ratification.
- **Method.**
  - Why the gates stay human: irreversibility (the holdout unseal as a "one-way door"),
    money, and program direction.
  - What I'd delegate next, and what I wouldn't.
  - The skeptic brief (POLICY step 8): every card and dossier gets an adversarial read
    before it is final.
- **Claims:** C-dr-cycles, C-ratifications (new). C-dr-cycles counts the DR prompt → results
  cycles: E2, E3, Fable ×2, E5, and post-E5 (three directions, feeding E6 and E7). The count covers
  only the epics shown (SD-SC-08).
- **Data:** `content/raci.yaml` (authored, each cell citing a policy line + an evidence commit;
  the exporter verifies each cited commit exists), plus `text/boundaries.json`.

### IV.21 From project to plugin

**Job:** show the engineering move a lead makes, from a working hack to a reusable,
tested tool.

- **60 s.** Headline: *"The loop outgrew the project, so I split mechanism from policy and shipped it as a plugin."*
  The figure is a split diagram, as of the export (E9 §2 row 6):
  - **the mechanism, in the plugin:** supervisor, tail, guard framework, the item, commit and
    repair skills, init, retro, the acceptance gate (`autorun-gate`), the verifier, and the
    backlog and cards (`autorun-plan`);
  - **the policy, in each repo:** `.autorun/POLICY.md`, `config.env`, `guard_rules.py`,
    `backlog.json`, the prompt and the ledger.
- **Explore.**
  - **The design principles** as flip cards, one per section of the plugin's design document (C-plugin-principles,
    `recomputed` from `plugin_principles`; 19 sections when this was designed). Each has a one-line
    rule, *the failure that caused it*, and the section's name (not a link, since the plugin stays
    private, SD-SC-05).
  - The **test harness:** a stub-`claude` end-to-end suite (C-plugin-tests, counted at the
    export; 39 tests when this was designed) that runs the supervisor against scripted sessions:
    CONTINUE with no commit, a usage-limit exit, a crash mid-item.
- **Method.** The extraction plan (config-driven, paths unchanged, minimal churn), and what
  broke in migration and how it was verified.
- **Claims:** C-plugin-principles (`recomputed`), C-plugin-tests (counted from autorun's own test
  files at the export), C-plugin-extracted (date + commit).
- **Data:** `plugin_principles` (parsed from the headings and first paragraphs of the plugin's design document).
- **Dependency:** none. The plugin stays private, so IV.21 is diagrams and prose, with no GitHub
  link and no plugin excerpts (§12 answer 2, SD-SC-05).

## 5. Act III — The verdicts (v0.7)

### III.13 Scope-decision explorer

**Job:** make the decision logs of E3–E7 browsable, as the densest evidence of how the program
was run.

- **60 s.** Headline: *"N decisions where I knowingly took the smaller path, each with its revisit trigger."*
  N is C-SD-count, the splitter's own count over E3–E7, never typed into the copy.
  The figure is a density strip of SD entries over time, per epic, with glyphs by type.
- **Explore.**
  - Full-text search (`SearchIndex`).
  - **Facets:** epic · type (compromise / defect found / conclusion / pre-registration) ·
    status (open / revisited / obsolete) · "touches a verdict".
  - The results list opens the public SD page. Each SD page gains **"cites" / "cited by"**
    lists from the cross-references the P1 parser extracts. This is deliberately not a graph
    drawing: lists are readable, and a hairball of every entry isn't.
- **Method.**
  - The convention (CLAUDE.md §6): when a narrower path is taken, record what was traded away
    and what would restore it.
  - Why that matters on a team: deferred scope stays reviewable instead of being forgotten.
- **Claims:** C-SD-count, C-SD-by-type (new, `recomputed`), C-SD-revisited (new).
- **Data:** `text/sd_entries.json` gains `type`, `status`, `cites[]`. `type` comes from
  `content/sd_tags.yaml`, which is **authored**: one line per entry, since type heuristics
  would be wrong often enough to matter. Plus `sd_search_index.json` (built by the exporter,
  ≤ 400 KB).

### III.14 What was learned, and what was not

**Job:** the synthesis. The failure taxonomy and the honest open set.

- **60 s.** Headline: *"N ways every positive result died, and the defence that caught each one."*
  N is C-taxonomy-count, from `content/taxonomy.yaml`. The figure is a `Matrix` of the causes
  against the epics where each struck, with a count per cell. The retrospective's four causes
  are look-ahead leakage · drift masquerading as signal · selection on the evaluation · silent
  environment/plumbing faults. E9.P4.E7 maps E6 and E7's incidents onto them, or adds a cause
  where none fits. One candidate is E6's DVOL-implied book: a premium visible at index level but
  not at the prices a seller gets (E9-G0 Q3).
- **Explore.**
  - Click a cause to see its incidents (SD entries): the GPU silently falling back to CPU
    (SD-E4-29), the routed loader ranking a sweep on 3 of 16 cells (SD-E4-30), the B3 PSI
    2.6–7.5 drift, and so on. Each comes with *the defence that worked*.
  - **The dead list vs the open set:** what is settled (with the external evidence needed to
    reopen it) against what was never tried (C6 sequence models, C8 on-chain, C9 market-making,
    C10 cross-venue), plus what E6 and E7 left open (their close-outs §4.2, with each one's
    reopening condition from §6).
- **Method.** The meta-lesson, quoted from the retrospective: *"the program's methodology
  out-performed its alpha."*
- **Claims:** C-taxonomy-count, C-taxonomy-{1..N}, C-dead-list, C-open-set.
- **Data:** `taxonomy_incidents` (authored `content/taxonomy.yaml` mapping cause → SD ids;
  the exporter validates that the ids exist).

## 6. Replay content pipeline (IV.18)

### 6.1 Sources, per P0 §6

The complete record comes from git, SD entries, the ledger and the supervisor log.
Transcripts, where they were retained, are an optional extra for verbatim excerpts.

| Replay | Spine | Optional transcript |
|---|---|---|
| R1 | SD-E4-24 · E4.P6.6a → 6.8 → 6.8b → P7 → G2 commits | — (pruned; P0 §6) |
| R2 | supervisor log 2026-07-24 (`.autorun/state/logs/supervisor.log`) · `ccdeb9f` · the E3-G1 dossier | — |
| R3 | `ea4f96c` · `9344574` · `c3a3ce5` · SD-E4-29/30 | — (pruned) |
| R4 | SD-E5-30(c) · SD-E5-31 · `02b5c53` → `afa1f4f` · the operator's verbatim sign-off | The 2026-09-28 sessions, in the archive (P0 §6); P0.3 lists the candidates |

If P0.3 picks P0 §6.1's added candidates, R5 (E6) and R6 (E7), they join this table and IV.18's cards.

### 6.2 Replay format (`content/replays/Rn.yaml` → bundle `replays/Rn.json`)

```yaml
id: R4
title: The easy pass
steps:
  - kind: situation | agent | rule | human | outcome
    text: "…"                         # authored, first person for 'human' steps
    evidence:
      - {type: commit, sha: 02b5c53}
      - {type: sd, id: SD-E5-30, anchor: c}
      - {type: excerpt, id: r4-psi-pin}   # reviewed excerpt (P1 §7.3)
      - {type: log, line_sha: …}          # supervisor log line: an excerpt, reviewed (P1 §7.3)
```

Authoring rules:
- Text is written by hand.
- Every step cites at least one piece of evidence.
- Excerpts pass the review gate.
- An `agent` step describes what the agent *did*, never what it "thought", unless a transcript
  excerpt shows it.

## 7. Act I — The system (v0.9)

igor-web `/algo` already tells the system story for non-specialists (raw feed → candles → TA →
architecture → experiments → trades → live). Act I is the **engineer's version**: the same
spine at depth, with numbers and code, and links across to `/algo` for the gentle version
instead of repeating it.

| Module | 60 s headline (draft) | Explore | Key data / claims |
|---|---|---|---|
| **I.1 Data & collector** | "A C++ collector, 189 columns per second per coin, and a pipeline that logs its own health." | Pipeline `StepDiagram` (Binance WS/REST → `bintri` (C++) → secondwise archive → 1m/5m klines → datasets); dataset-health table per coin (rows, time range, NaN %, ts gaps) from `dataset.log` | `pipeline_stats`; C-bintri-loc, C-secondwise-cols, C-dataset-rows |
| **I.2 Features** | "Three indicator libraries, cut to 180 features, with every drop explained." (the raw count comes from a claim computed from `feature_lists.py`, not asserted) | Funnel bar (raw per library → decorrelation drops → merged → final), sortable feature table with family, library and importance (p27 rankings); the **1m + 5m minute-wise merge with the 4-period shift**, which prevents look-ahead, as a small diagram. Foreshadows the autopsy | `feature_catalog` from `ml/feature_lists.py` (FINAL_3_LIBS = 180, and so on) + `p27_feature_rankings`; C-features-final |
| **I.3 Labels** | "Which barrier is touched first defines the label, and its geometry changes everything." | (1) An **illustrative** touch-label animation: a price path, TP/SL bands and a window, with the label assigned, clearly marked illustrative (`min_time_grain` exception, P1 §4). (2) A label-geometry `Heatmap`: TP × SL per horizon, toggling between dir-AUC and precision margin. The punchline: AUC rises with wider TP while economics stay negative. (3) The stage-2 economics table | `label_geometry` (p17 stage 1/2 cell summaries); C-E2-labels-auc-vs-econ, C-E2-stage2 |
| **I.4 Models & training** | "Walk-forward folds, per-fold Optuna, GPU training pinned so a driver fault can't change the numbers silently." | Walk-forward fold diagram (train / val / test windows per fold); HP-search protocol card; the device-pin story (SD-E4-29: a lost GPU silently fell back to CPU and changed every number → pinned device + loud failure) | C-folds, C-optuna-trials (from the MLflow snapshot), C-device-pin |
| **I.5 MLOps** | "Self-hosted experiment tracking, reproducible datasets, and long jobs that survive crashes." | MLflow layout (1 main + 4 per-fold experiments per coin × session × bracket, 35 tags) with **counts from a snapshot**; the resumability pattern (per-coin partials); OOM protection; content fingerprints on every artifact | `mlflow_summary` (§8); C-mlflow-runs, C-mlflow-experiments |
| **I.6 Live inference** | `C-live-status`, verbatim. E9-G0 Q6's wording runs past the 15-word headline rule, and the operator's wording wins | `FeedSnapshot` (when the feed last published and the coins it covered, labelled with the newest point's timestamp; values only on the operator's carve-out, SD-SC-12; §8); the architecture of the live path (`bintri -monitor` → `get_rich` → Binance orders; `feed_server` → public feed); the streaming causal head **certified against the batch head** (E4.P6.6 prep) | C-live-status (P0 §10.3 as superseded, SD-SC-07); `feed_snapshot` (§10); no trade counts or P&L (disclosure) |

## 8. MLflow snapshot (`showcase snapshot mlflow`, P1 extension)

- A separate, manual command. It reads MLflow **read-only**, with credentials from the env
  (never written), and writes `py/showcase/cache/mlflow_snapshot.json`.
- **The snapshot holds only aggregates:** experiment count by name pattern, run counts by
  status, Optuna trial counts per study, metric distributions for the few metrics shown
  (binned), and tag-key inventory (keys only, **never values**).
- The snapshot file becomes a pinned input (sha256 in the manifest). Exports stay offline and
  reproducible (P1 §11).
- The scanner runs on the snapshot before it is used. MLflow tags could contain paths or
  hostnames, and the tag-*values* exclusion is enforced in code.
- **The feed snapshot follows the same pattern** (E9-G0 Q6; SD-SC-07, SD-SC-12). `showcase
  snapshot feed` reads the public prediction feed once. It keeps only each coin's name and newest timestamp, never a
  value. The points sit inside E5's sealed FUTURE window. It writes `py/showcase/cache/feed_snapshot.json`, a pinned input, and
  the export never calls the feed. E9.P1.1 captures the file once, early, so the date survives if
  the feed goes away before v0.9. Values join
  only if the operator carves them out at Gate E9-G1 (SD-SC-12).

## 9. Lessons coda (`/lessons`, v0.9)

This is written in first person, and is the one page that is mostly prose.
1. **The meta-lesson:** the methodology out-performed the alpha, and that's the part that
   transfers.
2. **What I'd do differently.** Draft points, each tied to evidence:
   - Build the causal forward-replay path at the start. The leak survived two epics and was
     caught only by a forward-replay build.
   - Measure costs before the first model, not in E4.
   - Seal holdouts at plan time from the first epic. E5 did it; E2–E4 spent the seal.
   - Set the family-closing pre-commitment earlier.
3. **What transfers to a team of humans and agents:**
   - pre-registration as code;
   - freeze → record → authorised re-cut;
   - boundaries enforced by hooks, not by prompts;
   - a supervisor that re-checks;
   - an append-only decision log;
   - gates that stay human.
4. **What's next.** The honest open set (III.14), and where the operating model is going.
   The loop is already a reusable plugin.

The claims rule still applies. Evidence-tied points carry chips; the opinions are marked as opinions.

## 10. Exporter additions (P1, for P4)

| Table / text | Source | Train |
|---|---|---|
| `arch_bakeoff` | `test_data/tmp/p16_*_eval`, `p18_*`, `p23_autogluon*`, `p25_tabm*`, `p26_tabicl*` parquets (no MLP arm exists in this schema: §12 point 1) | v0.2 |
| `stage0_diag` | `p32_stage0/` | v0.2 |
| `e5_screens`, `s3_drift` | E5 close-out §2.1 · `e5s3_vol/`, `e5s3p3_shortvol/` (footer fingerprints) | v0.2 |
| `screen_limbs`, `null_dist`, `e7_funding` (E9-G0 Q3) | `test_data/tmp/e6p2/` and `e7p2/`, each P2 card and its cells with the card's footer fingerprint; S3's nulls from `e5s3_vol/`, `e5s3p3_shortvol/`. `screen_limbs` holds E6's coverage and limbs (a)–(d), the report-only DVOL-implied book, and E7's limbs per vehicle. `null_dist` holds the binned random-entry nulls of S3, E6 and E7, keyed by epic, screen and vehicle. `e7_funding` is the funding-by-momentum table. Verdicts and deciding numbers stay in `verdict_ledger` | v0.2 |
| `prereg_pairs` | `content/prereg_pairs.yaml` + git timestamps | v0.5 |
| `replays/*` | `content/replays/*.yaml` + resolved evidence | v0.5 |
| `autorun_recovery` | `.autorun/state/logs/supervisor.log` | v0.5 |
| `autorun_withheld` | the count of items P1 §2's filter dropped (a tooling epic, not shown) | v0.5 |
| `plugin_principles` | the plugin's design document | v0.5 |
| excerpts `seal_core`, `bar_example`, … | `ml/e5_seal.py`, E5 bar code/tests. No plugin code while the plugin is private (SD-SC-05) | v0.5 |
| `text/sd_entries.json` + `type` / `status` / `cites` + `sd_search_index.json` | SD logs + `content/sd_tags.yaml` | v0.7 |
| `taxonomy_incidents` | `content/taxonomy.yaml` (validated ids) | v0.7 |
| `pipeline_stats` | `dataset.log` files under `~/data/bintri/<coin>/` (aggregates only) | v0.9 |
| `feature_catalog` | `ml/feature_lists.py` (AST-parsed, not imported) + `p27_feature_rankings.parquet` | v0.9 |
| `label_geometry` | `p17_label_geometry/` (2.1 GB of fold CSVs → cell summaries; precompute like leak corr) | v0.9 |
| `mlflow_summary` | the snapshot (§8) | v0.9 |
| `feed_snapshot` (E9-G0 Q6) | the feed snapshot (§8): per coin, its name and newest timestamp (SD-SC-12) | v0.9 |

New input roots, which extend the P1 allow-list:
- `~/data/bintri/<coin>/dataset.log`, files matching only that name;
- `py/showcase/cache/`;
- `py/test_data/tmp/e6p2/` and `e7p2/` (E9-G0 Q3);
- the plugin's design document and hook (already allowed).

## 11. Definition of done (per module)

1. The 60 s / Explore / Method layers are complete, and each lens has its note.
2. Every number is a verified claim, and every figure has a chip and a table view.
3. Playwright covers the module's interactions (toggle states, keyboard paths), and axe is clean.
4. The module passes the disclosure read at its release (the §11.3 P3 checklist rows 1–3, scoped
   to the module).
5. The module's JS stays within the island budget (P2 §7.4).
6. Its hand-off to the next module reads correctly in its act.

## 12. Open points

1. **MLP arm:** the bake-off headline says "seven families" only if the MLP eval exists on disk
   in the shared schema. Otherwise it says six, and the headline is written from the claim, not
   assumed. This is checked in the v0.2 input spike.
   **Answered by E9.P1.1 (2026-10-16): six.** No MLP arm was ever registered or evaluated in the shared schema
   (spike §3; SD-SC-19), so the headline says six.
2. **Is the plugin public?** IV.21 is much
   stronger with a public repo, a README and a demo GIF (P6). If it's private, IV.21 shows
   excerpts only.
3. **Replay transcripts:** do you want verbatim agent excerpts in replays at all, or
   narration + evidence only? *Rec: a few short excerpts per replay, where they show a rule
   being applied. They're the most persuasive evidence for AI-role readers, and each one
   passes your review.*
4. **Lessons tone:** P4 drafts it, but it's your voice more than anywhere else. I'd write a
   first draft from the evidence and expect heavy edits from you.

**Operator answers (2026-10-15):**
1. *(MLP arm: not an operator question; answered by E9.P1.1: six, see the point above.)*
2. **The plugin stays private for now, and may go public later.** Until then IV.21 explains the plugin in
   **diagrams and prose only**: the mechanism/policy split diagram, the design-principle cards (rule + the failure
   that caused it) and the test-harness story, told without a GitHub link and without code excerpts from the
   plugin's repo. Its claims (C-plugin-principles, C-plugin-tests, C-plugin-extracted) still resolve against the
   plugin's private design document and test suite, like every binka-backed claim. Going public later turns on a "View on GitHub"
   link and the P6 README + demo GIF (P6 §7). Logged as SD-SC-05.
3. **Verbatim transcript excerpts: yes**, a few short ones per replay, each passing the operator's review (P0 §5.3).
   Transcripts are pruned over time (the oldest one retained on 2026-10-15 dates from 2026-09-27), so the R1–R3
   sessions are already gone and R4's are at risk. E9's first action archives the candidate transcripts privately
   (E9 plan §5, P0.0).
4. **Lessons: Claude drafts and the operator edits only minimally.** So the draft must already read as the operator's
   own writing. §9's draft is written from the evidence in the operator's voice, calibrated on their own words in the
   record (verbatim sign-offs, igor-web copy). Every opinion is marked as one, and nothing claims what the operator
   didn't say or do. The operator does one light pass, and the draft isn't re-cut around a heavy edit.

## 13. Amendments from E9-G0 (2026-10-15)

Applied by E9.P0.1 from [E9](E9_2026-10-15.md) §2 and §8. The rows are in-place fixes. The exporter tables are
built at E9.P4.E2–P4.E9.

| Change | Why |
|---|---|
| II.10 becomes "Null models & the strategy-class screens, E5–E7", with E6 and E7's cards and Explore panels. Its cards read `verdict_ledger`; `screen_limbs`, `null_dist` (which absorbs `s3_null_dist`) and `e7_funding` hold only what the ledger lacks (§1, §3, §10) | E9-G0 Q3 |
| `LiveTicker` becomes `FeedSnapshot`. I.6 shows `C-live-status` and a dated snapshot of when the feed last published, with no values unless the operator carves them out (§2, §7, §8, §10) | E9-G0 Q6; SD-SC-07; SD-SC-12 |
| IV.17 adds E6.P2 and E7.P2 to the commit-order list. It shows the seals through E7 with every disclosed contact; C-seal-exception was "the single disclosed exception", false since SD-E6-24, and becomes C-seal-contacts (§4) | E9-G0 Q3 |
| IV.19 adds its one line on a tooling epic, not shown, read from `autorun_withheld`. Its loop values are claims checked against `config.env` (§4) | E9-G0 Q5 (SD-SC-08); E9 §2 rows 5–6 |
| IV.20 adds the verifier as an actor, and C-dr-cycles runs through the post-E5 cycle (§4) | E9 §2 row 6; E9-G0 Q3, Q5 |
| IV.21's diagram shows the mechanism as of the export, its counts are claims, and it has no GitHub link and no plugin excerpts (§2, §4, §10) | E9 §2 rows 6 and 8; SD-SC-05 |
| III.13's count is C-SD-count over E3–E7, not a typed 99 (§5) | E9 §2 row 3; E9-G0 Q3 |
| III.14 counts its causes from `taxonomy.yaml` and takes in E6 and E7's incidents and open items (§5) | E9-G0 Q3 |
| The replay transcripts come from the E9.P0.0 archive, and IV.18 counts no replays, since P0.3 may add R5 or R6 (§4, §6.1) | E9 §2 row 7; E9-G0 Q3 |
| E9.P1.1 captures the feed snapshot early (§8) | E9-G0 Q6: the feed may not last until v0.9 |
| `autorun_recovery` reads `.autorun/state/logs/supervisor.log` (§10) | E9 §2 row 5 |
