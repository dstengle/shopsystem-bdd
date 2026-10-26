# Plan of w199 (supervision: a transition decided by how a session ended and what its result holds)

Sources: the research notes (`1-research/notes.md`), the earlier plan (`2-plan/plan.md`, outcome QUESTION), the capability, design-decision 0038 (worker-results-are-files), the accepted scenarios in `features/supervision.feature` (lines 956 to 1059 read again for this plan), and the work-item's `## Answers`. The person answered Reading B to both of the earlier plan's questions. Those answers are taken here as rulings: decisions 9 and 12. Outcome: DONE.

## 1. What goes green

Every red here is a Given or Then that has no step definition (notes part 1). Under those steps, probes P-a to P-j (notes part 2) show that the behaviour is also wrong for r128, r129, r131, r132, r133 and r88.

- **r4**, "an implementer whose result gives no question has its branch merged only if the work-item's scenarios and the whole suite pass on it: <case>" (5 rows). The Given at line 122 has no step. Today the merge gate goes through `outcome()`, which reads the status (supervise_merge.py `claimed`).
- **r61**, "implementers working at the same time have the branches r4 merges merged one at a time, in the order they ended". The Given at line 476 has no step.
- **r31**, "a planner's result with a `fileset` writes that file set into the work-item as it makes the transition to planned". The Given at line 686 has no step.
- **r45**, "a worker whose session <ending> makes the work-item's transition to failed, recording how the session ended" (4 rows). The Givens at line 908 have no steps.
- **r128**, "the <session> for <node> that <ending> is recorded and printed as a fault of <node>, whatever its result says" (5 rows). The Givens have no steps. A round's fault, or an answering session's fault, is never recorded under its node and never printed (P-f, P-i; D1).
- **r129**, "the questions a <who>'s result gives go <where>, and <node> makes its transition from <from> to <to>" (5 rows). The Givens have no steps. A researcher that gives PARTIAL with a question stops w1 at awaiting-answer (P-d; D5).
- **r130**, "a <who> whose result gives no question and its stage's output makes the work-item's transition from <from> to <next>" (4 rows). The Givens have no steps.
- **r131**, "a <who> whose result gives neither a question nor <missing> puts a question naming it under the work-item's ## Questions and makes the work-item awaiting-answer" (4 rows). The Givens have no steps. Nothing checks for an output (P-c; D4).
- **r132**, "a <stage>'s result giving <output> is taken as its stage's output" (10 rows). The Givens have no steps. Nothing reads a researcher's file set as its output (P-e).
- **r133**, "a researcher whose result gives the outcome BLOCKED with its file set and no question is moved on by its output, not stopped by its outcome". The Given has no step. BLOCKED sends w1 to awaiting-answer (P-a; D3).
- **r134**, "when an intake round gives a question, the request's status stays as `work turn` set it". The Then at line 1058 has no step.
- **r89**, "when a session started under a delegation to answer a question <ending>, the question is left unanswered for the person". The error and no-result rows have no Givens. The turn-limit row passes.
- **r90**, "... its stage directory and log lines are committed" (3 rows). The Given at line 1397 has no step. The behaviour already holds (P-i).
- **r86**, "when a round `work run` started for a capability-proposal ends at its turn limit, the proposal keeps its status". It passes today and must keep passing.
- **r87**, "the <kind> round of <node> that <ending> brings no transition" (3 rows). The Givens have no steps.
- **r88**, "the <kind> round of <node> that <ending> ends `work run` with an error naming the round and how it ended" (3 rows). The Givens have no steps. The wording lacks "ended in an error", "ended at its turn limit" and "left no result `work run` can read" (P-f, P-g; D2).
- **r115**, "when the gate round of a capability-proposal <ending>, the initiative's other nodes are taken through their transitions before `work run` exits with an error" (3 rows). It passes today and must keep passing.

**Retired.** The 12 deprecated scenarios in the work-item's `## Retires` are removed from `features/supervision.feature`:
- 4 of r4;
- 1 each of r61, r31, r45, r89, r90, r87, r88 and r115.

Their step definitions go too where nothing else binds them, notably "the apply round gives BLOCKED" (supervision_rounds_steps.py) and "the gate round gives BLOCKED" (supervision_formulate_steps.py). Part 4 removes one more deprecated outline.

## 2. Where the change lands

Production:
- `scripts/supervise_worker.py`: `outcome()` stops reading the status word. It gives the result's questions, or else a question naming the missing output, taken from the output check (r129, r131, r133).
- `scripts/supervise_outputs.py` (new, added by decision 2): the stage-output check of r132. For each stage it says whether the result and the repository hold that stage's output, and gives the wording of r131's missing-output question. It is a new module because supervise.py has 25 lines of room.
- `CLAUDE.md`: a module-map row for supervise_outputs.py, as CLAUDE.md requires for every new module.
- `scripts/supervise.py`:
  - `stage()` sends a researcher's questions to the planner's brief and moves the work-item to researched (r129);
  - it makes the next transition only when the output is there (r130, r131);
  - `show()` prints each node with a fault this run recorded, of any kind (r128).
- `scripts/supervise_brief.py`: `research_questions` passes on the researcher's questions whatever status the researcher gave (r129, r133).
- `scripts/supervise_rounds.py`: `run_round`:
  - drops its refusal of a status other than DONE (r133);
  - writes a gate, apply or formulate round's questions under the proposal and moves it to awaiting-answer (r129);
  - checks the apply and formulate outputs (r131, r132);
  - records a faulted round as a fault of its node and keeps the node's status (r128, r86);
  - says how the round ended in r88's words.

  The integrate round's handling of questions and of a missing change list stays as today (decision 9).
- `scripts/supervise_faults.py`: `fail()`, or a sibling of it, records a fault under `## Faults` of any node. Only a work-item's status changes to failed (r45, r86). `session_end` and `cut_short` use r88's words, and r45's Then for work-items still matches.
- `scripts/supervise_answers.py`: `ask()`:
  - writes an answer whatever status the result gives (r133);
  - records a faulted answering session as a fault of the node whose question it was; the node stays awaiting-answer, the question unanswered, and the stage directory committed (r128, r89, r90);
  - when a result gives neither an answer nor a question, leaves the question for the person and writes no question (decision 12).
- `scripts/supervise_intake.py`: `take()` loses its DONE gate (r133) and leaves the request's status as `work turn` wrote it (r134).
- `scripts/supervise_merge.py`: `claimed()` merges on r4's tests and the output check, not on the status.

Tests:
- `tests/scenarios/supervision_outputs_steps.py` (new): the "the <who>'s result gives ..." Givens for r4, r31, r61 and r129 to r133.
- `tests/scenarios/supervision_session_faults_steps.py` (new): the Givens for round and answering-session endings, for r45, r87, r88, r89, r90 and r128. It is new because supervision_rounds_steps.py has 12 lines of room.
- `tests/scenarios/test_supervision.py`: imports of the two new modules.
- `tests/scenarios/supervision_then_workers.py`: the Thens of r128 and r129 (or put in a new module if room runs out).
- `tests/scenarios/supervision_faults_steps.py`: "recorded a fault of <node>" and "prints <node> with the fault".
- `tests/scenarios/supervision_intake_steps.py`: the Then of r134.
- `tests/scenarios/supervision_rounds_steps.py`: the round defaults deliver each kind's output (decision 3), and its BLOCKED Given is removed.
- `tests/scenarios/supervision_formulate_steps.py`: its BLOCKED Given is removed, and the formulate default delivers its output (decision 3).
- `tests/scenarios/supervision_given.py`: "every worker gives DONE" and its variants deliver each stage's output (decision 3).
- `tests/scripts/stub_claude.py`: a default output for each stage (decision 3). It has 26 lines of room, so whether to split it under the size rule is the implementer's call.
- `features/supervision.feature`: the retired scenarios and the deprecated r5 researcher outline (part 4) removed.

## 3. Decisions

1. **The outcome word decides nothing.** This covers `outcome()`, `research_questions`, `run_round`, the intake gate, the answer gate and the merge gate. Rests on r133 and r129.
2. **What each stage's output is.** Field names are from 0038.
   - researcher: a non-empty `fileset`;
   - planner: a `plan` and a non-empty `fileset`;
   - implementer: at least one commit on the work-item branch that the initiative branch lacks, on which r4's tests pass;
   - reviewer: a `findings` field;
   - answering session: an `answer`;
   - integrate and apply rounds: a change list that `entries()` reads;
   - formulate round: a non-deprecated scenario tagged `@r<n>` for each id the proposal adds or changes, on the initiative branch after the merge (formulation r1 and r11);
   - intake round: a line outcome or a question on each line;
   - gate round: its questions. With none, r117's approval question still applies, so r131 never fires for a gate.

   Rests on r132, r131 and 0038.
3. **The test stand-in delivers each stage's output by default.** "every worker gives DONE", "every round ends" and their variants keep meaning a session that did its work. Only the new Givens withhold an output. The defaults:
   - researcher and planner: a `fileset`; the planner also a `plan`;
   - implementer: a commit of a file named for its work-item;
   - reviewer: `findings`;
   - apply round: a change list that mirrors the proposal's own lists, so r114 leaves them as they were;
   - formulate round: a scenario committed for each id.

   Rests on r131 and r132. Nothing the narrator sees changes.
4. **A researcher that gives questions moves w1 to researched, with or without a file set.** r131 needs "neither a question nor its output". Rests on r129 and r131.
5. **A researcher's file set is not written into the work-item.** r31 names only the planner, and the planner reads the research result. Rests on r31 and r132.
6. **A fault wins over the result's questions and output.** A fault is an error, a turn limit or no readable result. Rests on r128 ("whatever its result says"), r87 and r45.
7. **Where a fault is recorded:**
   - a work-item worker: the work-item fails, as r45 has it;
   - a capability-proposal or initiative round: a `## Faults` bullet with the status kept (r86), then other nodes go on (r115), then the run exits with r88's error;
   - an answering session: a `## Faults` bullet on the node whose question it was, which stays awaiting-answer with the question unanswered (r89, r128).
8. **`show()` prints each node that has a fault recorded this run, whatever its status.** Rests on r128.
9. **The integrate round is unchanged, and an initiative never becomes awaiting-answer.** Its questions stay in its drafts for the gate round, and a missing change list stays r96's error naming the round. r129 and r131 do not move an initiative. Ruling: the work-item's `## Answers` (2026-10-26, part 2; gate answer 6 under q16's delegation), with r96.
10. **An intake round's questions are written in the request (r100).** The request's status stays as `work turn` wrote it (r134), never awaiting-answer.
11. **A gate round with a non-DONE status and a question** (D6): the question goes under p1's `## Questions` and p1 goes to awaiting-answer. r87 is about faults only. Rests on r129, r133 and r69.
12. **An answering session whose result gives neither an answer nor a question:** the question is left for the person as it stands, and no missing-answer question is written. r131 does not apply. The node stays awaiting-answer and the question unanswered. Ruling: the work-item's `## Answers` (2026-10-26, part 1; gate answer 7), with r77.

## 4. Tests the decisions break

- **Deprecated r5 outline "a researcher that gives <outcome> makes the work-item's transition to awaiting-answer"** (features lines 150 to 163). Decisions 1 and 4 break it: its QUESTION and BLOCKED rows now go to researched. r5 is retired, the outline is "Deprecated for: removal", and it pins the opposite of r133. **Removed**, with its step "the researcher gives <outcome>" if nothing else binds it. It is listed here so the review does not find an unlisted removal.
- **The 12 `## Retires` scenarios** are removed (part 1).
- **The deprecated r5 implementer outline (lines 135 to 148) and the deprecated r3, r16, r112 and r113 scenarios** keep passing under decisions 1 to 3 (notes part 4) and are kept.
- **Scenarios that use "every worker gives DONE", "every round ends" or their variants** would be broken by decision 2. Decision 3 keeps them as they are, not rewritten.
- **A scenario whose Then counts commits or files on the initiative branch** might clash with decision 3's default commit. The implementer finds any by running the whole suite and names the default commit so it does not collide. No Then is weakened.
- **The r96 and gate-round scenarios** are kept as they are by decision 9.
- **tests/scripts/test_supervise_answers.py:46-50 and tests/scripts/test_agents.py:79-85** were found sound by the researcher. Decision 12 keeps the unanswered path. Both are kept.
- **Not verified:** scenarios outside w199's accepts, which could not run under `--work-item w199`. The implementer runs the whole suite.

## 5. Open cases (for the implementer to name, not to choose)

- A planner's `plan`, or a reviewer's `findings`, that names a file which is not there.
- An apply round whose change list is present but empty.
- An intake round that leaves a line with neither an outcome nor a question. A request has no `## Questions` of its own.
- An answering session that gives a question rather than an answer, on a node that is already awaiting-answer.
- Faults recorded in an earlier run: `show()` prints only this run's.
- A formulate round for a proposal that adds and changes nothing.
