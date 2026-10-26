# Agentic inventory: what the loop's records hold (2026-10-16)

**Status: DRAFT for review at Gate E9-G1 (E9.P0.7).** The agent wrote it at E9.P0.3 from
[P0 §6](SHOWCASE_P0_design.md); the decision record is SD-SC-14 in the scope log.
It moves to binka-lab as `docs/agentic_inventory.md` at E9.P2.0, where it is public, so it follows
[the disclosure policy](disclosure_policy.md):
- counts only, and no transcript text (N9);
- the private tooling epic is out of every count (N8). IV.19's one count of it comes from the exporter (P1 §2), not
  from here;
- session ids appear as `‹session›`. The per-candidate list with sessions and lines is private (§5).

**Reproduce.** Every number in §2 comes from binka's `py/util/agentic_inventory.py`, pinned to a cut-off (git at
E9.P0.2's close-out, the logs up to E9.P0.3's launch), so it reproduces as long as the logs stay append-only:

```bash
cd py && pipenv run python util/agentic_inventory.py --check   # exit 0: §2 reproduces
cd py && pipenv run python util/agentic_inventory.py --write   # rewrite §2 after moving the cut-off
```

The prose in §1, §4 and §6 cites §2's tables and adds no count of its own, except dates and commit SHAs.

---

## 1. What the record holds

1. **Complete:** git, the SD logs and the ledger. **The ledger starts at E4**, not at E3 as P0 §6 said. Its first
   row is E4's ratification on 2026-07-30. The file was created on 2026-09-27 from the superseded entries of the task
   prompt, which began at E4. E0–E3's items are in git and their plan docs only (G2).
2. **The supervisor log is partial.** After the session that ended on 2026-08-03 at 00:10, none was launched until
   2026-09-27 (G4). E4's items except E4.P6.1, and E5 up to and including Gate E5-G1, ran outside the supervisor.
   From E4.P6.2 to E4.P7 the commit bodies record my sign-offs as given in the session, so those were interactive.
   For E4.P1–P4 and for E5 the record doesn't say. So per-item cost is known for nearly every row from E6 on, and
   for few of E4's and E5's (G3). Before 2026-10-05 there is no `costs.jsonl`, and a session's item can only be
   matched through its commit.
3. **Commit messages hold no session cost.** Their `$0` lines record vendor spend, and NOTIFY lines only repeat a
   run's cumulative cost line. So P0 §6 task (1)'s fallback recovers nothing. P1's `cost_source` is `log` or `unknown` in practice.
4. **The session logs come in two formats.** Up to 2026-10-11 each `.json` file is one result record: the session's
   final message and its usage, not a transcript. Stream transcripts (`.jsonl`) start on 2026-10-12. This corrects
   P0.1's note that every `item_*` file is a stream transcript. Both formats hold the agent's own text, so N9 covers
   both, and the exporter opens neither.
5. **The transcript archive** begins 2026-09-27. It holds headless and interactive sessions (G1). P0 §6's earlier
   count included the tooling epic's sessions; G1's doesn't.
6. **R1's discovery was interactive** (P0 §6.1's open question; STATUS carried item 4):
   - SD-E4-24 first appears in `b04193d` (2026-08-03 16:57), the E4.P6.6a prep commit.
   - It falls between two sign-offs that the commits record as given in the session the same day: `e87d615`
     (15:59) and `097ac5e` (23:07).
   - No supervisor session was launched between 2026-08-03 00:10 and 2026-09-27.

   So the site says the leak was found in an interactive Claude Code session, with me present.

## 2. Counts

<!-- BEGIN GENERATED: util/agentic_inventory.py -->
Cut-off: git `6b66f0f`; logs up to 2026-10-16 (the launch of E9.P0.3, which is left out). Every count leaves out the private tooling epic (N8).

### G1. The sources

| Source | Span | Count |
|---|---|---|
| git (binka, the loop branch) | 2021-04-07 → 2026-10-16 | 806 commits; 404 since 2026-05-01; 272 carry a Claude co-author trailer |
| Ledger | 2026-07-30 → 2026-10-16 | 67 rows |
| SD logs E3–E7 | — | 148 entries (29 · 35 · 32 · 25 · 27); the showcase log 13 |
| `supervisor.log` | 2026-07-24 → 2026-10-16 | 26 runs; 51 sessions (48 work, 3 repair); 48 with a cost line |
| `costs.jsonl` | 2026-10-05 → 2026-10-16 | 58 rows (39 sessions, 19 verifier runs) |
| Session logs, result records (`.json`) | 2026-07-24 → 2026-10-11 | 41 (2 empty) |
| Session logs, stream transcripts (`.jsonl`) | 2026-10-12 → 2026-10-16 | 10 |
| Transcript archive | 2026-09-27 → 2026-10-12 | 59 sessions (42 headless, 17 interactive) |

### G2. Commits and ledger rows by epic

| Epic | Commits naming it first | Ledger rows | ✓ | ✗ | ⛔ | ⏸ |
|---|---|---|---|---|---|---|
| E1 | 12 | 0 | 0 | 0 | 0 | 0 |
| E2 | 62 | 0 | 0 | 0 | 0 | 0 |
| E3 | 44 | 0 | 0 | 0 | 0 | 0 |
| E4 | 49 | 22 | 16 | 1 | 4 | 1 |
| E5 | 23 | 13 | 5 | 2 | 5 | 1 |
| E6 | 32 | 15 | 11 | 0 | 0 | 4 |
| E7 | 28 | 13 | 11 | 0 | 1 | 1 |
| E9 | 8 | 4 | 4 | 0 | 0 | 0 |
| none named | 548 | — | | | | |

Commits per year: 2021 167 · 2022 78 · 2024 65 · 2025 75 · 2026 421.

### G3. API-equivalent cost per ledger row

A session's cost goes to the ledger row whose commit it made. A session cut off before its commit goes to the next session on the same item. Nothing is estimated.

| Epic | Ledger rows | With a logged cost | Unknown | Logged cost |
|---|---|---|---|---|
| E4 | 22 | 1 | 21 | $33 |
| E5 | 13 | 3 | 10 | $11 |
| E6 | 15 | 14 | 1 | $230 |
| E7 | 13 | 12 | 1 | $177 |
| E9 | 4 | 2 | 2 | $69 |

Logged in all: $541 over 48 sessions, verifier runs included; $520 lands on 32 rows (median $13); $21 in 4 sessions lands on none. Commit messages record no session cost (their `$0` is vendor spend), so they recover nothing.

### G4. Loop events in `supervisor.log`

| Event | Count |
|---|---|
| item done | 23 |
| repaired | 3 |
| PAUSED | 9 |
| COMPLETE | 2 |
| STOPPED | 6 |
| waiting | 2 |
| halted | 2 |
| ERROR | 2 |
| repair decision | 3 |
| gate recovery | 1 |
| session ended rc ≠ 0 | 8 |
| session with no cost line | 3 |
| independent-verifier runs | 19, 19 with a verdict (0 BLOCKER, 3 MAJOR, 40 MINOR) |
| actions denied by permissions | 13 in 10 sessions |

Stretches of 14 days or more with no session launched: 2026-08-02 → 2026-09-27.

### G5. PAUSEs by boundary letter

| Letter | `NOTIFY … PAUSED` lines | Ledger ⏸ rows |
|---|---|---|
| d | 9 | 5 |
| — | 0 | 2 |

### G6. Case replays: spine and transcript coverage

| Replay | Spine ids found | In-episode transcripts | Lines | Sessions outside the window naming it |
|---|---|---|---|---|
| R1 | 4/4 | 0 | 0 | 5 |
| R2 | 1/1 | 2 | 2 | 3 |
| R3 | 5/5 | 0 | 0 | 4 |
| R4 | 4/4 | 6 | 31 | 4 |
| R5 | 3/3 | 10 | 89 | 7 |
| R6 | 3/3 | 11 | 98 | 2 |

<!-- END GENERATED -->

## 3. How the counts are made

- **The tooling epic.** An epic id is the first one named in a ledger item, a commit subject, a session's item text
  (`costs.jsonl`) or its NOTIFY lines (not the first supervisor's run label). A ledger row naming none (the gate
  re-decisions) takes the older row's. The sessions of one iteration (work, repair, resume) share its item. An
  interactive archive session takes the epic id its assistant lines name most. If a tenth or more of those ids are
  the tooling epic's, the session is mixed and is left out whole. Everything of the tooling epic is dropped, and
  this doc gives no count of it.
- **Cost (G3).** "Cost" is API-equivalent: the `total_cost_usd` Claude Code reports. The real cost was one flat
  subscription (P0 §4.2, `C-loop-cost`).
  - A session's cost goes to the ledger row whose commit it made inside its window, from launch to cost line, by
    committer date. A "(this commit)" row also takes the commit that added it to the ledger.
  - A session with no such commit (cut off by a usage limit, a repair, a resume after the gate) goes to the next
    session on the same item. Failing that, it goes to the previous one.
  - A verifier run goes to the session before it.
  - A resumed session reports the cost of the session it resumes again, on top of its own, so that cost is
    subtracted. The supervisor's own cumulative figures count it twice.
  - What is left lands on no row and is shown as such. Nothing is estimated.
- **Events (G4, G5).** NOTIFY lines are classed by their first words. A PAUSE's letter is the "(x)" after
  "boundary", "PAUSE" or a dash, in the NOTIFY line or the ledger reading; an "option (x)" is not a letter. A
  verifier run is counted from its start line. A legacy launch line names no session, so its archived transcript
  is matched by its start time (within two minutes). Only these structured fields are taken; the free text stays in binka (policy
  §4.4).
- **Transcripts.** They are read for metadata only: timestamps, session ids, and tallies of epic ids. A replay's
  anchors are its SHAs, SD ids and item ids. A line counts as an excerpt candidate only if it is the agent's own
  message (an assistant line or a result record) and names an anchor. "In-episode" means the line is dated inside the
  replay's window, in local (Vienna) dates like every date here. Nothing is quoted.
- **Not counted:** `usage.jsonl` (subscription readings; no exporter reads it), and the verifier's and skeptic's files
  and the item plans (N9).

## 4. Case replays

| Replay | Mode at the time | Spine (public) | In-episode transcript (G6) |
|---|---|---|---|
| R1 The look-ahead | Interactive (§1 point 6) | SD-E4-24 · `b04193d` → `88ec6dc` → `68c917e` · E4.P7 | None |
| R2 The gate pause | Headless: the supervisor's first day, 2026-07-24 | The run's `supervisor.log` lines (date, PAUSE letter) · `ccdeb9f` · the E3-G1 dossier | Two result records: the final messages of the item session and the gate session |
| R3 The lost GPU | Outside the supervisor (in the gap) | `ea4f96c` · `9344574` · `c3a3ce5` · SD-E4-29/30 | None |
| R4 The easy pass | Headless runs on 2026-09-28, between interactive sessions | SD-E5-30(c) · SD-E5-31 · `02b5c53` → `afa1f4f` | Headless and interactive sessions, in the archive |
| R5 A NO-READING held | Headless (E6.P2, 2026-10-09 → 10-11) | SD-E6-15, -22, -23 · the E6 card and G1 dossier | Headless sessions, mostly, in the archive |
| R6 A KILL accepted, its weak limb disclosed | Headless (E7.P2, 2026-10-11 → 10-12) | SD-E7-18, -25, -26 · the E7 card and G1 dossier | Headless sessions; the widest coverage of the six |

**Recommendation (the agent's call; I approve the replays at Gate E9-G1):**
- **R1, R2 and R4 for v0.x**, as P0 §6.1 recommended. R1 is the strongest rigor story and needs no transcript: its
  spine is the record. R2 is the governance story. R4's sessions are in the archive.
- **R5 as the fourth, for P4, in place of R3.** R5's sessions are in the archive. It shows a rule deciding the
  outcome (the coverage bar), and NO-READING ≠ KILL is a distinction III.12 is built on. R3's spine is commits and
  SD entries with no transcript, and IV.19's recovery counts (G4) carry its theme.
- **R3 and R6 stay in reserve.** R6 has the best coverage, but its story (a weak limb disclosed) overlaps R4's.

If I pick R5 or R6, they join P4 §6.1's table and IV.18's cards (P4 §6.1).

## 5. Excerpt candidates

G6 counts them per replay. The list itself, with each candidate's session, line range, anchors and file, is
private: `py/doc/planning/E9_inventory_excerpts_2026-10-16.md` stays in binka. A candidate is a pointer, not an
excerpt. An excerpt is curated from it at P4 (tool call → result → decision), redacted, and read by me before it
enters the bundle (policy §4.6). Until then no doc quotes it.

## 6. What changes downstream

- **P0 §6:** the source rows are corrected (ledger start, the session-log formats, the archive count, cost
  recovery); see P0 §13.
- **P1 §5.1 `autorun_items`:** `cost_source` is `log` or `unknown`. §3's attribution rule is the spec for
  `sources/autorun.py`, which may take over this script's parsers (P1 §15).
- **P4 IV.19:** the cost histogram has values for nearly every row from E6 on. Most of E4's and E5's are unknown
  and counted as such, not imputed (G3). The recovery
  counts start 2026-07-24 and miss the interactive stretch (G4), so they are flagged as partial.
- **P4 §6.1:** gains R5 if I approve it (§4).
