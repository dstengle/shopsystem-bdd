# Review of w238 (supervision r188, r189)

**Verdict: DONE.** No finding is Critical and none is triaged fix now. The commits do what r188 and r189 ask and what the plan's decisions 1 to 4 say. They change nothing under `features/`. The one test they change is the one the plan lists under "Tests the decisions break". There are four Minor findings: one hardening observation, two polish observations and one drop.

## Commits reviewed

From the brief's `Commits:`, oldest first. Their parent chain starts at `2d9ea17b work: w238 ready -> claimed`.

- `4b6996da` supervision r188: an integrate round keeps the ids its change list does not name; r189 steps (red). Files: `scripts/supervise_change.py`, `tests/scenarios/supervision_reintegrate_steps.py`, `tests/scripts/test_supervise_change.py`
- `3e242ec9` supervision r189: an integrate round keeps the terms its change list does not name in the glossary-proposal it was started for. Files: `scripts/supervise_change.py`, `tests/scripts/test_supervise_change.py`
- `7c39e421` supervision r189: g1's apply round gives the unheld answer so r221 starts the integrate round. File: `tests/scenarios/supervision_reintegrate_steps.py`

All touched files are in the work-item's fileset. I reviewed the change as `git diff 2d9ea17b 7c39e421`.

The implementers' results give other hashes: `440352d6`, `c39bac83`, `ecdeb3a7` (6-, 9- and 10-implement), and `d15918dc` in an earlier result. Each subject matches one merged commit, one to one. The hashes differ because the branch was rebased onto main twice (the answers record the rebase onto 0853ad46). See finding 3.

The suite comes from the brief's record: 1091 passed, 0 failed at 7c39e421. The expected failures listed there are all requests scenarios and other supervision scenarios, not r188 or r189.

## Removed and weakened tests

**One test changed, and the plan lists it.** I searched the diff for:
- deleted `def test_` and step functions;
- changed `assert` lines and parametrize lists;
- `skip` and `xfail`.

What I found:

- **`tests/scripts/test_supervise_change.py::test_a_round_started_for_one_proposal_merges_its_ids_into_another_held_proposal`, line 37.**
  - Before: p1, the round's own proposal, ended with `adds: [thing#r5]`, so the old full replacement dropped its held thing#r1.
  - After: p1 ends with `adds: [thing#r1, thing#r5]`.
  - This is still an exact assertion of the same strength. It now asserts the r188 behaviour, and the p2 assertions are kept.
  - The plan lists it in part 4, "Tests the decisions break".
- **The Given `questions_and_answers` in `supervision_reintegrate_steps.py`** was generalised from `p1` to `[pg]1`. For p1 it writes the same file, log line and commit as before, and it has no assertion. The same step text still matches. This is not a weakening.
- No test function was deleted. No skip or xfail was added.

## Allowances

- **10- and 11-implement reports:** `## Tests changed under an allowance` says "none". The commits agree: the only test change is the plan-listed one above.
- **3-implement report:** it names the plan-listed p1 assertion. That test is listed in the plan, not claimed under an allowance, and the commit matches what the plan says.
- 6- and 9-implement say the same.
- **Result: no allowance row claims more than the commits hold.**

## Cannot verify

- **The report's `--work-item w238` run (186 passed, 1 skipped).** I ran only the four unit tests of `test_supervise_change.py` and the r188 and r189 scenarios, and all six passed. I took the suite from the brief's record.
- **Stages 4-implement and 5-implement left no report and no result.** The work-item's Faults record two implementer sessions that ended with exit code 1. I cannot tell from the commits what those sessions tried. The merged commits are complete on their own.
- **The plan's open case 1.** This is an integrate round started for a capability-proposal or for the initiative whose change list names the glossary while a glossary-proposal is held. Decision 4 keeps the old behaviour, a fresh write of `glossary.md`, and no line or scenario of this work covers the case. It is unchanged by these commits, so I make no finding on it.

## Findings

### 1. Minor, observation (w238): `redraft_lists` drops the change list's ids for a list the proposal's front matter lacks

- **Where:** `scripts/supervise_change.py:74-84`.
- **What is wrong:** `redraft_lists` rewrites each of `adds:`, `changes:` and `removes:` with `re.sub(..., count=1)`. When the held proposal has no line for one of the lists, the sub matches nothing, and the ids the round's change list gives for that list are silently lost.
- **Why it matters:** `rewrite_lists`, which this call replaces for the own proposal, wrote all three lists whatever the file held, so this is a narrowing.
- **Why it is only hardening:** every proposal `work run` writes has all three lines, and so does every held capability-proposal or glossary-proposal from i25 onwards that I grepped. Only proposals of older, closed initiatives lack lines. No client sends this input today.
- **Reproduction:** `.shop/scratch/w238-12-review/test_probe.py`.
  - Setup: p1 holds `adds: [thing#r1]` and no `changes:` or `removes:`. The round is started for p1, and its change list adds thing#r5 and removes thing#r2.
  - Command: `python3 -m pytest -q -s .shop/scratch/w238-12-review/test_probe.py -p no:cacheprovider`
  - Result: the test fails. p1 ends with `adds: [thing#r1, thing#r5]` and no `removes:` line, so thing#r2 is lost.
- **Fix:** where a field line is missing, add it before the closing `---`, as `rewrite_lists` does.

### 2. Minor, observation (w238): new lint findings in the changed lines

`tools check --base 2d9ea17b` reports 10 ruff findings. Three are in lines these commits add:

- **`scripts/supervise_change.py:83`, B023 (loop variables `field` and `mine`).** This is a false positive, because `re.sub` calls the lambda before the loop moves on. The code copies the pattern of `merge_lists` (line 103), which has the same finding already.
- **`tests/scenarios/supervision_reintegrate_steps.py:92` and `:101`, RUF100.** The `# noqa: E731` comments are unused, because E731 is not enabled.

The fix is cheap: drop the two unused `noqa` comments, and pass `field`/`mine` as lambda defaults or build the replacement string first.

The other findings are not from these commits:
- B023 at lines 103 and 130 of `supervise_change.py`;
- the unused import `git` at `supervision_reintegrate_steps.py:13` (vulture too);
- FURB167 at `supervision_reintegrate_steps.py:225`;
- RUF100 at `test_supervise_change.py:7`.

### 3. Minor, observation (w238): the commit hashes in the implementers' results are not the merged ones

- **Where:** `.shop/work/i48/runs/w238/10-implement/result.json` and `11-implement/result.json`.
- **What is wrong:** they list `c39bac83` and `ecdeb3a7`, and 6-implement lists `440352d6`. The merged commits are `3e242ec9`, `7c39e421` and `4b6996da`.
- **What I verified:** the subjects match one to one. The difference comes from the rebases onto main recorded in the answers. No commit is missing and none is extra.
- **Fix:** none needed for this work-item. Name it if the result is used to find commits.

### 4. Minor, drop (w238): the drafts-path code is duplicated, and `write_proposals`' docstring is stale

- **Duplicated code:** `scripts/supervise_change.py:128-131` and `:149-152` repeat the "The drafts of this proposal are in …" rewrite.
- **Stale docstring:** `write_proposals`' docstring (lines 107-110) still says the own proposal has "its lists … replaced". Since r188 the lists are redrafted, keeping the ids the change list does not name.
- **Module header:** the plan said it would name r188 and r189; it does not.

This is polish. A helper would make it cleaner, but it changes nothing observable.

### Checked and not a finding

- **Nothing under `features/` changed** in the three commits (`git show --stat`). The `features/` change between the brief's Base and the tip is main's change, which arrived through the rebase.
- **Code no line asks for:**
  - The glossary branch's early `return written`, which skips the fresh `glossary.md`, serves r189 and plan decision 3: the glossary-proposal the round was started for is rewritten, with no second proposal.
  - Moving a held id that the change list names into the list the change list gives serves r188 with r148, as plan decision 2 says.
  - The apply path (`rewrite_lists`, r145) is untouched.
- **Behaviour against the capability:**
  - r188 is satisfied: the ids not named are kept.
  - r189 is satisfied: the terms not named are kept in g1, and no `glossary.md` is written.
  - r171 still holds when the round was not started for a glossary-proposal, because the old branch is unchanged.
  - The step change in 7c39e421 (g1's apply round gives `unheld_answers`) is what the person's answer of 2026-11-02 asked for. It reaches r189's integrate round through r221.
- **Size:** `tools size --limit 300` prints nothing. The touched files have 161, 80 and 226 lines.
- **Import contracts:** import-linter reports that the project states none.

## Commands run

- `git show --stat --format='%H %P %s' 4b6996da… 3e242ec9… 7c39e421…`
- `git diff 2d9ea17b… 7c39e421…`
- `git show 7c39e421:scripts/supervise_change.py`
- `git show 2d9ea17b:tests/scenarios/supervision_reintegrate_steps.py | grep -n "import\|noqa"` and the same for `test_supervise_change.py`
- `git log --oneline -1 --grep="^work: w238 ready -> claimed$"` gave 2d9ea17b
- `git diff 6cf63096 7c39e421 --stat -- features/`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 2d9ea17b…`
  - ruff: 10 findings (3 from these commits, see finding 2)
  - vulture: 1 finding (`git` unused import, from before these commits)
  - import-linter: no contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: nothing printed
- `wc -l` on the three touched files
- `python3 -m pytest -q tests/scripts/test_supervise_change.py tests/scenarios/test_supervision.py -k "test_supervise_change or keeps or redrafts_some" -rA`: 6 passed, including the r188 and r189 scenarios
- `python3 -m pytest -q -s .shop/scratch/w238-12-review/test_probe.py`: failed as reported in finding 1
- A grep of `.shop/work` for held proposals and their `adds:`/`changes:`/`removes:` lines
