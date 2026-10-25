# Report w181

## Budget
scripts/supervise_change.py, supervise_rounds.py, supervise_brief.py, supervise_analysis.py, supervise_done.py (new), supervise.py, workqueue_done.py, CLAUDE.md, tests/scenarios/supervision_integrate_steps.py, supervision_proposal_steps.py, supervision_analysis_steps.py, supervision_done_steps.py (new), test_supervision.py (13 files).

## Changed
- r107: `Changes.unknown` checks each named capability against spec/capabilities/ and the round's kept drafts. All unknown: round kept as r96 keeps it, error naming them. Some unknown: known proposals written and committed, then error naming the unknown.
- r108: proposals name the kept `drafts/round-<highest>/` path (trailing slash); gate/apply briefs get a `Drafts path:` line and the path in Read.
- r106: `analyse` commits measurement + record, then pushes.
- r105/r109: new `supervise_done.Dones.set_done` (called after `analyse` in `pull_through`), `workqueue_done.holds` public; commit message `work: i1 started -> done`. Records read from git. CLAUDE.md module row added.

## Red and green
Suite at start: 874 passed, 6 failed at 1fa62ff7 (the w181 scenarios among them).
- r107 red run: assertion `not (.shop/work/i1/nowhere.md).exists()` failed (proposal written, no error) — expected. r108 red: both examples failed on `Drafts path:` missing from the brief. r106 red: `ls-files` of the measurement empty (untracked). r105/r109: I wrote steps and production code together and did not re-run red after the steps (red was the undefined Given, per research notes); a deviation from the cycle.
- Final: `python3 -m pytest -q --work-item w181` → 148 passed, 1 skipped (the shell's option selects all of w181's scenarios plus helper tests); test_supervision.py → 6 passed (only w181's scenarios; the shell's PYTEST_ADDOPTS `--work-item w181` filters the rest, so other supervision scenarios (r92 line 1173 etc, r75/r76) were NOT run by me).

## Tests changed under an allowance
none

## Open questions
- Integrate round with no kept `drafts/round-<m>/`: the proposal names the stage directory (old behaviour); gate/apply then get that as their Drafts path. Unchosen otherwise.
- Proposals written before this change (sentence names a stage dir): they are given as-is.
- Analysis cut short / no record: nothing committed; no done.
- A rerun after analysis committed earlier: `measure initiative` behaviour unchanged.
- Push failures follow `self.push()`.
- `work run` with no initiative does not print a just-set-done initiative specially.

## Other
The plan contained no code. `tools size --limit 300` printed nothing. Nothing outside the file set.

Commits: c8df2363, 99d9953b, 4800cd94, 58fd30aa.
