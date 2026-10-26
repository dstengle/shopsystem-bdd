# Branch review of i37: findings

**Verdict: DONE.** No finding is Critical, none is triaged fix now, and every check was run and verified. There are two Minor findings (both observations) and four observations, one of which (O1) predates the branch.

## Range

`94be81b4..55c51d79` (main, 40 commits). Work-items:

- **w197** (requests r7, r23, r24; Retires the deprecated requests @r7): code commit `9237a0f9`, between `b6815a57 ready -> claimed` and `5575df89 claimed -> done`.
- **w198** (retires seven deprecated scenarios under r123, part_of i33-supervision as r123 asks: "under the capability-proposal of the last-drafted work-item whose replacement it retires", i.e. w194): code commit `ac8ed00f`, between `c3474104` and `8c8cdee0`.

Other commits:

- `5cfc4c92 spec:` (apply round 2) and `5d08c1c3 features:` (formulate round 3) are work run's rounds of the capability-proposal i37-requests. The ledger names both hashes.
- The rest are `work:`, `work note`, `work answer` and `work add` commits. Seven of them are i36's (`f85f1f1e`, `93e9547c`, `e7234895`, `3a1791f4`, `7a6ee0a9`, `9a4146b8`, `c62021e9`, all under `.shop/work/i36/`), because the initiative branch is main.

No commit outside a work-item changes code.

## Suite

`Suite: 911 passed, 0 failed at 55c51d79 in 22.7 s` (1 skipped, 56 subtests passed; `python3 -m pytest -q`, wall time from `time`).

- It runs in parallel: `pytest.ini` has `addopts = -n auto` (xdist; 1942% CPU).
- It is not in-process: step definitions run `scripts/work` through `subprocess.run` (`tests/scenarios/conftest.py:34`).
- It is under 60 s, so no finding.
- Count check: 926 at `c3474104` (w198's start), minus w198's 15 generated cases, gives 911.

## Checks

- **w197, its scenarios** (`pytest --work-item w197`): 148 passed, 1 skipped. `tests/scenarios/test_requests.py` together with `tests/scripts/test_bound.py`: 32 passed.
- **w198, its scenarios** (`pytest --work-item w198`): 153 passed, 1 skipped. `test_bound.py` passes (it is in the run above). w198's implementer did not run the whole suite; I did (above).
- **`tools check --base 94be81b4`**: exits 1.
  - `== ruff ==` reports 3 errors:
    - `.shop/work/i37/runs/requests/1-gate/mk.py:1` I001 and `:16` SIM115. This is new on the branch (F2).
    - `tests/scenarios/test_work_queue.py:7` I001. This was already there at base: `tools check` on the base revision of the file reports the same I001.
  - `== vulture ==` reports `tests/scenarios/test_work_queue.py:235: unused variable 'name2' (100% confidence)`. This is new on the branch: the base revision of the file is clean (F1).
  - `== import-linter ==` says "the project states no import contracts". Nothing is checked under that heading. I read the touched imports myself: no import was added on the branch.
- **`tools size --limit 300`** (the limit in CLAUDE.md): printed nothing and exited 0. No file is over, touched or not.
- **`features deprecated`**: `none deprecated`.
- **`features bindings`**: `every binding names a scenario`.
- **Randomized test of dry-run against real mode**: does not apply. No operation the branch touches (`work turn`, `work resolve`) has a dry-run mode.

## Removed and weakened tests

I searched the diff of `tests/` and `features/` for:

- deleted `def test_`, `@scenario`, step functions and parametrize or Examples rows;
- removed or loosened `assert`;
- added `skip` or `xfail`.

What I found:

- **w197**: `test_turn_passes_the_requests_turn_from_the_side_to_the_other_side_deprecated[upstream-asker]` and `[asker-upstream]`. These are generated from the retired deprecated @r7 scenario, which proved that `turn` passes the turn whichever side has it. The live @r7 Outline (both Examples, plus "status is not accepted") still proves it. The plan lists them in §4.
- **w197**: the `status_is` step in `tests/scenarios/requests_steps.py:70` was rewritten. For the words "not accepted" it now asserts `actual != "accepted"`; every other word is still compared for exact equality. No existing use is loosened. The plan lists it in §4 (decision 4).
- **w198**: 15 generated cases from seven retired deprecated scenarios, all on w198's Retires list and in plan §4 / D0. Each replacement exists with its `@r<n>` tag (I ran `features deprecated` on the base files) and passes in the suite at HEAD:
  - supervision @r75 (1): `measure initiative` is run after a kept review. Replaced by the @r75 Outline.
  - supervision @r102 (1): an integrate round is given the other initiatives' draft ids. Replaced by the live @r102, same title.
  - supervision @r105 (1): set done. Replaced by the @r105 Outline.
  - migration-tools @r15 (3): `migrate run` refuses on a dirty tree. Replaced by the @r15 `<command>` Outline.
  - work-queue @r1 (1): add writes a drafted work-item. Replaced by the live @r1.
  - work-queue @r23 (4): done on the last withdraw. Replaced by the live @r23.
  - work-queue @r9 (4): `work <command>` commits. Replaced by the live @r9.
- **w198**: step definitions `other_initiative` (`supervision_integrate_steps.py`) and `drafted` (`test_work_queue.py`) were removed. Each was used only by a retired scenario: I grepped `features/`, and the suite at HEAD collects with no missing step. The plan lists both (D1).

Nothing is removed or weakened that a plan does not list.

## Allowances

Both reports give `## Tests changed under an allowance: none`, so there is no row to verify. Every changed test is covered by its plan's "Tests the decisions break" (above).

## Cannot verify

none.

## Findings

- **F1. Minor, w198, `tests/scenarios/test_work_queue.py:235`. Triage: observation.**
  - What is wrong: removing `drafted`, the only function that used a parameter named `name2`, left the `name2` capture of `status_is` (".shop/work/{initiative}/{name}.md gives {name2}'s status as {status}") unused.
  - Why it matters: vulture now reports it at 100% confidence, so `tools check` fails on every future range that touches the file.
  - Fix: assert the file's `id` is `full("work-item", name2)`, or take the name with a non-capturing pattern.
  - Reproduction: `python3 <Scripts>/tools check --base 94be81b4` reports `== vulture == tests/scenarios/test_work_queue.py:235: unused variable 'name2'`. The base revision of the file, checked the same way, gives `vulture: clean`.
- **F2. Minor, no work-item (work run's gate commit `186b0c93`), `.shop/work/i37/runs/requests/1-gate/mk.py:1`. Triage: observation.**
  - What is wrong: the gate session's helper script, which wrote its `result.json`, was committed with the run directory.
  - Why it matters: it is now a tracked Python file that fails ruff (I001, SIM115) and is reached by `tools check` and `tools size`.
  - Fix: work run keeps only `brief.md`, `result.json`, `session.json` and drafts from a round's directory, or the gate writes no helper there. The file itself can go with the initiative's next cleanup.
  - Reproduction: the `tools check` output above.

There are no other findings:

- **Code no line asks for**: none. `turn`'s early return is r23. `resolve`'s `turn: asker` is r24. `status_is`'s "not accepted" serves the r7 scenario.
- **Behaviour against a Behaviour line or the Purpose**: none.
  - r23, r24 and narrowed r7 all hold (probe A/B below).
  - r8's "not delivered" guard is untouched: from reading `scripts/workqueue_request.py:156`, the upstream's turn on a delivered request leaves its status alone.
  - r10 "whichever side's turn" is unchanged.
  - r16 still refuses the asker in the upstream's turn on an accepted request (probe E).
- **The `features/` changes** are only `features retire` removals of scenarios the two Retires lists name, plus the formulate round's r7, r23 and r24 (work run's round, not a work-item). Nothing is Critical.

## Shape

- **Size limit (300)**: met for every touched file (`tools size` printed nothing). `scripts/workqueue_request.py` is 187 lines.
- **Module map**: met for every row touched.
  - `scripts/workqueue_request.py` ("the requests of a context: ... `turn`, `resolve`"): the r23 change is at :158-159 and the r24 change at :175-176. Met.
  - `tests/scenarios/requests_steps.py`, `supervision_integrate_steps.py` and `test_work_queue.py` ("step definitions, one module a concern"): met. No new concern, no new module.
- **Step definitions no scenario reaches**: w198 removed the two its retirements orphaned. Every other step of the retired scenarios is still used by a live scenario; I grepped `features/` for each step text. One leftover is the unused `name2` capture (F1).
- **Refactor**: none called for.

## Coupling

The branch adds no dependency and no new reliance on another project. The only coupling I found predates the branch, and its fix is outside this repository:

- The suite emits 438 `PytestRemovedIn10Warning`s from `pytest_bdd/compat.py:28`, which uses pytest's private `_fixturemanager._register_fixture` with `nodeid`.
- It will break when pytest 10 removes that.
- What would make it stable: pin `pytest<10`, or move to a pytest-bdd release that passes `node`.

## Observations

- **O1. Before the branch, out of range.** An asker's `work turn` on a `delivered` request rewrites its status to `awaiting-upstream`, so `delivered` is lost. r18 asks for this literally, and `scripts/workqueue_request.py:153` has no `delivered` guard. Before the branch a delivered request was usually in the asker's turn (accepting passed it there); r24 now makes that certain. A done initiative fulfilling the request would then fall under v_d1.
  - Fix: a request line exempting `delivered` from r18 (and r7), written first.
  - Reproduction: probe C below, `('delivered','asker')` → `work turn q1` → `('awaiting-upstream','upstream')`, exit 0. The base code takes the same path at :153.
- **O2. w197, opened by r23.** An `accepted` request now stays in the upstream's turn, so the upstream can rewrite its outcomes (r15). The next `work turn` sets it `refused` and passes the turn: probe D gives `('accepted','upstream')` → `work outcome q1 1 refused` → `work turn q1` → `('refused','asker')`, each exit 0. No line says whether acceptance is final. The plan names this open case (§5) and the implementer left it unchosen.
- **O3. w197, plan §5, not verified by me.** `supervise_intake.py`'s waiting set (open, awaiting-upstream) does not rerun an `accepted` request left in the upstream's turn. No line asks it to.
- **O4. Before the branch.** ruff I001 at `tests/scenarios/test_work_queue.py:7`: running `tools check` on the base revision gives the same error.

Probe (pytest file run from the deleted scratch directory with `python3 -m pytest -s -n 0`). It writes `.shop/work/requests/q1.md` in a fresh git repository under `tmp_path`, in the requests steps' file form, and runs `scripts/work`:

```
A. r23: upstream ends its turn, lines accepted, refused, withdrawn
  work turn q1                                  exit 0 -> ('accepted', 'upstream')
B. r24: resolve on that accepted request in the upstream's turn
  work resolve q1 --line 1 thing#r3 0.26.0      exit 0 -> ('delivered', 'asker')
C. the asker ends its turn on the delivered request
  work turn q1                                  exit 0 -> ('awaiting-upstream', 'upstream')
D. accepted in the upstream's turn: the upstream rewrites line 1 refused and ends its turn
  work turn q1                                  exit 0 -> ('accepted', 'upstream')
  work outcome q1 1 refused                     exit 0 -> ('accepted', 'upstream')
  work turn q1                                  exit 0 -> ('refused', 'asker')
E. accepted in the upstream's turn: the asker replies
  work reply q1 1 an answer                     exit 1 -> ('accepted', 'upstream') ["work: q1 is in the upstream's turn; the asker answers a question only in its own turn"]
```
