# Notes for w145 (formulation#r14, formulating-features without a small-change path)

Tools: `tools tests-of` refused (no map; not made, `map` runs the suite). Searches by text otherwise. `tools size --limit 300` printed nothing: no tracked Python file over 300.

## 1. Why each scenario is red today

None: formulation#r14 has no scenario. `features/formulation.feature` does not exist (ls, by search). The work-item says "no scenario". The `@r14` tags in `features/` (10 hits, by search) belong to other capabilities. Nothing run.

## 2. What the system answers today

None run. Read only:
- `scripts/supervise_rounds.py:11,26-33` (read): a formulate round starts only for a capability-proposal in status `approved`. Nothing starts a formulate round for one reworded scenario of a capability with no proposal.
- `scripts/supervise_worker.py:42` (read): `ROUNDS = ("apply", "formulate")`, no other kind.

## 3. Old assumptions

Old form: a glossary reword is done by the session itself through "formulating-features' small-change path", without a round or gate. New form (r14): a round of the kind `formulate`, no gate.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| skills/formulating-features/SKILL.md:18 ("If the person is talking to you") | session dispatches `initiative-round` and reads its reply | section goes (w145 brief) | none | by search (`talking to you`) |
| skills/formulating-features/SKILL.md:22 | "small-change path has no round: the session writes its scenarios itself" | path goes | none | by search |
| skills/formulating-features/SKILL.md:35, last sentence | v_t1 row of other capability goes to the small-change path after the commit | a formulate round for it instead | none | by search |
| skills/formulating-features/SKILL.md:37-41 "The Small-Change Path" | session writes and splices a reworded scenario itself, no gate | becomes a round of kind `formulate`, no gate | none | by search |
| skills/integrating-a-proposal/SKILL.md:43 | v_t1 reworded "through its small-change path" after the commit | names a path that no longer exists; w143's scope | none | by search |
| skills/integrating-a-proposal/SKILL.md:57 | hands off to "formulating-features' small-change path" | dangles; w143's scope | none | by search |
| skills/checking-spec-consistency/SKILL.md:62, 63, 64 | reworded "through formulating-features' small-change path, with no further approval" | dangles; no work-item of i24 owns this file (by search of .shop/work/i24-requests-and-the-context-loop) | none | by search |
| spec/capabilities/spec-consistency.md:24 (r6) | names "formulation's small-change path" | dangles; a spec line, changed only through integrating-a-proposal's gate | none (no test module for spec-consistency in tests/scenarios) | by search |
| agents/initiative-round.md:34 (formulate reply) | each v_t1 row for another capability returned for the session the person talks to | the reply needs a consumer; under `work run` none reads it (see 2) | none | by search, read of scripts/supervise_rounds.py |
| agents/initiative-round.md:3, 7 (description, skills list) | "Dispatched by integrating-a-proposal and formulating-features" | may stay true; the round text is read by the worker | none | read |
| README.md:54 | formulating-features has feature-formulator write scenarios | no small-change mention; unchanged | none | by search (`small-change`) |
| docs/ | no small-change mention | none | none | by search |

## 4. Tests the requirements make impossible to keep

`tools tests-of skills/formulating-features/SKILL.md` refused: no map. By search (`SKILL|skills/|formulat|small` in tests/): no test reads any `skills/*.md` file. No test asserts the small-change path or the "talking to you" section. Checked by reading `tests/scripts/test_agents.py`: it reads agent frontmatter only (r1 starters, r3 spec-writers have no Edit or Bash, r5 models, r6 planner no Bash, result-first); none is changed by this work. Sound: none can fail. `tests/scenarios/supervision_rounds_steps.py:64-73` covers only proposal formulate rounds: unaffected.

## 5. A step the work-item skips

The small-change path does not dispatch a `feature-formulator`, does not run the porcelain check of step 1 and the coverage check of step 2 by a round, and writes no drafts. A round does all three (agents/initiative-round.md:33, read). The round itself runs as a worker on its own branch and merges only on success (scripts/supervise_rounds.py:42-63, read); nothing in `work run` starts a formulate round for a single reworded scenario (see 2). No probe run: `read`.

## 6. Defects

None. No probe was run, so no defect is shown.

## 7. The file set

Must change:
- skills/formulating-features/SKILL.md (142 lines; Markdown, no line limit): drop l.18, l.22, the last sentence of l.35, and "The Small-Change Path" l.37-41; the reword becomes a round of kind `formulate`, no gate. Found by reading the file and by search.

May change:
- agents/initiative-round.md (55 lines): l.34 reply for v_t1 rows of other capabilities, l.3 description. Found by search.

Outside w145's accepted lines, dangling after the change (not for this item to edit, per the brief):
- skills/integrating-a-proposal/SKILL.md (106 lines): l.43, l.57. Owned by w143.
- skills/checking-spec-consistency/SKILL.md (162 lines): l.62-64. No i24 work-item owns it.
- spec/capabilities/spec-consistency.md (55 lines): r6. Changes only through integrating-a-proposal's gate.

Tests: none must change; none reads the skill text.

Module on the change's path if a starter for a reword round is added (not required by the text of r14; see 2):
- scripts/supervise_rounds.py: 74 lines, room 226 under 300.
- scripts/supervise.py: 234 lines, room 66.
- scripts/supervise_worker.py: 238 lines, room 62.
These are Python; `tools size --limit 300` printed nothing.

## Open readings (for the plan, not decided here)

A. A v_t1 row naming a scenario of a capability with no proposal: (i) a formulate round for that capability is started by `work run`, which no code does today; (ii) the row stays in the reply of the round that found it and is left for a person. The text of r14 does not say which.
B. The dangling small-change references in spec-consistency r6 and checking-spec-consistency: (i) changed with w145; (ii) left, to be changed by the spec-consistency work.
