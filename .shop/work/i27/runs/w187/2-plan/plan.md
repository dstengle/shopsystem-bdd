# Plan of w187: fix the findings of branch review 8 of i27

Accepts supervision r91-r97 and r66. Findings: `.shop/work/i27/runs/branch-review/8/findings.md`. The work-item has no rulings and no `Retires` section.

## 1. What goes green

None of the accepted scenarios is red today. The researcher ran all of them: 10 test ids, 10 passed (notes part 1). The work is in the findings, and the scenarios that cover them must stay green:

- **r95, r66** ("`work run` started with no initiative runs the integrate, apply and formulate rounds of different initiatives one at a time"; "`work run` started with no initiative takes every initiative that is neither done nor abandoned…"):
  - F11, the only finding the review sends on (Important, in the review's `questions`): the r95 scenario failed once in a loaded full suite run.
  - It passes alone and passed in a second full run. The cause is not known (notes D5).
  - Here, red means the failure captured under load (decision 1).
- **r92** ("an integrate round's change list gives one drafted capability-proposal for each capability it names, with what it adds, changes and removes on that capability"; "the change lists of two initiatives that name the same capability give two drafted capability-proposals with different ids"):
  - Both pass. But F4 / notes D1 is reproduced by probe A: two entries of one change list that name the same capability give two writes of the same file, and the second overwrites the first. `thing#r4` was lost.
  - This goes against r92. It goes red in a new script test (decision 2).
- **r91, r93, r94, r96, r97** (the drafts of an integrate round kept, both outline rows; a started initiative with neither proposal nor work-item given to integrate; no branch review and no measure without a work-item; integrate DONE without a change list is an error):
  - They pass, and no finding asks for a change to them. They must stay green.
- **Shape** (findings "Shape"): the CLAUDE.md `scripts/supervise*.py` row and the `supervise_rounds.py` module docstring are stale. Neither names the integrate round's ending (r91, r96) or r95's one-at-a-time rounds.
- **Deprecated scenarios retired:** none.

## 2. Where the change lands

- `tests/scenarios/supervision_all_steps.py`:
  - The r95 steps (`rounds_linger`, `serial_rounds_started`, `serial_rounds_apart`, and `sessions` if the record turns out to be at fault) are made to hold under load, per decision 1.
  - F2's two ruff errors at `:111` and `:127` are fixed, since these lines change anyway.
- `scripts/supervise_all.py` and `scripts/supervise_rounds.py`:
  - `supervise_rounds.py`: its module docstring names the integrate round, how it ends (r91, r96) and r95's round lock.
  - Both files: the round lock, only if decision 1 shows rounds overlapping (reading (b)).
- `scripts/supervise_change.py`: `Changes.write_proposals` writes one proposal for each capability and merges the adds, changes and removes of every entry that names it (decision 2).
- `tests/scripts/test_supervise_change.py` (new): the case of two entries for one capability, which no scenario drives. Decision 2 adds this file in place of a new feature scenario.
- `CLAUDE.md`: the `scripts/supervise*.py` row names the integrate round with r91/r96 and r95's lock on rounds.

Removed from the researcher's set:
- `scripts/supervise.py`: D4 is out (decision 3).
- `features/supervision.feature` and `tests/scenarios/supervision_integrate_steps.py`: this plan adds no scenario. Scenarios are formulation's to write.

## 3. Decisions

1. **F11 (r95, r66): capture the failure first, then fix only what it shows.**
   - The implementer runs the r95 scenario repeatedly, alone with `-n0` and beside a full `-n auto` suite run, until it fails, and keeps the failure text.
   - **If `serial_rounds_apart` fails** (one round started before another ended): the lock is incomplete. That breaks r95, so it is fixed in `supervise_all.py` / `supervise_rounds.py`, and the step stays as it is.
   - **If `serial_rounds_started` fails, or the run times out:**
     - The fault is the test's timing (the stand-in's `linger: 1`, notes D5). The stand-in's wait gets a margin, or the step waits on what the record shows rather than on a fixed time.
     - The overlap assertion stays as strict as it is.
   - **If no failure is captured after a reasonable number of loaded runs:** the implementer says so in its report and makes only the margin change. It keeps the strict `ended < started` check.
   - Rests on r95, r66, and the review's own fix for F11.
2. **F4 / D1 (r92): one proposal for each capability the change list names, however many entries name it.**
   - That proposal's `adds`, `changes` and `removes` are the union of every entry that names the capability, in the order they first appear.
   - `write_proposals` returns one path for each capability.
   - The red test is a script test in `tests/scripts/`. It drives `entries` and `write_proposals` the way probe A did, so it shows the lost id before the fix.
   - Rests on r92 ("a `drafted` capability-proposal for each capability the change list names, with the requirement ids and terms it adds, changes and removes on that capability").
3. **Out of scope** (no requirement this work-item accepts settles them, and none is a finding the review sends on):
   - **D4** (`work run i1` exits 0 with no work-item and a proposal awaiting answer):
     - r9 as written gives success when every work-item (here none) is green or withdrawn, so today's exit agrees with it.
     - Exit 3 would change what the narrator sees, and no line says so for `work run <initiative>`. It is left as it is.
     - It is named in the result's summary for the person.
   - **D2, D3, F3** (a capability name with `/` or `..`): r107 is i29's line, not accepted here.
   - **F5** (ids not checked against their form): observation.
   - **F6** (a failed commit leaves proposals uncommitted): observation.
   - **F7** (the apply brief does not name the kept drafts): r108, i29's.
   - **F9** (`work:` prefix in the commit subject): w166's, triaged drop.
   - **F10** (records left uncommitted): r106, i29's.
   - **The `move` gap** (notes part 5): not a finding.
   - **F2** on `supervise_brief.py:84` and `test_supervision.py:14`: triaged drop, and the files are untouched.

## 4. Tests the decisions break

None:
- **Decision 1:** it rewrites the r95 steps themselves. That is the fix, not a test it breaks. The overlap assertion keeps what it asserts.
- **Decision 2:** it changes what `write_proposals` returns only when two entries name one capability. The notes (parts 3 and 4) found no test with two such entries, and no test outside `supervise_rounds` that calls `write_proposals` or `supervise_change`. The r92 scenarios name distinct capabilities and keep their meaning.
- **Weakened test:** `second_not_refused` (w164's allowance) is not touched.

## 5. Open cases

For the implementer to name, not to choose:
- **Duplicate ids:** one id listed by two entries of the same capability, or the same id under `adds` in one entry and `changes` in another. Probe A did not try either case.
- **Entry with only a capability:** it gives a proposal with three empty lists (notes D3, related). Neither r92 nor r96 says whether that is a change list.
- **If F11's failure is in the stand-in's record:** if `sessions` reads a record that concurrent stand-ins append to, and the failure comes from that record rather than from the lock or the linger, the implementer reports it as found.
- **`started` with an unreadable request:** `due()` gives no integrate round and no error (notes part 2). r93's scenarios do not cover it.
