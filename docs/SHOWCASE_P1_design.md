# P1 design — Export pipeline, bundle contract & leak scanner (2026-09-29)

**Parent:** [SHOWCASE_plan.md](SHOWCASE_plan.md) §4. **Consumes:** P0's `claims.yaml`,
`disclosure_policy.md` and `agentic_inventory.md`. **Feeds:** P2 (binka-lab reads only the
bundle) and P3/P4 (every chart's data).

P1 builds the **only crossing point** between private binka and public binka-lab: a
command in binka that reads research records and results and writes a small, versioned,
sanitized, self-describing **bundle**. It must be safe by construction: a secret or a raw
row that would violate the policy fails the build. It must be traceable: every value can
be followed back to an input file hash and a commit. It must be reproducible: a rebuild
from the same inputs is byte-identical.

---

## 1. Scope

**In:** the `py/showcase/` package (readers, exporters, sanitizer, scanner, claims resolver,
bundle writer, CLI); the bundle format and table schemas; the excerpt review gate; tests;
exporters for the **v0.1 tables** (§5.1).

**Out:** exporters for P4-only tables. They are listed in §5.2 so the format fits them, but
are built in P4. Also out: anything that renders, and any MLflow write.

**A constraint the overall plan got wrong, now corrected (SD-SC-01).** Result artifacts live in
`py/test_data/tmp/` (19 GB) and `py/test_data/e5_data/` (4.7 GB), and both are
**gitignored**, so "rebuild from a clean checkout" is impossible. The contract is instead:
**byte-identical given the same pinned inputs.** The manifest records the sha256 of every
input, and `--check` rebuilds and diffs (plan §4 updated; the traded-away scope is logged as
SD-SC-01).

## 2. Architecture

```
py/showcase/
  __main__.py          CLI: export | check | review | scan | claims | snapshot
  config.py            input roots, bundle version, size budgets, allow/deny roots
  sources/             read-only readers; the ONLY modules that touch the filesystem
    docs.py            markdown: SD entries (### SD-…), result tables, section anchors
    results.py         parquet/pkl/json under test_data/, with footer.json provenance
    gitlog.py          commits, dates, files changed (subprocess git, no network)
    autorun.py         ledger table, supervisor logs (cost / NOTIFY / PAUSE lines), POLICY.md
    plugin.py          the plugin: its guard hook + binka guard_rules, self-tests
    mlflow_snapshot.py P4: reads a cached snapshot JSON, never the live server during export
  exporters/           one module per bundle table; pure functions: sources → DataFrame
  schema/              one table spec per table (columns, dtypes, tier, max_rows, grain)
  sanitize.py          text redaction transforms (paths, emails, hosts, IPs)
  scan.py              standalone, stdlib-only bundle scanner (vendored into binka-lab CI)
  claims.py            resolves and verifies claims.yaml against tables and docs
  bundle.py            deterministic writer + manifest
  review.py            the review gate: records what the operator approved, in one store (run by the operator only)
  tests/
```

Invocation (pipenv from `py/`, per the repo rule):

```bash
cd py && pipenv run python -m showcase export --out ../../binka-lab/data/bundle   # all tables
cd py && pipenv run python -m showcase export --only v0.1 --out …                 # a release set
cd py && pipenv run python -m showcase check  --bundle ../../binka-lab/data/bundle # rebuild + diff
```

Until E9.P2.0 creates `binka-lab`, `--out` is a staging dir, `py/showcase/out/`, and P2.0's card
moves the bundle (E9 §5 P1.8).

**Isolation rule.** Only `sources/` may open files, and they are restricted to
`config.ALLOWED_INPUT_ROOTS`:
- `py/doc/`: the docs the readers parse, by name (the SD logs, dossiers, plans and the ledger), so a new private
  doc stays out by default (SD-SC-13)
- `py/test_data/tmp/<listed subdirs>`
- `py/test_data/e5_data/derived/`
- `.autorun/`: its top-level files (POLICY.md, config.env, guard_rules.py, backlog.json) and the
  headers of the cards in `attention/`
- `.autorun/state/logs/supervisor.log` and `costs.jsonl`, by name (`py/.autorun_logs/` is gone). The
  per-item session logs beside them are transcripts and stay out (P0 §5.3)
- the plugin's repo: its design document, its hook, skills and tests, never the
  repo's other contents
- `~/dev/binka-lab/content/` (until E9.P2.0 the content files sit in `py/doc/planning/showcase/`)

`DENIED_ROOTS` always wins:
- `py/.env`
- `models/configs/`
- `~/data/bintri/`, all of it. The inputs it holds are allowed by exact filename: P4 §10's `dataset.log` and
  E9.P1.6's B1 parquets (SD-SC-13)
- `py/test_data/e5_data/raw/`, `py/test_data/e6_data/`, `py/test_data/e7_data/raw/`
- `py/test_data/e5_sealed/`, `py/test_data/e6_sealed/`, `py/test_data/e7_sealed/`
- the rest of `.autorun/state/`: the session logs, resume notes, item plans, and the verifier's and
  skeptic's files
- the hidden epic's files (rows in the exporter's private config; SD-SC-08). P0 §5.2 lists them today and is generalised at
  E9.P2.0
- any file pulled from an exchange account, by exact name from the private config. The cost wall reads E4's frozen
  card instead (disclosure policy N2; SD-SC-22)
- anything under `~/.ssh`

A test asserts that no module outside `sources/` imports `open`/`pathlib` reads, and that
every path a source resolves falls inside the allow-list. This backs up the disclosure policy
structurally: the live trading configs can't leak because no code can read them.

**The tooling epic is cut once, at the source layer** (E9-G0 Q5, SD-SC-08). Every `sources/` text reader passes
its records through one shared filter, which drops the tooling epic's: ledger lines, SD entries, supervisor-log
and cost lines, commits and card headers. Tables inherit the cut, so no exporter repeats it.
The filter keeps one number, the count of the tooling epic's ledger items it dropped, in the one-row
`autorun_withheld` table that IV.19's line reads. Records of other epics that only mention it
(E9's own ledger rows, commits and task titles, config comments) survive, and a sanitizer
transform (§7.2) replaces the mention. `test_isolation` tests the filter once. As a backstop,
the writer (§4) rejects any string value that still holds one of the tooling epic's tokens, checked on the decoded
values before encoding. The same backstop rejects the live box's identifying tokens (its provider, region and
hostname), a second private list in the same config (disclosure policy N2; SD-SC-22).

**The seal is applied once, the same way** (disclosure policy N5; SD-SC-13). Every `sources/` reader of market data
(prices, features, labels) strips E5's sealed rows (`strip_sealed`) before it returns them, so every precompute
inherits the seal. E4's recorded result files are not market data. The feed snapshot is the one exception, and it
keeps metadata only (SD-SC-12).

## 3. Bundle format (`bundle/v1/`)

```
bundle/v1/
  manifest.json
  claims.json               resolved claims (value, qualifier, source chip, status)
  tables/<name>.parquet     zstd, row-group ≤ 64k; read by DuckDB-WASM
  text/<name>.json          structured prose: SD entries, epic cards, boundaries, excerpts
  replays/<id>.json         case replays (P4 content; v0.1 carries R1/R2/R4 skeletons if ready)
  schema/<name>.json        JSON Schema per table and text file (emitted from schema/)
```

**Why parquet + JSON:** DuckDB-WASM queries parquet directly, with range reads, in the
browser. Prose fits JSON, and Astro can import it at build time. There is no CSV: types
must survive the round trip.

### 3.1 Manifest

```json
{
  "bundle_version": "1.0.0",          // semver; a major bump = breaking schema change
  "exported_at": "2026-10-02T10:00:00Z",   // the ONLY non-deterministic field; excluded from --check
  "binka_commit": "7762e66", "binka_dirty": false,
  "autorun_plugin_commit": "a814189",
  "content_commit": "<binka-lab content/ sha>",
  "inputs":  [{"label": "e4_cost_card", "sha256": "…", "bytes": 1234,
               "footer_fingerprint": null}],
  "tables":  [{"name": "cost_wall_coin", "rows": 9, "sha256": "…", "tier": "aggregate",
               "schema": "schema/cost_wall_coin.json", "release": "v0.1"}],
  "claims":  {"total": 42, "verified": 30, "draft": 12, "failed": 0},
  "scan":    {"scanner_version": "1", "findings": 0, "secret_digests_checked": 7}
}
```

- The export **refuses a dirty binka tree** for paths it reads (`--allow-dirty` exists for dev
  runs and stamps `binka_dirty: true`; CI in binka-lab rejects a dirty bundle).
- Each input is named by a label from the exporter's private config, never by its path: a path can name a private
  repo or a denied file (disclosure policy §4; SD-SC-22). The manifest's strings take the table classes (§4): its
  labels are short text, and its ids, digests, dates and versions are structured.
- Where a result file has a `.footer.json` (the E5 convention: fingerprint + sha256), the
  manifest carries the fingerprint. The provenance chip can then show the run key (for example
  `38dcdfdc`) that the research docs already cite.

### 3.2 Determinism rules

Rows are sorted by the table's declared key. Floats are rounded to the schema's precision
(default 6 significant digits). Parquet is written with pinned writer settings (pyarrow version
recorded, no statistics timestamps, dictionary on). JSON uses sorted keys and `indent=1`,
`ensure_ascii=False` (the repo's notebook rule applies). No wall-clock value goes anywhere
except `exported_at`. `check` rebuilds into a temp dir and compares every table/text sha256.

### 3.3 Size budget

The whole bundle stays under **15 MB**, and each act's tables under 4 MB (the site lazy-loads
per act). Each table spec declares `max_rows`, and the writer fails on overflow. Budgets live
in `config.py`, and the manifest reports the actual sizes.

## 4. Table spec (the schema contract)

Every table has a spec file. P2 generates the TypeScript types from the emitted JSON Schema,
so the two repos can't drift apart silently.

```python
TableSpec(
    name="leak_autopsy_coin",
    release="v0.1",
    tier="aggregate",                 # public | aggregate (P0 §5.1); 'never' cannot be declared
    grain="coin × substrate × window",
    key=["coin", "substrate", "window"],
    columns={
        "coin": Str(enum=COINS9),
        "substrate": Str(enum=["as_built", "causal"]),
        "window": Str(enum=["strict", "holdout", "calendar"]),
        "median_test_sharpe": Float(precision=4),
        "n_trades": Int(min=0),
        "source_fingerprint": Str(nullable=True),
    },
    max_rows=200,
    min_time_grain="1d",              # every table: no timestamp finer than a day (policy §2)
)
```

The writer enforces the spec strictly:
- An undeclared column fails the build.
- A wrong dtype fails the build.
- In any table, public or aggregate, a timestamp column finer than `min_time_grain` fails the build.
- Every string column declares its class: structured, short text, authored or record prose (disclosure policy §4).
  In release mode a record-prose value without a review record fails the build (SD-SC-13).

The time-grain rule is the **raw-row guard**: minute- or second-level series can't pass as
"aggregates". Deliberate exceptions, such as a 60-minute synthetic window for a chart,
need `min_time_grain=None` plus an `exception_reason` string and an `exception_kind`, one of the
disclosure policy's three (§2): `record_event` (a commit's, a log line's or a card's own time, as in
IV.17), `feed_snapshot` (I.6's newest timestamps) or `synthetic` (a synthetic or model-output
series). No kind admits a market or third-party series. The reason is shown in the review report.

## 5. Table catalogue

### 5.1 v0.1 (built in P1)

| Table / text | Module | Grain | Source → transform | Notes / risk |
|---|---|---|---|---|
| `text/epics.json` | Front door, III.11 | epic | Hand-curated `content/epics.yaml` (question, dates, verdict, killing fact, claim IDs) validated against the retrospective §1 table, E5 dossier §1 and the E6 and E7 close-outs §1–2 | Curated on purpose: prose is authored, numbers are claims. E0–E7 |
| `verdict_ledger` | III.12 | screen / cell | Parse the markdown verdict tables: E7 and E6 close-outs §2, E5 close-out §2.1–2.2, E3 shutdown dossier, E4 G1/G2 dossiers, E2 close-out → one normalized row (epic, id, class, verdict ∈ {ADVANCE, KILL, NO-READING, NO-GO, GO}, deciding_numbers, bar, sd_refs, commit) | Tables differ per epic, so each gets its own parser plus a fixture test; unparseable rows fail loudly. The E6 and E7 tables mix screens with milestones. Their parsers take the screen rows (E6.P2; E7.P2 per vehicle) with their limbs and send gate rows to `gate_events`. They keep the report-only books (E6's DVOL-implied book, E7's V3) with no verdict and `report_only = true`, and skip milestone rows ("landed", "pinned", "green", "not reached"), listing each in the review report. E6's "would KILL" limbs are deciding numbers of a NO-READING row, never a KILL |
| `text/sd_entries.json` | III.12 links (III.13 in P4) | SD entry | Split SD logs on `### SD-E<n>-<k>` with a numeric `<k>`, skipping the fenced template heading `### SD-E<n>-NN` (SD-SC-10) → id, epic, date, title, body (redacted), cross-refs | E3–E7, counted by the splitter (C-SD-count, P0 §4.2). Bodies go through `sanitize` + the scanner, then each body's review record (disclosure policy §4.2; SD-SC-13) |
| `cost_wall_coin` | II.7 | coin | `test_data/tmp/e4_cost/`: E4's frozen card and its `*_spread.pkl` summaries → fee per side bps, spread p50/p90 bps, round-trip bps | Needs the dev quartet's spread pkls (§12); the spike (§8 step 1) confirmed them. A coin outside the frozen card would mean new computation over sealed windows (policy N5). E4's pre-seal record, so its spread window is labelled (disclosure policy N5 rule 4). The fee per side crosses under N2's carve-out, with no tier, discount or account word, and no file pulled from the account is read (SD-SC-22) |
| `cost_wall_edge` | II.7 slider | coin × config | Flagship causal/as-built trade results (e4p6_causal / e4p6_stage2 pkls) → per coin: n, μ_gross (bps), σ (bps), 50-bin histogram of per-trade gross return | Slider math in the browser: net Sharpe(c) = (μ − c)/σ. That is exact from these three moments, so no row-level trades are needed |
| `leak_autopsy_coin` | II.9 | coin × substrate × window | e4p6_stage2 (9-coin causal re-cut), e4p6_holdout_eval, e4p6_calendar → median test Sharpe, n_trades | Values must reproduce C-E4-024-collapse (+0.1463 → −0.1353, 0/9); the claims resolver checks this |
| `leak_autopsy_corr` | II.9 | coin × feature × substrate | Recompute: corr(b1_btc_cumret_{1,3,5,10,15}m, fwd 20m return) on the as-built vs causal B1 parquet (`~/data/bintri/<coin>/<coin>_b1_causal.parquet` + the frozen as-built block) | **The one heavy exporter** (~394k rows × 9 coins). It is run as `showcase precompute leak_corr` → a cached small parquet that becomes the pinned input. The raw panel never enters the bundle. The precompute strips E5's sealed rows first (`strip_sealed`; disclosure policy N5 rule 2, SD-SC-13) |
| `leak_autopsy_events` | II.9 timeline | event | git log + SD-E4-24 / E4.P6.8b / E4.P7 / E4-G2 commits → date, event, sha, sd_ref | Feeds the "how it was found" strip, and the R1 replay later |
| `autorun_items` | III.11, IV.15 | item | AUTORUN_LEDGER table ⋈ git (sha → date, files, +/−) ⋈ `supervisor.log` + `costs.jsonl` (cost; the session → row rule of `agentic_inventory.md` §3) → item, epic, kind, reading, commit, api_equiv_usd (nullable), cost_source ∈ {log, unknown} | Named `api_equiv_usd`, not `cost_usd`: it is the notional API-price figure Claude Code reports, while the real spend was a flat subscription (P3 §14). Missing values stay null, and the UI shows them as gaps (P0 §6) |
| `autorun_pauses` | IV.16 | event | Supervisor `NOTIFY [high] … PAUSED` lines + ledger ⏸ rows → date, item, boundary letter. The reason text crosses only through the excerpt review (disclosure policy §4.4; SD-SC-13). From backlog mode (2026-10-15) a boundary opens a card instead: the `attention/` card headers whose title names a letter add rows (date, task, type, letter). A card's body holds the operator's answers and is never read | Boundary letter parsed from the reason or title; an unparsed PAUSE → `?`, listed in the review report. IV.16's (e) example, E4.P6.6's live shadow request, is a ledger sign-off row and a commit subject, neither a ⏸ row nor a PAUSE line: E9.P1.5 decides whether such a row counts (narrative IV.16; SD-SC-16) |
| `text/boundaries.json` | IV.16 | boundary | `.autorun/POLICY.md` "Approval boundaries" → letter, rule text: POLICY's boundaries as of the export, (a)–(g) on 2026-10-15 | Public. Each boundary's text is reviewed by hash in the review store (§7.3): verbatim, or a paraphrase, keyed by the sha256 of POLICY's exact text (as excerpts are keyed). A boundary whose current hash isn't recorded fails the export. At E9.P0.1, (e) is paraphrased without its note on the live box (P0 §10.3), and (f) is generic (SD-SC-09) |
| `guard_cases` | IV.16 tester | case | Run the plugin's **real** guard hook + binka `guard_rules.py` over (i) the plugin's self-test cases and (ii) a curated `content/guard_demo_cases.yaml` → command, cwd, decision, rule, message | Decisions come from the actual code, not re-implemented. Free-typing in the browser would ship the plugin's hook code, so it waits until the plugin is public (SD-SC-05) |
| `claims.json` | all | claim | `claims.yaml` → resolved (§6) | — |

### 5.2 P4 tables (format reserved, not built now)

- `arch_bakeoff`: union of `p16_*`, `p18_*`, `p23_autogluon`, `p25_tabm`, `p26_tabicl` eval
  parquets. These already share one schema (arch, coin, fold, val/test Sharpe, threshold,
  n_trades, gap), so this is nearly free.
- `label_geometry` (p17 stage1/2 → cell summaries)
- `feature_catalog` (`ml/feature_lists.py` + `bintri_features`)
- `e5_screens` + `s3_drift`, and the E5–E7 screen tables: `screen_limbs`, `null_dist` (the
  randomised-entry nulls of S3, E6 and E7; S3's book sits at the 40.8th pct) and `e7_funding`
  (E9-G0 Q3)
- `feed_snapshot` (I.6's dated snapshot, E9-G0 Q6: names and timestamps only, SD-SC-12) and
  `autorun_withheld` (§2's withheld count)
- `mlflow_summary` (experiment/run counts, metric summaries from a cached snapshot)
- `autorun_cost_daily`
- `replays/*`
- `pipeline_stats` (dataset sizes, row counts from `dataset.log`)

## 6. Claims resolution (`showcase claims`)

Each claim in `content/claims.yaml` (P0 §4.1) gains a machine-checkable `check`:

```yaml
- id: C-E4-024-collapse
  kind: recomputed
  values: {as_built_strict_median: 0.1463, causal_strict_median: -0.1353, causal_coins_positive: 0}
  check:
    table: leak_autopsy_coin
    sql: >
      select median(median_test_sharpe) filter (where substrate='as_built' and "window"='strict') as as_built_strict_median,
             ...
    tolerance: 5e-4
- id: C-E4-cost
  kind: recorded
  check:
    doc: doc/planning/E5_program_retrospective_2026-08-12.md#2-the-four-numbers
    contains: ["16.6–20.4 bps"]
```

- **`recomputed`:** the resolver runs the SQL with **DuckDB in Python** against the freshly
  written table. The site uses the same engine, so the verified query is the one the page
  can run. A mismatch beyond tolerance is a **hard failure**.
- **`recorded`:** the resolver checks that the cited section exists and contains the literal
  strings. That catches typos and stale anchors, not truth, which P0 human verification covers.
- **`illustrative`:** no check; the flag is carried to the UI label.
- `C-live-status` is `recorded` against a small `content/live_status.yaml` that holds E9-G0
  Q6's past-tense wording (P0 §10.3, SD-SC-07). I.6's snapshot carries its own date (P4 §8).
- The loop facts are `recorded` against `config.env` keys (C-loop-budget, C-loop-recovery,
  C-loop-limit). The check reads the named key, for example `MAX_LIMIT_WAIT`, and compares its
  value, so a changed config fails the claim instead of going stale (E9 §2 row 6). A value that
  names the tooling epic is described in the claim's text, never quoted (SD-SC-09).
- A claim whose check fails lands in `claims.json` with `status: failed`, and the build exits
  non-zero, unless `--allow-draft`, which binka-lab CI refuses for release builds.

Output per claim: id, text, value(s), unit, qualifier, status, and a provenance chip
`{doc, anchor, commit, fingerprint, table}`. P2 renders the chip from these.

## 7. Sanitizer and scanner

Three layers of defence, in the order they run:

### 7.1 Structural (by construction)

- The input allow/deny roots (§2). Denied files are never opened.
- Strict table specs (§4): no stray columns, no fine-grained timestamps in any table,
  and a `max_rows` cap on every table.

### 7.2 Redaction transforms (`sanitize.py`, applied to every text field)

| Pattern | Transform |
|---|---|
| Absolute paths under a home directory | `~/…` |
| Repo-absolute paths | repo-relative |
| Emails | removed unless allow-listed (operator's public address, if the operator wants it) |
| IPv4/IPv6, hostnames | `‹host›` unless in the closed allow-list: the third-party hosts the record names (exchanges, data vendors, documentation sites) and the two public sites' own hosts. Every other name under the operator's domains becomes `‹host›` too (disclosure policy N2; SD-SC-13, -22) |
| Notification-topic URLs | `‹notify›` |
| A mention of the tooling epic in a record that survived the filter (§2) | `a tooling epic, not shown` |
| Session ids (UUIDs) | `‹session›` (disclosure policy N9; SD-SC-13) |

### 7.3 Scanner (`scan.py`, runs over the final bundle bytes)

- **Stdlib only**, no binka imports. The same file is vendored into binka-lab `tools/`, and its
  version is stamped in the manifest.
- Pattern rules: cloud keys (AWS/R2 `AKIA…`, secret-key shapes), `Authorization:`/bearer
  tokens, basic-auth URLs `https://u:p@`, PEM blocks, 64-hex Binance-style keys, JWTs.
- High-entropy strings (≥ 32 chars, Shannon > 4.0) are flagged. An allow-list covers known-safe
  shapes: git SHAs (7/40 hex in `commit` fields), sha256 in manifest/footers, 32-hex run
  fingerprints. A 64-hex string passes only if it is a recorded digest (a manifest, footer or pre-registration hash),
  wherever it appears: SD bodies carry such digests in prose (SD-SC-13). The binka-side export checks each one
  against the record and lists it in the manifest, and the CI scanner allows only listed ones, plus the reviewed digests the manifest lists (the review store stays in
  binka).
- **Secret-value check (binka side only), by digest:** no session holds a secret value (disclosure policy N1;
  SD-SC-22). `showcase secrets digest`, which the operator runs in their own terminal (it refuses to run inside a
  loop session), reads the values from `py/.env` and the environment (the tracking server's credentials, the notification
  URLs, API keys) and writes, outside both repos, a salted sha256 per value and per encoded form (URL-encoded,
  base64, hex), each with its length and the secret's name. The scan hashes every same-length run of characters in
  the decoded strings and fails on a match, reporting the name only. A missing digest file fails the export, and so
  does one older than `py/.env` (checked by modification time, never by reading it); the manifest records the count
  (`secret_digests_checked`). This is the strongest check, and binka-lab CI can't run it,
  which is why the export refuses to write a bundle that failed it.
- **Excerpt review gate:** anything in `replays/` or marked `requires_review` (agent transcript
  excerpts, commit-message quotes beyond the subject line, passages of the loop's own files) must have
  its sha256 in the review store. `showcase review` shows each new or changed excerpt, redacted, and
  records the hash on my approval. A changed excerpt means a new hash, so it needs review again. SD entry
  bodies have their own per-entry review instead (§5.1; SD-SC-13), and transcript excerpts always go
  through this gate. Free text from the loop's logs, such as a PAUSE reason or a NOTIFY line, is an excerpt too
  (disclosure policy §4.4).
- **Review records** (disclosure policy §5; SD-SC-22). Every record (an excerpt's or a boundary's hash, an SD
  disposition, a flagged commit subject's disposition, a short-text value the release read covered) has one
  shape: the sha256 of the text as read, the published sha256 where it differs, the disposition and the date. All
  of them live in one store in binka, `py/showcase/review_records/`, written only by `showcase review`, the operator's
  command. It needs a terminal and refuses to run inside a loop session (an `AUTORUN_` environment, as
  `autorun-plan card answer` does). The store is one of the loop's protected paths (the operator adds it to
  `PROTECTED_PATHS`), so the supervisor's gate rejects an item that changes it. A value with no record is unread:
  the review report lists it, and in release mode record prose without one fails the export.
- **No silent fallback** (disclosure policy §3; SD-SC-22). The export fails if the private config is missing or
  any of its lists is empty (the tooling epic's rows, the live-box tokens, the account files, the redactions), if
  the digest file lacks a name on the private config's list of expected secrets, if the review store is missing,
  or if the policy differs from the commit its signature names anywhere outside the sign-off lines. Once the
  inventory's test reads the cache, a missing cache fails it rather than re-reading the archive. `showcase review`
  is run between loop items, and its records are committed before the loop resumes (a record left uncommitted dirties
  the tree, and a run during an item fails that item's gate). The operator reads each operator-run command before
  its first run.
- **History scan (binka side):** `showcase scan --repo ~/dev/binka-lab <range>` runs the same rules, the
  private token lists and the secret digests over the commits to be published: their trees, messages and
  author metadata. Every author, committer and co-author
  identity must be on an allow-list: the operator's published one and the agent's no-reply trailer.
  The operator runs it from binka before pushing those commits to the fresh public repo at launch, and
  again over each release's commits after (P3 §11.4; disclosure policy §4.9). In binka-lab, the vendored
  scanner also runs in the lab loop's check before each push, and in CI.

Findings fail the build, with file, offset and rule. There are no warnings-only rules in
release mode.

## 8. Work steps

1. **Input spike (half a session):** for each v0.1 table, open the source and confirm it holds
   what §5.1 assumes. Key points: whether the 9-coin spread pkls exist, whether the e4p6 pkls
   carry per-trade gross returns, and whether the frozen as-built B1 block is still on disk.
   Any gap is either downgraded to a `recorded` claim-backed tile or re-derived. Findings are
   recorded in the implementation plan.
2. Package skeleton: `config.py` roots, `sources/` with the isolation test, `TableSpec` +
   writer + manifest + `check`.
3. `scan.py` + `sanitize.py` + planted-secret tests (they must catch every planted secret and
   pass the allow-listed hashes).
4. Doc parsers (`docs.py`): SD splitter and the verdict-table parsers, with fixtures copied
   from real sections.
5. v0.1 exporters in dependency order: epics → verdict_ledger → sd_entries → autorun_items /
   pauses / boundaries → guard_cases → cost_wall_* → leak_autopsy_* (the corr precompute last;
   it is the only heavy job).
6. Claims resolver; bring every v0.1 claim to `verified`.
7. The first full `export --only v0.1` into `~/dev/binka-lab/data/bundle/`, then `check` for
   byte-identity, then the review report, read by me.

## 9. Tests (`py/showcase/tests/`, pytest)

| Test | Asserts |
|---|---|
| `test_isolation` | No file access outside `sources/`; allow/deny resolution, including symlinks and `..`; the filter drops the tooling epic's records from every reader and keeps only the withheld count; only the snapshot commands open a network connection, and `export` doesn't import them |
| `test_specs` | The writer rejects undeclared columns, bad dtypes, overflow, fine timestamps in any table (unless declared with one of the three exception kinds), and a string value holding a tooling-epic token or a live-box token |
| `test_determinism` | Exporting twice gives identical sha256s (a fixture bundle) |
| `test_scan` | Planted secrets (each rule and each encoding) are caught, the values through a fixture digest file; SHAs and fingerprints pass. Over a fixture repo, `scan --repo` catches a planted secret in a commit message and an identity that isn't on the allow-list |
| `test_review` | `showcase review` refuses a loop session and a session without a terminal; a record-prose value with no record fails a release-mode export |
| `test_sanitize` | Paths, emails, hosts and IPs are redacted; the allow-listed third-party hosts and the two public sites' hosts are kept, and any other name under the operator's domains is redacted |
| `test_parsers` | Each epic's verdict-table fixture parses to the expected rows; the SD split count per epic equals the log's unique numeric ids, with the fenced template heading skipped (SD-SC-10) |
| `test_claims` | Recomputed mismatch → failure; a recorded missing anchor → failure; tolerance respected |
| `test_guard_cases` | Every plugin self-test case reproduces its expected decision through the exporter path |

All fast tests run in under 10 s on fixtures. The real-data export is a separate `make`
target, not part of pytest. Since E9's loop wiring (2026-10-15, E9 §7), `CHECK_CMD` runs these
tests too.

## 10. Exit criteria

1. `export --only v0.1` succeeds with scanner findings 0, secret digests checked ≥ 1, and all
   v0.1 claims `verified`.
2. `check` reports byte-identity (every sha256 matches, ignoring `exported_at`).
3. The bundle is < 4 MB for v0.1, and every table is within `max_rows`.
4. `pytest py/showcase/tests` is green.
5. I have read the review report: redactions applied, unparsed boundary letters, the
   exception list for `min_time_grain`, and the short-text values the release adds (disclosure
   policy §5).

## 11. Decisions I've taken (flag if you disagree)

- **The bundle is committed to binka-lab git** (small, and parquet diffs are reviewable), not
  a release artifact. CI verifies manifest hashes. No LFS.
- **Prose is authored, numbers are exported.** Epic cards, headlines and replay narration live
  in `binka-lab/content/` (public, human-written). Numbers come from the bundle through claims.
  Nothing is auto-summarized.
- **Exporter code stays private in binka.** Only `scan.py` is vendored public, since its
  patterns are generic and its public presence is itself a signal.
- **No MLflow calls at export time.** A separate `showcase snapshot mlflow` (P4) writes a
  cached JSON that becomes a pinned input, so exports don't depend on the server. The two
  `showcase snapshot` commands (MLflow and the feed) are the only code that opens a network
  connection, and `export` never imports them; `test_isolation` checks both (disclosure policy
  §4.7; SD-SC-22).

## 12. Amendments from the P3 design (2026-09-30)

[P3](SHOWCASE_P3_design.md) §4, §5.3 and §6 need these v0.1 changes. They are built at P3 step 1.

| Change | Why |
|---|---|
| `cost_wall_coin` / `cost_wall_edge` cover the **dev quartet** (sui, dash, xrp, ton) × {spot, futures}, not 9 coins | The frozen E4 cost card measured only the dev quartet (holdouts were sealed at P1) |
| `leak_autopsy_corr` gains `shift_min ∈ {−2,…,+2}` | Drives the II.9 shift scrubber; same precompute pass |
| New `leak_autopsy_stage1` (dash + sui, 8 cells × substrate) from the E4.P6.8 causal card | II.9 beat 4 shows stage 1 and stage 2 |
| New `leak_autopsy_p7` (causal re-tune headline per coin) from the E4.P7 outputs | Answers the "misfit hyperparameters" confound inline |
| New `gate_events` (gate, date, option letter, verdict, commit) from the ledger's sign-off rows + commits | III.11 gate marks |

## 13. Amendments from E9-G0 (2026-10-15)

Applied by E9.P0.1 from [E9](E9_2026-10-15.md) §2 and §8. The rows are in-place fixes in §2, §5.1, §6 and §9. The
v0.1 rows are built at E9.P1.2–P1.7, and `gate_events` with the §12 deltas at E9.P3.1.

| Change | Why |
|---|---|
| The allow-list names `supervisor.log` and `costs.jsonl` in `.autorun/state/logs/`. `.autorun/` narrows to its top-level files and card headers; the rest of `.autorun/state/` is denied, session logs included | E9 §2 row 5. The session logs are transcripts |
| The tooling epic is cut once, at the source layer, with a withheld count, a sanitizer transform for mentions, and a writer backstop (§2, §7.2) | E9-G0 Q5; SD-SC-08 |
| The deny list adds the E6/E7 sealed trees and raw data | E9-G0 Q3 |
| `text/epics.json`, `verdict_ledger` and `gate_events` cover E6 and E7. The parser keeps "would KILL" limbs inside their NO-READING row and marks report-only books as not verdicts | E9-G0 Q3; P3 §2 |
| `text/sd_entries.json` splits the E3–E7 logs, skipping each log's template heading, and C-SD-count is the splitter's count | E9-G0 Q3; E9 §2 row 3; SD-SC-10 |
| `autorun_pauses` adds the cards of backlog mode | E9 §2 row 6 |
| `text/boundaries.json` follows POLICY's boundaries as of the export. Each boundary's text is reviewed by hash, and (e) and (f) are paraphrased | E9 §2 row 6; SD-SC-09 |
| Loop facts are claims checked against `config.env` keys; C-live-status holds the past-tense wording (§6) | E9 §2 row 6; E9-G0 Q6 |
| Tests cover the tooling epic's filter, the writer's check for its tokens and the SD split per epic, and `CHECK_CMD` runs them (§9) | E9-G0 Q5; E9 §2 row 3; E9 §7 |
| Until E9.P2.0 the export writes to `py/showcase/out/` (§2) | E9 §5 P1.8; SD-SC-06 |

## 14. Amendments from the disclosure policy (2026-10-16)

Applied by E9.P0.2 from [`disclosure_policy.md`](disclosure_policy.md). The rows are in-place fixes in §2, §4, §5.1,
§7.2 and §7.3, built at E9.P1.2–P1.6.

| Change | Why |
|---|---|
| `text/sd_entries.json`: a per-body review record replaces the excerpt-review exemption (§5.1, §7.3) | SD-SC-13 (1) |
| String columns declare a class, and record prose needs a review record (§4) | SD-SC-13 (1) |
| `autorun_pauses`: the reason text is an excerpt, and so is any free text from the loop's logs (§7.3) | SD-SC-13 (4) |
| The seal is applied once in `sources/`, so `leak_autopsy_corr` and P4's precomputes inherit it (§2, §5.1) | SD-SC-13 (2) |
| The sanitizer replaces session ids and keeps public vendor hosts (§7.2). A 64-hex string passes only as a recorded digest (§7.3) | SD-SC-13 (4) |
| `py/doc/` is allow-listed by named doc (§2) | SD-SC-13 (4) |

## 15. Amendments from the agentic inventory (2026-10-16)

Applied by E9.P0.3 from [`agentic_inventory.md`](agentic_inventory.md). The row is an in-place fix in §5.1, built
at E9.P1.2 and P1.7.

| Change | Why |
|---|---|
| `autorun_items`: cost comes from `supervisor.log` and `costs.jsonl` by the inventory's §3 rule, and `cost_source` drops `commit_msg`: commit messages hold no session cost. `sources/autorun.py` may take over the parsers of binka's `py/util/agentic_inventory.py` (§5.1) | SD-SC-14 |

## 16. Amendments from the claims register (2026-10-16)

Applied by E9.P0.4, which wrote `claims.yaml`. The decision record is SD-SC-15 (2); §6's resolver
(E9.P1.7) reads the register in this shape and takes over binka's `py/showcase/tests/test_claims_yaml.py`.

| Change | Why |
|---|---|
| §6's `check` also takes `files` + `column` + `distinct` (the distinct values of a column across parquet globs, named, not counted (E9.P1.1); `C-arch-families`) and `guard_selftest` (the guard hook's self-test counts, run in binka; `C-guard-tests`, N10). P1.7 may re-express the first as `sql` over `read_parquet` | Two v0.1 claims had no other check that runs before P1 |
| A `recorded` doc check names its doc and its section separately (`doc`, `section`: the heading's opening text), not as `doc#slug`. P1.7 may convert them to slugs | A `—` or `§` in a heading made the slug fragile |
| A claim may carry `as_of` (the cut-off of a growing count) and `pending` (what produces a draft's value); `source` may carry `fingerprint` (a gitignored input) and `private` (N10), and its `commit` may be a list when the values were recorded in several commits | Provenance the register needed |

## 17. Amendments from the input spike (2026-10-16)

Recorded by E9.P1.1; the evidence is in `E9_P1.1_input_spike_2026-10-16.md` §2
and §4 (SD-SC-19). Each row is built by the item named; §5.1 is not rewritten until then.

| Change | Built at |
|---|---|
| `verdict_ledger` adds `verdict_raw` (the verbatim word). `verdict` stays the five-word enum, set by one vocabulary map (word → enum, after glyphs and suffixes are stripped) with per-row overrides only where context changes a word's meaning; an unmapped word fails. E2's row comes from the label-sweep doc (there is no E2 close-out) | E9.P1.4 |
| The SD splitter keys on the id token, `^### (SD-E\d+-\d+)\b`, whatever separator follows (E7's first six entries use a colon). It reads the five logs by name (`completed/E3_…`, `completed/E4_…`, `planning/E5_…` … `E7_scope_decisions.md`), never a glob: a glob would match the tooling epic's denied log | E9.P1.4 |
| `cost_wall_edge` reads the per-trade net multipliers (`mults`) of the `spot_honest` eval rows; gross = log-return bps + the coin's spot c_RT. The as-built source is `calendar_eval.parquet`, the causal one `p68b_eval.parquet` | E9.P1.6 |
| `leak_autopsy_coin`'s key is coin × substrate × panel ∈ {calendar, holdout} × basis ∈ {strict, all}: "strict" is a cell basis, not a window, and the holdout panel exists only as built | E9.P1.6 |
| `leak_autopsy_corr`'s exact-filename allow-list adds `<coin>_merged.parquet` (column `close`), its `.scaler.json` sidecar (E4's `_raw_close` inverts the log-z scaling with it) and `_market/BTCUSDT_1m.parquet`, both through `strip_sealed`. The precompute reads the BTC series once and derives every shift from it, and each coin's forward return once. Its seal-stripped correlations are compared with SD-E4-24's recorded ones (sui, xrp, eth), and the difference is disclosed | E9.P1.6 |
| `autorun_pauses` matches the NOTIFY form `PAUSED — needs you`. A card's letter comes from a `boundary:` header field, which the card writer doesn't emit yet; until it does, a card row is `?` | E9.P1.5 |
| `leak_autopsy_events` and `gate_events` read curated files with one validator: a row's commit exists and its date matches. E3's gates have commits (G1 `ccdeb9f`/`bfcf3e0`, G2 `bb5d1b0`/`83dd266`) but no ledger row. `gate_events` rows keep §12's gate, option letter and verdict. E3's gates and E6-G1/E7-G1 have no ledger row of their own | E9.P1.5, E9.P3.1 |
| Every result reader resolves provenance one way: the `.footer.json` sidecar; else the file's own `fingerprint` key (E6's and E7's cards); else the sha256 its card's `fingerprint` lists for it (E6's and E7's other outputs); else it fails | E9.P1.6, E9.P4.E2 |

## 18. Amendments from the policy's revision (2026-10-16)

Applied by E9.P0.8 from the revised [`disclosure_policy.md`](disclosure_policy.md) (the G1 dossier's §7; SD-SC-22).
The rows are in-place fixes in §1, §2, §3.1, §4, §5.1, §7.2, §7.3, §9, §10 and §11, each built by the item named.

| Change | Why | Built at |
|---|---|---|
| The manifest names each input by a label from the private config, never by its path, and its strings take the table classes (§3.1) | A path can name a private repo or a denied file, and the manifest's strings had no class (policy §4) | E9.P1.2 |
| No file pulled from an exchange account is an input: such files are denied by exact name, and `cost_wall_coin` reads E4's frozen card and its spread summaries, labelled as pre-seal (§2, §5.1) | Policy N2's carve-out and N5 rule 4 | E9.P1.2, P1.6 |
| The writer's backstop also rejects a private list of the live box's identifying tokens, and the token lists serve every crossing: the writer, the move's check and `scan --repo` (§2, §7.3) | Policy §3, N2 | E9.P1.2, P1.3 |
| A time-grain exception declares one of three kinds (§4) | Policy §2 | E9.P1.2 |
| Only the snapshot commands open a network connection, and `export` never imports them (§11, §9) | Policy §4.7 | E9.P1.2; the commands at E9.P4.E9 |
| The sanitizer's host allow-list is closed: third-party hosts and the two public sites' own hosts. Every other name under the operator's domains becomes `‹host›` (§7.2) | Policy N2 | E9.P1.3 |
| The secret-value check compares salted digests that the operator writes from their own terminal; no session holds a value, and a digest file older than `py/.env` fails the export (§7.3) | Policy N1 | E9.P1.3, which asks the operator for the digest file on an act card before E9.P1.8 |
| One review store in binka, one record shape and one command: `showcase review`, the operator's alone. The store is a protected path, and passages of the loop's own files are excerpts (§5.1, §7.3, §9) | Policy §5, N10 | E9.P1.3; the operator adds the store to `PROTECTED_PATHS` (act card A-003) |
| `showcase scan --repo` runs over the commits to be published, commit metadata included, before they go to the fresh public repo at launch and with each release after, run by the operator; the lab loop's check runs the vendored scanner before each push (§7.3, §9) | Policy §4.9 | E9.P1.3; run at launch (P3 §11.4) |
| No silent fallback: a missing private input fails the export, and so does a policy changed since its signed commit (§7.3) | Policy §3, §7 | E9.P1.2, P1.3 |
| The verdict parsers drop any cell that carries a tax rate (§5.1's `verdict_ledger`) | Policy N7 | E9.P1.4 |
| E9.P1.5's sweep proposes a disposition for each commit subject it flags in a table; the dispositions join the SD review | Policy §4.3 | E9.P1.5 |
| The review report lists the short-text values a release adds, for the release read (§10) | Policy §5 | E9.P1.8 |

## 19. Built at E9.P1.2 (2026-10-16)

The skeleton of §2–§4 and §9–§11 is in `py/showcase/`, with §18's rows marked E9.P1.2 (SD-SC-23). Where the code
fixes something this design left open, it is recorded here; the rest of the design stands as written.

| Point | As built |
|---|---|
| The private config | `py/showcase/private_config.yaml`, in binka. It holds the tooling epic's id, paths and tokens, the live box's tokens, the account files (exact names, no patterns) and the input labels, read-only once loaded. No line this item wrote names its contents; the older mentions in the showcase docs are on the E9.P2.0 move list (the private sweep file's §3). Only `sources/` reads it. A missing file, invalid YAML, an empty list, a scalar where a list belongs, an epic id that isn't `E<n>`, a bad label or a token that isn't a regex fails the export. The redactions (E9.P1.5) and the expected secrets' names (E9.P1.3) join its required lists with their items |
| Inputs | Every input is read by its label, which the private config maps to a path; a read with no label fails, and the path still passes the roots. The manifest lists label, sha256, bytes and the `.footer.json` fingerprint; a footer without its sha256, one whose sha256 names other bytes, or one whose fingerprint isn't hex fails. The policy is read as a check, not an input: it is dirty-checked but has no manifest row |
| The roots | `config.py`: named files (the docs by name, the loop's top-level files, the two logs) and allowed dirs. Each denied root carries its own exact-name exceptions, which are thereby allowed with their `.footer.json` (`.autorun/state/` keeps its two logs; `~/data/bintri/` takes E9.P1.6's and P4's files), and the private config adds the tooling epic's path patterns and the account files. A path passes only if it is allowed and not denied both as written (with `..` folded) and with its symlinks resolved |
| The cut | `Sources.drop_hidden(records, key, kind)`: a record goes when the first epic id in its own id (an item, an SD id, a commit subject) is the tooling epic's, as the inventory's script decides; the count is kept per kind |
| The policy's signature | The Signed line in §7 reads `- [x] Signed (…): <date>, <initials>, <card>, <commit>`. Unsigned, the manifest says `policy_signed_commit: null` and `--release` fails. Signed, the text must equal the named commit's outside the sign-off lines, which are the opening Status paragraph, the Signed line and §7's gate records (`- Gate E9-G…` lines); the carve-outs line and anything after §7 are compared. The committed text is read through the same roots as a file on disk (`Sources.read_committed`), and only `sources/` may call the git and internal readers |
| Release mode | `export --release`: the signed policy, a clean tree and a review record for every record-prose value. The review store is E9.P1.3's; until then a release export fails on any record prose |
| The spec | `schema/` holds the column types (`Str` with its class, `Int`, `Float`, `Bool`, `Date`, `Timestamp`) and `TableSpec`; each table's spec sits beside its exporter. `min_time_grain` is `"1d"`, or `None` with a reason and one of the three kinds. The raw-row guard also fails a non-prose string holding a date with an hour (ISO, compact or day.month.year hh:mm); an integer column of epoch seconds can't be told from a count, so it rests on the spec's review. A table name is lower-case letters, digits and `_`. `fmt="json"` writes a spec'd table to `text/<name>.json`; `act` sets the per-act budget |
| The bundle | `export` builds every file in memory, then writes them to a staging dir and swaps it into `<out>/v1/` whole, so a failed build writes nothing. The manifest also carries `policy_signed_commit`, `autorun_plugin_dirty` (a dirty plugin tree fails like a dirty binka one), `pyarrow_version`, `unreviewed_prose` and `bytes`; `claims` and `scan` join with their items, and `content_commit` stays null until E9.P2.0. The manifest records `only` (the release an `--only` export kept), two tables can't share a name, and the dirty check covers the exporter's own code with the inputs. `check --bundle` takes the dir `export --out` took, rebuilds the same release set and names each file or manifest key that differs |
| Running the tests | `py/showcase/` is a package inside `py/`, which has its own `__init__.py`, so the suite runs with `--import-mode=importlib` and `PYTHONPATH=ml:.` from `py/`, as `CHECK_CMD` does (§10 criterion 4). A `pytest.ini` beside the tests would set it, but pytest then picks that file up for `CHECK_CMD`'s whole run, which breaks other suites |
| Network | No module imports network code except a `snapshot*` module (none yet), checked statically; and `export` runs under an audit hook in a subprocess that records no socket event and no snapshot module loaded |
| The inventory's cache | `util/agentic_inventory.py --build-cache`, the operator's pass (it refuses a loop session), writes `py/showcase/cache/archive_metadata.json`: per transcript its name, first timestamp, tallied epic and anchor lines, pinned to the script's cut-off, anchors and tally rules. `build(cache=…)` reads it and fails on a missing or stale file. Act card A-004 asks for the run; until the item that applies it switches the test, the test repeats the pass (D2′). The test also checks the rendered block for the private token lists (G1 V2) |

## 20. Built at E9.P1.3 (2026-10-17)

§7.2–§7.3 and §18's rows marked E9.P1.3 are in `py/showcase/` (SD-SC-24). Where the code fixes something §7 left
open, it is recorded here; the rest of §7 stands as written.

| Point | As built |
|---|---|
| Decoded strings (SD-SC-11) | `scan.py` reads every JSON string with its keys, every parquet string cell, column name and schema metadata value, and every file's path; other files as text. It is standard library only but for one lazy `pyarrow` import in its parquet decoder, which binka-lab's CI installs; a tree with parquet and no pyarrow fails. The export scans its files in memory, after the writer and before anything is written |
| Rules | Credential rules (always applied): cloud key ids, PEM blocks, authorization headers, bearer tokens, credentials in a URL or a `-u` flag, JWTs, known token prefixes, notification-topic URLs, password assignments. Shape rules: 64-hex, longer hex, a 64-character mixed key, and entropy (≥ 32 base64 characters, Shannon > 4.0, not word-like). Git SHAs and 32-hex fingerprints pass because hex can't exceed 4.0 bits |
| What passes a shape rule | A recorded digest by its exact token (the manifest's `*sha256` and `*fingerprint` values) and a string a review record covers, by its sha256: the manifest lists those (`reviewed_prose_sha256`), and CI exempts exactly them. Release mode fails on any finding; a dev export records `scan_findings` |
| The sanitizer | Runs inside `build()` on every short, authored and record-prose string before the writer's checks; a structured value it would change fails. Order: notification URLs, emails, user-at-host strings, home and repo paths, session ids, IPv4/IPv6, hosts, the tooling epic's mentions (`a tooling epic, not shown`, keyed on the private config's id). The host allow-list: third-party domains with their subdomains, the two public sites by exact name; other hosts under a closed TLD list become `‹host›` |
| The digest file | Outside both repos, mode 0600, written by `showcase secrets digest` (operator only). Per expected secret: salted sha256 of the raw value, percent-encoded, base64, hex and a URL's path, each with its length. The export fails if it is missing, older than `py/.env`, lacks an expected name (the private config's required `expected_secrets`) or holds no digest; `--no-secret-check` is a dev run's (manifest `secret_digests_checked: 0`) and `--release` refuses it |
| The review store | `py/showcase/review_records/<published sha256>.json`: `sha256`, `published_sha256` where it differs, `disposition` (`publish`, `redacted`, `withhold`), `date`. `showcase review` (operator only) shows each record-prose value with no record as published, with the shape rules it trips, and writes the answer; `build()`/`check()` read the store by default. A withheld value is not asked again and fails a release while a table still holds it |
| `showcase scan` | `PATH...` (a bundle dir uses its manifest's records) or `--repo REPO REV...`: every commit's tree, file names, message and identities, through `git log` and one `git cat-file --batch`. Identities: the private config's `published_identities` (empty fails) and the agent's no-reply |
| The manifest | Adds `scanner_version`, `scan_findings`, `secret_digests_checked` and `reviewed_prose_sha256`. `check` compares `secret_digests_checked` as checked-or-not, since the count is the local file's |
| Operator-only commands | `review` and `secrets digest` refuse an `AUTORUN_` environment and a session without a terminal (`operator_only.py`) |

## 21. Built at E9.P1.4 (2026-10-17)

§5.1's doc parsers and §17 rows 1–2 are in `py/showcase/sources/docs.py` (SD-SC-25). Where the code fixes something
§5.1 left open, it is recorded here; the rest stands as written.

| Point | As built |
|---|---|
| Inputs | Each doc is read by label (`sd_log_e3` … `sd_log_e7`, `verdicts_e2` … `verdicts_e7`, `verdicts_e4_g1`, `verdicts_e4_redecision`) and is on `ALLOWED_FILES` by name. E4-G2's source is the re-decision's sign-off (`E4_P6_redecision_2026-08-04.md` §12.1), not the G2 dossier |
| The splitter | `sd_entries(src)` → `SDEntry(id, epic, date, title, body, refs)`: keyed on the id token, fenced blocks skipped, an entry ending at the rule after it; 148 entries, the inventory's ids. `refs` expands the logs' abbreviations |
| The verdict rows | `verdicts(src)` → `rows` (`VerdictRow`: epic, id, level ∈ {screen, gate}, cls, verdict ∈ the five words or None for a report-only book, verdict_raw, deciding, bar, limbs, sd_refs, commit, report_only), `gates` (`GateRow`: epic, id, reading, sd_refs, for `gate_events`), `skipped` (milestones, pre-steps, cells that never ran, gates not reached, and E3's two carried cells with their deciding numbers and a note in E3's words: for the review report) and `dropped` (the N7 drops) |
| Gates | A gate decision is a gate row unless it closed the program NO-GO (E2's sweep, E3-G2, E4-G2: verdict rows with `level = gate`). No row reads GO |
| The vocabulary | One map after glyphs, bold and suffixes; of E3's own words, INCONCLUSIVE → NO-READING and TAKER-DEFAULT → KILL. SURVIVE-null (B2) and LIFT-BUT-SUB-ZERO (the P4.1 flagship) map to no verdict: they are listed as `carried` by name (`CARRIED`), the flagship in E3's words ("does not KILL … does not pass G2's positive-median-Sharpe bar"), its +0.084 lift with the shutdown dossier's §12.3 downgrade (E9.P1.4a; decision card D-001: `strict`). Unmapped words, missing columns, wrong cell counts, missing sections and unclosed fences fail |
| N7 | A kept cell with a tax word and a number is dropped and listed. SD bodies aren't filtered: their review record decides (E9.P1.5 reads them for N7) |


## 22. Built at E9.P1.5 (2026-10-17)

§5.1's doc- and loop-derived v0.1 tables are in `py/showcase/exporters/` (`docs.py`, `loop.py`), on readers in
`sources/` (`docs.py`, `loop.py`, `guard.py`), with §17's E9.P1.5 rows (SD-SC-26). Where the code fixes something §5.1
left open, it is recorded here; the rest stands as written.

| Point | As built |
|---|---|
| `text/epics.json` | An authored `showcase/epics.yaml` (E0–E7; it moves at E9.P2.0), validated before it crosses: E0–E4's window, question and verdict equal the retrospective's §1 cells, each card's literals appear in its source (E5–E7's close-out §1 prose), and its `C-epic-<id>-verdict` claim records its verdict. E3's card carries the look-ahead downgrade with its lift (SD-SC-25, D-001) |
| `verdict_ledger` | One row per `verdicts().rows` (§21), `sd_refs` space-separated. The free cells are short text, so a cell over 120 characters is record prose (policy §4). E3's two carried cells left at E9.P1.4a (D-001: `strict`): 25 rows |
| `text/sd_entries.json` | Every E3–E7 entry: id, epic, date, title (short text), body (record prose), refs, `withheld`. The private config's new required `redactions` (SD id → phrases) cuts each phrase from the title and body to `‹redacted›`, and a phrase that no longer matches fails. An entry whose published body the review store withholds is its id only (policy §4.2). The SD review's record keys on the body; the title is short text, read value by value at the release read |
| `autorun_items` | The ledger's rows oldest first (`n`). The hidden epic's rows are cut by the row's epic, inherited from the older row when its item names none (the inventory's rule); then the private `ledger` phrases are cut from the rest, joined to git (the row's commits: count, files, +/−; "(this commit)" resolved by `git log -S` on the ledger) and to the sessions' cost by the inventory's §3 rule (`agentic_inventory.item_costs`, through `sources/`). `api_equiv_usd` is null where no session matched (`cost_source = unknown`). `glyph` and `kind` (from the item's "(impl, review)") are structured; the item and reading cells are short text, so most readings are record prose |
| `autorun_pauses` | One row per (PAUSE, letter) from three sources: `PAUSED — needs you` NOTIFY lines, ledger ⏸ rows and the cards that name a boundary. Each gives its day, an item (an item id, the ledger's item cell or a card's task) and the letters it names, a chain of `(x)` after the reason's start, "boundary", "PAUSE" or a dash; none gives `?`. No reason or reading crosses. A card is read to the end of its header only (`Sources.read_headers`), and only its id, type, task, title, created and boundary fields are kept; a card's letter comes from its title ("boundary (d)") or a `boundary:` field, which no card writer emits yet; a card that names none is no PAUSE and has no row |
| `text/boundaries.json` | POLICY's "Approval boundaries", bullet by bullet, verbatim without the bullet marker, or as the paraphrase in the authored `showcase/boundary_paraphrases.yaml`, bound to the sha256 of POLICY's exact bullet: a changed bullet fails until its paraphrase is written again. (e) and (f) are paraphrased (P3 §9; policy rule 5). The text is record prose, so each boundary needs its boundary review record; the hash isn't published (a 64-hex value would trip the scanner) |
| `guard_cases` | The plugin's hook, read by label and run in-process: its 25 framework cases under its synthetic policy and binka's 25 CASES under binka's rules. The hook and binka's rules run from the bytes read by label. Each case is published as the sanitizer rewrites it (a home or repo path becomes `~` or repo-relative) and decided by the hook on exactly that command; a rewrite that would change the decision fails the export. Each row has the case's expected decision, the hook's decision and message, and the rule that fired, found by calling the hook's own rules in `check`'s order (a replay of that order: the hook doesn't report the rule). The curated `guard_demo_cases.yaml` wasn't built: binka's CASES already hold P3 §9's four examples |
| Inputs | New labels: `epics`, `epics_retrospective`, `claims`, `autorun_ledger`, `supervisor_log`, `autorun_costs`, `autorun_policy`, `autorun_cards` (a dir), `boundary_paraphrases`, `guard_rules`, `guard_hook`. The cards are one input, hashed over the fields kept from every header, so an answer changes no input row. An export reads each input once (`Sources` keeps the bytes), so a live log can't differ between two tables and its manifest row. `epics.yaml` and `boundary_paraphrases.yaml` join `ALLOWED_FILES` |
| Not built here | `leak_autopsy_events` and §17's curated-file validator go with the rest of the leak autopsy at E9.P1.6; `gate_events` at E9.P3.1 |

## 23. Built at E9.P1.6 (2026-10-17)

§5.1's data-derived v0.1 tables are in `py/showcase/exporters/data.py`, on readers in `sources/` (`results.py`,
`market.py`, `docs.curated`), with §12's `shift_min` and §17's E9.P1.6 rows (SD-SC-28). Where the code fixes
something §5.1 left open, it is recorded here; the rest stands as written.

| Point | As built |
|---|---|
| Provenance | `Sources.read_result`: a result file's `.footer.json`, else the sha256 `config.PINNED` holds for its label, else it fails. E4's files predate the footer convention and carry no fingerprint of their own (only `p68b_eval.parquet` has a digest in E4's freeze record, a blake2b, which matches), so this item pinned the eight it reads after checking them against the record. §17's other two clauses (a file's own `fingerprint` key, a card's list) join with their first readers at E9.P4.E2 |
| `cost_wall_coin` | The frozen card's c_RT table (dev quartet × spot, futures), its impact allowance and its funding table, with each coin's half-spread p50 and p90 at signal-like minutes from its `*_spread.pkl` (the p50 must equal the card's to 3 dp) and the spread window labelled per coin (2025-01-01 to its last minute). c_RT is re-derived from its terms (2 × fee + 2 × (half-spread + impact) + funding) within 0.02 bp, the card's rounding. The fee-source column is never read out (N2) |
| `cost_wall_edge`, `cost_wall_edge_hist` | Per coin and substrate, the flagship's trades (arm F, the named head `causal_rate_q`, spot_honest, every evaluable cell: E4's `_cell_rows` and `_pooled_mults`) as gross bps = mean net log return (E4's `_mult_stats`) + spot c_RT: n, μ, σ, and a second table of fixed 12-bps bins over ±300 bps with under- and overflow bins (a list column has no type in the spec). The pooled trades must equal the cells' recorded trade count and trade-weighted EV. μ is on E4's log basis: on an arithmetic one it is 0.3–0.6 bps higher (xrp's causal −0.27 becomes +0.36) |
| Windows | `cost_wall_edge`, `cost_wall_edge_hist` and `leak_autopsy_coin` carry `test_from`/`test_to`: the calendar panel's test span from E4's `window_bounds` (2025-10-24 → 2026-06-30), pre-seal record labelled (N5 rule 4). The holdout's folds are each coin's own and its eval file holds no dates, so its rows carry null (SD-SC-28). `cost_wall_coin` carries each coin's spread window |
| `leak_autopsy_coin` | Key coin (the nine and `all`) × substrate × panel × basis, basis ∈ {`all`, `strict` (over the 40-trade floor in that substrate), `paired_strict` (over it in both; stage 2's declared basis, E4's `paired_cells`)}: §17 had two bases, but E4.P6's confirmation (C-E4-P6-confirm) and stage 2 (C-E4-024-collapse) use different strict bases. The holdout panel is as built only |
| `leak_autopsy_corr` | Read from the pinned cache `cache/leak_corr.parquet`, which `showcase precompute leak_corr` writes (§5.1): 9 coins × 5 features × 2 substrates × `shift_min` −2…+2. The market readers (`sources/market.py`) take each input by exact name, hashed as it streams, and strip E5's sealed rows on read (BTC by its bar's close time); on the grid a forward fill never crosses a sealed minute. Features come from p35's `dev_grid` and `_btc_features` and the forward return as in `mechanism()`; `shift_min = s` reads BTC s minutes later than the substrate does. A certificate requires the derived shift-0 features to equal the B1 parquets' columns away from the seal edges (max \|Δ\| ≤ 1e-9, NaN masks equal); on the real files it is 0 over 47.3 M values. A non-finite correlation fails. The footer records every input's sha256, the parameters (shifts, horizon, edge, tolerance; with the inputs, they make the fingerprint) and the certificate. The rows are sorted by key, so a rerun is byte-identical |
| `leak_autopsy_events` | The authored `leak_events.yaml` (II.9 beat 6's chain, one commit per event), through `docs.curated`, §17's one validator for curated files: the fields, a quoted sha, the commit is in HEAD's history and its author date is the row's day, rows in date order; a repeated commit is checked on every row. `gate_events` reuses it at E9.P3.1 |
| The import chain | `export` imports no `ml/` module: E4's and E5's code is imported inside the functions that use it, so the audit subprocess (`PYTHONPATH=py`) still runs; the data builds get their own audit run, with `ml/` on the path. The dirty check adds every module under `ml/` the build imported (`sys.modules`), so an uncommitted edit to E4's code dirties the export |
| The market reader | `Sources.read_parquet(label, columns)`: the file's bytes are read once, hashed and parsed, one file at a time and not cached, with `read_bytes`' footer rule (`_record`). No checked path leaves `sources/` |

## 24. Changed at E9.P1.6a (2026-10-18)

C-002's changes H1–H10 (interim dossier §6.1; SD-SC-29, SD-SC-30). Each row
amends the row of §19–§23 it names; the rest stands as written there.

| Point (amends) | As built |
|---|---|
| `autorun_items`' counts (§22) | `n_commits`, `files`, `added` and `deleted` are nullable `Int64`. Besides SHAs and "(this commit)", a commit cell's words count: "close-out" is the commit that added the row (`git log -S`), any other name the one commit whose subject names the item id and holds the name. A name that resolves to none or two, an unknown SHA or a fragment nothing reads nulls all four; a row naming no commit has `n_commits` 0. The costs keep the inventory's join |
| `text/sd_entries.json` (§22) | The SD review's record keys on the entry's title, refs and body together (`TableSpec.review`), as published; a title-only change is asked again. A withheld entry is its id, epic and `withheld`: `date` is nullable and null |
| The sanitizer (§20) | An email's last label starts with a letter (E4's F notation, an `F`, an at-sign and `1.0`, stays); `precision@top-k`, `prec@top-k` and `top-<n>` stay (`AT_NOTATION`); `user@<IPv4>` is redacted whole, and a full stop after an address doesn't save it |
| What passes a shape rule (§20) | A manifest's records exempt only the files under its own directory: `scan PATH...` and `scan --repo` scope each manifest by its path. The export's own scan is one bundle, one manifest |
| The policy's signature (§19) | The commit is the Signed line's last comma-separated field (backticks and a full stop stripped), so a compact date before it is never taken for it |
| Release mode, `check` (§19) | The manifest records `release`; `check` rebuilds a release bundle as a release, so a review record gone since fails it. A bundle with no `release` key checks as a dev one |
| The bundle (§19) | A failed write or final swap leaves the old `v1/` and no `.stage-*` or `.old-*` dir; a run killed between the two moves leaves `.old-v1/`, which the next run puts back first |
| `leak_autopsy_corr` (§23) | The cache's footer also names the sha256 of the code that made it (`precompute.py`, `sources/market.py`, every `py/ml` module the run imported), and the fingerprint covers it. A cache footer without `code`, a changed hash or a missing file fails the read (`Sources.code_digests`, only `.py` under `py/ml` or `config.CODE`). Rerun 2026-10-18: parquet byte-identical, fingerprint `a8a26a6b5ca82c19` |

## 25. Built at E9.P1.7 (2026-10-24)

The claims resolver of §6 (SD-SC-31). Each row amends the section it names; the rest stands as written.

| Point (amends) | As built |
|---|---|
| Where it runs (§6) | `showcase/claims.py`, called by `bundle.build` after every table: the claims are one more table, `text/claims.json` (§3's `claims.json` sits in `text/` with the other structured files), through the sanitizer, the spec, the token backstop and the scanner like the rest. Its strings are structured or authored; a claim's `as_of` or qualifier may name a commit's or a log line's time, so the table declares a `record_event` time-grain exception. The manifest's `claims` is `{total, verified, draft, failed}` |
| A failed claim (§6) | Fails the export unless `--allow-draft` (a dev run; a release refuses it, and the manifest records it); `check` rebuilds with the old bundle's mode. A failure on a private source names nothing (N10). `showcase claims` lists each claim's status from a dev build in memory |
| The engine (§6) | The stdlib's SQLite in memory (`sources/sql.py`: `sqlite3` may open files, so only `sources/` imports it), with DuckDB's `median` registered. The SQL is written in the dialect both share (aggregates with `FILTER`, `median`, `round`, `count(distinct …)`, dates compared as ISO text), so the page can run the query that was checked; the SQL avoids SQLite's integer `/` and compares a timestamp with a full one. Only a SELECT runs (the authorizer). DuckDB isn't in the lock; adding it re-resolves the training environment's lock (SD-SC-31) |
| The checks (§6, §16) | `{doc, section, contains}`, `{config, key, equals}`, `{files, column, distinct}`, `guard_selftest` (the hook's own cases through `guard.guard_cases`, every one with its expected decision) and `{table, sql, tolerance}`: the SQL's one row over the table as published; each column names a value, matched exactly or within the tolerance. `table` alone names the table a value is shown from and checks nothing. A check whose table isn't in the build is skipped and listed (`unchecked`), and the claim is a `draft` in that build; a verified claim with no check fails. A malformed entry fails the build with its id. The `section` stays a heading prefix; a verified claim's own source (doc, section, fingerprint) must resolve too |
| The values (G1 dossier V5) | Every value a verified claim states is covered: by an SQL column, by a number or a word in the evidence its checks matched (the quoted literals, a key's value, the guard counts, the distinct names; a number as written, as a percentage of a share, or rounded half-up to the value's own places, never to an integer; counting words count; a date's or an id's digits don't), or by its `derived` note, which says why the source doesn't quote it (a glyph, a count of quoted rows, a difference) |
| Inputs | Every file a claim cites is a labelled input (`Sources.read_cited`, `Sources.distinct`), so the manifest lists it: nine docs and `.autorun/config.env` join the private config, and so do C-arch-families' 17 bake-off evals, by name (a new eval file the globs reach fails until it is labelled) |
| Growing counts | C-loop-items and C-pauses-by-boundary are pinned at their `as_of` by the SQL's date filter (2026-10-18), so a new ledger row moves the table, not the claim; a release restates the cut-off. A count no earlier record states (these two, C-verdict-counts) is verified as the exporter's own count over its table, and its qualifier says so |

## 26. Built at E9.P1.8 (2026-10-25)

Gate E9-G2's code (SD-SC-33). Each row amends the section it names; the rest stands as written.

| Point (amends) | As built |
|---|---|
| A withheld value (§7.3, §24) | Outside a review unit, the writer publishes it as `‹withheld›`, structured, wherever its published text appears. A review unit keeps its exporter's rule and the release check. A source value equal to the marker fails |
| The review report (§10 criterion 5, §18's last row) | `showcase report [--only]`, over the tables as `build` would publish them (`bundle.as_published`, the claims last), by place (table · key · column): redactions applied (markers, a path, any other rewrite), withheld values, boundary letters not parsed, time-grain exceptions, record prose with no record, short-text and authored values for the release read, the verdict parsers' listed cells (sanitized), N7 drops, claims not verified. It prints no text as read and writes nothing |
| `showcase review` (§7.3) | Each record-prose text once, in table and key order, with its place (an SD entry's id) and how many more places hold it. It doesn't resolve the claims |

## 27. Changed at card:A-004 (2026-10-25)

The operator ran the archive's one metadata pass (act card A-004, `done`; their `456aba6`: the transcripts' metadata,
the tooling epic's by name only). The row amends §19's; the rest stands as written there.

| Point (amends) | As built |
|---|---|
| The inventory's cache (§19) | `build()` reads only `py/showcase/cache/archive_metadata.json` (`cache=CACHE`, no archive branch): a missing or stale file fails, and only `--build-cache` scans the archive, so `--check`, `--write` and `--excerpts` don't open it either. An audit hook in the showcase tests' `conftest.py` refuses any open, `scandir` or `listdir` under the private archive with a `RuntimeError` (pathlib's glob swallows a `PermissionError`), so a `CHECK_CMD` run that would open the archive fails, and a test checks that the hook is live; the cache reproduces the committed block. A change to the cut-off, the anchors or the tally rules makes the cache stale, and its rebuild is the operator's (D2′; SD-SC-22 point 4) |

## 28. Built at E9.P3.1 (2026-10-26)

§12's last three tables and the points Gate E9-G2 and A-007 routed here (SD-SC-37). Each row amends the section it
names; the rest stands as written. Their four input labels are the operator's to add (act card A-008), so the export
runs them from that card's apply item on.

| Point (amends) | As built |
|---|---|
| `gate_events` (§12, §17) | The curated `gate_events.yaml`: one row per operator sign-off at a numbered gate of E3–E7 (7 gates, 12 sign-offs; E4-G2 six times, three of them holds), key (gate, sign_off). Columns gate, sign_off, epic, date, commit, option (the letter, as recorded), outcome (`proceed`, `hold`, `close`), reading (short text) and source (a label). §17's validator checks the commit and its day; the reading must appear verbatim in its source doc, bold dropped, so it is always the record's quote (V9); §12's "verdict" is that quote. Every close-out gate row the parsers find needs a row |
| `leak_autopsy_stage1` (§12) | E4.P6.8's stage 1 by E4's `paired_cells`: dash, sui × the calendar panel's four windows × substrate, with test Sharpe, trades, EV, `paired_strict` and the window's span. Reproduces its reading; the eval is pinned (`config.PINNED`) |
| `leak_autopsy_p7` (§12) | E4.P7's panel A by its `paired_cells`: the dev quartet × folds 0–3 × four arms (`frozen_as_built`, `frozen_causal`, `retuned_causal`, `reference`), test Sharpe and trades; span null (per-coin folds). Reproduces its reading; its eval and the E4.G2r record are pinned |
| The claims' engine (§25) | `pragma case_sensitive_like = on`: SQLite's `LIKE` matches case, as DuckDB's does (G2 dossier V4) |
| Release mode (§7.3, §26) | A release needs a review record for every short-text and authored value too (`bundle.READ`; the claims' included), written by `showcase review --short`; a withheld one crosses as `‹withheld›`. The manifest adds `unreviewed_short` and `records_on_proposal` (every record resting on a proposal, policy §5's count) |
| A withheld value (§26) | `TableSpec.withheld_rows = (column, value, columns)`: on those rows the writer publishes the columns as `‹withheld›`, whatever the store holds (a null stays null). `guard_cases` withholds the framework rows' command, cwd, rule and message this way (rule zero over N10) |
| YAML inputs (§2, §17) | Every YAML file the exporter reads (the private config, the claims, the epic cards, the curated lists, the paraphrases) fails on a repeated key at any depth (`sources/yamlio.py`) |
