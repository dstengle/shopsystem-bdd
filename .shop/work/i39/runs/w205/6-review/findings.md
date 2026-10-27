# Review of w205: `work list` and `work show <target>` (work-queue r34-r39)

**Verdict: DONE_WITH_CONCERNS.** One finding is triaged fix now: `work show <name>` reports a request, a capability-proposal or an initiative's own `initiative.md` as a work-item and exits 0 (F1). Otherwise the commit does what r34-r39 and the ruling (reading A) ask. No test was removed or weakened, and nothing under `features/` was changed.

## Commits reviewed

- The branch `work/w205` no longer exists, so the commits were taken from the checkout: those between `884f6bdd work: w205 ready -> claimed` and `04708be8 work: w205 claimed -> done`, leaving out `work run`'s own `work:` commits.
- That is one commit, **a033c460** "work list and work show <target> (work-queue r34-r39)". It touches 7 files (+178/-11): CLAUDE.md, scripts/work, scripts/workqueue_list.py (new), tests/scenarios/test_work_queue.py, tests/scenarios/work_queue_list_steps.py (new), tests/scenarios/work_queue_status_steps.py and tests/scenarios/work_queue_withdraw_steps.py.
- The implementer's result lists **bc517d85**, with the same subject. a033c460 is that commit rebased onto main: `git diff --stat bc517d85 a033c460 -- <the 7 files>` is empty. There is no difference to report.
- `work_queue_withdraw_steps.py` is outside the work-item's fileset. The stage-4 report names it and gives the reason: its `it gives {triples}` step was ambiguous with the new `it gives` steps.

## Removed and weakened tests

None.

What I searched for: deleted test functions, dropped parametrize cases, removed or loosened asserts, added skip or xfail, and steps rewritten to check something else. The diff removes no `def test_`, `assert`, `skip` or `xfail`. Its changes to existing steps:

- `work_queue_status_steps.with_state`: the parse step became a regex, and the `" and whose work-item "` splitting became a `findall`. It also accepts `work-items` and a question clause. Every existing feature line it matches (work-queue.feature lines 28, 63, 81, 92, 449-452, 461) still writes the same files. It has no assert.
- `work_queue_status_steps.open_with_proposal`: the fixed text "neither done nor abandoned" became `{state}`. It has no assert. See F4: the `state` parameter is ignored.
- `work_queue_withdraw_steps.gives`: the step was narrowed to `it gives \S+ in \S+ with .+`. Its body and assert are unchanged. Of the `it gives` lines in work-queue.feature, the only one it served before still matches it (line 194, r11). The step is loaded only by test_work_queue.py.

## Allowances

- Stage-4 report: "none". It says step definitions were respelled or widened without changing an assert, and that holds (above).
- Stage-5 report: "none beyond what bc517d85 already holds (setup in work_queue_status_steps.py and work_queue_withdraw_steps.py)". Taken as `setup` rows, both hold: neither file's diff adds, removes or changes an `assert`, an expected value or a parametrize case.

## Cannot verify

- The whole suite on main's head after the hand restoration of the requests scenarios (2ae8e313). I did not run the whole suite (not my job here), and the stage-5 report says the same thing is unconfirmed.
- The reports' run counts (151 passed under `--work-item w205`). I did not run them again.

## Findings

### F1. Important, fix now: `work show <name>` reports a request, a proposal or `initiative.md` as a work-item

- **Where:** scripts/workqueue_list.py:58-60 (`work_item`) and :74 (`show`).
- **What is wrong:** any target that is not an initiative goes to `workqueue.find`, which globs `.shop/work/*/<name>.md`. That glob also matches `.shop/work/requests/q1.md`, a capability-proposal `.shop/work/i1/p1.md`, and, when there is exactly one initiative, `.shop/work/i1/initiative.md`. Nothing checks the file's `kind`, so each is printed as a work-item and the command exits 0.
- **Reproduction:** a scratch repository under `.shop/scratch/w205-6-review/probe` with i1, a proposal p1 and a request q1, driven by `.shop/scratch/w205-6-review/test_probe.py`:
  - `show q1` → `work-item requests/q1 accepted`, exit 0
  - `show p1` → `work-item i1/p1 approved`, exit 0
  - `show initiative` → `work-item i1/initiative started`, exit 0
  - `show zz` → refused, "there is no work-item zz under .shop/work"
- **Why it matters:** these are wrong answers. r37 shows a work-item, and r7 says that what `work` cannot do is refused. `work show q1` is not an edge case: decision 0072 names `work show <id>` of a request as part of the person's surface, and the ledger carries r48 (`work show <request>`) as coming work. Until then a person typing it gets a request presented as a work-item of an initiative called "requests".
- **Fix:** in `work_item`, refuse under r7 when the file found has a frontmatter `kind` other than `work-item`, naming the target. That covers requests/, proposals and initiative.md. r48's later work-item can then add the request's detail.

### F2. Minor, observation: a malformed `raised.jsonl` line crashes `work list` with a traceback

- **Where:** scripts/workqueue_list.py:31-32 (`waiting`).
- **What is wrong:** `json.loads(line)` and the `found["upstream"]`, `found["request"]` and `found["status"]` lookups are not guarded. With a line lacking `status`, the probe gives `initiative i1 started` and then an uncaught `KeyError: 'status'`. A line that is not JSON would raise `JSONDecodeError` in the same way.
- **Why it is only an observation:** no command writes `raised.jsonl` yet (plan §5 and both reports name this), so no client sends this input today. Under r7 the right answer is a refusal naming the file and line.
- **Fix:** catch `ValueError` and `KeyError` there and raise `Refused("<path> line <n> is not a raised request")`.

### F3. Minor, observation: `work list --json` does not carry r39's waiting

- **Where:** scripts/workqueue_list.py:40-43.
- **What is wrong:** r39 says `work list` prints the waiting initiative, and r35 gives `--json`. The JSON object has no waiting entry. The r35 scenario says "and nothing besides", and r39's scenario runs text only, so the lines leave this open. The plan named it as an open case and stage 4's report says "not carried".
- **Fix:** a question for the next integrate round (r39 under `--json`), not a code change now.

### F4. Minor, observation: `open_with_proposal` takes `{state}` and ignores it

- **Where:** tests/scenarios/work_queue_status_steps.py:14-19.
- **What is wrong:** the Given now matches any state, but `initiative()` (test_work_queue.py:48-51) always writes `status: started`. Today this is harmless, because only "started" and "neither done nor abandoned" are used, and both mean started. A later scenario saying "that is done, whose capability-proposal ..." would silently set up a started initiative.
- **Fix:** write `state` into initiative.md, as `with_state` does with its `.replace("neither done nor abandoned", "started")`.

### F5. Minor, drop: lint findings the commit introduces

- scripts/workqueue_list.py:13: F401, `Refused` imported but unused.
- tests/scenarios/work_queue_list_steps.py:79: RUF015, prefer `next(...)` over `[...][0]`.
- These are cheap, but they are polish. If F1's fix uses `Refused`, the F401 goes away with it.

## Check headings (`tools check --base 884f6bdd`)

- **ruff:** 3 errors. F401 at workqueue_list.py:13 and RUF015 at work_queue_list_steps.py:79 are introduced by the commit (F5). The I001 at test_work_queue.py:7 was already there: the out-of-order `work_queue_start_steps` import exists at base.
- **vulture:** 2 hits, test_work_queue.py:236 `name2` and work_queue_status_steps.py:77 `notes`. Both exist at base (`git show 884f6bdd:...`), so neither comes from this commit.
- **import-linter:** the project states no import contracts.
- **size (`--limit 300`):** no file is over the limit.

## Behaviour against the lines

- **r34:** `list` prints every initiative (ended ones included), every request and every work-item. Holds.
- **r35:** `list --json` prints one object with the three kinds. Holds (see F3).
- **r39:** `list` reads only `.shop/work/<i>/raised.jsonl` and prints a waiting line for each request whose last status is not `delivered`. This is reading A as ruled. The upstream is never reached. Holds.
- **r36:** `show <initiative>` uses `workqueue_status.status` unchanged. Holds.
- **r37 and r38:** these hold for a real work-item. F1 covers the non-work-item targets.

No code was found that no line asks for. The waiting line's `(in ctx-up, accepted)` and the `question:` lines serve r39 and r37.

## Commands run

- `git log --format=%H -1 --grep="^work: w205 ready -> claimed$" work/w205` → fails (the branch is gone)
- `git log --format='%h %s' -15`
- `git log --format='%H %s' --grep="^work: w205 "`
- `git log --stat 884f6bdd..04708be8`
- `git show --stat bc517d85`
- `git diff 884f6bdd a033c460`
- `git diff --stat bc517d85 a033c460 -- <7 files>` → empty
- `grep` of capability lines, of feature steps, and of `workqueue.find`, `entry` and `read`
- `git show 884f6bdd:tests/scenarios/work_queue_status_steps.py` and `git show 884f6bdd:tests/scenarios/test_work_queue.py`, to check whether the lint hits were already there
- `python3 -m pytest -s -q -p no:cacheprovider -c /dev/null --rootdir .shop/scratch/w205-6-review .shop/scratch/w205-6-review/test_probe.py` → the probe output quoted in F1 and F2
- `python3 /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts/tools check --base 884f6bdd...`
- `python3 /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts/tools size --limit 300`
