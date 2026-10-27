# Review of w211 (narrowed: r25, r29-r34, r44, r45; no transport)

**Verdict: DONE_WITH_CONCERNS.** Two Important findings are fix now. Both are about how a command decides a request's side in a repository whose spec/index.md lists `## Upstreams`: (1) such a repository can no longer raise an internal request or give one a line outcome; (2) r34 is applied to `work outcome` only. Nothing is Critical: `features/` changes only by the two retirements the work-item lists. No test is removed or weakened beyond a Minor loosening of a shared step. tools check: vulture reports one issue (Minor). tools size: clean.

## Commits reviewed

The branch `work/w211` is gone, so the commits were taken from HEAD. They are those between `31862091 work: w211 ready -> claimed` (the last claim) and `fac769e5 work: w211 claimed -> done`:

- `91b7750d` requests: the gate of work request, the side check of work outcome, work show of a request; retire r1 and r3 scenarios (r25, r29-r34, r44, r45)

This matches the commit list in the implementer's result (6-implement/result.json). The earlier transport commits 8712f769 and 31436ec1 were reverted by 66c0c84a and 39a69952. `git diff --stat a82b4227 39a69952 -- . ':!.shop'` is empty, so the revert is complete.

## Removed and weakened tests

What I searched for: deleted step functions and test functions, parametrize cases, changed `assert`s, skip and xfail, and changed scenario lines in `features/`.

- `features/requests.feature` `@r1 @deprecated` and `@r3 @deprecated` were removed. Both are listed under the work-item's Retires and the plan (3-plan §4, D1), and were retired with `features retire` (`retired: [r6, r1, r3]` in the capability). This is allowed.
- `requests_write_steps.py`: the steps `lines_and_asker`, `names_origin` and `prints_id` were removed. Only the retired @r1 used them, and the new steps of r44 in `requests_world_steps.py` (`lines_are`, `names_asker`, `prints_new_id`) prove the same per row. Not weakened.
- `requests_write_steps.py`: `keeps_one_open` and `keeps_one` were removed and rewritten in `requests_world_steps.py:84-91`.
  - Before, they asserted that the only request kept is `q1.md`. Now they assert that exactly one new request is kept, under any id. That is a loosening.
  - `keeps_one` is also used by the live r19 (requests.feature:59) and r29 (:49), not only by the retired scenarios, contrary to the report's "which the retired scenarios used".
  - r19 still reads `q1` in `delegation_is`, so that scenario as a whole proves what it did. Graded Minor (finding 4). The plan does not list it.
- `test_requests.py`: two imports were added and nothing removed.

## Allowances

- `requests_write_steps.py upstream_keeps_none` (setup): **holds.** The diff changes only the id written into spec/index.md (from conftest's `INDEX` to `bounded-context/ctx-a`). It adds, removes or changes no assert, expected value or parametrize case. The plan names it under §4 (D6).
- "Removed with `features retire`: keeps_one_open, keeps_one, lines_and_asker, names_origin, prints_id": **holds only in part.** It is neither a `setup` row nor an `interim` row. It holds for the three steps only @r1 used. It does not hold for `keeps_one` and `keeps_one_open`, which live scenarios also use and which were rewritten with a looser assertion (finding 4, Minor, since r19 still pins q1 elsewhere).

## Cannot verify

- **No plan for what was built.** 2-plan and 3-plan plan the git transport that was reverted. The narrowed implementation (the gate, the outcome side check, the `show` of a request, the one-repository test world) was built from the coordinator's narrowing note in the work-item, not from a plan. I cannot check its decisions against a plan.
- **r25's "take in".** The capability's r25 names take-in among the one set of commands, but no take-in command exists (deferred to w212). The r25 scenario passes because `argv_of` returns None for "takes in …" and `each_one_command` accepts None (`requests_flow_steps.py:28-29, 67`). Whether r25 is delivered without a take-in is for the person, given the narrowing.
- **r28's "upstream keeps".** r29/r44 rows run by an asker: what "the upstream keeps" is bound to the one shared repository (report, Open questions). Delivery to a real upstream is w212.
- **The red-green cycle.** The report says the scenarios were not taken red one at a time.

## Findings

### 1. Important, fix now: a repository with `## Upstreams` can no longer raise or settle an internal request
- **Work-item:** w211.
- **Where:** `scripts/workqueue_request.py:99-105` (`gate`) and `:143-145` (`outcome`).
- **What is wrong:**
  - `gate` decides "the asker is not the upstream itself" (r30, r31) from whether spec/index.md has any `## Upstreams` bullet. The asker must already be the repository's own id (r32).
  - So in any context that lists an upstream (a consuming repository depending on, e.g., billing, as in docs/capability-format.md:202), every `work request` is treated as a request to an upstream. An internal request with `--source` (r44, first row) is refused with "an origin belongs to an internal request". One with only `--thread` is written into the repository's own queue as if it were the upstream's.
  - `outcome` then refuses every line outcome on any request whose asker is the repository's own id, internal requests included ("is a request to the upstream …").
  - Such a context can neither raise its own internal requests from observations nor take one through r15/r8/r9. That contradicts r44, r15 and r25 ("every asker and every upstream one set of commands … and one lifecycle"). No transport exists to carry the request anywhere else, so the request stays in a repository where no side may settle it.
- **Why it is not caught:** every scenario's upstream ctx-u has no `## Upstreams`, so none covers a context that both asks an upstream and is the upstream of its own requests. Plan 3-plan §5 named this case as open ("a repository … that has an upstream setting and also raises an internal request").
- **Verified by:** reading `gate`/`outcome` against the `upstreams()` parser (`:87-92`), and the `## Upstreams` form in docs/capability-format.md:193-203. No repository probe: `git init` is not a command allowed here.
- **Fix:** take the side from what names the request's upstream, not from the mere presence of upstreams (e.g. a request to an upstream names it). Without a transport (w212), that needs a ruling first: put the question to the person, or narrow r30/r31/r34 to where an upstream is named.

### 2. Important, fix now: r34 is applied to `work outcome` only
- **Work-item:** w211.
- **Where:** `scripts/workqueue_request.py:152-169` and `resolve` (`:187-`).
- **What is wrong:**
  - r34: "If a side writes a part of a request that is the other side's part, then `work` shall refuse, naming the side that writes that part, and change nothing." r4 and r5 name the parts: questions, line outcomes and resolution are the upstream's; lines and answers are the asker's.
  - The commits refuse only `outcome` by the asker. In the same asker repository, `work ask q1 …` (a question) and `work resolve q1 …` (the resolution) on its own request to the upstream still write the upstream's part.
  - `work reply` by the upstream on a request from another asker still writes the asker's answer.
  - The report names this as open ("no scenario asks"), but the line binds whether or not a scenario covers it.
- **Why it matters:** the asker can write the upstream's questions and resolution, which r34 and r5 say it never does.
- **Fix:** apply the same side check in `ask` and `resolve`, naming the upstream. For `reply` by the upstream, refuse naming the asker. That last one has no other path for an answer while there is no transport, so it falls under the same ruling as finding 1. Add a scenario row to r34 for each.

### 3. Minor, observation: the outcome refusal names only the first upstream
- **Work-item:** w211.
- **Where:** `scripts/workqueue_request.py:145`.
- **What is wrong:** `asked[0]` is named as "the upstream" even in a repository listing several upstreams. A request does not record which upstream it is for, so the name may be wrong.
- **Reproduction:** read from the code (spec/index.md with two `## Upstreams` bullets, then `work outcome` on an own request). Not run: it needs a git repository.

### 4. Minor, drop: the shared step "the upstream keeps one new request" no longer pins the id
- **Work-item:** w211.
- **Where:** `tests/scenarios/requests_world_steps.py:84-91`.
- **What is wrong:** it asserts one new request of any name, where it asserted `["q1.md"]`. r19 still reads q1 through `delegation_is`, so no scenario proves less. A later step that reads `new_request` would accept a wrongly numbered id.
- **Fix:** keep the id check where the Given leaves the queue empty.

### 5. Minor, drop: `names_asker` ignores what the scenario names (vulture)
- **Work-item:** w211.
- **Where:** `tests/scenarios/requests_world_steps.py:106` (vulture: unused variable `named`, 100% confidence).
- **What is wrong:** the step hard-codes `source: [o1, o2]` and `part_of: t1` instead of reading `named`. A new row naming other origins would assert the wrong thing.
- **Fix:** assert from `named`.

### 6. Minor, observation: every `work show` now reads every request's frontmatter
- **Work-item:** w211.
- **Where:** `scripts/workqueue_list.py:82-85`.
- **What is wrong:** `work show <work-item or initiative>` now first iterates `workqueue.requests(root)`, so a malformed request file stops a `show` that has nothing to do with requests. Reading `.shop/work/requests/<target>.md` alone would avoid it. No client sends this today.
- **Reproduction:** read from the code (a `requests/q9.md` whose frontmatter fails to parse, then `work show w1`). Not run.

### 7. Minor, drop: a second parser of `## Upstreams`
- **Work-item:** w211.
- **Where:** `scripts/workqueue_request.py:87-92`.
- **What is wrong:** it duplicates `supervise_brief.upstreams` with its own regex. The two can drift.

## Checks
- `python3 <Scripts>/tools check --base 31862091`:
  - ruff: all checks passed.
  - vulture: `tests/scenarios/requests_world_steps.py:106: unused variable 'named'` (finding 5).
  - import-linter: the project states no import contracts.
- `python3 <Scripts>/tools size --limit 300`: nothing printed (no file over the limit).

## Commands run
- `git log --format=%H -1 --grep="^work: w211 ready -> claimed$" work/w211` (branch gone)
- `git log --format='%h %s' --grep=w211 HEAD`, `git log --format='%h %s' -25 HEAD`
- `git diff --stat a82b4227 39a69952 -- . ':!.shop'` (empty: the revert is complete)
- `git show --stat 91b7750d`, `git show --stat fac769e5`
- `git show 91b7750d -- features scripts tests/...`
- `git show 91b7750d:tests/scenarios/requests_world_steps.py`, `…requests_flow_steps.py`, `…scripts/workqueue_request.py`
- grep of `--from`, `work request`, `## Upstreams` and of the removed step texts in features/; reads of conftest `INDEX`, `workqueue.requests`, `workqueue.entry`, `workqueue.context_path`, `supervise_brief.upstreams`, docs/capability-format.md §Upstreams
- `python3 /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts/tools check --base 31862091`
- `python3 /home/vscode/shopsystem-bdd/.shop/scratch/runner/scripts/tools size --limit 300`
