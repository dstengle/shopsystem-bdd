# Branch review 3 of i39 (Requests go through one shared tool)

**Verdict: DONE_WITH_CONCERNS.** Two findings are triaged fix now, both in w206:

1. **Code no line asks for.** `scripts/supervise_change.py:79-89,108-111` merges a redraft round's ids into another held capability-proposal's lists. No Behaviour line in `spec/capabilities/supervision.md` asks for this. The line is carried in request q20 (line 3), which is still `open` and not integrated.
2. **Data left invalid.** `scripts/supervise_change.py:112-115` points that other proposal at the redraft round's drafts. A proposal not yet applied loses the only pointer to its own drafts, and its gate and apply rounds then read another round's drafts (probe below).

One check could not be verified, carried from reviews 1 and 2: whether a real `claude -p` integrate round can read the upstream's spec outside its worktree (w202).

w206 fixes review 2's fix-now findings 1 and 2 and its observation 3:
- another proposal's applied ids are kept;
- `list --json` gives no `turn`;
- a malformed `raised.jsonl` line is refused without a traceback.

No change under `features/` comes from i39's work-items, and no test was removed or weakened.

## Range and work-items

- **Range:** `b4c4ad5e..ba907c58` on `main`.
  - Reviews 1 (`..d3079697`) and 2 (`..e4c0b40f`) covered the earlier part. I re-ran every check on the whole range.
  - I read in full only what changed after `e4c0b40f`.
  - `git diff --stat e4c0b40f HEAD -- scripts tests features` shows only w206's five files.
- **w202** (spec-integration#r44, `green`): `6e3c4f04` and `fe844bb3`. Unchanged since review 1.
- **w205** (work-queue#r34-r39, `green`): `a033c460` and `bf231ddc`. Unchanged since review 2, except where w206 changes `scripts/workqueue_list.py`.
- **w206** (fix of branch review 2, accepts work-queue#r34-r39, `green`):
  - Its commits run from `694a5f8e work: w206 ready -> claimed` to `85589330 work: w206 claimed -> done`.
  - Leaving out `work run`'s own commits, that is `e4e61321` "Fix branch review 2 findings…". It touches `scripts/supervise_change.py`, `scripts/supervise_rounds.py`, `scripts/workqueue_list.py`, `tests/scripts/test_supervise_change.py` and `tests/scripts/test_workqueue_list.py` (new). All five are in its fileset.
  - After `85589330`, the commits are `work` commands only: `61fb5d8d`, `b5bf81a4` (`work request: q20`), `7abd1e9e` and `ba907c58`.
- **Other commits after review 2:**
  - `69a0f839` commits branch review 2 (`work run`).
  - `40a0caa5` is a `work note`.
- **Commits that belong to no work-item:** none new. `2ae8e313` (the hand restoration) is carried from review 2, observation O6.

## Suite

`Suite: 965 passed, 16 failed at ba907c58 in 26.42 s` (`python3 -m pytest -q -p no:cacheprovider`; wall time 26.7 s).

- **Parallel:** yes, `-n auto` from `pytest.ini`.
- **In-process:** no. The steps drive `scripts/work` as a subprocess. The suite runs under 60 s, so this is not a finding.
- **The 16 failures** are the same 16 as in review 2. Each is a `StepDefinitionNotFoundError` on a scenario that is formulated but has no work-item yet:
  - 14 requests scenarios
  - design-model-check @r120
  - supervision @r135
- **With `-p work_items --work-item w206 --whole-suite`:** `965 passed, 1 skipped, 16 xfailed in 26.60s`. Nothing fails.

## Checks

- **w202** (`-p work_items --work-item w202`): 148 passed, 1 skipped, 56 subtests passed in 6.45 s.
- **w205** (`--work-item w205`): 154 passed, 1 skipped, 56 subtests passed in 3.92 s.
- **w206** (`--work-item w206`): 154 passed, 1 skipped, 56 subtests passed in 4.09 s. With `--whole-suite`: as above, 0 failed and 16 xfailed.
- **w206's new unit tests** (`-n 0 tests/scripts/test_workqueue_list.py tests/scripts/test_supervise_change.py`): 4 passed.
- **`tools check --base b4c4ad5e`:**
  - **ruff:** 28 errors (25 at review 2).
    - New in w206: `scripts/supervise_change.py:88` B023, twice (`field` and `mine`). Finding 5.
    - From before w206:
      - `supervise_change.py:114` B023 (w204)
      - `tests/scripts/test_supervise_change.py:7` RUF100 (w204)
      - `tests/scenarios/supervision_reintegrate_steps.py:13` F401 and `:137` FURB167 (w204)
      - `tests/scenarios/test_supervision.py:14` I001 (w204)
      - `tests/scenarios/test_work_queue.py:7` I001 (from before base)
      - `tests/scenarios/work_queue_list_steps.py:79` RUF015 (w205, dropped in review 2)
      - the round helper scripts committed under `.shop/work/{i39,i41}/runs/` (O5)
  - **vulture:** `tests/scenarios/work_queue_status_steps.py:77`, unused `notes`. The line is from before base.
  - **import-linter:** "the project states no import contracts". It is not `missing`.
- **`tools size --limit 300`:** printed nothing and exited 0. `supervise_rounds.py` is 229 lines and `supervise_change.py` is 126.
- **`features deprecated`:** 14 deprecated scenarios, as in review 2.
  - Their replacements have no `green` work-item: design-model-check @r120, requests @r44 and @r45.
  - The other 11 are deprecated for removal: design-model-check r117, 5 supervision scenarios, and work-queue r3, r11, r16, r17 and r18.
  - None is due for retirement.
- **`features bindings`:** "every binding names a scenario".
- **Dry-run against real mode:** not applicable. No operation the branch touches has a dry-run mode.

## Removed and weakened tests

None.

**What I searched for:**
- `git diff e4c0b40f HEAD -- tests features` has 0 removed lines.
- `git diff b4c4ad5e HEAD -- tests` adds no `skip`, `xfail` or `parametrize`.
- In `tests/scripts/test_supervise_change.py`, w206 adds a helper (`proposal`) and one test. The existing test and its helper `write` are unchanged.
- Review 2's list for the earlier range stands: setup-only step changes in w205, and no assert changed.

## Allowances

- **w206 `4-implement/report.md`:** "none". This holds: no existing test changed.
- **w205 and w202:** as in review 2, they hold.

## Cannot verify

- **(w202, carried from reviews 1 and 2)** Whether a real integrate round, `claude -p` with `Read` and no `--add-dir`, can read the upstream's `spec/` at a path outside its worktree.
  - Only a real session would show it, and I do not start one.

## Findings

### 1. Important, fix now (code no line asks for): a redraft round merges its ids into another held proposal's lists (w206)

- **Where:** `scripts/supervise_change.py:79-89` (`merge_lists`) and `:108-111`, called from `scripts/supervise_rounds.py:195`.
- **What is wrong:**
  - No Behaviour line asks for this. r92, r142 and r148 (`spec/capabilities/supervision.md:46,59,65`) speak only of the proposal being drafted anew.
  - The line that would ask for it is q20, line 3 (`.shop/work/requests/q20.md`, `b5bf81a4`). q20 is `open`, with `turn: upstream`, and it has not been integrated, so the line is not yet in the spec.
- **Why it matters:**
  - Behaviour reaches code only through a line. Until q20 is integrated, nothing in the spec keeps the merge, and a later change could take it out without breaking a scenario. Only the unit test `test_a_round_started_for_one_proposal_merges_its_ids_into_another_held_proposal` holds it.
  - The w206 review (stage 6) closed this on the person's answer of 2026-10-27, "carried in q20, line 3". By this review's rule, it stays fix now until that line is written.
- **Fix:** integrate q20 line 3 through integrating-a-proposal and formulate its scenario. Or confirm that i39 closes with this line carried by q20.
- **Note:** the merge itself is right. It fixes the data loss of review 2's finding 1, and the probe confirms that p2's own ids are kept.

### 2. Important, fix now (data left invalid): another held proposal is pointed at the redraft round's drafts (w206)

- **Where:** `scripts/supervise_change.py:112-115`. On the merge path this is plan D-f.
- **What is wrong:**
  - When a round started for p1 merges into p2, it also replaces p2's "The drafts of this proposal are in …" with p1's round's drafts path.
  - p2's gate and apply rounds take their `Drafts path:` from that sentence (`scripts/supervise_brief.py:76-79`). p2's integrate round takes its `Earlier drafts path:` from the same sentence (`supervise_brief.py:56-59`).
  - So if p2 has not been applied (`drafted`, `awaiting-answer` or `approved`), it loses the only pointer to its own drafts. Its apply round then applies p1's round's draft of p2's capability. That round was briefed with p1's earlier drafts only, not p2's.
  - The apply round's change list then replaces p2's lists (`rewrite_lists`, r114, `supervise_rounds.py:166-167`). That drops the ids p2's own drafts held, which the merge had just kept.
- **Why it is fix now:** the proposal is left naming drafts that do not hold its lines. This is data left invalid, and on apply its lines are lost.
  - In i39 every other proposal had already been applied when the redraft ran, so i39's own data is not harmed.
  - The state is reachable whenever proposals of one initiative are at different stages, which is how `work run` takes them side by side.
- **Reproduction:**
  - A pytest probe in `.shop/scratch/i39-branch-review/`, since deleted. i1 holds p1 (`thing`, `drafted`) and p2 (`other`, `approved`, adds `[other#r1]`, removes `[other#r3]`, drafts `runs/p2/1-integrate/drafts/round-1/`).
  - It ran `write_proposals(entries({"changes": [{thing adds thing#r5}, {other adds other#r2, other#r3; removes other#r1}]}), "runs/p1/5-integrate/drafts/round-1/", "p1")`.
  - p2 came back as `status: approved`, `adds: [other#r1, other#r2, other#r3]`, `removes: [other#r3, other#r1]`, with "The drafts of this proposal are in runs/p1/5-integrate/drafts/round-1/."
- **Fix:** on the merge path, leave the other proposal's drafts sentence as it is, so the replacement at `:112-115` runs only when `held.stem == own`. If the round's drafts for that capability must also be read, add them as a second sentence and have `supervise_brief.py` read every one. This also needs a line in q20.
- **Keep as a test** (`tests/scripts/test_supervise_change.py`): p2 `approved` with drafts `old/`, then `write_proposals(..., "drafts/", "p1")` with an entry for p2's capability. Assert that p2 still says "The drafts of this proposal are in old/."

### 3. Minor, observation: the merge leaves one id in both `adds` and `removes` (w206)

- **Where:** `scripts/supervise_change.py:85-88`. Each field is merged on its own.
- **What is wrong:** in the probe of finding 2, p2 came back with `other#r1` and `other#r3` each in both `adds` and `removes`. A gate round would then ask about an id that is both added and removed, and an apply round could not apply both.
- **Why it is an observation:** no line names this edge (plan §5 left it open, and the report says "both kept, unchosen"). No round in i39 has hit it.
- **Fix:** when q20 line 3 is integrated, settle which list wins. For example, an id the round removes leaves the proposal's `adds`.

### 4. Minor, observation: a first integrate round also merges (w206, carried from the w206 review)

- **What:** `supervise_rounds.py:195` passes `name`. For the initiative's first integrate round, `name` is the initiative, so every held proposal is merged into.
- **The gap:** q20 line 3 covers only a round "started for a capability-proposal".
- **Fix:** widen q20 line 3 to "a round of the kind `integrate`" when it is taken in.

### 5. Minor, drop: ruff B023 at `scripts/supervise_change.py:88` (w206)

- This is a false positive: `re.sub` calls the lambda within the same loop iteration.

### Carried from review 2, unchanged

- **O6, Minor, observation (no work-item):** `2ae8e313` is a commit made by hand outside any work-item or round. Nothing is wrong in it.
- **Minor, drop (w205):** RUF015 at `tests/scenarios/work_queue_list_steps.py:79`.

### Review 2's findings, now resolved

- **Finding 1 (data lost):** fixed by w206. Another proposal's ids are kept: the unit test passes, and the probe agrees.
- **Finding 2 (`turn` in `list --json`):** fixed. `workqueue_list.py:46` gives `{"request", "status"}`, and `test_list_json_gives_each_request_and_its_status_and_nothing_besides` passes.
- **Finding 3 (malformed `raised.jsonl`):** fixed. `workqueue_list.py:29-36` raises `Refused`, naming the file and the line (r7, `spec/capabilities/work-queue.md:40`), and the unit test passes.

## Shape

- **CLAUDE.md, size limit 300:** met. `tools size` printed nothing.
- **Module map, `scripts/supervise_change.py`** ("its writing of one drafted capability-proposal for each capability it names"):
  - Merging into a held proposal is within that concern, so it is met.
  - The module now imports `workqueue` for `frontmatter`, as `supervise_rounds.py` already does.
- **Module map, `scripts/supervise_rounds.py`:** met. Only the call at `:195` changed.
- **Module map, `scripts/workqueue_list.py`:** met. The refusal is in the reader of `raised.jsonl` that its row names.
- **`tests/scripts/` row ("tests of the scripts that no scenario drives"):**
  - `tests/scripts/test_workqueue_list.py` tests `work list`, which r34, r35 and r39 drive.
  - It is there because r35's step does not check "and nothing besides", and no scenario covers a malformed record.
  - Observation: move these checks into `work_queue_list_steps.py`, by making `gives_pairs` check every key, once a line covers the refusal. A check that shows it complete: the r35 scenario fails if `turn` is put back.
- **Carried from review 2:**
  - `workqueue_status.py`'s row becomes `work show <initiative>` when `work status` is retired.
  - `spec_integration_steps.py` holds two concerns (r44, r45).
  - The no-target `show` goes dead when requests#r13, work-queue r3 and r11 are retired.
- **Reachability:** w206 adds no step definitions. `merge_lists` is reached only by the unit test and by a real redraft round (finding 1).

## Coupling

- **`raised.jsonl`:** as in review 2. Nothing writes it yet. The writers would be requests#r29 and supervision#r135, both xfail.
  - Its form is given only in `workqueue_list.py`. w206 now refuses a line that lacks `upstream`, `request` or `status`, which narrows the form a future writer must meet.
  - What would make it stable: state the form in the Implementation section of work-queue or requests.
- **q20:** w206's behaviour is promised by an open request (finding 1), and q20 also carries work-queue r48 and r40 (the gate's answers that apply round 8 dropped).
- **Carried from reviews 1 and 2:**
  - the upstream's spec is read from a working-tree path (w202);
  - Claude Code's `-p` read scope (w202);
  - pytest-bdd's private `__scenario__` (`work_items.py`) and its 560 `PytestRemovedIn10Warning`s.

## Observations

- **F3 (w206):** an id lands in both `adds` and `removes`. Reproduction: the probe of finding 2 gave `adds: [other#r1, other#r2, other#r3]` and `removes: [other#r3, other#r1]`.
- **F4 (w206):** the first integrate round merges. Reproduction: read `supervise_rounds.py:195` (`write_proposals(..., name)`, where `name` is the initiative) against q20 line 3.
- **O1 (w205):** open questions are counted by position. Reproduction as in review 2.
- **O2 (w205):** a work-item with no `kind` gives the refusal "is a None". Reproduction as in review 2.
- **O3 (w205):** `list --json` does not carry r39's waiting. Reproduction as in review 2.
- **O4 (w205):** `open_with_proposal` ignores `{state}`. See `work_queue_status_steps.py:14-19`.
- **O5:** round helper scripts are committed under `.shop/work/*/runs/` and fail ruff (19 of the 28 ruff errors). Reproduction: the `tools check` output above.
- **O6:** `2ae8e313`, a commit made by hand. Reproduction: `git show --stat 2ae8e313`.

The probe was a pytest file in `.shop/scratch/i39-branch-review/`, run with `-n 0 -s`, and the directory is deleted. Its reproduction is in finding 2.
