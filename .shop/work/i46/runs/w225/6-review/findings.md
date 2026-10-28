# Review of w225 (second review, 6-review)

**Verdict: DONE_WITH_CONCERNS.** One finding is Important and fix now: the glossary-only done (r161) reads the initiative's `ledger.md` as a proposal. Every round appends to that file, so a real glossary-only initiative is never set done. The scenario passes only because its fixture writes no ledger.

Nothing changed under `features/`. No test was removed or weakened. The suite record shows 1068 passed and 0 failed at 52207c77; the expected failures are w212's parked requests scenarios.

The earlier review's fix-now finding (r117's approval question written on a glossary-proposal) has been answered. Under the person's delegation (2026-10-28) it was accepted as it is, with r117 widened through a request. It is not raised again here.

## Commits reviewed
- 0f01102e `work run: route a glossary-proposal through gate, apply and approved (r164 r165 r166 r167 r169 r170)`
- 52207c77 `work run: an initiative that changes only the glossary is set done (r161)`

The parent of 0f01102e is d5abde5f `work: w225 ready -> claimed`. The implementer's results list 9ebc483f and 58c712f0. `git diff --stat 58c712f0 52207c77 -- scripts tests features spec` is empty, so the merged commits carry the same change.

## Removed and weakened tests
None.

What I searched for, in the diff of `tests/`:
- deleted `def`s;
- dropped parametrize cases;
- removed or changed `assert`s;
- added skip or xfail;
- Then-step regexes that were widened.

Each changed step, compared before and after:
- **`gate_started`**: it called `rounds(repo, "gate")` before and calls `rounds(repo, kind, name)` now. `rounds()` defaults to `name="p1"` (`supervision_rounds_steps.py:150`), so the p1 case proves the same thing.
- **`apply_started` and `approved_after_apply`/`position`**: p1, which was the default, is now a parameter. The assertions are the same.
- **`proposal_awaiting`, `round_given_drafts`, `written_from_round`, `no_formulate_for_p1`**: `p1` became `[pg]1`. The assertions are the same.
- **`glossary_proposal_answered`**: only a Given's regex was widened. The step asserts nothing, and r172's scenario still uses it.

The plan lists no test the decisions break, and none is broken.

## Allowances
- **3-implement report:** "none (… no assertion changed)". This holds, as verified above.
- **4-implement report:** it made no commit and did not check the allowances.

## Cannot verify
- That the accepted scenarios were red before the commits. The research notes and the 3-implement report say 8 failed, but I have no run of my own.
- That r167 is meaningful. It was vacuous before the routing; it was accepted as covered by r166's routing (the person's delegated answer, 2026-10-28).

## Findings

### 1. Important, fix now: the glossary-only done never holds for an initiative with a ledger
- **Where:** `scripts/supervise_glossary.py:66-67` (`glossary_only_done`), from 52207c77.
- **What is wrong:** the function treats every `*.md` in the initiative's directory, apart from `initiative.md`, as a proposal or work-item, and returns False when any of them is not an approved glossary-proposal. `ledger.md` has no front matter, so its kind is `None`, and the function returns False.
- **Why every real initiative is hit:** `agents/initiative-round.md:50` says "Every round ends by appending one line to the initiative's ledger, `.shop/work/<initiative>/ledger.md`". A glossary-only initiative only exists after the integrate round that drafted its glossary-proposal, so its directory always has a `ledger.md` by the time g1 is approved.
- **Why it matters:** this is a wrong answer. r161 ("an initiative that changes only the glossary … `work run` shall set the initiative's status to `done`") is never delivered in a real run. The r161 scenario is green only because its Given (`supervision_done_steps.py:28-34`) writes no ledger.
- **Elsewhere this file is excluded:** `model_work.py:142` and `workqueue_status.py:41` both skip `ledger.md` when they read an initiative's directory.
- **Fix:** skip `ledger.md` as those modules do, or count only files whose front matter has a `kind`. Add a ledger line to the r161 Given (or to a step test) so that the scenario covers the case.
- **Reproduction:** `.shop/scratch/w225-6-review/test_probe_ledger.py` builds an initiative with an approved g1 (adds `term/ledger`) and a committed `spec/index.md` holding **ledger**, with and without `ledger.md`. `python3 -m pytest -q -s -n0 -p no:cacheprovider .shop/scratch/w225-6-review/test_probe_ledger.py` printed:
  - `without ledger.md: True`
  - `with ledger.md: False`

### 2. Minor, observation: the glossary-only done ignores raised requests that are not delivered
- **Where:** `scripts/supervise_done.py:28-37` and `scripts/supervise_glossary.py:62-76`.
- **What:** r105's clause on delivered requests is not checked for a glossary-only initiative.
- **Why it is only an observation:** r161 is silent on requests, so the code follows r161 as written. The plan's §5 names the case.
- **Reproduction:** a code read. `set_glossary_done` calls only `glossary_only_done`.

### 3. Minor, observation: an abandoned initiative can be set done
- **Where:** `scripts/supervise_done.py:31-32`.
- **What:** the only guard is `before == "done"`. An `abandoned` initiative given to `work run` by name, with only approved glossary-proposals and its terms committed, would move from `abandoned` to `done`. No client does this today.
- **Reproduction:** a code read. `grep -n abandoned scripts/supervise*.py` finds it only in `supervise_all.py`.

### 4. Minor, observation: a new unused `noqa`
- **Where:** `tests/scenarios/supervision_proposal_steps.py:172`, new in 0f01102e.
- **What:** `# noqa: E731` is unused, and ruff reports RUF100.
- **Fix:** remove it (cheap).

## Checks
`tools check --base d5abde5f`:
- **ruff:** 6 errors.
  - From these commits: `supervision_proposal_steps.py:172` RUF100 (finding 4).
  - Already there, on lines the commits did not touch: `workqueue.py:248` I001, `supervision_proposal_steps.py:102` and `:137` RUF100, `supervision_reintegrate_steps.py:13` F401 and `:174` FURB167.
- **vulture:** clean.
- **import-linter:** the project states no import contracts.

`tools size --limit 300` printed nothing, so no file is over the limit.

## Commands run
- `git log --format='%H %s' -1 0f01102e~1`
- `git log --stat 0f01102e~1..52207c77`
- `git diff 0f01102e~1 52207c77`
- `git diff --stat 58c712f0 52207c77 -- scripts tests features spec`
- `git diff --stat d5abde5f 52207c77 -- features/` (empty)
- `grep -nE "r161|r16[4-9]|r170|r172|r117\b|r105\b" spec/capabilities/supervision.md`
- `grep -n "def rounds" -A6 tests/scenarios/*.py`
- `sed -n 60,100p scripts/supervise_brief.py` and `sed -n 210,250p scripts/supervise.py`
- `ls .shop/work/i46/ .shop/work/i45/`
- `grep -rn ledger.md scripts/*.py`
- `grep -n "ledger\|work note" agents/initiative-round.md`
  - The risk checked: whether a real initiative's directory holds non-proposal `.md` files. It does: `ledger.md`, written by every round.
- `python3 -m pytest -q -s -n0 -p no:cacheprovider .shop/scratch/w225-6-review/test_probe_ledger.py`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base d5abde5f81be507f069972bf090ecea2868a0a14`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
