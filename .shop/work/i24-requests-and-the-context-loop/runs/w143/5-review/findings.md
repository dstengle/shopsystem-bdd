# Review of w143

**Verdict: DONE.** No Critical finding and nothing to fix now. The commit does what spec-integration#r35 and #r39 ask, and it removes the small-change path and the "If the person is talking to you" section, as design-decision/the-context-runs-without-a-coordinator requires. There are one Important observation (pointers in other skills to the removed path) and four Minor ones.

## Commits reviewed

- The branch `work/w143` is gone. Range on HEAD: `c86cd6a` (`work: w143 ready -> claimed`) .. `001bdca` (`work: w143 claimed -> done`).
- Non-`work:` commits in the range: `51208cc` "integrating-a-proposal and initiative-round: no small-change path, coordinator or gate cards; kind for job". It touches agents/initiative-round.md, scripts/supervise_brief.py and skills/integrating-a-proposal/SKILL.md (+18/-46). All three are in the work-item's fileset.
- The implementer's result lists `c5f4ecd`, which has the same subject and stat. `git diff c5f4ecd 51208cc` differs only under `.shop/` (the w144 review records and the log), so `51208cc` is the same patch, rebased when merged. This is not a finding.
- Also in the range are `847ef86` and `b5df407`. They are `work:` commits of w144 and w147, not w143's.

## Removed and weakened tests

None. `git diff --stat c86cd6a 001bdca -- features tests` is empty: no test file and no feature file changed. I searched tests/, scripts/, agents/, skills/ and hooks/ for `Job:`, `Kind:` and the small-change path. The only `Job:` was the label this commit changes (scripts/supervise_brief.py:33), and no test asserts it.

## Allowances

The report's `## Tests changed under an allowance` is "none". That matches the commits.

## Cannot verify

- The report's test run ("tests/scripts/test_agents.py and the supervision brief/round tests: 8 passed") and its suite record (798 passed). By the brief, I did not run them.
- That a `gate` round really gives its questions in result.json and that `work run` writes them on the proposal. No code starts a `gate` round yet, and the round path drops `questions` (scripts/supervise_rounds.py:49-55, per the plan). This is w146's work (supervision#r68, #r85, status drafted), not w143's.

## Findings

### 1. Important, observation: other skills still point at integrating-a-proposal's removed small-change path
- skills/checking-spec-consistency/SKILL.md:53, :59, :64 and skills/migrating-to-capabilities/SKILL.md:106 send a session through "integrating-a-proposal's small-change path" and its "Who Does What" dispatches ("a `initiative-round` with the job `integrate` ... as that skill's 'Who Does What' says").
- This commit removes both. The pointers now dangle, and they still tell a session to write lines itself, which decision 0068 forbids.
- The commit is not wrong in itself: the files are outside w143's fileset, and the plan named them for the branch review. But no i24 work-item covers them (no w*.md of i24 names either skill).
- Reproduction: `grep -rn -i "small-change" skills agents docs scripts tests` printed the lines above. `grep -ln "checking-spec-consistency\|migrating-to-capabilities" .shop/work/i24-requests-and-the-context-loop/*.md` printed nothing.
- Fix: a work-item under those skills' capabilities, so they go through `work run` rounds (formulating-features' small-change path goes too, w145).

### 2. Minor, observation: "job" left in agents/initiative-round.md:38
- Line 38 says "Run `work note` after your job's own commit". The plan (§2, "'job' becomes 'kind' throughout") and r40 use "kind".
- Fix: "after your kind's own commit" (or "the round's own commit").

### 3. Minor, observation: agents/initiative-round.md:38 still says "a dispatch names it"
- The initiative's name is said to come from "a dispatch". Under 0068 only `work run`'s brief starts a round.
- Fix: drop "a dispatch names it, and".

### 4. Minor, observation: the `apply` kind does not name `## Answers`
- agents/initiative-round.md:31 says "as the file of their answers". The capability's Implementation and the plan's Decision 5 say the `apply` kind is given the answers under the capability-proposal's `## Answers`. SKILL.md:18 says so; the agent's `apply` bullet does not.
- What it does still meets r39.
- Fix: "the answers under the capability-proposal's `## Answers`, or the approval in the person's words".

### 5. Minor, observation: SKILL.md:16 reads as forbidding what step 1 asks
- "No session writes spec, dispatches a writer, verifies a change list or keeps the gate". Yet the round this skill addresses dispatches the writer (step 1) and verifies the change list (step 2).
- The intent ("no session that talks to the person") is clear from the rest of the sentence, but the wording is loose.
- Fix: "No session the person talks to ...".

## Commands run

- `git log --format=%H -1 --grep="^work: w143 ready -> claimed$" work/w143`: unknown revision, so the branch is gone. The same grep on HEAD gave c86cd6a, and the `claimed -> done` grep gave 001bdca.
- `git log --format='%h %s' c86cd6a..001bdca`; `git show --stat 51208cc`; `git show --stat c5f4ecd`; `git diff c5f4ecd 51208cc --stat` (only .shop/ differs); `git show 51208cc`
- `grep -rn "Job:\|\"Job\|'Job\|Kind:" scripts tests agents skills hooks`: only supervise_brief.py:33 and initiative-round.md:25
- `grep -rn -i "small-change\|small change" skills agents docs scripts tests`: finding 1
- `grep -rn "job" ...`, `grep -rn "session" ...` on the two changed prose files: findings 2 and 5
- `grep -ln "r68\|r85" .shop/work/i24-.../w*.md`: w146 accepts supervision#r68, #r85 (drafted)
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base c86cd6a...`:
  - ruff: All checks passed!
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: printed nothing, so no file is over the limit
- `git diff --stat c86cd6a 001bdca -- features tests`: empty
