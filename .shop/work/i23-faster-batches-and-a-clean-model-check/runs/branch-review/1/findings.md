# Branch review of i23-faster-batches-and-a-clean-model-check

**Verdict: DONE_WITH_CONCERNS.** One finding is fix now: Important, w109. `work run` never starts a work-item whose `blocked_by` names a green work-item in another initiative. Nothing is Critical, and every check was run and verified. Besides that there are one ruff error (Minor, w113), the observations below, and the commits that belong to no work-item.

## Range

`1ad6281..1620d96` (base: the commit that added `initiative.md`; head `1620d96`, branch `next`).

Work-items, and the commits between each one's `ready -> claimed` and `claimed -> done`:

| work-item | status | commits | accepts |
|---|---|---|---|
| w107 | green | 753c5a6 | analysis-tools#r7 |
| w108 | green | e00780e | migration-tools#r4 r9 r30 r31 |
| w109 | green | 4232bc6 | supervision#r1 r20 r59-r63 |
| w110 | withdrawn (after its review) | 5d88909, aecf1e7, 2e956ab (still on the branch; w115 accepts the same four ids and fixes its review finding) | batch-measurement#r47 r57-r59 |
| w113 | green | a3cb90e | work-queue#r15 |
| w114 | green | 8f76e50 | analysis-tools#r58 |
| w115 | green | 4ebe93b | batch-measurement#r47 r57-r59 |
| w116 | green | 495a420 | design-model-check#r27 |
| w117 | green | aaeea80 | design-model-check#r106 |
| w118 | green | 8a32a57 | design-model-check#r111 |
| w101-w106, w112 | withdrawn | none (no commit between claimed and awaiting-ruling/failed) | |
| w111 | withdrawn | none inside work run; c8eb828 and 6559731 were delivered outside it (F4) | delivery#r17 r18 |

The remaining commits are the initiative's formulation and records (spec:, features:, `work add`, `work:` notes). There are also unrelated records and design notes (b61404b…a1fffa7, 749ed8a, f9a5ed2, c29a521) and i22 housekeeping (1a7dc75); see F5.

## Suite

`Suite: 723 passed, 0 failed at 1620d96 in 14.53 s` (1 skipped: tests/scripts/test_tools.py:78 "nothing is missing here", which is the environment and not this branch; 56 subtests passed).

- It runs in parallel: `-n auto` is in pytest.ini's addopts, on 32 CPUs.
- It is not in-process: the step definitions drive `work`, `model`, `measure`, `migrate` and `tools` as subprocesses.
- At 14.5 s it is under 60 s, so this is no finding.

## Checks

No work-item names a `check:`. Each green work-item's acceptance is its scenarios. I ran `python3 -m pytest -q --work-item <w>` for each at HEAD:

| work-item | result |
|---|---|
| w107 | 139 passed, 1 skipped |
| w108 | 152 passed, 1 skipped |
| w109 | 150 passed, 1 skipped |
| w113 | 146 passed, 1 skipped |
| w114 | 139 passed, 1 skipped |
| w115 | 146 passed, 1 skipped |
| w116 | 150 passed, 1 skipped |
| w117 | 143 passed, 1 skipped |
| w118 | 139 passed, 1 skipped |

The skip in each is the test_tools.py:78 skip above.

`tools check --base 1ad6281` (exit 1):

- **ruff**: 1 error, `tests/scenarios/work_queue_answer_steps.py:2:1: I001 Import block is un-sorted or un-formatted` (F2). The ruff here is 0.17.0, the version the plugin pins.
- **vulture**: clean.
- **import-linter**: "the project states no import contracts". No heading says `missing`.

The other checks:

- **`tools size --limit 300`**: prints nothing. tests/scenarios/design_model_check_problems.py is at exactly 300 lines (touched by w116).
- **`features deprecated`**: two scenarios, both from i21 and not this branch's:
  - migration-tools @r15 "`migrate run` on a repository with <change> refuses… (deprecated)"
  - work-queue @r1 "add with --part-of… (deprecated)"

  The work-items for their replacements (i21 w86, w89, w90) are withdrawn, not green.
- **`features bindings`**: "every binding names a scenario".
- **Dry run against real mode**: `model decisions --check` against `model decisions` is the system's one dry-run/real pair (no branch change touches it). The suite has no randomized test that they agree (F7). My probe tried **40 cases**, all agreeing.

## Removed and weakened tests

I searched the test diff `git diff 1ad6281 HEAD -- tests` for removed `def`s and step decorators, changed `assert`s, parametrize and Examples rows, and `skip`/`xfail`. No skip or xfail was added.

1. **supervision_then_workers.py `one_at_a_time`** ("no worker was started before the one before it had ended"), removed by w109.
   - It proved the old one-worker-at-a-time pull.
   - It went with the retired deprecated @r1 scenario, which w109's Retires lists. w109's plan lists it under "Tests the decisions break".
2. **test_supervision.py `merged_in_line`**, removed by w109.
   - It went with the retired deprecated @r20 scenario. Retires lists it and so does the plan.
   - The new r61 Then (`merged_in_end_order`) asserts more: the order, and no merge commit.
3. **The deprecated @r20 "no more than two" scenario**, retired by w109. It is listed in both, and its Then stays in use.
4. **migration_safety_steps.py**, w108: the `notes/n1.md … about names` Given and Then were removed with the retired deprecated r4 scenario. Retires and the plan list it.
5. **migration_version_steps.py**, w108: the old-wording r30 and r31 Thens were replaced with the reworded ones. They went with the retired deprecated r30 and r31 scenarios, which the plan lists.
6. **analysis_tools_probe_steps.py `failed_command`**, w107: `assert "e1" not in stdout` is now `"e1"/"e2"` not among the whole lines, plus e3-e5 present.
   - This is loosened from a substring to a whole line, and also strengthened by the e3-e5 check.
   - w107's plan lists it under "Tests the decisions break" (D-a).
7. **batch_measurement_then_steps.py `gives_totals`**, w110: it now compares only the columns the table names.
   - This is loosened, and w110's plan lists it.
   - The r42 table (batch-measurement.feature:166-168) still names every column.
8. **work_queue_answer_steps.py**: the When "with an answer of two lines" now takes `{line_break}`. It went with the retired deprecated @r15 scenario (w113), and the row "a newline" keeps the old case.
9. **The deprecated @r47 batch-measurement outline**, retired by w110 (2e956ab). w110's and w115's Retires list it.

Every change under `features/` in a work-item's commits removes only a deprecated scenario that its Retires lists: e00780e, 4232bc6, 2e956ab and a3cb90e. There is no Critical.

## Allowances

- **w108 `setup`** (the r4/r9 Givens now commit): **holds**. The diff only moves and adds `old.commit()`, with no assert, expected value or example changed.
- **w113 `setup`** (test_work_queue.py `with_items` writes a log line for a ready item): **holds**. It adds a log write, and no assert changes.
- **w118** (test_model_output.py:14-19, "fixture only"): **holds** as setup.
  - The diff adds `self.observation()`, and the assertion line is unchanged. It is also in the plan.
  - The one warning counted is now `w_uncited_obs` instead of `w_unserved_cap`, as the plan says.
- **w107, w109, w110, w114, w115, w116, w117** give "none". I checked them against the diff and found no unlisted change to a test.

## Cannot verify

None. One caveat: ruff 0.17.0 (w114's pin) is the version installed here, and I did not query the package index, since no project content goes to an external service.

## Findings

### F1. Important, w109, fix now: a work-item blocked by a green work-item of another initiative is never started

- **Where**: scripts/supervise_pool.py:46-50 (`blocked`), with :62 (`statuses = dict(self.items())`) and supervise.py:60-61 (`items()` keeps only this initiative).
- **What is wrong**: a blocker in another initiative is never `"green"` in `statuses`, so the work-item stays blocked forever.
- **Why it matters**:
  - Ids are global (work-queue r12), and the repository itself uses blockers across initiatives: i10/w28 is `blocked_by: [work-item/w67]`, and w67 is in i11 and green; i1/w1 is blocked by i10/w30.
  - `work run` ends with such a work-item untouched. That contradicts r1 (pull until no work-item can make a transition); r63 forbids a worker only *while* the blocker is not green.
  - The implementer named this open case ("counts as not green, never moved") and it was not resolved.
- **Reproduction** (probe test_probe_blocked.py): i1/w2 is drafted with `blocked_by: [work-item/w9]`, and i2/w9 is green. `Pool.blocked("w2", {"w2": "drafted"})` → `True`.
- **Fix**: build the statuses from `workqueue.items(self.root)` across every initiative, keyed by name, and add an r63 example with a green blocker in another initiative.

### F2. Minor, w113, fix now (cheap): ruff I001

- **Where**: tests/scenarios/work_queue_answer_steps.py:2.
- **What is wrong**: the import block followed by the new `BREAKS` table fails ruff at the pinned 0.17.0, so `tools check` exits 1 on the branch.
- **Fix**: `ruff check --fix` on the file.

### F3. Minor, w109, observation: merge order can differ from end order (r61)

- **Where**: supervise_worker.py:167-175 and supervise_merge.py:102-106.
- **What is wrong**:
  - An implementer's place in `self.finished` is taken only once its thread acquires `self.lock`.
  - A merge holds `self.lock` for its whole test run. Two implementers that end during that wait on the lock, and Python's lock does not grant in arrival order, so their merge order can be swapped.
- **Why it matters**: the merge itself stays correct, since each branch is rebased; only r61's order is at stake.
- **Reproduction**: from reading only; it needs three implementers side by side and a merge running. I did not run it.
- **Fix**: append to `self.finished` under `self.turns` as soon as `self.session(...)` returns, before taking `self.lock`.

### F4. Important, w111 (withdrawn), observation: skill changes delivered outside `work run`

- **Where**: c8eb828 and 6559731 (skills/delivering-an-initiative/SKILL.md).
- **What is wrong**: these commits belong to no work-item's claimed→done window. w111 is withdrawn, and no green work-item accepts delivery#r17 or #r18.
- **What I checked**: the text meets r17 (step 5, Retires) and r18 (step 3, stop before any `work add`). The coordinator's review and the whole suite are recorded in w111.md.
- **Why it matters**: nothing in the queue records them as delivered, and no task reviewer read the change.
- **Fix**: a work-item accepting delivery#r17 and #r18 (guarantees, which r27 now exempts) reviewed by `work run`, or the person's acceptance recorded.

### F5. Minor, none, observation: commits that are no part of i23

- **What**:
  - The session-scope records b61404b, 8e5c540, 6d84ee6, 6d573c8, 81b7f37, df1bf0c and a1fffa7.
  - The design note "requests and the context loop", 749ed8a, f9a5ed2 and c29a521.
  - i22's split files, 1a7dc75.
- **Why it matters**: there is no code among them, but i23's measurement and review range now include another topic.
- **Fix**: commit such records on the branch of the work they belong to.

### F6. Minor, w115, observation: a unit test passes on contradictory output

- **Where**: tests/scripts/test_measure_runs.py:39-43.
- **What is wrong**:
  - The fixture gives `10-research` the session id s-1, while pairing by order maps it to s-3. The s-1 stage then has **14 turns and** `session_json: "empty"`.
  - The test asserts only the mark, and its name says "later run" while the empty one is the earlier (k=2).
- **Reproduction** (probe test_probe_misc.py): `{'session': 's-1', 'turns': 14, 'session_json': 'empty'}`.
- **Why it matters**: r57 gives a stage named as empty without its figures. Real `work run` data is consistent, so the test is what is wrong.
- **Fix**:
  - Give 10-research the session id s-3, and assert `"turns" not in first`.
  - Optionally, pair an empty run only with sessions that no other session.json of the stage claims.

### F7. Minor, none (predates the branch), observation: no randomized test that `model decisions --check` agrees with `model decisions`

Keep as a test (tests/scripts/test_model_decisions_agree.py). It tried 40 cases, all agreeing:

```python
import random
from test_model import ModelTest

WORDS = ["cart", "shelf", "price", "order", "a b", "x-y", "é", "q", "z"]

class DecisionsAgree(ModelTest):
    def decision(self, rng, n):
        name = "-".join(rng.sample(["cart", "shelf", "price", "order", "tax"], rng.randint(1, 3)))
        summary = " ".join(rng.choice(WORDS) for _ in range(rng.randint(1, 6)))
        self.write("spec/decisions/%04d-%s.md" % (n, name),
                   "---\nid: design-decision/missingmass.io/shop/%s-%d\nsummary: \"%s\"\ndate: 2026-%02d-%02d\n"
                   "status: %s\nby: someone\n---\n\n# %04d. %s\n" % (name, n, summary, rng.randint(1, 12),
                   rng.randint(1, 28), rng.choice(["accepted", "proposed", "superseded"]), n, name))

    def test_check_agrees_with_write(self):
        rng = random.Random(23)
        for case in range(40):
            with self.subTest(case=case):
                self.reset()
                for n in rng.sample(range(1, 60), rng.randint(0, 8)):
                    self.decision(rng, n)
                index = self.tmp / "spec/decisions/index.md"
                if rng.random() < 0.5:
                    index.parent.mkdir(parents=True, exist_ok=True)
                    index.write_text(rng.choice(["", "# hand written\n", "stale\n"]))
                before = index.read_text() if index.exists() else None
                checked = self.run_model("decisions", "--check")
                self.assertEqual(before, index.read_text() if index.exists() else None)   # --check writes nothing
                self.assertEqual(self.run_model("decisions").returncode, 0)
                self.assertEqual(checked.returncode, 0 if before == index.read_text() else 1)
                self.assertEqual(self.run_model("decisions", "--check").returncode, 0)
```

## Shape

I checked the CLAUDE.md rules and the module-map rows the branch touched:

- **Size limit**: met. Every touched file is ≤ 300 lines; design_model_check_problems.py is at 300 (w116; the next line pushes it over), analysis_tools_probe_steps.py at 284 and stub_claude.py at 258.
- **`scripts/supervise*.py`**: met.
  - The new supervise_pool.py (141 lines) has its row updated at CLAUDE.md:21 (4232bc6).
  - `Run` gains `Pool` (supervise.py:36), and `pair`, `together` and `claimed` moved out of supervise.py.
- **`scripts/measure` with `measure_*.py`**: met. Reading is in measure_read.py:22-87, figures in measure_build.py:32-63, and the contract in scripts/measure:31-33.
- **`scripts/tools` and `tools_env.py`**: met. The pin is tools_env.py:23 and :94, and the contract text is tools:25-27.
- **`scripts/model*.py`**: met. The changes are model_work.py:188-194 and model.lp:64 and :276; grammar.md:198 is kept alongside.
- **`scripts/workqueue_answer.py`**: met (:11-12, :27-28).
- **`scripts/migrate*.py`**: met (migrate_upgrade.py:36-46, :77).
- **`tests/scenarios/<capability>_*_steps.py`**: met. The new modules are supervision_parallel_steps.py and batch_measurement_reading_steps.py.
- **`tests/scripts/`**: met. test_measure_runs.py covers the pairing that no scenario drives with two runs.
- **Unreached code and steps**: vulture is clean, `features bindings` is clean, and the steps the retirements left unused were removed.

Observations on shape:

- supervise.py:53 `self.limit = 4` repeats `supervise_pool.WORKERS`. Drop: `read_delivery` always sets it.
- model_work.py:191 rebuilds a list of every fact for each accepted id. `self.caps.get(cap, {}).get("group") == "guarantees"` (model_facts.py:199 keeps the group) says the same. The check that shows the refactor complete: the r27 guarantees scenario passes.

## Coupling

- **Claude Code's transcript store**: supervise_worker.py:74-86 `with_transcript` and measure_read.py:109-123 rely on `$CLAUDE_CONFIG_DIR` (else `~/.claude`) and `projects/*/<session-id>.jsonl`.
  - This layout is internal to Claude Code, not published.
  - If it changes, `transcript_path` is silently left out (r62 is unmet without a word) and round trips become None.
  - Stable: take the path from what Claude Code publishes; hooks receive `transcript_path` as input, so a SessionEnd hook could write it into the stage directory.
- **`claude -p --output-format json`**: measure reads `session_id`, `usage.input_tokens`/`output_tokens`, `num_turns` and `total_cost_usd`. These are the SDK's documented result message, and measure refuses a session.json without them.
- **pytest-xdist**: scripts/work_items.py raises `SystemExit` in `pytest_collection_modifyitems`. Under `-n auto` this crashes with `INTERNALERROR … KeyError: <WorkerController gw0>` (recorded in w111.md).
  - That relies on behaviour xdist does not promise, and gives a crash where a refusal belongs (outside this branch's diff).
  - Stable: raise `pytest.UsageError` from the controller only.
- **PyPI**: `ruff==0.17.0` relies on that release staying on the index. It is installed here at that version.

## Observations

- **F3**: merge order under lock contention. From reading.
- **F6**: test_measure_runs fixture. Reproduction: `pytest -s -n 0 test_probe_misc.py` → `{'session': 's-1', 'turns': 14, 'session_json': 'empty'}`.
- **w113, line breaks outside r15**: an answer with U+001C/U+001D/U+001E is accepted (r15 does not name them), and `supervise.held` (supervise.py:170, `splitlines`) would split it into two bullets.
  - Reproduction: probe test_probe_breaks.py → `not refused ['0x1c', '0x1d', '0x1e']`.
  - Fix: `split("\n")` in `held`.
- **w108, whitespace-only plugin-version**: `" \n"` is said to be "empty" (migrate_upgrade.py:42).
  - Reproduction: `session_text` → `'Tell the person that .shop/plugin-version holds no version, and that it is empty.\n'`.
- **w108, multi-line plugin-version**: `"0.23.1\nfoo\n"` is quoted across two lines.
  - Reproduction: → `'… and that it holds "0.23.1\nfoo".\n'`.
- **w115, run count**: when a stage's run directories differ in number from its ended starts, no empty session.json is named (measure_build.py:62-63). Reproduction: from the implementer's report and the code.
- **w109, throughput**: `choose_locked` (supervise_pool.py:127-129) waits on `self.lock`, which a merge holds through its whole test run (supervise_merge.py:104), so no worker starts while a merge tests. Reproduction: from reading.
- **Deprecated scenarios from i21**: migration-tools @r15 and work-queue @r1 are still in features/, with their replacements' work-items (w86, w89, w90) withdrawn. Reproduction: `features deprecated`.
