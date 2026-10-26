# binka-lab autorun policy

Read in full at step 0 of every autorun item (the `autorun:item` skill says so). The skill carries the generic
procedure; this file carries what is this repo's own, and **where the two disagree, this file wins.**

binka-lab is Binka Lab, the public showcase of a private research repo, binka (epic E9). It stays private until the
operator launches it; then a fresh public repo gets its scanned commits (disclosure policy §4.9). **Everything
written here is written for publication.**

## Plan documents and the decision log

- The plan is `docs/E9_2026-10-15.md`, its lab-lane entries. `.autorun/backlog.json` picks the item, and
  `autorun-plan show <id>` prints its entry. The phase designs `docs/SHOWCASE_P2_design.md` to `P6` are the specs.
  `docs/SHOWCASE_plan.md`, `P0`, `P1`, the policy and the inventory are binka's, copied here for reference.
- Decisions, scope shifts and recorded defects go in as a new entry in `docs/LAB_scope_decisions.md` (SD-LAB-nn).
  The designs cite binka's SD-SC-nn entries, which stay in binka; the design text states each decision.
- The disclosure policy, `docs/disclosure_policy.md`, binds every word written here (its §4 rule 9). It is the
  signed text, copied from binka, and frozen in this repo.
- Writing an item beyond the plan is a gate act, never a step-11 choice.

## Isolation: the one-way rule (E9 §3)

A session here **never reads ~/dev/binka**: no file, no git command, no path. Its only input from binka is the bundle
that binka's exporter writes, uncommitted, into `data/bundle/`. A lab item commits it after its own checks
(`verify-bundle` and the scanner). The guard and the loop's settings enforce this. If the site needs a number, a
claim or an excerpt the bundle lacks, open a card for binka's lane. Never reconstruct it here.

## Approval boundaries

Pause for explicit operator sign-off, as a card (backlog mode), on:

- **(a)** deleting data outside this repo;
- **(b)** multi-day jobs (none are planned);
- **(c)** any real-money spend. The stack is on free tiers (GitHub, Cloudflare Pages, Access and Web Analytics), and
  `$0` is the standing default;
- **(d)** gate decisions (Gates E9-G3 and E9-G4, every release checkpoint): build the dossier with a
  recommendation and open a blocking checkpoint card. **Do not advance past a gate;**
- **(e)** the live trading system and exchange accounts: this repo never touches them, and the site shows no live
  state (policy N3);
- **(f)** personal data: none is read, asked for or written here (policy N6, N7);
- **(g)** publication and accounts: creating or changing anything on GitHub (the repo, its visibility, settings or
  secrets), Cloudflare (Pages, Access, DNS, Web Analytics) or Search Console; merging to `main` or `production`;
  making a repo public or removing an Access policy; posting or uploading anywhere; contacting anyone. The loop
  prepares an `act`, `checkpoint` or `comms` card with the exact steps, and the operator does them. The supervisor
  pushes only `autorun/loop`, which deploys a preview behind Access.

A decision card's options and recommendation go in a new SD-LAB entry, with Status "provisional" until the answer is
applied. A checkpoint dossier goes in `docs/E9_<task>_dossier_<date>.md`.

## Hard stops (autonomous mode)

With `AUTONOMOUS=1` the decider answers decision and checkpoint cards in my place. It leaves me spend, accounts and
secrets. It also leaves me these:

- **The disclosure policy** (`docs/disclosure_policy.md`): signing it, any carve-out from it, and any change to it
  after it is signed.
- **The disclosure policy's reviews:** every review its §5 lists, as signed. Here that is every release's disclosure
  read, the excerpt review and each read before publishing.

A card that carries any of these is mine. A decider's answer on it is no signature and no review record: the item
that applies such an answer doesn't carry it out, and asks me on a new card instead.

## Quality gate (step 5) and re-design (step 11)

`/simplify`, then `/code-review high`, then `CHECK_CMD`, looped up to two rounds. A design signed off at a gate is
never re-designed autonomously: write an SD-LAB entry and open a card (boundary (d)).

Item kinds: `design`, `dossier` and `impl` (config.env routes them).

## Running jobs (step 7)

There are no heavy jobs. Builds and tests run in the foreground (`npm run check`), never in the background. The
scanner runs on the system `python3`, and needs `pyarrow` only for parquet:
`uv run --no-project --with pyarrow python tools/scan.py data/bundle`.

## Guardrails

**Enforced for you:** the guard blocks any shell command that names a path into ~/dev/binka. The loop's settings deny
reading it, reading any `.env`, pushing, ssh, curl, wget and the Cloudflare and GitHub command-line tools, and editing
the loop's own files, the disclosure policy and the vendored scanner (both also frozen). If a rule fires, it is right:
change the command, don't work around it.

**Yours to keep:**

- Every word follows the policy's deny list (§3). No absolute home path, no host but the two public sites and named
  third parties, no email address, no session id, no secret-shaped string. The plugin that runs this loop is "the
  plugin": never its repository's name, its design document's file name, its code, hooks or skill text (N10). The
  hidden epic is "a tooling epic, not shown", never described (N8). No live state, outcome or config (N3), and no
  personal data (N6, N7).
- Numbers come only from the bundle, through claims. No number in the copy that isn't bound to a claim (P2 §5.3).
- CHECK_CMD runs the vendored scanner (`tools/scan.py`) over `content/`, `docs/`, `src/` and the loop's ledger and
  prompt, so every push is scanned first (policy §4.9). `npm run check` scans any other text directory it adds.
- Transcript and code excerpts enter only through binka's exporter, after the operator's excerpt review.

## Conventions

- Stage only this session's files, by name. Never stage `data/bundle/` before its checks pass.
- English only (SD-SC-02). The copy is in the first person, the operator's voice.
