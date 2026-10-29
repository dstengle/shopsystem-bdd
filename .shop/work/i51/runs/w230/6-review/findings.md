# Review 6 of w230 (supervision r209, r210)

**Verdict: DONE.** The commit does what r209 and r210 ask. Every removed test is listed in plan §4. The Critical finding of review 5 was the removal of the @r162 outline. The answer of 2026-10-29 in w230's `## Answers` settles it: that outline is retired with r162, so the removal stands. Nothing is triaged fix now and nothing is Critical. Two Minor findings remain.

## Commits reviewed

- `998966626eaac9e687ab55d5463ca3600d54a9b3` "supervision: a question outside a glossary-proposal goes to a session whatever words it names (r209, r210)". This is the brief's `Commits:`. Its parent is `1db40f6e work: w230 ready -> claimed`.
- Both implementer results list `051b2b9d`, the same change before `work run` merged it. Review 5 verified this: the same 5 files and +29/-73, with differences only under `.shop/`. This is not a finding.
- Files changed: `features/supervision.feature`, `scripts/supervise_answers.py`, `scripts/supervise_glossary.py`, `tests/scenarios/supervision_delegation_steps.py`, `tests/scripts/test_supervise_answers.py`. All are in w230's fileset.
- Suite: taken from the brief's record: 1066 passed, 0 failed at 99896662. The expected failures are w212's requests scenarios.

## Removed and weakened tests

I searched the diff for:
- deleted `def test_`;
- removed Scenario or Examples rows;
- removed `assert` lines;
- added `skip` or `xfail`;
- step patterns whose assertion changed.

What I found:

1. **Deleted: `tests/scripts/test_supervise_answers.py::test_a_question_names_a_term_of_the_glossary_or_a_glossary_proposal_as_a_whole_word_in_any_case`.**
   - It proved that `supervise_glossary.names_one` matches a glossary term or a glossary-proposal name as a whole word, in any case, and rejects partial words.
   - That is the r162 rule. r162 is in the capability's `retired:` list.
   - Listed in plan §4 "Tests the decisions break": yes.
2. **Removed: the `features/supervision.feature` @r162 @deprecated outline** (both examples).
   - It proved that a w1 question naming "ledger" or g1 went to no session and stayed unanswered.
   - Listed in plan §4: yes.
   - It is retired by the person's answer of 2026-10-29 in w230 ("Retires: the @r162 deprecated outline at features/supervision.feature:1334 is retired with r162 ... its removal stands").
   - The binding is `scenarios("supervision.feature")`, which binds the whole file, so no per-scenario binding is left behind.
3. **Steps widened, not weakened**, in `supervision_delegation_steps.py`:
   - `two_unanswered` takes `w\d+`;
   - `question_unanswered` takes `w1|g1`, with the same assertion;
   - `glossary_proposal_awaiting` takes an optional `## Questions` and writes the same file without one;
   - two new Thens for r210.

   The steps that the r163 outline and the r77 scenario use assert the same as before.

## Allowances

The report's `## Tests changed under an allowance` says "none". There are no rows to verify.

## Cannot verify

- **The red runs claimed in 3-implement's report.** The change landed as one commit, so the commits cannot show them. The code path supports the claim: before the change, `names_one` (old `supervise_answers.py:75`) kept w2's questions from any session.
- **The whole-suite pass after the fixture race of the first run.** I take it from the brief's suite record and did not re-run it.

## Findings

### 1. Minor, observation: the Retires ruling is recorded only as an answer (`.shop/work/i51/w230.md`)
- **What is wrong.** w230 still has no `## Retires` section. The retirement of the r162 outline is recorded only in `## Answers` (2026-10-29).
- **Why it matters.** A reader of the work-item looking for what it retires finds no `## Retires` heading, and review 5's Critical rested on its absence.
- **Fix.** If `work run` records rulings in their own section, write the answer there as well. This needs no code change.
- **Reproduction.** `grep -n "^## " .shop/work/i51/w230.md` gives only `## Questions` and `## Answers`.

### 2. Minor, observation: `CLAUDE.md:37`, row `scripts/supervise_glossary.py`
- **What is wrong.** The row still says the module gives "the questions under a delegation that name a term or a glossary-proposal, left for the person (supervision r162)". The commit deleted `names_one`, `terms_of` and `proposals_of`.
- **Why it matters.** The module map describes a concern the module no longer has.
- **Fix.** Drop that clause from the row. `CLAUDE.md` is outside w230's fileset, so this belongs to a later work-item or the initiative's close.
- **Reproduction.**
  - `grep supervise_glossary|names_one|terms_of|proposals_of` (excluding `.shop/`) finds the CLAUDE.md row.
  - The only `terms_of` left is an unrelated local helper in `tests/scenarios/supervision_proposal_steps.py`.

### Not findings (risks checked)
- **Unused import in `supervise_glossary.py`.** The risk was that `import re` became unused after `names_one` was deleted. It is still used at line 62 (`terms_in`), and ruff reports nothing for the file.
- **r209: a glossary-proposal's question reaching a session.** `Answers.asking` (`supervise_answers.py:51-58`) lists only work-items and capability-proposals, so a glossary-proposal's question goes to no session.
- **r210.** `answers` (line 74) now asks every open question, whatever its words.
- Nothing contradicts a Behaviour line or the Purpose.
- The commit adds no code that no line asks for: it only removes the r162 mechanism.

## Commands run

- `git show 998966626eaac9e687ab55d5463ca3600d54a9b3 -- . ':!.shop'` (the diff)
- `git log --oneline -3 9989666`
- `git log --format=%H -1 --grep="^work: w230 ready -> claimed$"` gave `1db40f6e`.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 1db40f6e…`:
  - **ruff:** 2 RUF100 (unused `noqa`) at `tests/scripts/test_supervise_answers.py:9,10`. Those lines were there before the commit, which touched only the end of the file.
  - **vulture:** unused `args` at `test_supervise_answers.py:36,51`, also there before.
  - **import-linter:** the project states no import contracts.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: printed nothing, so no file is over the limit.
- Greps:
  - imports of `supervise_glossary.py` and `supervision_delegation_steps.py`;
  - `r162|r163|r209|r210|retired:` in `spec/capabilities/supervision.md`;
  - `supervise_glossary|names_one|terms_of|proposals_of` across the tree.
- Read:
  - `features/supervision.feature:1290-1380`;
  - `scripts/supervise_answers.py:40-89`.
