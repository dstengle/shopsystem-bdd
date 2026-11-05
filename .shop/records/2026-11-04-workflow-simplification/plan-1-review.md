# Plan 1 of the workflow simplification: end-of-branch review

Reviewer: the one fresh end-of-branch reviewer. Range: `c46cce36..6d24906a`, 10 commits, branch `workflow-simplification`. Date: 2026-11-04. The reviewer changed nothing in the repository. The implementer's report is `plan-1-implementation.md`.

## Verdict

The branch can be pushed as a draft PR, but it isn't ready to merge yet. The mechanics are sound: every baseline holds, and every figure in the report reproduces exactly. `spec_unbuilt` is small, correct and tested. It marks only the listed ids of their own capability, and its xfail is non-strict.

The requirement lines are another matter. Several don't say what the design means, or their generated scenarios don't test their point:
- the batches g7 gap is one case of a wider class;
- two lines are logically wrong: `batches#r10` and `decision-tiers#r6`;
- the design's traceability chain (goal 1) and parts of the backlog view (goal 2) have no line at all.

These lines become the acceptance tests for plans 2-9. Once they are on `main`, "retire, never edit" makes every fix a retirement plus a new id, so the fixes should land on this branch before the merge. All of them are spec-only, and the ones proposed below parse in the grammar as it stands.

## Verification

| Check | Report | Got |
|---|---|---|
| `python3 -m pytest -q` | 946 passed, 1 skipped, 49 xfailed, 129 subtests | 946 passed, 1 skipped, 49 xfailed, 129 subtests passed (16.9 s) |
| `model check` | 53 violations, 16 warnings, 19 unresolved, 0 file problems | same |
| `model logic` | `11 findings: 6 L5, 5 L6`, none on a new capability | same; all 11 are on old capabilities or U-conditions |
| `model lexicon --check` | 398 terms, 0 problems | same |
| `features generate --check` | passes | exit 0; the diff from `c46cce36` only adds 7 features, so every existing feature is unchanged |
| `features vocab --check` | every step has one handler | same |
| `features bindings --unbound` | exit 0 | "every binding names a scenario", exit 0 |
| `tools size --limit 300` | silent | silent, exit 0 (`work_items.py` 248 lines, `features` 222, `spec_unbuilt.py` 68) |
| `tools check` | — | nothing to report |
| Task 11 count | 60 across 9 capabilities, `problems` empty | same; `grep -c '^- \[r'` gives 15+4+6+10+8+3+6+4+4 = 60 |
| `git status` after the runs | — | clean apart from the untracked report. The parse cache is written under `~/.cache`, outside the repository. |

## Findings an implementer can fix

### Should fix

**S1. `batches#r7`'s scenario doesn't test its point** (`spec/capabilities/batches.md:55`, `features/batches.feature:56`). The generator drops the "with no commit of the item" object. The scenario then asserts only that a pull request of the batch is published, which `r8` already asserts.

Fix: reword the line as follows. It parses, with `ShallNot … rel_commit_of_item`:
`While an item in a batch is \`needs-input\`, when the person runs \`work batch review\` on the batch, \`work\` shall publish a pull request of the batch, and \`work\` shall not publish a commit of the item.`

**S2. The generator dropping a precondition or object is a class of gap, not one case.** It needs to be in the record.
- `intake#r6` (`intake.md:49`, `features/intake.feature:50`): "every request line of the item is settled" is dropped. The scenario is word for word `readiness#r1`'s apart from the actor, so it tests nothing new.
- `batches#r8` (`batches.feature:66`): "every task of the batch is `done`" gives no Given.

Fix: list both beside g7 in the open problems. Then remove the generator gap, or reword the lines so their point is a positive or negative Then.

**S3. `intake#r6` adds nothing, and the rule it means is missing.** `readiness#r1` already readies any `shaped`, passing item. So an item with an unsettled request line is readied anyway, because `passing` (`spec/index.md:272`) doesn't include settledness.

The fix is one of these, and it touches the readiness bar, so the person may want to choose:
- (a) add "every request line of the item is settled" to `passing`'s definition;
- (b) replace `r6` with the refusal, which parses: `While an item is \`shaped\` and a request line of the item is not settled, if a session runs \`work ready\` on the item, then \`work\` shall exit with an error naming the request line and change nothing.`

Option (b) may give an L1 against `readiness#r1`. That would be the true conflict showing itself, and option (a) settles it.

**S4. `batches#r10` sets a parked item to `ready`, which isn't a transition** (`batches.md:67`). "every item in the batch" includes a `needs-input` item, and the glossary (`spec/index.md:262`) has no `needs-input` → `ready`. `model logic` doesn't catch it.

Fix: `… set the status of every item in the batch that is \`in-batch\` to \`ready\`.` This parses.

**S5. No line sets a batch `merged`.** The glossary has `awaiting-merge` → `merged`, and `telemetry#r1` depends on a `merged` batch, but `batches#r9` (`batches.md:63`) sets only the items.

Fix: `… shall set the status of the item to \`delivered\` and set the status of the batch to \`merged\`.` This parses.

**S6. `decision-tiers#r6` would flag a proposed supersession** (`decision-tiers.md:53`). As written, it fires whenever any decision supersedes an `accepted` one. Today 0073 (`proposed`) supersedes 0033 (`accepted`), so the rule would report a violation for a supersession that hasn't been accepted.

Fix: `While a design-decision that is \`accepted\` supersedes a design-decision that is \`accepted\`, …`

**S7. `pr-review#r3` contradicts the design's re-review** (`pr-review.md:42`, `:55`). `r3` makes every review read every commit of the batch. `r6` adds the fix's commits but never says "only". The design (goal 6, and the session's calls) says the re-review reads only what the fix touched.

Fix: restrict `r3` to the first review, for example "While no review of the pull request is written …". Or add a `shall not read` to `r6` for commits that aren't for the finding.

**S8. `backlog#r7` adds nothing beyond `r6`** (`backlog.md:58`, `features/backlog.feature:54`). The scenario asserts only `prints the item i2`. `r6` already prints every item, so this proves nothing about "marks a blocked item". The `i1` half of "print the item and …" is lost as well.

Fix: tie the blocker to the item, for example print "the item … and every item the item is depending on that is not `delivered`" in the blocked item's row. If that can't be said in the grammar, move the group to `## Not yet`.

**S9. `spec_unbuilt.problems()` has no caller** (`scripts/spec_unbuilt.py:35`). The report says so too. A mistyped id marks nothing, as Review Focus 3 asks, but nothing tells anyone about it.

Fix: the cheapest option is a test in `tests/scripts/test_spec_unbuilt.py` asserting `spec_unbuilt.problems(REPO) == []` on the repository itself, so the suite fails on a typo. The fuller option is a `model check` violation.

**S10. The report wrongly explains the drop in unresolved references from 29 to 19** (report, "Final state"). Running `model check` on `c46cce36` and diffing the output shows that all 10 lines that went away are in `.shop/work/i57/`, i57's withdrawn board-era proposals:
- `backlog.md` adds `backlog#r1`–`r8`, which now "resolve" against the new and unrelated `backlog` capability;
- `glossary.md` adds `term/…/backlog`;
- one "names nothing" line.

So the new terms didn't resolve references in existing files. It's an id collision that now points frozen history at the wrong lines.

Fix: correct the report. Then decide, probably in the migration plan, whether frozen `.shop/work/` references are excluded from resolution.

### Minor

- **M1.** A dependency is said two ways: the glossary's relation `item | depending on | item` (`index.md:313`) and backlog's `dependency` kind with `of`/`on` rows. `r5` uses one form and `r7` the other. Pick one. The `blocked` prose also says "depends on".
- **M2.** `batches#r1` says every ready, passing, unblocked item is picked. The prose cap (`batch_size`, default 4) contradicts that once more than four items qualify. Say "an item", or note the cap in the line's group title.
- **M3.** Some lines are weak or hard to test:
  - `telemetry#r4` checks only that the two names are printed;
  - `conversation#r2` has the flags `--session --transcript` with no values;
  - `readiness#r4`, `batches#r5` and `intake#r5` say "does not ask the question q1".

  These are acceptable for now, but record them.
- **M4.** The nine `grammar/corpus/<cap>.txt` files are written in the fixture vocabulary (`work-item`, `initiative`), as `test_spec_grammar` requires. So they exercise none of the new terms.
- **M5.** Test gaps: no test that `mark` leaves alone an id of the same number in another capability, and no direct test that `cmd_vocab` uses `unbuilt_lines`. Today only `test_bound`, through the real features, covers that.
- **M6.** `unbuilt:` on a capability that isn't codified is ignored silently, even by `problems()` (`spec_unbuilt.py:17`).
- **M7.** Scenario names: the batch plan is `b2` next to the batch `b1`, while items are named `b<n>` in the glossary. This is generator naming, but it's confusing to read.
- **M8.** Records:
  - the report was untracked, and the memory rule says records are committed and indexed (since committed with this review);
  - the ledger names the final commit as `6b3904fb`, but HEAD is `6d24906a`;
  - the tests being pytest functions rather than `unittest` is a deviation the report doesn't list. It's harmless.

## Findings that need the person's decision

- **P1. The traceability chain has no line.** Design goal 1 says an item's batch, PR and commits name the item, and the person asked for this explicitly. No requirement says the PR or the commits name their items. Should a `batches` line be added, for example "publish a pull request that names every item in the batch"?
- **P2. Parts of the backlog view are missing** (goal 2):
  - tables by state;
  - rank order and the WSJF score;
  - "how far the batch is along" for an item in a batch;
  - the question on a `needs-input` row (goal 3).

  None of these is a line. Rank order is prose in batches only. Should plan 1 say them, or plan 2?
- **P3. `needs-input` → `shaped` (`work answer`) is in the glossary but in no requirement.** A park doesn't record its question either. Review Focus 2's `work answer` therefore has nothing to check.
- **P4. Bugs' risk and likelihood ratings (goal 2) aren't in the lexicon**, and the roadmap doesn't mention them.
- **P5. The tier-1 decision checks are left out of the readiness bar.** The design's bar includes "the tier-1 decision checks … hold", but `passing` leaves that clause out, and so did the plan. Is the exclusion intended, perhaps until plan 6?
- **P6. Should the xfail be strict?** Non-strict (as the plan asked) shows a scenario that starts passing as XPASS, but the suite stays green, so nobody is made to act on it. Worse, a built scenario left in `unbuilt:` has its later failures hidden for good, and `features vocab --check` stops asking for its handlers. All 49 fail today for want of handlers, so `strict=True` is safe now and would force each id out of `unbuilt:` the moment it's built. Recommendation: strict, or a check that fails on XPASS.
- **P7. The rating values leak into the CLI contract.** `backlog#r4` makes the CLI `--value high-value --urgency low-urgency --size small`. Accept this, or keep the CLI's `high`/`low` and not name the flag spelling in the line?
- **P8. `intake#r1` loses who asked.** It drops "whose upstream is this bounded context", and "asked by a bounded context" doesn't tie the item to the request's asker. Accept until the grammar can say it, or move it to `## Not yet`?
- **P9. New lines lean on old-process terms that will retire with their capabilities:**
  - `fix now` is a value of review.md's `triage`;
  - `measurement` is defined as "for one initiative's deliveries", which conflicts with "measurement of batch";
  - `defect` is code-research's;
  - `failing` is analysis-tools'.

  Lift and redefine them in the glossary before those capabilities are retired.
- **P10. May unmerged lines be fixed in place?** S1–S8 change lines on this branch that have never been on `main`. The reviewer's view is that "retire, never edit" starts at the merge, but the person should confirm.
- **P11. Inverse relation rows.** `item proposes requirement` (glossary) and `requirement proposed by item` (pr-review) are two rows for one fact. Accept that, or teach the grammar the passive?

## The 11 deviations

1. **Rating values renamed.** Justified: the lexicon refuses one value in two attributes of one kind. It keeps the WSJF intent, since the L/M/H order is kept. Its cost to the CLI is question P7.
2. **`origin` → `provenance`.** Justified: the collision is real, and it caused `v_p2` in `requests#r6-r8`. The intent is kept, though the person now reads a different word.
3. **`depends on` → `depending on`.** Justified as a grammar limitation. It leaves two forms of dependency (M1).
4. **`features vocab --check` exempts unbuilt scenarios.** Justified, and the scope is right: only the lines from an unbuilt id's tag line to the next scenario, and the steps are still parsed. Not too broad for plan 1. Combined with the non-strict xfail it can hide a built scenario (P6).
5. **A corpus file per capability.** Justified: the test requires one. They don't exercise the new terms (M4).
6. **Group splits.** Justified by `v15l` and `v15n`. The meaning is kept.
7. **Terms added to capabilities.** Justified. Defining `untested` and `unrequired` in the controlled language is good. They rely on the old-process terms in P9.
8. **The transition `in-batch` → `ready`.** Justified, but `batches#r10` then also covers `needs-input` items (S4).
9. **`clean` defined in the controlled language.** Justified. The meaning is the same and `model logic` gains from it. It depends on review.md's `fix now` (P9).
10. **Wording the grammar can't take literally.** Mostly justified:
    - readiness's "the reason": acceptable;
    - brainstorming's "use `work ready`": acceptable;
    - intake loses the asker (P8);
    - telemetry's `compare` line is weaker than the plan's (M3).
11. **Progress lines in the plan.** Fine.

## The 4 open problems

1. **batches g7.** Confirmed. It's one case of a class that also hits `intake#r6`, `batches#r8` and `backlog#r7` (S1, S2, S8). A rewording that parses is given in S1.
2. **`problems()` has no caller.** Confirmed: should fix (S9).
3. **Glossary questions.** Keeping `blocked` in prose is acceptable: there's no L6 today. The inverse rows are P11. The P9 questions are added.
4. **Scenarios that use an item they never set up.** Confirmed in backlog g4, g5, g6 and g15, readiness g4 and conversation g4. Existing features (work-queue, requests, supervision) do the same, so it's a property of the generator that a handler has to absorb, not a defect of this branch. Minor; record it for plan 2's handlers.
