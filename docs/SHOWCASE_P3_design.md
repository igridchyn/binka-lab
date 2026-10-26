# P3 design — v0.1: the six launch modules, and going public (2026-09-30)

**Parent:** [SHOWCASE_plan.md](SHOWCASE_plan.md) §4. **Consumes:** the P0 narrative, claims and
disclosure policy; the P1 v0.1 bundle; the P2 shell, chart kit and deploy. **Output:** the first
public version of `lab.gridchyn.ai`, linked from igor-web `/algo` and the CV.

v0.1 has to carry the whole story on its own. A reader who only ever sees v0.1 should leave
with the spine, one rigor story (the leakage autopsy), one economics fact (the cost wall), the
program's shape (timeline and ledger) and the operating model (loop and boundaries). Anything
that doesn't serve one of those waits for P4.

*Since E9.P0.5:* the headlines, captions, intros, hand-offs and lens lines below are seeds. [`narrative.md`](../content/narrative.md) holds
the copy, and its §9 lists what changed and why (P0 §15).

---

## 1. What ships

| Route | Contents in v0.1 | Later (P4) |
|---|---|---|
| `/` | Front door (§3) | — |
| `/science` | Act intro · **II.7 Cost wall** (§4) · **II.9 Leakage autopsy** (§5) | II.8 bake-off, II.10 strategy-class screens, E5–E7 |
| `/verdicts` | Act intro · **III.11 Timeline & gates** (§6) · **III.12 Verdict ledger** (§7) · `/verdicts/sd/[id]` pages | III.13 SD explorer, III.14 learned / not learned |
| `/operating-model` | Act intro · **IV.15 Loop architecture** (§8) · **IV.16 Boundaries & guard hooks** (§9) | IV.17–21 |
| `/system` | **Stub**: a one-screen act summary (pipeline in one diagram + the live-status line) and "coming in the next release", linking to igor-web `/algo`, which already tells this part well | I.1–I.6 |
| `/about`, `/about/manifest`, `/about/data` | Provenance and method, manifest, data console (from P2) | — |
| `/lessons` | Not linked in v0.1 | P4 |

Act order in the nav stays System → Science → Verdicts → Operating model. The front door's
"choose your path" routes send each lens straight to the acts that serve it (§3.3), so the
thin `/system` stub is never the first thing a reader lands on.

## 2. Copy rules (apply to every module)

- **First person.** "I froze the configuration", "I authorised the re-cut".
- The agent is named explicitly on first mention per page: *"Claude Code (mostly Opus), running
  under my autorun supervisor"*, or "(Opus)" where a passage is about Opus-era work (amended at Gate E9-G1, P0
  §17). After that it's "the agent". I don't let "we" blur who did
  what: decisions are mine, and the agent's findings are credited to the agent. Where the work
  ran outside the supervisor (most of it up to Gate E5-G1: the supervisor ran only from
  2026-07-24 to 2026-08-03 before then), the copy says how it ran instead (amended at E9.P0.5,
  P0 §15).
- **Numbers only through `<Claim>`** (P2 §5.3). Qualifiers appear in the Method layer, always.
- **NO-READING is never paraphrased as a failure or a kill.**
- **No copy counts the noes** (E9-G0 Q4). A NO-READING isn't a "no", so no sentence, headline or
  tile tallies the program's negative verdicts. A chart that counts verdicts counts each verdict
  word on its own and never sums NO-READING with KILL or NO-GO (§7).
- **Live bot:** only through `C-live-status`, E9-G0 Q6's past-tense wording (P0 §10.3,
  SD-SC-07). No live P&L, balances or trade counts.
- Headlines: ≤ 15 words, declarative, one number at most. No adjectives doing the work of evidence.
- Glossary terms get a dotted underline and a tooltip on first use per module (P5 fills the
  tooltips; P3 marks the terms).

## 3. Front door (`/`)

### 3.1 Layout (desktop; the phone layout stacks in the same order)

1. **Eyebrow:** "Binka Lab · an ML research program, end to end".
2. **Spine (display type, E9-G0 Q4):** *"I built an ML trading system, then ran a
   pre-registered research program on it that kept saying no. Here is why you should believe
   the no."*
3. **Timeline strip** (compact `Timeline`): E0 → E7 as bands, each with its own verdict glyph
   and label (✓ infra · ✗ NO-GO · ⛔ NO-READING · ✗ KILL; P0 §3.1) and no tally. Clicking a band
   goes to its III.11 entry.
4. **Six `StatTile`s** (3 × 2):

| Tile | Claim | Why this one |
|---|---|---|
| "+0.15 → −0.14 Sharpe when one minute of look-ahead was removed" | C-E4-024-collapse | The rigor story in one line |
| "17–20 bps round-trip cost the model had to beat" | C-E4-cost | The economics |
| "N program gates, each one decided by me" | C-gates-count (`recomputed` from `gate_events`) | Governance |
| "N scope decisions logged" | C-SD-count (`recomputed`, E3–E7) | Process density |
| "6 model families benchmarked; the ceiling was the information" (the count is the claim's: six on the record, SD-SC-15) | C-arch-families | ML breadth (links to the P4 module; in v0.1 it goes to the ledger's E2 rows) |
| "N agent items on one flat Claude subscription" (not "autonomous": SD-SC-15) | C-loop-items, C-loop-sub (new, `recorded` from `content/operating_facts.yaml`) | Operating model. The cost story is "a flat subscription, with its usage limits pacing the loop" (C-loop-limit, §8), not a dollar figure (§14.3). The items of a tooling epic, not shown, aren't counted (SD-SC-08) |

5. **"Choose your path"** (three cards, each giving a reading time and a route):
   - *IC / Staff engineer:* Leakage autopsy → Cost wall → data console. "Try to break a number."
   - *Tech lead:* Timeline & gates → Leakage autopsy → Loop architecture.
   - *Manager / director:* Timeline & gates → Boundaries & hooks → Verdict ledger.
   Selecting a card sets the lens (P2 §6.1) and opens the first stop.
6. **One-paragraph "what this is"** (first person): the system was built and ran live, the
   research closed it as unprofitable, and this lab shows how that conclusion was reached
   and kept honest.
7. Footer links: igor-web `/algo` ("the narrative version"), CV, GitHub `binka-lab`. There is no
   link to the plugin while it stays private (SD-SC-05).

### 3.2 What the front door must never do

It must never show a chart that needs explaining, a number without a chip, or any
"profitable / alpha / edge found" phrasing. Beyond the timeline strip and the tile
sparkline-free numbers, it has no animation.

### 3.3 The 60-second path

The spine, the tiles and one path card are all above the fold on a 1440 × 900 screen. On a
390 px phone, the spine plus the first two tiles are above the fold.

## 4. II.7 — The cost wall

**Job:** show why a model that beats a coin flip still loses money.

- **60 s.** Headline: *"The model beat a coin flip. It never beat the 17–20 bps round-trip."*
  The figure is a `StatTile` pair: measured round-trip cost (spot, by coin) next to the
  flagship's gross per-trade edge (causal), with the difference in clay when negative.
- **Explore.**
  - **Controls:** coin (`sui`, `dash`, `xrp`, `ton`, the dev quartet the costs were measured
    on); venue preset (spot / futures, which snaps the slider to that coin's frozen c_RT); a
    cost slider from 0 to 30 bps.
  - **Chart A** (`Histogram`): the per-trade gross return distribution for the chosen coin,
    with a vertical line at the slider's cost. Trades to its left lose money after costs.
  - **Chart B** (`LineChart`): net per-trade Sharpe (μ − c)/σ as c sweeps 0–30 bps. Markers
    at the spot and futures c_RT, and a dot at the break-even c* = μ.
  - **What to notice:** c* sits left of even the futures cost for every coin. Even the
    cheapest venue is too expensive for the edge.
- **Method.**
  - The cost formula, shown literally:
    `c_RT = 2 × fee/side + 2 × (half-spread p50 at signal-like minutes + 1.0 bp impact)`.
    Where each term came from: the fee per side on E4's frozen cost card, the half-spread from
    order-book minutes in the top-10 % volatility regime, and the impact allowance from p50
    depth at a notional $1,000 size.
  - That slippage was *modelled* (5 bps base), not measured. That
    is the honest caveat.
  - The dir-AUC ≈ 0.6 context: "better than random, but thin and mostly volatility".
- **Claims:** C-E4-cost, C-E4-cost-coin-{sui,dash,xrp,ton}-{spot,fut} (new, `recorded` from the
  frozen cost card), C-E2-auc, C-cost-breakeven-{coin} (new, `recomputed` from `cost_wall_edge`).
- **Lens:**
  - IC: "the estimator is three moments; check it in the console".
  - Lead: "costs were measured and frozen *before* the tune that used them".
  - Manager: "the kill criterion was economic, not statistical".

**P1 delta:** the cost card covers the **dev quartet only** (holdouts were sealed at P1), so
`cost_wall_coin` has 4 rows × 2 venues, not 9. `cost_wall_edge` uses the same 4 coins, from
the causal re-cut panel.

## 5. II.9 — The leakage autopsy ⭐

**Job:** the flagship interview story. The best edge the program ever found came from one
minute of BTC's future. The process found it, measured it, refused to paper over it, and
closed the program on it.

### 5.1 The six beats (one scroll, each beat a sub-section with its own figure)

| # | Beat | Figure | What the reader should take away |
|---|---|---|---|
| 1 | **The edge.** The flagship configuration (cross-coin B1 features) confirmed on holdout coins and a calendar panel | `DotStrip`: per-coin median test Sharpe on the frozen (as-built) panels, all right of zero | "This looked real, and confirmed twice." |
| 2 | **The bug.** The coin grid is keyed by bar *close* time and BTC by bar *open* time, so at time t the feature read the close of BTC's bar [t, t+60): a price that doesn't exist until t+60 | `StepDiagram`: two aligned time axes (coin bars, BTC bars) with the reindex arrow; a toggle *as built* / *causal* slides the BTC axis by one bar | "A one-line indexing convention mismatch, not a modelling error." |
| 3 | **Measured, not argued.** Correlation of the feature with the coin's forward 20 m return | `BarChart`, coin × {as built, causal}: ≈ +0.18–0.20 vs ≈ 0.00. **Scrubber:** shift BTC by −2…+2 minutes; the correlation curve spikes only at the leaking shift | "All of the feature's predictive content was the look-ahead." |
| 4 | **The collapse.** Stage 1 (2 coins, 8 cells): strict median +0.23 → −0.09, 0/8 positive. Stage 2 (9 coins): +0.146 → −0.135, 0/9. A full re-tune on the causal substrate (E4.P7) stays collapsed | `BarChart` small multiples per coin, a toggle animating as-built → causal; the stage-2 panel is the default view | "It didn't shrink. It inverted, everywhere, and re-tuning didn't bring it back." |
| 5 | **What it was worth.** The flip side: knowing BTC's next minute is worth ~25–30 bps/trade, about the whole distance from −0.14 to +0.15 Sharpe | `StatTile` + one sentence | "A leak is also a measurement of information value." |
| 6 | **How it was handled.** Timeline, in date order: found during item E4.P6.6a → recorded as SD-E4-24, *not fixed in place* (the configuration was frozen) → gate decided MARGINAL, and the one allowed extra round was spent on a causal re-cut → reading declared in code *before* the first cell → stage 1 collapses → re-tune authorised → stays collapsed → stage 2 authorised → collapses → NO-GO, E4 closed (the re-tune's place corrected at E9.P0.5, P0 §15) | `Timeline` (the `leak_autopsy_events` table), each event with its commit chip | "The process, not luck, caught it, and the process decided what it meant." |

### 5.2 Honesty layer (Method, and inline where noted)

- **Inline at beat 4:** the stage-1 caveat that the entry itself declared. The hyperparameters
  were tuned on the leaked substrate, so the re-cut ran a misfit model. **Beat 4 then shows
  why that doesn't rescue it:** E4.P7 re-tuned on the causal substrate, and it stayed collapsed.
- The SD entry's own "what this does NOT mean" paragraph is quoted verbatim. At the time, it
  was *not* yet proof that the edge was entirely leak. The honest statement then was "an
  unknown part is unavailable live". The stage 2 and P7 results are what settled it.
- **Attribution (the P0 open item, now resolved as far as the records allow):** the commit
  history shows the finding was made by the agent (Claude Code, Opus) while working item
  E4.P6.6a on 2026-08-03 under the autorun procedure. *Settled at E9.P0.3:* the session was
  interactive, with me present (inventory §1 point 6; `C-E4-024-found`). **Copy:** *"found by the
  agent while building the forward-replay input for item E4.P6.6a, in an interactive session"*.
- The leak also runs through E3's "honest positive". The E3 dossier's §12.3 downgrade is shown
  as a reviewed excerpt, since it isn't an SD entry (corrected at E9.P0.5, P0 §15).
- **"The best edge the program ever found" keeps its meaning through E7** (E9-G0 Q3). Two later
  books posted positive numbers on other scales, and neither beat its null. E5's S3 book was
  positive after cost, but it sat at the 40.8th percentile of its random-entry null
  (C-E5-S3-null). E7's trend book had a positive annualised Sharpe as BTC beta with an
  off-switch, and its timing sat mid-distribution among random entries (C-E7-P2). Neither is on
  II.9's per-trade scale. The Method layer says so in one sentence and links to II.10.

### 5.3 Interaction details

- The substrate toggle is the page's one **global** control: flipping it in beat 3 also flips
  beats 1 and 4. The reader watches the whole edge disappear at once. The URL keeps
  `?substrate=causal` so a shared link lands in the same state.
- The shift scrubber (beat 3) snaps to integer minutes, is keyboard operable (← →), and
  announces "shift +1 minute: correlation 0.00" to screen readers.
- Reduced motion: the transitions become instant swaps.
- Each figure carries its table view and chip. Beat 6 chips link to `/verdicts/sd/SD-E4-24`
  and the stage cards' SD entries.

**Claims:** C-E4-024-corr, C-E4-024-corr-shift (new, `recomputed`), C-E4-024-stage1 (new),
C-E4-024-collapse, C-E4-P7-retune (new), C-E4-024-value, C-E3-lift.
**Lens:**
- IC: "reproduce beat 3's correlations in the console".
- Lead: "freeze first, record the defect, spend the one extra round on the re-cut".
- Manager: "the process killed my own best result, and that's the outcome I'd want from a team".

**P1 deltas:**
1. `leak_autopsy_corr` gains `shift_min ∈ {−2,…,+2}`, which drives the scrubber. It's computed
   in the same precompute pass, so the extra cost is small.
2. A new `leak_autopsy_stage1` table (2 coins × 4 cells × substrate) from the E4.P6.8 card.
3. A new `leak_autopsy_p7` table (the causal re-tune headline per coin) from the E4.P7 outputs.

## 6. III.11 — Timeline & gates

**Job:** the shape of the program at a glance. Each epic had a question, a bar, a signed verdict
and a killing fact. Where the record says a bar came late or went partly unrun, the card says so
(SD-E4-25; amended at Gate E9-G1, P0 §17).

- **60 s.** Headline: *"Each research epic asked one question, set its bar first, and got a signed answer."*
  The figure is a swim-lane `Timeline` from 2026-05 to 2026-10 (E7 closed 2026-10-12):
  - lanes: epics (E0–E7; no lane for a tooling epic, not shown, SD-SC-08);
  - marks: gates (◆), operator sign-offs (✎), PAUSEs (⏸);
  - bands: in-flight phases.
- **Explore.** Click an epic to open a card: question · its bar · verdict glyph ·
  killing fact · links (dossier SD pages, ledger rows). Toggle an overlay of **autorun items**
  (dots on the lane, coloured by reading glyph). This shows the agent's density of work
  against the human gate cadence.
- **Method.**
  - How gates worked: the dossier plus a recommendation, built by the agent, then a pause at
    boundary (d), then my sign-off with a lettered option, recorded verbatim.
  - The E5 family-closing pre-commitment ("on a fourth NO-GO the program family closes
    permanently").
  - After the family closed, E6 and E7 opened as a new program on E5's reopening standard
    (E5 close-out §5), each with its own kill screen and gate. E6 shows a NO-READING held as NO-READING at the gate. E7 shows a KILL accepted with its
    weakest limb disclosed.
- **Claims:** C-epic-{E0…E7}-verdict (new, `recorded`), C-gates-count (new), C-loop-items.
- **Data:** `text/epics.json`, `autorun_items`, `autorun_pauses`, plus gate sign-off events
  (a new small table, `gate_events`, parsed from the ledger's ✓SIGNED OFF rows and commits:
  **P1 delta**).

## 7. III.12 — Verdict ledger

**Job:** every screen and gate, with the number that decided it. It's the proof that
verdicts were mechanical.

- **60 s.** Headline: *"Every verdict, with the one number that decided it and the bar it was held to."*
  The figure is a summary strip: counts by verdict (ADVANCE / KILL / NO-READING / NO-GO), each
  with its status glyph and label. Each word is counted on its own, with no "no" total (§2).
- **Explore.** `LedgerTable`:
  - **Filters (one row):** epic, verdict, class.
  - **Columns:** id · class · verdict (glyph + label) · deciding number(s) vs bar · SD refs
    (links to public SD pages) · commit chip.
  - **Row expand:** the full "deciding numbers" cell and the qualifier.
  - The default sort is chronological; the NO-READING rows carry a one-line reason ("null limb
    unreachable", and so on).
- **Method.**
  - What each verdict word means, and why NO-READING ≠ KILL.
  - The recorded-but-never-decided counterfactuals (S1, S2), shown as *recorded, not verdicts*,
    exactly as the close-out dossier qualifies them. The same holds for E6's limbs (a) and (b)
    ("would KILL", reported under a NO-READING) and for the report-only books (E6's
    DVOL-implied book, E7's V3).
- **Claims:** one per ledger row that shows a deciding number (generated IDs
  `C-ledger-<epic>-<id>`, `recorded`, checked by `contains` against the dossier table).
- **Data:** `verdict_ledger`, `text/sd_entries.json`.

## 8. IV.15 — Loop architecture

**Job:** show that the ledger was worked by an AI agent inside a designed system, not by
prompting and hoping. (Amended at E9.P0.5, P0 §15: it said "most of the ledger was produced by an
autonomous agent", but E4's and E5's early items ran outside the supervisor.)

- **60 s.** Headline: *"One agent session per work item, a supervisor that checks its work, and me at every gate."*
  The figure is a `StepDiagram` of **two nested loops**:
  - **Outer: the supervisor** (in the plugin, Python stdlib), described as of the export
    (E9 §2 row 6). It launches a fresh headless `claude -p` session per item. It
    **independently verifies** every CONTINUE:
    - a commit exists, the prompt advanced, and a ledger line was added;
    - `CHECK_CMD` passes (in binka, the epics' test suites, where E5–E7's carry the seals and
      the hashed bars, plus the exporter's);
    - no frozen or protected path was touched, no test deleted or skipped, and no secret
      committed.

    A read-only verifier reviews the item when it touched the review zones (`REVIEW_ZONES`). The supervisor then applies bounded
    recovery or stops and pages me. Recovery means nudges, infra retries, repair sessions after
    an interruption, and a wait on the subscription's usage limit. Each budget is a claim read
    from `config.env` (C-loop-recovery, C-loop-limit).
  - **Inner: the item procedure** (`autorun:item`, 12 steps):
    0. read the policy
    1. confirm the item
    2. consistency-check it against prior findings
    3. write the plan
    4. implement, without running jobs
    5. quality gate: `/simplify` → `/code-review high`, up to two rounds
    6. commit
    7. run the job in the foreground
    8. analyse, and record any verdict as an SD entry
    9. document trade-offs
    10. checkpoint
    11. advance the prompt block
    12. write `LOOP_CONTROL.json` (CONTINUE / PAUSE / DONE) and stop

    The diagram follows the `autorun:item` skill at the export's plugin commit (the manifest's
    `autorun_plugin_commit`). As of 2026-10-15 that includes backlog mode: step 11 takes the
    next item from `autorun-plan next`, and a boundary opens a card for me instead of a PAUSE.
- **Explore.**
  - Step through the diagram. Each step shows *what it's for* (one line from the plugin's design document),
    *the failure it prevents*, and a real artifact: a commit, a ledger line, a
    `LOOP_CONTROL` example.
  - Below the diagram, an **item strip** from `autorun_items`: one mark per item, coloured by
    reading, sized by cost where known (unknown cost is a hollow mark and never estimated).
  - A short **"how it changed"** strip (E9 §2 row 6). It starts from the loop as first run in E3,
    then shows the `config.env` version blocks:
    - v0.2: per-kind routing, `CHECK_CMD` in the gate, and bounded recovery;
    - v0.3: the repository checks (frozen and protected paths, tests, secrets), the read-only
      verifier, the permission mode with its loop-only settings, and the supervisor pushing;
    - v0.4: the limit wait and repair sessions;
    - then backlog mode (lanes and cards, 2026-10-15).

    Each step names the section of the plugin's design document that explains it, as text, since the plugin stays
    private (SD-SC-05).
- **Method.** The design choices worth a lead's attention:
  - **Fresh session per item.** Context stays small; state lives in files with one job each.
  - **The ledger exists because** the prompt file had grown to 151 KB, 94 % of it superseded
    entries that every session re-read. Moving finished work out cut per-item context
    (C-ledger-context, new, `recorded` from the ledger header).
  - **The supervisor trusts nothing the session says:** it re-checks.
  - **Per-kind model and effort routing**, with budgets per item ($40) and in total ($300) in
    `config.env`.
  - **Extracted into a reusable plugin**, with mechanism and per-repo
    policy split apart.
- **Claims:** C-loop-items, C-loop-sub, C-loop-cost (shown as *API-equivalent, not spent*), C-loop-budget (new), C-ledger-context (new), C-loop-recovery and C-loop-limit (new, `recorded` from `config.env` at the export).
- **Cost framing:** the item strip sizes marks by **API-equivalent** compute, labelled that way on the axis and in the legend. Method explains the difference. The real cost was one flat Claude subscription, and the `config.env` budgets are notional per-item caps. The subscription's usage limits pace the loop: as of the export it waits out a 5-hour limit, for up to `MAX_LIMIT_WAIT` per item (C-loop-limit; 0 when this was designed), and halts on a weekly one. That makes the design point concrete: throughput under a fixed budget, not a metered one.
- **Disclosure:** a `config.env` value that names a tooling epic, not shown, is described, never quoted (SD-SC-09).
- **Lens:**
  - IC: "the supervisor's checks are code, not instructions" (it named the supervisor's source file, which is
    private: P0 §15).
  - Lead: "state in files, one job each; recovery is bounded, not open-ended".
  - Manager: "budgets, gates and an audit trail, like a team with a clear delegation charter".

## 9. IV.16 — Approval boundaries & guard hooks

**Job:** show where autonomy stops, and that the stop is enforced, not requested.

- **60 s.** Headline: *"What the agent may never do alone. Some of it is enforced in code."*
  The figure is one card for each of POLICY's boundaries as of the export, (a)–(g) on 2026-10-15.
  Each card has a one-line rule and a count of real PAUSE events at that boundary, plus the
  cards that named it once backlog mode began (both from `autorun_pauses`):
  - (a) data deletion
  - (b) multi-day jobs
  - (c) any spend
  - (d) program gates
  - (e) any live-box or exchange change, paraphrased without POLICY's note on the live box
    (P0 §10.3)
  - (f) the operator's personal data, in a generic form marked as paraphrased (SD-SC-13)
    (SD-SC-09). Its PAUSEs all belong to the epic that isn't shown, so its card gives no count
    and says so; the other counts cover the epics shown
  - (g) publication and accounts: the agent built this site, but only I can publish it
- **Explore.**
  1. **The PAUSE log:** click a card to see its real PAUSE events. Examples:
     - (d) the E3-G1 gate dossier (2026-07-24);
     - (d) the holdout unseal, "a one-way door" (2026-08-03);
     - (e) the live shadow run, not authorised (E4.P6.6).
     Each shows the agent's recommendation next to my recorded decision.
  2. **Guard-hook tester:** pick a command from `guard_cases`, such as:
     - an `rm -rf` of the pinned 33 GB tree;
     - `pipenv` from the repo root;
     - staging a protected notebook;
     - a harmless `git status`.
     Each case shows the **real** decision, the rule that fired and its message, as produced by
     running the plugin's guard hook with binka's rules (P1). A note explains the split: policy is
     prose the agent reads, and the hook is the part it can't talk its way past.
- **Method.**
  - Which boundaries are prose-enforced (read at step 0, and the supervisor pages on PAUSE)
    vs code-enforced: the guard hook, `CHECK_CMD`, the E5 seal raising `SealViolation`, and,
    as of the export, the supervisor's repository checks and the read-only verifier.
  - "A `PAUSE` names the boundary letter", and since backlog mode a card does too: why that
    makes the audit trail queryable.
  - Decisions at (e) are mine alone and never taken autonomously. The box's current state is
    not on the site (E9-G0 Q6, SD-SC-07).
- **Claims:** C-guard-tests, C-pauses-by-boundary (new, `recomputed` from `autorun_pauses`),
  C-seal-rule (new, `recorded` from `ml/e5_seal.py` docstring).
- **Disclosure check:** the guard cases name real paths (the pinned tree, the notebook). These
  are repo-relative and harmless, but the reviewer confirms them in the excerpt review (P1 §7.3).

## 10. Act intros and hand-offs (copy seeds; final text in `narrative.md`)

- **/science intro:** "The system worked end to end. The question was never *can it trade*,
  but *should it*. These two modules are why the answer was no."
- **/verdicts intro:** "The answer kept being no. Here is how each verdict was reached, and the
  bar it was held to before any data was read."
- **/operating-model intro:** "Most of that ledger was produced by an autonomous agent. Here is
  the system that kept it honest, and where I kept the decisions."
- **/system stub:** the one-diagram pipeline, the live-status sentence, and "the full act ships
  next; meanwhile, the narrative tour is at gridchyn.ai/algo".

## 11. Pre-launch validation

### 11.1 The 60-second test (P0 §8)

- **Who:** 3 people outside the project, ideally one recruiter or HR person, one engineering
  manager and one ML engineer. They get Access invites.
- **How:** open `/` on their own device. After 60 s the tab is closed, and they answer two
  questions: "What is this, in one sentence?" and "What's one thing that stood out about the
  author?"
- **Pass:** 3/3 reproduce the spine's gist (built a system, research said no, the no is
  trustworthy), and ≥ 2/3 name a differentiator (rigor or leak, agent operating model, pre-registration).
- On a fail, revise the spine or tiles and retest with a *new* person. People who have seen it
  are no longer naive.

### 11.2 The poke test

A Staff+ reviewer picks 3 numbers anywhere and traces each via chip → popover → console.
**Pass:** each takes < 2 min and matches.

### 11.3 Launch checklist (all ticked before flipping)

| # | Check | Owner |
|---|---|---|
| 1 | Bundle exported from a clean binka tree; scanner 0 findings; secret-value check ran | agent → operator reads report |
| 2 | Every v0.1 claim `verified`; the release build passes `remark-claims` in strict mode | CI |
| 3 | **Full-site disclosure read:** I read every page in both themes against the deny list (P0 §5.2), especially the guard cases, SD pages and commit-message quotes, and the short-text values the review report lists. It goes on an act card, which only I answer (disclosure policy §5) | operator |
| 4 | Live-status wording is `C-live-status` (P0 §10.3; SD-SC-07) | operator |
| 5 | Playwright + axe green; Lighthouse ≥ 95 on `/`, `/science` (warn-level but targeted) | CI |
| 6 | Phone pass on a real device: no horizontal scroll, toggles reachable, tables scroll inside their frame | operator |
| 7 | Poke test passed. **Fallback 60-second test** (§14.1) run and recorded. The human test is deferred to before P6's announcement | operator / fresh-context readers |
| 8 | GitHub repo: README written as a case study (short v0.1 version; the full one is P6), licence (MIT for code; content © me, CC BY-NC for prose), no binka history, secrets scan on the repo (gitleaks) | agent |
| 9 | `robots.txt` open, sitemap in place, OG image and titles set | agent |

### 11.4 Launch sequence (one sitting, in this order)

1. Merge `main` → `production`; confirm the deploy is behind Access.
2. From the binka checkout, run `showcase scan --repo ~/dev/binka-lab` over the commits to be published, messages
   and author metadata included; it must report no finding. Push only those commits to a **fresh public repo**, and
   keep `binka-lab` private as the lab loop's working repo, since a flipped repo would also show its pull requests,
   CI logs and every commit it still serves by hash. From then on I move each release to the public repo myself,
   after the same scan over the release's commits (disclosure policy §4.9). *This replaces the settled "flip
   `binka-lab` public" (2026-09-30) as a recommendation; I decide at launch (SD-SC-22).*
3. Remove the Cloudflare Access policy from `lab.gridchyn.ai` (keep it on `*.pages.dev`
   previews), and switch `robots.txt` to allow.
4. Check from a logged-out browser and a phone.
5. **igor-web:** add the lab link to `/algo` (a closing "go deeper" callout in Act 7, plus
   the hero) and the CV projects entry. This is a separate igor-web change that ships through
   its own `production` branch.
6. Submit the sitemap to Search Console, since the domain property already exists for `gridchyn.ai`.

LinkedIn, the video and the PDF wait for P6. v0.1 is a soft launch: linked, not announced.

## 12. Work steps

1. **P1 deltas first:** leak corr × shift, `leak_autopsy_stage1`, `leak_autopsy_p7`,
   `gate_events`, cost tables as a 4-coin quartet. Re-export, re-verify claims.
2. Finish `narrative.md` copy for the six modules plus the front door and act intros (P0 had
   seeds). Operator edit pass on the headlines and the spine.
3. Build modules in the order II.9 → II.7 → III.12 → III.11 → IV.15 → IV.16 → front door
   (the front door last, since its tiles quote the others).
4. `/system` stub, `/about` copy.
5. Internal review, then the §11.3 checklist, then the tests in §11.1–11.2.
6. Launch (§11.4).
7. Write the implementation summary and follow-ups (binka-lab `docs/`).

## 13. Exit criteria

1. `lab.gridchyn.ai` is public, with the six modules, front door, about pages and SD pages live.
2. The poke test and the fallback 60-second test have passed and their results are recorded in the P3 summary. The human 60-second test is owed before P6 (SD-SC-04).
3. igor-web `/algo` and the CV link to the lab.
4. There are zero scanner findings on the published bundle, and I have signed off the full-site
   disclosure read.
5. Analytics is receiving data.

## 14. Operator answers (2026-09-30)

1. **Testers:** none available right now. **Fallback (SD-SC-04):** v0.1 soft-launches on the
   poke test plus a *proxy* 60-second test. Three fresh-context model sessions each get only
   a 390 px and a 1440 px screenshot of `/`, with persona prompts (recruiter, EM, ML engineer)
   and the same two questions as §11.1, scored against the same pass bar. It's a weak signal:
   models aren't recruiters, which is why the human test stays **owed before P6's public
   announcement**. A short tester ask can be drafted whenever you want one.
2. **Licence:** MIT for code, CC BY-NC 4.0 for prose.
3. **Cost:** the only real cost was one flat Claude subscription. The `total_cost_usd` values in
   the supervisor logs are Claude Code's API-equivalent figures, not spend. Tile 6 and IV.15
   are reframed around that (§3.1, §8), and the bundle column is `api_equiv_usd`. The fact
   lives in `content/operating_facts.yaml` as `C-loop-sub`. The exact plan name is
   written there by the operator, not inferred.

## 15. Amendments from E9-G0 (2026-10-15)

Applied by E9.P0.1 from [E9](E9_2026-10-15.md) §2 and §8. The rows are in-place fixes. The exporter side is in
P1 §13.

| Change | Why |
|---|---|
| New copy rule: no copy counts the noes, and a verdict chart counts each word on its own (§2, §7) | E9-G0 Q4 |
| The live-bot rule, the "what this is" paragraph and launch check 4 use the past tense, through `C-live-status` (§2, §3.1, §11.3) | E9-G0 Q6; SD-SC-07 |
| The spine is Q4's wording, and the timeline strip runs E0 → E7 with one glyph per epic and no tally (§3.1) | E9-G0 Q3, Q4 |
| Tile 3 was "4 program verdicts, all pre-registered". It becomes "N program gates, each one decided by me", taking tile 6's gate clause. Tile 4's count is `recomputed` over E3–E7, and tile 6 leaves out the items of a tooling epic, not shown (§3.1) | E9-G0 Q4: E6 and E7 made the 4 stale, and a verdict tally under the spine reads as a count of noes. E9 §2 row 3; Q5 |
| The footer has no link to the plugin (§3.1) | E9 §2 row 8; SD-SC-05 |
| II.9's Method says why "the best edge" still holds through E7 (§5.2) | E9-G0 Q3: E7's book posted a higher Sharpe as beta, not edge |
| III.11's headline counts no epics. Its lanes run E0–E7 to 2026-10, and its Method adds E6 and E7 (§6) | E9-G0 Q3 |
| III.12 shows E6's "would KILL" limbs and the report-only books as recorded, not verdicts (§7) | E9-G0 Q3 |
| IV.15 describes the supervisor as of the export, with the "how it changed" strip. Its limits are claims, and config values that name a tooling epic, not shown, are described, not quoted (§8) | E9 §2 row 6; SD-SC-09 |
| IV.16 shows POLICY's boundaries as of the export, (a)–(g), with no count in its headline. Backlog-mode cards join the PAUSE counts, and the repository checks join the Method (§9) | E9 §2 row 6; E9 §4; SD-SC-09 |
| The /verdicts intro counts no noes (§10) | E9-G0 Q4 |

## 16. Amendments from the policy's revision (2026-10-16)

Applied by E9.P0.8 from the revised [`disclosure_policy.md`](disclosure_policy.md). The rows are in-place fixes in
§11.3 and §11.4; the decision record is SD-SC-22.

| Change | Why |
|---|---|
| Row 3's disclosure read also covers the short-text values the review report lists, and it goes on an act card | The data console shows every table row; the decider never answers an act card (the policy's §5) |
| §11.4 step 2: launch pushes the scanned commits to a fresh public repo, and `binka-lab` stays private as the lab loop's working repo; I move each release after its read and the same scan. Recommended in place of the flip; I decide at launch | A public repo shows its pull requests, CI logs and every commit it serves, and a revert can't take a leak out of its history (the policy's §4.9, §6) |
