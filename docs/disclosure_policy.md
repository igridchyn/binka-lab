# Disclosure policy: what may leave binka for Binka Lab

**Status: SIGNED 2026-10-24 (act card A-003), the text at `3f6f268`; §5 amended (SD-SC-35) and signed again
2026-10-25 (act card A-007), the text at `aed9638`.** The agent drafted it on 2026-10-16
(E9.P0.2) from [P0 §5](SHOWCASE_P0_design.md) as amended (P0 §11, §12, §18), with SD-SC-05…13 in
[the scope log](SHOWCASE_scope_decisions.md). Gate E9-G1 sent it back for its dossier's §7 (SD-SC-21), and E9.P0.8
revised it (SD-SC-22; [the repeat's dossier](E9_P0.8_dossier_2026-10-16.md)). It is written in binka and moves to
binka-lab as `docs/disclosure_policy.md` at E9.P2.0, where it is public. So it follows its own rules.

**Rule zero.** Nothing crosses from binka to anything public unless a rule below allows it. If two of its rules
disagree, the stricter one holds until I decide, and the disagreement gets an SD-SC entry. Where this policy and a
design doc differ, this policy holds (P0 §5).

**Only my own act signs this policy, changes it, carves anything out of it or takes one of its reviews** (§5–§7). An
answer that the loop's decider gives in my place never counts as one of these.

---

## 1. What crosses, and where

| Crossing | What crosses | How |
|---|---|---|
| **The bundle** | Tables, texts and the manifest the exporter writes | The exporter (`py/showcase/` in binka) is the only code that reads binka's files for the site (P1 §2). binka-lab commits the bundle after `verify-bundle` and the scanner (E9 §3) |
| **The E9.P2.0 move** | The planning docs in this folder | Redacted copies (§4.8) |
| **Text written in binka-lab** | Copy, the `content/` files, the README, OG text, captions, and the repo's own history: its commit messages and author metadata | Lab sessions never read binka (E9 §3); §4.9 |
| **Text about the project elsewhere** | igor-web's `/algo` link and CV entry, LinkedIn, the video, the one-pager (P6) | The agent drafts it and I publish it (boundary (g)). The deny list applies, and I read each piece before I publish it (§5) |

Nothing else crosses. binka-lab starts with none of binka's git history (P3 §11.3 row 8). The exporter's code stays
private, except the scanner `scan.py`, which is vendored into binka-lab's CI (P1 §11).

## 2. Tiers

| Tier | Meaning | Examples |
|---|---|---|
| **public** | May appear verbatim, after the review its source needs (§4, §5) | Methods; verdicts and their deciding numbers; research prose from plans, dossiers and SD entries; code excerpts from binka's research code; commit SHAs and subjects; aggregate metrics |
| **aggregate** | Only as summaries or charts the exporter computes, never a row of the source | Per-coin and per-fold metrics; backtest trade counts; EV distributions; feature importances; MLflow run counts and metric summaries; API-equivalent cost per item; counts and latencies from the loop's logs |
| **never** | Not in the bundle, the public repo or anything published, in any form or transform | §3 |

- **Every bundle table is public in full.** The `/about/data` console opens any table row by row (P2). "Aggregate"
  describes how a table is built, not who can see it. So no table has a timestamp finer than a day (P1 §4, the
  raw-row guard), unless its spec declares an exception with a reason. An exception is one of three kinds:
  - the record's own event times (a commit, a log line, a card), where the time is the point, as in IV.17;
  - the feed snapshot's newest timestamps, which are metadata (N3);
  - a synthetic or model-output series.

  A market or third-party series never gets one (N4).
- No table can declare tier `never` (P1 §4). A `never` source has no exporter.

## 3. The deny list ("never")

Each row names the layers that enforce it (P1 §7):
- **structural:** the allow/deny roots and the strict table specs (P1 §2, §4);
- **sanitizer:** the text transforms (P1 §7.2);
- **tokens:** the private token lists, which the writer rejects on decoded values and which every other crossing
  checks too: the move (§4.8) and binka-lab's history (§4.9). This policy doesn't list the tokens, because the
  lists would describe what they hide (P1 §2);
- **scanner:** P1 §7.3, reading decoded string values (SD-SC-11);
- **review:** the human reads in §5.

Prose can't be pattern-matched, so the rows marked "review only" rest on a human read. I'd rather say so than imply
that the scanner covers them. A layer whose private input is missing or empty (a token list, the digest file, the
review store) fails the export; it never passes by default (P1 §7.3).

### N1 — Credentials and secrets
- `py/.env` and every value in it, the MLflow credentials, exchange API keys, the notification endpoints, cloud
  storage keys, and any token-shaped string.
- **Enforced by:**
  - structural: `py/.env` is a denied root;
  - sanitizer: notification URLs become `‹notify›`;
  - scanner: key and token patterns, and entropy. On the binka side it also checks the bundle against salted
    digests of each secret value and its encodings, which I write in my own terminal, so that no session holds a
    value. A match or a missing digest file stops the export (P1 §7.3), and I rewrite the file after rotating a
    secret;
  - the vendored scanner runs again in binka-lab's CI, with the patterns only.

### N2 — Accounts, infrastructure and security posture
- **Accounts:** exchange account and order IDs, balances, and account attributes such as a fee tier or VIP level. No
  file pulled from an exchange account is an exporter input.
  - **The one carve-out (signed with this policy; SD-SC-22):** the fee rates per side, in bps, on E4's frozen cost
    card cross as research inputs, because II.7's cost model must stay open to inspection. Read against the
    exchange's public fee schedule, they imply an account attribute; I accept that. Nothing else about the account
    crosses with them: the claims and the copy call them "the fee per side" and name no tier, discount or account.
    The card is pre-seal record (N5 rule 4).
- **Infrastructure:**
  - IP addresses, any hostname that isn't a public DNS name, and SSH config;
  - which machine runs what: the live box's provider, plan, region and hostname, and what else runs on it;
  - a public DNS name of my own, for a service or an endpoint I run, other than the two public sites (this one and
    my website), since next to what runs where it can tie a service to a machine.
- **Security posture:** how a private service or account is secured (auth arrangements, key restrictions, ports).
- The dev box's hardware (RAM, GPU, driver versions) is public. Its hostname, user and addresses are not.
- **Enforced by:**
  - structural: `~/.ssh` is denied, and so is every file pulled from an exchange account;
  - sanitizer: IP addresses and hostnames become `‹host›`. A closed allow-list keeps third-party hosts (exchanges,
    data vendors, documentation sites) and the hosts of the two public sites, this one and my website. Every other
    name under my domains becomes `‹host›` too;
  - tokens: the live box's identifying tokens;
  - review: account attributes, posture and what runs where, in prose.

### N3 — The live system: configuration, deployment, state and outcomes
- **Configuration:** the live model configs (`models/configs/*trade*.json`): thresholds and position sizing. Also the
  live models, and MLflow artifacts of any kind. The coins it scored are public: the feed published them, and I.6
  shows them.
- **Deployment:** the processes, schedules and hosts of the live box.
- **State, now or at any past date:** whether it trades, whether its feed is alive, and its outages.
  - The one exception is I.6's dated feed snapshot, which shows each coin's name and its newest timestamp and nothing
    else (SD-SC-12, §4.7).
  - The feed's values stay out unless I carve them out (§7).
- **Outcomes:** any figure from the live account: P&L, balance, positions, fills, trade counts or returns.
  - The one statement about the live outcome is `C-live-status`, the wording I ratified at E9-G0 (Q6; SD-SC-07):
    > *"It ran live on Binance: it scored coins every second and placed real orders when a prediction cleared its
    > threshold. It never made money. Act II shows why."*
  - Nothing claims profit or performance for the live bot, as on igor-web's `/algo`.
- **Public:** the live path's architecture (its components and how data flows between them), and the research data's
  own gaps and outages, which are method (I.1).
- **Enforced by:**
  - structural: `models/configs/` is denied. The export never calls the live box, the feed or MLflow; only the
    snapshot commands do (§4.7);
  - claims: `C-live-status` is `recorded`, so its wording is checked at every export (P1 §6);
  - review.

### N4 — Third-party data and access
- **Data:** rows or series from exchange and vendor data: Binance klines, trades and funding prints, the vendor's
  secondwise dumps, Deribit chains and E6's Deribit trade tape, Tardis samples, and recorder output. A dated value (a
  timestamp with its price, rate or volatility) counts as a row. Redistribution terms are unclear, so only derived
  aggregates cross. An undated level or move quoted in prose ("a 3 % move") is fine.
- **Access:** how data was fetched from a provider, beyond naming the source.
- **Enforced by:**
  - structural: P1 §2's raw-data roots are denied, and every table spec carries the raw-row guard and a `max_rows`
    cap;
  - review: a dated value inside prose.

### N5 — Sealed-window content
The seals are E5's two windows, INTERIOR (2025-10-01 → 2025-12-31) and FUTURE (from 2026-07-01), which E6 inherited
unchanged, and E7's holdout files. No gate has read any of them, and the contacts on record are disclosed (rule 3).
1. The sealed trees `py/test_data/e5_sealed/`, `e6_sealed/` and `e7_sealed/` are never opened.
2. Nothing new is computed for the site from market data (prices, features, labels, feed points) dated inside a
   sealed window. A precompute over market data applies the seal (`strip_sealed`, `ml/e5_seal.py`) before it
   computes anything. Recorded results are not market data (rule 4). The feed snapshot is the one exception, and
   it keeps metadata only: coin names and newest timestamps, never a value (N3; SD-SC-12).
3. Apart from rule 4's results, a value in the record that is dated inside a sealed window is not republished. That
   covers a value a disclosed contact quotes, and a public fact (a fee schedule, a listing) dated inside the window.
   The contact itself is public: its date, its metadata (row counts, file sizes, which months exist) and what was
   done about it. The seals' record, contacts included, is part of the story (IV.17).
4. A result the record holds from before E5 declared its seal (ratified 2026-08-12) is the record, not sealed
   content: a seal governs reads from its declaration on. It crosses with its window labelled. Examples are E4's
   calendar panel, its forward replay, SD-E4-24's correlation slice, and its frozen cost card: the fee rates, and the
   spread summaries, whose window runs from 2025-01-01 to the card's freeze and so overlaps both of E5's windows.
5. E7's holdout *window* (from 2025-01-01) isn't denied as a window. Outside E5's windows its months were dev data
   for E5 and E6, whose results cross as usual (E7 close-out §1 point 5). Only E7's holdout files, and values
   computed from them, are sealed.
- **Enforced by:**
  - structural: the sealed trees are denied roots, and the seal is applied once, in the exporter's readers of market
    data, so every precompute inherits it (P1 §2);
  - review: rule 3's values sit in prose.

### N6 — Personal data
- Email addresses (mine only if I add it to the allow-list). binka-lab's commits carry only the author name and
  email I choose to publish, and I check them before its first commit (§4.9).
- Names of people other than me. Authors cited for a method are fine. People who helped (testers, reviewers) are
  named only with their consent.
- Absolute home paths: they become `~/…`, and repo paths become repo-relative.
- My private life beyond what I publish myself: where I live, family, health, and my career plans.
- **Enforced by:**
  - sanitizer: paths and emails;
  - scanner: binka's history scan (§4.9) checks every author, committer and co-author identity in binka-lab's
    history against the ones I publish;
  - review.

### N7 — My own finances
- My holdings, capital and balances, and which brokers, banks or exchanges I hold accounts with.
  - Binance is public, as the live system's venue.
  - A venue named as a data source or a modelled vehicle is research, not my account.
- My tax residence, tax regime and personal tax situation. No tax rate crosses, and no figure after an assumed tax:
  a regime's own rates, allowances and rules identify it as surely as its name. Research may say that it assumed a
  tax, as a labelled assumption that names no jurisdiction.
- Research sizes in dollars or euros are notional, and the site says so wherever they appear.
- **Enforced by:** review only.

### N8 — The private tooling epic
- One epic is **a private tooling epic over personal data**. Everything that belongs to it stays out: its docs, code,
  tests, data and records.
- The exporter cuts it once, at its source layer, using rows kept in the exporter's private config (P1 §2). This
  policy doesn't list those rows, because the list would describe the epic.
- The site describes it in one place: IV.19's line *"one tooling epic, not shown: personal data"*, with its item
  count. Elsewhere it is referred to, never described:
  - another record that mentions it reads "a tooling epic, not shown";
  - (f)'s card gives no PAUSE count, because its PAUSEs belong to that epic;
  - boundary text and config values that name it are described, never quoted (SD-SC-09).

  Nothing else on the site counts it, or says what it had or did.
- **Enforced by:**
  - structural: the source-layer cut, which is tested once (P1 §2);
  - tokens: the epic's tokens;
  - sanitizer: a surviving mention becomes "a tooling epic, not shown";
  - review: the boundary review (§4.5).

### N9 — Raw transcripts and the loop's private files
- **Transcripts never cross raw.** That covers the private archive I made on 2026-10-15, and the per-item session
  logs in `.autorun/state/logs/`: every file there except `supervisor.log` and `costs.jsonl`.
  - Apart from the interim re-read below, the loop reads the archive only to extract excerpts for my review, as
    POLICY (g) says.
  - The agentic inventory's counts come from one pass over the archive that I run myself. It reads the transcripts
    only to derive metadata (timestamps, session ids, tallies of the epic ids a session names, and where a replay's
    anchors appear), prints none of their text, and pins the derived values in a cache (E9.P1.2). Until that cache
    exists, the inventory's test repeats the pass on each run, as it has since E9.P0.3; after it, no test or export
    opens the archive.
  - The exporter never opens the archive or the session logs (P1 §2).
  - Only curated excerpts cross, through the excerpt review (§4.6).
- **The loop's private working files are never a source:** resume notes, item plans, lessons, the verifier's and the
  skeptic's files, and card bodies, which hold my answers. What the record says about them is public, because it is
  how the loop works, which Act IV shows. Examples: a commit that names an item plan, an SD entry that paraphrases a
  skeptic's finding, or my decision as recorded in a plan.
- **Session IDs** are identifiers, so they become `‹session›`.
- **Enforced by:**
  - structural: the archive is outside the allow-list. `.autorun/state/` is denied, apart from the two logs, which
    are allowed by name. Card bodies are never read (P1 §2, §5.1);
  - the excerpt review (P1 §7.3);
  - sanitizer: session IDs (added at E9.P1.3; SD-SC-13).

### N10 — The private plugin's code
- While the plugin is private (SD-SC-05), no code, hook or skill text from its repo crosses, and no link to it.
  IV.21 explains it in diagrams and prose, and its claims resolve privately. Prose from its design document (section
  names, short quotes) crosses only through the excerpt review.
- The guard cases are output, not code. Each is the real decision, rule and message from running the hook over
  binka's rules (P1 §5.1), and it crosses after the excerpt review (P3 §9).
- The loop's own files in binka (POLICY, `config.env`, the guard rules, the backlog, the prompt and the ledger)
  belong to binka. Their free text touches other rows (N3, N8 and this one). A passage of it is record prose (§4):
  it crosses through the excerpt review, and the boundaries through their own review (§4.5). A one-line value of at
  most 120 characters from them (a ledger cell, a task title) is short text, which the release read covers value by
  value (§5).
- **Enforced by:**
  - structural: the exporter reads the plugin's files only for claims, the guard cases and reviewed excerpts (P1 §2);
  - the excerpt review;
  - the release read.

## 4. Rules by source

**Free text from the record needs a review.** A table spec declares each string column as one of four classes
(P1 §4):
- structured (ids, dates, enums, numbers, verdict words), which needs nothing beyond the spec;
- short text: one line of at most 120 characters (a commit subject, a verdict cell), which the release read covers
  (§5). The writer treats a longer value, such as most ledger rows, as record prose;
- authored (the `content/` files: copy, epic cards, replay narration), which is written for publication, so the
  release read covers it (rule 9);
- record prose (an SD body, a passage from a plan, a dossier or one of the loop's own files, a log message, a commit
  body, transcript text). This crosses only with a review record: the SD review (rule 2), the boundary review
  (rule 5) or the excerpt review (rule 6). In release mode the writer fails a record-prose value that has no record.

The manifest's strings take the same classes. Its ids, digests, dates and versions are structured, and it names each
input by a label from the exporter's private config, never by its path, since a path can name something §3 denies
(P1 §3.1).

1. **Commit SHAs** are public: they prove provenance without exposing content, since binka stays private.
2. **SD entries.** Every SD entry body has a review record with one disposition: publish, publish redacted, or
   withhold. The record holds the sha256 of the source text and of the text as published (its title, body and
   cross-references), so a change to either the entry or its redactions fails the export until it is reviewed
   again. A withheld entry appears as its id only, marked withheld, with no title, body or reason. The exporter
   applies the redactions from its private config, because a list of redacted phrases would itself disclose them.
   This replaces the exemption in P1 §5.1 and §7.3 (SD-SC-13): the sweep behind this policy found entries that no
   automated transform can clear.
3. **Commit messages.** A subject is short text: it crosses after the token checks, the sanitizer and the scanner.
   E9.P1.5's sweep reads every subject against §3 and proposes a disposition for each one it flags: redact it, or
   withhold it and keep the SHA. I confirm them in the SD review. A subject over 120 characters is record prose, and
   anything beyond the subject line is an excerpt (rule 6).
4. **The loop's logs.** From `supervisor.log` and `costs.jsonl` the exporter takes structured fields only: dates,
   items, boundary letters, costs and counts. Free text from a log line, such as a PAUSE reason or a NOTIFY message,
   is an excerpt (rule 6). This replaces P1 §5.1's "reason (redacted)" in `autorun_pauses` (SD-SC-13). The same
   holds for a ledger ⏸ row: `autorun_pauses` takes its letter, date and item, not its text.
5. **Boundaries.** `text/boundaries.json` carries POLICY's boundaries as of the export. Each one is reviewed, as
   verbatim or as a paraphrase, against the sha256 of POLICY's exact text, and a boundary whose current hash has no
   record fails the export (P1 §5.1). (e) is paraphrased without its note on the live box. (f) reads only: *"The
   operator's personal data: a session never reads it, and nothing derived from it is committed"* (SD-SC-09;
   SD-SC-13).
6. **Excerpts: transcripts, code, commit bodies, log lines, and passages of the loop's own files.** Each excerpt is
   curated (a transcript's as tool call → result → decision), redacted, and read by me, or accepted on its proposal
   (§5), before it enters the bundle.
   Its review record is keyed by its sha256, so a changed excerpt needs review again (P1 §7.3). Until I approve an
   excerpt, it exists only in binka's private review batch, and no planning doc quotes it. Code excerpts come from
   binka's research code and tests, never from the plugin (N10) or the exporter.
7. **The snapshots.** The feed snapshot (I.6; N3) and the MLflow snapshot are pinned files, each written by its own
   `showcase snapshot` command. The commands sit in the exporter's package, but the export never runs them and never
   calls the feed or MLflow (P4 §8). Each is run deliberately, once per snapshot, and the scanner reads its file
   before the export uses it. The MLflow snapshot needs my credentials, so I run it. It holds aggregates and tag keys
   only: never tag values, artifacts or models.
8. **The E9.P2.0 move.** A redacted copy of each doc moves, and the original stays in binka. The loop prepares the
   copies. First the token checks run over the raw docs and list every passage that names what a list hides, for
   handling by hand with the passages SD-SC-13 points to. Then the sanitizer's transforms and the scanner run over
   the copies. I read the prepared copies in full (§5). A doc that can't be redacted without losing its sense stays
   in binka, and binka-lab gets a pointer.
9. **Text written in binka-lab** follows the deny list exactly as exported text does, and the release read covers
   it. The vendored scanner runs over it in the lab loop's check before each push, and again in CI. A push to a
   public repo is publication, so binka-lab's history crosses too:
   - before its first commit, I check the author name and email its commits will carry (N6);
   - a public repo shows more than its commits: its pull requests and their comments, its CI logs, and any commit it
     still serves by hash. So the public repo starts fresh at launch: binka's scan, with the token lists and the
     secret digests, runs over the commits to be published (trees, messages and author metadata), I push only those
     to a new public repo, and binka-lab stays private as the lab loop's working repo (P3 §11.4);
   - after launch, the lab loop's work stays in binka-lab until its release read, and I move each release to the
     public repo myself, after the same scan over the release's commits.

The live system, research sizes and sealed data follow their rows directly: N3, N7 and N5.

## 5. Reviews: who reads what, and when

**Every review here is mine alone** (the rule above §1). Where a review leaves records in the exporter's store
(excerpts, boundaries, SD dispositions, short-text values), only `showcase review` writes them, which I run in my own
terminal and which refuses to run inside a loop session. I run it between loop items and commit what it writes. The
store sits in binka, and the loop's gate protects it, so no loop item writes or edits a record (P1 §7.3). The other reads (the pages, the move, a piece published elsewhere)
are recorded by my own answer on the card that asks for them. Which card asks for each review is the plan's business
(E9 §4); a card the decider answers never stands in for one.

**Accepting a proposal instead of reading.** Where the loop has proposed a disposition for a value, by reference, in
a private proposals doc (E9.P1.5's: `E9_P1.5_review_proposals_2026-10-17.md`), I may accept the proposal without
reading the value as published. Accepting is my own act, like the review it replaces:
- I name the proposals doc and the commit I accept it at in a card answer, and `showcase review --by-proposal`,
  run in my own terminal under the same refusals, writes the records. Each one is marked as resting on that
  proposal, so it never reads as a read;
- it covers only a proposal of publish, publish redacted (with the cuts in the private config at that commit) or
  withhold, for the SD review, the boundary review and the excerpt review. A proposal that says to read first, a
  value with no proposal, and a value whose text changed after the proposals' commit are read as before;
- it doesn't touch the release read, the read before publishing or the move read: I still read every page before
  anything is public, SD pages and guard cases included;
- the bundle's manifest counts the records that rest on a proposal, and the site's method section says how many and
  what accepting a proposal means.

| Review | What it covers | When |
|---|---|---|
| **Excerpt review** | Transcript, code, commit-body and log excerpts, passages of the loop's own files, other record prose (§4), and the guard cases | Batched per release train (E9 §4) |
| **SD review** | Every SD entry body, as published, and the commit subjects the sweep flags (§4.3). The loop proposes the dispositions (E9.P1.5), and I read each published text or accept its proposal (above) | At Gate E9-G2 (E9.P1.8) |
| **Boundary review** | A boundary whose hash has no record | When the export fails on it |
| **Release read** | Every page in both themes against §3, especially the guard cases, SD pages and commit-message quotes, at v0.1 (P3 §11.3 row 3), then what each release adds or changes (P4 §11 item 4). It includes the short-text values with no record yet, which the review report lists, since the console shows every row | At every release, before it is public (§4.9) |
| **Read before publishing** | Each piece published elsewhere (§1): the video's script and captions, the LinkedIn post, the CV entry and igor-web's change | Before I publish each one |
| **Move read** | The prepared copies of the docs that move at E9.P2.0 (§4.8) | Once |

Text whose review record is unchanged isn't read again.

A review record means "read against this policy as signed", and a record that rests on a proposal means "accepted,
unread, on that proposal". After a change to the policy, a record still stands for
anything the change didn't touch (§6).

## 6. Changes and incidents

- After I sign, any change to this policy goes through an SD-SC entry and needs my signature again (the rule above
  §1). A new or widened `never` row means re-checking the scanner's rules, and every review record the row touches,
  over the bundle and the public repo.
- If denied content is found after publication, it comes down first: I revert and redeploy (boundary (g)), and I
  rotate a leaked secret. Then the finding is recorded with its cause and the rule that should have caught it.
- A revert doesn't take content out of a public repo's history, and copies may already exist. So a leak that reached
  binka-lab's history also needs that history rewritten and force-pushed, which is mine to do (boundary (g)). That is
  why §4.9's scans run before the fact.

## 7. Sign-off

I sign this policy at the G1 repeat (E9.P0.8), on act card A-003. Signing also confirms or overrules the calls the
agent made:
- SD-SC-09: boundaries (e) and (f) as paraphrases;
- SD-SC-12: the feed snapshot without values;
- SD-SC-13: the rules this policy adds to its spec;
- SD-SC-22: the revision's rules, N2's carve-out for the fee rates among them.

After that, P1 implements §3 and §4 as code in binka's exporter. Only the scanner's generic patterns are vendored
into binka-lab's CI. The token lists, the redactions, the secret digests and the review records stay in binka
(P0 §5.4).

- [x] Signed (date, initials, card, and the commit whose text I sign): 2026-10-25, IG, A-007, aed9638

A signature covers the text at that commit. If the file later differs from it anywhere outside these sign-off lines,
the export fails until I sign again (§6; P1 §7.3).
- Carve-outs: N2's fee rates, written into the text (SD-SC-22). Others, if any (each gets an SD-SC entry): ______
- Gate E9-G1, 2026-10-16: **rework**, decided by autorun (autonomous mode), so no signature. The policy went back for
  the G1 dossier's §7 (SD-SC-21), and E9.P0.8 revised it (SD-SC-22).
- Gate E9-G1, the repeat, 2026-10-24: **signed** on act card A-003, the text at `3f6f268`. D1a–D1d (the fee term as
  option (A), with N2's carve-out), C6, D2′, SD-SC-21's points 3–5 and SD-SC-22 are confirmed. The decider takes none
  of §5's reviews.
- Gate E9-G2, 2026-10-25: §5 amended to let me accept a proposal instead of reading (SD-SC-35). **Signed** on act card
  A-007, the text at `aed9638`.
