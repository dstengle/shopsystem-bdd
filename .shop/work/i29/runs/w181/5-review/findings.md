# Review of w181 (i29-supervision: r105–r109)

**Verdict: DONE.** No Critical finding, nothing triaged fix now. One Minor lint finding (observation).

## Commits reviewed

The branch `work/w181` no longer exists. The commits are therefore those between `307f8496 work: w181 ready -> claimed` and `a7102a44 work: w181 claimed -> done` on the checked-out history, leaving out `work run`'s own commits (w180/w184 moves, the i25/i27 branch reviews, w186/w187 drafted):

| On HEAD | Implementer's result | Subject |
|---|---|---|
| 4d3113e1 | c8df2363 | r107: a change list naming a capability nothing has gives no proposal and an error |
| 5048b72e | 99d9953b | r108: gate and apply rounds are given the kept drafts path |
| c482f4f8 | 4800cd94 | r106: commits the measurement and the analysis record |
| 07d5c24c | 58fd30aa | r105, r109: sets an initiative done and commits it |
| d87a295b | 25440376 | tests: the r92 scenario's repository holds the capability other |

`work run` re-applied the commits when it merged them, so their hashes differ from the ones in the results, but they are the same commits. Subjects match one for one. `git diff 25440376 d87a295b` over all 13 touched files is empty. No commit is missing and none is extra. (`0bd4ae49`, named in the second brief's suite record, is an earlier copy of the r105/r109 commit with the same subject.)

Files changed: CLAUDE.md (module row), scripts/supervise.py, supervise_done.py (new), workqueue_done.py, supervise_analysis.py, supervise_brief.py, supervise_change.py, supervise_rounds.py; tests/scenarios/supervision_{integrate,proposal,analysis,done(new)}_steps.py, test_supervision.py. Nothing under `features/`.

## Removed and weakened tests

None. I searched the test diff for removed lines (`^-`), deleted `def`s, changed or removed `assert`s, parametrize edits, `skip`/`xfail` and renamed steps. The only test line removed is the signature of `integrate_with_changes` (supervision_integrate_steps.py:43), which gains the `repo` fixture. Its pattern and the Thens it serves are unchanged (see Allowances). Everything else in the test diff is additions: new steps for r105–r109 and the `supervision_done_steps` import.

## Allowances

- 3-implement report: none.
- 4-implement report, `tests/scenarios/supervision_integrate_steps.py`, `integrate_with_changes` (the r92 scenario's Given), **setup**: **holds**. The diff adds a write and commit of `spec/capabilities/other.md`. It adds, removes or changes no `assert`, no expected value and no parametrize case. `proposals_written` (:146) still asserts the same two proposals. The scenario still proves r92 (one drafted proposal per named capability). r107 now needs the capability to exist somewhere, so the repository has to hold `other`; this is the fix plan §4 predicted. Note: the coordinator's answer calls :146 "the r107 scenario's assertion". It is in fact the r92 scenario (w167's), and it now passes because of this setup change, not because of any change to the assertion.

## Cannot verify

- The whole suite on the merged result. I did not run it (that is `work run`'s job). The implementer did not run the r75/r76 analysis scenarios or the work-queue done scenarios (work-queue.feature :57, :75) under the `--work-item` filter. Plan §4 argues they are unaffected, and from the diff I agree: `_holds`, `becomes` and `mark` are unchanged, and `holds` only wraps `_holds(..., {})`.
- The r107 path where some named capabilities are known and some are not (proposals committed, then refused). It follows from the code (supervise_rounds.py:103–119), but no scenario exercises it.
- The open cases of plan §5 that the report names without a scenario: a later run of an initiative whose analysis was committed earlier but whose request was undelivered then (`analyse` and `measure initiative` run again before `set_done`); a push failure after the records' commit. If the records' commit fails, `git` raises `GitFailed`, which is a `Refused`, so `work run` exits with an error rather than crashing (checked: supervise_worker.py:62–71).
- The 3-implement report admits that r105/r109 were not run red after their steps were written. I cannot check this from the commits; the steps they bind were undefined before w181.

## Findings

1. **Minor, observation**: scripts/supervise_analysis.py:10 (ruff I001, reported at :4). w181 added `git` to the `from supervise_worker import …` line, which made it 123 characters (it was 119). `tools check` now flags the import block as unformatted (I001), most likely because of the line width. Why it matters: lint is no longer clean on a file w181 touched. Fix: wrap the import or shorten the trailing comment. Reproduction: `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 307f8496` → `scripts/supervise_analysis.py:4:1: I001 [*] Import block is un-sorted or un-formatted`. The other three ruff findings (supervise_brief.py:89 ISC004, supervision_proposal_steps.py:96 RUF100, test_supervision.py:14 I001) are on lines w181 did not change. The test_supervision.py import w181 added is in sorted position. I take those three as already there.

What I checked against the lines, with nothing found:
- r107: `Changes.unknown` counts a capability as had if it is in `spec/capabilities/` or in any `drafts/round-*/spec/capabilities/` of the round. If every named capability is unknown, the round is refused through `refuse_integrate`, which names them (r96 keeps the round). If only some are unknown, proposals are written for the known ones (r92) and the run is then refused, naming the unknown ones. No proposal is written for an unknown capability, and the error names it. This matches r107.
- r108: `kept_path` gives the highest-numbered `drafts/round-<m>/` with a trailing slash. The gate and apply briefs read it back from the proposal's sentence and add a `Drafts path:` line plus a Read entry. I checked by reading that the regex `(\S+?)\.(?:\s|$)` survives the leading-dot `.shop/` and a trailing `/.`.
- r106: one commit of exactly the measurement and the record, then a push (r38).
- r105: `set_done` runs only inside the `lists_nothing(kept)` branch, after `analyse`. It needs the initiative not done, records tracked and clean in git (decision 6), and `workqueue_done.holds` (at least one work-item, each green or withdrawn, this context's requests delivered).
- r109: `Run.commit` of initiative.md and log.jsonl, then a push.
- No code with observable behaviour outside a line. The log line and the commit messages are the mechanism of r7 and r38. The fallback to the stage directory when no round was kept serves r108's open case.
- Size: `tools size --limit 300` printed nothing.

## Commands run

- `git log --format=%H -1 --grep="^work: w181 ready -> claimed$" work/w181` → branch gone; then the same grep on HEAD → 307f8496, done → a7102a44
- `git log --format='%h %s' --stat 307f8496..a7102a44`
- `git log --no-walk c8df2363 99d9953b 4800cd94 58fd30aa 25440376`, `0bd4ae49`
- `git diff --stat 25440376 d87a295b -- <the 13 files>` → empty
- `git diff 4d3113e1^ d87a295b -- scripts CLAUDE.md`, `-- tests`
- `grep -nE "^\- \[r(10[5-9]|92|96|38|75|76|84)\]" spec/capabilities/supervision.md`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 307f8496` → ruff: 4 errors (1 on a line w181 changed, above); vulture: clean; import-linter: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` → nothing printed
- `git show 307f8496:scripts/supervise_analysis.py`, `git show 307f8496:tests/scenarios/test_supervision.py`; `wc -c` of line 10 before and after
- Grep of `GitFailed`, `def git`, `def commit`, `def push` in scripts/
