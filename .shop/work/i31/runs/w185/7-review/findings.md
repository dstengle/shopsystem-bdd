# Review of w185 (round 7, after the fix in 6-implement): DONE

Verdict: the fix commit does what the person's two answers ask. (1) An apply round's change list naming a capability
that neither `spec/capabilities/` nor the drafts have is refused before any list is rewritten (r107). The round is kept,
the status is kept, and the error names the capability. (2) In `rounds()`, a refused round leaves only its own proposal
out. The other proposals' rounds still run, and the first error is raised once none is due. `pull_through` then drafts
and pulls before it re-raises (r111, r115). Nothing under `features/` changed, and no test was touched. No finding is
Critical and none is fix now. Everything left is an observation or a drop.

The earlier commits of w185 (`aef1793b`, `a0f2b5ba`, `ce5c1bfb`) were reviewed in `5-review/findings.md`. This review
covers the commits after the latest claim.

## Commits reviewed

The branch `work/w185` is gone (`git log work/w185`: unknown revision). On the checked-out branch, the commits run from
`507d361e` (work: w185 ready -> claimed) to `7e17c47b` (work: w185 claimed -> done). Leaving out `work run`'s own `work:`
commits, which are the i33 `awaiting-answer -> awaiting-answer` moves, one commit remains:

- `968344f4` supervise: an apply round's change list is checked against r107; a refused round leaves the other
  proposals' rounds to run (r111, r115). Files: `scripts/supervise_change.py` (+5 -4) and `scripts/supervise_rounds.py`
  (+24 -9).

The implementer's result lists `407107a3` with the same subject, minus its trailing "(r111, r115)". The commit was
rewritten when it was brought onto the initiative branch. `git diff --stat 507d361e 7e17c47b -- . ':!.shop'` shows only
these two files, so the change matches and this is not a finding.

## Removed and weakened tests

None. The commit touches no file under `tests/` or `features/`. I searched the commit for `def test_`, parametrize,
`assert`, `skip` and `xfail` and found none of them.

## Allowances

The report's `## Tests changed under an allowance` gives "none". It has no rows to verify, and none is needed.

## Cannot verify

- **No scenario pins either fix.** The report says so: no red run. I could not exercise the new paths with a probe,
  because no Python other than pytest is allowed and the steps need a full `Run`. What I verified by reading
  `7e17c47b:scripts/supervise_rounds.py`:
  - **The unknown-capability check comes first.** It runs before `rewrite_lists` and before `move`. So no list is
    written and no transition is made.
  - **The round is not kept twice.** `keep_round` runs once, inside the round lock. The raise is not inside the
    `except (Fault, GitFailed)` block, so that handler does not run `keep_round` again.
  - **The loop in `rounds()` ends.** A faulted name goes into `left`, and `due()` skips it. That covers the initiative
    name for integrate, since `due()` returns `self.initiative` as `due[0]`.
  - **A formulate round with questions does not loop.** When it starts from awaiting-answer, it returns without a
    move. The proposal then has more questions than answers, so it is no longer due.
- **The report's figures.** It gives 155 passed and 1 skipped for `--work-item w185`. I did not run the whole suite.

## Findings

### 1. Minor, observation: the two fixes can regress without a red (w185)

`scripts/supervise_rounds.py:63-76` (`rounds()`) and `:140-145` (the apply round's r107 check).

- **What is wrong:** no scenario has two due proposals with one of them refused. None has an apply round giving a list
  that names an unknown capability.
- **Reproduction:** the 6-implement report says "No scenario pins either fix, so there was no red run". The focused
  run `pytest tests/scenarios/test_supervision.py -k "capability or other_nodes or change_list or gate_round"` gave 10
  passed, and none of the 10 has these Givens.
- **Fix:** a later scenario for r115 with a second proposal due, and one for r107 with an apply round's change list.

### 2. Minor, observation: an apply list naming only other, known capabilities empties the proposal's lists (w185)

`scripts/supervise_rounds.py:146-147` with `scripts/supervise_change.py` `rewrite_lists`.

- **What is wrong:** take a list whose entries are all known capabilities, none of them the proposal's own. `applied`
  is not empty, so the proposal's `adds`, `changes` and `removes` are all written empty. The implementer gives this as
  an open question. The person's answer ("no list emptied") was given about unknown capabilities, and for those it
  holds now.
- **Reproduction:** by reading only. `if applied: self.rewrite_lists(name, applied)` runs with entries that the filter
  in `rewrite_lists` then drops.
- **Why it is not fix now:** r114 writes the proposal's lists "from the change list the round applied". No line or
  client sends such a list today.
- **Fix:** if wanted, a line through integrating-a-proposal.

### 3. Minor, observation: an unreadable apply change list is still ignored (w185)

`scripts/supervise_rounds.py:136-139` (`except BadChanges: applied = []`). This is carried from 5-review finding 3 and
is unchanged. No line names the case.

### 4. Minor, observation: with more than one refused round, only the first is named (w185)

`scripts/supervise_rounds.py:72-76` (`held = held or fault`). r88 and r115 name "an error" about the round. The plan's
open case left open whether a second fault is named, and no line names it. The second round's stage directory is kept
by its own `keep_round`, so nothing is lost.

### 5. Minor, observation: r107's "the round's drafts" for an apply round (w185)

`scripts/supervise_rounds.py:140` reads `unknown(applied, runs/<initiative>, runs=True)`.

- **What it does:** it reads the drafts of the initiative's integrate rounds (`runs/<initiative>/*/drafts/round-*`).
  It does not read the apply round's own stage directory (`runs/<proposal>/<label>`).
- **Why it does no harm:** the apply round's commits are merged before the check. A capability it wrote is therefore
  already in `spec/capabilities/`, so nothing is wrongly refused today.
- **Fix:** none needed.

### 6. Minor, drop: stale module docstring (w185)

`scripts/supervise_rounds.py:1-6` still says an awaiting-answer proposal "is given to an apply round". The commit
updated `supervise_change.py`'s docstring but not this one. It is left over from 5-review finding 6.

## Check and size

- `tools check --base 507d361e`:
  - ruff: All checks passed.
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: printed nothing. The touched files have 192 lines (`supervise_rounds.py`) and 88 lines
  (`supervise_change.py`).

## Commands run

- `git log --format='%H %s' -3 --grep="^work: w185 ready -> claimed$" --all`, and `git log work/w185` (gone)
- `git log --format='%h %s' -1 --grep=...` for ready -> claimed and claimed -> done
- `git log --oneline 507d361e..HEAD`
- `git diff --stat 507d361e 7e17c47b -- . ':!.shop'`
- `git show --stat 968344f4` and `git show 968344f4 -- scripts tests features`
- `git show 7e17c47b:scripts/supervise_rounds.py`
- `git show 7e17c47b:scripts/supervise.py | grep -A14 "def pull_through"`
- `grep` of `spec/capabilities/supervision.md` for r107 and r115
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 507d361e`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `wc -l scripts/supervise_rounds.py scripts/supervise_change.py`
- `python3 -m pytest -q tests/scenarios/test_supervision.py -k "capability or other_nodes or change_list or gate_round"`:
  10 passed
- `git status --short`: clean
