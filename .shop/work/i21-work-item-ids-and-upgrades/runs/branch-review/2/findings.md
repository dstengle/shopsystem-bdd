# Branch review 2: i21-work-item-ids-and-upgrades

**Verdict: DONE_WITH_CONCERNS.**

- **No finding is Critical, and none is triaged fix now.** The three issues that review 1 sent to the person are resolved at HEAD:
  - F1: w90 (was work-queue-5) now records a `## Retires` section (8022157).
  - F2: r26 was widened (988ef68) and the code built (w88, 36ad963). `migrate upgrade` has been run on this repository (9170f7a), and `model check` there goes from 0 unresolved and 88 file problems before it to 0 and 0 after it.
  - F3: `work add` takes a free-text title (w89, d8012dc).
- **One check could not be verified, so the verdict goes to the person.** w87's scenario (supervision r19) and the other `test_supervision.py` scenarios fail only because this session inherits `SHOPSYSTEM_WORK_RUN_WORKER`. This is the same cause as in review 1.
- **One new Important observation.** f69c120, a coordinator commit, deleted the r7 outline row `add i1 ../../w1` without deprecating it first (N1).

## Range and work-items

The range is `202c029c..9170f7a` (66 commits, release-0.24.0). It covers review 1's range `202c029c..5703519` and the 21 commits after it.

Every work-item was renamed by the repository's upgrade 9170f7a. The commits use the old names.

| Work-item (old name) | Accepts | Code commits | How it landed |
|---|---|---|---|
| w87 (supervision-6) | supervision#r19 | 36dd883 | direct bdd-implementer; never claimed; withdrawn |
| w85 (design-model-check-3) | design-model-check#r110 | 3c4f259 (in `work run`), 8869d09 (direct) | merged 7b4a237; withdrawn |
| w86 (migration-tools-1) | migration-tools#r15, r18-r20, r22-r28 | ff22a77 (in `work run`), 234e5c9 (direct) | merged ec98ce6; withdrawn |
| w90 (work-queue-5) | work-queue#r1, r12 | 8ca001d, 92e6f65 (direct) | merged 4456bb7; withdrawn; Retires recorded 8022157 |
| w88 (w1 before the upgrade) | migration-tools#r26 | 36ad963, between ec2bbb9 `ready -> claimed` and f3b75af `claimed -> done` | `work run`, task-reviewed, **green** |
| w89 (w2 before the upgrade) | work-queue#r1, r7 | d8012dc (direct, after `researched -> awaiting-ruling` 83a2cd0) | merged 196fb93; withdrawn |

Commits that belong to no work-item, all made by the coordinator:

- **spec:** 64d0443, 4cf0163, 44d7b80, 988ef68 (r26 widened).
- **features:** bd8cc67, 1a5bed2, 9ec49f5, f69c120 (the r26 scenario, and the r7 row dropped: see N1).
- **proposals and work-items:** 995acbb, 14be11a, bd4877a, 7465755, 6b10b62, c07398b, 2b82be6, 6230fc4, c29e68c, 8014407, 8022157.
- **bookkeeping:** a37e5b7, 68c4067, f9ecfe5, and the `work retry` and `work withdraw` commits.
- **9170f7a, `migrate upgrade: 0.23.1 to 0.24.0`:** the repository's own upgrade. It touches only `.shop/work/**` (renames and rewrites) and adds `.shop/plugin-version`. No code changed.

**Stage directories read:**

- `runs/w85`, `runs/w86` and `runs/w88`: every plan, report, result and review.
- `runs/branch-review/1`.
- w87, w89 and w90 have no implement stage.

## Suite

`Suite: 553 passed, 105 failed at 9170f7a in 7.82 s` (wall time 8.1 s).

- **How it ran:** `python3 -m pytest -q -n auto -p no:cacheprovider -rfEx`.
  - It runs in parallel: `pytest.ini`'s addopts carry `-n`.
  - It is not in-process: the steps run `migrate`, `work` and `model` as subprocesses.
  - Under 60 s, so no finding.
- **All 105 failures are in `tests/scenarios/test_supervision.py`**, and 220 lines of their output carry `work: it was started by a worker of another work run (of the branch review); a worker starts no delivery`.
- **Without that file:** 539 passed, 1 skipped.
- **No xfail or xpass is left.** At review 1 there were 18 xfailed and 17 xpassed.

## Checks

The work-items name no `check:`. Their check is the scenarios they accept, run with `-p work_items --work-item <id>`:

- **w85:** 126 passed, 1 skipped.
- **w86:** 142 passed, 1 skipped.
- **w88:** 124 passed, 1 skipped.
- **w89:** 136 passed, 1 skipped.
- **w90:** 125 passed, 1 skipped.
- **w87:** 1 failed, 122 passed. The failure is `test_a_researcher_is_given_the_workitems_file_set_and_accepted_scenarios_and_a_limit_of_40_turns`, and it carries the marker refusal. **Cannot verify.**
  - What I read instead: `scripts/supervise_worker.py` sets `MAX_TURNS = {"research": 40}` and passes it as `--max-turns`.

**w88's own target**, which its implementer and its task reviewer could not run: on a clone, `model check --json` gave the results below.

| | unresolved | file problems | violation kinds |
|---|---|---|---|
| 9170f7a^ | 0 | 88 (r110 file names) | v9b, v_s2, v_s3, v_w4 |
| 9170f7a | 0 | 0 | v_s2, v_s3, v_w4 |

The upgrade added no violation kind and removed v9b. **Verified.**

**`tools check --base 202c029c`:**

- **ruff:** 180 findings, all style.
  - UP031: 140
  - PLW1510: 12
  - FURB167: 11
  - RUF100: 8
  - UP032: 4
  - UP017: 3
  - I001: 2
  - The files involved are this branch's and two renamed research probes under `.shop/work/i19-…/runs/w83/`. They follow the existing modules' style. The PLW1510 calls at `migrate_upgrade.py:117-118` are the rollback, which ignores failure on purpose. Not graded.
- **vulture:** clean.
- **import-linter:** "the project states no import contracts".
- **`tools size --limit 300`:** printed nothing. The largest file the branch touched is `tests/scenarios/migration_upgrade_steps.py`, at 269 lines.
- **`features deprecated`:** two scenarios.
  - migration-tools @r15, the old `migrate run …` outline.
  - work-queue @r1, the old `add with --part-of …`.
  - Their replacements' work-items (w86 and w90) are `withdrawn`, not `green`, so this is no finding. See Observations.
- **`features bindings`:** "every binding names a scenario".
- **A dry-run mode and a real mode of one operation:** none. `migrate --dry-run` is under "Not yet", so there is no randomized agreement test to run.

## Removed and weakened tests

I searched `git diff 202c029c HEAD -- tests features` for removed `def test`, `assert`, `parametrize`, `skip`, `xfail` and `pytest.mark` lines, and for removed `Scenario` lines and Examples rows.

1. **@r2 and @r7 "add when the work-item's file already exists …" (deprecated)** were removed in 8ca001d, and their `as_it_was` step in 92e6f65 (w90).
   - They proved that `add` never overwrites a work-item, and that `add` refuses on an existing work-item.
   - They are listed in the plan's "Tests the decisions break", and now under w90's `## Retires` (8022157). **Holds.**
2. **The work-queue @r7 outline row `| i1 | ../../w1 | the name ../../w1 is not a file name |`** was removed, and the outline retitled from "add refuses a name or an initiative …" to "add refuses an initiative …", in f69c120. That is a coordinator commit, and it was neither deprecated first nor listed under any Retires.
   - It proved that `add` refused a name holding a path.
   - Under r1 the argument became a title, so the row contradicted r1. **N1.**
3. **The step "it prints a file problem naming X"** (`tests/scenarios/design_model_check_problems.py:164`, 8869d09, w85) still leaves r110's problems out of its count before it asserts `count == 1`. The filter now also drops "is already held by". There is no allowance for it. This is review 1's F4, still open (N2).
4. **Supervision r19's scenario** was retitled "… a limit of 25 turns" to "… a limit of 40 turns" in 9ec49f5. Its line changed through the small-change path (44d7b80), so this is a line change, not a weakening.
5. **The old `migrate run` outline (r15)** was retitled "(deprecated)" and kept.
6. **The work-queue step patterns and `World.work_item`:** as review 1 reported. Every scenario that uses them still matches.
7. **w88's Given** "work-items .shop/work/i10/a.md, …" was a literal step and became a parsed one. It builds the same items and holds no assertion.

No skip or xfail was added, no parametrize case was dropped, and no test function was deleted except `as_it_was`.

## Allowances

- **w88:** "none". 36ad963 changes no assertion, expected value or case. **Holds.**
- **w85 and w86:** "none", as review 1 verified.
- **w89, w90 and w87:** direct implementers, so there is no report.
  - d8012dc only adds `tests/scripts/test_work_add_title.py`.
  - w90's test changes are in its plan and its Retires.
  - 8869d09 is N2.

## Cannot verify

- **w87, supervision r19, `tests/scenarios/test_supervision.py`:** its r19 scenario and the other 104 supervision scenarios fail only on the inherited `SHOPSYSTEM_WORK_RUN_WORKER`.
  - Review 1 asked to run without it, and the request was refused, so I did not try again or work around it.
  - The code reads 40 turns.
- **The authority for N1:** f69c120's message gives a reason ("a title is no file name since r1 changed") but names no ruling. The ruling on w89 covers only the empty title.

## Findings

### N1. Important (no work-item: coordinator commit f69c120; observation): a non-deprecated outline row removed from features/
- **Where:** `features/work-queue.feature:110` (the r7 outline). The row `| i1 | ../../w1 | the name ../../w1 is not a file name |` was deleted and the outline retitled.
- **What is wrong:** a scenario was removed without first being deprecated and then retired by a work-item's Retires. Review 1's F3 asked for a ruling on deprecating this row; the commit records none.
- **Why it matters:** the feature files lost a case on no recorded authority. The behaviour is now right, though: under r1, `work add i1 ../../w1 …` writes `w<n>.md` with the heading `../../w1`, and `tests/scripts/test_work_add_title.py` pins a title holding `/`.
- **Why an observation:** no wrong answer follows from it.
- **Fix:** have the person confirm the removal, recorded as w89's or w90's Retires, or in the delegation record. No code changes.

### N2. Important (w85; observation): a step's assertion loosened with no allowance (review 1 F4, open)
- **Where:** `tests/scenarios/design_model_check_problems.py:164`.
- **What is wrong:** the step drops "a work-item's file is named w<n>.md" and "is already held by" problems before it asserts `count == 1`. No plan or allowance covers this.
- **Fix:** as review 1 said. Record the allowance with a ruling, or apply the filter only to fixtures not named `w<n>.md`.

### N3. Important (all withdrawn work-items; observation): code reviewed only by the branch review (review 1 F5, narrowed)
- **What is wrong:** 36dd883, 3c4f259, 8869d09, 234e5c9, 8ca001d, 92e6f65 and d8012dc had no task review. 36ad963 (w88) did.
- **Why an observation:** each is attributed in its work-item file and its merge, and this review read each one.

### N4. Minor (w88; observation): the ambiguity refusal says "reference" and repeats a line
- **Where:** `scripts/migrate_upgrade_ids.py:110` (`resolver(held, names, "reference", …)`).
- **Reproduction:** `i1-x/a.md`, `i2-y/a.md`, and `i3-z/c.md` with `blocked_by: [a]` and `for: a`, plus `i3-z/d.md` with `depends_on: [a]`. `migrate upgrade` exited 1, changed nothing, and printed `could not rename the reference a of .shop/work/i3-z/c.md: initiatives i1-x and i2-y all hold it` twice, then once for d.md.
- **Why it is only wording:** r7 holds, because the refusal names each change. The task review's finding 2 is still open.

### N5. Minor (w88; observation): the widened token pattern rewrites any token that equals a work-item's name
- **Where:** `scripts/migrate_upgrade_ids.py:50`.
- **What happens:** the task review's finding 3 is still open. Given `for: migration-tools#r26` beside a work-item `migration-tools.md`, the upgrade writes `w2#r26`.
- **I probed further:**
  - A comment in a block list is rewritten too: `- work-item/item # item` became `- work-item/w2 # w2`.
  - A qualified id of another context, `for: work-item/other.org/x/y/example`, is correctly left alone.
- **Why it is no wrong answer today:** this repository's `for:` values are all `work-item/<name>`, and it is already upgraded.

### N6. Minor (w88; observation): Decision 4's move check has no unit test
- **Where:** `scripts/migrate_upgrade.py:81-90`. This is the task review's finding 1.
- **Keep as a test:** a repository with `.shop/work/i1-x/a.md`, `.shop/work/i1-x/runs/a/x` and a tracked `.shop/work/i1-x/runs/w1/y`. `migrate upgrade` should exit 1 with `could not move .shop/work/i1-x/runs/a onto .shop/work/i1-x/runs/w1` and leave `a.md` in place.

### N7. Minor (w89; observation): a branch of `entry` no caller reaches
- **Where:** `scripts/workqueue.py:59`.
- **What is wrong:** `"file name" if what == "name"` is unreachable now. The only callers pass `"initiative"` (`workqueue.py:70`, `supervise.py:64`), and vulture does not see a dead branch.
- **Fix:** cheap; drop the conditional.

### N8. Minor (w88; observation): a stale module docstring
- **Where:** `scripts/migrate_upgrade_ids.py:1-4`.
- **What is wrong:** it still says "its initiative's `blocked_by` and `depends_on` follow". Since r26 changed, every work-item's `blocked_by`, `depends_on` and `for` follow, across initiatives, and an ambiguous name is refused.
- **Fix:** cheap; one sentence.

### N9. Minor (w85, w86, w90; observations from review 1, still open at HEAD)
- **F6:** two work-items holding one frontmatter id print no problem (`model_work.py:82`). r110 is checked on the stem.
- **F7:** `migrate status --hook` crashes with `ValueError` when `.shop/plugin-version` holds `next` (`migrate_upgrade.py:19`, `number()` is unchanged).
- **F8:** `migrate upgrade` crashes with `AttributeError` when `spec/index.md` has no `bounded-context` id (`migrate_upgrade_ids.py:22`).
- **F9:** initiatives with one number are numbered in `iterdir` order (`migrate_upgrade_ids.py:36`). The sort key is the number alone.
- **F10:** `add` beside a non-work-item `w<n>.md` refuses, naming a work-item that does not exist (`workqueue.py:81`).
- **F12 (drop):** `tests/scripts/test_migrate_upgrade_ids.py:12` makes `mkdtemp` repositories and never removes them.
- **F11 is fixed:** `scripts/work:49` now says `title`, and `skills/migrating-to-capabilities/SKILL.md:111` says `<title>` and to take the printed id.

### Probe that passed
I probed a repository partly on the new ids: 0.23.1, with an old `a.md` beside a `w1.md` that the 0.24.0 `work add` wrote, holding `blocked_by: [a]`.

- `migrate upgrade` exited 0. It made `w1.md` from a and `w2.md` from the old w1 (`blocked_by: [w1]`) and left the tree clean.
- `apply`'s temporary names handle the chained renames.
- This is how w88 and w89 were added on this branch before 9170f7a, and the real upgrade bears it out.

## Shape

The `CLAUDE.md` rules and module-map rows the branch touched:

- **Size limit 300:** met. `tools size` printed nothing.
  - `migration_upgrade_steps.py` is at 269 lines. The next scenario added there should go in a new module.
- **`scripts/migrate_upgrade*.py`, "one module a step":** met. The step is `migrate_upgrade_ids.py` (119 lines), and the framework with its new move check is `migrate_upgrade.py` (137 lines, `:81` `move_failures`, `:104` the refusal before any `git mv`).
- **`scripts/work` with `scripts/workqueue.py`:** met.
  - `workqueue.py:71-74` checks the title.
  - `work:49` names the argument `title`.
- **`scripts/model*.py`:** met (`model_work.py:82`).
- **`scripts/supervise*.py`:** met (`supervise_worker.py`, `MAX_TURNS`).
- **`hooks/hooks.json`:** met (`hooks/hooks.json:8`).
- **`tests/scenarios/`, one `<capability>_*_steps.py` module a concern:** met by `work_queue_add_steps.py`.
  - `migration_upgrade_steps.py` follows the existing `migration_*_steps.py` prefix, not `migration_tools_*`. This was already so before the branch.
  - Review 1's note still stands: `work_queue_add_steps.py` imports from `test_work_queue` inside functions. The refactor would be complete when `grep -n "from test_work_queue\|import test_work_queue" tests/scenarios/work_queue_add_steps.py` prints nothing.
- **`tests/scripts/`, tests of the scripts that no scenario drives:** met. `test_migrate_upgrade_ids.py` covers the block-list `for:`, the ambiguous refusal and a dangling name. `test_work_add_title.py` covers a title with `/` and the empty and line-break refusals.
- **Code no scenario reaches:** vulture is clean. N7 is a dead branch.
- **Code no line asks for:** none.
  - The ambiguity refusal and `move_failures` are migration-tools r7 ("If `migrate` cannot make every change … exit with an error, naming each change") and the Implementation note ("A relocation onto a file that exists is a change it cannot make").
  - The empty-title refusal is r7 under w89's ruling, reading A.
  - The newline refusal is r7, since a heading is one line.

## Coupling

Unchanged since review 1. The plugin relies on Claude Code's published plugin contract:

- `hooks/hooks.json` found by convention;
- `${CLAUDE_PLUGIN_ROOT}` expanded in a command hook;
- a SessionStart hook's stdout added to the session's context.

All of it is published. The hook has no `matcher`, so it speaks on resume and compact too. That is within the contract; add `"matcher": "startup"` if that is not wanted. The hook also needs `python3` on PATH, which the plugin's other commands assume too.

The repository is now on 0.24.0 (`.shop/plugin-version`), so the hook tells this repository's sessions nothing.

## Observations

- **The two deprecated scenarios have no work-item to retire them.** migration-tools @r15 old and work-queue @r1 old have built, withdrawn replacements. Reproduction: `python3 <Scripts>/features deprecated` prints both.
- **The supervision scenarios fail under every `work run` branch review.** `tests/scenarios/test_supervision.py` fails whenever `SHOPSYSTEM_WORK_RUN_WORKER` is set. The fixtures that start `work run` should drop it from the environment they pass. Reproduction: the suite line above.
- **N2 to N9:** reproductions are given with each.
- **Clean-up:** the probes ran in `.shop/scratch/i21-work-item-ids-and-upgrades-branch-review/` (pytest `tmp_path` repositories and clones of this worktree at 9170f7a and 9170f7a^). That directory has been deleted, and `git status` is clean.
