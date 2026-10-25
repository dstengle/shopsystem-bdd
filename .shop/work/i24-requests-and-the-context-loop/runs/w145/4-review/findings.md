# Review of w145 (formulation#r14): formulating-features without a small-change path

**Verdict: DONE.** No Critical finding, none triaged fix now. The commit does what r14 and decision 0068 ask of the two files in its fileset. Two observations, one Important and one Minor, cover references this commit leaves dangling or in conflict. Both lie outside w145's fileset.

## Commits reviewed

The branch `work/w145` is gone. On HEAD, the commits from `121fade work: w145 ready -> claimed` to `d825d2f work: w145 claimed -> done` are:
- `97299dc` formulating-features: no small-change path; glossary rewording in a formulate round (the implementer's)
- `4968876` and `cd1e1b2`: `work run`'s own `work:` commits for w146 and w147. They are not w145's.

The implementer's result lists `a8a59c7`. `97299dc` is the same commit rebased by `work run`: same message, author, date and stat. `git diff a8a59c7 97299dc` differs only in `.shop/work/` files of w146 and w147. So the change is the one the result lists. No finding.

The change touches `agents/initiative-round.md` (+1/-1) and `skills/formulating-features/SKILL.md` (+6/-12). Both are in the fileset. Nothing under `features/` or `tests/` changed, and no Python changed.

## Removed and weakened tests

None. `git diff --stat 121fade d825d2f -- features tests` is empty. The commit touches only two Markdown files. No test reads skill or agent body text: the research notes §4 say so, and `tests/scripts/test_agents.py` reads frontmatter only, which this commit does not change.

## Allowances

The report's `## Tests changed under an allowance` says "none". There are no rows to verify.

## Cannot verify

- The report's run: `pytest --work-item w145`, 142 passed and 1 skipped. I did not rerun it. `work run` ran the suite before the merge.
- r14 is a guarantees line with no scenario, so whether a formulate round really does the reword can only be shown by `measure` on a real batch, not from the commit.

## Findings

### 1. Important, triage observation: `checking-spec-consistency` and spec-consistency#r6 still route rewording through a path that no longer exists (w145)

- **Where:**
  - `skills/checking-spec-consistency/SKILL.md:57`, which names the heading "The Small-Change Path". That heading is gone, now "A Word the Glossary Avoids".
  - `skills/checking-spec-consistency/SKILL.md:62,63,64`.
  - `spec/capabilities/spec-consistency.md:24` (r6: "reworded to its line through formulation's small-change path").
- **What is wrong:** after `97299dc`, fix mode of checking-spec-consistency tells the session to "write the reworded scenarios yourself" through a section that no longer exists. That breaks decision 0068 ("No skill tells a session to write spec or feature files itself (the small-change paths go)"), and a Behaviour line of another capability still asks for the old path.
- **Why it matters:** a session following fix mode has no path to follow. Spec and skill now disagree with formulation's Purpose and with 0068.
- **Why it is not w145's to fix:** the plan (Decision 3) kept it out of scope, and the implementer named it in the report. r6 changes only through integrating-a-proposal's gate, and no i24 work-item owns the file. `skills/integrating-a-proposal/SKILL.md:33,43,48-57` has the same dangling path; w143 owns that.
- **Reproduction:** `grep -n -i "small-change" skills/checking-spec-consistency/SKILL.md spec/capabilities/spec-consistency.md` prints l.53, 57, 59, 62, 63, 64 and r6.
- **Fix:** a capability-proposal that changes spec-consistency#r6 to "in a round of the kind `formulate`", then the work-item that rewrites the skill's fix mode.

### 2. Minor, triage observation: the Hand-back Template still has a session write the feature file (w145)

- **Where:** `skills/formulating-features/SKILL.md:114`: "The session verifies `git status --porcelain` as in step 2, writes the drafted scenario over the old one and commits".
- **What is wrong:** this text was already there before the commit, but it now contradicts the new line 16 of the same file ("No session writes a feature file."), the capability's Purpose and decision 0068.
- **Why it matters:** the skill tells a session to do what it forbids two sections up.
- **Fix:** r10's work owns it. Have it say the `formulate` round does it.
- **Reproduction:** `grep -n "session" skills/formulating-features/SKILL.md` prints l.16 and l.114.

### 3. Minor, triage observation: a step reword in another capability's scenario has no work-item to turn it green (w145)

- **Where:** `skills/formulating-features/SKILL.md`, "A Word the Glossary Avoids". A reword that changes a step's text deprecates the old scenario and adds a changed one "for a work-item to turn green".
- **What is wrong:** that capability is not one the capability-proposal names. `scripts/supervise_draft.py:35-53` (`draft_proposals`) drafts work-items only for the capabilities a formulated proposal adds or changes. So no work-item is drafted for it, and the reworded scenario stays red until someone notices.
- **Risk checked:** I named the risk "nobody drafts the turn-green work-item" and checked it with one look at `draft_proposals`. It holds.
- **Earlier behaviour:** the removed Small-Change Path had the same gap, so this is a gap carried over, not a new wrong answer. No line names this edge.
- **Fix, when a client meets it:** a line saying which work-item turns a reword's changed scenario green.

The Purpose and Behaviour of formulation are otherwise kept. The extra rule "the `v_t1` rows that reword's own check shows are not followed again in this round" serves r14 (it ends the round) and has no observable output beyond it. I made no finding of code that no line asks for.

## Checks

- `tools check --base 121fade`:
  - ruff: nothing to check
  - vulture: nothing to check
  - import-linter: the project states no import contracts
- `tools size --limit 300`: printed nothing. No tracked Python file is over the limit.

## Commands run

- `git log --format=%H -1 --grep="^work: w145 ready -> claimed$" work/w145`: refused, unknown revision (the branch is gone)
- `git log --oneline -30 --grep=w145`, `git log --oneline -12`, `git log --oneline 121fade..d825d2f`
- `git show --stat 97299dc`, `git show --stat a8a59c7`, `git diff a8a59c7 97299dc --stat`, `git show 97299dc`
- `grep -n -i "small-change|small change|session|talking to|the person" skills/formulating-features/SKILL.md agents/initiative-round.md`
- `grep -n -i "small-change|small change" skills/checking-spec-consistency/SKILL.md skills/integrating-a-proposal/SKILL.md spec/capabilities/*.md`
- `cat spec/decisions/0068-the-context-runs-without-a-coordinator.md`
- `grep -n "def |capabilit" scripts/supervise_draft.py`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 121fade`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
- `git diff --stat 121fade d825d2f -- features tests agents skills`
