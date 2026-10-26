# Plan of w199 (supervision: transitions decided by how a session ended and what its result holds)

From the research notes (`1-research/notes.md`), the capability, design-decision 0038 (worker-results-are-files) and
the accepted scenarios in `features/supervision.feature`. Outcome: QUESTION. The plan covers everything except two
points, listed at the end, that change what the person sees.

## 1. What goes green

Every red listed here is a Given or Then with no step definition (notes part 1). Under those steps, the probes P-a to P-j
(notes part 2) show that the behaviour is also wrong for r128, r129, r131, r132, r133 and r88.

- **r4**: "an implementer whose result gives no question has its branch merged only if the work-item's scenarios and the whole suite pass on it: <case>" (5 rows). The Given at line 122 has no step. The merge gate goes through `outcome()`, which is keyed on the status (supervise_merge.py `claimed`).
- **r61**: "implementers working at the same time have the branches r4 merges merged one at a time, in the order they ended". The Given at line 476 has no step.
- **r31**: "a planner's result with a `fileset` writes that file set into the work-item as it makes the transition to planned". The Given at line 686 has no step.
- **r45**: "a worker whose session <ending> makes the work-item's transition to failed, recording how the session ended" (4 rows). The Givens at line 908 have no steps.
- **r128**: "the <session> for <node> that <ending> is recorded and printed as a fault of <node>, whatever its result says" (5 rows). The Givens have no steps. A round's fault, or an answering session's fault, is never recorded under its node or printed (P-f, P-i; D1).
- **r129**: "the questions a <who>'s result gives go <where>, and <node> makes its transition from <from> to <to>" (5 rows). The Givens have no steps. A researcher that gives PARTIAL with a question stops the work-item at awaiting-answer (P-d; D5).
- **r130**: "a <who> whose result gives no question and its stage's output makes the work-item's transition from <from> to <next>" (4 rows). The Givens have no steps.
- **r131**: "a <who> whose result gives neither a question nor <missing> puts a question naming it under the work-item's ## Questions and makes the work-item awaiting-answer" (4 rows). The Givens have no steps. Nothing checks that a stage gave its output (P-c; D4).
- **r132**: "a <stage>'s result giving <output> is taken as its stage's output" (10 rows). The Givens have no steps. Nothing writes a researcher's file set or reads it as an output (P-e).
- **r133**: "a researcher whose result gives the outcome BLOCKED with its file set and no question is moved on by its output, not stopped by its outcome". The Given has no step. BLOCKED sends the work-item to awaiting-answer (P-a; D3).
- **r134**: "when an intake round gives a question, the request's status stays as `work turn` set it". The Then at line 1058 has no step.
- **r89**: "when a session started under a delegation to answer a question <ending>, the question is left unanswered for the person". The error row and the no-result row have no Givens. The turn-limit row passes.
- **r90**: "when a session started under a delegation to answer a question <ending>, its stage directory and log lines are committed" (3 rows). The Given at line 1397 has no step. The behaviour already holds (P-i).
- **r86**: "when a round `work run` started for a capability-proposal ends at its turn limit, the proposal keeps its status". Passes today and must keep passing.
- **r87**: "the <kind> round of <node> that <ending> brings no transition" (3 rows). The Givens have no steps.
- **r88**: "the <kind> round of <node> that <ending> ends `work run` with an error naming the round and how it ended" (3 rows). The Givens have no steps. The messages do not use the words "ended in an error", "ended at its turn limit" or "left no result `work run` can read" (P-f, P-g; D2).
- **r115**: "when the gate round of a capability-proposal <ending>, the initiative's other nodes are taken through their transitions before `work run` exits with an error" (3 rows). Passes today and must keep passing.

**Retired**: the 12 deprecated scenarios in the work-item's `## Retires` are removed from `features/supervision.feature`. These are the 4 deprecated r4 scenarios, plus one deprecated scenario each of r61, r31, r45, r89, r90, r87, r88 and r115. Their step definitions are removed where nothing else uses them, notably "the apply round gives BLOCKED" (supervision_rounds_steps.py) and "the gate round gives BLOCKED" (supervision_formulate_steps.py). One more deprecated scenario is removed: see part 4.

## 2. Where the change lands

Production:
- `scripts/supervise_worker.py`: `outcome()` stops reading the status word. It returns the result's questions, or a question naming the missing output, from the output check below (r129, r131, r133).
- `scripts/supervise_outputs.py` (new; added by decision 2): the stage-output check of r132. For each stage, it says whether the result and the node's world hold the stage's output, and if not, it gives the wording of the missing-output question (r131). It is a new module because supervise.py has only 25 lines of room.
- `CLAUDE.md`: a row for supervise_outputs.py in the module map. CLAUDE.md requires a row for every new module.
- `scripts/supervise.py`: `stage()` sends a researcher's questions to the planner's brief and moves the work-item to researched (r129). It makes the next transition only when the output is there (r130). `show()` prints every node that has a fault this run recorded, of any kind (r128).
- `scripts/supervise_brief.py`: `research_questions` passes the researcher's questions on whatever status the researcher gave (r129, r133).
- `scripts/supervise_rounds.py`: `run_round` drops the refusal of any status other than DONE (r133). It writes the questions of a gate, apply or formulate round under the proposal and moves it to awaiting-answer (r129). It checks the apply and formulate outputs (r131, r132). A faulted round is recorded as a fault of its node with the status kept (r128, r86). The error says how the round ended in r88's words.
- `scripts/supervise_faults.py`: `fail()`, or a sibling of it, records a fault under the `## Faults` of any node (work-item, capability-proposal, initiative). It changes the status to failed only for a work-item (r45, r86). `session_end` and `cut_short` say "ended in an error", "ended at its turn limit" and "left no result `work run` can read" (r88). r45's existing wording for work-items must still match its Then.
- `scripts/supervise_answers.py`: `ask()` writes an answer whatever status the result gives (r133). A faulted answering session is recorded as a fault of the node whose question it was. That node keeps awaiting-answer and its question stays unanswered (r128, r89). Its stage directory is still committed (r90).
- `scripts/supervise_intake.py`: `take()` loses its DONE gate (r133). It leaves the request's status as `work turn` wrote it (r134).
- `scripts/supervise_merge.py`: `claimed()` merges by r4's test result and the output check, not by the status.

Tests:
- `tests/scenarios/supervision_outputs_steps.py` (new): the "the <who>'s result gives …" Givens for r4, r31, r61, r129 to r133.
- `tests/scenarios/supervision_session_faults_steps.py` (new): the round and answering-session ending Givens for r45, r87, r88, r89, r90 and r128. supervision_rounds_steps.py has only 12 lines of room.
- `tests/scenarios/test_supervision.py`: imports the new step modules.
- `tests/scenarios/supervision_then_workers.py`: the r128 Thens and the r129 Thens, or new Thens in one of the new modules if room runs out.
- `tests/scenarios/supervision_faults_steps.py`: "recorded a fault of <node>" and "prints <node> with the fault".
- `tests/scenarios/supervision_intake_steps.py`: the r134 Then.
- `tests/scenarios/supervision_rounds_steps.py`: "every round ends" and its siblings deliver each round kind's output (decision 3). The two BLOCKED Givens are removed.
- `tests/scenarios/supervision_formulate_steps.py`: the "gate round gives BLOCKED" Given is removed, and its round defaults deliver outputs (decision 3).
- `tests/scenarios/supervision_given.py`: "every worker gives DONE" and its variants deliver each stage's output (decision 3).
- `tests/scripts/stub_claude.py`: a default output for each stage when the script does not say otherwise (decision 3). It has 26 lines of room, so a split is the implementer's call under the size rule.
- `features/supervision.feature`: the retired scenarios removed, plus the r5 researcher outline (part 4).

## 3. Decisions

1. **The outcome word decides nothing anywhere.** This covers `outcome()`, `research_questions`, `run_round`, the intake gate, the answer gate and the merge gate. Rests on r133 and r129.
2. **What counts as each stage's output.** Field names come from design-decision 0038.
   - Researcher: a non-empty `fileset`.
   - Planner: a `plan` and a non-empty `fileset`.
   - Implementer: at least one commit on the work-item branch that the initiative branch lacks, on which r4's tests pass. A branch with no new commit has no output.
   - Reviewer: a `findings` field.
   - Answering session: an `answer`.
   - Integrate and apply rounds: a change list that `entries()` reads.
   - Formulate round: a scenario, not deprecated, tagged `@r<n>` for each id the proposal adds or changes, in the feature files on the initiative branch after the round's merge. This rests on formulation r1 and r11, and 0038 gives no formulate field.
   - Intake round: a line outcome or a question on each line.
   - Gate round: its questions. With none, r117's approval question still applies, so r131 never fires for a gate.

   Rests on r132, r131 and 0038.
3. **The test stand-in delivers each stage's output by default.** "every worker gives DONE", "every round ends" and their variants keep meaning a session that did its stage's work. Only the new Givens that withhold an output say so explicitly. Concretely, the default researcher and planner give a `fileset` and the planner a `plan`. The default implementer commits a file named for its work-item. The default reviewer gives `findings`. The default apply round gives a change list mirroring the proposal's own lists, so r114 leaves them as they were. The default formulate round commits a scenario for each id the proposal adds or changes. Without this, r131 turns most of today's suite awaiting-answer. Rests on r131 and r132. Nothing the person sees changes.
4. **A researcher that gives questions moves the work-item to researched, with or without a file set.** r131 needs "neither a question nor its output", so it does not fire. Rests on r129 and r131.
5. **A researcher's file set is not written into the work-item.** r31 names only the planner. The planner reads the research stage's result, as its brief says. Rests on r31 and r132.
6. **A fault (session error, turn limit, or no readable result) wins over the result's questions and output.** Rests on r128 ("whatever its result says"), r87 and r45.
7. **A fault's record depends on the node.**
   - Work-item worker: failed, as r45 already does.
   - Capability-proposal or initiative: a `## Faults` bullet with the status kept (r86). The run exits with an error naming the round in r88's words. The other nodes go on first (r115).
   - Answering session: a `## Faults` bullet on the node whose question it was. That node stays awaiting-answer with its question unanswered (r89, r128). r45 is about a work-item's stage workers (r2), not answering sessions.
8. **"prints <node> with the fault"**: `show()` prints each node that has a fault this run recorded, whatever its status. Rests on r128.
9. **The integrate round without a change list keeps r96's error.** r96 is a standing requirement and its scenario must keep passing. It is the more specific line. It is held pending question 2, which may extend it.
10. **An intake round's questions follow r100 and r134**: they are written in the request, and the request's status is left as `work turn` wrote it. They never send the request to awaiting-answer.
11. **A gate round that gives a status other than DONE with a question** (D6, reading A): the question goes under p1's `## Questions` and p1 moves to awaiting-answer. r87 is about faults only. Rests on r129, r133 and r69.

## 4. Tests the decisions break

- **features/supervision.feature, deprecated r5 outline "a researcher that gives <outcome> makes the work-item's transition to awaiting-answer"** (lines 150 to 163). Broken by decisions 1 and 4. Its QUESTION and BLOCKED rows give a question, so w1 moves to researched and goes on; its NEEDS_CONTEXT row still holds through r131. r5 is retired, its scenario is "Deprecated for: removal", and what it pins is the opposite of r133. **Removed** with its step "the researcher gives <outcome>" if nothing else binds it. Listed here so the review does not find it as an unlisted removal.
- **The 12 scenarios in `## Retires`**: removed (part 1).
- **The deprecated r5 implementer outline (lines 135 to 148), and the deprecated r3, r16, r112 and r113 scenarios**: checked against decisions 1 to 3 (by reading the notes' part 4). They keep passing once decision 3 holds, and are kept.
- **Every scenario that uses "every worker gives DONE", "every round ends" or their variants**: decision 2 breaks them unless decision 3 holds. They are kept through decision 3, not rewritten.
- **A scenario whose Then counts the implementer's commits or files on the initiative branch** could be affected by decision 3's default commit. The implementer finds any by running the whole suite. For each one, the default commit gets a name that does not collide with the Then; the Then is not weakened.
- **tests/scripts/test_supervise_answers.py:46-50 and tests/scripts/test_agents.py:79-85**: read by the researcher and found sound. Kept.
- **Not verified**: the scenarios outside w199's accepts. They could not run under this session's `--work-item w199` (notes, method). The implementer runs the whole suite.

## 5. Open cases (for the implementer to name, not to choose)

- A planner's `plan` that names a file which is not there, and a reviewer's `findings` naming a missing file. Does the output count?
- An apply round whose change list is present but empty.
- An intake round that leaves one line with neither an outcome nor a question. Where does r131's question go, given that a request has no `## Questions` of its own?
- An answering session whose result gives a question rather than an answer.
- Faults recorded in an earlier run under `## Faults`. `show()` prints only this run's faults.
- A formulate round for a proposal that adds and changes nothing. Its output is there by default.

## Questions (the outcome is QUESTION)

1. **An answering session that gives neither an answer nor a question** (r77's "leaves it for the person"; the delegation-answerer agent's not-covered result is DONE with no `answer`).
   - Reading A (r131 with r132): a question naming the missing answer is written under the node's `## Questions` and the node stays awaiting-answer. That new question is itself given to an answering session under the delegation (r77), so in one run it can recur with no bound. The person sees an extra question on each node whose question the delegation does not cover.
   - Reading B (r77): the question is left for the person as it stands and no question is written. The person sees only the original question, unanswered.
2. **An integrate round whose result gives questions** (spec-integration's reply carries questions, which the gate round then asks), or no change list.
   - Reading A (r129 and r131 as written): the questions, or a question naming the missing change list, go under i1's `## Questions` and i1 moves to awaiting-answer. That is a status the initiative lifecycle does not have, and no round is named for an answered initiative. The person sees i1 awaiting-answer, with the questions asked again by the gate.
   - Reading B: the integrate round's questions stay in its drafts for the gate round, as today. A missing change list stays r96's error. i1 keeps started.
