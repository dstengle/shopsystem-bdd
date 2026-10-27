# Review of w206: fix the findings of branch review 2 of i39

**Verdict: DONE_WITH_CONCERNS.** The commit does what the plan says. Finding 2 and finding 3 of branch review 2 are fixed, and finding 1 is fixed as reading B. No change under `features/`, no test removed or weakened. One finding is Important and triaged fix now under the rule for code no line asks for. The redraft round now merges its ids into another held proposal (D-e), and no Behaviour line of supervision states that yet. The person's answer of 2026-10-27 chose this and puts the line in the follow-up internal request after i39. Nothing in w206's code needs to change. What is needed is that line, written through integrating-a-proposal.

## Commits reviewed

- Claim commit: `694a5f8e` (`work: w206 ready -> claimed`). The branch `work/w206` is gone, so the range is `694a5f8e..85589330` (`work: w206 claimed -> done`), less `work run`'s own `work:` commits.
- One commit: `e4e61321` "Fix branch review 2 findings: list --json drops turn, malformed raised.jsonl refused, redraft merges into other proposals". It touches:
  - `scripts/supervise_change.py` +24/-3
  - `scripts/supervise_rounds.py` +1/-1
  - `scripts/workqueue_list.py` +8/-4
  - `tests/scripts/test_supervise_change.py` +25
  - `tests/scripts/test_workqueue_list.py` +33 (new)
- This matches the implementer's `result.json` (`commits: ["e4e61321 …"]`). Every file is in the work-item's fileset, and nothing under `features/` changed.

## Removed and weakened tests

None. I searched the diff of `tests/` for removed lines (`^-`), for `skip` or `xfail`, and for changed `assert` lines:
- `tests/scripts/test_supervise_change.py` gains only a helper `proposal` and one new test. The existing test and its helper `write` are unchanged. `write` still calls `write_proposals` without `own`, which the new optional parameter allows.
- `tests/scripts/test_workqueue_list.py` is new.

## Allowances

The report's `## Tests changed under an allowance` says "none". That holds: no existing test changed.

## Cannot verify

- The report's runs: red first (3 failed, 1 passed), then green (4 passed); `--work-item w206` 154 passed and 1 skipped; the supervision integrate/draft/proposal scenarios 84 passed and 1 xfailed. I did not rerun the suite, because `work run` ran it before it merged.
- The plan's §4 hands the implementer the check of `supervision_reintegrate_steps.py` and `supervision_integrate_steps.py`, which the researcher did not read. I could not see from the commit that they were checked, apart from the report's run of 84.
- The report path in `result.json` is `.shop/scratch/4-implement/report.md`. The report is in `.shop/work/i39/runs/w206/4-implement/report.md`, presumably where `work run` copied it. This is not a finding.

## Findings

### 1. Important, fix now (code no line asks for): another held proposal's lists merged, not replaced (w206)

- **Where:** `scripts/supervise_change.py:79-89` (`merge_lists`) and `:108-112` (the branch on `own`); the caller is `scripts/supervise_rounds.py:195`.
- **What is wrong:** an integrate round's change list can name a capability that another held capability-proposal argues. That proposal now keeps its own `adds`, `changes` and `removes`, and the round's ids it lacks are added after them. Its status stays as it was, and its drafts sentence is replaced. The narrator can see this in the proposal file. Supervision r142 and r148 cover only the proposal being drafted anew, and no Behaviour line asks for this. The person chose it as reading B in the answer of 2026-10-27, which also says "the supervision line stating it is carried in the follow-up internal request after i39".
- **Why it matters:** behaviour reaches code only through a line. Until the line exists, no scenario pins the merge, and a later change could bring back the overwrite that branch review 2 found.
- **Fix:** write the supervision line (with its scenario) through integrating-a-proposal, in the follow-up internal request the answer names. The code does not change. The person only needs to confirm that the follow-up request carries the line.

### 2. Minor, observation: `merge_lists` drops the round's ids for a field the held proposal's frontmatter lacks (w206)

- **Where:** `scripts/supervise_change.py:88`. `re.sub(r"(?m)^%s:.*$" % field, …, count=1)` rewrites only a line that is already there. If there is no `changes:` line, the merged list is written nowhere, and nothing reports it. The pattern also searches the whole file, not only the frontmatter, so a body line starting `adds:` could be rewritten instead.
- `rewrite_lists` does not have this problem: it removes the three fields and writes all three. The fix is to rebuild the frontmatter the same way, or to share `rewrite_lists`' head/tail splitting.
- **Reproduction:** `grep -L "^changes:" .shop/work/*/*.md` lists `.shop/work/i1-first-spec/spec-integration.md`, a capability-proposal with `adds:` but no `changes:` or `removes:` (`grep -n "^adds:\|^removes:\|^changes:" …` shows only line 8, `adds:`). Every proposal of i39, the one open initiative with held proposals, has all three fields, and `write_proposals` always writes all three. So no client sends such a file today. I did not run a probe, because the shell allows no Python but pytest. This comes from reading the code against the grep.

### 3. Minor, drop: new ruff B023 at `scripts/supervise_change.py:88` (w206)

- `tools check` reports B023 for `field` and `mine` in the new `merge_lists` lambda. It is a false positive: `re.sub` calls the lambda within the same iteration.
- B023 at `:114` (`said`, before w206 at `:96`) and RUF100 at `tests/scripts/test_supervise_change.py:7` were there before w206; the commit did not add them.

### Verified, no finding

- **Risk: D-a changes a `work list` output that a line or a step reads.** `work list --json` now gives `{"request", "status"}` only. That is what r35 says ("each … with its status"). The turn is still in `work show`, through `listing`'s unchanged tuple (`n, s, _, _`).
- **Risk: D-b's refusal lets a malformed record slip through or crash.** It catches `ValueError`, `KeyError` and `TypeError`. That covers a line that is not JSON, a missing key, a JSON value that is not an object, and an unhashable key. It raises `workqueue.Refused`, imported at `workqueue_list.py:13`, so the command exits with an error under r7 and gives no traceback. `work list` writes nothing, so "change nothing" holds.
- **Risk: the round's own proposal is no longer told apart from the others.** `own` is `name`, the stem of the proposal the round was started for (`supervise_rounds.py:195`). It is the same key `proposal_for` returns as `held.stem`. In the initiative's first round, `name` is the initiative, so every held proposal is merged into, as D-e says.
- **Risk: the new `import workqueue` in `supervise_change.py` adds an import cycle or breaks a contract.** import-linter reports "the project states no import contracts". `supervise_rounds.py` already uses `workqueue.frontmatter`.
- **Size:** `tools size --limit 300` printed nothing, so no file is over the limit.

## Commands run

- `git log --format=%H -1 --grep="^work: w206 ready -> claimed$"` gave `694a5f8e…`. `git log … work/w206` failed: the branch is gone.
- `git log --format='%h %s' 694a5f8e..HEAD`; `git log --format=%H -1 --grep="^work: w206 claimed -> done$"` gave `85589330`.
- `git show --stat e4e61321`; `git show e4e61321 -- scripts tests`
- `git show HEAD:scripts/supervise_change.py`; `git show HEAD:scripts/supervise_rounds.py` (lines 170-200)
- `grep -n "def frontmatter" scripts/workqueue.py`, `grep -rn "^def frontmatter" scripts/*.py`, `grep -n Refused scripts/workqueue_list.py`
- `grep -n "r7\b\|r35\b\|r39\b…" spec/capabilities/work-queue.md`; `grep -n "r148\|r142\|r114" spec/capabilities/supervision.md`
- `python3 <Scripts>/tools check --base 694a5f8e…`: ruff gave 4 (B023 ×2 new at :88, B023 at :114 and RUF100 from before); vulture clean; import-linter: no contracts stated.
- `python3 <Scripts>/tools size --limit 300`: nothing printed.
- `grep -L "^changes:" .shop/work/*/*.md`; `grep -n "^adds:\|^removes:\|^changes:\|^kind:\|^status:" …`
