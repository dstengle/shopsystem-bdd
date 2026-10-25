# Review of w137

**Verdict: DONE.** No finding is Critical and none is triaged fix now. There is one Important finding, triaged observation: a round's branch is merged without r6's put-back of `.shop/work/`. There are four Minor findings.

## Commits reviewed

- The `work/w137` branch is gone, so I read the commits on the checked-out history between `ecd3386 work: w137 ready -> claimed` and `d1921a3 work: w137 claimed -> done`. Other work-items' commits in that range (2a2c0de, 8a79d9c, a672127, 1a98149, 362abc2, 3aa3912) are not w137's.
- w137's one commit is `395fd37 work run: apply then formulate rounds for an answered capability-proposal (r70, r71, r80, r83)`.
- The implementer's result lists `6a37039` with the same message and the same diffstat: 8 files, +178/-12. 395fd37 is that commit rebased onto the initiative branch when it was merged (r61). Its content is the same, so this is not a finding.
- Files: CLAUDE.md, scripts/supervise.py, scripts/supervise_brief.py, scripts/supervise_rounds.py (new), scripts/supervise_worker.py, scripts/workqueue.py, tests/scenarios/supervision_rounds_steps.py (new), tests/scenarios/test_supervision.py.
- Nothing under `features/` changed.

## Removed and weakened tests

None. I searched the diff of `tests/` for:
- removed lines (`^-`): there are none;
- deleted `def test`, changed `parametrize`, removed or loosened `assert`;
- added `skip` or `xfail`.

The only change to an existing test file is one added import in `tests/scenarios/test_supervision.py`. Section 4 of the plan, "Tests the decisions break", says none.

## Allowances

The report's `## Tests changed under an allowance` says "none", and none is needed: no existing test changed.

## Cannot verify

- The report's figures: red 4 failed / 142 passed, green 146 passed, and touched modules 315 passed. I did not rerun the whole suite. I did rerun the four w137 scenarios (they pass, below).
- How a real `initiative-round` agent behaves under the `apply` and `formulate` tools: `READER` plus `git add`, `git commit` and `Agent`, with no Write or Edit, which leaves writes to acceptEdits. The tests use the stand-in for claude, so whether the real agent's subagents can write their drafts and spec files under this list is not shown. The report notes a related surprise: the drafts live in git-ignored scratch, which a round's worktree lacks.

## Findings

### 1. Important, observation: a round's branch is merged without r6's put-back
- **Where:** scripts/supervise_rounds.py:49-55, w137.
- **What is wrong:** `round()` merges `round/<p>-<k>-<kind>` into the initiative branch with `git merge` and never puts back the branch's changes under `.shop/work/`. supervision r6 says: "If a worker changes a file under `.shop/work/` outside its stage directory, then `work run` shall put the file back as it was." A round is a worker. The implementer's merge does this put-back through `Merge.under_work` (scripts/supervise_merge.py:55-66, called at :122), and a detached stage does it through `tree_changes` (supervise.py:155). The round path has neither.
- **Why it matters:** a round that commits a proposal file, a work-item or `log.jsonl` would have that change merged into the queue's history. The report names this as an open case.
- **Reproduction (by reading; no client sends this today):** `grep -n "under_work\|tree_changes" scripts/supervise_rounds.py` finds nothing. Under the initiative-round agent, the apply and formulate jobs commit `spec/`, `features/` and the rebound test files only, so this is hardening.
- **Fix:** before the merge, run the branch's `.shop/work/` changes through `under_work` (or refuse the merge as a round fault), as `merge()` does for an implementer.

### 2. Minor, drop: unused unpacked variable
- **Where:** scripts/supervise_rounds.py:49, w137.
- **What is wrong:** `data, failure = self.worker(...)` never uses `data`. ruff reports RUF059.
- **Fix:** `_, failure = ...`.

### 3. Minor, drop: a file outside the claimed file set
- **Where:** tests/scenarios/supervision_rounds_steps.py, w137.
- **What is wrong:** this new file is outside w137's `fileset:`, yet the report's "Outside the file set" says "None". The plan named `supervision_proposal_steps.py`, which already existed. The new module is the right home under CLAUDE.md's "a new concern gets a new module". But the file set is the claim (design-decision/the-file-set-is-the-claim), and the report should have named it there.
- **Fix:** none in code. The report should list the file.

### 4. Minor, observation: `move` allows more proposal statuses than plan decision 7
- **Where:** scripts/workqueue.py:18-19 and 150-152, w137.
- **What is wrong:** plan decision 7 gives a capability-proposal the statuses drafted, awaiting-answer, approved, formulated, merged and withdrawn. `move` instead allows the whole work-item lifecycle plus approved and formulated: `claimed`, `green` and `failed` are taken for a proposal, and `merged` is not.
- **Reproduction:** by reading line 151. `own = STATUSES + PROPOSAL_STATUSES` for a capability-proposal. No caller moves a proposal to a work-item-only status today.
- **Also:** the refusal still says "no status of the work-item lifecycle" for a proposal.
- **Fix:** a proposal's own tuple of statuses, as the plan gives.

### 5. Minor, drop: no turn limit for a round
- **Where:** scripts/supervise_worker.py:43-44, w137.
- **What is wrong:** plan decision 8 asked the implementer to set a round's turn limit and name it. `MAX_TURNS` has no `apply` or `formulate` entry. The report says so ("Round turn limit: none set").
- **Why it is Minor:** no line requires a limit; r19 is the researcher's only.

### Also reviewed and found sound
- **Merge and fault paths:** the round-branch merge (Q1 reading A) and the fault path that keeps the proposal and exits 1 (Q3 reading B) have no Behaviour line of their own. They follow the person's recorded answers on w137 and serve r70, r71, r80 and r83, so they are not "code no line asks for".
- **Q2:** a proposal with no questions starts apply, through the `>=` check in `due()`, which follows the answer to Q2.
- **The `keep_round` commit:** it is mechanism, so that the next run finds `.shop/work/` committed (r28) and starts the round again, as the Q3 answer says.
- **Loop termination:** `rounds()` ends. Each pass either moves the proposal on (awaiting-answer, then approved, then formulated) or raises `Refused`.
- **Order of git steps:** the worktree is removed before `git branch -d`, so the delete is not refused for a checked-out branch.

## Tools

- `tools check --base ecd3386`:
  - ruff: 2 rows. `scripts/supervise_rounds.py:49 RUF059` is w137's (finding 2). `scripts/workqueue.py:239 I001` is already there: those lines are from 7b769e8, before the claim.
  - vulture: clean.
  - import-linter: the project states no contracts.
- `tools size --limit 300`: printed nothing. The largest touched file is scripts/workqueue.py at 286 lines.

## Commands run

- `git log --format='%h %s' f890f2f..HEAD`; `git log --format='%h %p %s' ecd3386..d1921a3`
- `git show --stat 395fd37`; `git show --stat 6a37039`; `git diff 395fd37^ 395fd37`
- `grep` over scripts/supervise*.py, spec/capabilities/supervision.md, agents/initiative-round.md, skills/integrating-a-proposal/SKILL.md
- `sed -n` reads of supervise.py, supervise_worker.py, supervise_brief.py, supervise_merge.py
- `python3 -m pytest -q -p no:cacheprovider tests/scenarios/test_supervision.py -k "apply or formulat or approved"`: 4 passed
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base ecd3386`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `wc -l` of the touched files
- `git log -L235,242:scripts/workqueue.py`
