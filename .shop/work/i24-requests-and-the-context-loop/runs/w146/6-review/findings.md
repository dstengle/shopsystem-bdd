# Review of w146 (second review, after the answer of 2026-10-25)

**Verdict: DONE.** The commit does what r68 and r85 ask, and both scenarios pass. No test was removed or weakened, and nothing under `features/` changed. The one Important finding of the first review (5-review F1, a non-`DONE` gate still moves the proposal on) has the person's answer: accept the work-item as it stands, with a supervision line written first (integrate round 8) and a fix work-item of its own. So it is no longer fix now here. No finding is Critical or fix now.

## Commits reviewed

The branch `work/w146` is gone (`git log ... work/w146`: unknown revision). On HEAD: `aa4ada2 work: w146 ready -> claimed` .. `db142c6 work: w146 claimed -> done`, then `5abcc50 work: w146 done -> awaiting-answer`. In that window, without the `work:` commits and w148's `fd180a0`:

- `bbca36c` work run starts a drafted proposal's gate round and writes its result's questions under ## Questions. It changes `scripts/supervise.py`, `scripts/supervise_brief.py`, `scripts/supervise_rounds.py`, `scripts/supervise_worker.py` and `tests/scenarios/supervision_rounds_steps.py` (+59 −5). All five are in the fileset.

The result names `c71999a`. `git diff c71999a bbca36c --stat -- scripts tests` shows only w148's three files, so `bbca36c` is `c71999a` rebased at merge. That is not a finding. No w146 commit follows `5abcc50`. The later commits that touch these files, `c79de72` and `aedf564`, belong to other work.

## Removed and weakened tests

None. I searched the diff for deleted test or step functions, removed or loosened `assert`s, parametrize changes and skip/xfail. The one test file gains 49 lines and loses none. `move()`'s new loop treats the existing callers' single string `question` as one bullet, as before, and `None` or `""` as none.

## Allowances

The report gives "none". The diff agrees.

## Cannot verify

- The report's counts ("144 passed, 1 skipped" for `--work-item w146`; "798 passed, 2 failed" at start). The whole suite is not run here. I ran the two w146 scenarios: 2 passed.
- Whether the real `initiative-round` agent returns its gate as the strings r68 asks for. That is agent behaviour, and the scenarios use a stand-in.

## Findings

### F1. Important, answered (w146): a gate round that does not end `DONE` still moves the proposal to `awaiting-answer`
- `scripts/supervise_rounds.py:64-65` in `bbca36c` (line 72 on HEAD). `round()` never reads the result's `status`. A `BLOCKED` gate with no questions leaves the proposal at `awaiting-answer` with 0 questions, so `due()` (0 answers ≥ 0 questions) then runs apply and formulate without the person's gate.
- Triage: this was fix now in 5-review. The person answered on 2026-10-25: accept the work-item as it stands. The non-`DONE` end of a round gets a supervision line first (integrate round 8), and its own fix work-item delivers it. So it is not fix now for w146.

### F2. Minor, observation (w146): a `DONE` gate result with no questions goes straight on to apply
- This is the same code as F1. The plan's §5 and the report name it. Reproduction: the researcher's probe_zero (2-research notes §6 D1) gave `EXIT 3`, rounds `1-apply` and `2-formulate`, and p1 at `formulated`. The line F1's answer calls for should settle this case too.

### F3. Minor, observation (w146): a string `questions` in a gate result is written as one bullet per character
- `scripts/supervise_rounds.py:64` in `bbca36c`: `[q ... for q in data.get("questions") or []]` iterates a string, so `"questions": "Which?"` writes six bullets: `- W`, `- h`, …. Each of them then counts toward `due()`.
- This contradicts plan decision 3 ("A string `questions` counts as one question"). That decision credited the rule to supervise_worker.py, but `outcome()` (supervise_worker.py:241) has the same comprehension and splits a string the same way ("W; h; i; …"). So the plan's premise was wrong, not the implementer's copy of it.
- No client sends a string: `agents/initiative-round.md:29` asks for a list of strings. That makes this hardening. Found by reading. A Python probe is outside this session's allowed commands.
- Fix: `[question] if isinstance(question, str)` in the comprehension, as `move()` already does.

### F4. Minor, drop (w146): an empty-string question is written as an empty bullet `- `
- Same place, with `scripts/supervise.py:109-110`. That bullet counts toward `due()`. No client sends `""`.

### F5. Minor, drop (w146): the gate round gets apply and formulate's tools
- `scripts/supervise_worker.py:45-48`: joining `ROUNDS` gives `gate` `git add`, `git commit` and `Agent`. The agent's gate job writes no card files and needs only `work note`, which commits the ledger itself.
- `work note` commits through the script, so trimming the gate's tools needs a separate tool list. That is polish, and it costs more than it gives.

## Commands run

- `git log --format='%h %s' --grep="^work: w146 " HEAD`: claim `aa4ada2`, done `db142c6`, then `5abcc50`.
- `git log --format=%H -1 --grep=... work/w146`: unknown revision (the branch is gone).
- `git log --format='%h %s' aa4ada2..db142c6`; `git log db142c6..HEAD -- <fileset>`: only `c79de72` and `aedf564`, neither from w146.
- `git show --stat bbca36c`; `git diff c71999a bbca36c --stat -- scripts tests`; `git show bbca36c -- scripts`; `git show bbca36c -- tests`.
- `grep` on `spec/capabilities/supervision.md` for r68, r69, r85 and the Implementation lines 129-130; `grep -i questions agents/initiative-round.md`; `grep -n -A10 "def outcome" scripts/supervise_worker.py` (for F3: whether a string question counts as one elsewhere. It does not).
- `python3 -m pytest -q -k "drafted_capabilityproposal_is_given_to_a_gate_round or gate_round_work_run_started_for_a_capabilityproposal_ends" tests/scenarios/test_supervision.py`: 2 passed.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base aa4ada2df20e2140b41321b1bd954acb7009a197`:
  - **ruff:** 2 × I001, in `scripts/supervise_analysis.py:4` and `tests/scenarios/test_work_queue.py:7`. Neither file is touched by `bbca36c`.
  - **vulture:** clean.
  - **import-linter:** the project states no import contracts.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`: printed nothing.
- `git status --short`: clean.
