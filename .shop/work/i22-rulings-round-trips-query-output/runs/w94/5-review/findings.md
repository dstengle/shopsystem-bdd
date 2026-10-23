# Review of w94: measure counts round trips

**Verdict: DONE_WITH_CONCERNS.** The code does what r41, r42, r53-r56 ask, and all 20 batch-measurement scenarios
pass. There is one Critical finding, and it is bookkeeping: the commits retire a deprecated scenario in
`features/batch-measurement.feature`, but the work-item has no `## Retires` section listing it. The person's answer
of 2026-10-23 (reading A) orders exactly this retirement, so the change is right. What is missing is the work-item's
record of it. Everything else is Minor.

## Commits reviewed

The branch `work/w94` is gone, so the commits were taken from HEAD, between `cc3757f work: w94 ready -> claimed` and
`c52189f work: w94 claimed -> done`, leaving out w95's `work:` commits (db73865, f60cc79):

- cd39016 measure counts awaiting-answer transitions; retire the deprecated awaiting-ruling scenario (r41)
- 6212f6f measure gives each stage its session's round trips, and the totals turns and round trips (r42, r53, r55)
- a207018 show prints each stage's round trips beside its turns, and the turns and round trips totals when given (r54, r56)

The implementer's result lists 893d3a5, fe1f052 and da48c3c. Those commits exist and have the same subjects.
`git diff --stat` between each listed commit and its landed copy is empty under `scripts tests features`, so the
landed commits are rebased copies with the same content (w95's claim commits come between them). The third subject
is shortened in `result.json`, which is cosmetic. Files changed: the ten in the fileset, and no others.

## Removed and weakened tests

What I searched for: deleted `def`s, dropped parametrize cases, removed or loosened `assert`s, added skip or xfail,
and rewritten steps. I read the whole diff of `tests/` and `features/`.

1. **The deprecated r41 scenario was removed** ("each work-item is given with its transitions, its awaiting-ruling
   and failed counts ... (deprecated)"). It proved that a log's `awaiting-ruling` transitions are counted. Plan §4
   lists it, and the person's answer rules it. It is also a `features/` change (Finding 1).
2. **`then_steps.gives_counts`** was rewritten from `awaiting-ruling`/`awaiting_ruling` to
   `awaiting-answer`/`awaiting_answer`. Before, it proved the awaiting-ruling count. Now it proves the awaiting-answer
   count, which the current r41 scenario uses. Plan §4 lists it.
3. **`then_steps.gives_totals`** changed in two ways. It now asserts turns and round trips when the table names
   them. It also now asserts output, new input and cache-read tokens **only if the table names them**. Before, those
   three were always asserted, and a table without them failed with a KeyError. So it is loosened for those three
   columns: it now passes on a table that omits them. Plan §4 lists it ("rewritten to assert each column its table
   names"). See Finding 3 for the allowance row.
4. **`given_steps.stages_sessions_took`** now reads columns by header and takes the 5- or 7-column table. It changes
   no assert. Plan §4 lists it.
5. **`show_steps.runs_show`** now runs `measure initiative` only when `world.has_log` is set. The r44 Given
   (`measure_wrote`) calls `world.stage` → `world.log`, which sets `has_log`, so r44 still runs the initiative. I
   checked this by running r44: it passed. The plan does not list this step, but it is setup: it touches no assert or
   expected value.

No skip or xfail was added, and no parametrize case was dropped.

## Allowances

| Row | Holds? |
|---|---|
| `gives_totals`, interim | **Does not hold as written.** `git log -S "def gives_totals"` shows it was first committed in 4eba334 (i12, 2026-10-22), before the initiative's base dc9ece7, so it is not this initiative's test. The change is still covered because plan §4 lists it under "Tests the decisions break". Finding 3. |
| `stages_sessions_took`, setup | Holds. The diff adds, removes or changes no `assert`, expected value or parametrize case. |
| `gives_counts` renamed (plan §4) | Holds: the plan lists it. |

## Cannot verify

- The red-then-green sequence the report gives (KeyErrors at the Thens), and "Suite at the start: 645 passed, 6
  failed". Neither leaves a trace in the commits.
- That a real Claude Code store has the layout D2 assumes (`<config>/projects/<project dir>/<session>.jsonl`). Also
  that a `claude -p` stage's own rows carry `requestId` and no `agentId`/`isSidechain` while subagent rows live
  elsewhere. Only the test's synthetic store exercises this. I did not read the user's `~/.claude`.
- That `features retire` was the tool used for the removal. The result (scenario removed, nothing else changed in
  the feature) is consistent with it. There was no per-scenario binding to remove: `test_batch_measurement.py` binds
  the whole file through `scenarios()`.

## Findings

### 1. Critical: a features/ change the work-item does not list under Retires (fix now)
- **File:** `features/batch-measurement.feature:83-105` (at f60cc79), commit cd39016, work-item w94.
- **What is wrong:** the deprecated @r41 scenario is removed, and `.shop/work/i22-rulings-round-trips-query-output/w94.md`
  has no `## Retires` section listing it.
- **Why it matters:** the rule allows a `features/` change only for a deprecated scenario the work-item lists under
  Retires. Here the authority sits only in the `## Answers` text. The person's answer ("w94 retires the deprecated
  r41 scenario (a Retires section)") does order this retirement, and the plan's D1 flagged that the coordinator
  should record it. The removal is the right change; the work-item's record lags it.
- **Fix:** the coordinator adds to w94.md a `## Retires` section naming "each work-item is given with its
  transitions, its awaiting-ruling and failed counts and the commits its merge brought in (deprecated)" (@r41). No
  code change is needed. Reverting the removal would contradict the answer.

### 2. Minor: the report's completeness check misstates `tools check` (observation)
- **File:** `runs/w94/4-implement/report.md`, "Completeness check": "`tools check`: nothing to check".
- **What is wrong:** `tools check --base cc3757f` reports 47 ruff findings on the touched files. Most are the
  repository's prevailing `%` style (UP031) on older lines. Lines this work-item added are among them:
  `scripts/measure_build.py:7` (I001, the extended import), `scripts/measure_read.py:104`,
  `tests/scenarios/batch_measurement_transcripts.py:23-24` and `tests/scenarios/batch_measurement_world.py:99`
  (UP031).
- **Why it matters:** the report claims a clean check that was not clean. The lints themselves match the code
  around them.
- **Fix:** report the check's real output. Optionally wrap the import at measure_build.py:7.

### 3. Minor: the allowance row for `gives_totals` claims "interim", which does not hold (observation)
- **File:** `tests/scenarios/batch_measurement_then_steps.py:139-148`.
- **What is wrong:** the step predates the initiative (4eba334, i12). It is also loosened: output, new input and
  cache-read tokens are now asserted only `if column in wanted`.
- **Why it matters:** a future totals table that drops one of those columns would pass silently. The plan does list
  the rewrite, so this is not an unlisted weakening.
- **Fix:** keep the three token columns unconditional and make only turns and round trips conditional. Correct the
  allowance row to cite plan §4.

### 4. Minor: the totals give round trips 0 when no stage's transcript was found (observation)
- **File:** `scripts/measure_build.py:106-107`, and `scripts/measure_show.py:17-21` (`totals_of`).
- **What is wrong:** `totals["round_trips"] = sum(s.get("round_trips", 0) ...)` is always written. A measurement
  where no transcript was found therefore gives "round trips 0" in its totals, and `show` and `compare` print it,
  instead of leaving it out as r55 does for a stage. When only some stages have transcripts, the total is a silent
  undercount.
- **Reproduction:** from the code (I wrote no probe store). Every stage without `round_trips` adds 0, and `totals_of`
  prints the row whenever the key is present, so `show` prints `round trips | 0`. The plan's open case named this,
  and the report answers "0 is written". No line chooses either answer (r42 names round trips in the totals; r55 and
  r56 speak of stages).
- **Fix:** if wanted, a line for the totals when stages lack round trips, through integrating-a-proposal.

### 5. Minor: the r42 Given ignores its "20 turns, 45 round trips" (drop)
- **File:** `tests/scenarios/batch_measurement_given_steps.py:148-152`.
- **What is wrong:** `transcript_inside_with_trips` drops the turns and round trips. The scenario's claim that the
  s-9 figures stay out of the totals is proved only through the slim session's rows, not through 45 requests.
- **Fix:** write s-9 with 45 distinct request ids so that the exclusion is tested.

### 6. Minor: formatting nit (drop)
- **File:** `tests/scenarios/batch_measurement_then_steps.py:73`: `"round_trips","output tokens"` is missing a space
  after the comma.

No behaviour contradicts a Behaviour line or the Purpose. No code was found whose observable behaviour no line asks
for: the store lookup, the subagent exclusion and the refusal on a store transcript of unknown shape serve r53, r55
and r47 (plan D2-D4). The contract text in `scripts/measure` matches.

## Commands run

- `git log --format='%H %s' -12`. The `work/w94` branch is unknown; HEAD history used instead.
- `git show --stat 893d3a5 fe1f052 da48c3c`; `git diff --stat <listed> <landed> -- scripts tests features` (all empty)
- `git diff f60cc79 a207018 -- scripts tests features` (the change, read once)
- `python3 -m pytest -q -rA tests/scenarios/test_batch_measurement.py --whole-suite` → 20 passed. Without
  `--whole-suite` the session's filter collects the 7 scenarios w94 accepts, and those 7 passed.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base cc3757f`:
  - ruff: 47 findings (Finding 2)
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` → nothing printed. The largest touched file is
  given_steps at 213 lines.
- `git log -S "def gives_totals"` and `git log -S "def stages_sessions_took"` → 4eba334 (i12)
- `git blame -s` on the ruff-flagged lines
- Greps: the `has_log` uses, the other tests reaching measure (none outside the batch_measurement world)
