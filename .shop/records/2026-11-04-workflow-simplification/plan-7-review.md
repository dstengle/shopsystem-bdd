# Plan 7 of the workflow simplification: end-of-branch review

This is the review of plan 7 (telemetry), range `22d14c2a..d89d16d6` on `workflow-simplification`. It was done
2026-11-05 by one fresh reviewer, who read:
- `plan-7-telemetry.md`: its Review Focus, Global Constraints and D1-D19;
- `plan-7-implementation.md` and the implementer's ledger (`.superpowers/sdd/plan-7-telemetry/progress.md`);
- `design.md` goal 8, `recon.md`, and the rulings of plans 1-6;
- `CLAUDE.md`, the six new `measure_*` modules and the changes to `scripts/measure`, `measure_show.py` and
  `measure_write.py`;
- decisions 0060, 0078 and 0079, and the three changed skills.

The reviewer changed nothing in the repository except this file, which is not committed. The probes ran in
`/home/vscode/.claude/jobs/7e9ba079/tmp/review7/`.

## Verdict

**Approve plan 7's code. Fix one workflow blocker before the first real batch.**

`measure batch`, `measure defect`, and `show` and `compare` by batch name do what D2-D12 say:
- Every verification figure in the report reproduces.
- The cost arithmetic matches a hand computation to the micro-dollar.
- All five Review Focus classes are pinned by the tests the plan names, and the probes below confirm them.
- No prompt, brief or description text reaches a record.

The smoke run surfaced three issues, which this review weighs:
- **Issue 1 is a blocker for building-a-batch step 7, the design inherited from plan 5.** When a subagent writes a
  file named `findings.md`, the harness refuses it every time. Every such Write in this machine's transcripts was
  refused: 4 of 4, at depths 1 and 2, the plugin's own `bdd-branch-reviewer` among them. A real `pr-reviewer`
  therefore cannot do what the skill says it does.
- Issue 3 (`changed_lines`) should be fixed before a knob is tuned on it.
- Issue 2 (the driver is a subagent) should be fixed by saying so in the summary. A rule for it is a question below.

## Verification (the plan's exact invocations)

| Check | Report | Got |
|---|---|---|
| Task 6 Step 1 (unbuilt) | `False 5 []` | `False 5 []` |
| `python3 -m pytest -q \| tail -2` | 1459 passed, 1 skipped, 4 xfailed, 135 subtests passed (29.7 s); ceiling report `test_e2e_codified` 13.3 s | 1459 passed, 1 skipped, 4 xfailed, 135 subtests passed (29.9 s). `tail -2` shows the ceiling's last line, `test_supervision` flaky-scenario 11.2 s: the same report, a different line shown |
| `python3 -m pytest -m timing -n 0 -q` | 2 passed, 1464 deselected (5.8 s) | 2 passed, 1464 deselected (5.7 s) |
| `model check` | 53 / 16 / 19 / 0 | 53 violations, 16 warnings, 19 unresolved references, 0 file problems |
| `model logic` | 11 findings: 6 L5, 5 L6 | same |
| `model lexicon --check` | 401 terms, 0 problems | same |
| `model decisions --check` | 4 hold, 0 failing | same |
| `features generate --check` | exit 0 | exit 0 |
| `features vocab --check` | every step has one handler | same |
| `features bindings --unbound` | every binding names a scenario | same |
| `tools size --limit 300` | silent | silent, exit 0 |
| `tools check $(git diff --name-only 9d765bb8...HEAD -- '*.py' scripts/measure)` | ruff, vulture clean | ruff "All checks passed!", vulture clean, import-linter no contracts |
| Own limits | `measure` 142 ≤ 150, `measure_show.py` 122 ≤ 135, `measure_write.py` 42 ≤ 50 | 142, 122, 42 |
| Smoke reviewer cost | $0.276098, 5 requests, output 3,712 | The transcript `agent-aa132733cd0321037.jsonl`, recomputed by hand: 5 requests, $0.2760984. Its cache writes are all 5 min (19,657 + 5,723 + 3,953 + 1,129 + 1,516), none 1 h |
| Review Focus tests | named in the plan | all 14 exist in the modules the plan names |

## Probes (a scratch merged batch, synthetic transcripts)

`probe/test_probe7.py` reuses the suite's `merged` fixture: batch-1 reviewed with a fix-now finding, fixed, reviewed
clean and merged. Its store is the test's own. Results:

| Probe | Result |
|---|---|
| A main session with one request a day before `started`, two inside and one 3 days after | 2 requests counted. The window holds |
| A whole session 2 days before the window | absent |
| A subagent whose first request is a day before (`batch-1 t2 b2`) | absent (D4) |
| A repeated transcript (`main.jsonl` copied with the same `requestId`s) | counted once: 2 requests, $0.000892 = 2 × (10·4 + 20·20 + 30·0.2)/1e6 |
| The same row, with no `requestId`, `message.id` or `uuid`, in two files | **counted twice** (2,000,000 output tokens, $40). See M4 |
| A cache-write mix on `claude-opus-5-5`: input 1,000, 5 min write 2,000, 1 h write 3,000, read 4,000, output 500 | $0.0488. By hand: (1000·4 + 2000·4·1.25 + 3000·4·2 + 4000·0.20 + 500·20)/1e6 = (4,000 + 10,000 + 24,000 + 800 + 10,000)/1e6 = 0.0488. New input is 6,000; `cache_creation_input_tokens` is ignored when the breakdown is given |
| A model with no price (`claude-mythos-5-1`) | `unpriced {"claude-mythos-5-1": 1}`, and the summary line says so. The session row shows cost `0` (see M5) |
| Roles | `shopsystem-bdd:pr-reviewer` with any description → review. `batch-1 fix f1` → fixing. `batch-1 t1 b1 …` → implementing. No meta, started at `closed` → fixing. **`batch-7 review 3` → review in batch-1** (M2). **`Explore` "Find the parser" → implementing** (M1) |
| Text leaks | Neither `SECRETPHRASE` (in a description) nor "Find the parser" is in the record |
| `changed_lines` | **1**, the last review's range `b95db14..ec99f6d`. The batch's change `forked_from..ec99f6d` is **56** lines (Issue 3) |
| `measure defect b9` / `--says "  "` / no `--says` / `b3`, which is in no batch | exit 1 `there is no item b9`; exit 1 `--says is empty`; exit 2 argparse; exit 1 `b3 "Another" is in no batch`. Nothing was committed by any of them |
| `measure defect b2 --says "a fault\n\nwith a blank line"`, then `measure batch --replace` | `defect-1.md`, `after_merge {b2: 1}`, `per_item 1.0` |
| `compare batch-1 <initiative record>` | exit 1, `… is a batch's measurement and … is not` |
| `compare batch-1 batch-9` | exit 1, `no measurement of batch-9 …; run measure batch batch-9` |
| `compare batch-1 <junk>` | exit 1, `is not a measurement` |
| `compare batch-01 batch-1` | exit 1, `no measurement at batch-01` (read as a path) |
| `compare batch-1 batch-5`, where batch-5's record is only `{"batch", "cost_by_role": {}}` | **exit 0, with an empty column** (M7) |
| `compare batch-1 batch-1` | ratio 1. Rows whose base is 0 show `-` |
| Old model ids | `claude-opus-4-1-20250805` and `claude-opus-4-20250514` price at $5 / $25 through the key `claude-opus-4` (M3) |

## Findings

### B1. blocking (for the first real batch; not plan 7's code): the reviewer cannot write its findings file

- **Where:** `skills/building-a-batch/SKILL.md:35` ("It writes the findings file the brief names") and `:37` ("never
  edit the findings file"); `agents/pr-reviewer.md:18, 43, 58, 66-93`.
- **Evidence:** the tool result the reviewer got was `Subagents should return findings as text, not write report
  files. Include this content in your final response instead.` I swept every subagent transcript under
  `~/.claude/projects/` (`review7/writes.py`):
  - **Every Write by a subagent of a file named `findings.md` was refused: 4 of 4.** They were 2 by
    `shopsystem-bdd:bdd-branch-reviewer` at depth 1, 1 by a general-purpose agent at depth 1, and the smoke
    reviewer at depth 2.
  - Writes of files named `*review*` mostly succeeded (61 ok, 1 refused).
  
  So the guard is the harness's, keyed on the kind of file, not on depth. A `pr-reviewer` dispatched from the main
  batch session, as plan 5 designs it, will be refused too. Plan 5's design ("the agent writes the findings file")
  does not hold, so step 7 stops at `work batch reviewed` (`has no findings file`).
- **Fix:** make the reply the channel, and have the batch session save it. The main session is not under the guard.
  - `agents/pr-reviewer.md`: "Your final reply is the findings file's content and nothing else, starting at
    `## Verdict`." Write leaves its tools. §"What you return" (`:93`) gives that shape in place of the path and the
    summary.
  - `building-a-batch` step 7: "Save the reviewer's reply byte for byte at the brief's `Findings file:` path (Write),
    then run `work batch reviewed`. Saving is not editing; never change a byte of it."
  - `test_skill_building_a_batch.py` pins "byte for byte at the brief's `Findings file:`". The agent test pins that
    `pr-reviewer` has no Write.
  - Do not rename the file to get past the guard. That works against the harness's intent and may stop working.
- **Ruling recommended (Q1):** the reply is the channel, as above, rather than a `work batch reviewed --from -` that
  reads stdin. Stdin would put the reviewer's text through a shell heredoc, and nothing would be gained, since
  `reviewed` parses the file either way.

### S1. should fix: `changed_lines` measures only the last review's range (Issue 3)

- **Where:** `scripts/measure_batch.py:158`, `changed_lines(root, reviews[-1].range)`.
- **Evidence:** the probe gives 1 against 56 for the batch. In the smoke run it was 2, the fix commits. After any fix
  loop the knob reads the size of the last fix, not of the batch. 0079 tunes batch size and `[review] size` against
  these figures, so a batch that needed fixes would look smaller than one that did not.
- **Fix:**
  - `changed_lines` = numstat over `batch.forked_from..reviews[-1].head`: the whole batch as last reviewed, `.shop/`
    left out.
  - Each entry of `reviews` gains `lines`, its own range's count, so the first review's size (what `[review] size`
    judged) and the fix sizes stay visible.
  - Test: in `test_the_knobs_are_given` on the `merged` fixture (two reviews), `changed_lines` equals numstat over
    `forked_from..<review 2 head>`, and `reviews[1]["lines"]` equals that of review 2's range. Red first against today's
    code.
- **Ruling recommended (Q3):** the whole batch, as above, with each review's own `lines`.

### S2. should fix: a batch driven from a subagent measures planning 0, and nothing says so (Issue 2)

- **Where:** `scripts/measure_batch.py:188` (the default directory); `scripts/measure_batch_sessions.py:55-56`
  (a subagent counts only when it starts inside the window); `scripts/measure_batch_show.py:50-51` (the only warning
  is `sessions_found == 0`).
- **Evidence:** the smoke run. The driver was itself a subagent: its rows carry an `agentId`, its first request is
  before `started`, and it is dropped whole. Its transcript is under the main session's directory, not under the
  worktree's `project_dir`. The record shows planning `0` with no line saying why. Deviation 3 adds to this: a
  directory whose transcripts all fall outside the window prints an empty table and no warning.
- **Fix, now:** `summary` adds one line when no main-session request is counted in the window: `no main session in
  the window at <dir>: a batch driven from a subagent or from another directory needs --sessions <the main session's
  directory>`. It adds another when transcripts were found but none counted: `no session in the window at <dir>`.
  Add a test for each. Keep D2's one-directory default, which is right for the designed workflow, where the batch
  session is a main session in the base checkout.
- **Question (Q2):** should a subagent that is the parent of a counted batch subagent count as the driver? The meta
  files carry `parentAgentId` (the smoke reviewer's has `"parentAgentId": "acc3f32dd4ba3f880"`). Such a subagent would
  be `planning`, counted like a main session (its requests inside the window).
  **Ruling recommended:** yes. It is cheap (`agent_types` reads one more key), and it makes `--sessions <main session
  dir>` measure a subagent-driven batch correctly. That is how every plan of this branch has been run.

### Minor

- **M1. A subagent with a description that is not the batch's is charged to implementing or fixing**
  (`measure_batch_sessions.py:29`). The probe's `Explore` "Find the parser" → implementing. Rule 4 was meant for a
  subagent with no meta. Fix: rule 4 only when there is no description; a subagent described otherwise → `planning`,
  the session's own helper work. Ruling recommended: as stated.
- **M2. Deviation 5 lets another batch's description take its role in this batch**
  (`measure_batch_sessions.py:25`). The probe's `batch-7 review 3` → review in batch-1. Fix: match `batch-<this n>`
  only (pass the batch's name into `role_of`). Another batch's subagent inside this window goes to rule 4, or to M1's
  `planning`.
- **M3. The key `claude-opus-4` prices retired Opus 4.0 and 4.1 at $5 / $25** (`measure_cost.py:11`). The table this
  plan rests on states no price for them, and they were $15 / $75. That is a guess, against D5 and 0018. Fix: key
  `claude-opus-4-5` … `claude-opus-4-8` explicitly and leave older ids unpriced. Claude Haiku 5.5's rate above a 100K
  prompt ($0.50 / $2.50) is not modelled either. Name it in telemetry's `## Not yet`.
- **M4. A row with no `requestId`, `message.id` or `uuid` in two files is counted twice**
  (`measure_read.request_key`, `:137`, falls back to `(path, line)`). Real Claude Code rows carry `requestId`, so the
  impact is low. Fix: fall back to `(session, agent, timestamp)` in `measure_batch_read`, or leave it and say so in
  the module docstring.
- **M5. A session whose every request is unpriced shows cost `0`** (`measure_batch_sessions.py:72`). Fix: `cost` is
  `None` when no request of the session is priced, and `show` prints `-`.
- **M6. `compare` accepts a degenerate batch record** (`measure_batch_show.py:55-56`, `is_batch` reads two keys). A
  record of only `{"batch", "cost_by_role": {}}` compares with exit 0. Fix: require the D9 keys `compare` reads
  (`tokens`, `cost`, `defects`, `findings_by_grade`), else refuse naming the missing key (0018).
- **M7. `compare` prints no knob** (`measure_batch_show.py:80-90`), though 0079 asks a knob decision to give
  `compare`'s figures, and analyzing-a-batch says "say the sizes (items, changed lines) beside the ratio". Fix: add
  rows for `items`, `changed lines` and `reviews`.
- **M8. The skills run `measure batch` twice.** building-a-batch (`:39`) runs it and commits after `work batch
  merged`. analyzing-a-batch step 1 (`:16`) runs it again, and that run is refused without `--replace`. Fix: step 1
  reads "read the measurement building-a-batch wrote (`measure show`); run `measure batch` only when there is none".
  building-a-batch says nothing about measuring after `abandon`; add it beside `abandon`.
- **M9. Refusal text is doubled or unnamed.** The probe printed `measure: measure defect: --says is empty`, and
  `measure: there is no item b9` with no command. Fix: drop the inner `COMMAND` prefix, or have `scripts/measure`
  print the subcommand once.
- **M10. D5's note "Claude Code writes 1 h caches, as the live transcripts show" is not what the smoke run shows**:
  all 5 of its requests wrote 5 min caches. The code reads the breakdown, so no figure is wrong. This is for the
  record only.

## The implementer's decisions

| # | Judgement |
|---|---|
| 1 Requests counted once across files | Agreed. The probe's copied transcript is not doubled. M4 is the one hole |
| 2 A body for the scenario's fix-now finding | Agreed. Forced by plan 5's M5 |
| 3 `sessions_found` counts files | Acceptable. S2 adds the line it lacks |
| 4 `per_item` and `goals` from Task 2; `date` last | Agreed |
| 5 Any `batch-<n>` in a description | Disagreed (M2). The batch's own name is cheap to pass |
| 6 `findings_by_triage` with zeros | Agreed |
| 7 Old `noqa: E402` removed | Agreed. `tools check` is clean |
| 8 Refusal order, and the lock | Agreed. The text is M9 |
| 9 Tests going further, so the mutations bite | Agreed. Good practice |
| 10 `FIGURES` in the shared helper, loaded by path | Agreed |
| 11 A batch record known by two keys | Agreed for `show`. `compare` should check more (M6) |
| 12 `model decisions` prints "wrote" | Agreed. Nothing to match |
| 13 analyzing-a-batch's report sections | Agreed. They follow step 3 |
| 14 The smoke run's three differences | Acceptable, and honestly reported. The reviewer was general-purpose because the installed plugin lacks `pr-reviewer`, as D18 foresaw. Review 2 was a hand stand-in, said so. Planning 0 was explained |

**The real reviewer run.** It answers plan 5's open problem only for a toy change: two items, each a one-line file.
Its $0.28, 5 requests and 36 s of session time are the floor of a review's cost, not an estimate of a real batch's.
The first real batch's measurement gives that. The figure itself is exact: recomputed by hand from the transcript, it
is $0.2760984. The reviewer was usefully adversarial: it found that neither item built its line. It also exposed B1.

## Questions for the person (the person is unavailable; rulings recommended)

- **Q1 (B1):** the findings travel as the reviewer's reply, saved byte for byte by the batch session, and Write
  leaves `pr-reviewer`'s tools. *Recommended: yes.*
- **Q2 (S2):** a subagent that is the `parentAgentId` of a counted batch subagent is the batch's driver: `planning`,
  counted like a main session. *Recommended: yes, with the summary warnings in any case.*
- **Q3 (S1):** `changed_lines` is the whole batch, `forked_from..<last review head>`, and each review keeps its own
  `lines`. *Recommended: yes.*

## Files

- Probe: `/home/vscode/.claude/jobs/7e9ba079/tmp/review7/probe/test_probe7.py`, its output `probe-out.txt`, and the
  merged scratch repository `base/test_probe0/`.
- Transcript sweeps: `review7/refusals.py`, `review7/writes.py`.
- Verification output: `review7/verify.txt`.
