# w143 research notes

Scope: w143 is a guarantees work-item (no scenario) on spec-integration r35 and r39. Its work-item narrows reading to
skills/integrating-a-proposal/SKILL.md, agents/initiative-round.md, the capability and decision 0068. Parts 3-5 need more:
I read the code path of an initiative-round by search and targeted reads (scripts/supervise_rounds.py, supervise_worker.py,
supervise_brief.py), and nothing else. No `tools map` exists: `tools tests-of` answers "no map", so every test list is `by search`.
`tools refs` not run: the changes are prose; no Python name changes. Nothing run; no probes; no scratch files written.

## 1. Why each scenario is red today

None. No accepted scenario: `features/spec-integration*.feature` does not exist (glob, none). Searching `features/` for
`@r35` and `@r39` (grep, by search) finds only other capabilities' tags: design-model-check.feature:397 (r35),
batch-measurement.feature:5 (r39), supervision.feature:648 (r35) and :711 (r39), feature-file-tools.feature:89, 361, 478,
488, 497, 505 (r35). None is spec-integration's.
Nearest, not accepted by w143 (supervision's side of the gate, read only, not run):
- features/supervision.feature:987-994 `@r68` — a drafted proposal is given a gate round whose brief asks for questions.
- features/supervision.feature:996-1002 `@r85` — the questions a gate round's result gives are written under the proposal's `## Questions`.
Both are supervision's requirements; they show the consumer of r35 is outside w143's accepted set.

## 2. What the system answers today

None run. No accepted scenario, and w143 changes prose only. Read-only findings on the nearest path (see 5 and 6).

## 3. Old assumptions

Table: place (file:function or line) | what it does today | what the requirement makes of it | tests that execute it | found by

| place | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| skills/integrating-a-proposal/SKILL.md:18-29 "If the person is talking to you" | session dispatches initiative-round for integrate, gate, apply; publishes the gate page from the cards | retired (spec r8/r10/r11 gone; decision 0068 "skills lose their If the person sections"); gate becomes result questions (r35) | none | read; grep "talking to you" |
| skills/integrating-a-proposal/SKILL.md:21 "publish the gate page from those files" | session reads cards under `<drafts>/gate/` | the gate round's questions come in its result.json (r35); no card files | none | read |
| skills/integrating-a-proposal/SKILL.md:48-59 The Small-Change Path | session writes two lines itself, no round | removed (retired r34/r36-38 family per work-item) | none | read; grep "Small-Change" |
| skills/integrating-a-proposal/SKILL.md:33 "The small-change path below has no round" | points at 48-59 | goes with it | none | read |
| agents/initiative-round.md:23-31 "The job your input prompt names", jobs `integrate`, `gate`, `apply`, `formulate` | input word is "job" | r39: the input gives the kind; "kind" is the spec's word (spec Implementation: "gives the kind integrate, gate or apply") | none | read; grep "job" |
| agents/initiative-round.md:29-30 `gate` writes cards under `<drafts>/gate/`, replies with path and count | card files | r35: one question per decision in its result, each marking the recommended reading, lines in full | none | read |
| agents/initiative-round.md:29 "marks the coordinator's recommendation" | names a coordinator | decision 0068: no coordinator; r35 says "marking the recommended reading" | none | read; grep "coordinator" in agents/ and skills/ (this line only in agents/initiative-round.md) |
| agents/initiative-round.md:11, 18 "The session that dispatched you ... keeps the gate" | a session keeps the gate | decision 0068 replaces it | none | read |
| agents/initiative-round.md:38 ledger file `.shop/scratch/run/ledger-<initiative>.md` | appends to a file | r40 (not accepted by w143) says `work note` | none | read |
| scripts/supervise_brief.py:32-33 `if rnd: lines.append("Job: %s" % stage)` | writes the input label `Job:` | r39 reading that the input names the kind: label becomes `Kind:` (conditional, see 7) | none by search (no test contains "Job:") | read; grep "Job:" tests/ |
| scripts/supervise_rounds.py:42-63 `round()` | runs `initiative-round` through `worker()`, raises only on failure, then `move(name, before, after)` | the gate round's questions must reach the proposal (r35 end-to-end; consumer is supervision r85) | none by search (tests/scenarios/supervision_rounds_steps.py drives apply and formulate only: grep `rounds(repo, "apply")`) | read |
| scripts/supervise_rounds.py:11 AFTER; scripts/supervise_worker.py:42 ROUNDS = ("apply", "formulate") | a gate or integrate round is never started by the code | r35 presumes a gate round; decision 0068 says work run starts gate and integrate | none by search (grep `"gate"`, `"integrate"` in scripts/ and tests/: none) | read; grep |

Outside w143's accepted set, same old assumption, for the planner's information only:
- skills/formulating-features/SKILL.md:16-22 "If the person is talking to you", and :37-45 its Small-Change Path (formulation's capability).
- skills/checking-spec-consistency/SKILL.md:53-64 and skills/migrating-to-capabilities/SKILL.md:106 point at integrating-a-proposal's small-change path, which w143 removes.
- agents/initiative-round.md:36-38 `formulate` reply and `apply` reply wording: not changed by r35/r39.

## 4. Tests the requirements make impossible to keep

tests-of: no map, so by search.
- tests/scripts/test_agents.py (88 lines), read: test_r1 (only initiative-round starts an agent, line 41-43), test_r5 (model pins, 62-68), ResultFirst (82-88, four stage agents, not initiative-round). None asserts the job word, the gate cards or the Small-Change Path. Verified sound: none of them breaks when the two prose files change.
- tests/scenarios/supervision_rounds_steps.py (74 lines): grep for question|gate|card found nothing; drives apply and formulate rounds only. Sound, no change needed.
- grep of tests/ for "Job:", "gate/", "Small-Change", "talking to you", "coordinator": no matches (by search). So none.
- features/supervision.feature:988 and :997 (r68, r85) are the gate-round scenarios; they are red, not impossible to keep: they describe the consumer side and are not in w143's set.

## 5. A step the work-item skips

The existing way a worker's result becomes a question on the work-item: scripts/supervise.py:163-165 calls `outcome(agent, data, failure)` (scripts/supervise_worker.py:231-238), which returns the result's `questions` as the question put to the person, then `move(..., "awaiting-answer", question)`.
The round path (scripts/supervise_rounds.py:49-63) calls `worker()` (which normalises `questions` to a list, supervise_worker.py:199-205), raises only on `failure`, and moves the proposal with no question. Effect only the skipped step produces: a question recorded on the proposal, and the stop at `awaiting-answer`. So a round's result questions are dropped, and r35's gate questions could not reach the proposal through this path.
Mark: read (not run).

## 6. Defects

Read only; none reproduced by a run. Each would need its own probe before it is called a defect:
- A round's result `questions` are dropped: scripts/supervise_rounds.py:49-55 (see 5). Reproduction not run.
- No code starts a `gate` or `integrate` round: scripts/supervise_worker.py:42 and supervise_rounds.py:11 (see 3). Decision 0068 says work run does. Reproduction not run.

## 7. The file set

Changed by w143's accepted requirements (r35, r39), prose:
- skills/integrating-a-proposal/SKILL.md (106 lines; no limit: a skill, not Python). Remove "If the person is talking to you" (18-29), the Small-Change Path (48-59), the card-publishing step (21), and the "small-change path below" reference (33). Found by read and grep.
- agents/initiative-round.md (55 lines). "job" to "kind" (lines 13, 23, 25, 27-31, 38); the gate job gives questions in its result (29-30), not cards; "coordinator" (29) and "session ... keeps the gate" (11, 18) go. Found by read and grep.
- scripts/supervise_brief.py (115 lines; room 185 under 300). Conditional, one reading of r39: the input label `Job:` (line 33) becomes `Kind:`, so the input and the agent agree. Found by read and grep. Without it the agent text says "kind" while its input says "Job:".
Not changed by w143, checked:
- spec/capabilities/spec-integration.md (57 lines): already the target text.
- tests/scripts/test_agents.py (88 lines; room 212): sound, see 4.
- scripts/supervise_rounds.py (74; room 226) and scripts/supervise_worker.py (238; room 62) and scripts/supervise.py (234; room 66): the round's questions and the gate round are r85 (supervision), not w143. Listed so the planner sees the consumer, not a file w143 must change.
Limit: CLAUDE.md, 300 lines per Python file; the skill and agent are not Python.
