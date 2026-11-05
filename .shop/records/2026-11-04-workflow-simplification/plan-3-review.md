---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-3-review
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: done
---

# Plan 3 of the workflow simplification: the end-of-branch review

This is the one end-of-branch review of plan 3 (readiness and intake). It covers `3fab8af5..8bf65d63` on
`workflow-simplification`, and checks it against `plan-3-readiness-intake.md` (Review Focus, Global Constraints, D1-D19),
`plan-3-implementation.md`, `design.md`, `plan-1-rulings.md`, `plan-2-rulings.md` and `CLAUDE.md`. The reviewer changed
nothing in the repository except this file. The CLI was probed in scratch repositories under
`/home/vscode/.claude/jobs/7e9ba079/tmp/review3/`. These were the generate fixture (`s1`, and its clone `s1b`), a clone
of this branch (`live`), and an export of `3fab8af5` (`base`) used for comparison.

## Verdict

**Approve, with fixes before the merge. Nothing is blocking.** Both capabilities are built as specified, and every
baseline the report gives reproduces exactly. The old `work outcome` is byte-identical. `spec/` is never written, and
the temporary copy is always removed. An L1 outside the item does not block it. The two skills meet brainstorming r1
and r2 as written.

Five findings should be fixed before the merge:
- `work intake` takes in this context's own outgoing request.
- One test is vacuous: it calls `model` with a bad argument order.
- Both skills tell the session to reword a line with a command that cannot reword.
- A counter-proposal stops its request from ever closing.
- The timing flake now fails nearly every full run. The cause is the extra suite load from plan 3's tests, not a slower
  `model logic`.

## Verification (report vs got)

All commands were run in the worktree with the plan's exact invocations, on 2026-11-05.

| Check | Report | Got |
|---|---|---|
| Unbuilt ids (Task 6 Step 1 one-liner) | `False False ['r3'] 36 []` | `False False ['r3'] 36 []` ✓ |
| `python3 -m pytest -q` | 1143 passed, 1 skipped, 27 xfailed, 131 subtests. The flake failed in 6 of 10 runs, and the final run was clean. | **1 failed**, 1142 passed, 1 skipped, 27 xfailed, 131 subtests, in **6 of 6 runs**. The failure was always `test_model_logic_on_the_live_spec_is_fast` (2.0-2.2 s CPU against a 2 s limit). It passes alone (1 passed). The counts otherwise match. |
| `model check \| tail -1` | 53 violations, 16 warnings, 19 unresolved, 0 file problems | same ✓ |
| `model logic \| tail -1` | `11 findings: 6 L5, 5 L6` | same ✓ |
| `model lexicon --check \| tail -1` | `401 terms, 0 problems` | same ✓ |
| `features generate --check` | exit 0 | exit 0 ✓ |
| `features vocab --check \| tail -1` | `every step has one handler` | same ✓ |
| `features bindings --unbound` | `every binding names a scenario` | same ✓ |
| `tools size --limit 300` | silent | silent, exit 0 ✓ |
| `tools check $(git diff --name-only 3d9e2a91...HEAD -- '*.py' scripts/work)` | clean | ruff and vulture clean; import-linter states no contracts ✓ |
| Line budgets | `work` 211 (≤222), `workqueue_request.py` 252 and unchanged, `backlog_handlers.py` 261 | 211, 252, 261 ✓ |
| Spec edits | only `unbuilt:`, `## Implementation, may change` and `## Not yet` | The only removed lines in `spec/` are the three `unbuilt:` lines. `features/` is untouched ✓ |
| `work ready` time (fixture) | 0.13 s warm, 0.32 s with an empty cache | 0.2 s warm ✓ |
| `work ready` time (**this repository's spec**, on a clone, a `backlog` line) | not measured | **1.5 s** warm (passing). 0.12 s for a parse refusal, because the solve is skipped. **9.9 s** with an empty `XDG_CACHE_HOME`, which compiles the PGF. |

### The CLI probes

| Probe | Result |
|---|---|
| `work line --into nothing` / `--into legacy` (uncodified) | Both refused naming the capability. Exit 1, nothing committed ✓ |
| `work line` with both TEXT and `--term`, or neither | refused ✓ |
| `work line b1 TEXT --into CAP` (TEXT first) | accepted ✓ |
| A line starting `#` | refused, but the message names neither the item nor `work line` (M8) |
| `work line b1 --into work-queue -- '-x'` | exit 2, `unrecognized arguments: -- -x` (M9) |
| `work ready`, passing and failing items | `spec/` sha256 identical before and after. `TMPDIR` is empty after each run, and the tree is clean ✓ |
| **An L1 elsewhere** (`work-queue#r9` written into `spec/`, clashing with `r1`) | an unrelated item readies. An item whose line clashes with r1 and r9 is refused, with both L1s named ✓ |
| A line into `review` (`guarantees`) | readies ✓ |
| An item with a term bullet (`frobnicate`) and a line using it | readies ✓ (no test pins this, M4) |
| `work intake q1` twice | The second is refused: `q1 "Request q1" was taken in already, as b7 "Request q1"` ✓ |
| `work intake` on `awaiting-asker` and `delivered` | refused naming the status ✓ |
| `work intake` on `awaiting-upstream` from `product/…` | `shaped`, provenance `product` ✓ |
| `work intake q99` | `there is no request q99 under .shop/work/requests` ✓ |
| **`work intake` on this context's own request to an upstream** | **taken in as `b9`, provenance `own`**. Its every `work outcome` is then refused (S1) |
| Old `work outcome`: base scripts vs head on cloned repos (`q5 1 accepted`, `q5 2 question`, `q5 9 accepted`, `q5 1 bogus`, and the asker's turn) | the request bytes, the commit subjects and the file lists are identical ✓ |
| `outcome … accepted` with no `--into` on a taken-in request | refused, naming `--into` ✓ |
| `outcome … rewritten --line <non-parsing>` | refused with `parsed up to:`. It calls the counter-proposal "line 1" (M7) |
| `rewritten --line`, then `turn`, accepting the new line, `ready`, then `turn` | The item readies. The request goes back to `awaiting-asker`, and every later `turn` returns it there (S4) |
| `outcome q1 1 bogus` on a taken-in request | written, with a note on the item (M1) |
| `outcome q7 3 accepted --into work-queue --in g10` | `--in` is read as an abbreviation of `--into` (M2) |

## Findings

### Blocking

None.

### Should fix

**S1. `work intake` takes in this context's own outgoing request.** (`scripts/intake_moves.py:48-67`)
- Evidence: in `s1`, I added `## Upstreams` to `spec/index.md` and wrote `q6` with `asker:
  bounded-context/ex.com/prod/ctx` (this context). `work intake q6` printed `b9 "Request q6" shaped`, with provenance
  `own`. After that, `work outcome q6 1 accepted --into work-queue` is refused: `q6 is a request to the upstream up; the
  upstream writes the line outcomes`.
- The result is an item that can never be answered. The skill's description ("a request is open or awaiting the upstream
  in this repository's `.shop/work/requests/`") invites exactly this, because outgoing requests are kept in the same
  folder.
- Fix: in `intake`, refuse before writing, with the predicate of `workqueue_request._refuse_upstream_part`. That is: an
  asker in `own_askers`, upstreams listed and no `source`. The message should be "`q<n> "<title>"` is a request to the
  upstream <up>; it is taken in there". Add a row to `test_intake_refuses_a_request_out_of_turn`, or a test of its own.
  Narrow the skill's description to requests from a peer or the product.

**S2. `test_model_check_accepts_reasons` is vacuous.** (`tests/scripts/test_intake_outcome.py:147-151`)
- Evidence: it runs `model check --root <repo>`. `model` takes `--root` before the subcommand, so the run exits 2 with
  `unrecognized arguments: --root …`, and the test passes on the absence of a phrase. With the right order, the base
  scripts report `q1.md: … a section other than Answers, Lines, Outcomes, Questions, Resolution: Reasons`, and head
  reports nothing. So the code (D13) is right, and only the test checks nothing.
- Fix: run `[model, "--root", str(taken), "check"]`. Assert that `returncode != 2`, and that no output line names
  `q1.md`.

**S3. The skills send the session to a command that cannot do the step.**
- **Rewording a line.**
  - `skills/taking-in-a-request/SKILL.md:22` says "reword the accepted lines it names in the item with `work line`".
  - `skills/shaping-items/SKILL.md:21` says "reword the lines it names … and run it again".
  - `work line` only adds a line (report, open problems). A session that follows either skill adds a second line next to
    the bad one, so the item stays not passing.
- **`model parse` cannot see an item's terms.** `shaping-items` step 2 (`:19`) says to check each line with `model
  parse` and to write a missing word as a term with `work line --term`. A term written that way is only on the item, so
  `model parse` of a line that uses it still refuses. (In my probe, `work ready` accepted the same line once the term was
  on the item.)
- Fix, until a reword command exists (plan 4):
  - Say that the line is reworded by editing its `- [r<n>]` bullet in the item's `## Requirements` (same id) and
    committing it, or that the item is withdrawn and shaped again.
  - Say that a line using a term added with `--term` is checked by `work ready`, not by `model parse`.
  - Also have `taking-in-a-request` say what to do when every line is refused: `work refuse <b>`, because an item with no
    requirement line is never passing (D7).
  - A test that every `` `work <sub>` `` mentioned for rewording is a command that rewords is overkill. A read-through is
    enough.

**S4. A counter-proposal stops its request from ever closing. Question for the person.** (`scripts/intake_moves.py:120`,
`scripts/workqueue_request.py:195-210`)
- Evidence, on `q7`:
  - line 1 `rewritten --line …` added line 3;
  - the asker and the upstream each took one `turn`;
  - lines 2 and 3 were `accepted --into work-queue`;
  - `work ready b10` readied the item;
  - after that, `work turn q7` set `awaiting-asker` again. `turn` counts every entry of `## Lines` and needs every
    outcome to be settled, and `rewritten` is not settled. So the request never reaches `accepted` (requests r8/r9).
- D11 already says a rewritten line is not the item's. The request's negotiation does not follow that.
- The only way out is `work outcome q7 1 withdrawn`, which replaces `rewritten`, loses the record of the counter-proposal,
  and uses the asker's word for it. Neither skill says to do it.
- **Recommended ruling:** a rewritten line whose counter-proposal has a settled outcome counts as settled for `turn`. This
  changes `requests` behaviour, so it needs a new requests line (retire-never-edit does not apply before the merge, by P10,
  but the line is new). Build it in plan 4 next to the batch intake session, and put it in intake's `## Not yet` now.
  Until then, `taking-in-a-request` step 3 should say that the request stays `awaiting-asker` after a counter-proposal is
  accepted. That is harmless for the item.

**S5. The timing flake is now near-certain, from the suite load and not from `model logic`.**
(`tests/scripts/test_revision_done.py:129-144`)
- Evidence:
  - Alone, `model logic --json` on the live spec takes 1.31-1.45 s CPU at head and 1.32-1.35 s at `3fab8af5`, three runs
    each. Plan 3 changed only prose in `spec/`, and `model logic` is no slower.
  - Full suite: head failed **6 of 6** runs (2.0-2.2 s CPU, 2.3-2.5 s wall). The `3fab8af5` export failed **0 of 4**.
    Head with plan 3's 7 new test files `--ignore`d failed **1 of 3**, the rate known before.
  - Suite CPU went from about 265 s user and 60 s sys to about 288 s user and 75 s sys, roughly +12%, with the same 16-17
    s wall time on 32 workers.
  - The new tests start many `work` subprocesses, each of which runs GF and clingo, and they push the best of three
    measured runs just over 2 s.
  - The export is a one-commit repository, so 5 of `test_migrate_upgrade_codified.py`'s tests error there for lack of
    history. They are quick, and they do not explain the 0 of 4.
- So the report's "no baseline got worse" does not hold for the suite. The plan allowed "may fail once", and it now fails
  nearly every run.
- Fix:
  - **Recommended:** the CPU-time ceiling measures the machine when it runs among 32 busy workers. Move it out of the
    parallel run:
    - mark it `timing`;
    - make `addopts` `-m "not fixture and not timing"`;
    - add `python3 -m pytest -m timing -n 0 -q` to every plan's baseline list, next to the suite.
    It is then still run every time, alone, where 2 s is meaningful (it passes there in 2.75 s, with three solves at
    most).
  - **Stopgap,** if it must stay in the parallel run: up to 5 attempts with `time.sleep(2)` between them, so the
    measurement falls after the burst of the 17 s suite.
  - Either way, this is a question for the person only if they want the CPU ceiling held under xdist. Recommended
    ruling: no; hold it serially.

### Minor

| # | Where | Evidence | Fix |
|---|---|---|---|
| M1 | `scripts/intake_moves.py:81-99` | `work outcome q1 1 bogus` on a taken-in request writes `1. bogus` and a note on the item. The old path accepts any word as well, which is kept for compatibility. The new path has no such constraint. | In `_refusals`, refuse a word outside the glossary's `line outcome` values (`accepted`, `rewritten`, `refused`, `question`, `withdrawn`). |
| M2 | `scripts/work` (the `outcome` parser) | `--in g10` on `work outcome` is read as `--into g10`, because of argparse's prefix matching. `work line` has `--in`, so a session will type it. | `allow_abbrev=False` on the `outcome` subparser, or on both. |
| M3 | `tests/scripts/test_readiness_bar.py:108-111` | `test_a_guarantees_line_is_not_generated` checks only exit 0. `features_generate.generate` on `review.md` returns the header with no warning, so the test passes with or without the guarantees skip at `readiness_bar.py:73`. | Call `well_formed` in-process with `features_generate.generate` monkeypatched to raise, and assert no reason. |
| M4 | tests | No test runs `work ready` with an item's own term bullet and a line that needs it (D4's route for a missing word), and none runs an L1 elsewhere on the real solver (Review Focus 2 is pinned only with `spec_solve.run` stubbed). Both pass in my probes. | Add `test_a_line_with_the_items_term_readies` (TERM + FROBNICATE), and an unstubbed version of the L1-elsewhere probe (DONE written into the fixture's `spec/`, ABANDON on the item). |
| M5 | `scripts/readiness_bar.py:84-85` | A missing scenario is found by matching `features generate`'s stderr wording, `features generate: <gid>: no scenario: …`. If generate rewords that message, groups with no scenario pass silently. | Have `features_generate` expose the skipped groups, for example `generate(..., skipped=list)` or a `scenario_text` wrapper, and use that. |
| M6 | `CLAUDE.md:70` | The `backlog_moves.py` row lists `idea … depend`. It lacks `work ready` (`ready`, refused with the bar's reasons). The `backlog_items.py` row does not mention `request`/`asked_by`. | Add both. |
| M7 | `scripts/intake_moves.py:145-148` | A counter-proposal that does not parse is reported as `line 1 does not parse in the upstream's requirement grammar`, which reads as request line 1. | Wrap the refusal: `work outcome: the counter-proposal does not parse: …`. |
| M8 | `scripts/backlog_lines.py:104-108` | `the line starts with #, …` names neither `work line` nor the item (design goal 10, and the plan's "names next to ids"). | Prefix it with `work line: <label>:`. |
| M9 | `scripts/backlog_cli.py:14-22, 50` | `p.__class__ = _LineParser` swaps a parser's class after construction, and `--` before TEXT is then refused. | Replace with `sub.add_parser("line", …)` followed by `parse_intermixed_args` in `cmd`, or make TEXT `nargs="*"` and join it. At least document `--` as unsupported. |
| M10 | `scripts/intake_moves.py:108-130` | The note reads `line 2 of request q1 accepted: fits into work-queue#r10`, with the reason inserted before `into`. | Put `into <id>` before the reason. |
| M11 | `scripts/intake_moves.py:70-78` | `handles` treats a malformed `.shop/backlog/` (`Refused`) as "not taken in", and sends a taken-in request's outcome down the old path without saying so. | Let `Refused` propagate, or catch only a missing backlog. |
| M12 | `scripts/intake_moves.py:21`, `:128`, `:145` | It imports five `_private` helpers of `workqueue_request`. Its `import backlog_lines` and `import workqueue_lines` are inside functions with no cycle or cost reason. (The lazy `readiness_bar` import in `backlog_moves.ready` is justified: it keeps clingo out of every `work` call.) | Move the two imports to the top. When `workqueue_request.py` is next split, make the helpers public. |
| M13 | `scripts/intake_moves.py:56-59` | `intake` reads only `status`. An `open` request with `turn: asker` is taken in. | Also require `turn: upstream`. |

### Questions for the person

- **S4**, a rewritten line and the request's end. Recommended ruling: as S4 says, plan 4 adds the requests line, and the
  skill says so now.
- **S5**, the CPU ceiling under xdist. Recommended ruling: hold it serially, in a `timing` run of its own.
- **The skills against `superpowers:brainstorming`.** `shaping-items`'s description says "before any design document or
  plan is written", but `superpowers:brainstorming` (always on in these sessions) ends in a design document. When both
  fire, the session has two instructions that contradict each other. Recommended ruling: `shaping-items` wins inside this
  repository. Say in its Overview that it replaces brainstorming's "write the design doc" ending here (design goal 4:
  "for larger work a design record is still written", beside the items).

## What met its point

- **Review Focus 1-5:**
  - Each has its pinned test, and my probes reproduce each one.
  - The cleanup of `readiness-*` holds on refusal as well as on success.
  - The old `work outcome` matches the base scripts byte for byte, including the base's own laxity (a line number that
    does not exist, any word).
- **The scenarios:**
  - None is vacuous on its point:
    - r2's refusal must name `work-queue#r5` and `frobnicate`;
    - intake r6's refusal must name `line 1 of request q9`, which only `unsettled` produces;
    - r2-r4 read the request's `## Outcomes`, a changed file holding the reason, and the turn.
  - The D16 Thens (readiness r4, intake r5) require only that the command exists, as Q2 ruled. In both worlds the command
    really runs: r4 refuses an `idea` item, and r5 takes the world's `awaiting-upstream` request in.
- **The skills against brainstorming r1 and r2:**
  - `shaping-items` writes lines with `work line` before `work ready`.
  - The pinned sentence is there, and nothing after `work ready` waits on the person.
  - `test_skill_shaping_items.py` reads them as `test_agents.py` reads the agents, which D15 accepted.
  - The usability gaps are S3.
- **Module boundaries:**
  - `backlog_lines` (the item's block), `readiness_bar` (the bar) and `intake_moves` (intake and the item side of
    outcome) each hold one concern, and each has its `CLAUDE.md` row.
  - `workqueue_request.py` is untouched.
  - The bar runs one solve over the whole copy, so it also catches an L1 across capabilities.

## The implementer's rulings

| # | Ruling | Judgment |
|---|---|---|
| 1 | The `work ready` row is left out of `test_each_move_follows_its_row`. | **Accept.** D7 makes an item with no lines fail. The move has its own test. |
| 2 | `DONE` gives an L1 and an L3, so the L3 test uses `abandon` on a `proposed` initiative, and `DONE` gets a test of its own. | **Accept.** This is better than the plan, because the L1-naming case is now tested. |
| 3 | `work turn` is run once in `test_the_rewritten_line_is_not_the_items`. | **Accept.** It is the right reading: the counter-proposal already passed the turn. |
| 4 | `as_dict` gives `request`/`asked_by` only when set. | **Accept.** Plan 2's pinned JSON keys required it. A consumer must use `.get`. Say so in `work show --json`'s help when the format is documented. |
| 5 | The `_LineParser` subclass. | **Accept, with M9.** The Python 3.11 argparse problem is real, but the class swap is a smell. |
| 6 | The dest of `--line` is `text`. | **Accept.** It is forced by the positional `line`. |
| 7 | The rewritten outcome sets `awaiting-asker`/`asker` itself, and the rule is written twice. | **Accept for now.** The plan said "do not copy it", but the edit is a closure in a file the plan froze, so this was the least bad option. Plan 4 should lift `turn`'s edit to a module-level `_turned(text)`, which costs no lines in `workqueue_request.py`, and call it. |
| 8 | One `spec_solve.run(copy)` over the whole copy. | **Accept.** It is better than the plan's per-capability call, because the solve is whole-context anyway and finds cross-capability L1s. |
| 9 | `ThenK_A` for `request line` is a registry handler. | **Accept.** `vocab --check` reads only the registry. |
| 10 | `local("ThenExitsErr", "reason")` returns False when no readiness Given kept a reason. | **Accept.** Without it, supervision's step breaks. |
| 11 | The counter-proposal fixture is `ABANDON`. | **Accept.** |
| 12 | The skill names `work quote` in words, to pass `test_the_skills_name_only_commands_work_has`. | **Accept, reluctantly.** It sidesteps the test instead of teaching it. Better: let the test exempt a command named on the same line as the unbuilt id (`brainstorming r3`), so that the skill can write `` `work quote` `` when it is built. |
| 13 | Extra tests, and README's skills list. | **Accept.** The extra tests (no such request, the round trip, the JSON, `--line`/`--into` pairing) are all useful. |

Of D1-D19, the report says all were kept, and the code bears that out. D3's duplicate ids across items were seen in the
probe (`b1` and `b2` both took `work-queue#r5`), as expected. They are plan 4's to catch.
