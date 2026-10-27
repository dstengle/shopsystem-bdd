# Review of w202 (spec-integration#r44)

**Verdict: DONE_WITH_CONCERNS.** The code does what the plan says and the r44 scenario passes. One Important finding is triaged fix now: integrating-a-proposal's writer template asks the writer for request lines in the upstream's glossary terms, but the same template does not let the writer read the upstream's spec. The template for round 1 does not ask for request lines at all. There are also two Minor findings.

## Commits reviewed

The branch `work/w202` is gone. I took the commits between `d8fd6b33 work: w202 ready -> claimed` and `488540bb work: w202 claimed -> done` on HEAD, leaving out `work run`'s own `work:` commits. That leaves one commit:

- `6e3c4f04` spec-integration r44: the integrate round is told its upstreams and gives the lines of a request into them

This matches the implementer's `result.json` `commits` and the report's `## Commits`. Files changed: `agents/initiative-round.md`, `docs/capability-format.md`, `scripts/supervise_brief.py`, `skills/integrating-a-proposal/SKILL.md`, and two new files, `tests/scenarios/spec_integration_steps.py` (107 lines) and `tests/scenarios/test_spec_integration.py` (8 lines). All are in the work-item's fileset. Nothing under `features/` was changed.

## Removed and weakened tests

None. I looked in `git diff d8fd6b33 6e3c4f04` for deleted or changed lines under `tests/`, dropped parametrize cases, changed or removed `assert` lines, and added `skip` or `xfail`. The only test changes are the two new files.

## Allowances

The report lists none ("none"), and I found none in the commit.

## Cannot verify

- **Reading the upstream's spec.** The round reads the upstream's published spec at an absolute path outside its worktree. `supervise_worker.session` starts `claude -p` with `--allowedTools` and `acceptEdits` but no `--add-dir`. I cannot tell from the commits whether a real (non-stub) session may read that path. The stand-in session in the scenario reads nothing. The plan names this as an open case (§5) and the report leaves it open.
- **Real rounds.** The scenario's Thens check the brief `work run` writes, which is real. The `requests` content they check comes from the stand-in's script. Whether a real `initiative-round` session gives billing's terms is only as good as the prompts (see finding 1).

## Findings

### 1. Important, fix now: the writer is asked for lines in the upstream's terms but may not read the upstream's spec (work-item w202)

**Where:** `skills/integrating-a-proposal/SKILL.md`, the Question Template (the line changed by `6e3c4f04`, around l.59) and The Template (around l.40-47).

**What is wrong:**
- The commit adds to the Question Template (rounds 2 and later) that the `capability-writer` should reply with "the lines of a request into that upstream ... in the terms of that upstream's glossary".
- The same template still says "You may read that file, anything under spec/, features/ and docs/, and the earlier rounds ... Nothing else."
- So the writer is asked for wording it is not allowed to read: the upstream's glossary sits outside `spec/`.
- The round-1 Template, which is the round r44's scenario runs, was not changed. It does not ask for request lines.
- Meanwhile `agents/initiative-round.md` (the line added at l.29) has the round itself read the upstream's spec and give `requests`.
- So the agent and the skill now give two different accounts of who drafts the lines. The account in the skill cannot be followed.

**Why it matters:** r44 requires the lines to be "in the upstream's terms". In a round 2 or later, a writer following its template can only guess those terms. The round may then pass on lines worded in this context's terms, for example "refund" where billing says "credit note". That is a wrong answer to r44.

**Fix:** pick one of these:
- Take the parenthesis out of the Question Template, so the round drafts the request lines itself, as `initiative-round.md` says.
- Or add the upstream's published spec path to the files both templates let the writer read, and ask for the lines in both templates.

### 2. Minor, observation: lint errors in the new test files (work-item w202)

**Where:**
- `tests/scenarios/spec_integration_steps.py:8`: `parsers` is imported but unused (F401).
- `tests/scenarios/spec_integration_steps.py:10`: `CONTEXT` is imported but unused (F401).
- `tests/scenarios/test_spec_integration.py:3`: the import block is unsorted (I001).
- `tests/scenarios/test_spec_integration.py:6`: the `noqa` directive is unused (RUF100).

**Reproduction:** `python3 <Scripts>/tools check --base d8fd6b33` reports these 4 ruff errors and 2 vulture rows. It exits 1.

**Fix:** remove the unused imports, sort the block and drop the `noqa`.

### 3. Minor, drop: duplicated `work run` launcher (work-item w202)

**Where:** `tests/scenarios/spec_integration_steps.py:59-71`.

**What is wrong:** `run_integrate` copies the environment setup of `run_work` in `tests/scenarios/test_supervision.py:63-76` (the stub PATH, `STUB_CLAUDE_*`, the PYTHONPATH filtering). It also uses `__import__("subprocess")` inline.

**Why it matters:** the two copies will drift.

**Fix:** move the launcher into a shared helper (for example in `supervision_world.py`). This is out of this item's fileset, so it is dropped here.

## Risks checked outside the diff

- **Code with no Behaviour line behind it:** none. `Briefs.upstreams`, the `Upstream:` lines, the Read-list entries and `REQUEST_LINES` all serve r44. The new `## Upstreams` section in `docs/capability-format.md` is the format the Implementation section points to. With no `## Upstreams` in `spec/index.md`, the integrate brief is unchanged.
- **Which root relative paths resolve from:** `self.root` is the repository root, and the plan intends relative paths to resolve from there. The scenario's relative path resolves correctly.
- **Malformed input:** a missing spec path or a malformed bullet are not handled. The plan names them as open cases (§5) and no line asks for them, so they are not findings.

## Commands run

- `git log --format='%H %s' --grep="^work: w202 "`, `git log --oneline -15`: `work/w202` is gone (`git log ... work/w202` gave "unknown revision"); found the commits on HEAD
- `git log --stat d8fd6b33..488540bb`, `git diff d8fd6b33 6e3c4f04`
- `cat features/spec-integration.feature`; `git show 6e3c4f04:scripts/supervise_brief.py`; `git show 6e3c4f04:skills/integrating-a-proposal/SKILL.md`
- `grep` for session permissions in `scripts/supervise*.py`; `sed -n 200,260p scripts/supervise_worker.py`
- `grep` for `STUB_CLAUDE_PLAN` in `tests/scenarios` and `tests/scenarios/test_supervision.py`
- `python3 <Scripts>/tools check --base d8fd6b33`:
  - ruff: 4 errors (finding 2)
  - vulture: 2 unused imports (finding 2)
  - import-linter: "the project states no import contracts"
- `python3 <Scripts>/tools size --limit 300`: printed nothing, so no file is over the limit
- `python3 -m pytest -q tests/scenarios/test_spec_integration.py -p no:cacheprovider`: 1 passed
