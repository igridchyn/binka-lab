You are continuing the autonomous execution of **E9's lab lane, Binka Lab (`docs/E9_2026-10-15.md`)** in `~/dev/binka-lab`. Work the **single next open item to completion in this session, then stop** — a fresh session is opened for each item.

**First action: invoke the `autorun:item` skill** (`/autorun:item`). It carries the per-item sequence, the control-signal contract and the state-file roles, and tells you to read `.autorun/POLICY.md` (this repo's boundaries, guardrails and conventions). Then read, in order:

1. `.autorun/state/CURRENT_TASK.md` — resume state and the last checkpoint (may not exist yet on the first item).
2. The CURRENT ITEM block below — what this session's item is.
3. The plan documents it names.

`.autorun/LEDGER.md` is the one-line-per-item history. **Do not read it as part of an item** — `git log` has the detail if you need it.

<!-- ===== CURRENT ITEM — step 11 replaces ONLY this block; change nothing else in this file ===== -->
<!-- kind: impl -->
<!-- item: E9.P2.1 -->
**E9.P2.1 — Scaffold and tokens: Astro 5, React, TS strict, Fontsource; tokens.css, check-tokens, check-palette; npm run check with the vendored scanner (P2 §10 step 2)** · lane **review**
- Plan: `autorun-plan show E9.P2.1` (docs/E9_2026-10-15.md).
- **Hand-off notes (E9.P2.0's setup).**
  - This is the repo's first item. The spec is `docs/SHOWCASE_P2_design.md` (§2 stack, §3 layout, §4.1 tokens, §10
    step 2); E9 §3 gives `npm run check` its parts (tsc, eslint, vitest, the content build, Playwright and axe).
  - `npm run check` must run `python3 tools/scan.py` over `content/`, `docs/` and `src/`: CHECK_CMD runs it over
    `content/` and `docs/` only, and hands the rest to `npm run check` once `package.json` exists (POLICY).
  - `data/bundle/v1/` holds binka's staged bundle, uncommitted. E9.P2.2 commits it after `verify-bundle` and the
    scanner; leave it out of this item's commits.
<!-- ===== END CURRENT ITEM ===== -->

Begin with the skill, then the reads, then the current item.
