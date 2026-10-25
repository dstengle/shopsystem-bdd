# Review of w144: initiative-round appends its ledger line with work note

**Verdict: DONE_WITH_CONCERNS.** One finding is Important and should be fixed now. In integrating-a-proposal, the `gate` dispatch and the round-2 `integrate` dispatch do not give the initiative's name. The agent's new text says a round with no initiative skips the ledger line. So those rounds still write no ledger line, which breaks r40. Nothing is Critical: no change under `features/` and no test removed or weakened.

## Commits reviewed

The branch `work/w144` is gone. The commits are the ones between `9ff231e work: w144 ready -> claimed` and `200e433 work: w144 claimed -> done` on the checked-out branch, leaving out `work run`'s own `work:` commits (b48662c belongs to w143):

- `8ff0080 initiative-round appends its ledger line with work note (r40)`: agents/initiative-round.md, scripts/supervise_worker.py, skills/formulating-features/SKILL.md, skills/integrating-a-proposal/SKILL.md (+11 −9).

The implementer's result lists `6d5851d`. That is the same commit rebased: same message and author date, and `git diff 6d5851d^ 6d5851d` is identical to `git diff 8ff0080^ 8ff0080`. The hashes differ but the content does not, so this is no finding.

## Removed and weakened tests

None. The commit touches no file under `tests/` or `features/` (`git log --stat` over the range). The plan lists no test under "Tests the decisions break". I searched for the risk the plan named (tests reading initiative-round's tools or the rounds' tool lists) and the commit leaves them alone.

## Allowances

The report's `## Tests changed under an allowance` says "none". That holds: no test changed.

## Cannot verify

- That a real `claude -p` round under `work run` runs `python3 <Scripts>/work note …` and that the allowance `Bash(python3 <SCRIPTS>/work note *)` matches its command. This is a guarantees work-item with no scenario. I checked by reading that the brief's `Scripts:` (supervise_brief.py:30) is the same `SCRIPTS` the allowance uses.
- Merging the round's ledger commit back. supervise_rounds.py:54 merges the round branch into the initiative branch. If someone runs `work note` on the initiative branch while a round is running, both sides append to `ledger.md` and the merge can conflict. The round then faults and the proposal keeps its status. I could not reproduce this: it needs a repository fixture, and this review's shell allows no `git init`. I checked that no `supervise*.py` writes the ledger itself (grep `ledger`), so only a person's `work note` during a run could cause this.
- The report's suite figures (142 passed with `--work-item w144`; 798 at start). I did not rerun them: `work run` ran the suite before merging.

## Findings

### F1. Important, fix now: two of the skill's dispatches still do not name the initiative (work-item w144)

- **Where:** skills/integrating-a-proposal/SKILL.md:21, step 2: the `gate` dispatch ("naming the rounds' drafts and any reports to show") and the new `integrate` round 2 ("Their answers go to a new `initiative-round`, job `integrate`, round 2, in their own words").
- **What is wrong:** the commit added "the initiative's name" to steps 1 and 3 only. agents/initiative-round.md:38 now says: "If your input names no initiative … reply with your work and say the line was not written". So every `gate` round and every answers round dispatched this way skips its ledger line, which goes against spec-integration#r40 ("When `initiative-round` finishes a round, … shall append one line to the initiative's ledger"). The plan (§2) named "the answers round" among the dispatches to change. That change was not made.
- **Why it matters:** these rounds leave no line in the tracked ledger (design-decision/the-ledger-is-tracked). The ledger is the record of what each round ended with, so it is missing entries.
- **Fix:** in step 2, have both the `gate` dispatch and the round-2 `integrate` dispatch give "the initiative's name", as steps 1 and 3 now do.

### F2. Minor, observation: a `BLOCKED` round's ledger line is not decided (work-item w144)

- **Where:** agents/initiative-round.md:38.
- **What:** r40 says "finishes a round". The agent text does not say whether a round that ends `BLOCKED` appends a line. The plan (§5) and the report ("Open questions") both leave this open.
- **Reproduction:** a reading only. `grep -n BLOCKED agents/initiative-round.md` finds nothing in "The ledger" about it.
- **Fix:** add one sentence choosing either reading, for example "a round that ends BLOCKED appends a line naming the block".

### Not findings (checked)

- Code no line asks for: the only code change is supervise_worker.py:45-46. It gives the `apply`/`formulate` rounds `Bash(python3 <SCRIPTS>/work note *)` and nothing else. That serves r40 and the-ledger-is-tracked, and it gives no other `work` subcommand, which is consistent with the-context-runs-without-a-coordinator.
- Splitting r6 ("commit … to `spec/` alone") from the ledger: `work note` commits the ledger by pathspec in its own commit (research notes §2, probe), and the agent text puts it after the job's own commit.
- Size: supervise_worker.py is 240 lines (limit 300). `tools size --limit 300` printed nothing.

## Commands run

- `git log --format=%H -1 --grep="^work: w144 ready -> claimed$" work/w144`: refused, the branch is gone.
- `git log --format='%H %s' -1 --grep="^work: w144 ready -> claimed$"` → 9ff231e. The same for `claimed -> done` → 200e433.
- `git log --format='%h %s' 9ff231e..200e433` and `git log --stat … -- . ':!.shop'`.
- `git show 8ff0080`, `git show --stat 6d5851d`, `git show --stat b48662c`.
- Compared `git diff 8ff0080^ 8ff0080` with `git diff 6d5851d^ 6d5851d`: SAME. This went through a temporary file `a.diff` in the stage directory, which I removed straight after. It was an accidental extra write.
- `grep` over scripts/supervise_*.py, agents/ and skills/ for `ROUNDS`, `integrate`, `gate`, `ledger` and `spec/ alone`. Read supervise_rounds.py and supervise_brief.py:20-45.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 9ff231e…`: ruff "All checks passed!"; vulture "clean"; import-linter "the project states no import contracts".
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: no output.
- `wc -l scripts/supervise_worker.py`: 240.
