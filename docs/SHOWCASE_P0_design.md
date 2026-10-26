# P0 design — Narrative, claims register & disclosure policy (2026-09-29)

**Parent:** [SHOWCASE_plan.md](SHOWCASE_plan.md) §4. **Next:** P1 design (export pipeline), which
consumes this phase's `claims.yaml` and `disclosure_policy.md` as its contract.

P0 writes no app code. It decides **what the site says, which number backs each statement,
and what may never leave binka.** Everything later is mechanical once these are fixed.

---

## 1. Deliverables

They are written in binka, in `py/doc/planning/showcase/`, until E9.P2.0 creates `~/dev/binka-lab/` and moves
them to the paths below (SD-SC-06).

| File | Purpose | Consumed by |
|---|---|---|
| `docs/planning/` | This doc + the plan, moved from binka at E9.P2.0 (binka keeps a one-line pointer) | all phases |
| `content/narrative.md` | Spine, act hand-offs, and per-module outlines at the three depths (§3) | P3–P4 copy |
| `content/claims.yaml` | The claims register: every published number, with its source (§4) | P1 exporter, P2 provenance chip |
| `docs/disclosure_policy.md` | Three disclosure tiers, deny-list, redaction rules (§5) | P1 sanitizer + scanner, reviewers |
| `docs/agentic_inventory.md` | What records of the autorun loop exist, how complete they are, and which case replays they can support (§6) | P1 exporter, IV.18 |
| `content/glossary.yaml` | Term → one-line plain definition → deep link (§7) | P5 tooltips |

## 2. Audiences and what each must take away

| Persona | Time budget | Enters via | Must leave believing |
|---|---|---|---|
| **Recruiter / sourcer** | 60 s | Front door | "Senior, AI-native, rigorous, and builds real systems." They can repeat the spine. |
| **Hiring manager / eng director** | 5 min | Front door → one act | This person runs a research program like a lead: gates, kill criteria, cost control, delegation to agents inside boundaries. |
| **Staff+ IC interviewer** | 30+ min | Any deep link, the GitHub README | The methods survive scrutiny. They find the leakage autopsy and the seal code, and try to break a number. Provenance has to hold. |

"Choose your path" on the front door sets a lens (IC / Lead / Manager). The lens changes the
order of the "why it matters" callouts, not the content, and is implemented in P5.
The lens copy is written in P0, one line per module per lens.

## 3. Narrative structure

### 3.1 Spine and act hand-offs

- **Front door:** the spine sentence (plan §1, E9-G0 Q4), then the timeline strip E0 → E7. Each
  epic is one band with its own verdict glyph and label, in P2 §4.2's status roles: ✓ for the
  infra epics E0–E1, ✗ NO-GO for E2–E5, ⛔ NO-READING for E6, ✗ KILL for E7. E5's band is
  labelled "family closed". The strip shows no tally (§11).
- **I → II:** "The machine works end to end. The question was never *can it trade*, but *should it*."
- **II → III:** "The answer kept being no. Here is the ledger of how each verdict was reached."
- **III → IV:** "Most of that ledger was produced by an autonomous agent loop. Here is how it was kept honest."
- **IV → Lessons:** "What transfers to a team of humans and agents."

*Written at E9.P0.5:* these hand-offs are seeds. The final hand-offs and act intros are [`narrative.md`](../content/narrative.md)
§2 (§15).

### 3.2 Module outline template (one per module in `narrative.md`)

```
## <n> <Title>
- 60s   : headline (≤ 15 words) + the one chart/tile + its claim IDs
- 5min  : the interactive — what the reader manipulates, what they should notice
- deep  : method, caveats, links to public excerpts (code / SD entries / dossiers)
- lens  : IC: … | Lead: … | Manager: …
- claims: [C-xxx, …]
- data  : bundle tables needed (names only; P1 defines schemas)
```

*Written at E9.P0.5:* [`narrative.md`](../content/narrative.md) §1.4 uses this template with the site's names (60 s, Explore,
Method; P2 §6.2), plus a Next and an Open field.

### 3.3 v0.1 modules: seeded outlines (to be finished in P0)

| Module | 60 s headline (draft) | Interactive (5 min) |
|---|---|---|
| Front door | "Bars written before the data, verdicts signed at gates, and no self-deception." | Timeline strip; tiles hover to show their source |
| II.7 Cost wall | "The model beats a coin flip, but not the 17–20 bps round-trip cost." | Cost slider 0–30 bps × bracket; per-trade EV curve crosses zero; measured-cost band per coin |
| II.9 Leakage autopsy ⭐ | "The best edge we ever found was worth +0.15 Sharpe, and it came from one minute of BTC's future." | Toggle *as built* / *causal* per coin (9 coins); correlation with forward return +0.19 → 0.00; strict median +0.146 → −0.135; a "how it was found" timeline |
| III.11 Timeline & gates | "Each research epic: one question, a pre-registered bar, a signed verdict." | Swim-lane timeline (E0–E7); click an epic to see its question, bar, verdict and killing fact |
| III.12 Verdict ledger | "Every screen, with the number that decided it." | Filterable table (epic, class, verdict); NO-READING styled apart from KILL |
| IV.15 Loop architecture | "One agent session per work item, a supervisor, a ledger, and a human at every gate." | Animated diagram of one item's lifecycle (steps 0–12, as of the export) |
| IV.16 Boundaries & hooks | "What the agent may never do alone, and the part enforced in code." | POLICY's boundaries as of the export, (a)–(g), with (f) generic (SD-SC-09), and their real PAUSE and card events; guard-hook rule tester (pick a command and see the real allow/deny decision, precomputed by the exporter; free typing waits for a public plugin, SD-SC-05) |

*Written at E9.P0.5:* [`narrative.md`](../content/narrative.md) finishes these outlines and outlines every other module. Its §9
lists what changed from these seeds and why (SD-SC-16).

## 4. Claims register (`content/claims.yaml`)

### 4.1 Schema

```yaml
- id: C-E4-024-corr            # stable, never reused
  text: "BTC 1m cumulative return correlates with the forward 20m return as built, but not causally"
  values: {as_built: [0.18, 0.20], causal: 0.00}
  unit: pearson_r
  kind: recorded | recomputed | illustrative   # recorded = cited from a doc block; recomputed = P1 regenerates it from data
  source:
    doc: doc/completed/E4_scope_decisions.md#SD-E4-24
    commit: <sha where the number was recorded>
    run: <mlflow run id | script + args>        # optional
  tier: public | aggregate | never             # §5
  qualifier: "measured on ~394k grid minutes per coin, recent slice"   # the honest caveat, always shown in 'deep'
  modules: [II.9]
  status: draft | verified                     # verified = someone re-read the source and matched the value
```

Rules:
- **No number goes on the site without an ID.** P2 CI fails a page that renders a number not
  bound to a claim (P2 designs how).
- `recomputed` beats `recorded` for anything charted. `recorded` is fine for tiles and prose.
- A qualifier is mandatory whenever the source doc gives one: scope-honesty clauses (like
  E5 dossier §1 1–4) are carried over, not dropped.
- `illustrative` values carry a visible "illustrative" label (the igor-web `/algo` precedent).

### 4.2 Seed claims (from records already read; P0 verifies each)

| ID | Claim | Source |
|---|---|---|
| C-E2-auc | dir-AUC ≈ 0.6, thin and vol-dominated | E5 retrospective §1; E2 close-out |
| C-E4-cost | spot round-trip cost 16.6–20.4 bps per coin (futures about 5.2 bps cheaper; corrected at E9.P0.4, SD-SC-15) | retrospective §2.1; E4.P1 |
| C-E4-floor | re-tuned incumbent median test Sharpe −0.137 | retrospective §2.2 |
| C-E3-lift | B1 cross-coin lift +0.08–0.10; flagship −0.053 | retrospective §2.3 |
| C-E4-024-corr | as-built corr +0.18…+0.20 → causal ≈ 0.00 | SD-E4-24 |
| C-E4-024-collapse | strict median +0.1463 → −0.1353, retention −0.92, 0/9 coins positive | retrospective §2.3; E4.P6.8b |
| C-E4-024-value | look-ahead worth ~25–30 bps/trade EV | retrospective §2.4 |
| C-E5-screens | 6 screens: 2 KILL, 3 NO-READING, 1 ADVANCE | E5 close-out §2.1 |
| C-E5-S3-null | short-vol book at 40.8th percentile of randomised-entry null | E5 close-out §3.1 |
| C-E5-S3-R | chain-mid net EV +8.39 %/yr vs cost +3.15 %/yr | SD-E5-31 |
| C-E5-S3-D | drift PSI BTC 2.455 / ETH 0.722 vs < 0.25 (pooled 0.204 would have passed) | SD-E5-31, SD-E5-30(c) |
| C-E6-P2 | E6's BTC short-variance kill screen read NO-READING: (cov) was short on both halves. (a) and (b) would KILL, reported as such and not as a verdict | E6 close-out §1–2; `E6_P2_card_2026-10-09.md` |
| C-E7-P2 | E7's trend screen read ✗KILL on both verdict vehicles (V1 perp: K3, K5, margin; V2 EU spot: K3, K4, K5), accepted at Gate E7-G1 | E7 close-out §1–2; `E7_P2_card_2026-10-12.md` |
| C-SD-count | scope decisions logged across E3–E7, `recomputed` by the SD splitter: 148 when counted on 2026-10-16 (29 + 35 + 32 + 25 + 27 unique ids; each log's fenced template heading is not an entry, SD-SC-10). All five logs are closed, so the count is final | SD logs |
| C-loop-cost | per-item and cumulative **API-equivalent** $ (Claude Code's `total_cost_usd`). **Not money spent:** the only real cost was one flat Claude subscription (operator, 2026-09-30) | `supervisor.log` + `costs.jsonl` (§6); commit messages hold none ([inventory](agentic_inventory.md) §1) |
| C-live-status | E9-G0 Q6's past-tense wording (§10.3) | `content/live_status.yaml` |
| C-arch-families | 6 model families benchmarked on one protocol (corrected at E9.P0.4, SD-SC-15; E9.P1.1 found no MLP arm, SD-SC-19) | the bake-off eval files (`arch_name`), E2 arch shortlist |
| C-guard-tests | guard-hook self-test case count | the plugin's tests |

Target for P0 exit: **all v0.1 claims `verified`** where the record holds the value (a value P1 computes stays
`draft` until E9.P1.7, §8 criterion 2), and the rest at least `draft` with a source.

*Written at E9.P0.4:* `claims.yaml` holds every seed above, every claim the v0.1 modules name (P3
§3–§9) and at least one claim per later module. A CHECK_CMD test runs each claim's check. Nine v0.1 claims stay
`draft` until P1 computes their values, and `C-arch-families` is six, not seven (SD-SC-15, §14).

## 5. Disclosure policy (`docs/disclosure_policy.md`)

**Written: [`disclosure_policy.md`](disclosure_policy.md) (E9.P0.2, 2026-10-16), revised at E9.P0.8 for the operator's
signature at the G1 repeat.** This section is its spec. Where the two differ, the policy holds (SD-SC-13, -22; §12,
§18).

### 5.1 Tiers

| Tier | Meaning | Examples |
|---|---|---|
| **public** | May appear verbatim | Methods, verdicts, SD entries (after redaction), plan/dossier excerpts, code excerpts from `ml/` research drivers, passages of binka's guard rules, POLICY and prompts through the excerpt review (the plugin's code and skill text are private, SD-SC-05), aggregate metrics |
| **aggregate** | Only as summary statistics or charts computed by the exporter, never row-level | Per-coin/per-fold metrics, trade counts, EV distributions, feature importances, MLflow run *counts* and metric summaries |
| **never** | Must not cross into the bundle or the public repo in any form | See 5.2 |

### 5.2 Deny list ("never")

- Credentials and secrets: `py/.env`, the MLflow credentials, Binance API keys, the notification endpoints,
  cloud storage keys, and any token-shaped string.
- Account and infra identifiers: exchange account/order IDs, balances, the live box's IP and
  hostnames (the policy's N2 says which names stay), SSH config.
- **Live trading configuration:** `models/configs/*trade*.json` thresholds and position
  sizing, plus live-box deployment details.
- **Raw third-party data rows:** Binance klines/trades and funding prints, the vendor's secondwise dumps,
  Deribit chains and E6's Deribit trade tape, Tardis samples. Redistribution terms are unclear,
  so only derived aggregates cross.
- **Sealed-window content:** anything derived from the E5 INTERIOR/FUTURE windows (as the policy's N5 defines it), and the sealed
  trees `py/test_data/e5_sealed/`, `e6_sealed/` and `e7_sealed/` (E7's holdout files). *Corrected
  at E9.P0.2 (SD-SC-13):* this said there was "essentially nothing", but E4's calendar panel and forward
  replay overlap E5's windows; the policy's N5 decides what crosses. E7's holdout *window* is not denied: outside E5's
  windows its months were dev data for E5 and E6, whose results cross as usual (E7 close-out §1
  point 5).
- Personal data: emails, names other than the operator's, and absolute home paths
  (they become `~/…`).
- **A private tooling epic over personal data** (E9-G0 Q5, SD-SC-08): its docs,
  its code, fixtures and tests,
  its data,
  and its rows
  in the ledger, SD logs, supervisor logs and commit history. The exporter cuts it at its source layer (P1 §2). IV.19's line is the
  one place the site describes it (P4 §4). Another epic's reference to it reads "a tooling epic,
  not shown" (P1 §7.2). Boundary (f) appears only in a generic form, and config values that
  name it are described, never quoted (SD-SC-09). These docs go public at E9.P2.0 (SD-SC-06), so
  P0.2 writes this row into the public policy generically ("a private tooling epic over personal
  data"), and the exact rows stay in the exporter's private config.

### 5.3 Redaction rules for documents and replays

- Paths are relativised to the repo root. Commit SHAs are public (they prove provenance
  without exposing content, since binka stays private).
- Commit messages and SD entries get passed through the scanner, then a human read.
- Agent transcripts: only curated excerpts (tool call → result → decision), never raw
  dumps. Every excerpt is read by the operator before it enters the bundle. The source is the
  private archive made at E9.P0.0, which the loop reads only to
  extract excerpts for that review (POLICY (g)). The inventory's counts come from one pass over it
  that the operator runs and that keeps only derived metadata (the policy's N9). The per-item session logs in
  `.autorun/state/logs/` are transcripts too, and the exporter never opens them (P1 §2).
- The igor-web `/algo` precedent holds: no profit or performance claims about the live bot.

### 5.4 Sign-off

The operator signs `disclosure_policy.md` at P0 exit (the G1 repeat), on an act card: the
loop's decider never signs it, changes it or takes its reviews (the policy's §5). P1 implements
the scanner from §5.2 as code (patterns + an allow-list), run in binka's exporter and again in
binka-lab CI.

## 6. Agentic inventory (`docs/agentic_inventory.md`)

Module IV depends on what records exist. Current state of the sources:

| Source | What it holds | Completeness | Use |
|---|---|---|---|
| `git log` (binka) | Every item's commit, with rationale in the body (recounted by E9.P0.3: [inventory](agentic_inventory.md) G1, G2) | **Complete** | Backbone of timeline, throughput and case replays |
| `py/doc/planning/AUTORUN_LEDGER.md` | One line per finished item: date, item, reading, commit | Complete from its first row, E4's ratification on 2026-07-30. The file was created 2026-09-27 from the task prompt's superseded entries, so E0–E3 are in git and the plan docs only | Ledger view, throughput (a tooling epic's rows denied, §5.2) |
| SD logs E3–E7 (C-SD-count, §4.2) | Every scope shift, defect and conclusion | Complete | Scope-decision explorer, replays |
| `.autorun/state/logs/` (gitignored; moved from `py/.autorun_logs/`, which is gone) | `supervisor.log` (from 2026-07-24): iterations, $ per item, NOTIFY/PAUSE lines. Per-item session logs `item_<n>_…`: one result record each (`.json`, the final message and usage) up to 2026-10-11, stream transcripts (`.jsonl`) from 2026-10-12. `costs.jsonl` (from 2026-10-05): $ per item. `usage.jsonl`: subscription usage readings | **Partial**: no session between 2026-08-03 00:10 and 2026-09-27, so E4 and E5 ran outside it (inventory G3, G4) | Cost ledger where present, gaps shown as gaps. The exporter reads only `supervisor.log` and `costs.jsonl` |
| A private archive (made at E9.P0.0, oldest 2026-09-27; counted in inventory G1) | Session transcripts | **Partial**: R1–R3's sessions were pruned before the archive | Excerpt candidates only, each read by the operator first (§5.3) |
| `.autorun/POLICY.md`, `config.env`, `guard_rules.py`, `backlog.json` | Boundaries, budgets, per-kind model routing, recovery, lanes, guard rules | Complete | IV.15, IV.16, IV.19 |
| The plugin (its design document, hooks and tests) | Mechanism and rationale | Complete | IV.15, IV.21 |
| Deep-research prompts/results (E2/E3/E5, Fable DR, post-E5's three directions; a later cycle is denied) | Human → DR → plan loop | Complete | IV.20 division of labour |

**P0 tasks.** (1) Recover per-item cost from commit messages and NOTIFY lines where logs are
missing, and mark unknowns as unknown, never estimated. (2) Pick the case replays.
*Done at E9.P0.3* ([`agentic_inventory.md`](agentic_inventory.md)): commit messages hold no session cost, and NOTIFY
lines only repeat a run's cumulative cost line, so a row without a logged session stays unknown (inventory §1, §3). The replay pick is its §4.

### 6.1 Candidate case replays (pick 3–4)

| Replay | Why it's a good story | Primary sources |
|---|---|---|
| **R1 The look-ahead found mid-build** | The agent found SD-E4-24 while building the forward B1, measured the leak instead of arguing it, and **did not fix it in place** (policy: record, don't silently fix) → causal re-cut → collapse | SD-E4-24, E4.P6.8b, E4.P7 commits |
| **R2 Pause at a gate** | E3-G1: the loop built the dossier and the recommendation, then stopped at boundary (d) and notified | supervisor log 2026-07-24 (in `.autorun/state/logs/supervisor.log`), `ccdeb9f` |
| **R3 Failure handling** | E4.P7: null control failed (GPU lost) → pause → routed-loader fix → resume | `ea4f96c`, `9344574` |
| **R4 Declining the easy pass** | E5.P3: pooled drift 0.204 would pass. The per-currency reading was pinned in code first (SD-E5-30(c)), so KILL | SD-E5-30/31, `afa1f4f` |
| *R5 A NO-READING held* (candidate, E9-G0 Q3) | E6.P2: the free trade tape couldn't mark and fill the construction to its pre-registered coverage, so the screen read NO-READING, though the economics it would have read were far below the bar. The gate closed E6 without relabelling it | SD-E6-15, -22, -23; the E6 card and G1 dossier |
| *R6 A KILL accepted, its weak limb disclosed* (candidate, E9-G0 Q3) | E7.P2: KILL on both vehicles. The dossier said K3 was near one-way, so the two-sided evidence was K4 and K5 (on the perp, K4 did not hold), and the operator accepted the KILL with that acknowledged | SD-E7-18, -25, -26; the E7 card and G1 dossier |

Recommendation: **R1, R2 and R4 for v0.x**, with R3 in P4. R1 and R4 are rigor stories, and
R2 is the governance story. Each replay format: *situation → what the agent did (excerpts) →
the rule that constrained it → the human decision → the outcome*. R5 and R6 were added with the
record through E7. Their sessions, like R4's, are in the transcript archive, while R1–R3's are
not. P0.3 weighs them against R1–R4.

**To verify in P0:** whether R1's discovery came from an autorun session or an interactive
one. Either works, but the site must say which. *Verified at E9.P0.3:* interactive (inventory §1 point 6).

**E9.P0.3's pick** (inventory §4, for the operator at Gate E9-G1): R1, R2 and R4 for v0.x, and R5 for P4 in place
of R3. R3 and R6 are in reserve.

## 7. Glossary seed (`content/glossary.yaml`)

kline · secondwise · touch label / bracket · dir-AUC · Sharpe (per-trade vs annualised) · bps ·
round-trip cost · taker · maker · look-ahead / causal / as built · sealed window · pre-registration ·
kill bar · NO-READING vs KILL · null model / randomised-entry null · PSI (drift) · QLIKE ·
VRP · scope decision (SD) · gate / dossier · approval boundary · guard hook · autorun item.

From E6 and E7 (E9-G0 Q3): iron fly (defined-risk short volatility) · DVOL · option mark vs
trade tape · coverage bar · hurdle rate · reachability (a limb that can go both ways) · "would
KILL" (a limb reported under a NO-READING) · perpetual future (perp) and funding · trend rule
(long/flat) · volatility targeting · point-in-time universe · verdict vehicle · MAR (return
over maximum drawdown) · holdout · limb (one part of a test with several).

From Gate E9-G1 (§17): the verdict words the v0.1 copy shows: NO-GO · ADVANCE · MARGINAL.

Each entry: `id`, `term`, `aliases` (optional), `short` (≤ 20 words, no jargon, no number), `long` (optional),
`link` (module anchor). The seed is [`glossary.yaml`](../content/glossary.yaml).

## 8. Success criteria

**P0 exit:**
1. `narrative.md` has every module outlined, and all v0.1 modules completed at all three depths plus the lenses.
2. Every v0.1 claim in `claims.yaml` whose value exists in the record is `verified`, and every other module has ≥ 1
   `draft` claim. A v0.1 claim recomputed from a table P1 hasn't built yet stays `draft`, and E9.P1.7 verifies it
   (`C-gates-count`: E9.P3.1, which builds `gate_events`; SD-SC-15).
3. `disclosure_policy.md` is signed by the operator.
4. `agentic_inventory.md` is complete, with replays chosen and per-item cost recovered or marked unknown.
5. The glossary seed has short definitions for all terms.

**Site-level (checked at P3 and P5):**
- **60-second test:** 3 people outside the project read the front door for 60 s, then state
  the spine and one differentiator. Pass = 3/3 get the spine and ≥ 2/3 name a differentiator.
- **Poke test:** a Staff+ reviewer picks any 3 numbers and traces them to source via the
  provenance chip in under 2 minutes each.
- **Perf:** first contentful paint < 1.5 s on a mid-range phone; bundle < 15 MB, lazy-loaded per act.

## 9. Work steps

1. *(Moved to E9.P2.0, SD-SC-06.)* P0 writes its docs in binka's `py/doc/planning/showcase/`.
   P2.0 creates `~/dev/binka-lab`, moves them in and leaves a pointer in binka.
2. Write `disclosure_policy.md` first. It constrains what the other deliverables may quote.
3. Build the agentic inventory (§6): scripted counting over git, the ledger and logs; the
   replay choice is a judgment call.
4. Claims: verify the §4.2 seeds against their sources, then add claims module by module
   while outlining `narrative.md`.
5. Glossary.
6. Operator review: sign the disclosure policy, approve the replays and the v0.1 headlines.

## 10. Operator answers (2026-09-29)

1. **Voice:** first person throughout.
2. **Naming the agent:** explicit: "Claude Code (Opus) running under my autorun supervisor."
   **Superseded 2026-10-16 (Gate E9-G1, D4d (A); SD-SC-21):** "Claude Code (mostly Opus)" where the copy names
   the agent for the whole program, and "(Opus)" where a passage is about Opus-era work (§17).
3. **Live bot:** the answer gave I.6 a present-tense working wording, left out of this copy because it is
   superseded (below).

   Guardrails: no P&L, balance or trade-count figures from the live account (the deny list
   in §5.2 still covers configs and account data). This is tracked as claim `C-live-status` (kind
   `recorded`, re-checked at every export).

   **Superseded 2026-10-15 (E9-G0 Q6, SD-SC-07).** The wording for `C-live-status` and I.6 is now:
   > *"It ran live on Binance: it scored coins every second and placed real orders when a
   > prediction cleared its threshold. It never made money. Act II shows why."*

   It stays true whatever the box does next, so it needs no per-release re-check. I.6 shows a
   dated snapshot of the feed instead of a live ticker (P4 §2, §7). The guardrails above still hold.

## 11. Amendments from E9-G0 (2026-10-15)

Applied by E9.P0.1 from [E9](E9_2026-10-15.md) §2 and §8. The rows are in-place fixes, except §10.3, where the
2026-09-29 answer stays and is marked superseded.

| Change | Why |
|---|---|
| The deliverables are written in binka, in this folder, until E9.P2.0 moves them (§1, §9 step 1) | E9 §2 row 10; SD-SC-06 |
| The timeline strip runs E0 → E7, with one glyph per epic and no tally. II → III's hand-off and the seed headlines for the front door, III.11 and IV.16 count no noes, epics or boundaries (§3.1, §3.3) | E9-G0 Q3, Q4. "Five epics" and "five things" became false with E6, E7 and boundaries (f) and (g) |
| ⛔ marks NO-READING only, as in P2 §4.2. The family close is a label on E5's band | E6's NO-READING would have clashed with "⛔ CLOSED" |
| Seed claims add C-E6-P2, C-E7-P2 and C-live-status. C-SD-count is `recomputed` over E3–E7: 148, not the 153 E9 §2 gave (§4.2) | E9-G0 Q3, Q6; E9 §2 row 3; SD-SC-10 |
| The deny list adds a tooling epic (not shown), the E6/E7 sealed trees, E6's trade tape and Binance funding prints (§5.2) | E9-G0 Q5 (SD-SC-08, SD-SC-09); Q3 |
| Transcript excerpts come from the E9.P0.0 archive, and the session logs count as transcripts (§5.3) | E9 §2 row 7; POLICY (g) |
| The inventory uses `.autorun/state/logs/`, the transcript archive, the E3–E7 SD logs and `backlog.json` (§6) | E9 §2 rows 5–7 |
| Replay candidates R5 (E6) and R6 (E7) are added, for P0.3 to weigh (§6.1) | E9-G0 Q3 |
| The glossary seed gains E6 and E7's terms (§7) | E9-G0 Q3 |
| `C-live-status` takes the past-tense wording (§10.3) | E9-G0 Q6; SD-SC-07 |

## 12. Amendments from the disclosure policy (2026-10-16)

Applied by E9.P0.2, which wrote [`disclosure_policy.md`](disclosure_policy.md) from §5. The rows are in-place fixes;
the policy's own additions are SD-SC-13.

| Change | Why |
|---|---|
| §5 points at the policy, which holds where the two differ | E9.P0.2 |
| §5.1's public tier names binka's own guard rules and prompts. The plugin's code and skill text are private | SD-SC-05; SD-SC-13 (3) |
| §5.2's sealed-window sentence is corrected | SD-SC-13 (2) |

## 13. Amendments from the agentic inventory (2026-10-16)

Applied by E9.P0.3, which wrote [`agentic_inventory.md`](agentic_inventory.md) from §6. The rows are in-place fixes;
the decision record is SD-SC-14.

| Change | Why |
|---|---|
| §6's ledger row: complete from E4, not E3 | The ledger's first row is 2026-07-30; the file was created 2026-09-27 |
| §6's logs row: the session-log formats, and the gap from 2026-08-03 to 2026-09-27 | Inventory §1 points 2 and 4 |
| §6's archive row drops its count, which included sessions of a tooling epic, not shown | Policy N8 |
| §4.2 `C-loop-cost` and §6's task (1): commit messages hold no session cost | Inventory §1 point 3 |
| §6.1: R1 was interactive; the replay pick | Inventory §1 point 6, §4 |

## 14. Amendments from the claims register (2026-10-16)

Applied by E9.P0.4, which wrote `claims.yaml` from §4. The rows are in-place fixes; the decision
record is SD-SC-15.

| Change | Why |
|---|---|
| §4.2's `C-arch-families` row, P3 §3.1 tile 5, P4 II.8's headline and the plan's point 3 say six model families, not seven | The bake-off files hold six; the MLP arm counts only if E9.P1.1 finds it (P4 §12 point 1) |
| §4.2's `C-E4-cost` row: futures about 5.2 bps cheaper, not "≈ 4–5" | The frozen cost card |
| §4.2 gains a pointer to the register, and §8 criterion 2 lets a v0.1 claim whose table P1 hasn't built stay `draft` | Nine v0.1 values don't exist before P1; E9.P1.7 verifies them |
| P3 §3.1 tile 6 says "agent items", not "autonomous agent items" | Inventory §1 point 2: E4's items except E4.P6.1, and E5's up to Gate E5-G1, were interactive |
| P3 §4's Method no longer cites the live fill log's count | Disclosure policy N3: fills are a live-account figure |
| P3 §5.2's attribution says the session was interactive | The inventory settled it (§6.1) |

## 15. Amendments from the narrative (2026-10-16)

Applied by E9.P0.5, which wrote [`narrative.md`](../content/narrative.md) from §3. Every headline, caption, intro, hand-off and
lens line in §3, P3 and P4 is a seed that the narrative supersedes. Those seeds stay as they were, with a pointer
(§3.1, §3.3, and P3's and P4's heads), and the narrative's §9 lists what changed and why. The rows below are the
design facts fixed in place. The decision record is SD-SC-16.

| Change | Why |
|---|---|
| P3 §5.1's beat 6 lists the events in date order: the re-tune (E4.P7) came before stage 2 | `e176bcb` (2026-08-10) precedes `68c917e` (2026-08-11), and the order feeds `leak_autopsy_events` |
| P3 §5.2 shows E3's downgrade as a reviewed excerpt | It is the E3 dossier's §12.3, not an SD entry |
| P3 §8's IV.15 job says "an AI agent", not "an autonomous agent" | E4's items except E4.P6.1, and E5's up to Gate E5-G1, ran outside the supervisor (inventory §1 point 2) |
| P3 §8's IV.15 IC lens no longer points at the supervisor's source file | The plugin is private (policy N10) |
| P3 §2's naming rule says how the sessions ran where the supervisor didn't run them | Before Gate E5-G1 the supervisor ran only from 2026-07-24 to 2026-08-03 (inventory §1 point 2) |
| P2 §5.3's lint flags any digit outside a `<Claim>` or a name | An unbound count, such as a tile's, is a number too (narrative §1.1) |
| P1 §5.1's `autorun_pauses` row notes that IV.16's (e) example is neither a ⏸ row nor a log PAUSE line | E9.P1.5 decides whether a sign-off row that names a boundary letter counts |
| E9 §5's E9.P2.0 card moves or repoints the showcase doc tests | They read the docs at their binka paths (SD-SC-14, -15, -16) |
| §3.1, §3.2 and §3.3, and P3's and P4's heads, point to the narrative | E9.P0.5 |

## 16. Amendments from the glossary seed (2026-10-16)

Applied by E9.P0.6, which wrote [`glossary.yaml`](../content/glossary.yaml) from §7. The rows are in-place fixes; the decision
record is SD-SC-17.

| Change | Why |
|---|---|
| §7's entries carry P5 §2.1's `id` and `aliases`; `acts` stays P5's | A `<Term id>` mark needs the id, and the no-jargon check needs the aliases |
| §7's `short` holds no number, and so does P5 §2.1's rule and its example | No definition is bound to a claim (narrative §1.1) |
| §7's seed adds "as built" and "limb" | The seed's own definitions need them ("causal" against "as built"; "a limb that can go both ways") |
| E9 §5's E9.P2.0 card repoints `test_glossary_yaml.py` too | It reads the glossary and the narrative at their binka paths |

## 17. Amendments from Gate E9-G1 (2026-10-16)

Applied by card:C-001 from the gate's answer ([E9](E9_2026-10-15.md) §9; the G1 dossier §8). The rows are in-place
fixes, except §10.2, where the 2026-09-29 answer stays and is marked superseded. The decision record is SD-SC-21.

| Change | Why |
|---|---|
| §10.2's naming: "Claude Code (mostly Opus)" for the whole program, "(Opus)" for Opus-era work | The commits' co-author lines name Sonnet and Fable models on parts of E2–E5's work (the dossier's D4d (A), C5) |
| P3 §2's naming rule says the same, in place | The same co-author lines; narrative §9's agent's-model row cites it |
| P3 §6's III.11 Job and card say "a bar" and "its bar", not one written before the data was read or "pre-registered", and the Job adds that the card says where a bar came late or went partly unrun; the seed headline stays (P3's head) | E4's program verdict was decided with some of its criteria never run, and its worst-coin gate was made operational only at the verdict (SD-E4-25; the dossier's D4b, C2) |
| §7's taker/maker is two entries | Two ideas get two entries (SD-SC-17 point 1; the dossier's D5a, C3) |
| §7's seed adds NO-GO, ADVANCE and MARGINAL | The v0.1 copy shows them, and E9.P3.2 marks its terms before E9.P5.1 (the dossier's D5d, C4) |

## 18. Amendments from the policy's revision (2026-10-16)

Applied by E9.P0.8, which revised [`disclosure_policy.md`](disclosure_policy.md) for the G1 dossier's §7. The rows are
in-place fixes; the decision record is SD-SC-22.

| Change | Why |
|---|---|
| §5.1's public tier takes passages of binka's guard rules, POLICY and prompts through the excerpt review, not their text as a whole | Their text touches the live system, a tooling epic (not shown) and the private plugin (the policy's N10) |
| §5.3: the loop reads the archive only to extract excerpts, as POLICY (g) words it, and the operator runs the one pass that pins the inventory's counts as derived metadata | The policy's N9; D2's option (A) |
| §5.4: the operator signs on an act card, and the decider never signs the policy, changes it or takes its reviews | The policy's §5 (the G1 dossier's B1) |
| §5.2's host clause defers to the policy's N2: the project's own public names are redacted too, apart from the two public sites, and the line no longer names the box's provider | The policy's N2 (S4) |
