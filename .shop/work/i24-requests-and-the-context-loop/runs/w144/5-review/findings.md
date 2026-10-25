# Review of w144 (after the answer): initiative-round appends its ledger line with work note

**Verdict: DONE.** No finding is Critical and none is left to fix now. The first review's F1 was the gate dispatch and the round-2 integrate dispatch in integrating-a-proposal step 2 not naming the initiative. The person's answer of 2026-10-25 rules it: the work-item is accepted as it stands. I checked the reason the answer gives, and it holds:
- spec-integration lists r34 and r37 under `retired:` (line 7).
- w143 is `claimed`, and its fileset includes skills/integrating-a-proposal/SKILL.md, the file holding the "If the person is talking to you" section.

So F1 is now ruled and not open. F2 stays an observation.

## Commits reviewed

The branch `work/w144` is gone. The range runs from `9ff231e work: w144 ready -> claimed` to `200e433 work: w144 claimed -> done` and holds:
- `8ff0080 initiative-round appends its ledger line with work note (r40)`. It touches four files, all in the work-item's fileset: agents/initiative-round.md, scripts/supervise_worker.py, skills/formulating-features/SKILL.md and skills/integrating-a-proposal/SKILL.md.
- `b48662c` is in the range too. It is a `work:` commit of w143, so it is left out.

The implementer's result lists `6d5851d`. The first review showed that `6d5851d` and `8ff0080` have the same diff and that the hash differs only because the commit was rebased, so this is not a finding.

Since the answer, w144 has had no commit of its own. The only `work:` commits for it are `7f2a957 done -> awaiting-answer` and `05632c6 work answer: awaiting-answer -> done`. The fileset files have one later commit, `97299dc` to formulating-features, and it is not w144's.

## Removed and weakened tests

None. `git diff --stat 9ff231e 200e433 -- features tests` prints nothing. The plan's "Tests the decisions break" lists none.

## Allowances

The report says "none", and that holds: no test changed.

## Cannot verify

- That a live `claude -p` round under `work run` runs `python3 <Scripts>/work note …` and that the allowance `Bash(python3 <SCRIPTS>/work note *)` matches the command it runs. This is a guarantees work-item and no scenario covers it.
- Whether the round's ledger commit merges back cleanly. If a person runs `work note` on the initiative branch while a round is running, the merge can conflict (see the first review).
- The report's suite figures. I did not rerun the suite: `work run` runs it before merging.

## Findings

### F1. Important, ruled by the person's answer (work-item w144): no longer fix now
- skills/integrating-a-proposal/SKILL.md:21: the gate dispatch and the round-2 integrate dispatch do not name the initiative.
- The answer (2026-10-25) accepts the work-item as it stands. The section goes with w143, and r34 and r37 are retired. I verified both facts (above).
- **Triage: drop** (ruled).

### F2. Minor, observation (work-item w144)
- agents/initiative-round.md:38 does not say whether a round that ends `BLOCKED` appends a ledger line. r40 says "finishes a round", so it does not settle this.
- **Reproduction:** a reading only. The agent's "The ledger" paragraph does not mention `BLOCKED`.
- **Fix:** add one sentence that chooses a reading.

### Not findings (checked)
- Code no line asks for: the only code change is supervise_worker.py:45-46. It gives the rounds `work note` and no other `work` subcommand. That serves r40 and design-decision/the-ledger-is-tracked.
- No change under `features/`.

## Commands run
- `git log --format='%h %s' -1 --grep="^work: w144 ready -> claimed$"` → 9ff231e; `git log --format='%h %s' --grep="^work: w144 "`
- `git log --format='%h %s' 9ff231e..200e433`; `git show 8ff0080`
- `git log --format='%h %s' 200e433..HEAD -- <the four fileset files>` → 97299dc only
- `git diff --stat 9ff231e 200e433 -- features tests`: no output
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 9ff231e`:
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: no output, so no file is over the limit
- Grep for `r34|r37|r68` in spec/capabilities/spec-integration.md, for the dispatches in skills/integrating-a-proposal/SKILL.md, and for the status and fileset of w143.md
