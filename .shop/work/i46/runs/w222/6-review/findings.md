# Review of w222 (supervision r171, r172), round 6

**Verdict: DONE.** Nothing is Critical and nothing is triaged fix now. The commit writes one `drafted` glossary-proposal from an integrate round's glossary entries and includes it in the round's commit (r171). r172 holds because no apply route exists for a glossary-proposal. Review 5 raised one fix-now finding, the contradiction with supervision#r93 at `scripts/supervise_rounds.py:47`. It was answered on 2026-10-28: the code is accepted as it is, and r93's retirement is raised as a request. It is recorded below as an observation. The other findings are hardening and polish.

## Commits reviewed

- `606654ee5daa4dc0dbddac51f0ee248cceab4cec` "supervision r171, r172: an integrate round's glossary entry is written as a drafted glossary-proposal". This is the only commit the brief's `Commits:` gives. The implementer results name `4e45fc32`, which has the same subject and the same 6 files. Review 5 checked that it is the same change, rebased by `work run`'s merge, so this is not a finding.
- Suite: taken from the brief's record, not run: 1024 passed and 0 failed at 606654ee. The expected failures are w212's scenarios and those that now belong to w223, w224 and w225 (the person's answer of 2026-10-28).
- Files: CLAUDE.md, scripts/supervise_change.py, scripts/supervise_rounds.py, tests/scenarios/spec_integration_steps.py (outside the file set, declared in the report), tests/scenarios/supervision_integrate_steps.py, tests/scenarios/supervision_proposal_steps.py. `features/` is not touched.

## Removed and weakened tests

What I searched for: in the `-` lines of `git show 606654ee`, removed `def`s, `assert`s, parametrize cases, skip or xfail markers, and rewritten steps.

- `tests/scenarios/spec_integration_steps.py:113` (old line), step `drafts_glossary_change`, the Then of spec-integration#r54's scenario. The commit removes `assert not (repo / ".shop/work/i1/glossary.md").exists()`. Before, the step also proved that the integrate round wrote no `glossary.md`. Plan §4 does not list it ("None"). It is claimed under an allowance, and the allowance holds (see Allowances).

Nothing else was removed or weakened. The other `-` lines are two import lines that were widened, the module docstring, the CLAUDE.md row, and the r93 condition in production code.

## Allowances

- `interim`, `spec_integration_steps.py` `drafts_glossary_change`: **holds.** `git log -S'glossary.md").exists()' 134745663..606654ee` shows the assertion was first added in `085527d8` (spec-integration r54), after the base, and removed in 606654ee. Plan D1/D2 says `work run` now writes `glossary.md` from that entry. The step no longer asserts the opposite, and r54 itself says nothing about the file.

## Cannot verify

- That r171's scenario would have failed on an assertion rather than by looping. The 3-implement report says the run before the writer timed out at 120 s, and no red assertion was captured.
- That r172 still holds once r165's apply route for glossary-proposals is built (w225). Today it passes because the route is absent, and these commits cannot show more than that.

## Findings

### 1. Important, w222, observation (ruled): `scripts/supervise_rounds.py:47` departs from supervision#r93's text
r93 says a `started` initiative "has neither a capability-proposal nor a work-item" is given an integrate round. The commit adds `and not self.glossary_proposals()`, so an initiative that holds only a glossary-proposal gets none. On 2026-10-28 this was answered as accepted as it is: r93's wording is out of date, and its retirement for a line that names the glossary-proposal is raised as a request. No new question is needed. The contradiction stays until that request is delivered.

### 2. Important, w222, observation: `scripts/supervise_change.py:133-139` overwrites an existing `glossary.md`
Whenever a change list names the glossary, `write_proposals` writes `self.dir / "glossary.md"` from scratch. It does not check whether the file exists and does not merge. For capability-proposals, r148 handles this with `proposal_for`, `rewrite_lists` and `merge_lists` (lines 109-121). Here, a later integrate round in the same initiative (a re-integration under r141/r148) whose change list names the glossary again would reset an `awaiting-answer` or `approved` glossary-proposal to `drafted`. Its `## Questions` and `## Answers` would be lost, along with any terms the new entry does not name. No line or scenario covers a second glossary entry (plan §5, report's open questions).
Reproduction: reading lines 129-139. The path is fixed and nothing reads the file before writing it. No scenario drives two integrate rounds that both name the glossary, so I ran no probe.
Fix: first write a line saying what a second glossary entry does to an existing glossary-proposal (rewrite in place keeping status and Q&A, as r148 does, or merge as `merge_lists` does), then write the code.

### 3. Minor, w222, observation: `scripts/supervise_change.py:134` file name collides with a capability named `glossary`
A capability-proposal is written to `<capability>.md` (line 122). A capability named `glossary` would therefore be written to the same `glossary.md` in the same round, and the glossary-proposal would overwrite it. No capability has that name today (`ls spec/capabilities`).
Fix: give the glossary-proposal a name no capability can take, or refuse a capability named `glossary`.

### 4. Minor, w222, drop: new ruff findings in the new step code
- `tests/scenarios/supervision_integrate_steps.py:81`: RUF059, the unpacked `commit` is never used.
- `tests/scenarios/supervision_proposal_steps.py:137`: RUF100, unused `noqa: E731`.

Fix: write `_, _, text = found[0]` and drop the `noqa`.

## Checks

- `tools check --base 134745663`:
  - ruff: 26 errors. Two are new in this commit (finding 4). `supervise_change.py:91,118` B023 is in lines the commit did not change. The rest are in other files or in `.shop/` round scripts.
  - vulture: clean.
  - import-linter: the project states no import contracts.
- `tools size --limit 300`: printed nothing. The touched files have 140, 269, 246, 168 and 223 lines.
- Focused run of the two accepted scenarios (r171, r172): 2 passed.
- CLAUDE.md: the `supervise_change.py` row names the module's new concern. The `supervise_rounds.py` change sits inside that module's existing concern, the rounds.
- Code no line asks for: none. The glossary-proposal's fields serve r171. Its drafts sentence serves r170. The `glossary_proposals()` helper serves the r93 condition, which was ruled on.

## Commands run

- `cat .shop/work/i46/w222.md`; `ls -R .shop/work/i46/runs/w222`; `git log --stat -1 606654ee`
- `cat` of the plan, both implement reports and result files, and review 5's findings
- `git show 606654ee`; `git status --short`
- `grep -n -E "r93|r170|r171|r172|r165|rests_on" spec/capabilities/supervision.md`; `ls spec/capabilities`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 134745663cfa0a109b8564370c2464ef9ee9a7d5`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`; `wc -l` on the touched files
- `python3 -m pytest -q -n0 tests/scenarios/test_supervision.py -k "change_list_naming_the_glossary or glossaryproposal_awaitinganswer_with_a_question"`: 2 passed
- `git log --format="%h %s" 134745663..606654ee -S'glossary.md").exists()' -- tests/scenarios/spec_integration_steps.py`
- Read `scripts/supervise_change.py` lines 95-140
