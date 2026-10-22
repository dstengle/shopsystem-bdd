---
id: measurement/missingmass.io/shopsystem/shopsystem-bdd/2026-10-22-research-at-the-limit
kind: measurement
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-10-22
---

A read-only diagnosis by a general-purpose agent on Fable (no plugin role diagnoses a role), asked by the person
("researchers seem to be growing extensively ... figure out what we are missing"). The harness refused the agent's
Write of its report; the coordinator saved it from the agent's reply. It corrects
2026-10-22-0-23-0-findings.md: `num_turns` is not the unit `--max-turns` limits.

# Why research stages end at the limit

Read-only diagnosis, 2026-10-22, branch release-0.23.0. Sources: the 14 raw researcher transcripts under `~/.claude/projects/-tmp-work-run-*-research/` (every research stage of i15, i8 and i19, plus one of i17), their `session.json`, briefs and notes under `.shop/work/*/runs/*/1-research/`, and the plugin's own code. Counts were made by one-off scripts in the session scratchpad; `measure` does not make them, so they are a request for the script (see Not counted).

## The cause, in short

1. **The limit was set at the researcher's natural length, then the environment started eating 3 to 9 turns of it.** `--max-turns 25` counts API round trips. Before 2026-10-22 16:19 every researcher finished in 14 to 30 round trips (i15 size-check 24, i8 migrate-run 25, migrate-kb 30, migrate-kb-2 14). From that commit (67f1ddb, supervision r22) `work run` puts `--work-item <name>` into every worker's `PYTEST_ADDOPTS` (`scripts/supervise_worker.py:68-77`), and `scripts/work_items.py:103-105` raises `SystemExit` when the files pytest was given hold no scenario the work-item accepts. The agent definition tells the researcher to probe the system only through pytest files in its scratch directory (`agents/code-scout.md`, "Probes": "your shell runs no other Python"; `supervise_worker.py:28` allows Bash only `python3 -m pytest*`). A probe file holds no scenario, so every probe run fails until the researcher discovers `--whole-suite`, `--work-item=` or `-p no:work_items -o addopts=`. 32 of 59 probe runs across the 14 sessions failed this way, all in the 9 sessions started after r22; 8 of those 9 ended at the limit. The 5 sessions before r22 had 0 such failures and none ended at the limit.
2. **The number that said "research is growing" measures something else.** `measure` reports `num_turns` from session.json (`scripts/measure_read.py:61`). For a finished session that equals the number of user messages (prompt plus one per tool result): i15's "50 turns" were 24 round trips and 49 tool calls; migrate-kb's "70" were 30 round trips and 69 calls. A capped session reports 26 whatever it did (25 round trips, 36 to 50 calls). In the unit the limit counts, research has not grown: 24, 25, 30, 14 before; 25 (stopped) after.

## 1. What a researcher spends its turns on

API round trips (the unit of `--max-turns`), tool calls, and what went wrong, per session. `env-fail` = pytest calls returning `SystemExit`/`INTERNALERROR`/`unrecognized arguments`/`no tests ran`; `refused` = Bash calls the allowlist rejected (pipes to `grep -v`, `env`, `python3 -c`, a shell variable); `1-call` = round trips carrying one tool call; `probeOK`/`notes` = round trip of the first probe that printed output, and of the notes write.

| session (date, claude) | ended | round trips | calls | 1-call | env-fail (first..last turn) | refused | probeOK | notes |
|---|---|---|---|---|---|---|---|---|
| i8 migrate-run (10-20 18:46, 2.1.299, no cap, no r22) | finished | 25 | 43 | 12 | 0 | 0 | 14 | 22 |
| i8 migrate-kb (10-20 22:45, no cap, no r22) | finished | 30 | 69 | 15 | 0 | 1 | 19 | 27 |
| i8 migrate-kb-2 (10-20 23:59, cap, no r22) | finished | 14 | 33 | 5 | 0 | 0 | 6 | 12 |
| i15 size-check (10-21 00:11, cap, no r22) | finished | 24 | 49 | 7 | 0 | 2 | 10 | 19 |
| i17 v-s2-one-tag (10-22 15:01, 2.1.307, cap, r22) | limit | 25 | 39 | 16 | 1 (11) | 2 | 18 | none |
| i8 holding-renamed-and-rebound (10-22 16:44) | limit | 25 | 38 | 17 | 7 (12..19) | 1 | 17 | none |
| i8 migration-rebind-1 | limit | 25 | 43 | 17 | 4 (11..22) | 0 | 16 | 24 |
| i8 migration-rebind-2 | limit | 25 | 48 | 14 | 3 (10..15) | 2 | 17 | 24 |
| i8 migration-rebind-3 | limit | 25 | 50 | 9 | 5 (7..19) | 3 | never | none |
| i8 migration-rebind-4 | finished | 23 | 44 | 12 | 3 (9..11) | 2 | 13 | 21 |
| i19 design-model-check-1 #1 (10-22 19:57, 2.1.308) | limit | 25 | 43 | 16 | 7 (17..25) | 3 | 21 | none |
| i19 design-model-check-1 #2 | limit | 25 | 42 | 18 | 5 (15..22) | 0 | 21 | none |
| i19 feature-file-tools-1 | limit | 25 | 36 | 18 | 1 (22) + name collision | 2 | never | none |
| i19 work-queue-1 | limit | 25 | 38 | 17 | 6 (14..22) + name collision | 3 | 21 | none |

Tool calls by kind, all 14 sessions: Bash pytest 125, Grep 118, Read of scripts 64, Read of tests 55, Bash read-only (`ls`, `wc`, `cat`, `sed`) 50, `tools refs` 73 (in 40 calls), `tools tests-of`/`untested` 32, Write probe 29, Write result 20, Write notes 9, Read feature 25 (design-model-check.feature is 757 lines, read in three pages), Read brief/work-item/spec/CLAUDE.md 50.

Finished against capped, what the same turns buy:

- Finished (migrate-kb-2, 14 round trips): brief, work-item, spec, `wc -l` of the file set, collect the feature's tests, run the test file once, read four scripts and four test modules, one probe file, run it (turn 6: `5 passed`), `tests-of` (no map), a second probe, notes, result. The brief's `File set:` was followed as given.
- Capped (i19 work-queue-1): brief, result PARTIAL, work-item, spec, CLAUDE.md, feature file, scripts, test module, collect (turn 6); turns 7 to 22 are pytest: the accepted scenario by node id exits 3 with `mainloop: caught unexpected SystemExit!` (call 24), a probe gives the same (26, 27), `-p no:work_items` gives `unrecognized arguments: --work-item` (28), `--work-item=` finally collects (29), the probe prints at call 33 (turn 21); four turns remain and go to `wc -l`, `ls .shop/work/*/work-queue-1.md`, `git status`. No notes.
- The capped sessions that did write notes (migration-rebind-1, -2) wrote them at round trip 24 and were stopped while rewriting the result; their result still says DONE, and 0.22.0's `work run` (before r45) took it (`.shop/work/i8-model-in-consumers/log.jsonl` moves both to `researched` and on to a plan).

In holding-renamed-and-rebound, 7 of 12 pytest calls are the fight (calls 24-32); in design-model-check-1 #1 the fight runs from turn 17 to the last turn (calls 32-43: `-p no:xdist` → `unrecognized arguments: -n`; `-o addopts=` → `SystemExit`; `-p no:work_items` → `unrecognized arguments: --work-item`; a private `probe.ini` → `SystemExit` twice; `--work-item=` at call 43 finally prints, on the session's last round trip).

## 2. Why research "grew": each candidate cause, with evidence

**(a) `--work-item` in every worker's pytest (r22, 67f1ddb, 2026-10-22 16:19). The cause.** `scripts/supervise_worker.py:75-76` puts `--work-item <name>` into `PYTEST_ADDOPTS` for every worker; `scripts/work_items.py:90-105` deselects every item that is not a scenario of an accepted requirement and raises `SystemExit("--work-item %s: no scenario carries a requirement it accepts")` when nothing is left. Under pytest.ini's `addopts = -n auto` that surfaces as a wall of `mainloop: caught unexpected SystemExit!` and `INTERNALERROR> KeyError: <WorkerController gw0>`; with `-n 0` as the plain `SystemExit`. Reproduced today from this checkout with a one-line probe: `PYTEST_ADDOPTS="--work-item work-queue-1" python3 -m pytest -q -s -n 0 probe_demo.py` → `SystemExit: --work-item work-queue-1: no scenario carries a requirement it accepts`; without the variable → `probe ran, 1 passed`. The researcher's definition requires exactly this kind of file (`agents/code-scout.md`, "Probes"), and r14/`supervise_worker.py:28` allow no other interpreter. 32 of 59 probe runs failed on it; 0 before r22, 32 after. The definition says nothing about the option: six sessions read `scripts/work_items.py` to get past the plugin's own option (holding call 34, rebind-1 call 32, rebind-2 call 29, rebind-3 call 49, design-model-check-1 #2 call 36, work-queue-1 call 19).

**(b) Work-item names repeating across initiatives. A second, independent fault of the same option.** `work_items.accepted()` (`scripts/work_items.py:46-50`) takes the first `*/<name>.md` in sorted order. `.shop/work/i10-delivery-on-v3/work-queue-1.md` (accepts r8-r10) sorts before i19's (r11); i10's `feature-file-tools-1` (r11, r21, r40) before i19's (r7, r60-r62). Reproduced: under `--work-item work-queue-1`, `--collect-only tests/scenarios/test_work_queue.py` collects 20 of 26 and none is the `show --json` scenario; under `--work-item feature-file-tools-1` the file collects 6 of 69, none of i19's. For these two work-items even r4 ("why each scenario is red, from a run of it") cannot be done: the run of its own scenario by node id exits 3 (work-queue-1 call 24), and feature-file-tools-1 spent calls 19-36 (turns 9-25) on collection, saw "63 deselected", read work_items.py, and never ran a scenario or a probe.

**(c) The limit (r19, 2f48945, 2026-10-20 23:35) and what it is measured against.** The limit counts API round trips; `measure`'s "turns" is `num_turns`, which for a finished session is the count of user messages and for a capped one is 26. Every capped transcript has exactly 25 distinct `requestId`s; i15's has 24 and 49 tool results and reports 50; migrate-kb's 30 and 69, reports 70; migrate-kb-2's 14 and 33, reports 34. The record's "research that finished took 34 to 70 turns" is 14 to 30 in the limit's unit, and 25 sits inside that range: two of the four pre-r22 sessions used 24 and 25. The limit was never generous; with (a) taking 3 to 9 round trips it is below the task. Since r45 a session at the limit makes the work-item `failed` whatever its result says, and r40 stops the run at the first `failed`, so the cheapest stage ($0.03-0.35; the four i19 stages together cost $0.136) now ends whole deliveries.

**(d) The agent definition.** Haiku at low effort (decision 0015) batches poorly: 14-18 of 25 round trips carry a single tool call in the capped sessions, against 7 of 24 in i15 and 5 of 14 in migrate-kb-2, although the definition says to run independent calls in one turn. The same model and effort finished in 14-30 round trips before r22, so this is a multiplier, not the cause. Two instructions cost turns every session: "`tools tests-of` ... first" while "you do not make one [map]" (31 of 32 `tests-of`/`untested` calls answered `tools: no map: make one with tools map`; `work run` never makes the map); and "`tools refs <dotted name>`" where `refs` wants a bare name (9 of 73 `refs` calls answered "nothing in the project is defined as", e.g. `workqueue.items`, `scripts/work.cmd_show`). The notes' seven parts are written last in one Write (turn 19-27 in the finished sessions), so a session stopped at 25 leaves nothing of what it found; r44's result-first rule preserves a summary, but r45 discards it.

**(e) The brief.** Not the cause: finished and capped sessions had the same brief shape (`File set:` where the work-item has one, `Accepted scenarios:` by title). Two omissions cost turns: the i19 work-items have no `fileset:`, so the researcher starts from `ls scripts`/`glob **/*.py` (feature-file-tools-1 calls 6-7, work-queue-1 call 9); and the accepted scenarios are given by title in feature files of 400-757 lines, read in two or three pages (25 feature reads in 14 sessions), with no line number or node id.

**(f) The repository.** pytest.ini's `addopts = -n auto -m "not fixture"` makes `-p no:xdist` an error (`unrecognized arguments: -n`, 5 sessions) and turns the plugin's `SystemExit` into the `mainloop`/`INTERNALERROR` wall, which hides the one-line reason unless `-n 0` is passed. The repository has not grown in a way that matters: file sets are 4-8 files of 50-280 lines.

**(g) The allowlist.** 0-4 refusals a session, each a wasted round trip; migrate-kb-2 had none and finished in 14. A contributor, not the cause.

## 3. What is missing, ranked by expected effect

The figure to move: research stages ending at the limit, 8 of 9 since r22 (8 of 12 since r19); and round trips per research stage, now pinned at 25.

1. **The `--work-item` option must not refuse a worker's probe or a non-scenario test.** Either `work_items.py` keeps every item that is no scenario (probe files, tests/scripts/*) and refuses only when scenarios were collected and none is accepted, or `work run` leaves `--work-item` out of the researcher's `PYTEST_ADDOPTS` (the researcher runs scenarios by node id already). Rests on: 32 of 59 probe runs failed on the option, all after r22; 0 of 5 sessions before r22 at the limit, 8 of 9 after. Expected: 3-9 round trips a session return, putting every session seen here under 25 (the first working probe moves from turn 16-21 to 9-14, where the finished sessions' were). Measured by: probe runs failing on the environment (0), and stages at the limit.
2. **A work-item name is one initiative's.** `work_items.accepted()` should take the initiative from the worker's environment (`SHOPSYSTEM_WORK_RUN_WORKER` already carries the name; carry `<initiative>/<name>`), or refuse an ambiguous name as `work withdraw` does. Rests on (b): two of i19's three work-items collide with i10's and cannot run any accepted scenario. Measured by: the accepted scenarios' node ids collect under `--work-item` for every work-item of the initiative, and stages at the limit.
3. **Judge the limit in its own unit, and give it headroom while a limit ends the work-item.** `measure` should count round trips (distinct assistant `requestId`s) beside `num_turns`; finished researchers used 14-30 (median 24.5), so 25 is a coin toss even after (1) and (2). Raise to 40 (cost $0.03-0.35 a stage) or keep 25 and let a session at the limit keep its result and notes for the planner instead of `failed` (r45 + r40 stop the run). Measured by: round trips per research stage and stages at the limit, both from `measure`.

Smaller, after those three: (4) make the coverage map once per `work run`, or let the researcher run `tools map` for its file set (31 of 32 `tests-of`/`untested` calls wasted; measure: "no map" answers → 0); (5) until (1) lands, one line each in the definition on what `--work-item`, `-n auto` and `-m "not fixture"` do to its pytest, and that `tools refs` takes a bare name (measure: `unrecognized arguments` and "nothing defined as" answers); (6) write `notes.md` part by part as r44 does for the result, and give the brief each accepted scenario's node id or feature line (measure: notes present in stages that ended at the limit; feature reads per session).

## Not counted

- Round trips, tool calls by kind, environment-failed pytest runs and refusals were counted by one-off scripts over the raw transcripts, not by `measure`; `measure` reports `num_turns`, a different unit from the one `--max-turns` limits. A round-trip column is a request for the script.
- The 0.21.0/0.22.0 slim exports were not needed: every research session of i15, i8 and i19 has a raw transcript on this machine.
- Whether Haiku at low effort batches worse on claude 2.1.307/308 than on 2.1.299 cannot be separated from (a): every post-r22 session is also a later client.
- Two apparent environment failures in i15 and migrate-run were the text of `work_items.py` in a `cat`, not failures, and are excluded; "deselected" matches were dropped as pytest's normal `-m "not fixture"` line.
