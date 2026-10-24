# w132 research: model check's request rules v16a, v_d1, v17, v3, v18, v_d3

Method: `tools` at /home/vscode/shopsystem-bdd/scripts. `refs` ran. `tests-of` and `untested` have no map (`tools: no map`), so every test count here is `by search`. `tools size --limit 300`: no file over 300. Probes in `.shop/scratch/w132-1-research/` (git-ignored; `git status --porcelain` clean). Marks: `run` = executed, `read` = from reading.

## 1. Why each scenario is red today

Command (run): `python3 -m pytest -q -n 0 --tb=short tests/scenarios/test_design_model_check.py -k "v16a or v_d1 or v_d3 or v17 or v18"`, and `-k is_v3`. All 14 cases fail with StepDefinitionNotFoundError on their first Given (pytest-bdd stops there). Then steps are undefined too (read: no `<code> names <ids>` or `does not name` step in tests/scenarios; the only such steps are v_e and v15).

- v16a (`...dated_after_20261023...is_v16a`): Given "an initiative i1 dated 2026-10-24 that fulfils no request" missing (line 833).
- v_d1 (5 Examples, `...is_not_delivered_is_v_d1[...]`): Given "an initiative i1 with status done" missing (843); the request Given (844) missing too.
- v_d3 (`...is_v_d3`): Given "a delivered request q1" missing (859).
- v17 (`...is_v17`): Given "a request q1 that is part of no job-thread and cites no origin" missing (868).
- v3 (`...is_v3`): Given "a capability thing with requirement r1 and no requirement r9" missing (877).
- v18 (6 Examples, `...is_v18[...]`): Given "a repository whose bounded context is bounded-context/missingmass.io/shopsystem/shopsystem-bdd" missing (887); then "an initiative i1 whose source names <id>" and "nothing in the repository has the id <id>" missing (read: design_model_check_given.py:140 has only "an id nothing in the repository has", another phrasing).

Code side (read, confirmed by run in section 2):
- scripts/model.lp has no v16a, v17, v18 or v_d3 rule and no `label` for them.
- scripts/model.lp:239-240 v_d1 is only "done with a part open"; the r114 clause is absent.
- scripts/model.lp:93-95 v3 is "a scenario is on a needs edge"; no fact `needs` is ever emitted (grep: none), so it never fires.
- scripts/model.lp:22 declares `resolution/2`; nothing emits it.
- scripts/model_work.py:93-125 `read_work` globs every directory under .shop/work/, so `requests/` is read as an initiative (see defect D1); no request is read at all.
- scripts/model_work.py:117-122 emits only `age` from `date`, never a date fact; no `fulfils` field is read.
- scripts/model_facts.py:23-26 KINDS lacks `request`.
- scripts/model.lp `#show` (lines 292-304) lists no v16a, v17, v18, v_d3.

## 2. What the system answers today

Probes (run): `python3 -m pytest -q -s -n 0 -p no:warnings .shop/scratch/w132-1-research/probe_model_rules.py` and `probe_fix.py`. Each repository is under the scratch `repos/`; each line is `python3 <worktree>/scripts/model --root <repo> check [--json]`. Trimmed results:

- P1 v16a inputs (run): i1 dated 2026-10-24 with no source; i2 dated 2026-10-23; i3 dated 2026-10-24 with `fulfils: request/…/q1`. `check`: "0 violations, 0 warnings, 0 unresolved references, 0 file problems", exit 0. `facts` shows `age` per initiative, no date, no fulfils. So v16a is silent for i1 today.
- P2 v_d1, request in .shop/work/requests (run): i1 `status: done` (no parts), q1 open with `source: [initiative/…/i1]`. `check`: `file: .shop/work/requests: no initiative.md`, exit 1; no v_d1.
- P3 v_d1 part-open clause (run): i1 done, p1 capability-proposal `drafted` with `part_of: initiative/…/i1`. `check --json`: violations `v_d1 [i1]`, label "a done initiative has a part open", exit 1. (Also an unresolved capability in my fixture, not relevant.)
- P4 v_d3 (run): q1 `delivered` with `1. thing#r1 1.0`, i1 `started`. Only the requests-directory file problem; no v_d3.
- P5 v17 (run, corrected fixture): q1 with `source: []`, q2 with `source: [observation/…/obs-1]`. Violations none; warning `w_uncited_obs (1)` for obs-1 although q2 cites it; the request-directory file problem. No v17.
- P6 v3 (run): q1 `delivered` with `1. thing#r9 1.0` (no r9), q2 `1. thing#r1 1.0`. Violations: `v_s3` for thing#r1 (my fixture has no scenario), file problem for requests. No v3, no unresolved for r9.
- P7 v18 (run, corrected id): i1 `source: [request/missingmass.io/shopsystem/other/q3]`. `check --json`: violation `v10a [i1, request/…/other/q3]` ("a source that is not an origin"), unresolved "names nothing in this repository", exit 1. No v18.
- P7b v18 with observation other-context (run): i1 source `observation/…/other/2026-10-01-x`: `v10a` too (an unresolved source counts as not an origin, model.lp:148). No v18.
- P7c v18 with initiative other-context (run): i1 source `initiative/…/other/i2`: `v10a` and unresolved. No v18.

Nearest cases (run): empty requests (no directory): every probe above without the request file gives 0 problems; a stored request of any form (P2–P6) gives the directory file problem; the v_d1 "another context" and "asker" distinctions cannot be probed: no reader of asker exists (read: `asker` is a free string from `work request --from`, workqueue_request.py:75).

## 3. Old assumptions

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| scripts/model.lp:93-95 v3 (needs edge) | fires on a scenario in a `needs` edge; `needs` never emitted, so dead | r116 takes code v3 for "resolution names a requirement"; old meaning must go or the label clashes | none (by search: no test asserts v3) | refs/grep `v3`, `needs` |
| scripts/model.lp:239-240 v_d1 (part open) | done initiative with an open part | r114 adds a second clause under v_d1; the spec table (capability line 48) has no row for the part-open clause | none (by search: no test asserts v_d1) | grep `v_d1` |
| scripts/model.lp:136-137 v9e (source on non-initiative) | any `source` fact on a non-initiative | a request's `source` (v_d1 Givens, grammar.md:73 initiative/request/job-thread) would fire v9e | none (by search) | grep `source` |
| scripts/model.lp:146-148 v10a (source must be origin) | a source naming a request or initiative fires | v18's Given (initiative source names a request) fires v10a; r114's request source naming i1 would too | none (by search; the v18 scenario asserts only v18) | P7, grep |
| scripts/model.lp:284 w_uncited_obs | observation with no `source(_, O)` | a request citing an observation should count as citing it (P5 shows it does not) | design_model_check_problems.py:291-300 (by search) | P5, grep |
| scripts/model_work.py:113-116 initiative `source` facts | only initiatives' sources emitted | requests' sources and `fulfils` need new facts | test_model_reading.py:185 (by search; initiative source only) | grep `source` |
| scripts/model_work.py:117-122 date → age only | `age` days, no date | v16a needs the date string against 2026-10-23 | none (by search) | P1 |
| scripts/model_work.py:93-125 read_work | every .shop/work/ directory read as an initiative | requests/ must be read as requests (r19) | none asserts the directory problem (by search) | P2 |
| scripts/model_facts.py:23-26 KINDS, qualify 67-81 | no `request`; `request/q1` short form not qualified | `request/<name>` short form needs qualifying | none (by search) | read |
| scripts/model.lp:22 `#defined resolution/2` | declared, never emitted | v3 needs resolution facts from `## Resolution` entries | none | grep |
| scripts/model:19-40 CONTRACT text | says the reader reads no other layout; requests not listed | r19 lists `.shop/work/requests/*.md` | none (by search) | read |
| scripts/model.lp:286 w_many_requests / across/2 | counts `across` open requests; `across` never emitted | request status facts would make it live | none | grep `across` |

## 4. Tests the requirements make impossible to keep

Map absent, so by search (`tests-of` unavailable). Checked and sound for these changes:
- tests/scripts/test_model.py:166-174 RulesTest: every `#show` relation has exactly one label. New shows need labels, old v3 label replaced, not duplicated. Keep: sound if paired.
- tests/scripts/test_model.py:204 v_d2 test: unaffected by r114/r119.
- tests/scenarios/design_model_check_trace.py:190-201 `_lp_labels` order: rules output follows label order; new v labels must sit in the v section before the w_ labels (rule_order uses text position, model_check.py:36-39).
- tests/scenarios/design_model_check_glossary.py:137-149 and design_model_check_trace.py:125 "no violation names the initiative" (abandoned/done formulated initiatives): their initiatives are dated 2026-10-15 (tests/scenarios/conftest.py:141, test_model.py:121), so r113 is silent; r114 needs a request, none exists. Sound.
- tests/scripts/test_model_reading.py:185 (initiative source reading): unaffected.
- tests/scripts/test_model_reading.py:92 docstring only; no test asserts v3 or needs.
- No test writes a request or asserts the requests-directory problem (by search of tests/ for `requests`: only work-queue steps, which do not run model).
- Verified none breaks as its test is written; no test asserts the old v3 or old v_d1 meaning.

## 5. A step the work-item skips

Read: the existing request writers do checks the new rules repeat, but the scenarios write requests by hand.
- `work request` (scripts/workqueue_request.py:65-70) refuses a request with neither source nor thread, and a line not in EARS form. Only these two refusals; no effect beyond the file. The v17 Given (origin-less request) cannot be made through `work request`; only by hand.
- `work resolve` (workqueue_request.py:104-114) sets `delivered` and writes the resolution without checking the fulfilling initiative is `done` (v_d3) or that the requirement exists (v3). Its only refusal is status not accepted. So both checks land only at `model check` time; `resolve` produces what v_d3 and v3 later report.
- `work turn` (workqueue_request.py:92-101): sets accepted/refused from the lines; no delivered check.

## 6. Defects

D1. A repository with a request file gets a file problem and exit 1, whatever the request says. Repro (run, P2): `repo/.shop/work/requests/q1.md` (a `work request` form) plus `.shop/work/i1/initiative.md`; `python3 scripts/model --root repo check` prints `file: .shop/work/requests: no initiative.md`, exit 1. Cause: scripts/model_work.py:93-98 reads every directory under .shop/work/ as an initiative. Read: the r112 scenario "a request not of the form `work request` writes is a file problem" expects a file problem naming `.shop/work/requests/q1.md`; this output names the directory, so that scenario is red too (read, not run).

## 7. Conflicts for the plan (both readings given; not decided here)

C1 Where `fulfils` lives. grammar.md:302 and :75 put it on the initiative (`initiative I … fulfils REQ`; fulfils(I, Q)). r114 and the v_d1 Givens put the link on the request (`part_of` or `source` names the initiative). v16a and v_d3 Givens use the initiative form. Reading A: the initiative's `fulfils` field, plus a request side for v_d1. Reading B: request side only. The spec does not fix the file form.
C2 v_d1 is two rules under one code: keep the part-open clause (grammar.md:224-226 "v_d1 extended" keeps both) and add the request clause. One label cannot fit both; the spec table has no row for the old clause.
C3 v3: the dead needs rule and r116's resolution rule share code and `#show v3/…`. grammar.md:131 is the v4 resolution rule; the needs rule belongs to v3 grammar (replaced in v4, grammar.md:131 comment). Plan removes or renames the old one.
C4 "this context" asker (v_d1 Examples). The asker field is free text (workqueue_request.py:75, `--from`). Reading A: the asker equals the context path `missingmass.io/shopsystem/shopsystem-bdd`. Reading B: the asker is the upstream/this repository's own name, which is nowhere in the files. The Examples `another context` must be `does not name` under either reading.
C5 `source` on requests: grammar.md:73 allows initiative, request and job-thread sources, but model.lp v9e/v10a and the v18 Given (initiative whose source names a request) assume origins only. Reading A: new `source` facts for requests and the rule relaxed to allow requests. Reading B: a separate relation (e.g. `request_source`) so v9e/v10a stay.
C6 v17 "cites an origin": reading A: any `source`. Reading B: only origin kinds (observation, measurement, review-finding, model.lp:42). The scenario cites an observation, so both pass it.
C7 v18 against check_id: a node's own id in another context already gives a file problem (model_facts.py:83-87). v18 is for references (the scenario's source). Plan must say whether an own id of a foreign path also prints v18.
C8 v16a threshold: the spec gives 2026-10-23 as a literal, not "today". Comparison of the date string works (YYYY-MM-DD); model_work.py:117-122 validates the form.

## 8. The file set

Changed (production):
- scripts/model.lp (304 lines; not Python, outside the 300 limit): labels and rules for v16a, v_d3, v17, v18; v_d1 request clause; v3 replaced; `#defined` for new facts; `#show` lines. Search: this file, grep of the codes.
- scripts/model_facts.py (275 lines, room 25): KINDS gains `request`; `qualify`, `want`/`check_refs` for the v18 foreign-id fact; Model fields for requests. Search: refs `check_id`, `qualify`.
- scripts/model_work.py (213, room 87): `dated` fact from `date`; `fulfils` read; the directory loop skips requests/ (D1). Search: read_work, read_part.
- A new module scripts/model_requests.py (new concern, reads .shop/work/requests/*.md; needs a row in CLAUDE.md's module map) — recommended, not existing. Read: model_work.py is at 213 and the request reader would add about 80 lines.
- scripts/model (137, room 163): CONTRACT text lists the request reading (r19). Search: CONTRACT.
- scripts/model_parse.py (271, room 29): only if `## Resolution` entries need a parser; read.

On the path, not edited but must keep passing:
- scripts/model_check.py (139, room 161): solves with model.lp; `rule_order` by text position; no edit unless labels move.
- scripts/model_report.py (87, room 213): `why`; keeps its trace of proposals; no edit needed (read).
- scripts/workqueue_request.py (114, room 186): writer of the request form; read only (its form is what the reader must match).

Tests:
- tests/scenarios/test_design_model_check.py (53, room 247): add an import line for a new steps module.
- tests/scenarios/design_model_check_given.py (244, room 56): Givens for the six scenarios (or a new module).
- tests/scenarios/design_model_check_then.py (227, room 73): generic `<code> names <ids>` and `does not name`.
- tests/scenarios/design_model_check_problems.py (300, room 0): not to be edited; a new steps module instead.
- tests/scripts/test_model.py (213, room 87): RulesTest must keep passing; new unit tests optional.
- Suggested new module tests/scenarios/design_model_check_requests_steps.py for the request Givens (new concern, one module).
