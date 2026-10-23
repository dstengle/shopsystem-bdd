# Review of w94 (6-review): measure counts round trips

**Verdict: DONE.** This is the second review. The first review's only Critical finding was that the deprecated @r41
scenario was removed from `features/` while w94.md had no `## Retires` section. Commit 6c803dc has since added that
section, so the finding is resolved. The code commits have not changed since that review. The code does what r41,
r42 and r53-r56 ask, and all 20 batch-measurement scenarios pass. No finding is Critical and none is triaged fix now.
What remains is Minor.

## Commits reviewed

The branch `work/w94` is gone. The commits are taken from HEAD, between `cc3757f work: w94 ready -> claimed` and
`c52189f work: w94 claimed -> done`, leaving out w95's `work:` commits (db73865, f60cc79):

- cd39016 measure counts awaiting-answer transitions; retire the deprecated awaiting-ruling scenario (r41)
- 6212f6f measure gives each stage its session's round trips, and the totals turns and round trips (r42, r53, r55)
- a207018 show prints each stage's round trips beside its turns, and the turns and round trips totals when given (r54, r56)

The implementer's result lists 893d3a5, fe1f052 and da48c3c. Those commits have the same subjects.
`git diff da48c3c a207018 -- scripts tests features` is empty, and the stat of `893d3a5^..da48c3c` matches
`f60cc79..a207018` (10 files, +194/-55). So the landed commits are rebased copies with the same content. The third
subject is shortened in result.json, which is cosmetic.

After the merge, 6c803dc added the Retires section to w94.md (and a note to w95.md). `git log c52189f..HEAD` on the
ten fileset files is empty, so nothing has touched w94's code since.

## Removed and weakened tests

What I searched for: deleted step functions, dropped parametrize cases, removed or loosened asserts, added skip or
xfail, and rewritten steps. I read the whole diff of `tests/` and `features/` once.

1. **Deprecated @r41 scenario removed** ("... its awaiting-ruling and failed counts ... (deprecated)"). It proved
   that awaiting-ruling transitions are counted. Plan §4 lists it, and w94.md's `## Retires` now names it with the
   person's answer (reading A). **It holds.**
2. **`then_steps.gives_counts`** was renamed from awaiting-ruling to awaiting-answer. It now proves the awaiting-answer
   count, which the current r41 scenario uses. Plan §4 lists it.
3. **`then_steps.gives_totals`** now asserts the turns, round trips and token columns only when the table names
   them. The three token columns used to be asserted unconditionally, so this is a loosening. Plan §4 lists it.
   Today both totals tables in the feature (lines 119 and 135) name all three token columns, so no coverage is lost
   today (Finding 2).
4. **`given_steps.stages_sessions_took`** now reads the table by its header and takes 5 or 7 columns. It changes no
   assert. Plan §4 lists it.
5. **`show_steps.runs_show`** now runs `measure initiative` only when `world.has_log` is set. This is setup: it
   changes no assert. r44 still passes (in the 20 passed).

No skip or xfail was added, and no parametrize case was dropped.

## Allowances

| Row | Holds? |
|---|---|
| `gives_totals`, interim | **Does not hold as written.** The step predates the initiative's base (first committed in i12, as the 5-review found with `git log -S`). The change is still covered, because plan §4 lists it under "Tests the decisions break". Minor. |
| `stages_sessions_took`, setup | Holds. It adds, removes or changes no assert, expected value or parametrize case. |
| `gives_counts` renamed | Holds: plan §4 lists it. |

## Cannot verify

- The red-then-green sequence the report gives, and its suite count at the start.
- That a real Claude Code store has the layout D2 assumes (`<config>/projects/<dir>/<session>.jsonl`), and that a
  real stage's own rows carry `requestId` with no agentId/isSidechain. Only the test's synthetic store exercises
  this. I did not read `~/.claude`.
- That `features retire` was the tool used for the removal. The resulting diff is consistent with it.

## Findings

### 1. Minor: the report misstates `tools check` (observation, w94)
- **What is wrong:** `report.md`'s Completeness check says "`tools check`: nothing to check". Ruff actually reports
  lints on lines this work-item added: `scripts/measure_build.py:3` (I001, the extended import),
  `scripts/measure_read.py:104` and `tests/scenarios/batch_measurement_transcripts.py:23-24` (UP031). These match
  the `%` style of the code around them.
- **Fix:** report the check's real output.

### 2. Minor: the `gives_totals` token columns became conditional (observation, w94)
- **File:** `tests/scenarios/batch_measurement_then_steps.py:144-146`.
- **Why it matters:** a future totals table that leaves out a token column would pass silently. Plan §4 lists the
  rewrite.
- **Fix:** keep the three token columns unconditional and make only turns and round trips conditional. Correct the
  allowance row.

### 3. Minor: the totals give round trips 0 when no transcript was found (observation, w94)
- **File:** `scripts/measure_build.py:107`, and `scripts/measure_show.py:17-21`.
- **What happens:** `totals["round_trips"]` is always written, so `show` prints `round trips | 0` when no stage has a
  transcript, and the total is an undercount when only some stages have one. No line chooses this: r55 and r56 speak
  of stages, and r42 names round trips in the totals.
- **Reproduction:** from the code. Each stage without `round_trips` adds 0, and `totals_of` prints the row whenever
  the key is present.
- **Fix:** if wanted, write a line for this case through integrating-a-proposal.

### 4. Minor: the r42 s-9 Given ignores its "20 turns, 45 round trips" (drop, w94)
- **File:** `tests/scenarios/batch_measurement_given_steps.py:148-152`. The exclusion of s-9 from the totals is
  proved only through the slim session's tokens.

### 5. Minor: formatting nits (drop, w94)
- `then_steps.py:73`: a space is missing after a comma.
- `world.py:51`: a comment is misaligned.

No behaviour contradicts a Behaviour line or the Purpose. No code was found whose observable behaviour no line asks
for: the store lookup (r53, r55 and the Implementation note), the subagent exclusion (r53, "the session's
transcript"), the refusal on a store transcript of unknown shape (r47), and the contract text all serve their lines.

## Commands run

- `git log --format='%h %s' -25` and `git log --grep "^work: w94 ready -> claimed$"` → cc3757f. `work/w94` does not
  exist.
- `git log cc3757f..c52189f`, `git show --stat 6c803dc`, and `git log c52189f..HEAD -- <fileset>` (empty)
- `git log --no-walk 893d3a5 fe1f052 da48c3c`; `git diff --stat 893d3a5^ da48c3c` and `git diff --stat f60cc79 a207018`
  (both 10 files, +194/-55); `git diff da48c3c a207018 -- scripts tests features` (empty)
- `git diff f60cc79 a207018 -- features/` and `-- scripts tests` (read once)
- Grep "gives the totals" in the feature: both tables name the token columns.
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300` → nothing printed
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base cc3757f`:
  - ruff: 190 findings repo-wide, mostly the prevailing UP031; on w94's lines, Finding 1
  - vulture: clean
  - import-linter: the project states no import contracts
- `python3 -m pytest -q tests/scenarios/test_batch_measurement.py --whole-suite` → 20 passed
