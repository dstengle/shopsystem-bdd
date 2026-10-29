# Review of w230 (supervision r209, r210)

**Verdict: DONE_WITH_CONCERNS.** The code and steps do what r209 and r210 ask, and every removed test is listed in the plan. One Critical finding: the commit removes a scenario from `features/supervision.feature` although w230 has no `## Retires` section listing it. The removal is a reasoned plan decision (D2), but under the review rules only the person can accept it.

## Commits reviewed

- `998966626eaac9e687ab55d5463ca3600d54a9b3` "supervision: a question outside a glossary-proposal goes to a session whatever words it names (r209, r210)". This is the brief's `Commits:`.
- Both implementer results list `051b2b9d`. That is the same change rebased by `work run`: `git show --stat` of each gives the same 5 files and the same +29/-73, and `git diff 051b2b9d 9989666 --stat` differs only under `.shop/`. This is not a finding.
- Files: `features/supervision.feature`, `scripts/supervise_answers.py`, `scripts/supervise_glossary.py`, `tests/scenarios/supervision_delegation_steps.py`, `tests/scripts/test_supervise_answers.py`. All are within the work-item's fileset.
- Suite: taken from the brief's record: 1066 passed, 0 failed at 99896662. The xfails are w212's expected requests scenarios.

## Removed and weakened tests

What I searched for:
- deleted `def test_`;
- removed Scenario/Examples rows;
- removed `assert` lines;
- added `skip` or `xfail`;
- step regexes whose assertion changed.

What I found:
1. **`tests/scripts/test_supervise_answers.py::test_a_question_names_a_term_of_the_glossary_or_a_glossary_proposal_as_a_whole_word_in_any_case`** was deleted.
   - It proved that `supervise_glossary.names_one` matches a glossary term or a glossary-proposal name as a whole word, in any case, and rejects partial words.
   - That is the r162 rule, which the capability retires (line 7, `retired:`).
   - Listed in plan §4 "Tests the decisions break": yes.
2. **`features/supervision.feature` @r162 @deprecated outline** "under a delegation, a question of the initiative that names <named> is left for the person and given to no session (deprecated)", with both examples, was removed.
   - It proved that a w1 question naming the term "ledger" or the glossary-proposal g1 went to no session and stayed unanswered.
   - Listed in plan §4: yes.
   - The removal itself is Finding 1.
3. Step definitions in `supervision_delegation_steps.py` were widened, not weakened:
   - `two_unanswered` now takes `w\d+` instead of only w1 and writes the same file shape.
   - `question_unanswered` now takes `w1|g1` and makes the same assertion on the named file.
   - The g1 Given now takes an optional `## Questions`; without one it writes the same file as before.
   - The steps the r163 outline and the r77 scenario use still assert the same thing.

## Allowances

The report's `## Tests changed under an allowance` says "none". There are no rows to verify.

## Cannot verify

- **The red runs in 3-implement's report** (4 failed on undefined steps, then r210 failing on its Then): the commits cannot show them, since the change landed as a single commit. The code path supports the claim: before the change, `names_one` at `supervise_answers.py:75` kept w2's g1-naming question from any session.
- **"Suite at start: 1065 passed, 4 failed"** in 3-implement's report: this is not checkable from the commits.

## Findings

### 1. Critical, fix now: `features/supervision.feature:1334` (base): the r162 deprecated outline was removed without a Retires entry

- **What is wrong.** The commit removes the @r162 @deprecated Scenario Outline (19 lines). w230 (`.shop/work/i51/w230.md`) has no `## Retires` section, and nothing lists this scenario. A change under `features/` is allowed only when it removes, with its binding, a deprecated scenario that the work-item lists under Retires. The binding is `scenarios("supervision.feature")`, which binds the whole file, so no per-scenario binding was left behind.
- **Why it matters.** Scenarios are retired by `work run` through a Retires list (r73) or the r123 retiring work-item, not by an implementer. Here the implementer chose to retire one (plan D2).
- **Mitigating facts (verified).**
  - r162 is in the capability's `retired:` list.
  - The person approved retiring r162 on 2026-10-29 (`.shop/work/i51/supervision.md:40-41`).
  - Under r210 the outline can no longer pass, so keeping it would fail w230's whole-suite gate (r4).
  - r73 did not list it because its `Deprecated for: r209 and r210` names requirements, not a scenario. That is a drafting gap the research noted (notes §3).
- **Fix.** The person rules on it. Either record the outline under w230's `## Retires` as a ruling, which accepts the removal as made, or restore it and retire it through r123's retiring work-item, with the gate's handling of the now-red outline settled. The r73 reading of a `Deprecated for:` line that names requirement ids may also need its own request.

### 2. Minor, observation: `CLAUDE.md` module map, row `scripts/supervise_glossary.py`

- **What is wrong.** The row still says the module gives "the questions under a delegation that name a term or a glossary-proposal, left for the person (supervision r162)". The commit deleted that function (`names_one` and its helpers).
- **Why it matters.** The map now describes a concern the module no longer has.
- **Fix.** Reword the row to the glossary-proposal withholding only. `CLAUDE.md` is outside w230's fileset.
- **Reproduction.** `grep -n supervise_glossary CLAUDE.md` shows the row. `grep -rn names_one scripts tests` finds nothing.

### 3. Minor, drop: `tests/scripts/test_supervise_answers.py:9,10,36,51`: existing `tools check` warnings

- **What is wrong.** `tools check` reports RUF100 unused `noqa` at lines 9 and 10, and vulture reports an unused `args` at lines 36 and 51. The commit touched this file but not these lines; the warnings were there before it.

### Behaviour against the capability

- `Answers.asking` (`supervise_answers.py:51-58`) lists only awaiting-answer work-items and capability-proposals. A glossary-proposal's question therefore goes to no session (r209).
- `Answers.answers` now asks every open question, whatever words it uses (r210).
- Nothing contradicts a Behaviour line.
- The commit adds no code that no line asks for: it only removes code that served the retired r162.

## Commands run

- `git show --stat 9989666`; `git show 9989666` (the whole diff)
- `git log --oneline -1 051b2b9d`; `git log --oneline -4 9989666`; `git diff 051b2b9d 9989666 --stat`; `git show --stat 051b2b9d`
- `grep -n "r162\|r163\|r209\|r210\|r123\b\|r73\b\|Retires\|rests_on\|retired" spec/capabilities/supervision.md`
- `grep -rn -e r162 -e names_one -e terms_of -e proposals_of -e "scenarios(" tests scripts`: no production or test references remain. `terms_of` in `supervision_proposal_steps.py` is a separate local helper.
- `grep -n -e "Glossary holds the term" -e "was given to no session" -e "glossary-proposal g1 is awaiting-answer" features/*.feature`: the widened steps are still used.
- `grep -n ... .shop/work/i51/supervision.md .shop/work/i51/initiative.md`: the person's approval of r209/r210 and the retirement of r162/r163.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 1db40f6e`:
  - ruff: 2 RUF100 in `test_supervise_answers.py`, existing (Finding 3);
  - vulture: 2 unused `args`, existing (Finding 3);
  - import-linter: no contracts.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: printed nothing, so no file is over 300 lines.
