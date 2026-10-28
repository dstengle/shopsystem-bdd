# Review of w225

**Verdict: DONE_WITH_CONCERNS.** There is one finding to fix now (Important). The routing in these commits sends a glossary-proposal into r117's approval question, which r117 asks only for a capability-proposal. Nothing changed under `features/`. No test was removed or weakened. The suite is green (1068 passed at 52207c77, per the suite record).

## Commits reviewed
- 0f01102e `work run: route a glossary-proposal through gate, apply and approved (r164 r165 r166 r167 r169 r170)`
- 52207c77 `work run: an initiative that changes only the glossary is set done (r161)`

Parent of 0f01102e: d5abde5f `work: w225 ready -> claimed`. Both implement results list 9ebc483f and 58c712f0. `git diff 9ebc483f 0f01102e --stat` shows differences only under `.shop/` (the merge rebased the commits), so the code is the same. The 4-implement session made no commit; the 3-implement session made both.

## Removed and weakened tests
None.

What I searched for: in the diff of `tests/`, deleted `def`s, dropped parametrize cases, removed or changed `assert`s, added skip/xfail, and changed regexes of Then steps.

Each changed step, compared before and after:
- `supervision_rounds_steps.py` `gate_started`
  - Before: `len(rounds(repo, "gate")) == 1`.
  - After: `len(rounds(repo, kind, name)) == 1`.
  - `rounds()` defaults to `name="p1"` (l.150), so before it also counted only p1's gate rounds. A p1 scenario proves the same thing. The step now also serves "apply … for g1".
- `apply_started`, `approved_after_apply` and `position`: the same check, with p1 now a parameter (default `p1`). No assertion was loosened.
- `supervision_formulate_steps.py` `proposal_awaiting`, `supervision_proposal_steps.py` `round_given_drafts` and `written_from_round`, `supervision_reintegrate_steps.py` `no_formulate_for_p1`: `p1` became `[pg]1`, with the same assertion.
- `glossary_proposal_answered`: only a Given's regex was widened (", given by its gate round" made optional). It asserts nothing.

## Allowances
The 3-implement report's `## Tests changed under an allowance` says "none (existing steps widened … no assertion changed)". That holds, as verified above. The 4-implement report says it did not verify this; this review did.

## Cannot verify
- That the accepted scenarios were red before the commits. The research notes and the 3-implement report say they were (8 failed on missing steps, then `AssertionError: ([], '', '')`). No run of mine shows it.
- r167 was vacuous before the routing. It is accepted as covered by r166's routing, per the person's delegated answer of 2026-10-28.

## Findings

### 1. Important, fix now: r117's approval question is written on a glossary-proposal, and no line asks for that
- **Where:** `scripts/supervise_rounds.py:159-161` (unchanged code). The commits' routing, `supervise_rounds.py:58-61` and `supervise_glossary.route` (`supervise_glossary.py:27-32`), now reaches it.
- **What is wrong:** a gate round for g1 that gives no question now writes "Are the lines of g1 approved as drafted? …" under g1's `## Questions`. That is an observable output. r117 names only "a round of the kind `gate` … for a capability-proposal", and the question talks about "lines" where a glossary-proposal has terms.
- **The other half:** `supervise_glossary.route` refuses an apply round to an awaiting-answer glossary-proposal with no question (`questions and …`). Read literally, r165 holds when there is no question at all, and r70 says so for capability-proposals.
- **Taken together:** what happens to a glossary-proposal whose gate gives no question is decided by code, not by a line. The plan (§5) and the 3-implement report ("Open questions") both name this case as unspecified.
- **Why it matters:** behaviour reaches code only through a line. The person sees a question that no supervision line says will be asked.
- **Fix:** write the line first, through integrating-a-proposal. Either widen r117 to a glossary-proposal (with wording about terms), or add a line saying the no-question gate goes straight to apply. Then make the code match. Otherwise, limit r117's branch to `kind: capability-proposal`.
- **Reproduction (code read):** in `run_round`, `if kind == "gate" and not asked:` does not check the proposal's kind. The 3-implement report confirms: "g1 is asked the approval question as p1 is, since the shared code does that; unspecified for g1."

### 2. Minor, observation: the glossary-only done ignores raised requests that are not delivered
- **Where:** `scripts/supervise_done.py:28-37` (`set_glossary_done`) and `scripts/supervise_glossary.py:62-76`.
- **What:** r105's last clause (every request this context raised that names the initiative is `delivered`) is not checked. `workqueue_done.holds` is deliberately skipped.
- **Why it matters:** r161 says nothing about requests, so this follows r161 as written. Still, a glossary-only initiative that raised a request could be set `done` before the request is delivered.
- **Reproduction:** a code read. `set_glossary_done` calls only `glossary_only_done`, which reads the proposals and `spec/index.md`. The plan's §5 names the case.

### 3. Minor, observation: an abandoned initiative can be set done
- **Where:** `scripts/supervise_done.py:31-32`.
- **What:** the guard is only `before == "done"`. An `abandoned` initiative given by name to `work run <initiative>`, with only approved glossary-proposals and its terms committed, would move `abandoned -> done`.
- **Note:** `set_done` has the same guard, but behind more conditions. No client does this today.
- **Reproduction:** a code read only. Nothing in `supervise*.py` excludes an abandoned initiative given by name (`grep -n abandoned scripts/supervise*.py`: only `supervise_all.py`).

### 4. Minor, observation: a new unused `noqa`
- **Where:** `tests/scenarios/supervision_proposal_steps.py:172`.
- **What:** `listed = lambda … # noqa: E731` is new in 0f01102e. Ruff reports RUF100 (E731 is not enabled). This is cheap polish: remove the `noqa`.

## Checks
`tools check --base 0f01102e~1`:
- **ruff:** 6 errors.
  - From these commits: only `supervision_proposal_steps.py:172` RUF100 (finding 4).
  - Already there: `workqueue.py:248` I001 (line not touched), `supervision_proposal_steps.py:102` and `:137` RUF100 (lines that existed before), `supervision_reintegrate_steps.py:13` F401 and `:174` FURB167 (not touched).
- **vulture:** clean.
- **import-linter:** the project states no import contracts.

`tools size --limit 300`: printed nothing. No file is over the limit.

## Commands run
- `git log --stat 0f01102e~1..52207c77`
- `git diff 0f01102e~1 52207c77`
- `git diff 9ebc483f 0f01102e --stat`
- `git log --format='%H %s' -1 0f01102e~1`
- `git show 52207c77:scripts/supervise_brief.py` (gate and apply brief), `git show 52207c77:scripts/supervise_rounds.py` (due, route, run_round), `git show 52207c77:scripts/supervise.py` (pull_through), `git show 52207c77:scripts/supervise_done.py`
- `grep -rn "def rounds" tests/scenarios/` (risk checked: whether widening `gate_started` and `apply_started` loosened them; it did not)
- `grep -n "r161|r16[4-9]|r170|r172|r105|r97|r117|r145" spec/capabilities/supervision.md`, `grep -n r55 spec/capabilities/spec-integration.md`
- `grep -n abandoned scripts/supervise*.py spec/capabilities/supervision.md`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools check --base 0f01102e~1`
- `python3 /home/vscode/shopsystem-bdd/scripts/tools size --limit 300`
