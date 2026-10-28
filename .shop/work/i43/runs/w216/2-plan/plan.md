# Plan of w216 (supervision r154-r157)

Planned from `.shop/work/i43/runs/w216/1-research/notes.md`. Where I read code or tests beyond the notes, I name them in the decision that needed them.

## 1. What goes green

All ten scenarios are red today for the same reason: pytest-bdd stops at the first Given, which no step definition matches (notes §1, `python3 -m pytest -q --work-item w216`: 10 failed). Behind the steps, there is no code at all for these requirements. `branch_review` starts the reviewer as soon as push verification passes. It runs nothing first, and its brief has only Head, Base, Worktree and Run directory.

- **supervision#r154**, Outline "before the branch review starts, <run> is run at the initiative branch's head", 7 examples: the whole suite, w1's scenarios, w2's check `python3 -c pass`, `tools check`, `tools size`, `features deprecated`, `features bindings`. Red: the Given that names a work-item's check is undefined. Also, no code reads a work-item's `check:`, and none makes any of these runs for the branch.
- **supervision#r155**, "the branch reviewer is given each run made before it, with its command, how it exited and its output, and the commit they ran at". Red: undefined Given. The brief has no runs.
- **supervision#r156**, "the branch reviewer is given the commits from the initiative branch's base to its head, each with the work-item it belongs to or none, and the change of that range less .shop/". Red: undefined Given (the implementer's commit plus the concurrent notes.txt commit). Nothing attributes commits to work-items.
- **supervision#r157**, "the branch reviewer is given as files to read the work-items' capabilities, the design-decisions they rest on, and each work-item's plan, report and review findings". Red: undefined Given (under thing/other with rests_on). The brief has no `Read:` list.

The work-item has no Retires section, so it retires no deprecated scenario.

## 2. Where the change lands

- `scripts/supervise_review.py`: `branch_review` makes the r154 runs once push verification has passed and before it writes the brief. The brief then gives the runs (r155), the commits and the change (r156) and the files to read (r157). `unread` is unchanged.
- `scripts/supervise_branch_runs.py` (new): the r154 runs in the review's worktree, each recorded as its command, exit code and output, together with the commit they ran at.
- `scripts/supervise_review_read.py` (new): what the brief gives to read. This covers the commits from base to head, each with its work-item or none, the change of that range less `.shop/`, and the files to read.
- `agents/bdd-branch-reviewer.md`: the brief now gives the runs, the commits with their work-items, the change and the `Read:` list. The reviewer reads these instead of running or deriving them. "What you run" becomes "what you are given", and "The branch" drops the derivation of commits from `work:` subjects.
- `CLAUDE.md`: one module-map row for each new module.
- `tests/scenarios/supervision_branch_steps.py` (new): the Givens and Thens of r154-r157.
- `tests/scenarios/test_supervision.py`: one import line for the new step module, like the other step modules.
- `tests/scenarios/supervision_world.py`: `item_text` can write a work-item's `check:`.

Removed from the researcher's set, because the decisions below change nothing in them:
- `scripts/supervise.py`: the call sites of `branch_review` keep their form.
- `scripts/supervise_merge.py`: `tests()` and the `merged` log line are read as they are.
- `scripts/supervise_worker.py`: the reviewer's tools stay as they are. Narrowing its Bash is q24/i44, not this item.
- `tests/scenarios/supervision_given.py`: the new Givens go in the new module. None of them is matched by the work-items regex at its line 54, because their text has commas and backticks that its `items` group cannot take.

If any of these turns out to need a change, `work claim` claims it.

## 3. Decisions

1. **Order.** The push is verified first, as today. Only then are the runs made, then the brief written, then the session started. If the push verification fails, nothing is run. Rests on r51 and r35, and on r154's "first". The runs are work run's own and take no session slot (r60 counts sessions).
2. **Where and at what commit.** The runs are made in the branch review's own detached worktree, which is at the commit the brief gives as `Head:`. The brief names that commit as the one the runs ran at, under a label other than `Head:`. Rests on r154, r155, and r27/r50: `unread` reads every brief line that begins `Head:`.
3. **The whole suite.** This is the suite command as supervision's Implementation section gives it: `tests(name)["suite"]`, so `.shop/delivery.toml`'s `[tests]` is honoured. It is given the name of one work-item of the initiative, the first by name. By r27 every work-item is `green` or `withdrawn` when the review starts, so the expected-red set of r43/r122 is the same whichever one is named. The reviewer reads the same record a merge's suite line gives. Rests on r154, r43, r122 and the Implementation line for the suite command. This is research conflict C2, reading B. Under it the narrator sees the suite counted as everywhere else in `work run`. A bare pytest run instead would show other initiatives' parked scenarios (w212's) as failures.
4. **Each work-item's scenarios.** Every work-item of the initiative, whatever its status, each with `tests(name)["work_item"]`. Rests on r154's "each work-item".
5. **Each check a work-item names.** This is the `check:` field of a work-item's frontmatter (design-decision/work-file-forms names `check` among a work-item's fields). It is one command line, split and run like work run's own test commands, with no shell. A work-item with no `check:` has none. Rests on r154.
6. **`tools check`** is run with `--base <Base>`, the initiative branch's base that the brief gives. `tools size` is run with its own default limit. `features deprecated` and `features bindings` are run bare. All of them are run from the plugin's `Scripts` directory with the project's `python3`. Rests on r154 and r156's range from base to head. This is research conflict C3, reading A.
7. **What a run gives (r155).** Each run has its own part of the brief: its command, its exit code (Implementation line "r155: how a run exited is given as its exit code") and its whole output. A run that fails is given like any other. The environment is `with_scripts()` with no worker variable, so `--whole-suite` is allowed (work_items.py's `pytest_configure`).
8. **No line of a run's output, the commit list or the diff begins at column zero.** Each is indented in the brief, so `Head:` stays the only brief line that `unread` and the retire steps' `^Head:` read. Rests on r27 and r50. `unread` itself is kept unchanged.
9. **Commit attribution (r156)** comes from what `work run` records, not from a range of subjects. This is research conflict C1, reading A.
   - A commit is w1's when either of these holds:
     - it is among the `commits` of a log.jsonl `merged` line of w1. The merge is fast-forward (design-decision/the-file-set-is-the-claim), so these commits are "the merge of work/w1".
     - its subject is a transition `work: w1 <before> -> <after>`.
   - Every other commit from base to head is given with none.
   - Reading B is ruled out by the r156 scenario itself. It takes in the commits between w1's transitions, and that would wrongly attribute the concurrent notes.txt commit to w1.
   - The log read is the initiative's log.jsonl at the head.
10. **The change less `.shop/`** is the diff from Base to head with every path under `.shop/` excluded. It is given in the brief (r156; the scenario reads it there).
11. **Files to read (r157)** are one `Read:` list in the brief:
    - `spec/capabilities/<under>.md` for each distinct `under:` of the initiative's work-items.
    - Each design-decision those capabilities' `rests_on` name, given by its id as `rests_on` gives it. This needs no mapping to `spec/decisions/` paths (design-decision/references-are-ids).
    - Each `plan.md`, `report.md` and `findings.md` found in each work-item's kept stage directories under `runs/<work-item>/`, every attempt, in stage order, as repository-relative paths.

    Rests on r157.
12. **No new log.jsonl event.** The runs are evidenced by the brief, which is written before the session starts. Nothing new is stored where the narrator reads. This keeps `verified_before_all` sound (decision 4 of the notes §3 constraint). Rests on r49, which names the review's own log lines.
13. **The reviewer's agent prompt** is changed to read the runs, the attribution and the `Read:` list from the brief, and not to run the suite, the scenarios, the checks, `tools` or `features` again. Rests on r155 ("without running any of them again", the scenario's pin) and design-decision/the-v3-agents (the role's instructions live in its definition).

## 4. Tests the decisions break

None. I checked the notes' list (§3) against each decision:

- `tests/scenarios/supervision_review_steps.py` `verified_before_all` counts `start` lines. Decision 12 adds no log line. Sound.
- `tests/scenarios/supervision_retire_steps.py` (`^Head:` regex) and `tests/scripts/test_supervise_review_due.py` (`unread`, `unread_mine`). Decision 8 keeps `Head:` the only column-zero `Head:` line, and `unread` is unchanged. Sound.
- `tests/scripts/test_agents.py` asserts only the reviewer's frontmatter tools and model. Decision 13 changes the body only. Sound.
- `tests/scenarios/supervision_then_workers.py` and `supervision_analysis_steps.py`: the order of the reviewer's start and the brief's mtime are unchanged, because the runs come before the brief is written. Sound.
- `tests/scripts/test_work_items_worker.py`: work run's own runs set no worker variable. Sound.

Every existing scenario that reaches a branch review now also makes the r154 runs in its fixture repository. They assert nothing about them, but they take longer. The implementer should note the suite's wall time before and after.

## 5. Open cases

These are cases the scenarios are silent about. The implementer names how the code meets each one; the plan does not choose.

- A run that cannot start at all (command not found, OSError): how it is given in the brief.
- A very long run output or diff: the plan gives it whole. Any bound would be a later line.
- The initiative has no base (`self.base()` gives none): what `tools check` gets, and the range the commits and the change are read from.
- A `check:` that needs a shell (pipes, `&&`), or whose quoting the frontmatter reader changes. The r155 scenario's check has double quotes inside it.
- A work-item with several attempts of a stage: decision 11 lists every attempt's file.
- A CLAUDE.md that gives a size limit other than `tools size`'s default.
- A commit that is both among a `merged` line's commits and named by another work-item's transition. This should not occur, because transitions are work run's own commits.
- `tools check` may be red at head in this repository (ruff errors noted in the ledger, notes C4). Under r155 it is given as red, not hidden.
