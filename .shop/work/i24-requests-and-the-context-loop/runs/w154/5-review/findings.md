# Review of w154

**Verdict: DONE.** No Critical finding, none triaged fix now. One Minor lint finding and one observation.

## Commits reviewed

The branch `work/w154` is gone. Its commits are the ones on HEAD between `d12acec work: w154 ready -> claimed` and `7cb5c3c work: w154 claimed -> done`, leaving out `work run`'s own `work:` commits (`5c02366 work: w134 done -> green`):

- `2739c54 work run: a round ending other than DONE makes no transition and stops the run (r86-r88)`. It touches scripts/supervise_rounds.py (+5), tests/scenarios/supervision_rounds_steps.py (+43) and tests/scripts/stub_claude.py (+4 -2).

The implementer's result lists `c437cb4`, and that hash is not the one on HEAD. `git show --stat c437cb4` gives the same message, the same three files and the same +52 -2. `git diff c437cb4 2739c54` differs only in w134's run files, log.jsonl and w134.md, which came from the rebase over `work run`'s w134 commits. The patch is the same, so the difference is the merge's rebase, not a finding.

All three changed files are in the work-item's fileset. test_supervision.py is in the fileset but was not changed: the report says the "p1 is drafted" step went in supervision_rounds_steps.py instead, which the plan allowed.

## Removed and weakened tests

None. The diff to tests is additions only: four Givens/Thens in supervision_rounds_steps.py, and in stub_claude.py a plan key `round:<kind>`. I searched the diff for removed `def test`, removed `assert`, changes to parametrize lists, and added `skip` or `xfail`, and found none. The stub change keeps its previous merge: it starts from `default`, the agent's plan overrides it, and the new `round:<kind>` key overrides both only when present, so existing plans keyed by agent behave as before. No file under `features/` is changed.

## Allowances

The report gives "none", and the commits contain nothing that needs one.

## Cannot verify

- The report's figures: suite at start 830 passed / 3 failed, and `--work-item w154` 145 passed, 1 skipped. I did not re-run the suite. The three w154 scenarios do pass (below).
- That `work run` with no initiative stops only the affected initiative when its round gives a non-DONE outcome (plan §5, report "Open questions"). No scenario covers it, and the commit does not touch supervise_all.py.

## Findings

### 1. Minor: tests/scripts/stub_claude.py:182, ruff FURB167 (`re.M` alias)
- **What is wrong:** the line added by this commit, `re.search(r"^# (\w+) of ", brief, re.M)`, fails `tools check --base d12acec` on ruff FURB167.
- **Why it matters:** `tools check` exits 1 on this change, so the lint gate is red for the branch.
- **Fix:** use `re.MULTILINE` (or run `ruff --fix`).
- **Work-item:** w154.
- **Triage:** observation. It is cheap, but it is not a wrong answer, a crash or lost data. Reproduction: `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base d12acec` gave `tests/scripts/stub_claude.py:182:46: FURB167 [*] Use of regular expression alias re.M`, exit 1.

### 2. Minor: scripts/supervise_rounds.py:62-64, 72-73, a non-DONE round's commits are merged before the refusal
- **What is wrong:** a round that faults keeps its branch `round/<name>-<label>` unmerged (lines 65-71). A round that gives a readable non-DONE outcome has already had its branch merged into the initiative branch and deleted (lines 62-64) before line 72 refuses. `keep_round` then commits with the message `work: <name> <kind> round <label> faulted`, even though the round did not fault.
- **Why it matters:** an `apply` round that committed part of its edits to `spec/` and then gave BLOCKED would leave those edits on the initiative branch. The next run would then start apply again on a partly applied tree. The agent's brief (agents/initiative-round.md:55) tells it to "leave what exists as it is" when BLOCKED, so no client does this today. No Behaviour line names what happens to a non-DONE round's commits: r87 forbids transitions, not commits.
- **Fix:** if wanted, check the outcome before the merge and keep the branch as the fault path does. Give the commit message the outcome rather than "faulted".
- **Work-item:** w154.
- **Triage:** observation (hardening). Reproduction: by reading only. I ran no probe, because the stand-in claude makes no commits on the round branch. The verified risk is that line 63 `git merge` runs before the `status != "DONE"` check at line 72.

### Verified, no finding
- **r86, r87, r88:** a readable non-DONE result now calls `keep_round` (commit and push, so r46 and r38 hold), makes no `move` and writes no questions, as the ruling's reading B requires. It raises a Refused that names the round, its stage directory and the outcome. The r88 message for a missing result is unchanged ("wrote no result file"), and the step matches it (D-d).
- **Integrate round (D-c):** it stays `started` on a non-DONE outcome, because nothing rolls it back. This agrees with r84 and r86.
- **Code no line asks for:** none. The message's summary text is mechanism for "how it ended" (r88).

## Commands run

- `git log --format='%h %s' --grep="^work: w154 " HEAD`, `git log --format='%h %s' -8 HEAD`
- `git show --stat 2739c54`, `git show --stat c437cb4`, `git diff c437cb4 2739c54 --stat`, `git show 2739c54`
- `cat -n scripts/supervise_rounds.py`; `grep` of spec/capabilities/supervision.md (r85-r88), tests/scripts/stub_claude.py imports, agents/initiative-round.md
- `python3 -m pytest -q -p no:warnings tests/scenarios/test_supervision.py -k "<the three r86/r87/r88 scenarios>"`: 3 passed
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base d12acec`:
  - ruff: 1 error (finding 1)
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: printed nothing (no file over the limit)
