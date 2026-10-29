# Plan of w236 (supervision#r218)

## 1. What goes green

- **supervision#r218**: "a change to .shop/work/ in the repository's own checkout, less another initiative's path run side by side, that is not committed when a worker ends is put back, and the work-item's transition is to failed, naming the file" (features/supervision.feature:2021).
  Red today, from the notes:
  - its Given at :2025 (i1's researcher at work while another session changes `.shop/work/i1/initiative.md` and a session of i2 changes `.shop/work/i2/initiative.md`, neither committed) has no step definition (`StepDefinitionNotFoundError`, run);
  - its last Then, "nothing recorded of w1 names .shop/work/i2/initiative.md", has no step definition (search);
  - behind them, `Faults.checkout_changes` in scripts/supervise_faults.py leaves out only the group's own run directories and log tails, so i2's path would be put back and named in w1's fault, and the last Then would fail (read).
- Retired scenarios: none. The work-item has no Retires section. The `@deprecated` r28 scenario (:570) stays and still passes (notes §3).

## 2. Where the change lands

- `scripts/supervise_faults.py`: `checkout_changes` also leaves out each path under the initiative directory of every other run in the group (runs side by side). Such a path is not put back, and it is not in the list it returns. Its docstring cites r218 and r214 in place of the retired r28.
- `tests/scenarios/supervision_faults_steps.py`: the new Given at :2025 and the new Then "nothing recorded of {name} names {path}".

Taken out of the researcher's set:
- `scripts/supervise_worker.py`: `Run.worker` already builds its Fault from the list `checkout_changes` returns. Once i2's path is left out of that list, the fault names only i1's files, so the file needs no change.
- `scripts/supervise.py`: every run already has its initiative directory (`self.dir`, line 51) and the shared `self.group` (line 65), so nothing needs passing in. The file also has only 5 lines of room left.

## 3. Decisions

1. **What counts as "another initiative that work run is running side by side".** It is every run in the `group` other than the run whose worker ended, and the path left out is the part under that run's initiative directory, `.shop/work/<initiative>/`. This rests on supervision#r214 and #r218: the requirements define the part by initiative and by being run side by side, and the group is how `work run` with no initiative takes initiatives together (supervise_all). A single-initiative run has a group of one, so it leaves nothing extra out.
2. **The exclusion applies whoever made the change.** A path is left out because of where it is, not because of which session wrote it. r218 words the exclusion by path ("less each path under ..."); the "by a session of that initiative" condition belongs to r215/r216, which this work-item does not accept. `work run` cannot see who wrote a file, so a path test is the only reading available. In the scenario's fake, i1's researcher worker writes the i2 file; that is the test's double for "a session of i2".
3. **A left-out path is neither put back nor named.** It is skipped before the put-back and the returned list, the same way own run directories are skipped today (r218 "less ...", r214 "leave out").
4. **The new Given** sets every worker to DONE and has the code-scout's "elsewhere" write both files in the main checkout, the way `another_session_changes` (supervision_faults_steps.py:42) does for one file. The i2 text is its committed text plus an added line, as supervision_given.py:172 does, so that i2's run can still read its initiative fields. "Every round ends" is already set for the group by the steps before it (supervision_all_steps.py). Rests on r218's scenario.
5. **The new Then "nothing recorded of w1 names <path>"** checks that the path appears nowhere in w1's work-item file (its `## Faults` included) and in no line of i1's log.jsonl that names w1. Rests on r218: "naming only the files of that part". The existing Thens at :2027 (supervision_faults_steps.py:103) and :2028 (`is_failed`, :86) already match and are kept as they are.

## 4. Tests the decisions break

None. Verified from the notes (§3) and by reading the steps:
- `another_session_changes` (supervision_faults_steps.py:42) drives a single-initiative run whose group is itself, so i1's path is still put back and named.
- supervision_given.py:167 and the test at test_supervision.py:158 commit i2's change, so `git status` shows nothing for that path, before and after.
- The r28 deprecated scenario (:570) asserts only i1's path.

No test in tests/ asserts that another initiative's uncommitted path is put back.

## 5. Open cases (for the implementer to name, not to choose)

- **i2's own check.** When one of i2's sessions ends while `.shop/work/i2/initiative.md` is still changed (written here by i1's worker), i2's own `checkout_changes` treats it as i2's own path, puts it back and may fault p2. The r218 scenario's Thens hold either way. The behaviour belongs to r215/r216 (:2002, :2011), which w236 does not accept. Name what happens; do not change it here.
- **Order of i1's and i2's checks.** If i2's run puts the file back before i1's researcher ends, i1 never sees the path. Both orders satisfy the scenario.
- **Later commits by i1's run.** If a later commit of i1's run (`keep_round`, the item's commit) stages paths broadly under `.shop/work/`, it could take in i2's uncommitted change. The notes read these commits as path-level; name it if a run shows otherwise.
- **Renames.** A rename porcelain line (`old -> new`) under another initiative's directory: `checkout_changes` reads `line[3:]` as one path. Name it if it comes up.
