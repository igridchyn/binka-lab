# P6 design — Distribution: the assets, the human test, and the announcement (2026-10-15)

**Parent:** [SHOWCASE_plan.md](SHOWCASE_plan.md) §4. **Builds on:** v1.0 (P5). **Program wrapper:**
[E9](E9_2026-10-15.md) §5 P6. **Output:** the lab announced, with every asset that points at it published, and the
CV, LinkedIn and igor-web updated.

Until P6 the lab is a soft launch: linked, not announced. P6 decides when people are told, what they see first, and
what the operator carries into interviews. Nearly every P6 output is **published by the operator** (E9 boundary
(g)). The agent's part is producing assets that are ready to publish, and the checks behind them.

---

## 1. What ships, and who publishes it

| # | Asset | Where it lives | Agent produces | Operator does |
|---|---|---|---|---|
| 1 | The **human 60-second test** (blocking) | P6 summary | The tester ask, protocol and score sheet | Recruits 3 testers, runs the test, records answers |
| 2 | **README as a case study** | `binka-lab` GitHub | The full README | Reviews and merges |
| 3 | **3-minute walkthrough video** | YouTube (public), linked from the site | Script, shot list, clean screen captures, captions | Records the voice-over, does the final cut, uploads |
| 4 | **1-page PDF** | `lab.gridchyn.ai/binka-lab-one-pager.pdf` | The `/one-pager` route and its PDF build in CI | Reviews and attaches it to applications |
| 5 | **LinkedIn post** (and the Featured item) | the operator's LinkedIn | Two draft variants plus a first comment | Edits and posts |
| 6 | **Interview talk tracks** | **private**, in binka | The tracks | Rehearses them; they never go public |
| 7 | **CV and igor-web updates** | the CV, igor-web | Copy drafts and the igor-web change on a branch | Merges igor-web to `production`, updates the CV |
| 8 | The plugin's **README + demo GIF** | *Deferred* until the plugin is public (SD-SC-05) | — | Decides if and when the repo goes public |

## 2. The human 60-second test (SD-SC-04): blocking

v0.1 launched on a proxy test (three model readers). The human test is owed **before any announcement** (P3 §14.1).

- **Who:** 3 people outside the project, ideally one recruiter or HR person, one engineering manager and one ML
  engineer. Not people who have seen the site. A failed round needs **new** testers.
- **Ask (drafted by the agent, sent by the operator):** about 5 minutes of their time, a link, and two questions.
  The draft is ≤ 80 words, comes in an email and a DM variant, and doesn't describe the site (that would prime them).
- **Protocol** (P3 §11.1, unchanged): open `/` on their own device. After 60 s, close the tab, then answer *"What
  is this, in one sentence?"* and *"What's one thing that stood out about the author?"* The site must be the
  production URL, and no tour or lens is set in the link.
- **Pass:** 3/3 reproduce the spine's gist, and ≥ 2/3 name a differentiator (rigor or the leak, the agent operating
  model, pre-registration).
- **Record:** answers verbatim but anonymised (role only) in the P6 summary, scored against the bar, with the
  proxy test's result beside them, since the gap between the two is itself worth knowing.
- **On a fail:** the agent proposes a spine or tile change from the answers, the operator picks one, it ships, and
  the test is re-run with new people. The announcement waits.

## 3. README as a case study (`binka-lab/README.md`)

The GitHub README is the deep-link entry for Staff+ readers (P0 §2), so it carries the story on its own.

1. **One-paragraph summary:** the spine, then the link to the site and the 3-minute video.
2. **Three stories, 3–5 sentences each,** each with one claim and a deep link: the leakage autopsy, the gate pause,
   and the loop with its boundaries.
3. **"How to check my numbers":** the provenance chain, from chip → claim → bundle table → `/about/data`, and how to
   verify the bundle's hashes locally (`npm run verify-bundle`).
4. **The repo map:** what each top-level directory is, and that the exporter and research code stay private (with
   the reason).
5. **Build and run locally:** three commands.
6. **Licence** (MIT for code, CC BY-NC 4.0 for prose) and the citation line.

Numbers appear through the same claims: the README is generated from a template by a build step that fills claim
values, so it can't drift from the site. CI fails if `README.md` differs from the rendered template.

## 4. The 3-minute walkthrough video

### 4.1 Script (≈ 420 words at 140 wpm, in six beats)

| Beat | Time | On screen | Says |
|---|---|---|---|
| 1 Hook | 0:00–0:20 | The front door, spine in view | The spine, and why the "no" is the result |
| 2 The system | 0:20–0:45 | `/system`: the pipeline diagram, the feed snapshot | What was built, in one breath. It ran live, and it never made money (E9-G0 Q6) |
| 3 The leak | 0:45–1:30 | II.9: the shift scrubber moving, then the collapse | The story in four steps: found → measured → not fixed quietly → the result collapsed |
| 4 The rules | 1:30–2:10 | IV.17 commit order, IV.16 boundaries, one replay step (R4's, if P0.3 keeps it) | Pre-registration as code, and the agent working inside boundaries |
| 5 The operating model | 2:10–2:40 | IV.19 tiles, IV.20 matrix | What the agent did, what I decided, and what it cost |
| 6 Close | 2:40–3:00 | The front door's path cards | The three paths, and the URL |

The script follows the copy rules (P3 §2): first person, every number on screen comes from a claim on the page
shown, and no profit language. The operator edits it once before recording.

### 4.2 Production

- **Screen captures:** the agent records each beat's segment with Playwright (`recordVideo`, 1920 × 1080, light
  theme, scripted scrolls and clicks at a fixed pace) against `production`. These are clean, repeatable takes that
  can be re-recorded after any site change. No cursor shake and no notifications in frame.
- **Voice:** the operator records the voice-over. Recommended over a synthetic voice, because an interviewer will
  hear the same person later. Fallback: captions only, with a quiet music bed.
- **Captions:** a `.vtt` from the final script with timings, uploaded with the video. They're burned in for the
  LinkedIn upload, since LinkedIn autoplays muted.
- **Edit:** the operator cuts it in whatever editor they use. The agent provides an EDL-style cut list (segment →
  start/end → beat).
- **Hosting:** YouTube, public (its search and recommendations are a channel too), plus a native LinkedIn upload for
  the post. The site **links** to it with a static poster image, with no embed (P5 §6).

## 5. The 1-page PDF

- **A route, `/one-pager`**, styled for print (A4, also fits US Letter with safe margins), built from claims like
  any page. Hidden from nav and `sitemap.xml`, and `noindex`.
- **Content:**
  - the spine;
  - six numbers (the front door's tiles);
  - the three stories as one line each;
  - a small operating-model diagram (the IV.15 loop);
  - "what I'd bring to a team" (three lines from `/lessons`);
  - the URL with a QR code (generated at build, no external service);
  - the name, the CV link and the export date.
- **Built in CI:** Playwright `page.pdf()` renders it, and the PDF is published at a fixed URL. A test checks it's
  exactly one page, and that its text extracts with every claim value present.
- The operator reviews it once on paper (printed) and once on a phone.

## 6. LinkedIn

- **Two drafts:**
  - **Short** (≈ 120 words): the hook, one story, the link.
  - **Long** (≈ 300 words): the hook, three things the program shows, what I'd do differently, the link and the
    video.

  Both are first person and plain, with no hashtag block (at most 3 relevant ones) and no "excited to announce".
- **The first comment** carries the link, where reach requires it, and the operator decides. A second comment
  gives the one-pager link.
- **Featured section:** an item for the site, with the OG image from P5 §7 (checked in Post Inspector).
- **Claims rule:** every number in the post exists as a claim on the site, and the post links to it. The agent
  lists each number with its claim id beside the draft, for the operator's check.
- **Timing:** a weekday morning, after the human test, the video and the PDF are all live. The operator
  picks the day.

## 7. The plugin (deferred, SD-SC-05)

The plugin stays private for now (P4 §12, operator answer 2026-10-15). P6 therefore ships **no** plugin README and
**no** GitHub link, and IV.21 stays diagrams and prose.

If the operator later decides to make it public, a separate item covers:
- a README pass for outside readers;
- the licence;
- a secret and path scan of the full history (gitleaks plus the lab's `scan.py` patterns);
- a demo GIF recorded with `vhs` from the stub-`claude` test harness, so no real session or repo appears in it;
- turning on IV.21's "View on GitHub" link.

That decision isn't on P6's critical path.

## 8. Interview talk tracks (private)

They live in binka (private), **never in `binka-lab`**: they are meant for practice, not publication.

## 9. CV and igor-web

- **CV:** the projects entry is rewritten around the spine and three bullets (rigor, operating model, breadth),
  linking to the site and the one-pager. The agent drafts and the operator edits the CV itself.
- **igor-web:** the `/algo` link exists since P3. P6 adds the lab to the home page or projects listing with its OG
  image, and the video link. The change is made on an igor-web branch, and the operator merges it to its
  `production`.

## 10. The announcement sequence (one sitting, in this order)

1. The human 60-second test has passed and been recorded (§2).
2. v1.0 is on `production`. The disclosure read is signed for any text P6 added: README, `/one-pager`, the video
   page link. Each piece published elsewhere (the video's script and captions, the LinkedIn post, the CV entry and
   igor-web's change) is read against the deny list before it goes out (disclosure policy §5, amended 2026-10-16 by
   E9.P0.8; SD-SC-22).
3. The video is uploaded (public), and its link is live on the site.
4. The one-pager PDF is live at its fixed URL.
5. The igor-web change is merged, and the CV is updated.
6. The LinkedIn post goes out, and Featured is updated.
7. A check from a logged-out browser and a phone: the post's preview, the site, the video and the PDF all work.

Measurement is Cloudflare Web Analytics only (cookieless): referrers, visits per route, and the share of visits
that reach a second act. These are noted in the P6 summary at +1 week and +4 weeks. No other tracking is added.

## 11. Work steps

1. The tester ask, the protocol sheet and the score sheet. **PAUSE (g)**: the operator recruits testers and runs the
   test.
2. The README template and its CI check.
3. The `/one-pager` route, its PDF build and its tests.
4. The video script, shot list, Playwright captures, captions and cut list. **PAUSE (g)**: the operator records,
   edits and uploads.
5. The LinkedIn drafts with their claim table, plus the CV and igor-web drafts.
6. The talk tracks (in binka, private).
7. The announcement card: §10's sequence with every asset's status. **PAUSE (g)**: the operator announces.
8. The P6 summary: test results, published URLs, and the analytics notes at +1 and +4 weeks.

## 12. Exit criteria

1. The human 60-second test has passed with 3 people outside the project, and the result is recorded.
2. The README, video, one-pager and LinkedIn post are published, and every number in them traces to a claim.
3. The CV and igor-web link to the lab.
4. The talk tracks exist, in the private repo only.
5. The P6 summary is written, with the analytics notes.

## 13. Decisions I've taken (flag if you disagree)

- **Voice-over by the operator, not synthetic** (§4.2). An interviewer hears the same voice later.
- **The video is hosted on YouTube and linked from the site, not embedded** (§4.2, P5 §6).
- **The README and the one-pager are rendered from claims in CI** (§3, §5), so neither can drift from the site.
- **Talk tracks stay private, in binka** (§8).
- **The plugin's public release is off P6's critical path** (§7, SD-SC-05).

## 14. Amendments from E9-G0 (2026-10-15)

Applied by E9.P0.1 from [E9](E9_2026-10-15.md) §2 and §8. The rows are in-place fixes.

| Change | Why |
|---|---|
| Video beat 2 shows the feed snapshot and says the system ran live and never made money (§4.1) | E9-G0 Q6; SD-SC-07 |
| Beat 4 and the talk tracks use the replays P0.3 keeps. A story whose replay isn't on the site cites its module or SD page instead (§4.1; §8's talk tracks follow it at E9.P6.6) | E9-G0 Q3: P0 §6.1 adds R5 and R6 as candidates |
