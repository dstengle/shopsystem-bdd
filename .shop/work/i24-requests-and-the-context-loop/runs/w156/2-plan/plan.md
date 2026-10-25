# Plan of w156: fix branch review 1's F1 (supervision#r77, supervision#r78)

The work-item accepts supervision#r77 and #r78 and names the findings file of branch review 1. Of that file's five fix-now findings, only F1 falls under these two requirements: delegated answers fail on a node with two or more open questions. F2 to F5 are under other requirements or capabilities (r10/r46, design-model-check r27, batch-measurement, work-queue r23), and this work-item does not accept them (see 5).

## 1. What goes green

- **supervision#r77**: the Scenario Outline "under a delegation, each question of the initiative goes to a session of its own, given only the delegation and the files it names, that <reply>" (features/supervision.feature:957-972). It has two rows, "answers it" and "leaves it for the person".
- **supervision#r78**: "an answer given by a session started under a delegation is written naming that delegation" (features/supervision.feature:974-981).
- **Why red today:** neither is red. The notes (section 1) ran all three tests and each passed. Each gives one question per node, so `Answers.answers` commits the node before the next session starts. The defect is in the case these scenarios do not show: two or more open questions on one node. The notes reproduced it (section 2, "two questions, one node"; D1):
  - `work run` exits 1 with "the session answering w1's question faulted: … .shop/work/i1/w1.md changed in the repository's own checkout and not committed; work run put it back".
  - The first answer is reverted, and w1.md has no `## Answers`.
  - Every later run does the same.
- **The red the implementer sees:** a new regression test (decision D2). It is red today, as the probe shows.
- **Deprecated scenarios retired:** none. The work-item has no `## Retires`.

## 2. Where the change lands

- `scripts/supervise_answers.py` (121 lines): in `Answers.answers`, each answer a session gives is committed on the initiative branch as soon as it is written, before the next question's session starts (D1). The node's closing move or commit at the end of its questions stays as it is.
- `tests/scripts/test_supervise_answers.py` (new): drives `work run` through the real `work` entry point with the stand-in claude (`tests/scripts/stub_claude.py`, as the scenarios use it), on a repository whose initiative fulfils a request with a delegation. It holds these cases:
  - **two open questions on one node, both answered:** exit 0; `## Answers` holds two bullets in question order, each naming the delegation (r78); w1 has moved on from `awaiting-answer`; the main checkout's `.shop/work/` is clean.
  - **first question left for the person, second answered:** no answer is written, and the node stays `awaiting-answer`. This pins the existing gap rule, under which the n-th answer answers the n-th question.

  The research probe `.shop/work/i24-requests-and-the-context-loop/runs/w156/1-research/probe_delegation.py` (`test_two_questions_one_node`) shows the setup. The test must not import the probe from the run directory. It may reuse the scenario helper modules or build its own minimal repository, whichever keeps it under 300 lines.

Removed from the researcher's set, and why:
- `features/supervision.feature`: the review asks for an r77 Examples row with two questions on one node. A `.feature` change belongs to formulation. The implementer may commit no `.feature` file other than through `features retire` (agents/bdd-implementer.md), and the planner writes only the plan. The row is left as a follow-up (see 5).
- `tests/scenarios/supervision_delegation_steps.py`: it was in the set only to give that row a two-question Given. Without the row it is not needed.

No module on the path goes over 300 lines: supervise_answers.py has room for 179 more, and the test file is new.

## 3. Decisions

- **D1. Each answer is committed before the next session starts.** Answers are not held back until all of the node's sessions have ended.
  - Rests on supervision#r28: the main checkout's `.shop/work/` must equal its last commit when a worker ends. Today's uncommitted answer breaks that for the next answerer.
  - Rests on supervision#r78: when a session answers a question, its answer is written. A later session on the same node that faults (r89) must not take away an answer already given. Holding answers until the node's end would lose them on a fault.
  - The commit carries the node's file only. It makes no status transition (r7's "work-item's file … and nothing else"). The node's move to its asked-from status, when all its questions are answered, is unchanged.
- **D2. The two-question case is pinned by a test in `tests/scripts/`, not by a feature row.**
  - The implementer cannot add the row (the agents/bdd-implementer.md commit rule), and the review's fix needs a red test.
  - CLAUDE.md's module map gives `tests/scripts/` to "tests of the scripts that no scenario drives", and no scenario drives two questions on one node.
  - The behaviour asserted is the one r77 and r78 already state: each question gets its own session, and an answer is written naming the delegation. No new behaviour is chosen.
- **D3. The rest of the notes' findings stay out of scope**: D2 (zero questions), D3 (no log line), D4 (the answerer's read scope), the line-break silence, `answer_lines`' "the person gave" label, r70's count of delegated answers, and F-obs-2 (the answer pass runs once a run). r77 and r78's fix for F1 needs none of them. Most would change what the narrator observes, under requirements this work-item does not accept (r89, r90, r57, r70). One side effect: under D1, the answer in the notes' "no log line" case is now committed before the asked-from refusal. That is the only change there.

## 4. Tests the decisions break

None. What I verified:
- The notes' search (section 4) found no test that asserts the old single-commit-per-node shape.
- `tests/scenarios/supervision_delegation_steps.py` asserts on git only in the r90 Thens ("the initiative branch has a commit of the answering session's stage directory…", "nothing of that stage directory or of log.jsonl is left uncommitted"). Those run on the fault path, where `ask` raises before any answer is written, so D1 does not touch them.
- The r77 and r78 tests read the answer text and the sessions' briefs, not the commit count.

## 5. Open cases (for the implementer to name, not to choose)

- **The r77 Examples row the review asked for** (two questions on one node) is still unwritten. It needs a formulation change to features/supervision.feature, outside this work-item.
- **A session that faults after an earlier answer on the same node was committed:** the run stops as today (`Refused`), and the earlier answer is now kept. Whether that matches r89 and r90 in full is not w156's to settle.
- **When a question is left for the person and a later question on the same node gets an answer**, that answer is dropped (the gap rule). The session ran, but nothing of its answer is kept.
- **The `before` state handed to the node's closing move or commit**, once intermediate answer commits exist: whether it must be re-read after each answer commit.
- **The other fix-now findings, F2 to F5**, are not covered by any work-item, because one drafted work-item cannot accept lines of several capabilities (review F-obs-6). The same goes for the review's Minor M1 and M2.
