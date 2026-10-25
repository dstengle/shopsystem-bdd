# Research of w146: gate round for a drafted capability-proposal

Scripts: `/home/vscode/shopsystem-bdd/scripts`. No coverage map (`tools tests-of` answers "no map"; `tools map` not run): every test list below is `by search`. `tools refs` not run; names searched by text.

Accepted: supervision r68 (gate round for a `drafted` proposal, brief asks for questions) and r85 (gate result's questions written under `## Questions`).

## 1. Why each scenario is red today

- **r68** "a drafted capability-proposal is given to a gate round ...": `python3 -m pytest -q "tests/scenarios/test_supervision.py::test_a_drafted_capabilityproposal_is_given_to_a_gate_round_whose_brief_asks_for_the_gate_as_questions_each_a_decision_with_its_readings_and_the_recommended_reading_marked"` (run): `StepDefinitionNotFoundError: Given "i1's capability-proposal p1 is drafted"` (line 1007). Later steps also undefined (read; pytest-bdd stops at the first):
  - `a round of the kind gate was started for p1` (no step; `rounds()` in supervision_rounds_steps.py matches a brief by `# <kind> of p1`, so only a new Then is needed)
  - `the gate round's brief asks for the gate as questions, each a decision with its readings and the recommended reading marked` (no step; grep `readings|recommended` in tests/scenarios: no match)
  - `every round ends` (defined, supervision_rounds_steps.py:27).
- **r85** "when the gate round ... ends, the questions its result gives are written under ## Questions": same run (run): `StepDefinitionNotFoundError: Given "i1's capability-proposal p1 is drafted"` (line 1016). Undefined after it (read):
  - `the gate round's result gives the question "...", with the readings "One book." and "Two books.", "One book." marked recommended, and every round ends` (no step; grep `result gives` in tests/scenarios: none)
  - `p1's ## Questions holds "...", with the readings ... marked recommended` (test_supervision.py:220 defines a different `... holds "X" and then "Y", and its Answers ...` step; does not match).

What is missing in code (read):
- `scripts/supervise_rounds.py` `AFTER` (line 11) has no `drafted` key; `due()` (lines 26-33) never selects a drafted proposal, so no gate round starts.
- `scripts/supervise_rounds.py` `round()` (42-63) moves `before -> after` with `self.move(name, before, after)` and no question; it never reads the result's `questions`. A gate needs `after = awaiting-answer` and the questions written.
- `scripts/supervise_worker.py` line 43 `ROUNDS = ("apply", "formulate")` and the loop at 44-46 that builds `TOOLS[_round]`: no `gate` entry. `Workers.tools()` (line 115) evaluates `TOOLS[stage]` as a default argument, so a `gate` stage raises KeyError before any session starts.
- `scripts/supervise_brief.py` `brief()` (line 29-33): the `Capability-proposal:` and `Job:` lines come only from `ROUNDS`; the brief has no text asking for questions with readings and a recommended reading (r68's brief content). The brief's round text is generic (lines 47-55).
- `scripts/supervise.py` `section()` (114-127) writes one bullet per call; `move(question=...)` (105-112) takes one string. Gate questions are a list (`worker()` turns a string into a one-item list, supervise_worker.py 201-206).
- `agents/initiative-round.md` line 29, job `gate`: writes card files under `<drafts path>/gate/` and replies with the path and a count. It does not say to put the questions in `result.json`. **Conflict** with `spec/capabilities/spec-integration.md` r35 (the gate gives its questions "in its result") and with supervision.md lines 130: the planner must choose; both readings are below in part 7.

## 2. What the system answers today

Probe files are in `.shop/scratch/w146-2-research/`; each runs a stand-in claude (`SHOPSYSTEM_WORK_CLAUDE`) that writes a DONE `result.json` with one question, in a fresh git repository with a bare remote, under `work run` via `python3 /home/vscode/shopsystem-bdd/scripts/work run i1`. Run with `python3 -m pytest -q -s -n 0 <path>` (xdist swallows output without `-n 0`).

- **drafted proposal alone (r68's Givens)** — `probe_gate.py` (run): exit 0; stdout empty; no `session` line; `p1.md` still `status: drafted`; no log; no new commit. Why (read): `items()` lists work-items only, so `all([])` is true and the run is silent and successful. Under r68 a gate round should start.
- **answered awaiting-answer proposal (apply path, the pattern a gate round copies)** — `probe_apply.py` (run): exit 3 (from a w1 that `work run` drafted from the formulated p1 and then failed in the stand-in's repo; not part of the apply path). Log: `awaiting-answer -> approved` after a `1-apply` round session `end`, then `approved -> formulated` after `2-formulate`. Run directories `runs/p1/1-apply` and `runs/p1/2-formulate` exist. The stand-in's `questions` for the apply round were not written to the proposal: `round()` never reads them.
- **awaiting-answer proposal with no question and no answer (nearest case of a gate with zero questions)** — `probe_zero.py` (run): exit 3; `runs/p1/1-apply` and `2-formulate` made; log `awaiting-answer -> approved -> formulated`. See defect D1.
- Gate result `questions` as a string, a list or a number (read, supervise_worker.py 201-206): a string becomes a one-item list; any other non-list is a Fault for the round (`round()` raises it; the proposal keeps its status). Not run.

## 3. Old assumptions

Rule: a proposal reaches `awaiting-answer` only through an apply or formulate path, never from a gate.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| supervise_rounds.py: `AFTER`, `due()` | a proposal starts a round only at `awaiting-answer` (with Answers >= Questions) or `approved`; `drafted` is absent | `drafted` must start a `gate` round; a zero-question proposal at `awaiting-answer` is due for apply (see D1) | by search: supervision_rounds_steps.py r70/r71/r80/r83 scenarios (they start at awaiting-answer/approved; none starts at drafted) | read |
| supervise_rounds.py: `round()` | runs a round, merges, `move(before, after)`; ignores `questions` | a gate round must write its questions under `## Questions` and move to awaiting-answer; questions must be written as N bullets | by search: the r70, r71, r80, r83 scenarios | read |
| supervise_rounds.py: `rounds()` and `run()` ordering (supervise.py:192) | rounds run before `draft()` and `pull()` | a drafted proposal is now picked up before anything else | by search: none (no drafted-proposal scenario) | read |
| supervise_worker.py: `ROUNDS`, `TOOLS` loop (43-46) | apply and formulate only | a gate needs `TOOLS["gate"]` and a ROUNDS entry | by search: none | read |
| supervise_worker.py: `Workers.tools()` (115) | `TOOLS[stage]` is evaluated even when delivery names the stage | a `gate` stage without a TOOLS entry raises KeyError | none | read |
| supervise_brief.py: `brief()` (29-33) | the round heading `Capability-proposal:` and `Job:` for ROUNDS only | gate brief needs the job and the question ask | by search: supervision_rounds_steps.py `rounds()` matches `# <kind> of p1` in the brief | read |
| supervise.py: `section()`, `move(question=)` (105-127) | one bullet per call; `held()` reads bullets | gate writes N bullets, each a question with readings | by search: supervision_answers/faults steps (single question) | read |
| supervise.py: `questions()` (181-184) and `run()`'s print (208-212) | open questions are Questions past Answers | a gate's questions must show as open for the person | by search: supervision_faults/answers scenarios | read |
| agents/initiative-round.md, job `gate` (line 29) | writes cards, replies path and count | spec r35 wants questions in result.json; supervision r85 reads them there | none (agent text, not run) | read |
| workqueue.py: `PROPOSAL_STATUSES`, `move()` (18-19, 142-167) | a proposal may move to any STATUSES value, `awaiting-answer` included | none beyond the gate's transition; `move` does not check the lifecycle | by search: supervision_rounds scenarios | read |
| model_work.py:11 capability-proposal status set | lacks `awaiting-answer` (lists drafted, approved, merged, formulated, withdrawn) | a gate makes `awaiting-answer` the proposal's normal state; `model check` may refuse it | none (`model check` not run) | read |

## 4. Tests the requirements make impossible to keep

- `tools tests-of` has no map. By search, the tests on the old behaviour are the apply/formulate scenarios in `tests/scenarios/supervision_rounds_steps.py` and the test module `tests/scenarios/test_supervision.py`. Their Givens start at awaiting-answer, approved or formulated, not drafted, so the gate does not change them (read; not run).
- `tests/scripts/test_agents.py:43` asserts the round starters are `initiative-round` only; a new job text in `agents/initiative-round.md` leaves it true (read). `:64` checks each agent's model; unaffected.
- No test asserts that a drafted proposal starts nothing (by search: no supervision step gives a drafted proposal and checks the run).
- No test runs a zero-question awaiting-answer proposal (by search).
- Verified sound (read): the apply/formulate rounds' tests do not depend on `due()` skipping `drafted`. None found impossible to keep.

## 5. A step the work-item skips

The gate's transition to `awaiting-answer` is the only one that leaves the question to the result rather than to the person's answer. The steps the existing `awaiting-answer` path gives, and the gate path would skip:
- writing each question as a `## Questions` bullet (`move(question=)` / `section()`): the only thing that makes `due()` wait for an answer. With no question written, `due()` (Answers >= Questions, both zero) is due at once. Shown by probe_zero (run).
- a refusal for a result whose `questions` is empty while `status` is DONE: none exists (read, supervise_worker.py 201-206 accepts `[]` or missing).
- the apply round ignores `questions` (probe_apply, run): a gate that gave questions and then went to apply without answers would also pass (read, `round()`).

## 6. Defects

**D1: a proposal at awaiting-answer with no question goes through apply and formulate unanswered.**
Reproduction: `python3 -m pytest -q -s -n 0 .shop/scratch/w146-2-research/probe_zero.py` (run). The probe writes `p1.md` with `status: awaiting-answer` and no `## Questions`/`## Answers`, commits, runs `python3 /home/vscode/shopsystem-bdd/scripts/work run i1`.
Came back: `EXIT 3`; `ROUND DIRS ['.shop/work/i1/runs/p1/1-apply', '.shop/work/i1/runs/p1/2-formulate']`; `P1 status ['status: formulated']`; log lines `awaiting-answer -> approved` then `approved -> formulated`, both `by: work run`.
Expected by spec (read, supervision r70: "every question ... has an answer"): no apply round while nothing is asked. Today's vacuous truth in `due()` (supervise_rounds.py 30-31) lets a gate with no questions pass. Relevant to r85 and r69. Not judged here.

**D2 (minor): a run over only a drafted proposal exits 0 and prints nothing.**
Reproduction: `probe_gate.py` (run). Came back: `EXIT 0`, empty stdout, no session. Reason (read): `items()` (supervise.py:64) lists work-items only. Part of r68's red; listed so the plan knows the silent success.

## 7. The file set

Must change (for the two scenarios and for what passes today to keep passing):
- `scripts/supervise_rounds.py` (74 lines, room 226): `AFTER` and `due()` take `drafted` to `gate`/`awaiting-answer`; `round()` writes the result's questions as bullets for a gate. Found by read and probe_apply/probe_zero.
- `scripts/supervise_worker.py` (240 lines, room 60): `ROUNDS` and the `TOOLS` loop take `gate`. Found by read (lines 43-46, 115).
- `scripts/supervise_brief.py` (115 lines, room 185): the gate brief's job line and the question ask (readings and recommended reading). Found by read (lines 29-55).
- `tests/scenarios/supervision_rounds_steps.py` (75 lines): new steps: drafted proposal Given, gate result Given, gate-started Then, brief-ask Then, `## Questions holds ... with the readings ... marked recommended` Then. Found by run (first undefined step) and grep.

Maybe change (planner decides):
- `agents/initiative-round.md` (not Python; line 29, job `gate`): cards only today; spec r35 wants `result.json` questions. Both readings: (a) the gate writes cards and `result.json` questions; (b) the gate writes `result.json` questions only. Not decided here.
- `scripts/supervise.py` (234 lines, room 66): only if the rounds' question write is moved out of `section()`'s single-bullet path. Read.
- `tests/scenarios/test_supervision.py`: the scenario module; only if its step module must be bound there (line 220 holds a similar step). Read.

On the change's path, not edited:
- `scripts/workqueue.py` (286 lines, room 14): `move()` takes `awaiting-answer` for a proposal already (read).
- `scripts/model_work.py` (219 lines, room 81): proposal status set lacks `awaiting-answer` (read; `model check` not run).
- `scripts/supervise_faults.py` (160 lines, room 140): `Fault`, `fault_of` used by `round()` (read).
- `scripts/supervise_draft.py` (80 lines, room 220): drafts only formulated proposals (read; unchanged by the gate).

Size: `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` printed nothing (run): no tracked Python file is over 300 lines. No `CLAUDE.md` size limit differs from 300.
