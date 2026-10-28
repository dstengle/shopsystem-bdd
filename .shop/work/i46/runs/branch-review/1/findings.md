# Branch review of i46

**Verdict: DONE_WITH_CONCERNS.** One Important finding is triaged fix now (finding 1). The branch delivers r54 before supervision r158 and r164. Under r54 a real integrate round now puts its terms in a glossary entry. `work run` reads that entry and writes it into no proposal, so the gate round is told to ask about no term. Nothing is Critical. Every check has a run in the brief, so nothing is under Cannot verify.

## Range and work-items

- Range: `134745663c..1f6680407a` (Base is the commit that added i46's `initiative.md`; Head is `w219 done -> green`).
- Work-items: **w219** (spec-integration r54, r55; green). Its commits are 942384ff, b4d3632e, e3c56f80, 07da6b11, a732bf6e, 085527d8 (r54), 55bed875 (r55), ae62d73d and 1f668040.
- 18 commits belong to no work-item: abb7bdd9, a2a554c4, 92e82b4e, 15c2f748, a0295498, 0d951852, 883b574c, a7147684, 48d1d0cb, 7ef2d04f, 4580cd45, edf0301e, c325cfe5, 441c5954, ef695630. They are the initiative's spec apply commit, its formulate rounds and merge, its work notes and transitions, and `work request: q32` (see finding 5).

## Suite

- `Suite: 1036 passed, 0 failed at 1f668040 in 33.74 s`. The full line: 1036 passed, 1 skipped, 36 xfailed, 8 xpassed, 624 warnings, 56 subtests passed. Command: `pytest -q -n auto ... --whole-suite`, exit 0.
- It runs in parallel (`-n auto`, xdist).
- It is not in-process. The step definitions drive the entry point through `subprocess.run([sys.executable, .../scripts/work, ...])` (tests/scenarios/test_supervision.py:79). The suite is under 60 s, so this is no finding.
- Dry-run versus real mode: the system has no dry-run mode of its own operations. The only `--dry-run` in scripts/ is a `git push --dry-run` probe (supervise_review.py:55, supervise_faults.py:71). No randomized agreement test is owed.

## Checks

All at 1f668040.

- **w219's scenarios** (`pytest -q -n auto -p work_items --work-item w219`): exit 0, 182 passed, 1 skipped, 56 subtests passed, in 6.95 s. w219 names scenarios and no check command.
- **`tools check --base 134745663c`**: exit 1.
  - **ruff:** 10 errors.
    - 7 are in the formulate rounds' committed helper scripts: `.shop/work/i46/runs/design-model-check/1-formulate/splice.py:3,4,8` (SIM115) and `.shop/work/i46/runs/supervision/1-formulate/splice.py:1` (I001) and `:2,15,23` (SIM115). See finding 4.
    - 3 are B023 in `scripts/supervise_change.py:90,90,117`. These lines were already there before the branch, and are false positives (see finding 6).
  - **vulture:** clean.
  - **import-linter:** the project states no import contracts.
- **`tools size`**: exit 0 and printed nothing. No file is over 300 lines, whether the branch touched it or not.
- **`features deprecated`**: exit 0. It lists 21 deprecated scenarios. Of the branch's:
  - the five r27 scenarios are for r124;
  - two r77 scenarios: one for r163, one for removal;
  - two r92 scenarios: one for r159, one for removal;
  - one r104 scenario, for r168.

  The rest come from earlier initiatives.
- **`features bindings`**: exit 0, "every binding names a scenario".

## Removed and weakened tests

None.

What I searched for: in the brief's change, every `-` line under `tests/` and `features/`, looking for deleted test functions, dropped Examples rows or parametrize cases, removed or loosened asserts, and added skip or xfail. I also compared each rewritten step against what it proved.

- **`tests/`**: only `tests/scenarios/spec_integration_steps.py` and `tests/scenarios/spec_integration_apply_steps.py` changed (w219, 085527d8 and 55bed875). Both only gained lines. One step was split: `answered_proposal` (spec_integration_apply_steps.py:20-32) now calls `answered_proposal_in`, which writes the same file and makes the same commit, so the step still proves the same thing.
- **`features/`**: the formulate rounds a0295498 and edf0301e changed existing scenarios only by adding `@deprecated`, ` (deprecated)` and a `Deprecated for:` line. The scenarios affected are r27 ×5, r77 ×2, r92 ×2 and r104 ×1. No step and no Examples row of theirs was removed, and they still run.

w219's plan, under "Tests the decisions break", says none, and that agrees with this.

## Allowances

w219's report, under `## Tests changed under an allowance`, says "none". The commits agree: no existing test's assert, expected value or case changed.

## Cannot verify

Nothing. Every check this review owes has a run in the brief, at 1f668040.

## Findings

### 1. Important, w219, fix now: a glossary entry's terms reach no proposal and are kept out of the gate's questions (scripts/supervise_change.py:102, scripts/supervise_brief.py:13-16, :79-82)

- **What is wrong:**
  - w219 changed the integrate brief's CHANGE_LIST. It now tells a real integrate round to put every term in one `{"glossary": true}` entry and in no capability's entry.
  - `work run` accepts that entry (`entries`, supervise_change.py:26-30), but `write_proposals` skips it (supervise_change.py:102). Nothing writes the glossary-proposal: supervision r158 is not built, and in i46 it is still a question.
  - The gate round's brief for a capability-proposal lists only that proposal's adds, changes and removes. It says "Ask questions only on the lines and terms listed above … and on no other line or term" (supervise_brief.py:79-82). So the terms are now excluded from the gate's questions by name.
  - At apply, `supervise_glossary.withheld` finds no glossary-proposal, so the apply brief withholds nothing (supervise_brief.py:86).
  - Before w219, terms rode in a capability entry under r92, the proposal listed them, and the gate asked about them.
- **Why it matters:** a term the round drafted either reaches `spec/index.md` without the gate having asked the person about it, or is silently left unapplied with no record on any part. That contradicts design-decision/the-glossary-is-a-target-of-spec-work (0073: terms "the gate approves before they are applied to spec/index.md") and design-decision/gate-on-behaviour-lines. Any integrate round that drafts a term reaches this; i45's round 1 drafted 5. The initiative branch is `main`.
- **Reproduction (by reading; a run would show it, not run):**
  - supervise_change.py:102 filters `e.get("glossary")` out of the proposals.
  - supervise_rounds.py:144-148 and :196 pass the list straight to `write_proposals`.
  - supervise_brief.py:79-82 restricts the gate to the proposal's lists.
  - The test that would show it: a supervision scenario in which the integrate round gives `{"capability": "thing", "adds": ["thing#r4"]}` and `{"glossary": true, "adds": ["term/ledger"]}`. Then, after `work run i1`, either a drafted glossary-proposal names `term/ledger` (r158), or some gate brief names `term/ledger`. **Not run.** Today neither holds.
- **Fix:** deliver supervision r158 and r164 (answer r158's question in i46 and formulate them) before another integrate round runs on `main` with a term change. Until then, either do not run integrate rounds that draft terms, or put the old wording (terms in the capability's entry) back in CHANGE_LIST through a line.

### 2. Important, w219, observation: r55's "not approved" is read as "status other than `approved`", which will withhold a glossary-proposal's own terms from its own apply round (scripts/supervise_glossary.py:15, scripts/supervise_brief.py:86)

- **What is wrong:** `withheld` holds back the terms of every glossary-proposal that is not `approved`, and every `apply` brief carries that line. But supervision r166 makes a glossary-proposal `approved` only after its apply round, and r165 starts that round once the person's answers are in.
- **Why it matters:** once r165 is built, the glossary-proposal's own apply round will be told to apply none of its own terms. That contradicts r165, r166 and 0073.
- **Reproduction:** read supervise_glossary.py:15 against supervision.md r165 and r166. Today nothing writes a glossary-proposal (r158), so this is not reached. The w219 review raised the same thing as its finding 1.
- **Fix:** in the work-item that builds r165, leave the round's own proposal out, and count a proposal whose gate questions are all answered as approved. Or settle the reading through integrating-a-proposal.

### 3. Minor, w219, observation: the glossary entry's form is barely checked (scripts/supervise_change.py:26-35)

- More than one glossary entry is accepted, and so are non-`term/` ids in a glossary entry and `term/` ids in a capability entry.
- `{"glossary": true, "capability": "x"}` is read as a capability entry.
- No client sends any of these today. Plan §5 leaves them open. Decide them with r158.

### 4. Minor, no work-item, observation: the formulate rounds committed helper scripts that fail ruff (.shop/work/i46/runs/design-model-check/1-formulate/splice.py, .shop/work/i46/runs/supervision/1-formulate/splice.py)

- They are tracked Python files under the CLAUDE.md size rule, and they make `tools check` exit 1 with 7 of its 10 ruff errors.
- The i39 ledger already names this pattern ("ruff errors in … round helper scripts").
- **Fix:** do not commit round helper scripts. Either keep them under `.shop/scratch/`, or exclude `.shop/` from ruff.

### 5. Minor, no work-item, observation: commits on the branch belong to no work-item

There are 18 such commits, listed above. Each is a commit of `work run`'s rounds or of `work note`, `work request` or `work` transitions, and none changes code under `scripts/`.

The features/ changes in them are additions by formulate rounds (a0295498, a7147684, edf0301e) and deprecations of retired lines' scenarios. That is formulation's own channel (supervision r146), not a work-item changing `features/`, so I have not graded them Critical. No work-item commit changes anything under `features/`.

### 6. Minor, no work-item, drop: ruff B023 in scripts/supervise_change.py:90, :117

- These lines were already there; w219 touched the file but not them.
- Risk checked: does a lambda capture a stale loop variable? I read lines 87-91 and 115-118. Each lambda is called by `re.sub` within the same iteration, so `field`, `mine` and `said` are always current. It is a false positive.
- A `# noqa: B023` would quiet it.

### 7. Minor, w219, observation: the r54 step asserts an absence that r158 may break (tests/scenarios/spec_integration_steps.py:1086)

- `assert not (repo / ".shop/work/i1/glossary.md").exists()` guards against the glossary entry being taken as a capability named `glossary`.
- If r158 names its glossary-proposal `glossary.md`, this assert fails for the right behaviour.
- **Fix:** check `kind: capability-proposal` instead, when r158 is built.

### 8. Minor, w219, observation: the r55 Thens on spec/index.md cannot fail by themselves (tests/scenarios/spec_integration_apply_steps.py:1005-1015)

The stand-in apply round never writes `spec/index.md`, so only the brief assertions (`term/refund`, `term/order`, "Apply none of them to spec/index.md") can catch a regression. The same was found in the w219 review, finding 3.

### 9. Minor, no work-item, observation: 8 XPASS in the suite are not named

`-rfEx` lists xfails, not xpasses. They are probably r124 Examples rows that already held, since 10 of r124's 18 rows are xfail. A run with `-rX` would name them; **not run**.

## Shape

- **Size limit:** met. `tools size` printed nothing; supervise_glossary.py is 27 lines.
- **"A new concern gets a new module and a row":** met. `scripts/supervise_glossary.py` has its row (CLAUDE.md:37).
- **Row `scripts/supervise*.py`** (supervise_brief.py, supervise_change.py): met. The brief and the change-list reading stay in their modules.
  - The row for `scripts/supervise_change.py` says "one drafted capability-proposal for each capability it names". That is still true, but the row does not say the glossary entry is read and set aside.
  - The module docstring (supervise_change.py:1-3) and the `entries` docstring (:17) still describe capability entries only. Cheap to fix; the w219 review's finding 4.
- **Row `tests/scenarios/`, one `<capability>_*_steps.py` module a concern:** met. The r54 steps are in spec_integration_steps.py and the r55 steps in spec_integration_apply_steps.py.
- **Dead code and steps:** vulture is clean. `answered_proposal` is still reached by the r46 scenario. No step definition lost its scenario.
- **Small duplication:** supervise_glossary.py:6 `FIELDS` repeats supervise_change.FIELDS, and supervise_brief.py:86 reads the glossary-proposals twice (`withheld`, then `text`).

## Coupling

- **pytest-bdd:** step tags become marks, giving `PytestUnknownMarkWarning: pytest.mark.deprecated`. The `PytestRemovedIn10Warning`s (`_register_fixture`, `FixtureDef` baseid) come from pytest-bdd's own compat layer against pytest internals. Upgrading to pytest 10 under this pytest-bdd would break the scenario suite. It relies on nothing the repository itself reaches past the published API. Registering a `deprecated` marker and pinning pytest-bdd and pytest together would make it stable.
- **The new code (w219):** depends only on the standard library and `workqueue.frontmatter`.
- **The `initiative-round` result form:** `{"glossary": true, …}` is an internal contract between `work run` (supervise_brief.py CHANGE_LIST) and agents/initiative-round.md. Both changed in one commit.

## Observations

- Finding 2: once r165 is built, a glossary-proposal's own apply brief will list its own terms as withheld. Reproduction: read supervise_glossary.py:15 against supervision r166.
- Finding 3: `entries([{"glossary": true, "adds": ["thing#r1"]}, {"glossary": true}])` is accepted. Reproduction: read supervise_change.py:26-35; not run.
- Finding 4: `tools check` ruff gives SIM115/I001 in the two `1-formulate/splice.py` files. Reproduction: the brief's `tools check` run.
- Finding 5: 18 commits with no work-item. Reproduction: the brief's Commits list.
- Finding 7: `spec_integration_steps.py:1086` asserts that no `.shop/work/i1/glossary.md` exists. Reproduction: by reading.
- Finding 8: the stand-in apply round writes no `spec/index.md`. Reproduction: spec_integration_apply_steps.py:985-993.
- Finding 9: the brief's suite output gives "8 xpassed" and no XPASS lines.
