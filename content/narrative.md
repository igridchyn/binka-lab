# Binka Lab narrative: the spine, the acts and every module (2026-10-16)

**Status: DRAFT; its spine, v0.1 headlines and naming approved at Gate E9-G1 (2026-10-16, decided by autorun; §9).**
The agent wrote it
at E9.P0.5 from [P0 §3](../docs/SHOWCASE_P0_design.md), the
module specs in [P3](../docs/SHOWCASE_P3_design.md) (v0.1) and [P4](../docs/SHOWCASE_P4_design.md) (the later trains), and the claims
in `claims.yaml`. The decision record is SD-SC-16 in the scope log, and
the gate's answer is SD-SC-21. This file moves to binka-lab as `content/narrative.md` at
E9.P2.0, where it is public, so [the disclosure policy](../docs/disclosure_policy.md) binds it.

**What it is.** P3 and P4 say what each module shows, how it works and what it is for. This file says what the site
*says*: the copy at each depth, the claim field behind every number, and why each module matters to each reader (the
lens lines). Every headline, caption, intro, hand-off and lens line in P0 §3, P3 and P4 is a seed that this file
supersedes (P0 §15). E9.P3.2 finishes the v0.1 copy from it, after my edit pass on the headlines and the spine.

---

## 1. How this file works

### 1.1 Every number is a binding

- `[[shown :: C-id.field]]` binds the text shown to a field of a claim in `claims.yaml`. A range or a change names two
  fields: `C-id.field,field`. E9.P3.2 turns each one into `<Claim id=… field=…/>` tags (P2 §5.3).
- A verified claim's numbers are its field's values, rounded only for display. Nothing here is re-derived.
- A draft claim shows as `[[N :: C-id]]` until the item its `pending` names verifies it. Copy that depends on a draft
  carries that binding in its own sentence, so the sentence fails the check once the value exists and must be
  rewritten from it.
- A wording claim (`C-live-status`, `C-meta-lesson`) is quoted whole, with no field.
- Outside a binding there are no digits, except in names: dates, section marks, ids that start with a capital letter
  (epics, items, gates, SD entries, modules, replays, limbs), release tags, code spans, and a numbered part of a source
  ("point 8", "beat 6", "stage 2"). A count that is one of a claim's values is bound even when it is written as a
  word ("eight cells"). The lint can't tell such a word from a structural one ("three depths"), so the review checks
  it.
- `py/showcase/tests/test_narrative_md.py` (in binka's CHECK_CMD) checks all of this against the register. After
  E9.P3.2, binka-lab's `remark-claims` takes over, with the same digit rule (P2 §5.3 as amended).

### 1.2 Copy rules

P3 §2's rules bind every module. This file applies them with three additions:
- **The agent's naming.** Where the copy names the agent for the whole program, it is "Claude Code (mostly Opus)", and
  where a passage is about Opus-era work, such as II.9's discovery, it is "Claude Code (Opus)". The commits' co-author
  lines, where a commit has one, mostly name Opus models, with Sonnet and Fable models on parts of E2 to E5's work;
  May's commits (E0 and E1) have none (Gate E9-G1, D4d (A); SD-SC-21). P0 §10's "running under my autorun supervisor"
  holds after Gate E5-G1 (2026-09-27). Before that gate the supervisor ran only from 2026-07-24 to 2026-08-03, for
  E3's last items and E4.P6.1, and I started the agent's sessions myself for the rest of the work. Where the copy is
  about that work, it says so (P3 §2 as amended; SD-SC-16).
- **Nothing from the record is quoted here.** An SD body, a dossier passage, a log line and a transcript are pointed
  to by id, and each crosses through its own review (policy §4.2, §4.4, §4.6).
- **Planning notes stay out of the copy.** A module's `Open:` field holds what is still to be settled, so that
  E9.P3.2 can lift the copy layers as they are.

### 1.3 Lens lines

P5 §3.2's rules: at most thirty-five words, first person, one point, at most one bound number, never a restatement of
the headline. IC is method and evidence, Lead is judgement and the team pattern, Manager is risk, cost, governance
and delegation. These are the drafts E9.P5.2 finishes, one note per module per lens. The front door, the `/system`
stub and `/lessons` have none.

### 1.4 The module template

P0 §3.2's template, with the names the site uses (P2 §6.2):

```
### <id> <Title> · <release>
- 60 s:    the headline (≤ 15 words), the one figure, and its takeaway
- Explore: what the reader manipulates, and what to notice
- Method:  method, the caveats (the qualifiers), the public links (SD pages, reviewed excerpts)
- Lens:    IC / Lead / Manager
- Claims:  exactly the register's claims whose `modules` name this module
- Data:    the bundle tables (names only; P1 §5 and P4 §10 define them)
- Next:    the hand-off to the next module in its act
- Open:    what is still to be settled (only where something is)
```

The release is the train that ships the module: v0.1 (P3), then v0.2, v0.5, v0.7 and v0.9 (P4 §1). The ids P4 plans
for later modules are in P4's own Claims lines, and P4.E2–E9 add them to the register as their tables land (SD-SC-15).

---

## 2. The spine, the act intros and the hand-offs

- **Spine** (E9-G0 Q4; the front door's display type): I built an ML trading system, then ran a pre-registered research program on it that kept saying no. Here is why you should believe the no.
- **Act intros.** Each act page opens with the hand-off into it, plus one sentence of its own (P2 §6.1).
  - `/system`, Act I: This is the machine: a C++ collector, a feature and label pipeline, GPU training with tracked
    experiments, and a live inference-and-execution path. igor-web's `/algo` tells it gently; this act is the
    engineer's version.
  - `/science`, Act II: *I → II* + "This act is how the answer was reached."
  - `/verdicts`, Act III: *II → III* + "Each verdict is shown against its bar, and where the record says a bar was
    set late or left partly unrun, the ledger says so too."
  - `/operating-model`, Act IV: *III → IV* + "The agent is Claude Code (mostly Opus). This act is about the loop it ran in
    under my autorun supervisor: after Gate E5-G1, and before it for E3's last items and E4.P6.1. For the rest of the
    work up to that gate, I started its sessions myself."
  - `/lessons`: *IV → Lessons* + "The program closed. What it taught me about running research with agents is the
    part I'd take to any team."
- **Hand-offs** (the footer of each act page):
  - I → II: The system worked end to end. The question was never *can it trade*, but *should it*.
  - II → III: The answer kept being no. Here is the ledger of how each verdict was reached.
  - III → IV: I worked that ledger with an AI agent, under rules I wrote. Here is how it was kept honest.
  - IV → Lessons: What transfers to a team of humans and agents.

---

## 3. The front door

### Front door (`/`) · v0.1

The layout, the above-the-fold rule and what the page must never show are P3 §3's.

- **60 s**
  - Eyebrow: Binka Lab · an ML research program, end to end
  - Spine: I built an ML trading system, then ran a pre-registered research program on it that kept saying no. Here is why you should believe the no.
  - Timeline strip: one band per epic, each with its glyph and label, and no tally (P0 §3.1; P2 §4.2's status
    roles). A click opens its III.11 card.
    - E0: [[✓ fixes shipped :: C-epic-E0-verdict.glyph,verdict]]
    - E1: [[✓ infra shipped :: C-epic-E1-verdict.glyph,verdict]]
    - E2: [[✗ NO-GO :: C-epic-E2-verdict.glyph,verdict]]
    - E3: [[✗ NO-GO :: C-epic-E3-verdict.glyph,verdict]]
    - E4: [[✗ NO-GO :: C-epic-E4-verdict.glyph,verdict]]
    - E5: [[✗ NO-GO :: C-epic-E5-verdict.glyph,verdict]], with the band labelled
      [[family closed :: C-epic-E5-verdict.label]]
    - E6: [[⛔ NO-READING :: C-epic-E6-verdict.glyph,verdict]]
    - E7: [[✗ KILL :: C-epic-E7-verdict.glyph,verdict]]
  - Six tiles, each a `StatTile` with its chip, in two rows of three:
    - [[+0.15 → −0.14 :: C-E4-024-collapse.as_built_strict_median,causal_strict_median]] per-trade Sharpe when one
      minute of look-ahead was removed. Links to II.9.
    - [[17–20 bps :: C-E4-cost.spot_min_bps,spot_max_bps]] round-trip cost the model had to beat. Links to II.7.
    - [[7 :: C-gates-count.gates]] program gates and [[12 :: C-gates-count.sign_offs]] sign-offs, each one mine. Links
      to III.11.
    - [[148 :: C-SD-count.total]] scope decisions logged. Links to III.12's SD pages in v0.1, and to III.13 from v0.7.
    - [[6 :: C-arch-families.families]] model families benchmarked; the ceiling was the information. Links to the
      ledger's E2 rows in v0.1, and to II.8 from v0.2. The count is the claim's: E9.P1.1 found no MLP arm in the
      shared schema (SD-SC-15, SD-SC-19).
    - [[73 :: C-loop-items.items]] agent items on [[one :: C-loop-sub.subscriptions]] flat Claude subscription. Links to
      IV.15. "Agent items", not "autonomous" ones (SD-SC-15).
- **Explore**
  - Hovering a tile or a band shows its source (the provenance chip).
  - Choose your path: three cards. Each sets the lens and opens its first stop, with a reading time computed at
    build (P5 §4.1):
    - IC / Staff engineer: "Try to break a number." Leakage autopsy → Cost wall → the data console.
    - Tech lead: "How the program was run: gates, a leak caught, a loop with rules." Timeline & gates → Leakage
      autopsy → Loop architecture.
    - Manager / director: "Where the agent stops, and I decide." Timeline & gates → Boundaries & hooks → Verdict
      ledger.
- **Method**
  - What this is (one paragraph, first person; the agent's first full naming on `/`): I built binka, an ML system for
    trading crypto: a C++ collector, a feature and training pipeline, and a live inference-and-execution path.
    [[It ran live on Binance: it scored coins every second and placed real orders when a prediction cleared its threshold. It never made money. Act II shows why. :: C-live-status]]
    I ran a pre-registered research program on it with an AI agent, Claude Code (mostly Opus), working under rules I wrote:
    in sessions I started for most of the work up to E5's first gate, and mostly under my autorun supervisor after
    it. The program closed every direction it tested. This lab shows how each verdict was reached, and how it was kept honest.
  - Footer: igor-web `/algo` ("the narrative version"), the CV, and the GitHub repo `binka-lab`. No link to the
    plugin while it is private (SD-SC-05).
- **Claims:** C-E4-024-collapse, C-E4-cost, C-gates-count, C-SD-count, C-arch-families, C-loop-items, C-loop-sub,
  C-live-status, C-epic-E0-verdict, C-epic-E1-verdict, C-epic-E2-verdict, C-epic-E3-verdict, C-epic-E4-verdict,
  C-epic-E5-verdict, C-epic-E6-verdict, C-epic-E7-verdict
- **Data:** `text/epics.json`, `claims.json`

---

## 4. Act I — The system

### `/system` stub · v0.1

- **60 s**
  - One screen (P3 §1, §10): the pipeline in one diagram (the exchange's streams → bintri, the C++ collector → a
    per-second archive → one-minute and five-minute bars → features → labels → models → the live path), the
    live-status line, and "The full act ships in a later release. Meanwhile, the narrative tour is at
    gridchyn.ai/algo."
  - Live-status line: [[It ran live on Binance: it scored coins every second and placed real orders when a prediction cleared its threshold. It never made money. Act II shows why. :: C-live-status]]
- **Claims:** C-live-status
- **Data:** none (the diagram is authored)

### I.1 Data & collector · v0.9

- **60 s**
  - Headline: A C++ collector records [[N :: C-secondwise-cols]] columns per coin each second; the pipeline logs its health.
  - Figure: the pipeline as a `StepDiagram`, from the exchange's streams through bintri to the per-second archive,
    the bars and the datasets.
  - Takeaway: The data was engineered, and its health was measured at every step.
- **Explore**
  - Step through the pipeline.
  - A dataset-health table per coin: rows, time range, NaN share and timestamp gaps, from each build's
    `dataset.log`.
- **Method**
  - The secondwise pipelines reuse the one-minute scaler, so training, validation, test and backtest share one
    feature scale (E1).
  - The research data's own gaps and outages are method, so they are shown (policy N3). The collector's hosts and
    transport are infrastructure, and they stay out (N2).
- **Lens**
  - IC: Every dataset build writes its own health log, so a gap or a NaN region shows in the table before it can
    show up in a result.
  - Lead: I made the dataset builds reproducible before I trusted any model trained on them. That infrastructure
    epic is why later datasets could be rebuilt from their logs.
  - Manager: The data foundation was its own epic with a shipped result, so the research epics spent their time on
    questions, not on rebuilding inputs.
- **Claims:** C-secondwise-cols
- **Data:** `pipeline_stats`
- **Next:** I.2. "The raw columns become features."
- **Open:** the column count, from a per-second archive's header at E9.P4.E9. P4's draft headline had a number no
  record supports yet (SD-SC-15).

### I.2 Features · v0.9

- **60 s**
  - Headline: Three indicator libraries, cut to [[N :: C-features-final]] features, with every drop explained.
  - Figure: a funnel bar: raw features per library → decorrelation drops → merged → the final set before and after
    its drift drop (C-features-final's qualifier).
  - Takeaway: The final feature set is the output of written rules, not a hand-picked list.
- **Explore**
  - A sortable feature table: family, library and importance (the `p27` rankings).
  - The merge of one-minute and five-minute features, with the shift that keeps a five-minute bar's values out of
    the minutes before it closes. It is a small diagram, and it foreshadows II.9.
- **Method**
  - The drop lists are code (`ml/feature_lists.py`), and the exporter parses them rather than importing them.
  - The final count is shown at both steps, before and after the drift drop, from the claim (SD-SC-15).
- **Lens**
  - IC: Each feature's path from its library to the final set is in code, including the rule that dropped it, and
    the table reads those lists directly.
  - Lead: I cut features by rules written before the cut (correlation, importance, drift), so nobody could tune the
    feature set toward a result.
  - Manager: The feature set is documented down to each drop, so a new engineer can audit it without asking me.
- **Claims:** C-features-final
- **Data:** `feature_catalog`
- **Next:** I.3. "Features need a target. The label defines what a good trade is."

### I.3 Labels · v0.9

- **60 s**
  - Headline: The label is the barrier touched first. Wider take-profits raised AUC, not the economics.
  - Figure: the label-geometry `Heatmap`: take-profit × stop-loss for each horizon, toggling between dir-AUC and the
    precision margin.
  - Takeaway: A better classification score didn't mean a better trade.
- **Explore**
  - An illustrative touch-label animation: a price path, the take-profit and stop-loss bands and a window, with the
    label assigned. It is labelled illustrative (P1 §4's `min_time_grain` exception).
  - The geometry heatmap, and the stage-2 economics table.
- **Method**
  - Asymmetric touch labels: whichever of the up and down margins the price touches first within the forward window
    sets the label.
  - E2's label sweep found every geometry negative after costs on folds with enough trades
    (C-E2-labels-auc-vs-econ).
- **Lens**
  - IC: The heatmap shows AUC and the economics side by side for each geometry, so the gap between the two is
    visible cell by cell.
  - Lead: I judged label designs on the economics, not on the classification score, because the score was the
    number that could improve while the strategy didn't.
  - Manager: Choosing the right metric was a decision with money attached: a model can look better on paper while
    the business case stays negative.
- **Claims:** C-E2-labels-auc-vs-econ
- **Data:** `label_geometry`
- **Next:** I.4. "Then the models, and how they were trained without fooling themselves."
- **Open:** the headline asserts what the label sweep's claim will show ([[N :: C-E2-labels-auc-vs-econ]] until
  E9.P4.E9 verifies it).

### I.4 Models & training · v0.9

- **60 s**
  - Headline: Walk-forward folds, per-fold tuning, and a GPU pin so no driver fault changes numbers silently.
  - Figure: the walk-forward fold diagram, with the train, validation and test windows of each fold.
  - Takeaway: Selection used validation data, and the record names the exceptions.
- **Explore**
  - The fold diagram, and the hyperparameter-search protocol card.
  - The device-pin story: a lost GPU silently moved training to the CPU and changed every number, so every compute
    step now checks the device it resolved and fails loudly (C-device-pin).
- **Method**
  - Selection uses validation only.
  - SD-E4-29 records the fault and SD-E4-31 the pin. The implicit device default stayed in frozen source
    (C-device-pin's qualifier).
- **Lens**
  - IC: The device check runs inside every compute step, so a fallback to the CPU stops the run instead of quietly
    changing the numbers.
  - Lead: When an environment fault changed results without an error, I made the failure loud and permanent instead
    of fixing that one run.
  - Manager: A silent infrastructure fault is a research risk. This one was caught, recorded and closed with a
    guard, not a workaround.
- **Claims:** C-device-pin
- **Data:** `mlflow_summary`
- **Next:** I.5. "Training at this scale needs tracking and jobs that survive."
- **Open:** the device-pin story rests on its claim ([[N :: C-device-pin]] until E9.P4.E9 finds its recording
  commits).

### I.5 MLOps · v0.9

- **60 s**
  - Headline: Self-hosted experiment tracking, reproducible datasets, and long jobs that survive crashes.
  - Figure: the MLflow layout, with [[N :: C-mlflow-runs]] runs counted from a pinned snapshot.
  - Takeaway: The experiments are tracked, and the long jobs recover.
- **Explore**
  - The experiment layout: a main experiment and per-fold ones for each coin, session and bracket, with the tag keys.
  - The resumability pattern (per-coin partial results), OOM protection, and the content fingerprint on every
    artifact.
- **Method**
  - The snapshot holds aggregates and tag keys only, never tag values, artifacts or models, and I run it, because it
    needs credentials (policy §4.7).
  - The tracking server's host is infrastructure (N2).
- **Lens**
  - IC: Every artifact carries a content fingerprint, so a result on this site points at the exact file that
    produced it.
  - Lead: I made long jobs resumable by default, because a crash several hours in costs a day and tempts you to
    trust a partial result.
  - Manager: Self-hosted tracking kept the experiment history in my hands at a fixed cost, and it is what the
    provenance on this site is built on.
- **Claims:** C-mlflow-runs
- **Data:** `mlflow_summary`
- **Next:** I.6. "Finally, the path that ran live."

### I.6 Live inference · v0.9

- **60 s**
  - Headline: [[It ran live on Binance: it scored coins every second and placed real orders when a prediction cleared its threshold. It never made money. Act II shows why. :: C-live-status]]
  - The headline runs past the fifteen-word rule, and my wording wins (P4 §7).
  - Figure: a `FeedSnapshot`: when the feed last published and which coins it covered, labelled with the newest
    point's timestamp. It shows no price, confidence, direction or threshold (SD-SC-12).
  - Takeaway: It was a real pipeline, and the site makes no claim about its returns.
- **Explore**
  - The live path's architecture: `bintri -monitor` → `get_rich` → exchange orders, and the feed server → the
    public feed.
  - The streaming causal head, certified against the frozen batch head (E4.P6.6 prep, `56cfc03`).
- **Method**
  - The site shows no live P&L, balance, position, fill or trade count, and it shows the feed's state only as the
    dated snapshot (policy N3).
  - The snapshot is a pinned file, captured once, and the export never calls the feed (P4 §8).
- **Lens**
  - IC: The streaming head was certified against the frozen batch head, the check a live path needs before it can
    serve the features the research measured.
  - Lead: I describe the live path by its architecture and one past-tense sentence, and make no claim about what it
    earned.
  - Manager: The site states one fact about the live system and no performance figures, by policy, so nothing on it
    can be read as a returns claim.
- **Claims:** C-live-status
- **Data:** `feed_snapshot`
- **Next:** Act II, through the I → II hand-off.

---

## 5. Act II — The science

### II.7 The cost wall · v0.1

- **60 s**
  - Headline: The model beat a coin flip. Its causal edge didn't cover the [[17–20 bps :: C-E4-cost.spot_min_bps,spot_max_bps]] round-trip.
  - Figure: a `StatTile` pair for each coin: its measured spot round-trip cost, next to the flagship's gross
    per-trade edge on the causal substrate, its break-even cost c\*. The gap is in clay where it is negative. The
    four values, as mean log returns: sui [[+1.63 :: C-cost-breakeven-sui.c_star_bps]], dash
    [[+11.38 :: C-cost-breakeven-dash.c_star_bps]], xrp [[−0.27 :: C-cost-breakeven-xrp.c_star_bps]], ton
    [[+2.59 bps :: C-cost-breakeven-ton.c_star_bps]].
  - Takeaway: Better than chance is not enough when every round trip costs this much.
- **Explore**
  - Controls: the coin (the dev quartet the costs were measured on: sui, dash, xrp and ton); a venue preset (spot or
    futures), which snaps the slider to that coin's frozen cost; and a cost slider.
  - Chart A, a `Histogram`: the coin's per-trade gross returns on the causal substrate, with a line at the slider's
    cost. Trades left of it lose money after costs.
  - Chart B, a `LineChart`: the net per-trade Sharpe, (μ − c)/σ, as the cost sweeps. It has markers at the coin's
    spot and futures costs (C-E4-cost-coin-sui-spot and its siblings) and a dot at break-even, c\* = μ.
  - Notice: where c\* sits against each venue's cost. P3 §4 expects it left of even the futures cost on every coin
    It is, on all four (sui [[+1.63 :: C-cost-breakeven-sui.c_star_bps]] against its futures
    [[11.37 bps :: C-E4-cost-coin-sui-fut.c_rt_bps]]).
- **Method**
  - The cost model, shown literally as the per-coin claims' qualifier gives it: a round trip pays the fee on each
    side, plus twice the sum of the half-spread at signal-like minutes and an impact allowance.
  - Where each term came from: the fee per side on E4's frozen cost card; the median half-spread at the most volatile
    minutes; and an impact allowance at a notional position size (policy N7: sizes are notional, and the copy says
    so).
  - Slippage was modelled, not measured. That is the caveat, and no figure from the live account is quoted (policy
    N3; SD-SC-15).
  - The costs were measured and frozen at E4.P1 (2026-07-31), before the tune that used them. The spread window
    runs from 2025-01-01 to the freeze, across the windows E5 sealed later; it predates the seal, so it crosses with
    its window labelled (N5 rule 4).
  - Futures were about [[5.2 :: C-E4-cost.futures_saving_bps]] bps cheaper per coin, with funding counted in their
    cost.
  - dash's order book was thin against the notional position, so its impact allowance is the least safe
    (C-E4-cost-coin-dash-spot's qualifier).
  - The dir-AUC context: [[≈ 0.6 :: C-E2-auc.dir_auc_approx]], better than random but thin, and most of its
    precision lift was volatility timing. It comes from one baseline model at one label geometry (C-E2-auc's
    qualifier).
  - The as-built substrate, which carried the look-ahead, did clear the cost. II.9 is why that doesn't count.
- **Lens**
  - IC: The break-even point comes from three moments of the per-trade returns, so every curve on this page is one
    query in the data console.
  - Lead: I had the costs measured and frozen before the tune that used them, so the economics couldn't drift
    toward a pass.
  - Manager: The kill criterion was economic, not statistical: a model that beats chance still has to pay for every
    trade.
- **Claims:** C-E4-cost, C-E4-cost-coin-sui-spot, C-E4-cost-coin-sui-fut, C-E4-cost-coin-dash-spot,
  C-E4-cost-coin-dash-fut, C-E4-cost-coin-xrp-spot, C-E4-cost-coin-xrp-fut, C-E4-cost-coin-ton-spot,
  C-E4-cost-coin-ton-fut, C-cost-breakeven-sui, C-cost-breakeven-dash, C-cost-breakeven-xrp, C-cost-breakeven-ton,
  C-E2-auc
- **Data:** `cost_wall_coin`, `cost_wall_edge`
- **Next:** II.8 from v0.2: "Was the learner the limit? The bake-off says no." In v0.1, II.9: "One configuration did
  clear this wall. The next module is why it doesn't count."
- **Open:** settled: the fee term (SD-SC-13 point 8). At the G1 repeat (2026-10-24) I signed the policy with
  option (A): the fee per side is shown on its own, as N2's one carve-out, and the words that tied it to the account
  are gone from the claims, Method and P3 §4 (C6). The Notice line was rewritten from c\*'s values at
  E9.P1.7.

### II.8 Model bake-off & tabular saturation · v0.2

- **60 s**
  - Headline: [[6 :: C-arch-families.families]] model families, one answer: the features, not the learner, set the ceiling.
  - Figure: a `DotStrip`, one row per family (logistic, LightGBM, XGBoost as the control, AutoGluon, TabM, TabICL;
    no MLP row: E9.P1.1 found none in the shared schema, SD-SC-19). Each dot is a coin × fold median test Sharpe,
    with a zero line and the control's median as a reference line.
  - Takeaway: Swapping the learner moved the result less than the folds did.
- **Explore**
  - Selectors: the metric (test Sharpe, the gap from validation to test, dir-AUC where logged), the head variant, and
    the coin.
  - "How much of the lift is volatility timing?": a volatility timer alone reproduced a median
    [[93 % :: C-E2-stage0-voltimer.median_share]] of the models' precision lift.
  - Notice: logistic regression reaches [[N :: C-E2-logistic-ratio]] of XGBoost's Sharpe.
- **Method**
  - The bake-off protocol: the XGBoost control in every comparison; Bar A, a paired-bootstrap interval of the
    difference above zero against the control; Bar B, a positive median on traded folds.
  - The two priors: saturation, and threshold transfer beating ranking. The dead-list entries this closed.
  - The external deep-search survey that produced the shortlist.
  - The logistic ratio compares two losing numbers (its qualifier). Models run on other protocols, such as the live
    bot's PyTorch MLP and E3's frozen-representation screens, are not counted (C-arch-families' qualifier).
  - The dir-AUC baseline is II.7's (C-E2-auc).
- **Lens**
  - IC: The control is in every comparison and the bars are paired against it, so a family only wins by beating
    XGBoost on the same folds.
  - Lead: When the families agreed, I stopped searching architectures and moved the question to the information.
    That pivot became E3.
  - Manager: A broad, cheap benchmark settled where not to spend the next stretch of effort, which is the main
    thing a bake-off is for.
- **Claims:** C-E2-auc, C-arch-families, C-E2-stage0-voltimer, C-E2-logistic-ratio
- **Data:** `arch_bakeoff`, `stage0_diag`
- **Next:** II.9. "Changing the information did produce one edge. Here is where it came from."
- **Open:** the takeaway and P4's expectation, that the spread between families is smaller than the spread between
  folds, are written from `arch_bakeoff` at E9.P4.E2.

### II.9 The leakage autopsy ⭐ · v0.1

- **60 s**
  - Headline: The program's best edge, [[+0.15 :: C-E4-024-collapse.as_built_strict_median]] per-trade Sharpe, came from one minute of BTC's future.
  - Figure: beat 1's `DotStrip`, under the page's substrate toggle (as built / causal).
  - Takeaway: The process found the leak, measured it, and let it decide the epic.
- **Explore**: the six beats, one scroll, each with its figure. The substrate toggle is the page's one global control.
  1. **The edge.** Before the leak was found, the frozen flagship configuration (cross-coin features) confirmed
     twice: [[+0.1856 :: C-E4-P6-confirm.holdout_strict_median]] median test Sharpe on the holdout coins, then
     [[+0.1461 :: C-E4-P6-confirm.calendar9_strict_median]] on a calendar panel where
     [[9 of 9 :: C-E4-P6-confirm.calendar9_coins_positive,coins]] coins were positive.
     - Figure: a `DotStrip` of each coin's median test Sharpe on the frozen panels, all right of zero.
     - Takeaway: This looked real, and it confirmed twice.
  2. **The bug.** The coin grid was keyed by each bar's close time, and BTC's series by its open time. So at time
     `t` the feature read the close of BTC's bar `[t, t+60)`, a price that didn't exist until `t+60`.
     - Figure: a `StepDiagram` of two aligned time axes, coin bars and BTC bars, with the reindex arrow. The toggle
       slides BTC's axis by one bar.
     - Takeaway: An indexing convention mismatch with a one-line fix, not a modelling error.
  3. **Measured, not argued.** As built, the feature correlated [[+0.18 to +0.20 :: C-E4-024-corr.as_built]] with
     the coin's return over the next [[20 minutes :: C-E4-024-corr.horizon_min]]; read causally,
     [[≈ 0.00 :: C-E4-024-corr.causal]].
     - Figure: a `BarChart`, coin × {as built, causal}, with a scrubber that shifts BTC a minute or two either way
       (as built, [[+0.1259 to +0.1745 :: C-E4-024-corr-shift.as_built_at_0_min,as_built_at_0_max]] from the
       moment the feature reads BTC's future, and at most [[0.01 :: C-E4-024-corr-shift.as_built_before_0_max_abs]]
       a minute before). Caption, for the one-minute feature: "The correlation appears the moment the feature reads
       BTC's future, and not a minute before." The curve is a step, not P3's spike: every later reading of BTC is
       still inside the forward window (SD-SC-28).
     - SD-E4-24 measured sui, xrp and eth on a recent slice. The bars for every coin are the exporter's recompute,
       with E5's sealed rows stripped first (N5 rule 2).
     - Takeaway: All of the feature's predictive content was the look-ahead.
  4. **The collapse.** Stage 1 (dash and sui, [[eight :: C-E4-024-stage1.cells]] cells): strict median
     [[+0.2312 → −0.0906 :: C-E4-024-stage1.as_built_strict_median,causal_strict_median]], with
     [[0 of 8 :: C-E4-024-stage1.cells_positive,cells]] cells positive. Stage 2
     ([[nine :: C-E4-024-collapse.coins]] coins):
     [[+0.1463 → −0.1353 :: C-E4-024-collapse.as_built_strict_median,causal_strict_median]], with
     [[0 of 9 :: C-E4-024-collapse.causal_coins_positive,coins]] coins positive. A full re-tune on the causal
     substrate (E4.P7) stayed collapsed, at a strict median of [[−0.1407 :: C-E4-P7-retune.retuned_strict_median]].
     - Figure: `BarChart` small multiples per coin; the toggle animates as built → causal. Stage 2 is the default
       view.
     - Inline caveat, which the entry declared before the run: stage 1's hyperparameters were tuned on the leaked
       substrate, so it ran a misfit model. The re-tune answers that: tuned on the causal substrate, the edge stayed
       collapsed.
     - Takeaway: It didn't shrink. It inverted, everywhere, and re-tuning didn't bring it back.
  5. **What it was worth.** Knowing BTC's next minute was worth about
     [[25–30 bps :: C-E4-024-value.ev_bps_per_trade]] of expected value a trade: roughly the whole distance from
     [[−0.14 to +0.15 :: C-E4-024-value.sharpe_span]] Sharpe.
     - Figure: a `StatTile` and one sentence.
     - It is an upper bound on what an honest fast path could capture, not an existence proof (the qualifier).
     - Takeaway: A leak is also a measurement of information value.
  6. **How it was handled.** A `Timeline` from `leak_autopsy_events`, in date order, each event with its commit
     chip:
     - 2026-08-03: the agent, Claude Code (Opus), found it while building E4.P6.6a's forward replay, in an
       interactive session with me present (`b04193d`; C-E4-024-found). It was recorded as SD-E4-24 and not fixed in
       place: the configuration was frozen, and changing it would have turned the confirmation into a new
       configuration.
     - 2026-08-03: the program verdict (E4.P6.7) was decided MARGINAL, and I spent the epic's one extra round on a
       causal re-cut (`097ac5e`).
     - 2026-08-03: the re-cut's reading was committed in code before its first cell (`c973274`).
     - 2026-08-04: stage 1 collapsed (`88ec6dc`). The record built on the leaked substrate was impeached, and the
       re-decision came back to me (SD-E4-26).
     - 2026-08-05: I deferred the re-decision and authorised a re-tune on the causal substrate, E4.P7 (`48be9d2`;
       SD-E4-27).
     - 2026-08-09: the re-tune's reading was committed in code before its first cell (`64aa7b6`).
     - 2026-08-10: the re-tune stayed collapsed (`e176bcb`).
     - 2026-08-11: stage 2 was pre-registered (SD-E4-32), authorised (`4ddc546`; SD-E4-33) and run. It collapsed
       on all its coins (`68c917e`).
     - 2026-08-12: Gate E4-G2 was re-decided NO-GO, and E4 closed (`65abb0d`; SD-E4-35).
     - Takeaway: A forward-replay build caught it, and the process decided what it meant.
- **Method** (the honesty layer)
  - Which number is the edge: the headline and the front-door tile use stage 2's as-built median on the full panel
    of [[nine :: C-E4-024-collapse.coins]] coins, because its causal twin was measured on the same cells. The
    holdout (beat 1) and stage 1's dev coins, dash and sui (beat 4), read higher on fewer cells.
  - Attribution: the agent found the leak while building the forward-replay input for item E4.P6.6a, in an
    interactive session with me present. That is inferred from the record: the commits record my sign-offs in that
    session the same day, and the supervisor launched nothing that day after midnight (C-E4-024-found's qualifier).
  - SD-E4-24's own "What this does NOT mean" paragraph, verbatim, from its reviewed SD page (policy §4.2). At the
    time the entry was not proof that the edge was all leak: an unknown part was unavailable live. The re-tune and
    stage 2 settled it. E4's close-out puts it formally: the edge was not separable from the look-ahead.
  - The windows: the calendar panel (2025-10-02 → 2026-06-30) and SD-E4-24's slice overlap the windows E5 sealed
    later. They predate the seal (ratified 2026-08-12) and cross with their windows labelled (N5 rule 4; the claims'
    qualifiers).
  - The re-tune's first sweep ranked on too few cells and was discarded (SD-E4-30), and the compute device was
    pinned after a lost GPU (SD-E4-29, SD-E4-31). The re-tune's number is the second sweep's (C-E4-P7-retune's
    qualifier).
  - E3's "honest positive" carried the same leak: its cross-coin lift of [[+0.08 to +0.10 :: C-E3-lift.lift]] over
    the [[−0.137 :: C-E4-floor.median_test_sharpe]] floor was measured on the leaked substrate. The E3 dossier's
    §12.3 downgrades it, and it is shown as a reviewed excerpt, since it isn't an SD entry.
  - "The best edge" keeps its meaning through E7 (E9-G0 Q3). E5's short-volatility book was positive after cost,
    but it sat at the [[40.8th :: C-E5-S3-null.percentile]] percentile of its random-entry null. E7's trend book had
    a positive annualised Sharpe as BTC beta with an off-switch, and its timing sat mid-distribution among random
    entries (C-E7-P2). Neither is on this page's per-trade scale (II.10).
  - Interaction (P3 §5.3): `?substrate=causal` keeps the toggle's state in a shared link. The scrubber snaps to
    whole minutes, works from the keyboard and announces its value. Reduced motion swaps states instantly. Every
    figure has its table view and chip, and beat 6's chips link to `/verdicts/sd/SD-E4-24` and the stage cards'
    SD entries.
- **Lens**
  - IC: Rerun the as-built and causal correlations in the data console. The whole effect sits in one alignment
    choice, and the causal feature carries nothing.
  - Lead: The configuration was frozen first, the agent recorded the defect instead of patching it, and I spent the
    one extra round on a causal re-cut.
  - Manager: The process killed my own best result. That is what I'd want from a team: the rules decided, not the
    person with the most riding on the answer.
- **Claims:** C-E4-024-collapse, C-E4-024-corr, C-E4-024-corr-shift, C-E4-024-stage1, C-E4-P6-confirm,
  C-E4-P7-retune, C-E4-024-value, C-E3-lift, C-E4-floor, C-E5-S3-null, C-E7-P2, C-E4-024-found
- **Data:** `leak_autopsy_coin`, `leak_autopsy_corr`, `leak_autopsy_stage1`, `leak_autopsy_p7`,
  `leak_autopsy_events`, `text/sd_entries.json`
- **Next:** II.10 from v0.2: "The leak closed the touch-trading family's best lead. The next screens changed the
  strategy class itself." In v0.1, the II → III hand-off.

### II.10 Null models & the strategy-class screens, E5–E7 · v0.2

- **60 s**
  - Headline: Each new strategy class was held to a bar written before its data.
  - Figure: one card per screen, grouped by epic: E5's [[six :: C-E5-screens.screens]] classes (carry,
    cross-sectional rank, short volatility, pairs, seconds-level lead-lag and regime), E6's BTC short variance, and
    E7's slow trend rule on two vehicles. Each card shows its verdict glyph and the deciding number against its bar,
    from `verdict_ledger`. E5's cards say [[$0 :: C-E5-screens.cost_usd]] and at most
    [[two days :: C-E5-screens.max_days]] each.
  - Takeaway: Changing the strategy class didn't change the discipline.
- **Explore**
  1. The null that mattered (S3): the randomised-entry null of the short-volatility book, with the real book at the
     [[40.8th :: C-E5-S3-null.percentile]] percentile. Caption: what the book earned came from the unconditional
     premium, not from the forecast.
  2. The escalation's limbs (E5.P3). Limb R held: chain-mid net EV of
     [[+8.39 %/yr :: C-E5-S3-R.net_ev_pct_per_year]] against a cost of
     [[+3.15 %/yr :: C-E5-S3-R.cost_pct_per_year]], though ETH lost money at tradeable prices. The drift limb
     decided: a pooled reading of [[0.204 :: C-E5-S3-D.psi_pooled]] would have passed, while BTC
     [[2.455 :: C-E5-S3-D.psi_btc]] and ETH [[0.722 :: C-E5-S3-D.psi_eth]] failed against a bar of
     [[0.25 :: C-E5-S3-D.bar]]. The per-currency reading was pinned in code before any number existed
     (SD-E5-30(c)), which is replay R4.
  3. Unreachable limbs (S1, S2): why a null limb can be unreachable, which makes the verdict NO-READING. The
     counterfactual re-reads are shown as recorded, not decided.
  4. E6, a NO-READING held as NO-READING: the coverage limb against its pre-registered bars, both short. Beside it,
     limbs (a) and (b), which would KILL, labelled as reported and not decided (C-E6-P2). The gate closed E6
     without relabelling it. Next to it, the report-only DVOL-implied book: the premium shows at index level, not at
     the prices a seller gets.
  5. E7, a KILL on both vehicles, accepted at the gate: the limb table per vehicle as `reading()` read it, with each
     limb's reachability stated first. K3 was near one-way, so the two-sided evidence is K4 and K5, and on the perp
     K4 did not hold (C-E7-P2's qualifier). Then the funding-by-momentum table the plan promised either way.
- **Method**
  - The screen template: the class, the hypothesis, an economic limb, a null limb, a kill bar in code, and the seal.
  - Why each null was built the way it was: randomised entry, prevalence-matched, and so on.
  - The close-outs' scope-honesty clauses (E5, E6 and E7, each §1), as reviewed excerpts.
  - What was not screened (E5's C6, C8, C9 and C10), and what E6 and E7 left open (their close-outs §4.2).
- **Lens**
  - IC: Each screen pairs its economic limb with a null built to match it, so a pass has to beat random entry, not
    just zero.
  - Lead: When the obvious ideas were exhausted, I changed the strategy class instead of tuning harder, and held
    each new class to a cheap, pre-registered screen.
  - Manager: Each screen had a fixed budget and a bar in code before it ran, so a direction could be closed in
    days instead of drifting on for months.
- **Claims:** C-E5-screens, C-E5-S3-null, C-E5-S3-R, C-E5-S3-D, C-E6-P2, C-E7-P2
- **Data:** `e5_screens`, `s3_drift`, `null_dist`, `screen_limbs`, `e7_funding`, `verdict_ledger`
- **Next:** the II → III hand-off.

---

## 6. Act III — The verdicts

### III.11 Timeline & gates · v0.1

- **60 s**
  - Headline: Each research epic asked one question, set its bar, and got a signed answer.
  - Figure: a swim-lane `Timeline` from 2026-05 to 2026-10. There is one lane per epic, E0–E7, with marks for the gates (◆), my sign-offs (✎) and the PAUSEs (⏸), and bands for the phases in
    flight. [[7 :: C-gates-count.gates]] gates in all, signed off [[12 :: C-gates-count.sign_offs]] times.
  - Takeaway: The program had a shape: a question, a bar, a verdict and a signature, epic after epic.
- **Explore**
  - Click an epic for its card: the question, its bar, the verdict glyph, the killing fact, and links
    to its dossier's SD pages and its ledger rows. The verdicts are the epic verdict claims below.
  - An overlay of the agent's items, as dots on each lane coloured by reading ([[73 :: C-loop-items.items]] items). First
    mention on `/verdicts`: the agent is Claude Code (mostly Opus), in sessions I started for most of the work up to
    E5's first gate, and mostly under my autorun supervisor after it.
  - Notice: how much of the agent's work ran between the gates, against the cadence of my decisions.
- **Method**
  - How a gate worked: the agent built the dossier and a recommendation, the work paused at boundary (d), and I
    signed a lettered option, recorded verbatim.
  - Where the record says a bar came late or went partly unrun, the card says so: E4's program verdict (E4.P6.7) was
    decided with some of its criteria never run, and its worst-coin gate was made operational only at the verdict
    (SD-E4-25).
  - E5's pre-commitment that closed the family: on a fourth NO-GO, the program family closes permanently (E5 plan
    §7).
  - After the family closed, E6 and E7 opened as a new program on E5's reopening standard (E5 close-out §5), each
    with its own kill screen and gate. E6 shows a NO-READING held at its gate, and E7 a KILL accepted with its
    weakest limb disclosed.
  - E0 and E1 were infrastructure epics: their ✓ marks a shipped result, not a research verdict.
  - A gate signed off more than once has a mark for each sign-off: E4-G2 was signed off six times, three of them
    keeping it undecided, and only the last closed it (C-gates-count's qualifier). Each mark quotes the record's own
    reading. E5 closed outside a numbered gate, when I accepted E5.P3's KILL; its mark is the verdict ledger's row.
  - The overlay starts at E4, where the ledger starts. E4's items except E4.P6.1, and E5's up to Gate E5-G1, ran
    outside the supervisor (C-loop-items' qualifier).
- **Lens**
  - IC: Each card shows the bar its epic set, and the dossier and SD links let you check what each bar said and
    when.
  - Lead: I kept each epic to one question and one bar. That scoping made each verdict quick to reach and hard to
    argue with.
  - Manager: The agent's items are the dots and the gates are mine. The overlay shows how much work ran between
    the decisions only I could make.
- **Claims:** C-gates-count, C-loop-items, C-epic-E0-verdict, C-epic-E1-verdict, C-epic-E2-verdict,
  C-epic-E3-verdict, C-epic-E4-verdict, C-epic-E5-verdict, C-epic-E6-verdict, C-epic-E7-verdict
- **Data:** `text/epics.json`, `autorun_items`, `autorun_pauses`, `gate_events`
- **Next:** III.12. "Each gate rested on numbers. The ledger shows every one."

### III.12 Verdict ledger · v0.1

- **60 s**
  - Headline: Each verdict is listed with the numbers that decided it and the bar it faced.
  - Figure: a summary strip of counts by verdict word (ADVANCE, KILL, NO-READING and NO-GO), each with its glyph and
    label, counted on its own and never summed into a count of noes ([[4 :: C-verdict-counts.ADVANCE]] ADVANCE,
    [[11 :: C-verdict-counts.KILL]] KILL, [[5 :: C-verdict-counts.NO-READING]] NO-READING,
    [[3 :: C-verdict-counts.NO-GO]] NO-GO).
  - Takeaway: Each verdict is a number against a bar, and the record says where a bar itself fell short (SD-E4-25).
- **Explore**: the `LedgerTable`
  - Filters, in one row: epic, verdict, class.
  - Columns: id, class, verdict (glyph and label), the deciding numbers against the bar, the SD references (links to
    the public SD pages), and a commit chip.
  - A row expands to the full deciding-numbers cell and its qualifier.
  - The default sort is chronological. A NO-READING row carries a one-line reason, such as "null limb unreachable".
  - Notice: the NO-READING rows are styled apart from KILL, and each says why its bar couldn't read.
- **Method**
  - What each verdict word means, and why NO-READING isn't KILL.
  - Recorded, never decided: E5's S1 and S2 counterfactual re-reads, E6's limbs (a) and (b) ("would KILL", reported
    under a NO-READING), and the report-only books (E6's DVOL-implied book, E7's V3). They are shown exactly as the
    close-outs qualify them, and the strip doesn't count them (C-verdict-counts' qualifier). So are E3's carried
    cells, B2 and the flagship, which E3 carried forward without a verdict of their own; the flagship's lift
    goes with its look-ahead downgrade.
  - Each row's deciding number is a claim of its own, which the exporter generates (`C-ledger-<epic>-<id>`,
    `recorded`, checked against its dossier table; P3 §7).
- **Lens**
  - IC: Each row's number is checked against the dossier table it came from, and the row links the SD entries that
    carry it.
  - Lead: I kept NO-READING apart from KILL even where merging them would have been tidier. A screen that couldn't
    read proved nothing either way.
  - Manager: Each verdict traces to its number, its bar, its SD entries and its commit, so a reviewer doesn't have
    to take my word for it.
- **Claims:** C-verdict-counts
- **Data:** `verdict_ledger`, `text/sd_entries.json`
- **Next:** III.13 from v0.7: "Behind the ledger are the decisions that shaped it." In v0.1, the III → IV hand-off.

### III.13 Scope-decision explorer · v0.7

- **60 s**
  - Headline: [[148 :: C-SD-count.total]] scope decisions, each logged with its reason and its revisit trigger.
  - Figure: a density strip of the SD entries over time, per epic, with glyphs by type
    ([[N :: C-SD-by-type]] by type).
  - Takeaway: The program wrote down what it traded away, as it went.
- **Explore**
  - Full-text search.
  - Facets: epic; type (compromise, defect found, conclusion, pre-registration); status (open, revisited, obsolete);
    and whether the entry touches a verdict.
  - A result opens its public SD page, which lists what it cites and what cites it. It is deliberately not a graph
    drawing: lists are readable, and a hairball isn't.
- **Method**
  - The convention (binka's working rules): when a narrower path is taken, record what was traded away and what
    would restore it. On a team, that keeps deferred scope reviewable instead of forgotten.
  - Many entries are the agent's calls, and they say so. The ones I decided say that too.
  - A withheld entry appears as its id only (policy §4.2), so the explorer shows a gap where one is withheld.
- **Lens**
  - IC: Search any decision and follow its links: each entry lists the entries it rests on and the ones that later
    revisited it.
  - Lead: Whenever a task needed more than planned and a narrower path was taken, the trade was written down with
    the condition that would reopen it.
  - Manager: Deferred scope stays visible: a reviewer can see what was traded away, why, and what would bring it
    back, instead of finding out later.
- **Claims:** C-SD-count, C-SD-by-type
- **Data:** `text/sd_entries.json` (with type, status and cites), `sd_search_index.json`
- **Next:** III.14. "Every one of those decisions was made against a known way to fail."

### III.14 What was learned, and what was not · v0.7

- **60 s**
  - Headline: [[N :: C-taxonomy-count]] ways every positive result died, and the defence that caught each.
  - Figure: a `Matrix` of the causes against the epics where each struck, with a count per cell. The causes start
    from the retrospective's: look-ahead leakage, drift masquerading as signal, selection on the evaluation, and
    silent environment and plumbing faults.
  - Takeaway: The failures repeated, so the defences became standing rules.
- **Explore**
  - Click a cause to see its incidents (SD entries) and the defence that worked: the GPU silently falling back to
    the CPU (SD-E4-29), the routed loader ranking a sweep on too few cells (SD-E4-30), the drift in E3's positioning
    features, and so on.
  - The dead list against the open set: what is settled, with the external evidence needed to reopen it, and what
    was never tried (C6 sequence models, C8 on-chain, C9 market-making, C10 cross-venue), plus what E6 and E7 left
    open, each with its reopening condition.
- **Method**
  - The meta-lesson, quoted from the retrospective and marked as a conclusion, not a measurement:
    [[The program's methodology out-performed its alpha :: C-meta-lesson]]
  - E9.P4.E7 maps E5–E7's incidents onto the causes, or adds a cause where none fits. E6's DVOL-implied book is one
    candidate: a premium visible at index level but not at the prices a seller gets.
- **Lens**
  - IC: Each incident links the SD entry that recorded it and the defence that caught it, so the taxonomy can be
    checked entry by entry.
  - Lead: I turned each failure into a checklist item for the next design. The causes recurred, so the defences
    became standing rules rather than one-off fixes.
  - Manager: The open set is as explicit as the dead list: what would reopen a closed direction is written down, so
    the decision to stop is reviewable later.
- **Claims:** C-taxonomy-count, C-meta-lesson
- **Data:** `taxonomy_incidents`
- **Next:** the III → IV hand-off.

---

## 7. Act IV — The operating model

### IV.15 Loop architecture · v0.1

- **60 s**
  - Headline: One agent session per item, a supervisor that re-checks it, and me at every gate.
  - Figure: a `StepDiagram` of two nested loops, as of the export.
    - Outer, the supervisor: a Python program in the plugin. It launches a fresh headless `claude -p` session for
      each item, and it verifies every CONTINUE itself: a commit exists, the prompt advanced and a ledger line was
      added; the check command passes (in binka, the epics' test suites, where E5–E7's carry the seals and the
      hashed bars, plus the exporter's); and no frozen or protected path was touched, no test deleted or skipped,
      and no secret committed. A read-only verifier reviews an item that touched the review zones. Then it applies
      bounded recovery, or it stops and pages me.
    - Inner, the item procedure, step by step as of the export (P3 §8's list): read the policy · confirm the item ·
      check it against prior findings · write the plan · implement without running jobs · the quality gate
      (simplify, then code review, for a bounded number of rounds) · commit · run the job in the foreground ·
      analyse, and record any verdict as an SD entry · document the trade-offs · checkpoint · advance the prompt ·
      write the control signal (CONTINUE, PAUSE or DONE) and stop. Since backlog mode (2026-10-15) the next item
      comes from the backlog, and a boundary opens a card for me instead of a PAUSE.
  - Takeaway: The agent does the work, the supervisor checks it in code, and I decide at the gates.
- **Explore**
  - Step through the diagram. Each step shows what it's for, the failure it prevents, and a real artifact from
    binka: a commit, a ledger line, a control-signal example. The purpose of each step is paraphrased from the
    plugin's design document, through the excerpt review (N10).
  - The item strip (`autorun_items`): one mark per item, coloured by reading and sized by API-equivalent compute
    where it is known ([[73 :: C-loop-items.items]] items). An unknown cost is a hollow mark, never an estimate.
  - How it changed: the loop as first run in E3 (2026-07-24, the supervisor's first day), then the `config.env`
    version blocks. v0.2 added per-kind routing, the check command in the gate and bounded recovery; v0.3 the
    repository checks, the read-only verifier, the permission mode and the supervisor pushing; v0.4 the limit wait
    and repair sessions; then backlog mode (2026-10-15). Each names its design-document section as text, with no
    link (SD-SC-05).
  - Notice: which steps the supervisor re-checks in code after the session ends, and which rest on the agent
    following the procedure.
- **Method**
  - A fresh session per item keeps the context small, and the state lives in files with one job each.
  - The ledger exists because the prompt file had grown to [[151 KB :: C-ledger-context.prompt_kb]],
    [[94 % :: C-ledger-context.superseded_share]] of it finished entries that every session re-read.
  - The supervisor trusts nothing the session says: it re-checks in code.
  - Per-kind model and effort routing, with notional budgets of [[$40 :: C-loop-budget.per_item_usd]] an item and
    [[$300 :: C-loop-budget.per_run_usd]] a run: a runaway guard, not spend.
  - Bounded recovery: a fixed number of nudges, retries, resumes and repair sessions, then a halt that pages me
    (C-loop-recovery, as of the export).
  - The cost story: the real cost was [[one :: C-loop-sub.subscriptions]] flat Claude subscription. Its usage
    limits pace the loop: it waits out the short limit, up to [[12 h :: C-loop-limit.max_limit_wait]] an item, and
    halts on the weekly one. The item strip's sizes are Claude Code's API-equivalent figures
    ([[$541 :: C-loop-cost.logged_total_usd]] logged in all), labelled that way on the axis and in the legend. They
    are not money spent, and most of E4's and E5's items have no logged cost (C-loop-cost's qualifier).
  - The loop is packaged as a reusable plugin, with mechanism and per-repo policy split apart (IV.21). The plugin is
    private, so there is no link and no code (SD-SC-05; N10).
  - The check command is described as "the epics' test suites and the exporter's" (SD-SC-09).
- **Lens**
  - IC: The supervisor doesn't take the session's word: it re-checks the commit, the tests and the protected paths
    in code before it accepts an item.
  - Lead: State lives in files with one job each, and recovery is bounded: a stuck item gets a fixed number of
    retries, then the loop stops and pages me.
  - Manager: Budgets, gates and an audit trail, like a team with a written delegation charter, paced by a flat
    subscription's usage limits rather than a bill.
- **Claims:** C-loop-items, C-loop-sub, C-loop-cost, C-loop-budget, C-ledger-context, C-loop-recovery, C-loop-limit
- **Data:** `autorun_items`, `claims.json`
- **Next:** IV.16. "Between the gates the loop runs on its own. Here is what it may never do alone."
- **Open:** who decides the gates. Gate E9-G1, this site's own gate, was answered by the supervisor's decider in
  autonomous mode (2026-10-16; SD-SC-21). So this module's "me at every gate" and "I decide at the gates", the
  front door's "each one decided by me", IV.16's (d), IV.20's headline and the lessons' "gates that stay human"
  hold for the research program's gates, E0–E7, and the gate count's list stays theirs. Whether and how the copy
  shows the decider, I settle at E9.P3.2's edit pass.

### IV.16 Approval boundaries & guard hooks · v0.1

- **60 s**
  - Headline: What the agent may never do alone. Some of it is enforced in code.
  - Figure: one card for each of POLICY's boundaries as of the export, (a)–(g). Each card has a one-line rule and a
    count of the real PAUSEs and cards at its letter, by where each was recorded and never summed: at (d),
    [[9 :: C-pauses-by-boundary.notify_d]] in the supervisor's log, [[6 :: C-pauses-by-boundary.ledger_d]] in the
    ledger and [[one :: C-pauses-by-boundary.card_d]] card; at the other letters shown,
    [[zero :: C-pauses-by-boundary.other_letters]] (the tooling epic's PAUSEs aren't shown, N8):
    - (a) deleting data;
    - (b) multi-day jobs;
    - (c) any spend;
    - (d) program gates;
    - (e) any live-box or exchange change, paraphrased without POLICY's note on the live box (policy §4.5);
    - (f) the operator's personal data: a session never reads it, and nothing derived from it is committed. This is
      the policy's paraphrase, and the card says so. It gives no count, because its pauses belong to a tooling
      epic, not shown (N8);
    - (g) publication and accounts: the agent built this site, but only I can publish it.
  - Takeaway: Autonomy stops at the irreversible, the outward-facing and anything touching money.
- **Explore**
  1. The PAUSE log: click a card to see its events, each with the agent's recommendation next to my recorded
     decision. A PAUSE's reason is a log line, so it crosses only through the excerpt review (policy §4.4); the
     cards show the letter, the date, the item and the decision. Examples:
     - (d) the E3-G1 gate dossier (2026-07-24);
     - (d) the holdout unseal, which the freeze record called a one-way door (2026-08-03);
     - (e) the live shadow run, not authorised (E4.P6.6, 2026-08-03).
  2. The guard-hook tester: pick a command from `guard_cases` and see the real decision, the rule that fired and its
     message, produced by running the hook over binka's rules (P1). The cases include an `rm -rf` of the pinned
     frozen tree, `pipenv` from the repo root, staging a protected notebook, and a harmless `git status`. A note
     explains the split: the policy is prose the agent reads, and the hook is the part it can't talk its way past.
     Free typing waits for a public plugin (SD-SC-05).
  - Notice: which rules the hook enforces in code, and which hold only because the agent stops and asks.
- **Method**
  - Prose-enforced: the POLICY, which the agent reads at step 0, and the supervisor paging me on a PAUSE.
    Code-enforced: the guard hook, the check command, the E5 seal raising `SealViolation` (C-seal-rule), the
    supervisor's repository checks and the read-only verifier.
  - "A PAUSE names the boundary letter", and since backlog mode a card does too. That makes the audit trail
    queryable.
  - The decisions at (e) are mine alone, never taken autonomously. The live box's current state is not on the site
    (E9-G0 Q6; SD-SC-07).
  - The guard's self-test has [[25 :: C-guard-tests.binka_cases]] cases of binka's own, each a command with the
    decision it must get. The framework's cases are counted, not shown (N10).
  - The seal: E5 sealed two windows in code, a sealed read raises `SealViolation`, and only the gate driver may
    unseal, once (C-seal-rule). IV.17 has the full record.
  - The guard cases name real repo-relative paths, so they go through the excerpt review (P1 §7.3).
- **Lens**
  - IC: Pick a command in the tester and see the hook's real decision. The cases are the hook's own output, not a
    re-implementation of it.
  - Lead: I put the rules that matter most into code. The prose policy is read at every step, but a hook is the part
    an agent can't argue past.
  - Manager: Irreversible or outward-facing actions need my sign-off: gates, spend, live changes, publication. Each
    pause names its boundary, so the audit trail can be queried.
- **Claims:** C-guard-tests, C-pauses-by-boundary, C-seal-rule
- **Data:** `text/boundaries.json`, `autorun_pauses`, `guard_cases`
- **Next:** IV.17 from v0.5: "Some rules are older than any run. Here is how a bar was fixed before its data." In
  v0.1, the act ends here.
- **Open:** the (e) example is recorded as a ledger sign-off row and a commit subject, not as a ⏸ row or a log PAUSE
  line, so `autorun_pauses` as specified gives (e) no event. E9.P1.5 decides (P1 §5.1's note; SD-SC-16).

### IV.17 Pre-registration as code · v0.5

- **60 s**
  - Headline: Every reading was committed before its first result. The commits prove the order.
  - Figure: a `CommitOrder` strip, one row per pre-registered item, from the declaring commit to the first-result
    commit: E4.P6.8 `c973274` → `88ec6dc`; E4.P7 `64aa7b6` → `e176bcb`; E5.P3 `02b5c53` → `afa1f4f`; and E6.P2 and
    E7.P2, whose bars were closed in code before their first cells (E7's at `71bf890`). The pairs are curated in
    `content/prereg_pairs.yaml`.
  - Takeaway: "Pre-registered" is something you can check here, not something you have to believe.
- **Explore**
  1. The seal: a timeline of the seals through E7. E5's two windows show no reads (E6 sealed them again). E7's
     holdout is unspent by E7 but not unseen: outside E5's windows its months were dev data for E5 and E6. Every
     disclosed contact is shown in its close-out's own words, as a reviewed excerpt: E5's count-only touch by an
     aborted attempt (SD-E5-26), the one DVOL bar an E6 skeptic printed at the seal's edge (SD-E6-24), and E7's
     contacts with holdout-dated information (its close-out §1 point 5). A code excerpt of `ml/e5_seal.py` shows
     `strip_sealed`, `assert_unsealed` and the single gate exception that raises `SealViolation`.
  2. Hashed bars: a bar is a number in code whose digest was pinned at pre-registration. A code excerpt of one bar
     and its test shows how changing the bar afterwards fails the suite the supervisor runs.
  3. Freeze records: a named configuration is content-hashed, so the confirmation runs provably used the same
     configuration. It links to II.9, where the freeze is why the leak was recorded rather than quietly fixed.
- **Method**
  - Why commits prove the order: binka is private, but the SHAs and timestamps are public, and the declaring commit
    subjects are quoted.
  - The limit: a commit proves the order in this repository's history, not that nothing was looked at before. The
    seal and the loader guards are that defence, and the page says so plainly (C-prereg-pairs' qualifier).
- **Lens**
  - IC: Check the order yourself: each row pairs the commit that declared a reading with the commit that first
    reported it, and the timestamps are public.
  - Lead: Each bar was written in code before its first cell and closed to amendment. Only a gate could restate it,
    and a quiet change would fail the suite.
  - Manager: Pre-registration made each verdict auditable after the fact: what would count as a pass was fixed and
    timestamped before anyone saw a number.
- **Claims:** C-seal-rule, C-prereg-pairs
- **Data:** `prereg_pairs`, and the excerpts `seal_core` and `bar_example`
- **Next:** IV.18. "Rules on paper are easy. Here are moments they were tested."
- **Open:** the headline holds only if every pair is ordered ([[N :: C-prereg-pairs]] pairs until E9.P4.E5).

### IV.18 Case replays · v0.5

- **60 s**
  - Headline: Moments where the rules, not the agent's judgement, decided what happened next.
  - Figure: one replay card per chosen replay, each with a one-line hook: R1, R2 and R4, with R5 in place of R3
    (inventory §4; SD-SC-14):
    - R1, the look-ahead: "The agent found a one-minute leak in the flagship, and was not allowed to fix it
      quietly." (C-E4-024-found)
    - R2, the gate pause: "Dossier built, recommendation written, loop stopped: a program gate is mine."
    - R4, the easy pass: "A pooled reading would have passed. The per-currency reading had been fixed in code
      first." (C-E5-S3-D)
    - R5, a NO-READING held: "The free trade tape couldn't mark and fill the construction to its bars, so the
      screen read NO-READING, and the gate kept it that way."
    - In reserve: R3, the lost GPU; R6, a KILL accepted with its weak limb disclosed.
  - Takeaway: The agent did the work, and the rules decided what it could do next.
- **Explore**: the `ReplayPlayer`, a handful of steps per replay: the situation → what the agent did → the rule that
  constrained it → my decision → the outcome.
- **Method**
  - Where each step's evidence comes from: a commit, an SD entry, a supervisor log line or a transcript excerpt.
    What was cut, and why.
  - I read every excerpt and log line before it enters the bundle (policy §4.6).
  - An agent step describes what the agent did, never what it "thought", unless an excerpt shows it.
  - R1 ran in an interactive session and has no transcript; its spine is the record (inventory §4).
- **Lens**
  - IC: Each step cites its evidence (a commit, an SD entry, a log line or an excerpt I reviewed), so a replay is a
    reconstruction you can check.
  - Lead: These are the moments the rules were tested: the agent did the work, and rules written in advance decided
    what it could do next.
  - Manager: Each replay ends with a human decision at a boundary. That is the delegation model: the agent proposes,
    and I decide at the edges.
- **Claims:** C-E5-S3-D, C-E4-024-found
- **Data:** `replays/*`
- **Next:** IV.19. "Replays are moments. Here is the whole run, counted."
- **Open:** the replay claims (`C-R*`). They waited for the replay pick (SD-SC-15 point 7), which Gate E9-G1
  approved (2026-10-16; SD-SC-14, SD-SC-21). E9.P4.E5 adds them with the replay tables (E9 §5).

### IV.19 Throughput & compute · v0.5

- **60 s**
  - Headline: The limit on autonomy was my sign-off, not the budget.
  - Figure: three `StatTile`s: the items worked ([[73 :: C-loop-items.items]]), the PAUSEs at a boundary
    ([[9 :: C-pauses-by-boundary.notify_d]] in the supervisor's log), and the median latency from a PAUSE to my sign-off
    ([[N :: C-pause-latency]]). Under the items, one line, the one place the site counts it (N8):
    [[N :: C-loop-items-hidden]] items of one tooling epic, not shown: personal data.
  - Takeaway: The loop worked steadily, and the waiting was on me.
- **Explore**
  1. Items per week, stacked by reading (✓, ✗, ⛔, ⏸), from `autorun_items`.
  2. The latency from a PAUSE to my sign-off, per gate, as a `DotStrip`. It shows where I, not the agent, was the
     bottleneck. E5-G1 is the long one: its screens finished 2026-08-19, and the gate was decided 2026-09-27. Its
     PAUSE fell in the stretch the supervisor log misses, so the latency is partial (C-pause-latency's qualifier).
  3. API-equivalent compute per item, as a `Histogram` labelled "API-equivalent, as reported by Claude Code; the
     real cost was a flat subscription" (C-loop-sub). Unknown values are counted, not imputed
     ([[$541 :: C-loop-cost.logged_total_usd]] logged in all).
  4. Recovery events (nudges, infra retries, repairs, limit waits and halts), counted where the supervisor log was
     kept, and shown as partial ([[N :: C-recovery-counts]]).
- **Method**
  - The loop as of the export, its values claims checked against `config.env`: the notional budgets
    ([[$40 :: C-loop-budget.per_item_usd]] an item) are a runaway guard, not spend, and the usage limits pace the
    loop (C-loop-limit).
  - Per-kind routing: Opus throughout, at the highest effort for design and dossier items.
  - What a metered team would do differently.
- **Lens**
  - IC: Every count here comes from the ledger and the supervisor log, and the gaps in the log are shown as gaps
    rather than filled in.
  - Lead: I count my own sign-off delay next to the agent's throughput, so the bottleneck is measured rather than
    assumed.
  - Manager: A flat subscription makes throughput, not spend, the thing to manage. The budgets in the config are a
    runaway guard, not a bill.
- **Claims:** C-loop-items, C-loop-sub, C-loop-cost, C-loop-budget, C-loop-limit, C-pauses-by-boundary,
  C-pause-latency, C-recovery-counts, C-loop-items-hidden
- **Data:** `autorun_items`, `autorun_pauses`, `gate_events`, `autorun_recovery`, `autorun_withheld`
- **Next:** IV.20. "Who did what, then: the charter."
- **Open:** the headline and the takeaway hold only if the latency data shows the waiting was on me
  ([[N :: C-pause-latency]] until E9.P4.E5).

### IV.20 Human/AI division of labour · v0.5

- **60 s**
  - Headline: I framed the questions and signed the gates. The agents did the work in between.
  - Figure: a `Matrix` of activities against actors.
    - Activities: frame the question, external literature search, plan drafting, pre-registration, implementation,
      code review, running jobs, the skeptic check, verdict analysis, the gate decision, spend, live changes.
    - Actors: me, the Claude Code agent (autorun), claude.ai deep research, the skeptic subagent, and, as of the
      export, the supervisor's read-only verifier.
    - Cells: ● owns, ◐ contributes, — never.
  - Takeaway: The delegation was written down, and the record shows it was kept.
- **Explore**
  - Click a row for its evidence: the policy line that assigns it, plus one real instance (a commit or an SD entry).
  - The research loop as a `StepDiagram`: a retrospective (the agent, directed by me) → a deep-research prompt (the
    agent drafts, I edit) → deep research (claude.ai) → a plan drafted from the results (the agent) → ratification
    (me, a verbatim sign-off). Each step shows its real artifact ([[N :: C-dr-cycles]] cycles).
- **Method**
  - Why the gates stay human: irreversibility (the holdout unseal as a one-way door), money, and program direction.
  - What I'd delegate next, and what I wouldn't.
  - The skeptic brief: every card and dossier gets an adversarial read before it is final.
  - Who wrote the words: the first-person copy on this site, the tour and lens notes included, is the agent's draft
    in my voice. I give it one light pass; of the lens notes, I edit a sample and skim the rest.
- **Lens**
  - IC: Each cell cites a policy line and a real commit or SD entry, so the charter is checked against what actually
    happened.
  - Lead: I kept the framing and the gates, and delegated the rest inside written boundaries. The skeptic step is the
    part I'd copy first on any team.
  - Manager: Irreversible calls stay human: the unseal, spend, live changes and program direction. The rest is
    delegated with a written charter and an audit trail.
- **Claims:** C-dr-cycles
- **Data:** `content/raci.yaml` (authored: each cell cites a policy line and an evidence commit), `text/boundaries.json`
- **Next:** IV.21. "The loop that did this outgrew the project."

### IV.21 From project to plugin · v0.5

- **60 s**
  - Headline: The loop outgrew the project, so I split mechanism from policy into a plugin.
  - Figure: a split diagram, as of the export.
    - The mechanism, in the plugin: the supervisor, the tail, the guard framework, the item, commit and repair
      skills, init, retro, the acceptance gate, the verifier, and the backlog and its cards.
    - The policy, in each repo: `.autorun/POLICY.md`, `config.env`, `guard_rules.py`, `backlog.json`, the prompt
      and the ledger.
  - Takeaway: A working hack became a tested tool with a clear line between mechanism and policy.
- **Explore**
  - The design principles as flip cards, one per section of the plugin's design document
    ([[N :: C-plugin-principles]] principles): a one-line rule, the failure that caused it, and the section's name as
    text. Each card goes through the excerpt review (N10).
  - The test harness: a stub `claude` end-to-end suite ([[N :: C-plugin-tests]] tests) that runs the supervisor
    against scripted sessions: a CONTINUE with no commit, a usage-limit exit, a crash mid-item.
- **Method**
  - The extraction plan: config-driven, paths unchanged, minimal churn. What broke in the migration, and how it was
    verified.
  - The plugin is private for now: no GitHub link and no code excerpts (SD-SC-05). Its claims resolve privately
    (N10).
- **Lens**
  - IC: The supervisor is tested end to end against a stub that scripts its failure modes, so the recovery paths run
    in tests before they run for real.
  - Lead: Once the loop worked, I separated the reusable mechanism from this repo's policy, so another project can
    adopt it without inheriting binka's rules.
  - Manager: Turning a working hack into a tested tool is what lets a practice outlive one project, and the split
    between mechanism and policy is what made it possible.
- **Claims:** C-plugin-tests, C-plugin-principles
- **Data:** `plugin_principles`
- **Next:** the IV → Lessons hand-off.

---

## 8. The coda

### Lessons (`/lessons`) · v0.9

Mostly prose, in my voice. The agent drafts it from the evidence, and I edit it lightly (P4 §12 answer 4). Every
opinion is marked as one, and each point tied to evidence carries its chip. It has no lens notes.

- **The meta-lesson:** [[The program's methodology out-performed its alpha :: C-meta-lesson]], and that is the part
  that transfers. It is marked as a conclusion, not a measurement.
- **What I'd do differently**, each point tied to its evidence:
  - Build the causal forward-replay path at the start. The leak survived two epics and was caught only by a
    forward-replay build (II.9; SD-E4-24).
  - Measure costs before the first model, not in E4 (II.7).
  - Seal holdouts at plan time, from the first epic. E5 did; E4 spent its holdout coins on a confirmation the leak
    then voided (II.9; IV.17).
  - Set the family-closing pre-commitment earlier (III.11).
- **What transfers to a team of humans and agents:** pre-registration as code; freeze, record, then an authorised
  re-cut; boundaries enforced by hooks, not by prompts; a supervisor that re-checks; an append-only decision log;
  and gates that stay human.
- **What's next:** the honest open set (III.14), and where the operating model goes from here. The agent was Claude
  Code (mostly Opus), and the loop it ran in under my autorun supervisor is already a reusable plugin (IV.21).
- **Claims:** C-meta-lesson
- **Data:** none

---

## 9. For Gate E9-G1

**What I approve** (E9 §1; the E9.P0.7 dossier carries it): the spine (§2, E9-G0 Q4's wording, unchanged); the v0.1
headlines (the front door's spine and six tiles, and II.7, II.9, III.11, III.12, IV.15 and IV.16); and the hand-off,
intro and naming changes below.

**Answered 2026-10-16:** approved, decided by autorun (the G1 dossier §8; SD-SC-21). Its changes are the
agent's-model and III.11 rows below, the II.7 row's quote of the headline as it stands (C1), and IV.15's and
IV.16's Notice lines, which the template asks for (§1.4) and the draft lacked (C7).

**What changed from the seeds, and why.** This table is the canonical list (SD-SC-16). The rows marked *in place*
also fixed a design fact in P3 or P0, which P0 §15 records (§17 for Gate E9-G1's); every other seed is superseded by
this file, not edited.

| Where | Change | Why |
|---|---|---|
| II.7 headline | "Its causal edge didn't cover" the round-trip, where the seed said "it never beat" it | As built, with the leak, it did clear the cost; II.9 is why that doesn't count |
| II.9 headline | "The program's best edge … came from one minute of BTC's future", with "per-trade" added | The seed spoke in the first-person plural, against the first-person rule, and ran past fifteen words |
| II.9 beat 6 (*in place*, P3 §5.1) | The timeline is in date order: the re-tune (E4.P7) came before stage 2 | P3 had stage 2 first. The commits date the re-tune to 2026-08-10 and stage 2 to 2026-08-11 |
| II.9 Method (*in place*, P3 §5.2) | E3's downgrade is a reviewed excerpt from the E3 dossier §12.3, not a public SD page | It isn't an SD entry |
| The agent's naming (*in place*, P3 §2) | Front door, `/verdicts`, `/operating-model` and II.9 say how the sessions ran: mostly sessions I started up to E5's first gate, the supervisor after it (II.9's was interactive) | Before Gate E5-G1 the supervisor ran only from 2026-07-24 to 2026-08-03; E4's items except E4.P6.1, and E5's up to Gate E5-G1, ran outside it (inventory §1 point 2). P0 §10's naming would be false for that work |
| The agent's model (*in place*, P3 §2; Gate E9-G1) | "Claude Code (mostly Opus)" where the copy names the agent for the whole program: the front door, `/operating-model`, `/verdicts` and `/lessons`. II.9's discovery keeps "(Opus)" | The commits' co-author lines name Sonnet and Fable models on parts of E2 to E5's work, and an Opus model on the discovery's commit (the G1 dossier's D4d (A) and C5) |
| III.11 headline, Explore, IC and Lead; a Method line (*in place* for the Job and the card, P3 §6) | "set its bar", not "set its bar first"; the card shows "its bar", not "the pre-registered bar"; the Method cites SD-E4-25 | E4's program verdict was decided with some of its criteria never run, and its worst-coin gate was made operational only at the verdict (SD-E4-25; the G1 dossier's C2) |
| III → IV, `/operating-model` intro, IV.15's job (*in place* for the job, P3 §8) | "I worked that ledger with an AI agent", not "most of that ledger was produced by an autonomous agent loop" | The same record; SD-SC-15 found the same for tile 6 |
| IV.15 IC lens (*in place*, P3 §8) | No pointer to the supervisor's source file | The plugin is private (N10) |
| III.12 headline | A declarative sentence, "the numbers that decided it" | The seed had no verb, and some verdicts rest on several numbers (E7's limbs) |
| IV.15 headline | "One agent session per item, a supervisor that re-checks it, and me at every gate" | The seed ran to seventeen words |
| `/science` intro | "This act is how the answer was reached", not "these two modules are why the answer was no" | It holds for every train, and E6's NO-READING isn't a no |
| Front door | P0 §3.3's seed line ("Bars written before the data, …") is retired | P3 §3.1 made the spine the display type |
| III.13 headline | "scope decisions, each logged with its reason and its revisit trigger" | The seed said "where I knowingly took the smaller path": many entries are the agent's calls, and many record a defect or a conclusion |
| IV.19 headline | One sentence with no number | The seed had three numbers against the one-number rule |
| I.1, I.3, I.4, IV.21 headlines | Shortened or de-hyped | The seeds ran past fifteen words, or let an adjective do the work of evidence ("changes everything") |

**Open points** are in the modules' `Open:` fields: IV.16 (the (e) count, for E9.P1.5), IV.18 (the replay claims,
at E9.P4.E5), and the lines that wait for a draft's value (I.1, I.3, II.7, II.8, II.9, IV.17, IV.19). Gate E9-G1
settled the model in the agent's naming, which SD-SC-16 point 10 had left open (§1.2), and its repeat settled II.7's
fee term (2026-10-24; II.7's `Open:` field records the answer).
