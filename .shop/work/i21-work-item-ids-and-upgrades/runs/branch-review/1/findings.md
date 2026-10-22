# Branch review: i21-work-item-ids-and-upgrades

**Verdict: DONE_WITH_CONCERNS.** The branch delivers what its lines ask on the inputs the scenarios build, but four things go to the person:

- **One Critical finding.** Two deprecated scenarios were removed by a work-item that lists no Retires (F1).
- **Two findings triaged fix now.**
  - `migrate upgrade` on this repository, the first real target, leaves `model check` with 20 references that no longer resolve. Before the upgrade there were none (F2).
  - `work add` refuses a title that holds "/" (F3).
- **One check I could not verify.** supervision-6's scenario (supervision r19) and every other `test_supervision.py` scenario fail in this session. The cause is the marker `SHOPSYSTEM_WORK_RUN_WORKER`, which `work run` set for the branch review. The permission layer refused to unset it, and I did not work around that.

## Range and work-items

`202c029c..5703519` (45 commits, release-0.24.0). The initiative is i21-work-item-ids-and-upgrades. Every work-item is `withdrawn` and was finished outside `work run`:

| Work-item | Accepts | Code commits | How it landed |
|---|---|---|---|
| supervision-6 | supervision#r19 | 36dd883 | direct bdd-implementer, merged fb24896; never claimed |
| design-model-check-3 | design-model-check#r110 | 3c4f259 (in `work run`: ready→claimed 6fa418f, then claimed→awaiting-ruling 7fe72a2), 8869d09 (direct) | merged 7b4a237 |
| migration-tools-1 | migration-tools#r15, r18-r20, r22-r28 | ff22a77 (in `work run`: b4a211e…0a46dcb), 234e5c9 (direct fix of its task review's F1/F2) | merged ec98ce6 |
| work-queue-5 | work-queue#r1, r12 | 8ca001d, 92e6f65 (direct; never claimed) | merged 4456bb7 |

Commits of formulation and of the coordinator, which belong to no work-item:

- spec: 64d0443, 4cf0163, 44d7b80
- features: bd8cc67, 1a5bed2, 9ec49f5
- proposals and work-items: 995acbb, 14be11a, bd4877a, 7465755, 6b10b62, c07398b, 2b82be6
- bookkeeping: a37e5b7, 68c4067, and the `work retry` and `work withdraw` commits

The brief has no `Read:` line. I found the stage directories under `.shop/work/i21-work-item-ids-and-upgrades/runs/` and read all of them. supervision-6 has no stage directory. design-model-check-3 has no review. work-queue-5 has no implement or review stage.

## Suite

`Suite: 546 passed, 105 failed at 5703519 in 7.75 s` (wall time 8.0 s).

- **How it ran:** `python3 -m pytest -q -n auto -p no:cacheprovider -rfEx`, in parallel (xdist `-n auto`).
- **Not in-process:** the step definitions run the scripts (`migrate`, `work`, `model`) as subprocesses. The suite is under 60 s, so this is no finding.
- **The 105 failures are all in `tests/scenarios/test_supervision.py`.** The cause is the inherited marker `SHOPSYSTEM_WORK_RUN_WORKER`:
  - `work run` refuses (r21) with "work: it was started by a worker of another `work run` (of the branch review); a worker starts no delivery". 220 lines of the output carry that message.
  - The other failures show what follows from it: no worker started, no branch, statuses unchanged.
  - `env -u SHOPSYSTEM_WORK_RUN_WORKER …` needed approval, which this session cannot give, so the supervision scenarios are not verified at HEAD.
- **Everything outside `test_supervision.py` passes.** That includes the scenarios this branch added and the `tools map` tests that the implementers had seen fail.

## Checks

The work-items name no `check:`. Their check is the scenarios they accept, run with `-p work_items --work-item <name>`:

- **design-model-check-3:** 119 passed, 1 skipped.
- **work-queue-5:** 118 passed, 1 skipped.
- **migration-tools-1:** 134 passed, 1 skipped.
- **supervision-6:** 115 passed, 1 failed. The failure is `test_a_researcher_is_given_the_workitems_file_set_and_accepted_scenarios_and_a_limit_of_40_turns`, and it carries the marker refusal. **Cannot verify.**
  - What I read instead: `scripts/supervise_worker.py:40` sets `MAX_TURNS = {"research": 40}`, and line 186 passes it as `--max-turns`. The step `supervision_then_workers.py:213-215` asserts the feature's number.

`tools check --base 202c029c`:

- **ruff:** 161 findings in the files the branch touched, all style:
  - UP031 percent-format: 124
  - PLW1510 `subprocess.run` without `check`: 11
  - FURB167 `re.M`/`re.I`/`re.S`: 10
  - RUF100 unused noqa: 7
  - UP032: 4
  - UP017: 3
  - I001: 2

  These are the same patterns the existing modules use, and none is a defect. The PLW1510 calls in `migrate_upgrade.py:99-100` are the rollback, which ignores failure on purpose.
- **vulture:** clean.
- **import-linter:** "the project states no import contracts".
- **`tools size --limit 300`:** printed nothing. The largest new file is `tests/scenarios/migration_upgrade_steps.py`, at 227 lines.
- **`features deprecated`:** two scenarios.
  - `migration-tools.feature` @r15, the old `migrate run … (deprecated)`, deprecated for the `<command>` outline.
  - `work-queue.feature` @r1, the old `add with --part-of … (deprecated)`, deprecated for the title/id scenario.
  - Their replacements' work-items (migration-tools-1, work-queue-5) are `withdrawn`, not `green`, so no finding under that rule. But no work-item is left that will retire them; see Observations.
- **`features bindings`:** "every binding names a scenario".
- **A dry-run mode and a real mode of one operation:** none. `migrate --dry-run` is under "Not yet" in migration-tools.md, so there is no randomized agreement test to run.

## Removed and weakened tests

I searched `git diff 202c029c HEAD -- tests features` for removed `def test`, `assert`, `parametrize`, `skip`, `xfail` and `pytest.mark` lines, and for removed scenarios.

1. **Scenario removed:** `work-queue.feature` @r2 "add when the work-item's file already exists leaves the file as it was (deprecated)" (8ca001d), with its step `as_it_was` (92e6f65).
   - It proved that `add` never overwrites a work-item.
   - work-queue-5's plan lists it under "Tests the decisions break", under reading A of its question.
   - The work-item has no Retires section: see F1.
2. **Scenario removed:** `work-queue.feature` @r7 "add when the work-item's file already exists is refused, saying so, with an error (deprecated)" (8ca001d).
   - It proved that `add` on an existing work-item is refused.
   - The plan lists it the same way as #1. No Retires: see F1.
3. **Assertion loosened:** `tests/scenarios/design_model_check_problems.py:165` (8869d09). The step "it prints a file problem naming X" now drops r110's two problem texts before it asserts `count == 1`.
   - It proved that exactly one file problem names the file.
   - design-model-check-3's plan says "None" under "Tests the decisions break". 8869d09 has no report and no allowance: see F4.
4. **Step patterns rewritten in `test_work_queue.py`:** `prints_statuses` narrowed to `\S+ with .+`, `drafted` excludes `whose`, `given_fields` reads the printed id, `with_items` accepts a repeated "and whose work-item".
   - work-queue-5's plan lists each one. Every scenario that used them still matches and passes.
5. **`World.work_item`** (conftest.py) gained defaulted arguments. The existing callers are unchanged.

No skip or xfail was added, no parametrize case was dropped, and no test function was deleted except `as_it_was`.

## Allowances

- **design-model-check-3:** the report says "none". 3c4f259 changes no assert, expected value or case, so "none" holds. 8869d09 came later and has no report (F4).
- **migration-tools-1:** the report says "none". ff22a77 and 234e5c9 only add tests, so "none" holds.
- **work-queue-5 and supervision-6:** no implementer report, because they were direct implementers. work-queue-5's test changes are all in its plan's "Tests the decisions break". supervision-6 changed no test.

## Cannot verify

- **supervision-6's scenario (r19) and the other 104 `test_supervision.py` scenarios at HEAD.** They fail only on the inherited worker marker, and unsetting it was refused.
- **The ruling behind F1.** No record of the coordinator's ruling on work-queue-5's question says which reading it took. The work-item file says only "Ruled by the coordinator".
- **My own conduct, for the record:** one read-only command ran after a `cd` into the initiative's directory. I came straight back and nothing was written.

## Findings

### F1. Critical (work-queue-5, fix now): two deprecated scenarios removed without a Retires
- **Where:** `features/work-queue.feature` (8ca001d removed the @r2 and @r7 "add when the work-item's file already exists …" scenarios). The work-item file is `.shop/work/i21-work-item-ids-and-upgrades/work-queue-5.md`.
- **What is wrong:** a change under `features/` is allowed only for a deprecated scenario that a work-item lists under Retires. work-queue-5 has no Retires section, and its own question says the implementer therefore may not retire them. The removal is reading A of that question. No record says reading A was the ruling.
- **Why it matters:** the feature files lose two scenarios on no recorded authority. The @r7 one pinned a refusal that still exists in the code (`workqueue.py:81`).
- **Fix:** have the person confirm reading A, then record it as a `## Retires` section of work-queue-5 naming both scenarios. Nothing in the code changes.

### F2. Important (migration-tools-1, fix now): `migrate upgrade` leaves references that no longer resolve
- **Where:** `scripts/migrate_upgrade_ids.py:56` (`rewrite_item` rewrites only `blocked_by`/`depends_on`) and `:72` (`plan` builds `names` one initiative at a time).
- **What is wrong:** the step rewrites a work-item's old name in its own initiative's `blocked_by` and `depends_on` only. It does not rewrite:
  - `for:`, the field of an enabling work-item, even within one initiative;
  - a `blocked_by` that names a work-item of another initiative.
- **Reproduction:** I cloned HEAD into a pytest `tmp_path` (outside the checkout), then ran `python3 scripts/migrate upgrade` and `python3 scripts/model check --json` in the clone.
  - The upgrade exited 0: "upgraded to 0.24.0: work-items named by ids", one commit of 276 files, nothing left uncommitted.
  - `model check` had **0 unresolved before and 20 after**. Examples:
    - `.shop/work/i15-size-limit/w77.md: work-item/…/size-check is not a work-item in this repository`, from `for: work-item/size-check`, same initiative;
    - `i1-first-spec/w1.md` → `formulation-1`, from `blocked_by`, another initiative;
    - `i10-delivery-on-v3/w30.md` → `pytest-bdd-suite`, `final-layout-read`.
- **Why it matters:**
  - This repository is on 0.23.1, and the hook already offers it this upgrade. This session's own start said so.
  - Taking the offer leaves its work model invalid, and the old names survive only in git's rename history.
  - The upgrade contradicts migration-tools' Purpose (an upgrade "takes a repository … from one plugin release to the next") and design-decision/work-items-named-by-ids ("every command that names a work-item names it by that id").
  - The code does what r26 says. r26 itself is too narrow.
- **Fix:**
  1. Write the line first, through integrating-a-proposal: r26 rewrites every work-item reference (`for`, `blocked_by`, `depends_on`), in the work-items of every initiative.
  2. Then build `names` across all initiatives in `plan` and rewrite `for:` too.
- **Keep as a test:** a repository with `spec/index.md` holding `id: bounded-context/example.org/acme/shop`, and three work-items, each `---\nid: work-item/example.org/acme/shop/<name>\nkind: work-item\nstatus: drafted\n<extra>---\n# t\n`:
  - `.shop/work/i1/a.md`;
  - `.shop/work/i1/b.md` with `for: work-item/a`;
  - `.shop/work/i2/c.md` with `blocked_by: [work-item/a]`.

  Commit them and run `migrate upgrade`. Today it exits 0, but `i1/w2.md` keeps `for: work-item/a` and `i2/w3.md` keeps `blocked_by: [work-item/a]`. Both should name `w1`. The real-target check is the same: on a clone of this repository, `model check --json`'s `unresolved` is the same before and after `migrate upgrade`.

### F3. Important (work-queue-5, fix now): `work add` refuses a title holding "/"
- **Where:** `scripts/workqueue.py:71`, `entry(title, "name")`.
- **What is wrong:** r1 makes the argument a title, written as the `# ` heading, and no longer a file name. Yet `work add i1 "Read a/b files" --part-of capability-proposal/p1 --under thing --accepts thing#r1` exits 1 with "work: the name Read a/b files is not a file name".
- **Why it matters:**
  - It is a refusal where r1 asks for a write.
  - The delivering-an-initiative skill now tells sessions to give a title that "says what it delivers", and this project's titles routinely name paths (`scripts/features`).
  - The plan's D1 kept the check so that the existing r7 outline row `add i1 ../../w1` still passes. That row now contradicts r1.
- **Fix:** have the person rule on deprecating the r7 `../../w1` row for `add`. Then check a title only for empty or a newline.

### F4. Important (design-model-check-3, observation): a step's assertion loosened with no allowance
- **Where:** `tests/scenarios/design_model_check_problems.py:165` (8869d09).
- **What is wrong:** "it prints a file problem naming X" now excludes the problems that carry r110's texts before it asserts that exactly one problem names the file. The plan said no test breaks, and no report or allowance row covers the change.
- **Why it matters:** the step no longer fails when an r110 problem appears beside the one it pins, for files such as `.shop/work/i1/p1.md`.
- **Why an observation:** the scenarios' feature text names `p1.md` work-items, so they cannot be renamed without a feature change. The step still proves that its own problem appears exactly once.
- **Fix:** record it as an allowance with a ruling, or narrow the filter to the scenario rows whose fixtures are not `w<n>.md`.

### F5. Important (all four work-items, observation): code commits outside any work-item window, most never task-reviewed
- **What is wrong:** apart from ff22a77, every code commit lies outside a `ready -> claimed` … `claimed -> done` window:
  - 3c4f259's window ends in `awaiting-ruling`, not `done`;
  - 36dd883, 8869d09, 234e5c9, 8ca001d and 92e6f65 were direct implementers.
- **Why it matters:** none of 36dd883, 8869d09, 234e5c9, 8ca001d, 92e6f65 or 3c4f259 had a task review. This branch review is their only review.
- **Why an observation:** each is attributed in its work-item file and merge message, and each was reviewed here (F1, F3, F4, F6, F10).

### F6. Minor (design-model-check-3, observation): two work-items holding one frontmatter id print no problem
- **Where:** `scripts/model_work.py:82`.
- **Reproduction:** `i1/w3.md` and `i1/w4.md`, both holding `id: work-item/…/w3`. `model check --json` prints no problem or unresolved naming either file.
- **Why an observation:** r110's id is the file stem, by the formulation ruling, and the plan named this as open case D3. A copied work-item file whose id was not edited goes unnoticed.

### F7. Minor (migration-tools-1, observation): the hook crashes on a non-version `.shop/plugin-version`
- **Where:** `scripts/migrate_upgrade.py:18`.
- **Reproduction:** `migrate status --hook` with `.shop/plugin-version` holding `next` exits 1 with `ValueError: invalid literal for int() with base 10: 'next'`. The task review's F3, still open.

### F8. Minor (migration-tools-1, observation): `migrate upgrade` crashes on a `spec/index.md` without a context id
- **Where:** `scripts/migrate_upgrade_ids.py:21`.
- **Reproduction:** with `spec/index.md` holding `---\ntitle: shop\n---\n` and `.shop/work/i1/a.md`, `migrate upgrade` exits 1 with `AttributeError: 'NoneType' object has no attribute 'group'`. Nothing is written or committed.
- **Why an observation:** migration-tools r7 asks for a refusal naming the change, not a traceback. But a repository on the final layout always has the id.

### F9. Minor (migration-tools-1, observation): initiatives with one number are numbered in directory-listing order
- **Where:** `scripts/migrate_upgrade_ids.py:35`.
- **Reproduction:** with `.shop/work/i2-b/x.md` and `.shop/work/i2-a/y.md`, `migrate upgrade` made `i2-b/w1.md` and `i2-a/w2.md`. The order follows `iterdir`, so it is not deterministic.
- **Fix:** sort by `(number, directory name)`.

### F10. Minor (work-queue-5, observation): `add` beside a non-work-item `w<n>.md` refuses with a wrong message
- **Where:** `scripts/workqueue.py:81`.
- **Reproduction:** with `i1/w1.md` a work-item and `i1/w2.md` a capability-proposal, `work add i1 T …` exits 1: "the work-item w2 already exists (.shop/work/i1/w2.md); work add leaves it as it was".
- **Why it matters:** r12 numbers from work-items only, so the refusal names a work-item that does not exist. No client names a proposal `w<n>` today.

### F11. Minor (work-queue-5, observation): stale `name` in two places
- `scripts/work:49`: the positional argument of `add` is still `name`.
- `skills/migrating-to-capabilities/SKILL.md:111`: still says `work add <initiative> <name>`. It was not touched by the branch, but its meaning changed: the name is now a title, and the work-item is `w<n>`.
- **Fix:** cheap; rename both to `title` and say that the id is printed.

### F12. Minor (migration-tools-1, drop): temporary repositories are never removed
- **Where:** `tests/scripts/test_migrate_upgrade_ids.py:11`. `tempfile.mkdtemp()` repositories are never removed.

## Shape

The `CLAUDE.md` rules and module-map rows the branch touched:

- **Size limit 300:** met. `tools size` printed nothing.
- **`scripts/migrate*.py`, and the new row `scripts/migrate_upgrade*.py`** ("one module a step"): met. The step is in `migrate_upgrade_ids.py` (93 lines) and the framework in `migrate_upgrade.py` (119).
- **`hooks/hooks.json`** (new row): met, `hooks/hooks.json:8`.
- **`scripts/work` with `scripts/workqueue.py`:** met, `workqueue.py:62` `highest` and `:68` `add`.
- **`scripts/model*.py`:** met, `model_work.py:82`.
- **`scripts/supervise*.py`:** met, `supervise_worker.py:40`.
- **`tests/scenarios/`, one `<capability>_*_steps.py` module a concern:** met by `migration_upgrade_steps.py` and `work_queue_add_steps.py`. `work_queue_add_steps.py:9,30,55` imports from `test_work_queue` inside functions to avoid a circular import. That works, but a shared helper module would be cleaner. Observation; it would be complete when `work_queue_add_steps.py` has no import from `test_work_queue`.
- **`tests/scripts/`:** met, `test_migrate_upgrade_ids.py`.
- **Code no scenario reaches:**
  - vulture is clean.
  - The guard at `workqueue.py:81` is reached only beside a non-work-item `w<n>.md` (F10).
  - The `as_it_was` step went with its scenario.
- **Code no line asks for:** none found.
  - `status --hook` is the Implementation note's mechanism.
  - The refusal outside a git repository and the rollback message are migration-tools r7 ("If `migrate` cannot make every change … exit with an error").
  - "upgraded to …" is a message's words.
  - "the work-item id … is already held by …" is r110.

## Coupling

The plugin depends on Claude Code's plugin contract:

- **What it relies on:** `hooks/hooks.json` found by convention, `${CLAUDE_PLUGIN_ROOT}` expanded in a command hook, and a SessionStart hook's stdout added to the session's context. All of it is published.
- **Verified:** this session's own start showed the installed 0.24.0 plugin's hook text ("This repository is on plugin version 0.23.1 … Offer the person the upgrade …").
- **No `matcher`:** the hook runs on every SessionStart source (startup, resume, clear, compact), so a resumed or compacted session is told the offer again. It is within the contract and stable. A `"matcher": "startup"` would limit it if that is wanted.
- **`python3` on PATH:** the hook needs it. The plugin's other commands assume the same.

## Observations

- **The deprecated scenarios will stay forever as things stand.** Both scenarios that `features deprecated` lists (migration-tools @r15 old, work-queue @r1 old) have built, withdrawn replacements, and no work-item will retire them. Reproduction: `python3 <Scripts>/features deprecated`, which printed the two lines in Checks.
- **Every branch review of this repository fails its supervision scenarios.** `tests/scenarios/test_supervision.py` fails whenever `SHOPSYSTEM_WORK_RUN_WORKER` is set, and `work run` sets it for the branch reviewer (`supervise_worker.py:69`). This is not new on this branch. The fixtures that start `work run` should drop the marker from the environment they pass. Reproduction: the suite line above, where all 105 failures carry "a worker starts no delivery".
- **Until this repository runs the upgrade, `model check` fails it on r110.** On the clone it printed 131 problems before the upgrade and 43 after, so about 88 are r110's "a work-item's file is named w<n>.md". This is expected until the upgrade, which F2 blocks.
- F4, F5, F6, F7, F8, F9, F10, F11: reproductions above.
- The probes ran from `.shop/scratch/i21-work-item-ids-and-upgrades-branch-review/` and on pytest `tmp_path` repositories. That directory has been deleted.
