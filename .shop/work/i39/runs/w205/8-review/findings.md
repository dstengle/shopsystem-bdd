# Review of w205 (round 8): the fix of review F1

**Verdict: DONE.** No finding is Critical, and none is triaged fix now. The one code commit does what the 2026-10-27 ruling on F1 asks: `work show <name>` now refuses a request, a capability-proposal or `initiative.md`, naming its kind, where it used to print each of them as a work-item. Nothing under `features/` changed, and no test was removed or weakened.

## Commits reviewed

- The branch `work/w205` is gone (`git log ... work/w205` gives "unknown revision"). So the commits were taken from the checkout: those between the last `1508cd06 work: w205 ready -> claimed` and `1b9a3c40 work: w205 claimed -> done`, leaving out `work run`'s own `work:` commits.
- That is one commit, **bf231ddc** "work show refuses a file that is not a work-item, naming its kind (review F1)". It changes scripts/workqueue_list.py by +4/-1.
- The implementer's result lists exactly `bf231ddc`, so the commits match.
- The file is in the work-item's fileset.
- The earlier work (a033c460, r34-r39) was reviewed in round 6 (6-review/findings.md) and is not reviewed again here.

## Removed and weakened tests

None. The commit touches no test file.

What I searched for: any test file, `def test_`, `assert`, parametrize, skip or xfail in `git show bf231ddc`. Only scripts/workqueue_list.py appears.

## Allowances

The 7-implement report's `## Tests changed under an allowance` is "none". That holds: no test changed.

## Cannot verify

- The report's run count (`--work-item w205`: 151 passed, 1 skipped). I did not run it again, because `work run` runs the suite.

## Findings

### F1. Minor, observation: the new refusal is covered by no scenario

- **Where:** scripts/workqueue_list.py:59-61.
- **What is wrong:** no scenario drives `work show q1`, `work show p1` or `work show initiative`, so nothing stops the refusal from regressing. The report says the same.
- **The line it serves:** the refusal serves r37 (show a work-item) and r7 (refuse what `work` cannot do), as the ruling asks. So this is not code that no line asks for.
- **Reproduction:** `.shop/scratch/w205-8-review/test_probe.py`, run with pytest. It gives:
  - `q1` → refused: `q1 is a request, not a work-item or an initiative that work show shows`
  - `p1` → refused: `p1 is a capability-proposal, ...`
  - `initiative` → refused: `initiative is a initiative, ...`
  - `w1` → exit 0: `work-item i1/w1 ready`
  - `zz` → refused: `there is no work-item zz under .shop/work`
- **Exit status:** scripts/work:175 catches `workqueue.Refused`, so the command exits with an error.
- **Fix:** a scenario under r37/r7 in the next formulate round, or r48's work-item (`work show <request>`) when it comes.

### F2. Minor, drop: the refusal's wording reads oddly for two kinds

- **Where:** scripts/workqueue_list.py:61.
- **What is wrong:**
  - For `initiative.md` the message reads "initiative is a initiative".
  - For a file with no `kind` it reads "w2 is a None". Probe: a work-item file without `kind` gives `w2 is a None, not a work-item ...`. No such file exists in the repository: `grep -L "^kind:" .shop/work/*/w*.md` printed nothing, and every test fixture writes `kind`.
- **Why it is only polish:** the refusal and its exit status are right in both cases.

## Risks verified outside the diff

- **Whether every real work-item carries `kind: work-item`.** If one did not, the fix would refuse a real work-item. `grep -L "^kind:" .shop/work/*/w*.md` printed nothing, and the fixtures (test_work_queue.py:37, :148) write `kind`. The risk does not arise.
- **Whether a `Refused` from `show` becomes an error exit.** It does: scripts/work:175 catches `workqueue.Refused`.

## Check headings (`tools check --base 1508cd06`)

- **ruff:** all checks passed. The F401 from round 6 is gone, because `Refused` is now used.
- **vulture:** clean.
- **import-linter:** the project states no import contracts.
- **size (`--limit 300`):** printed nothing; no file is over the limit.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w205 ready -> claimed$" work/w205` → unknown revision (the branch is gone)
- `git log --format='%H %s' --grep=w205 HEAD`
- `git log --stat 1508cd06..1b9a3c40`
- `git show bf231ddc`
- `cat -n scripts/workqueue_list.py`
- `grep -n Refused scripts/work`
- `grep -n "def find" -A15 scripts/workqueue.py`
- `grep` of r34-r39 and r7 in spec/capabilities/work-queue.md
- `grep -L "^kind:" .shop/work/*/w*.md`
- `grep -rn "kind:" tests/scenarios/test_work_queue.py tests/scenarios/work_queue_list_steps.py`
- `python3 .../scripts/tools check --base 1508cd06`
- `python3 .../scripts/tools size --limit 300`
- `python3 -m pytest -s -q -p no:cacheprovider -c /dev/null --rootdir .shop/scratch/w205-8-review .shop/scratch/w205-8-review/test_probe.py`
