# Review of w209 (design-model-check r120, r121)

**Verdict: DONE.** No Critical finding and none triaged fix now. One Important-free review: two Minor findings (one observation, one drop).

## Commits reviewed

- The branch `work/w209` is gone. The commits are those between `aa345eeb work: w209 ready -> claimed` and `baaa1e6f work: w209 claimed -> done` on HEAD, less `work:` commits: one, `8823d293 design-model-check: v17 lets off a job-thread id and a raised-for request; v18 exempts a raised-for request (r120, r121)`.
- The implementer's result lists `c0603921`, the same commit before `work run` rebased it onto `1e72bfa4`. The patches are identical: `git show --format= c0603921 | sha1sum` and the same for `8823d293` both give `ee8bd0d4…`. Message, author and date match. See finding 2.
- Files: `features/design-model-check.feature` (-10), `scripts/model.lp`, `scripts/model_requests.py`, `tests/scenarios/design_model_check_requests.py`, `tests/scenarios/design_model_check_then.py`. All are in the work-item's fileset.

## Removed and weakened tests

None. What I searched for:

- **Features:** the only change is the removal of the `@r115 @deprecated` scenario "a request that is part of no job-thread and cites no origin is v17 (deprecated)", the one the work-item's Retires quotes word for word. The `@r115` tag is in the capability's `retired` list. This is an allowed retirement, not a removed test.
- **Given at `design_model_check_requests.py:99`:** the old Given "…part of no job-thread and cites no origin$" now matches r120's q1 phrase. Its body is unchanged (a request with `part_of` set to an initiative). `grep` finds no feature line left that uses the old phrase.
- **Then at `design_model_check_then.py:129`:** the pattern now also takes ", " as a separator, and ids exclude commas. Every existing Then line using v16a/v_d1/v_d3/v17/v3/v18 was checked with grep over `features/*.feature`. None has a comma in an id, and each splits as before. The assertions are unchanged.
- **Other test changes:** no assert was removed or loosened, and no skip or xfail was added.

## Allowances

The report gives "none", and none is needed: no remaining test's assertions changed.

## Cannot verify

- The report's full-suite record (968 passed, 8 failed at the start; 158 passed for `--work-item w209`). I did not run the whole suite. I ran only the focused scenarios: `-k "v17 or v18 or form"` gives 8 passed.

## Findings

### 1. Minor (observation): an asker given as this context's own id is not taken as internal by the form check
- **Where:** `scripts/model_requests.py:58`, `raised = data.get("raised_for") and str(data["asker"]).strip() != "internal"`.
- **What is wrong:**
  - The request file's form lets the asker of an internal request be written `internal` or as the context's own id. See requests' Implementation (asker "a context id, `internal`, …"), and `workqueue_request.py:44`, where `mine` holds both `internal` and `bounded-context/<own path>`.
  - requests#r45 refuses a request whose asker is the upstream itself when it names neither `--source` nor `--thread`. So `work request` never writes such a request with `raised_for` only.
  - But `model check` accepts that form when the asker is written as the own context id, and reports no file problem. Under r112 it should report one.
- **Reproduction:** `.shop/scratch/w209-4-review/test_probe_asker.py`, run with `python3 -m pytest -q -s -n 0 -p no:cacheprovider <it>`. It writes q1 with `raised_for: request/ex.com/prod/other/q7` and no `part_of` or `source`. What came back:
  - asker `bounded-context/ex.com/prod/ctx` (own): exit 0, 0 file problems;
  - asker `internal`: exit 1, the file problem "neither part_of nor source";
  - asker `bounded-context/ex.com/prod/other`: exit 0.
- **Why it is hardening:**
  - No client writes this today. `work request --raised-for` does not exist yet (research D2), so only a hand-written file has `raised_for`.
  - The plan's decision 3 names only "not internal", and no scenario covers this case.
- **Fix:** count both `internal` and `bounded-context/<this context's path>` as internal in `request_form`.
- **Work-item:** w209.

### 2. Minor (drop): the result names the pre-rebase hash
- **Where:** `3-implement/result.json`, `commits`.
- **What is wrong:** it lists `c0603921`, but HEAD has `8823d293`. The patch is identical (see above).
- **Fix:** nothing to fix in w209's code. This is a by-product of `work run`'s rebase.
- **Work-item:** w209.

### Checked, no finding
- **Contradiction with Behaviour or Purpose (none found):**
  - v17 (`model.lp:262-263`) lets off a request in two cases: one whose `part_of` id has the kind job-thread (`req_thread`, judged from the id, as r43 reads ids), and one whose `raised_for` is a `request/` id. This matches r120.
  - v18 (`model.lp:266-267`) exempts only an id that some request's `raised_for` names. This matches r121's "other than the request a request is raised for".
  - The labels follow r120 and r121. The v18 label leaves out "judged from the id alone", as plan decision 5 allows.
- **Code no line asks for (none found):**
  - `req_thread` and `req_raised_for` serve r120 and r121.
  - The `request_form` change serves r112 together with requests#r44 and r31: a request from another context's asker with `--raised-for` alone.
- **`world.cited`** is set only by `initiative_citing` and read only by the new q9 Given. In every r121 row, the initiative Given comes before `<raised>`.
- **A `raised_for` naming a non-request kind:** the form is accepted, but no `req_raised_for` fact is made, so v17 still fires. This is consistent; the report lists it as an open question.

## Tools

- `tools check --base aa345eeb…`:
  - **ruff:** 2 errors in `tests/scenarios/design_model_check_requests.py`, I001 (imports) and FURB167 (`re.M` at line 157). Both were there before the commit: the import block is unchanged, and the `re.M` call is at line 132 in `git show aa345eeb:…`. The commit only moved it. So they are already there, not from w209.
  - **vulture:** clean.
  - **import-linter:** the project states no import contracts.
- `tools size --limit 300`: printed nothing, so no file is over the limit.

## Commands run

- `git log --format=%H -1 --grep="^work: w209 ready -> claimed$"` → `aa345eeb`. `git log --oneline aa345eeb..HEAD`, `git show --stat c0603921`, `git show --stat 8823d293`, and `git show --format= <both> | sha1sum`.
- `git show 8823d293 --format=` (the diff, read once).
- `grep` over `features/*.feature` for the v-code Then lines and for the old Given phrase. `grep` of `spec/capabilities/requests.md` (r29, r31, r44, r45, asker) and of `scripts/workqueue_request.py` (asker, internal).
- `git show aa345eeb:tests/scenarios/design_model_check_requests.py | grep …` (were the ruff errors already there?).
- `python3 -m pytest -q -n 0 tests/scenarios/test_design_model_check.py -k "v17 or v18 or form"` → 8 passed.
- `python3 -m pytest -q -s -n 0 -p no:cacheprovider .shop/scratch/w209-4-review/test_probe_asker.py` → output above.
- `python3 <Scripts>/tools check --base aa345eeb…` and `python3 <Scripts>/tools size --limit 300`.
- `git status --short` → clean.
