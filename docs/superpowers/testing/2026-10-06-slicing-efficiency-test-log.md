# Test log: slicing takes the suite record, cuts the fast suite first, probes dependencies, edits through the scripts

Headless runs: cwd the fixture, `claude -p --model opus --plugin-dir <this checkout>`, superpowers from the installed marketplace, stream-json transcripts, `$SCRATCH/fixtures/stock/bin` first on `PATH`. No run read a file of this repository outside `skills/`, `agents/` and `scripts/`.

Fixtures (scratchpad only):
- `stock`: a dependency. `spec/capabilities/stock-levels.md` with the Behaviour line "When a client runs `stock reserve <sku> <n>`, the stock level falls by n and the reservation is listed." and under Not yet "`stock reserve`: specified, not built. Promoted when a shop reserves stock." (also `receive` and `reservations` not built). `bin/stock` answers `stock level <sku>` with `5` and anything else with `stock: unknown command`, exit 2.
- `slice`: the cart example. `spec/` with `index.md`, `decisions.md` (the ledger), `cart.md`, and an approved `reserve-at-checkout.md` ("When the customer checks out, each line's quantity is reserved in stock and the checkout is confirmed." and its refusal). `features/reserve-at-checkout.feature` with two untagged scenarios, "Checking out reserves each line in stock" and "Checking out more than stock holds", whose Givens say "stock holds N". `CLAUDE.md` says "Depends on stock (../stock), installed on PATH as `stock`." and nothing about speed. `tests/conftest.py`'s `pytest_sessionstart` sleeps 65 s; `pytest.ini` has no `-n`. The plan has slices 1–2 green; after the commit `19a20f5` the suite was run and recorded with `plan log`, then committed: `Suite: 2 passed, 2 failed at 19a20f5 in 65 s; failing: Checking out reserves each line in stock, Checking out more than stock holds`. `plan show --last-suite --current` says `current`.

Prompt: "The reserve-at-checkout features are approved. Slice them and plan the batch." When a run stopped at a question, it was resumed with "Go ahead as the workflow says."

## Discarded run

The first baseline's fixture was copied with `tests/__pycache__` compiled in the pristine copy, so pytest-bdd read the pristine copy's feature files and the new tags did not select. The run spent its time on that (7 whole-suite runs, a pytest-bdd source dive) and git had no identity in the fixture. Discarded as a fixture fault; the fixture was rebuilt without `__pycache__` and with a local git identity. What it showed before the fault matches the clean baseline: a whole run despite the record, plan and tags edited by a Python heredoc, the dependency read by `cat bin/stock`, no fast-suite slice.

## Baseline (RED)

First turn, then resumed once.

- **Suite run although the record holds.** `git diff --stat 19a20f5 HEAD; timeout 300 python -m pytest -q 2>&1 | tail -15`: the diff showed only the plan, and it ran anyway (whole-suite runs 1, 65 s). It then wrote a second record by hand, `Suite: 2 passed, 2 failed at 927da3c; failing: ...`, with no time and the plan commit's hash. RED.
- **Fast-suite enabling slice.** None. The 65 s went unremarked. RED.
- **Probe.** Already present: `stock receive Widget 5; echo "exit $?"; stock reserve Widget 2; ...` -> `stock: unknown command`, `exit 2`. The dependency's spec read whole (`cat CLAUDE.md spec/capabilities/*.md`). Logged as prose ("BLOCKED on a dependency: ... `stock receive` and `stock reserve` exit 2"), no `Probe:` line, no `REQUEST stock:` line; the stock work was cut as this repository's enabling slice 3, `blocked: the installed stock answers level only`.
- **Reserve slices planned as buildable.** First turn: slices 4 and 5 `blocked: on slice 3`. Resumed: writing-plans wrote a task for each blocked slice, Task 1 being stock's own work ("get `stock receive` and `stock reserve` working ... runs through stock's own workflow"), and logged "execution waits on slice 3". RED on the tasks.
- **Plan and tag edits.** Slices and log by `python - <<'EOF' ... s.replace('## Backlog\n',new,1) ... open(p,'w').write(s)`; tags by `sed -i 's/^  Scenario: Checking out reserves .../  @slice-4\n&/ ...' features/reserve-at-checkout.feature`; markers by `sed -i` on `pytest.ini`; a log line by `echo "- 2026-10-07 Tasks for slices 3-5 ..." >> docs/superpowers/plans/cart-slices.md`. Counts by `python -m pytest --collect-only -q -m slice-4` and `-m slice-5` (65 s each). RED.
- **writing-plans plan.** Global Constraints: "Each task's red-green runs `python -m pytest -q -m slice-N`. Run the whole suite (`python -m pytest -q`) once before the slice's last commit." Each task's steps: "Run `python -m pytest -q`. Expect 3 passed, 1 failed". No code blocks. No `Scripts:`. RED on the run protocol and `Scripts:`.
- **Fresh session.** Not recommended: "Subagent-driven: a fresh agent implements each task ... I recommend this", offered against "Native: I implement the tasks myself in this session". RED.

## Edits

`skills/slicing-into-increments/SKILL.md`:
- Overview: the Scripts paragraph (`plan`, `features`, `--help` as contract).
- Step 1 "Take the suite's result": a `current` record is the run; otherwise run timed and record as bdd-red-green's suite record. "Check the suite is fast": over 60 s and serial, or the entry point started as a program in more than one test per command, with no reason in `CLAUDE.md`, gives an enabling slice `Check: the suite -> <N> passed, <M> failed, in under <bound> s`.
- Step 2 "Probe what a dependency provides": a probe at the installed version, `Probe:` logged; a failing probe blocks the slice `awaiting <project>` with a `REQUEST <project>:` line and no task; a spec read is not a probe, and is read whole.
- Step 3: the fast-suite slice first. Step 4: every plan edit through `plan`. Step 5: `features tag`, `features count --by-tag`.
- Hand-off: counts from `features count --by-tag`; the run-protocol bullet replaced by markers and expected counts only; `Scripts:` in Global Constraints; recommend a new session when writing-plans asks how to execute.
- The Plan File: the log template carries the record's form, `Probe:` and `REQUEST` lines; archiving is `plan archive <batch>`.
- Rationalizations, from the baseline and the spec's evidence: a fresh run while only the plan changed; the slow suite; the dependency's spec as proof; tasks written for blocked slices; executing from this session.
- Red Flags: no `Probe:` line; a capability read by section range; a task for a `blocked` slice; `sed`, a heredoc or `python -c` on the plan or a tag line; a plan task that says when to run the whole suite.

## Green run

**Iteration 1.** PASS on every criterion.
- No suite run: whole-suite runs 0, `--collect-only` calls 0. It ran `plan show --last-suite --current` in its first command; final message: "I didn't re-run the suite: the last recorded run (2 passed, 2 failed) still matches the code, since only the plan has changed since."
- Slice 3 is `A fast suite`, `Kind: enabling`, `Check: \`python -m pytest -q\` -> 2 passed, 2 failed, in under 10 s`.
- Probes logged with `plan log`: `Probe: stock reserve Widget 1 -> 'stock: unknown command', exit 2` (and `level`, `receive`, `reservations`); `REQUEST stock: promote \`stock reserve <sku> <n>\` (with its refusal over the level) and \`stock receive <sku> <n>\` from Not yet; ...`; slices 4 and 5 `blocked: awaiting stock`. The stock spec was read whole (`cat`).
- Every edit through the scripts, in one command: `plan log`, `plan add-slice 3/4/5`, `plan status 4 "blocked: awaiting stock"`, `features tag "Checking out reserves each line in stock" slice-4`, `features tag ... slice-5`, `features count --by-tag`, `plan check` -> `ok`. The feature diff is the two tag lines.
- writing-plans plan: one task, slice 3; Global Constraints `- Scripts: /home/vscode/shopsystem-bdd/scripts`; "Their tasks are written when stock ships." Verification lists each marker with its expected result, counts "from `features count --by-tag`", and no when-to-run. It first wrote "`plan log` a suite record with the new time" into the checkpoint and edited it out before committing. No code blocks, file contents, diffs or step-definition bodies.
- Final message: "I recommend running the plan from a new session that reads the plan file, so it doesn't carry this session's spec and slicing context."

**Fix round 1 (task review).** Two clauses amended, no headless re-run, by the controller's ruling: the green run already behaved as the corrected wording says.
- The fast-suite trigger now reads "over 60 s, and either the test command does not run in parallel or the step definitions start the entry point as a program in more than one test per command". Before, the second arm could be read without the bound. In the green run the slice was cut for a 65 s serial suite, which both readings cover.
- The hand-off's "why each scenario is red today" now takes "the suite's result from its record" and allows running only the red scenarios, not the suite. The green run's writing-plans phase ran no suite: it took the failures from the record.

## Not verified by a run

The archive paragraph (`plan archive`) and the slow-suite trigger's second arm (the entry point started as a program in more than one test per command) had no fixture here.
