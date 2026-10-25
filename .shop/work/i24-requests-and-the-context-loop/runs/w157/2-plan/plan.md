# plan of w157 (supervision#r77, branch review 1 F1)

## 1. What goes green

supervision#r77, in `features/supervision.feature`:

- **Scenario Outline (L971):** "under a delegation, each question of the initiative goes to a session of its own, given only the delegation and the files it names, that <reply>". Both examples (`answers it` and `leaves it for the person`) already pass today (notes §1, run). They must stay green.
- **Scenario (L988):** "under a delegation, a work-item with two questions has each given to a session of its own, and both answers stay written when the run ends". It is red today for two reasons:
  - Its steps are missing. The run stops with `StepDefinitionNotFoundError` at L991 (the Given for two questions, "each with no answer"). The Given at L992 (an answer for each question) and the two Thens at L994/L995 ("<quoted question>" was given to a/another session of its own) are missing too. The Then at L996/L997 already exists (`answer_names_delegation`).
  - The behaviour is missing (probe P1, defect D1). `answers()` writes the first answer into the main checkout without committing it. When the second answering session ends, `checkout_changes` (called from `supervise_worker.worker` L185) treats the uncommitted answer as a worker's change: it puts the file back and faults. The run exits 1 and no answer is kept.

This work-item retires no deprecated scenarios.

## 2. Where the change lands

- `scripts/supervise_answers.py`: `answers()` commits each answer as soon as it has written it, before the next question's session starts (decision D1). The item's closing move (or its no-move commit) and the push stay after its questions.
- `tests/scenarios/supervision_delegation_steps.py`: four new steps. The Given at L991 writes w1, awaiting-answer, with the two questions and no `## Answers`. The Given at L992 calls `asked_by_the_log`, sets the default and `initiative-round` to DONE, and gives the delegation-answerer one answer per question (decision D2). The Then at L994/L995 takes a quoted question: one regex with `a|another`, reusing `given_to` and `read_list`, checking the brief holds the delegation and no `.shop/work/`/`spec/` before "Run directory:", and checking the other question is not in it.
- `tests/scripts/stub_claude.py`: one step can now be chosen by the brief's `Question:` line (decision D2), and the docstring says so. The file is at 260 lines and must stay at 300 or fewer.

Removed from the researcher's set:
- `scripts/supervise_faults.py`: not changed, because D1 commits the answers rather than exempting them from the check.
- `tests/scenarios/supervision_answers_steps.py`: not changed, because the new Given goes beside the other delegation steps.
- The rest of the researcher's list was read-only context and stays unchanged: `supervise.py`, `supervise_worker.py`, `supervise_brief.py`, `workqueue*.py`, `test_supervision.py`, `supervision_given.py`, `supervision_world.py`.

## 3. Decisions

- **D1. Commit each answer the moment it is written** (using the existing `commit(name, before, before)`, which also commits the item's run directories and log and pushes), rather than having `checkout_changes` let work run's own answers through.
  - Rests on supervision#r28: "the main checkout's `.shop/work/` differs from its last commit when a worker ends" must keep meaning a fault. An uncommitted answer would make the checkout differ from its last commit, so leaving it out of the check would bend r28's text. Committing keeps r28 intact for every session.
  - Rests on supervision#r38: each commit on the initiative branch is pushed, so a push per answer is what r38 asks for.
  - Rests on design-decision/a-script-supervises-delivery: work run's own writes are committed by work run.
  - The commit message stays `work: <name> <before> -> <before>` (Implementation, may change).
  - A per-answer commit happens only after a session that gave `DONE` with an answer. A session that faults or leaves the question still goes through `keep_round` and r89/r90 as today.
- **D2. The stand-in picks its step for an answering session by the question in the brief.** It looks for a plan entry keyed by the question (for example under a `question:` prefix) and lays it over the agent's entry, the same way `round:<kind>` already takes precedence.
  - The scenario says "the session given Q answers A". A per-agent `fields` entry cannot give two different answers, and a test aid that depends on the order sessions start in would tie the scenario to that order.
  - Rests on supervision#r77: each question goes to a session of its own.
- **D3. Defect D2 of the notes (a refused `measure initiative` still exits 0) is out of this work-item.** No requirement of r77 covers it, and the notes put it down to the stand-in's `session.json`. It is left to the branch review.

## 4. Tests the decisions break

None.
- D1 keeps the r28 scenario (L576) true: nothing is exempted from `checkout_changes`.
- The notes searched for tests that count commits or pushes under a delegation (r38, r7) and found none.
- r89/r90 only reach the per-answer commit after a successful session, so a failed session's record is not committed early (notes §4).
- The P3 path (no answer given) keeps its single closing commit.
- D2 only adds to the stand-in: plans without a question key behave as before.

## 5. Open cases

- A second answer whose commit or push fails, after the first answer is already committed and pushed. What the run reports, and in what state it leaves w1, is not covered by the scenarios. The notes (§5) show an uncaught push `Fault` there already.
- After per-answer commits, the item's closing commit may find nothing left to commit (for example a capability-proposal whose questions were all answered). It must not fail on an empty commit.
- The push at the end of `answers()` may become redundant now that each commit pushes. Whether to keep it is for the implementer to say.
- A second session that faults after the first answer was committed. The first answer then stays committed. The scenarios do not say whether the fault's message should mention it.
