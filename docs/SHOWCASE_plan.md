# Binka Lab — portfolio showcase: overall plan (2026-09-29)

**Status:** plan v2 (refined after operator decisions, 2026-09-29). Per-phase designs follow
one at a time: [P0](SHOWCASE_P0_design.md) → [P1](SHOWCASE_P1_design.md) → [P2](SHOWCASE_P2_design.md) → [P3](SHOWCASE_P3_design.md) → [P4](SHOWCASE_P4_design.md) → [P5](SHOWCASE_P5_design.md) → [P6](SHOWCASE_P6_design.md). Since 2026-10-15 the program wrapper is
epic **[E9](E9_2026-10-15.md)** (lanes, gates, loop items; ratified 2026-10-15). These docs move into the
`binka-lab` repo at E9.P2.0 (SD-SC-06), and binka keeps a pointer. **Amended for E9-G0 by E9.P0.1, 2026-10-16 (§7).**

## 1. Goal

A public, interactive deep-dive into the AI/ML work behind binka that raises the operator's
standing for **senior IC, tech lead and management roles in AI**. It has to work for three
readers at three depths (P0 §2) and survive an expert poking at it: every number traces to a
record.

**The spine (E9-G0 Q4):** *"I built an ML trading system, then ran a pre-registered research
program on it that kept saying no. Here is why you should believe the no."* No copy counts the
noes: a NO-READING isn't a "no" (P3 §2).

What it demonstrates, in priority order:
1. **Scientific rigor under temptation.** Leakage autopsy, sealed windows, kill bars in code,
   NO-READING ≠ KILL.
2. **An AI-native operating model.** An autonomous agent loop that ran the research inside
   explicit approval boundaries, with guard hooks, a cost ledger and human gates. It is
   extracted into a reusable plugin.
3. **ML and systems breadth.** A C++ collector, 200+ features, 6 model families, GPU
   training, self-hosted MLflow, cost-aware evaluation, and an inference-and-execution path
   that ran live on Binance.
4. **Leadership judgment.** Scoping, gate decisions, knowing when to stop, and writing it up.

## 2. Decisions (signed 2026-09-29)

| # | Decision | Value |
|---|---|---|
| D1 | Repo | New **public** repo `binka-lab` (created private, flipped public at v0.1 launch). binka stays private. |
| D2 | Domain | **`lab.gridchyn.ai`**. The zone is already on Cloudflare, so hosting is Cloudflare Pages. |
| D3 | Agentic-ops depth | **Deep.** It becomes a first-class act with its own modules and replayed case studies, not a single section. |
| D4 | Stack | Astro 5 + React islands, static-first. Pages read parquet with `hyparquet`; DuckDB-WASM runs only in the `/about/data` console (revised in the P2 design). Tokens are a vendored igor-web snapshot (SD-SC-03). |
| D5 | Data flow | binka `py/showcase/` exporter → versioned, sanitized bundle + `manifest.json` → binka-lab `data/`. It is one-way: binka-lab never reads binka. |
| D6 | Honesty rules | No profit claims. Illustrative data is labelled as such. Every published number has a claims-register entry (P0 §4). |

## 3. Information architecture: four acts

The site is organised as four acts plus a front door. A reader can stop after any act and
still leave with a complete story.

| Route | Act | Modules |
|---|---|---|
| `/` | **Front door** | 60-second overview: spine, timeline E0→E7, 6 key-number tiles, "choose your path" (IC / lead / manager) |
| `/system` | **I. The system** | 1 Data & collector · 2 Features · 3 Labels · 4 Models & training · 5 MLOps · 6 Live inference |
| `/science` | **II. The science** | 7 Evaluation & the cost wall · 8 Model bake-off & tabular saturation · 9 **Leakage autopsy** ⭐ · 10 Null models & the strategy-class screens, E5–E7 |
| `/verdicts` | **III. The verdicts** | 11 Program timeline & gates · 12 Verdict ledger (every epic shown) · 13 Scope-decision explorer (the E3–E7 SD logs) · 14 What was learned / not learned |
| `/operating-model` | **IV. The operating model** | 15 Loop architecture · 16 Approval boundaries & guard hooks · 17 Pre-registration as code (seal, hashed bars) · 18 Case replays · 19 Cost & throughput ledger · 20 Human/AI division of labour · 21 From project to plugin |
| `/lessons` | Coda | What I'd do differently, and what transfers to a team |
| `/about` | — | Provenance, manifest viewer, method notes, links (igor-web `/algo`, CV, GitHub) |

⭐ = flagship. The leakage autopsy (II.9) and case replays (IV.18) are the two interview
stories, and they get the most design effort.

## 4. Phases

| Phase | Output | Exit criterion | Est. sessions |
|---|---|---|---|
| **P0 Narrative, claims & disclosure** | `narrative.md`, `claims.yaml` register, `disclosure_policy.md`, `agentic_inventory.md`, `glossary.yaml`, written in binka until E9.P2.0 moves them to `binka-lab` (SD-SC-06) | Every v0.1 module has its 60 s / 5 min / deep outline, every v0.1 number has a claim entry with a source, and the disclosure policy is signed | 2–3 |
| **P1 Export pipeline (binka side)** | `py/showcase/` exporters, bundle schema, sanitizer + leak scanner, tests, `make showcase-export` | The bundle rebuilds byte-identically from its pinned inputs (`--check`), the scanner passes, and every v0.1 claim resolves | 3–4 |
| **P2 Scaffold binka-lab** | Astro app, tokens, layout, chart kit, DuckDB-WASM loader, CI (build · lint · link-check · Lighthouse budget · bundle-schema check), Pages deploy on `lab.gridchyn.ai` (behind Cloudflare Access until launch) | "Hello bundle" page renders a live manifest in prod | 2 |
| **P3 v0.1 end-to-end slice** | Front door, II.7 cost wall, II.9 leakage autopsy, III.11–12 timeline & ledger, IV.15–16 loop & boundaries | Three outside readers pass the 60-second test (P0 §8); repo flipped public; linked from igor-web `/algo` and CV | 3–4 |
| **P4 Full build-out** | The rest of acts I–IV in the order II → IV → III → I (science and operating model first, since they differentiate most) | All modules shipped; every chart carries a provenance chip | 6–8 |
| **P5 Explainability & polish** | Glossary tooltips, per-role "why it matters" lens, guided tour, mobile/a11y/dark-mode pass, performance budget | Lighthouse ≥ 95 on all four metrics; a11y audit clean | 2 |
| **P6 Distribution** | 3-min walkthrough video, 1-page PDF, README as case study, LinkedIn post, interview talk tracks (the plugin's README + demo GIF deferred: it stays private, SD-SC-05) | Assets published; CV and site updated | 1–2 |

Versioning: **v0.1** = P3, **v0.5** = P4 half-way (acts II + IV complete), **v1.0** = P5 done.

## 5. Cross-cutting rules

- **Provenance on every chart.** A chip reading `source · commit · run` opens the claim entry
  and links to the public excerpt, if there is one.
- **Three depths per module.** The headline and one chart are always visible. "Explore" opens
  the interactive. "Method" opens the deep write-up.
- **Static-first.** No backend and no live call. I.6 shows a dated snapshot of the prediction
  feed (SD-SC-07).
- **The data bundle is small:** < 15 MB total, and no raw exchange rows (P0 §5).
- **Written like an engineer, not a marketer.** State numbers plainly, qualify them
  honestly, and keep adjectives out.
- **Planning convention carries over:** each phase gets a design → implementation plan →
  summary doc in `binka-lab/docs/`.

## 6. Risks

| Risk | Mitigation |
|---|---|
| Scope creep (21 modules) | v0.1 ships 6 modules and goes public; P4 order is fixed by differentiation value |
| Secret or sensitive leak | P0 disclosure policy + P1 scanner in CI on both repos; the bundle is the only crossing point |
| "He failed to make money" reading | The spine frames the negative result as the product; the lessons page is explicit about what transfers |
| Agentic replays are gappy (older transcripts pruned) | P0 inventory decides the replay source: git + SD + ledger + supervisor logs are complete; transcripts are a bonus |
| Staleness | The family is closed, so the site is a dated snapshot by design; the manifest shows the export date |
| Maintenance burden | Static site, one exporter command, no servers |

## 7. Amendments from E9-G0 (2026-10-15)

Applied by E9.P0.1 from [E9](E9_2026-10-15.md) §2 and §8. The rows are in-place fixes. Each phase design carries
its own "Amendments from E9-G0" section.

| Change | Why |
|---|---|
| The spine drops the count: "kept saying no", and no copy counts the noes (§1) | E9-G0 Q4 |
| The record runs through E7: the timeline is E0→E7, E6 and E7 are in the ledger and the SD explorer (E3–E7), and II.10 covers the strategy-class screens of E5–E7 (§3) | E9-G0 Q3 |
| A tooling epic is not shown on the site, apart from one line in IV.19's item counts | E9-G0 Q5; SD-SC-08 |
| The live system is described in the past tense; I.6 shows a dated feed snapshot, and the site makes no live call (§1, §5) | E9-G0 Q6; SD-SC-07 |
| The operating-model act describes the loop as of the export, with a short "how it changed" strip | E9 §2 row 6 |
| The docs are written in binka and move to `binka-lab` at E9.P2.0 (header, §4) | E9 §2 row 10; SD-SC-06 |
| The plugin gets no public README or GIF for now (§4) | E9 §2 row 8; SD-SC-05 |
