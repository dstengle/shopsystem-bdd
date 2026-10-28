# Review of w222 (supervision r171, r172)

**Verdict: DONE_WITH_CONCERNS.** The code does what r171 asks: one `drafted` glossary-proposal written from the change list's glossary entries and committed with the integrate round. r172 holds because no route exists for it to break. One Important finding is triaged fix now. Plan D3 makes `Rounds.due` skip an integrate round that supervision#r93's text asks for. The code is defensible, since taking r93 literally would loop on a glossary-only initiative, but the line has to be reworded first so it agrees with the code.

## Commits reviewed

- `606654ee5daa4dc0dbddac51f0ee248cceab4cec` "supervision r171, r172: an integrate round's glossary entry is written as a drafted glossary-proposal". Both implementer results name `4e45fc32`, which has the same subject. `git show --stat` of the two gives the same 6 files with the same counts (82+/6-), so 606654ee is 4e45fc32 rebased by `work run`'s merge. The two commits are the same. This is not a finding.
- Suite: from the brief's record, 1024 passed and 0 failed at 606654ee. The expected failures are w212's and those of w223/w224/w225 by the person's answer of 2026-10-28. I did not run the suite.
- The 4-implement session wrote no code and saw no red run. The 3-implement session saw r171 red only as undefined steps. r172 was red only as undefined steps and passes by absence, as plan D5 says.

## Removed and weakened tests

What I searched for in the diff: removed `def`s, `assert` lines, parametrize cases, skip/xfail, and rewritten steps. Commands: `git show 606654ee` (I read the whole diff), then a grep of its `-` lines.

- `tests/scenarios/spec_integration_steps.py` `drafts_glossary_change` (the Then of spec-integration#r54's scenario "the round drafts a change to the glossary"). The diff removes `assert not (repo / ".shop/work/i1/glossary.md").exists()`. Before, the step also proved that no glossary.md was written. Now it proves only that the brief and the change list carry the glossary entry. Plan §4 says "None" and does not list it. The report claims it under an allowance (see below).

Nothing else was removed or weakened. The other `-` lines are an import line and the r93 condition line in production code.

## Allowances

- `interim`, `tests/scenarios/spec_integration_steps.py` `drafts_glossary_change`: **holds.** The assertion was first committed in `085527d8` ("spec-integration r54: ..."), and `git merge-base --is-ancestor 134745663 085527d8` confirms that commit comes after the base. spec-integration#r54 says nothing about whether a glossary-proposal file exists. The step now asserts what plan D1/D2 says, namely that glossary.md is written by `work run` (supervision#r171). Plan §4 was wrong to say no test breaks, and the report says so.

## Cannot verify

- That r171's scenario would fail without the D3 change by asserting, not by looping. The 3-implement report says the run before the writer timed out at 120 s ("the loop the plan's D3 predicts"). No red assertion was captured for either Then.
- r172 was never red on an assertion. It passes because no apply route for glossary-proposals exists (r165 belongs to w225). Whether r172 still holds once r165 is built cannot be checked from these commits.

## Findings

### 1. Important, w222, fix now: `scripts/supervise_rounds.py:47` contradicts supervision#r93
r93: "**When** an initiative is `started` and has neither a capability-proposal nor a work-item, `work run` shall start a round of the kind `integrate` ...". The commit adds `and not self.glossary_proposals()`. A started initiative that holds only a glossary-proposal gets no integrate round, which is the opposite of what r93's text says. The plan (D3) justifies this with decision 0073 ("an initiative that changes only the glossary is delivered with no capability-proposal"), with r93's intent ("left nothing behind"), and with the loop that taking r93 literally would cause under r171. The reasoning is sound, but the behaviour now rests on a reading of r93, not on a line. Why it matters: r93's scenario and any later reader of r93 will expect the literal behaviour, and `model check` cannot see the discrepancy. Fix: keep the code and retire r93 for a new line through integrating-a-proposal, e.g. "... has neither a capability-proposal, a glossary-proposal nor a work-item ...", with its scenario moved onto the new id.

### 2. Important, w222, observation: `scripts/supervise_change.py:132-138` overwrites an existing glossary-proposal
`write_proposals` always writes `glossary.md` from scratch. A later integrate round in the same initiative can be a re-integration of a capability-proposal with answers (r141, r148). If its change list names the glossary again, it replaces an existing glossary.md, which may be `awaiting-answer` with `## Questions`/`## Answers` or even `approved`. The status resets to `drafted`, and the questions, answers and terms the new entry does not name are lost. For capability-proposals r148 keeps this from happening. For glossary-proposals no line covers it (plan §5 and the report's open questions raise it). Reproduction: reading lines 132-138. The path is fixed (`self.dir / "glossary.md"`) and there is no `exists()` check or merge. I ran no probe because no scenario drives a second integrate round naming the glossary. Fix: a line that says what a second glossary entry does (rewrite in place keeping status/Q&A as r148 does, or merge as `merge_lists` does), then the code for it.

### 3. Minor, w222, observation: `scripts/supervise_change.py:133` file-name collision with a capability named `glossary`
The capability-proposal for a capability `glossary` is `glossary.md` too (line 122), so the second write overwrites the first in the same round. No capability has that name today (`ls spec/capabilities`). Fix: give the glossary-proposal a name no capability can take, or refuse a capability named `glossary`.

### 4. Minor, w222, drop: new ruff findings in new test code
`tools check` reports two new findings in lines this commit added: `tests/scenarios/supervision_integrate_steps.py:81` RUF059 (unpacked `commit` never used) and `tests/scenarios/supervision_proposal_steps.py:137` RUF100 (unused `noqa: E731`). Also, the r171 Then "the commit that wrote i1's glossary-proposal" does not check that the commit it finds is the integrate round's commit, only that exactly one commit added such a file. Fix: `_, _, text = found[0]` and drop the `noqa`.

## Checks

- `tools check --base 134745663`: ruff found 24 errors. The two named in finding 4 come from this commit. `supervise_change.py:91,118` B023 is outside the diff's hunks, so it predates this commit. The rest are other files or `.shop/` scratch scripts. vulture: clean. import-linter: no contracts stated.
- `tools size --limit 300`: nothing printed. The touched files have 140, 269, 246 and 168 lines.
- CLAUDE.md: the module-map row for `supervise_change.py` was updated for the module's new concern. No new module was added, so no new row was needed.
- `features/`: the commit does not touch it.

## Commands run

- `cat .shop/work/i46/w222.md`, `ls -R .shop/work/i46/runs/w222`, `git show --stat 606654ee`
- `git show 606654ee`; the plan, both reports and both result.json files read with `cat`
- `git log --oneline -1 4e45fc32`, `git show --stat 4e45fc32`, `git merge-base --is-ancestor 134745663 085527d8`, `git show 085527d8 --stat`
- `grep -n` for r93/r159/r171/r172/glossary in `spec/capabilities/supervision.md`; `grep` for r54/r55 in `spec/capabilities/spec-integration.md`
- `cat spec/decisions/0073-the-glossary-is-a-target-of-spec-work.md`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 134745663...`, `python3 .../tools size --limit 300`, `wc -l` on the touched files
- `sed -n` on `scripts/supervise_change.py` (60-140), `tests/scenarios/spec_integration_steps.py` (100-115), `tests/scenarios/supervision_integrate_steps.py` (76-84)
