# plan of w214 (supervision r149, r150, r151, r152, r153)

From the research notes (`.shop/work/i42/runs/w214/1-research/notes.md`), the capability, the accepted scenarios and the
answers on the proposal `.shop/work/i42/supervision.md` (gate rounds 1 and 2, 2026-10-28), which count as rulings here.

## 1. What goes green

- **supervision#r149**: "a formulate round that formulates nothing because the proposal's answers change lines not in
  spec/ is followed by a new integrate round for the proposal" (features/supervision.feature:1503). Red: the Given "the
  formulate round for p1 formulates nothing, giving that p1's answers change lines not in spec/" and the Then "a round of
  the kind integrate was started for p1 after the formulate round had ended" are undefined; in code, `Rounds.route`
  sends an answered proposal whose last move came from approved back to formulate, never to integrate.
- **supervision#r150**: "an apply round that gives an answer the drafts it applied do not hold is followed by a new
  integrate round for the proposal" (1070). Passes today (run, by the researcher) through the `nothing_applied` path. It
  must stay green. Decision 2 widens the code to what r150 says.
- **supervision#r151**: "an apply round that gives an answer the drafts it applied do not hold is followed by no
  formulate round for the proposal before the new integrate round's drafts are applied" (1080). Red: the Then "no round
  of the kind formulate was started for p1" is undefined. The flow already holds (read): apply nothing, then integrate,
  then drafted, then gate, then awaiting-answer.
- **supervision#r152**: "... leaves the proposal's status as it was" (1513). Red: the Given and both Thens ("p1 was
  awaiting-answer when the formulate round for p1 had ended", "no transition of p1 was made between the start of the
  formulate round for p1 and the start of the integrate round for p1") are undefined. In code, the formulate branch of
  `Rounds.run_round` moves the proposal to `formulated` when no question is given.
- **supervision#r153**: "... has given its output" (1524). Red: the Given variant ", and no scenario" and the Then "no
  question naming the formulate round's output as missing was written under p1's ## Questions" are undefined. In code,
  the formulate branch asks `supervise_outputs.unformulated`'s missing scenarios as a question.
- **Retired**: the `@r140 @deprecated` scenario "an apply round that applies nothing because the proposal's answers give
  what its drafts do not hold is followed by a new integrate round for the proposal (deprecated)"
  (features/supervision.feature:1059-1069) is removed, as the work-item's Retires names it. Its binding in
  tests/scenarios/test_supervision.py goes with it if it has one. Run `features bindings` to find out.

## 2. Where the change lands

- `scripts/supervise_rounds.py`: `route` sends a proposal back to integrate when its latest round (failed integrate
  rounds aside, as `applied_nothing` does today) sent it back. That is an apply round that gave an unheld answer
  (decision 2), or a formulate round that gave its nothing-formulated field (decision 1). The check runs for a proposal
  `awaiting-answer` and for one `approved` (decision 3). `applied_nothing` is generalised and renamed to say it reads
  either round. The formulate branch of `run_round` takes a nothing-formulated result as its output, as the apply branch
  takes `nothing_applied`: it commits the proposal at the status it had, makes no move, asks no question and returns
  (r152, r153). Comments that cite r140 cite r150 instead.
- `scripts/supervise_outputs.py` (added by decision 4): the readers of a round's result that `route` and `run_round`
  use. These are `gives_nothing` (moved here), its formulate counterpart and the unheld-answers check. This file's
  concern is what a stage's result gives as its output. The move keeps supervise_rounds.py (267 lines) under 300.
- `scripts/supervise_brief.py`: the formulate round's brief names the nothing-formulated field and when to give it, in
  a constant beside `UNHELD_ANSWERS`. A brief is only given to the formulate kind.
- `agents/initiative-round.md`: the `formulate` section gives the field's contract, worded as the `apply` section's
  `nothing_applied` sentence: a sentence, no `questions`, and `work run` then starts an integrate round.
- `tests/scenarios/supervision_formulate_steps.py`: the Given "the formulate round for p1 formulates nothing, giving
  that p1's answers change lines not in spec/", with the optional ", and no scenario" tail, sets `round:formulate` to
  DONE with the field. `round:formulate` is the formulate round's entry in the test's `plan` dict.
- `tests/scenarios/supervision_reintegrate_steps.py`: the Thens for r149 (integrate after the formulate round's end),
  r152 (awaiting-answer at the formulate round's end; no move of p1 between the formulate round's start and the
  integrate round's start), r153 (no missing-output question naming the formulate round or a scenario) and r151 (no
  formulate round started for p1). Its docstring names r149-r153 and not r140.
- `features/supervision.feature`: the @r140 deprecated scenario removed (Retires).

The researcher's set, plus `scripts/supervise_outputs.py` (decision 4). Nothing removed.

## 3. Decisions

1. **The formulate round's field is `nothing_formulated`, a sentence saying that the proposal's answers change lines
   not in spec/, given with no `questions`.** `work run` reads it the way `gives_nothing` reads `nothing_applied`: a
   non-empty string and no question. It reads it whatever `changes` or scenarios the round gives. This is the
   researcher's reading A. It rests on supervision#r153 and on the proposal's answer "r149 against r131/r132: reading
   (a) ... take that case as the round's output, as r147 does for apply", which asks for the apply mirror. The field is
   part of `work run`'s contract with its own round and the narrator does not see it, so it is not a question
   (design-decision/worker-results-are-files).
2. **"An answer that the drafts it applied do not hold" (r150, r151) is an apply result whose `unheld_answers` is a
   non-empty list, given beside `changes` or beside `nothing_applied`, or one that gives `nothing_applied`.** This is the
   researcher's reading A. The proposal's answers settle it. "r150 against r140: reading (a)" says r150 covers r140's
   case. "r150 against r144-r146: reading (b)" added r151 for the partial apply. "r150/r151 against r144 and r145:
   reading (a), meant" says that a partial apply still goes `approved` and writes its lists (r144, r145), then goes to a
   new integrate round (r150), not to formulate (r151 over r146). The status stays `approved` while that integrate
   round runs (r143), and the round sets it `drafted` (r142).
3. **The sent-back check in `route` covers an `approved` proposal as well as an `awaiting-answer` one.** Without it, a
   formulate round started from `approved` that gives `nothing_formulated` keeps `approved` (r152) and is routed to
   formulate again, round after round. A partial apply (decision 2) would also go to formulate. This rests on r149 and
   r150, which name no status, and on r151.
4. **The result readers move to `supervise_outputs.py`.** This follows CLAUDE.md's size limit: supervise_rounds.py has
   33 lines of room, and r153 makes these readers part of "what a stage's result gives as its output", the module's
   concern.
5. **r83 stands; r152 is its exception.** This is the proposal's answer "r152 against r83: reading (a)". A formulate
   round with no question and no `nothing_formulated` still goes `formulated`, and still has its missing scenarios
   asked (r131, r132).

## 4. Tests the decisions break

None broken, checked by reading (the implementer confirms by running the suite):

- spec-integration r46's scenarios (tests/scenarios/spec_integration_apply_steps.py): the stand-in apply round gives
  `unheld_answers` beside `changes`. Under decision 2, p1 now goes on to an integrate round, where it used to go to
  formulate. That integrate round has no plan and gives no change list, so `work run` ends in r96's error. The Thens
  still hold: they count one apply round, read the kept result and check that p1 is not `awaiting-answer` (it is
  `approved`, kept by r143), and `run_integrate` does not check the exit code. Leave them as they are. If a run shows
  otherwise, the test is rewritten to assert those same three things, and the integrate round that follows is r150's
  to assert, not r46's.
- r83 and r116 (formulate with no question and scenarios present, or with a question), r131 and r132 (formulate output
  missing), r147, r150, r141-r143 and r148 (apply gives `nothing_applied`): none gives `nothing_formulated` or
  `unheld_answers`, so their paths are unchanged.
- The @r140 deprecated scenario is removed by Retires. That is not a broken test.

## 5. Open cases (for the implementer to name, not to choose)

- A formulate result that gives `nothing_formulated` and also `questions`. Under decision 1 it is not
  nothing-formulated, so its questions are asked. No scenario covers it.
- A formulate round that gives `nothing_formulated` and has also committed scenarios. No scenario covers it.
- An apply result that gives `unheld_answers` and `questions` together. Under decision 2 the proposal goes to
  integrate once the questions are answered, and the new round is given those questions and answers (r141). No scenario
  covers it.
- An `unheld_answers` that is not a list of strings, such as one string or empty strings.
- README.md's 0.28 entry (r140-r148) may want a line for r149-r153 in the release notes. That is not in this file set.
