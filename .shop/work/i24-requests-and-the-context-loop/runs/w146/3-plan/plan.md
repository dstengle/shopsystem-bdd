# Plan of w146: work run starts a proposal's gate round and writes the questions its result gives

Planned from `runs/w146/2-research/notes.md` (run 1 of research ended at its turn limit and gives nothing). Accepts supervision#r68, supervision#r85. No `## Retires`, no `## Rulings`.

## 1. What goes green

- **supervision#r68**: "a drafted capability-proposal is given to a gate round whose brief asks for the gate as questions, each a decision with its readings and the recommended reading marked". Red today because the first Given, "i1's capability-proposal p1 is drafted", has no step. Behind it, the two Thens have no step either ("a round of the kind gate was started for p1", "the gate round's brief asks for the gate as questions…"). In the code, `due()` in `supervise_rounds.py` never selects a `drafted` proposal, so a run over only a drafted proposal exits 0 and prints nothing (notes D2, probe_gate). `gate` has no entry in the worker's `ROUNDS` or `TOOLS`, and the brief has no text asking for questions.
- **supervision#r85**: "when the gate round `work run` started for a capability-proposal ends, the questions its result gives are written under the proposal's ## Questions". Red at the same first Given. Behind it, the step for the result's question (Given) and the step for "p1's ## Questions holds … marked recommended" (Then) are undefined. The similar step at test_supervision.py:220 does not match. In the code, `round()` never reads a result's `questions` (probe_apply).
- Deprecated scenarios retired: none.

## 2. Where the change lands

- `scripts/supervise_rounds.py`: `drafted` becomes a due status whose round kind is `gate`. When a gate round ends, `round()` takes the questions from its result and writes them under the proposal's `## Questions` in the commit of the proposal's transition.
- `scripts/supervise_worker.py`: `gate` joins `ROUNDS`, so `TOOLS["gate"]` exists. Today `Workers.tools()` would raise KeyError for a gate stage.
- `scripts/supervise_brief.py`: the gate round's brief carries the round heading (`# gate of p1`), the `Capability-proposal:` and `Job:` lines like apply and formulate, and the ask: give the gate as questions, each a decision with its readings and the recommended reading marked.
- `scripts/supervise.py`: `move(question=)` and `section()` write one bullet per call. They must write each of a gate's questions as its own bullet, in order (234 lines, room 66).
- `tests/scenarios/supervision_rounds_steps.py`: the new steps. The drafted-proposal Given, the gate-result Given, the gate-started Then, the brief-ask Then and the `## Questions holds … marked recommended` Then.

Removed from the researcher's set:
- `agents/initiative-round.md`: the researcher's "conflict" is already settled in the worktree. The job `gate` (line 29) now says to give `questions` in the result as a list of strings, one per decision, with readings and the recommended reading marked, and to write no card files. So nothing changes there.
- `tests/scenarios/test_supervision.py`: the r68 and r85 scenarios are already collected by name (the researcher ran them by test id), and supervision_rounds_steps' steps are already bound. Nothing changes there.
- `scripts/workqueue.py`, `scripts/model_work.py`, `scripts/supervise_faults.py`, `scripts/supervise_draft.py`: these are on the path but not edited (notes part 7).

## 3. Decisions

1. **A `drafted` capability-proposal is due for a round of the kind `gate`.** It runs among the rounds `work run` starts before drafting and pulling, as apply and formulate do. Rests on supervision#r68.
2. **The gate round's brief carries an explicit ask**: give the gate as questions, each a decision with its readings and the recommended reading marked. It also carries the round heading and `Job: gate`. The gate brief gives no answers. Rests on supervision#r68 and spec-integration#r35.
3. **A gate result's `questions` are written verbatim, one `## Questions` bullet each, in the order given.** A string `questions` counts as one question (the rule that exists today in supervise_worker.py, and supervision's "Implementation, may change"). `work run` does not parse, reorder or reformat readings or the recommended mark: the round gives each question as one string that already holds them. The round writes nothing on the proposal itself. Rests on supervision#r85, the Implementation note on r68/r85, and design-decision/worker-results-are-files.
4. **After the gate round ends, the proposal transitions to `awaiting-answer`.** Without a status after `drafted`, the proposal stays due and the gate round restarts every pass. supervision#r69 settles which status. r69 itself is accepted by w152 (and w136). Its scenario may turn green here as a side effect; this work writes no step for it.
5. **The scenario's stand-in result for r85 gives one question string** that holds the question, the two readings and the mark on "One book.". The Then checks that p1's `## Questions` has a bullet holding all of these. The wording that marks "recommended" is the test's own and shared by the Given and the Then. The other steps' Givens stay as they are: "every round ends" sets the initiative-round outcome. Rests on supervision#r85.
6. **"a round of the kind gate was started for p1"** uses the existing `rounds()` helper (brief heading `# gate of p1`) and expects exactly one such round. Rests on supervision#r68.

## 4. Tests the decisions break

None. What was verified:
- Every fixture that writes a capability-proposal file and runs `work run` writes it `awaiting-answer` (supervision_rounds_steps) or `formulated` (supervision_proposal_steps). None writes it `drafted`. So decision 1 starts no gate round in an existing scenario.
- supervision_world's work-items name `capability-proposal/p1` without writing the file.
- `World.proposal` in tests/scenarios/conftest.py defaults to `drafted`, but only the design-model `model check` steps use it, and they never run `work run`. The same holds for tests/scripts/test_model*.py.
- tests/scripts/test_agents.py (:43, :64) is untouched, because the agent file does not change.
- Decision 3 keeps one-question callers (supervision_answers/faults steps) as they are: one question is still one bullet.

## 5. Open cases (for the implementer to name, not to choose)

- **A gate result with no questions (`[]` or missing) under `DONE`.** By decision 4 the proposal goes to `awaiting-answer` with nothing asked. Today's `due()` (Answers ≥ Questions, both zero) then starts apply and formulate at once (notes D1, probe_zero). The r68 scenario's "every round ends" gives exactly such a result, so in that run apply, formulate and drafting may follow the gate. Its Thens look only at the gate round. No requirement settles a refusal here. Name what happens; add no refusal.
- **A gate round whose outcome is not `DONE`, or whose session faults.** Today `round()` raises the Fault and the proposal keeps its status. Say whether that holds for the gate as well.
- **The exit and printout of a run whose only node is a proposal left `awaiting-answer`.** `items()` lists work-items only, so the run may exit 0 without printing the proposal's open question (D2). Neither scenario checks this.
- **`model_work.py`'s capability-proposal status set lacks `awaiting-answer`.** `model check` may refuse a proposal the gate leaves in that state. This is outside r68 and r85.
- **A question string that holds a newline.** It is written as a bullet verbatim. Say what the bullet looks like.
