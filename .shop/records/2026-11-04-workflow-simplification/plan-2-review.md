# Plan 2 of the workflow simplification: end-of-branch review

This is the review by the one fresh end-of-branch reviewer, on 2026-11-04. It covers `391612df..f64c68d4` on
`workflow-simplification`, which is five commits: four tasks and the report. I read it against `plan-2-backlog.md`
(its Review Focus, Global Constraints and Decisions), `design.md` goals 1, 2 and 10, `plan-1-rulings.md` and
`CLAUDE.md`. I verified the claims in `plan-2-implementation.md` by running the plan's commands. I also probed the CLI
in scratch repositories outside the worktree. Apart from this file, nothing in the repository was changed.

## Verdict

**Ready to merge, with two should-fix findings. Nothing is blocking.**

- **The checks match the report.** Every verification figure in the report reproduces. All 17 backlog scenarios pass,
  and 37 unbuilt scenarios stay as expected failures.
- **The old commands behave as before.** `work list`, `show`, `status`, `withdraw`, `answer` and `show q<n>` give
  byte-identical output and commits at `391612df` and at `f64c68d4`. I checked this on a copy of this repository's
  real `.shop/work/`.
- **All five Review Focus classes behave as the plan says:**
  - routing by `b<n>`;
  - cycles, both refused and written by hand;
  - dependencies on missing or withdrawn items;
  - `|` and line breaks in titles;
  - malformed files.
- **The scenarios test their point.** I made 12 changes that break the code on purpose. 11 of them each made exactly
  the backlog scenario they should fail. The one that survived (all tables headed `idea`) is caught by a script test
  (finding M1).

**The two should-fix findings:**
- **S1:** two lines `work` prints name an item by its bare id, against the plan's "names next to ids" constraint.
- **S2:** the rule the implementer added for negated item Thens decides plan 4's exit code before plan 4 is written.

The rest are minor findings and two questions, each with the ruling I recommend.

## Verification

All commands were run in the worktree at `f64c68d4`, using the plan's exact invocations (Task 5, Steps 1-2).

| Check | Report | Got |
|---|---|---|
| `python3 -m pytest -q` | 1059 passed, 1 skipped, 37 xfailed, 129 subtests. The known flake failed once under xdist and passed alone. | 1 failed, 1058 passed, 1 skipped, 37 xfailed, 129 subtests. The failure was `test_model_logic_on_the_live_spec_is_fast`, the known flake. Run alone, it passed. So: **1059 passed, 37 xfailed**, as reported. |
| `model check \| tail -1` | 53 violations, 16 warnings, 19 unresolved, 0 file problems | same |
| `model logic \| tail -1` | `11 findings: 6 L5, 5 L6` | same |
| `model lexicon --check \| tail -1` | 401 terms, 0 problems | same |
| `features generate --check` | exit 0 | exit 0. `features/backlog.feature` is not in the diff. |
| `features vocab --check \| tail -1` | `every step has one handler` | same |
| `features bindings --unbound` | `every binding names a scenario` | same |
| `tools size --limit 300` | silent | silent, exit 0 |
| `tools check` over the branch's Python files and `scripts/work` | clean except `scripts/work`'s RUF100 | Vulture and import-linter are clean. Ruff gives 11 RUF100 on `scripts/work`, exit 1. The base had 9 of them, so the 2 new imports added 2 (M7). |
| Unbuilt ids (Task 5, Step 1) | `False 48 []`, where the plan expected 37 | `False 48 []`. Of the 48, 11 belong to `brainstorming` (3) and `pr-review` (8), which have no feature file. The report's explanation holds. |
| Backlog tests alone | n/a | `test_backlog.py` and `test_backlog_*.py`: 108 passed |
| Smoke run (Task 5, Step 3) | Two tables, b1 scores 5.00, b2 blocked by b1 (shaped) with 10 unescaped `\|`, 6 commits | Same, run under bash. The plan's snippet calls `$W` unquoted, which fails under zsh, the person's shell (M10). |
| `unbuilt:` per commit | each id leaves `unbuilt:` in its task's commit | Confirmed: r1, r15 in `bfc07c3c`; r2, r3, r9-r14, r16 in `e5aa5231`; r4, r5 in `a5bfe3cb`; r6-r8, r17 in `e1f04d2e` |
| Spec lines | no requirement line edited | Confirmed: `backlog.md` changes only `unbuilt:`, `## Implementation, may change` and `## Not yet`. |
| `git status` | clean | clean, except this record |

### Probes in scratch repositories

The probes ran under `/home/vscode/.claude/jobs/7e9ba079/tmp`.

| Probe | Result |
|---|---|
| Old commands, run from base `scripts/` and from the new ones, on a copy of the real `.shop/work/` | Identical output and exit for each of these: `list`, `list --json`, `show`, `show --json`, `show i57`, `show i59 --json`, `status`, `show w212`, `show w212 --json`, `answer i58/spec-integration …`, `answer w212 x --change`, `withdraw w212` (with an identical commit), `withdraw w9999`, `show q1`, `answer backlog x`. Only `show b1` differs, as intended. |
| `depend b1 --on b2` after `b2 --on b1` | Refused: `closes the cycle b1 "…" -> b2 "…" -> b1 "…"`, exit 1, nothing committed |
| Depending on itself, a duplicate, an unknown item | Each is refused and labelled |
| Hand-written cycle b2 ↔ b3, then `work backlog` and `work depend b4 --on b2` | Both exit 0 at once, with no hang. Each row names the other item. |
| `depends_on: [b6, b9]`, with b6 withdrawn and b9 missing | `blocked by b6 "F" (withdrawn); blocked by b9 (missing)`, exit 0 |
| Ties and unrated items | Two items at 3.00 go to the lower `b<n>`. Partly rated and unrated items follow the rated ones, by number. |
| A title with `\|`, `"` or a leading `#`, or a blank title, or a title with U+2028 | `\|` is escaped in the cell and in the `waiting on` label. `"` and `#` are kept. A blank title, and one with U+2028, are refused. |
| A note `#n` or an empty note | Both refused |
| Malformed files: `status: doing`, no frontmatter, `depends_on: b1` (a scalar), an id that does not match the file name | `backlog`, `show` and `depend` refuse, naming the file and the field. `shape b1` and `idea` still work when the malformed file is another item's. |
| `b07.md`, and `kind: nonsense` with an unknown key | `b07.md` is **silently skipped** (M3). `kind: nonsense` is **accepted** (M4). |
| A question of two lines, holding a `\|` | The row shows `question: First \| line?`. `work answer` joins the two lines into `- Q: First \| line? second line`. |

### Mutations (scenario vacuity)

I made each change to a copy of the tree at `f64c68d4`, then ran `tests/scenarios/test_backlog.py`.

| Mutation | Failed scenario |
|---|---|
| The provenance cell printed `-` | r6 |
| No `blocked by` in a row | r7 |
| No `question:` in a row | r17 |
| Every table headed `## idea` | **none** (M1) |
| `work show` prints the id without the title | r15 |
| The refusal names no status | r3 |
| `work rate` ignores `--urgency` | r4 |
| `work answer` leaves the item `needs-input` | r16 |
| `work withdraw` from `ready` writes `refused` | r11 |
| `work depend` writes into the target instead of the needing item | r5 |
| `--json` prints a list instead of an object | r8 |
| `work idea` writes `shaped` | r1 |

## Findings

### Blocking

None.

### Should fix

**S1. Two outputs name items by bare id, against the plan's "Names next to ids" constraint (design goal 10).**
- **Where:**
  - `scripts/backlog_cli.py:57`: `work depend` prints `b2 "Rank | order" depends on b1`, with b1 bare.
  - `scripts/backlog_cli.py:99`: `work show b<n>` prints `  depends on: b1, b2`.
- **Evidence:** the constraint says "every line `work` prints about an item names it by `backlog_items.label(item)` …
  This covers confirmations, refusals and tables." The commit message of `work depend` labels both items, but its
  stdout does not. No test pins either line.
- **Fix:**
  - Print the dependencies' labels. For a missing target, print the bare id with `(missing)`, as `waiting on` does.
    For `depend`, use `"%s depends on %s" % (label(item), label(target))`.
  - Add a script test on each line.

**S2. The rule for negated item Thens fixes plan 4's exit code in advance.**
- **Where:** `tests/scenarios/backlog_handlers.py:62-64`.
- **What the rule does:** a Then of the form "the item i<n> is not `v`" now asserts that the last run exited 0.
- **Why it was added:** to stop batches#r3 (`the item i1 is not `in-batch`` after `work batch start`) from passing as
  an XPASS when the command does not exist.
- **The problem:** the spec does not require exit 0. A correct `work batch start` might find nothing it can pick and
  refuse with exit 1. batches#r3 would then fail against a correct implementation, and plan 4 would have to choose an
  exit code to suit a test.
- **Fix:** assert that the command exists rather than that it succeeded. Fail when the last run exited 2 with argparse's
  `invalid choice` on stderr, or more generally when the run is a usage error. This still keeps batches#r3 an
  expected failure until `work batch start` exists, and it leaves the exit code to plan 4.
- **If the rule is kept:** say it in plan 4's Global Constraints.

### Minor

- **M1. r6's status check cannot catch a wrong heading.**
  - **Where:** `tests/scenarios/backlog_handlers.py:226-227`, with D15.
  - **Evidence:** every item the scenario names defaults to `idea`, so printing every table as `## idea` still passes
    r6 (the mutation above).
  - **Why it is minor:** `test_tables_come_in_state_order_and_skip_empty_states` and `test_every_column_of_a_row`
    catch it.
  - **Fix:** none needed. If the handler is touched again, also assert that the heading's count `(<n>)` equals the
    number of rows under it.
- **M2. r8 runs on an empty backlog.**
  - The scenario names no item, so `work backlog --json` prints `{"items": []}`, and printing `{}` would also pass.
  - This is the line's point (a JSON object), and `test_json_is_one_object_in_table_order` pins the content. Note it
    only.
- **M3. Files with odd names in `.shop/backlog/` are skipped, against D16 ("never skipped").**
  - **Where:** `scripts/backlog_items.py:120` and `:141`.
  - **Evidence:** `b07.md`, `b0.md` and `bx.md` are ignored by `work backlog` and by numbering, with no word printed.
  - **Fix:** in `items()`, refuse any `*.md` in `.shop/backlog/` whose stem fails `is_item`, as
    `<rel>: id: the file name is not b<n>`.
- **M4. `kind` is not checked.**
  - **Where:** `scripts/backlog_items.py:88-101`.
  - **Evidence:** a file with `kind: nonsense` parses as an item.
  - **Fix:** refuse `kind != "item"`, naming the field `kind`, and add it to the parametrised malformed-file test.
- **M5. `LINE_BREAKS` is copied rather than imported.**
  - **Where:** `scripts/backlog_items.py:20-21`.
  - **Evidence:** it is a copy of `workqueue_answer.LINE_BREAKS`, and its comment says so. The two are equal today.
  - **Fix:** `from workqueue_answer import LINE_BREAKS`.
- **M6. `test_work_answer_on_a_work_item_is_unchanged` does not test what its name says.**
  - **Where:** `tests/scripts/test_backlog_moves.py:117-122`.
  - **Evidence:** it runs on a `w3` that does not exist, so it exercises only the "not found" path. I checked the real
    path (`answer w212 x --change`, `answer i58/spec-integration …`) by hand, and it is identical to base.
  - **Fix:** write an `awaiting-answer` work-item, with a `log.jsonl` transition, and compare the result of
    `work answer w1 x --change` with a direct call to `workqueue_answer.answer`, as the show test does.
- **M7. `scripts/work`'s RUF100 grew from 9 to 11, so `tools check` on the plan's file list exits 1.**
  - This is a judged deviation (below). It is inherited, and the new imports follow the file's convention.
  - **Fix**, in any later plan that touches `scripts/work`: drop the 11 `# noqa: E402`. The project's ruff does not
    enable E402. Then `tools check` is clean.
- **M8. A refused or withdrawn item can be made a dependency.**
  - **Where:** `scripts/backlog_moves.py:304-318`.
  - **Evidence:** `work depend b1 --on b6` with b6 withdrawn is accepted. By D9 it then blocks b1 for good, and no
    command removes a dependency (D5). See Q1.
- **M9. `b0` and `b01` go to the work-queue.**
  - **Where:** `scripts/backlog_items.py:44`, with `scripts/work`.
  - **Evidence:** `work show b01` says `there is no work-item b01 under .shop/work`.
  - **Why it is minor:** harmless, and consistent with `is_item`. Note it only.
- **M10. The plan's smoke snippet runs only under bash.**
  - **Where:** `plan-2-backlog.md`, Task 5, Step 3.
  - **Evidence:** it sets `W="python3 …"` and runs `$W …` unquoted, which zsh does not split.
  - **Fix:** in later plans' smoke steps, use a shell function, `W() { python3 …/scripts/work --root "$d" "$@"; }`.

### Questions for the person, each with my recommended ruling

**Q1. Does a dependency on a withdrawn or refused item block for good?**
- **The situation:** D9 says it does, and D5 gives no command that removes a dependency. As built, such an item stays
  `blocked by … (withdrawn)` until someone edits the file by hand. Plan 4's batch picking will never take it.
- **Recommended ruling:** keep D9's display, since the person sees why the item is blocked.
  - Now: refuse `work depend` on a target that is `refused` or `withdrawn` (one check in `depend`, and one test).
  - Plan 4, where blocking starts to stop work: add a removal, `work depend B --drop B2`.

**Q2. Should a negated Then require a successful run (S2)?**
- **Recommended ruling:** no. Require that the command exists, and leave its exit code to the line that builds it. If
  the person prefers the implementer's rule, it should be written into plan 4's constraints, so that `work batch
  start` with nothing it can pick exits 0.

## The deviations

| Deviation | Judgment |
|---|---|
| D1 overridden: built on `workflow-simplification`, not on `plan-2-backlog` | Accepted. It follows the main session's ruling, and the plan's D1 row records it. |
| Unbuilt count 48, not 37 | Accepted. This is a mistake in the plan's figure, not in the code: 11 ids belong to capabilities with no feature file. |
| readiness#r3 passed vacuously; fixed by labels in `says` | Accepted and good. A registry Then about an item now has to name the item's label, which carries goal 10 into plans 3 and 4. The report says so under open problems. |
| batches#r3 passed vacuously; fixed by requiring exit 0 on a negated Then | Accepted as a stopgap. Replace it as in S2 or Q2. |
| `ThenExitsErr` on an item added in Task 1 rather than Task 2 | Accepted. Without it, backlog#r3 would have passed as an XPASS against the argparse error. |
| The `question` locals return False outside a scenario that keeps items | Accepted. It keeps supervision's questions on work-items routed as before, and the full suite passes. |
| `blocked_by` shaped as `[{"id", "status"}]`; `work show --json` switched to `row_json` | Accepted. The plan left the shape open, and the shape is pinned by `test_show_json_has_the_row_keys`. |
| An answer with no question is written `- A: <text>` | Accepted. It fills a gap D17 left. |
| A note, reason or answer starting with `#` is refused | Accepted. It is needed, because otherwise D16 would refuse the file afterwards. A title starting with `#` is correctly allowed, since it follows `# `. |
| The report has no frontmatter | Accepted. `model check` has no `report` kind, and plan 1's report has none either. |
| A 60 s subprocess timeout instead of pytest-timeout | Accepted. |
| `tests/scripts/backlog_testing.py` with no row of its own in the module map | Accepted. The `tests/scripts/` row covers it. Every new module under `scripts/` has a row, and `backlog_world.py` and the handlers are named in their rows. |
| `scripts/work` RUF100 | Accepted. It was there before, and the file grew 192 → 202, within the 25 allowed. See M7. |
| D15: the world's own items are `i90`/`i91` (b90/b91) | Accepted. The plan named b90 for `work depend` only, and the second item serves a dependency given by one half. |

### Notes on design fit

- **Goal 1 (states):** the eight statuses match the design. Origin is `provenance`, a property. No transition yet
  leads into `ready`, `in-batch`, `delivered` or `needs-input`; plans 3 and 4 add them.
- **Goal 2 (backlog):**
  - The rank follows WSJF as the person decided, with ties to the item added first.
  - Each row shows name, origin, ratings and blockers.
  - Risk and likelihood, and how far a batch is along, are in `## Not yet`, with reasons. Leaving them out is right
    for now.
- **Goal 10 (names):** met everywhere except S1.
- **Anti-goal "adding an idea must not start work":** met. `work idea` writes and commits one file, and nothing else.
- **Module boundaries:** each of the four modules has the concern its map row names:
  - `items`: the file;
  - `moves`: the commits;
  - `view`: reads only;
  - `cli`: the wiring.

  `scripts/work` has 10 lines of routing. No file is near 300 lines; the largest is `backlog_handlers.py` at 261.
