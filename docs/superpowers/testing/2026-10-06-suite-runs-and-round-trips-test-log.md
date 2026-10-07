# Test log: suite runs count once, rule-decided splits, behaviour defects never Minor

Headless runs: cwd the fixture, `claude -p --model opus --plugin-dir <this checkout>`, superpowers from the installed marketplace, stream-json transcripts. No run read a file of this repository outside `skills/`, `agents/` and `scripts/`, so none was discarded.

Fixtures (scratchpad only):
- `impl`: the bdd-red-green example; `cart.md` with the receipt Behaviour line; slices 1–2 green, `@slice-3` "Asking for a receipt" red on undefined steps; `CLAUDE.md` with a module map (`cart/__init__.py`: the cart and its lines) and the rules "No module over 40 lines." and "A new concern gets a new module and a row in the module map."; `cart/__init__.py` at 38 lines; the plan's log holding `Suite: 2 passed, 1 failed at 52fb186 in 0.2 s; failing: Asking for a receipt`, committed after `52fb186`; a brief saying the change lands "in `cart/__init__.py`, beside the cart", with `Scripts:` in its Global Constraints.
- `impl-norecord`: `impl` without the record commit.
- `review`: the example plus the Behaviour line "When the shopper removes a product, the cart no longer holds it and still holds every other product it held." and one scenario (one pen, removed, cart empty); then a commit whose `Cart.remove` is `self.lines.popitem()`, whatever the name. The scenario passes. Brief, report ("Concerns: None") and review package under `.superpowers/review/`.

Prompts: `impl` "Dispatch the shopsystem-bdd:bdd-implementer agent with the brief .superpowers/briefs/task-3.md, report to .superpowers/reports/task-3.md, on branch main."; `review` "Dispatch the shopsystem-bdd:bdd-task-reviewer agent with the brief, report and package under .superpowers/review/."

Whole-suite runs are counted from the subagent's Bash calls (a pytest invocation with no `-m`, `-k`, node id, module path or `--collect-only`, judged per command segment). The headless controller's own verification runs are listed beside them: no text this change touches governs it.

## Baselines (RED)

**impl.** The implementer read the brief, then ran the whole suite in its first command (`...; wc -l cart/*.py; python -m pytest -q 2>&1 | tail -3`), never looking at the record, and stopped: "BLOCKED. Slice 3 isn't implemented and nothing is committed. ... `CLAUDE.md` also says a new concern gets a new module and a row in the module map. So the receipt probably belongs in a new `cart/receipt.py`, with a `CLAUDE.md` row. That contradicts the brief's \"where the change lands\". ... Please decide". Whole-suite runs 1, at the start; hand-back for size; 0 commits; no record. RED: a start run against a holding record, and a round trip for a split the rules decide.

**review.** The reviewer found the defect by a probe and graded it Critical: "`remove` calls `self.lines.popitem()`, which deletes the most recently added line, whatever `name` was passed." The missing coverage went as a separate Important: "Changing the feature file may be outside the brief's scope; if so, the controller should send it back to the plan, not leave it as an unrecorded gap." Not Minor, but not marked as a question for the spec, and no route for the line's scenario. RED on the marking; the grade already held.

## Edits

- `skills/bdd-red-green`: the whole-suite run before the last commit is the slice's suite record; new section "The Suite Record"; the check cycle's step 3 iterates on the touched modules and runs the whole suite once at the end; one rationalization row and one red flag (a start-of-slice run with a holding record), from the baseline's start run.
- `agents/bdd-implementer.md`: runs follow bdd-red-green, the task starts from `plan show --last-suite`; two commits, the change then the checkpoint with the record for the change's commit; the size-limit stop narrowed to "no rule in `CLAUDE.md` says where the code goes", with the rule-decided split made and named in the checkpoint; the record line in report and reply.
- `agents/bdd-task-reviewer.md`: the implementer's record is the run, checked against the change commit; behaviour contradicting a Behaviour line or Purpose is Important, marked `spec question` when no scenario covers it, never Minor.
- `agents/bdd-branch-reviewer.md`: one suite run at the batch's head with wall time and a record line for the controller; the fast-suite check (60 s); the behaviour-defect grade; a Suite record output section.

## Green runs

**Iteration 1.**
- impl: PASS. Subagent whole-suite runs 1 (after the code, before the commit). It ran `plan show --last-suite` in its first command and went straight to `-m slice-3`. Created `cart/receipt.py` (13 lines) and the row `` `cart/receipt.py` | the receipt: a cart's lines and total as text ``; checkpoint: "Surprised by: cart/__init__.py was at 38 of 40 lines, so per CLAUDE.md the receipt went in a new module cart/receipt.py (row added to the module map) ... not beside the cart as the brief said." Commits `793b55a Cart: a receipt listing each line and the total`, then `a4d8b9e Plan: slice 3 green, suite record at 793b55a` holding `Suite: 3 passed, 0 failed at 793b55a in 0.1 s`. `plan show --last-suite --current`: `current`. The controller re-ran the suite once to verify.
- impl-norecord: FAIL. `plan show --last-suite` printed nothing; the implementer went to `-m slice-3` and wrote step definitions with no start run. Subagent whole-suite runs 3, all after the code (one `-n auto` attempt failed for want of xdist and was repeated without it). The double negative "do not run the whole suite at the start unless there is none" did not bind.
- review: PASS. "Critical ... `remove` calls `self.lines.popitem()` ... `spec question`: no scenario covers line 11's \"still holds every other product it held\" part. The controller should add one alongside the fix", with a scenario sketched; the absent-product case Important, also `spec question`; "Minor: None." Graded Critical, above Important. It also flagged the report's record for naming no commit (the fixture's report predates the convention).

**Iteration 2.** `agents/bdd-implementer.md` adds, after the brief's sentence: "When it prints no record, there is none: run the whole suite once, before any step definition, and that is the task's starting state."
- impl-norecord: PASS. Subagent whole-suite runs 2: `time python -m pytest -q` in its third call, before `tests/conftest.py` was written; then once after the code. Two commits, record `Suite: 3 passed, 0 failed at 2e325bf in 0.2 s` naming the change commit; `current`.
- impl (re-run against the amended text): PASS. Subagent whole-suite runs 1; `cart/receipt.py`, a module-map row, the split in the checkpoint; `2915770` the change, `361ea68` the checkpoint with `Suite: 3 passed, 0 failed at 2915770 in 0.1 s`; `current`. The controller ran the suite twice to verify.

The Suite Record section was afterwards unwrapped to one line per paragraph, as the rest of the skill; no word changed.

## Not verified by a run

The branch reviewer's edits (one run at the head, the record line, the fast-suite check) had no fixture here; slicing's use of a holding record is Task 4's. The headless controller re-ran the suite after every implementer, a record holding: the controller's text is not in this plugin's agents.
