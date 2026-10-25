# Review of w185: DONE_WITH_CONCERNS

Verdict: the commits make the accepted scenarios pass and stay inside the plan's design, with two departures from the plan
that contradict Behaviour lines. (1) An apply round's change list skips the r107 capability check. (2) Under r115, a
refused round stops the rounds of the initiative's other proposals. Both are Important and triaged fix now. Nothing under
`features/` changed beyond the retired scenario. No test was removed or weakened.

## Commits reviewed

The branch `work/w185` is gone. The commits are the ones between `80506ab1` (work: w185 ready -> claimed) and `e53f2587`
(work: w185 claimed -> done) on the checked-out branch, leaving out `work run`'s own commits and the i32/i33 commits that
came in by merge (`380be1d1`, `da59b6b8`, `9a888415`, `5f743a7b`; these touch only `.shop/`, see `git diff --stat` below):

- `aef1793b` r111: steps for a started initiative with a ready work-item, done after green; stand-in gives usage
- `a0f2b5ba` r116: widen the round-started Then to formulate, answered_proposal writes the asking round's move
- `ce5c1bfb` r83 r112 r113 r114 r115: formulate questions, apply change list into the proposal, other nodes before a
  round's error; retire old r83

The implementers' results list `c0b69237`, `159c7530` and `2b29d748`, with the same subjects. Those commits were rewritten
when the branch was brought onto the initiative branch. Each subject and change matches its counterpart, so the difference
is only in the hashes and is not a finding.

## Removed and weakened tests

I searched the diff for deleted `def test_`, dropped parametrize cases, removed or changed `assert` lines, `skip` and
`xfail`, and step functions rewritten to assert something else.

- `features/supervision.feature` @r83 @deprecated "when the formulate round … ends, the proposal is formulated
  (deprecated)": removed. The work-item lists it under Retires. Its binding is `scenarios("supervision.feature")`, so it
  has no binding of its own to remove. It proved that a proposal reaching a formulate round ends up formulated. The new
  @r83 scenario proves the same thing for a formulate round that gives no question. Allowed.
- `tests/scenarios/supervision_rounds_steps.py` `questions_hold`: rewritten. Before, it asserted the gate's reading form
  for exactly four quoted strings; any other count raised an unpack error. Now four quoted strings take the same path as
  before, and any other count checks that each question is held. Not weakened.
- `apply_started`: widened to `apply|formulate` and "answers?". For kind apply it asserts what it did before (exactly one
  apply round, and each answer in its brief). Not weakened.
- `answered_proposal`: changed setup only (below). Not weakened.

The plan's "Tests the decisions break" lists none of these as broken, and none needs listing.

## Allowances

- Report 3-implement, `answered_proposal` (setup): **holds**. The diff adds an optional `adds` group to the regex and a
  log.jsonl line for "given by its … round". It adds, removes or changes no `assert`, no expected value and no
  parametrize case.
- Report 4-implement gives "none" and calls `questions_hold` the initiative's own step. It is not an `interim` claim, and
  no allowance is needed because nothing was weakened.

## Cannot verify

- That r70 is now met as the person's answer asks ("only a gate round's answered questions start an apply round"). No
  scenario fails if `route()` is removed. The r116 Then passes on the old apply-then-formulate chain (the person ruled
  r116 met as is), and so does the new r83 (the 4-implement report says so). The r70 scenario writes no log move. r112
  probably detects it, but I did not run a mutation. See Minor finding 4.
- The reports' suite figures (156 passed, 1 skipped for `--work-item w185`). I did not run the whole suite: `work run`
  ran it before the merge.
- Whether ruff's `I001` on `tests/scenarios/test_supervision.py` was there before these commits. The added import is in
  alphabetical place, so it is probably the existing `from .supervision_world import *` / `import (…)` pair. The two
  `FURB167` hits in `tests/scripts/stub_claude.py:189-190` are on lines the commits did not touch.

## Findings

### 1. Important, fix now: an apply round's change list skips the r107 check (w185)

`scripts/supervise_rounds.py:126-131` (in `ce5c1bfb`) with `scripts/supervise_change.py:52-65` (`rewrite_lists`).

- **What is wrong:** an apply round's `changes` are now read (r114). An entry naming a capability that neither
  `spec/capabilities/` nor the drafts have is dropped without a word, by `rewrite_lists`' `each["capability"] ==
  argues` filter. `work run` then goes on and exits successfully. `self.unknown()` runs only for integrate (line 118).
- **Why it matters:** r107 reads "If a change list that `work run` reads names a capability that neither … have, then
  `work run` shall … exit with an error, naming the capability." The plan's D3 says outright that r107 applies to this
  list. The implementer left it out and gave it only as an open question ("ignored").
- **Related:** if the list's entries name only other capabilities, `applied` is not empty, so all three of the
  proposal's lists are written empty. What integrate drafted is lost.
- **Fix:** run `self.unknown(applied, …)` for the apply round too. On an unknown capability, keep the round as r96 does
  and exit with the r107 error, before `rewrite_lists` and the approved move.

### 2. Important, fix now: under r115 a refused round stops the other proposals' rounds (w185)

`scripts/supervise.py:205-213` (in `ce5c1bfb`) and `scripts/supervise_rounds.py:62-67` (`rounds()`).

- **What is wrong:** the Refused is caught around the whole of `self.rounds()`. The loop stops at the first faulted
  round, so a second capability-proposal of the initiative that is due (drafted, approved, or answered) gets no round in
  this run. The 4-implement report says so ("rounds() stops at the first"). The plan's D4 had "the remaining proposals'
  rounds … all still run".
- **Why it matters:** r115 reads "… `work run` shall take the initiative's other nodes through their transitions before
  it exits with an error". r111 says the same for any node left able to move. Another proposal is another node.
- **Fix:** in `rounds()`, hold the first Refused, leave out the proposal whose round faulted, and keep running the rounds
  due for the others. Raise the held Refused after `draft()` and `pull()`, as now.

### 3. Minor, observation: an apply round's unreadable change list is ignored (w185)

`scripts/supervise_rounds.py:127-130`.

- **What is wrong:** `BadChanges` is swallowed, and the proposal moves to approved with integrate's lists. No line names
  this case; the plan left it open.
- **Reproduction:** none run (no Python other than pytest is allowed). The code reads it plainly: `except BadChanges:
  applied = []`, then no rewrite.
- **Fix:** none needed now. A line for it would come through integrating-a-proposal.

### 4. Minor, observation: no scenario pins `route()` (w185)

`scripts/supervise_rounds.py:51-60`.

- **What is wrong:** the person's answer asks that r70 be implemented so a formulate round's answered questions start no
  apply round. Neither the r70 scenario nor the r116 scenario fails if `route()` returns `AFTER[status]` for every
  status.
- **Why it matters:** the behaviour can regress without a red. The code itself is right and serves r70 and r116 (it is
  not code that no line asks for).
- **Fix:** none now. The person ruled r116 met as is. A later Then "no round of the kind apply was started for p1" would
  pin it.

### 5. Minor, drop: change outside the file set (w185)

`tests/scripts/stub_claude.py:267`.

- **What is wrong:** the stand-in's result now carries `usage`. The file is not in the work-item's `fileset`. The
  3-implement report lists it under "Outside the file set", with its reason: `measure initiative` refused the stand-in's
  session without it, so r111 could not go green.

### 6. Minor, drop: stale docstrings (w185)

- `scripts/supervise_rounds.py:1-6` still says an awaiting-answer proposal "is given to an apply round".
- `scripts/supervise_change.py:1-3` still speaks only of "An integrate round's change list".

### 7. Minor, drop: a step defined twice (w185)

`tests/scenarios/supervision_formulate_steps.py:72` defines `"p1 is awaiting-answer"`, which
`test_supervision.py`'s `(?P<name>\w+) is awaiting-answer$` already matches. It does no harm.

## Check and size

- `tools check --base 80506ab1`:
  - ruff: 3 errors (`tests/scenarios/test_supervision.py:14 I001`, `tests/scripts/stub_claude.py:189,190 FURB167`), on
    lines the commits did not change (see Cannot verify).
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: printed nothing; no tracked file is over the limit.

## Commands run

- `git log --format='%H %s' -1 --grep="^work: w185 ready -> claimed$"` and the same for `claimed -> done`
- `git log --oneline -15`
- `git log --format='%h %s' 80506ab1..e53f2587`
- `git show --stat` and `git show` for `aef1793b`, `a0f2b5ba` and `ce5c1bfb`
- `git diff 80506ab1 e53f2587 --stat -- features tests scripts`, and the same with `-G "skip|xfail|^\s*def test_|assert"`
- `git show e53f2587:scripts/supervise_rounds.py`, `git show e53f2587:scripts/supervise_change.py` and
  `git show e53f2587:tests/scenarios/test_supervision.py`
- Grep of `features/supervision.feature` for the @r70 @r83 @r111-@r116 scenarios, and grep of
  `spec/capabilities/supervision.md`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 80506ab1…`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `git status --short` (clean)
