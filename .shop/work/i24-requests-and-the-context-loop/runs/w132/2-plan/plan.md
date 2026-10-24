# Plan of w132: model check's request rules v16a, v_d1, v17, v3, v18, v_d3

Under design-model-check; accepts r113, r114, r115, r116, r117, r119. There is nothing to retire and no ruling.

**The research notes are out of date in one way.** Since the research ran, the base has gained the reading of requests (r19, r112). `scripts/model_requests.py` exists. It reads `.shop/work/requests/q<n>.md`, checks the request's form and emits `node`, `status` and the check of its id. `read_work` skips `requests/`, so defect D1 is gone. `KINDS` holds `request`. `tests/scenarios/design_model_check_requests.py` holds the r112/r118 Givens and `request_text`. Section 2 of the notes (what the system answers) and section 4 (no test breaks) still hold for everything below.

## 1. What goes green

All 14 cases are red today. Each one fails with StepDefinitionNotFoundError on its first Given. The Then steps of the form "`<code>` names / does not name" do not exist, and model.lp has no rule for any of these clauses (notes §1, §2).

- **design-model-check#r113**, "an initiative dated after 2026-10-23 that fulfils no request is v16a".
  - Red because model.lp has no v16a. The initiative reader emits `age` but no date and does not read `fulfils` (P1).
- **design-model-check#r114**, "a done initiative whose own request in this context is not delivered is v_d1", 5 Examples.
  - Red because v_d1 is only the part-open clause, and nothing reads a request's asker, `part_of` or `source` (P2, P3).
- **design-model-check#r119**, "a delivered request whose initiative is not done is v_d3".
  - Red because model.lp has no v_d3 and nothing emits a fact for `fulfils` (P4).
- **design-model-check#r115**, "a request that is part of no job-thread and cites no origin is v17".
  - Red because model.lp has no v17 and a request's links are not read (P5).
- **design-model-check#r116**, "a delivered request whose resolution names a requirement the spec does not have is v3".
  - Red because today's v3 is the dead `needs` rule (model.lp:93-95) and `resolution` is never emitted (P6).
- **design-model-check#r117**, "an id of a kind kept in .shop/work/ with another context's path is v18", 6 Examples.
  - Red because model.lp has no v18. Such a source gives only v10a and an unresolved reference (P7, P7b, P7c).

## 2. Where the change lands

- `scripts/model.lp`:
  - new rules, each with its `label` and `#show`: v16a/1, v_d3/1, v17/1, v18/1, and v3/2 in place of v3/1;
  - a second v_d1 clause, and a single label for v_d1 that covers both clauses;
  - `#defined` for each new fact.
  - Every new label goes in the violation section, above the `w_` labels, because the order of rules is the order of the text.
- `scripts/model_requests.py` (49 lines): the request reader also emits:
  - its asker;
  - its `part_of` and each `source`, under request-only relations (decision 3);
  - each `## Resolution` entry as a resolution fact naming a requirement.
- `scripts/model_work.py` (216 lines): an initiative's `date` gives a date fact as well as `age`, and its `fulfils` field gives a fact for `fulfils`.
- `scripts/model_facts.py` (277 lines, room for 23): where `qualify` passes another context's full id through (line 79), it records a fact for v18 when the id's kind is kept in `.shop/work/`.
  - If this would take the file over 300 lines, the implementer stops and reports it. Do not split the file in this work-item.
- `tests/scenarios/design_model_check_requests.py`: the Givens of the six scenarios, built on `request_text`, extended to set the asker, `part_of` or `source`, the status and the resolution:
  - an initiative with a date that fulfils no request or a given request;
  - an initiative with a status;
  - each request phrasing;
  - the capability with r1 and no r9;
  - the bounded-context Given and "nothing in the repository has the id".
- `tests/scenarios/design_model_check_then.py` (227 lines): one generic pair of steps, "`<code>` names `<ids>`" and "`<code>` does not name `<ids>`" (ids joined by "or" or "and"), read from `model check --json`. Also the step "once i1 is done, v_d3 does not name q1", which rewrites i1's status and runs the check again.

Removed from the researcher's set:
- the new module `model_requests.py` (it exists now);
- `scripts/model`, whose CONTRACT already lists the reading of requests (line 36);
- `model_parse.py`, because a `## Resolution` entry is a numbered line that the request reader can read itself;
- `test_design_model_check.py`, because no new steps module is added.

## 3. Decisions

1. **An initiative carries `fulfils`.** It is one request id, read with `qualify` and the kind `request`. A request has no field that points back.
   - Rests on: r113 and r119, whose wording is "an initiative … that fulfils"; work-queue#r22 (`work start` writes an initiative that fulfils the request); grammar.md:75, `fulfils(I, Q)` initiative → request; the capability's Implementation, "facts use grammar.md's relation names".
   - `fulfils` is not added to r24's list of fields resolved as unresolved references.
2. **v16a compares the initiative's `date` with the literal 2026-10-23.** It does not compare it with today. An initiative with no date, or with a malformed date, is not v16a; a malformed date stays the r27 file problem.
   - Rests on: r113.
3. **A request's `part_of` and `source` go under request-only relations, not under `part_of` and `source`.** Read through grammar.md's `part_of` and `source`, a request with `part_of` i1 would fire v_k3, v_k5 and v_d2, and a request whose source names i1 would fire v9e and v10a. No requirement asks for any of that. Today requests give none of those rows, and they still give none.
   - Rests on: design-model-check#r10, #r34 and #r59, whose rules range over parts, and a request is not a part kind (model_work.py PART_KINDS).
4. **The asker counts as "this context" when it is `internal` or the bounded context's own id.** A request is "kept in this context" when it is read from `.shop/work/requests/`; r46 already refuses a request whose own id is not of this context. The v_d1 Given for "another context" writes another bounded context's id.
   - Rests on: r114; the requests capability's Implementation (the asker is a context id, `internal` or the product level); grammar.md:51 ("the upstream itself when internal").
5. **v_d1 keeps its part-open clause and adds r114's clause under the same code.** The added clause: i1 is `done`, and a request whose asker is this context and whose `part_of` or `source` names i1 is not `delivered`. The single label names both cases.
   - Rests on: r114; design-model-check#r36, which needs the part-open clause; grammar.md:224-226 ("v_d1 extended").
   - RulesTest wants one label for each code, which is why there is a single label.
6. **v17 holds for a request that is not part of a job-thread and does not cite an origin.**
   - "Part of a job-thread": its `part_of` names a node of kind `job-thread`.
   - "Cites an origin": a `source` names a node of an origin kind (`origin/1` in model.lp: observation, measurement, review-finding).
   - A source that names an initiative is not an origin, as v10a's label already says.
   - The request of the v17 Given needs a `part_of` that is not a job-thread (an initiative). Without one it fails r112's form check ("neither part_of nor source") and becomes a file problem, not a request.
   - Rests on: r115; r112.
7. **v3 replaces the dead `needs` rule (model.lp:93-95).** It becomes v3/2 over (request, requirement), for a request that is `delivered` and whose resolution names an id that is not a requirement node.
   - The requirement part of each `## Resolution` entry (`<n>. <requirement> <version>`, the form `work resolve` writes) is read with `resolve_req`.
   - An entry that is not a requirement reference is the dangling problem `resolve_req` already reports. A well-formed reference to a missing requirement is v3 only, not an unresolved reference as well.
   - Rests on: r116; grammar.md:124 and :131 (`needs` is gone in v4); r24, whose list of fields does not include a resolution.
8. **v18 judges each id that `qualify` reads from this context's files, the node ids themselves included.**
   - The kinds kept in `.shop/work/` are: initiative, the part kinds (PART_KINDS), and request.
   - An id fires v18 when it has the full form `<kind>/<context path>/<name>` with a context path other than this one.
   - Whether anything has the id plays no part. Unresolved references and v10a stay as they are.
   - A node whose own id is foreign keeps r46's file problem and gives v18 as well, because r117 says "an id in this context's files".
   - Rests on: r117.
9. **v_d3 holds when a request is `delivered`, some initiative fulfils it, and that initiative is not `done`.**
   - Rests on: r119; grammar.md:228.

## 4. Tests the decisions break

None. Here is what was checked, from notes §4 and the current code:
- **tests/scripts/test_model.py RulesTest** (every `#show` has exactly one label) keeps passing. v3's label is replaced, not added to; v_d1 keeps one label; each new code gets one.
- **design_model_check_trace.py `_lp_labels`** keeps passing, because the new labels sit above the `w_` labels.
- **v16a fires on no existing fixture.** The fixture initiatives are dated 2026-10-15 (tests/scenarios/conftest.py:141, test_model.py:121).
- **The existing request fixtures fire none of v17, v_d1 or v18.** The `request_text` of the r112/r19 tests (asker `internal`, source obs-1) has a source of an origin kind, so it is not v17, and names no initiative, so it is not v_d1. Its ids are of this context, so it is not v18.
- **No test asserts the old v3 (`needs`) or the old v_d1 label.** By search; there is no tests-of map.

## 5. Open cases

The scenarios are silent about these. The implementer names each one in the report.

- **This repository's own `model check`** will report v16a for i24 (dated 2026-10-24, no `fulfils`) until i24 fulfils a request. Name it if a branch check runs `model check` on the repository.
- **An asker written as a bare context path** (`missingmass.io/shopsystem/shopsystem-bdd`, without `bounded-context/`), or as the product level, under v_d1.
- **A `fulfils` that names a request nothing in the repository has**, under v16a and v_d3.
- **A request's `part_of` that names a job-thread id nothing has**, under v17.
- **`w_uncited_obs` still counts an observation that only a request cites** (P5). The relations of decision 3 leave it as it is today.
- **v18 for an id that `qualify` never sees**, for example inside a decision's `source`, which is only resolved.
- **A malformed `## Resolution` entry** (no version, or not numbered).
