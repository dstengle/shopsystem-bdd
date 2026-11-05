---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-9-review
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
---

# Plan 9 (retirement and the 2.0 step): end-of-branch review

One fresh reviewer, 2026-11-05, of `f9807bc8..b1d2f68e` on `workflow-simplification`: Tasks 1-8 by the first
implementer, 9-11 by the second. The review read `design.md`, `roadmap.md`, `plan-9-retirement.md` (Review Focus,
Global Constraints, D1-D23, the carried-over table), `plan-9-implementation.md` (claims, deviations 1-27), the rulings
of plans 1-8, `CLAUDE.md`, `README.md`, `hooks/hooks.json`, `.claude-plugin/` and
`scripts/migrate_upgrade_simplified.py`. It ran the plan's verification commands, a retirement diff over the range,
the 2.0.0 upgrade on scratch clones, and the new workflow end to end in a scratch repository. The scratch directories
are under `/home/vscode/.claude/jobs/7e9ba079/tmp/review9/`. Nothing in the repository was changed but this record,
and it is not committed.

## Verdict

**Approve. Nothing is blocking.** The branch can go to the person as one pull request to `main` once the five
"should fix" items below are fixed. Each is small, and only S2 and S4 need a ruling, each with a recommended one.
Q3, on peer request q14, is not a code change, but D20's reading of it is wrong and should be corrected before
anyone runs `work resolve` on it.

The review checked the following, and each holds:
- **Retire, never edit.** All 271 retired lines are in their capability's `retired:` list. No merged line was edited.
  The only group edits are D17's P10 example data (r14, r19). `model restates` still reports 0 missing.
- **`.shop/work/`.** It is unchanged byte for byte, except that `FROZEN.md` was added and `q14.md` was moved (`R100`).
- **The upgrade.** It loses nothing, running it twice is safe (the second run does nothing), and it puts everything
  back when it fails, including when the failure comes after the step's changes are made.
- **The new workflow.** It runs end to end in a scratch repository.
- **The hooks.** Every hook exists and exits 0 under `python3 -S`.

What the review found:
- **The report has one false figure:** `tools check` is not clean (S3).
- **Three spots still describe the old workflow** in places a consumer or a session reads, which the plan's grep test
  does not cover:
  - `.claude-plugin/marketplace.json` (S1);
  - `spec/universal.md`'s U1/U2/U6/U9/U10 (S2);
  - `agents/architecture-reviewer.md` (S4).
- **A 0.29 repository that upgrades straight to 2.0 is told two contradictory things** about `.shop/work/` proposals,
  and is pointed at a skill that no longer exists (S5).

## Verification

Each command was run with the plan's exact invocation, at `b1d2f68e`.

| check | the report | measured here | |
|---|---|---|---|
| `python3 -m pytest -q -p no:cacheprovider` | 1260 passed, 1 skipped, 77 subtests | **1260 passed, 1 skipped, 77 subtests** (24.4 s) | ✓ |
| `-m timing -n 0` | 4 passed | **4 passed** (2.9 s) | ✓ |
| collected ids | 1261 (−394 / +72 over the plan) | 1583 at `f9807bc8` → **1261**: −393 / +71 net | ✓ (net −322 both; per-task sums count one id added and later removed) |
| `model check` | 0 / 16 / 0 / 0 | **0 violations, 16 warnings, 0 unresolved, 0 file problems** | ✓ |
| `model logic` | 4 L5 | **4 findings: 4 L5** | ✓ |
| `model lexicon --check` | 402, 0 problems | **402 terms, 0 problems** | ✓ |
| `model decisions --check` | 5 hold | **5 check decisions: 5 hold, 0 failing** | ✓ |
| `model restates` | 581: 140 / 441 / 0 / 0 | **581 ids: 140 restated, 441 dropped, 0 pending, 0 missing** | ✓ |
| `features generate --check` | exit 0 | **exit 0** | ✓ |
| `vocab --check` / `bindings --unbound` | clean | **every step has one handler / every binding names a scenario** | ✓ |
| `tools size --limit 300` | silent | **silent, exit 0** | ✓ |
| `tools check $(git diff --name-only --diff-filter=d 19e9fee5 -- …)` | "ruff and vulture clean" | **ruff: `tests/scripts/test_request_counter.py:90:58: F811 Redefinition of unused repo from line 15`; exit 1** | ✗ (S3) |
| unbuilt | `{} 0 []` | **`{} 0 []`** | ✓ |
| `ls agents skills` | 3 / 5 | **3 / 5**, as D12 lists | ✓ |
| plugin / `.shop/plugin-version` / `migrate status` | 2.0.0 / 2.0.0 / none pending | **2.0.0 / 2.0.0 / none pending** | ✓ |
| `--help` of every subcommand of `model`, `measure`, `migrate`, `features`, `tools`, `work` | (Task 3's test covers `work`) | **all exit 0** | ✓ |
| import scan: every tracked script and test resolves its imports | `test_kept_modules` | **no import of a missing module**; no string reference to a deleted module outside `test_kept_modules.OLD`/`test_retirement` | ✓ |
| hooks under `python3 -S` (in the repo, in a 1.0.0 clone, outside a repo) | `test_hooks` | `migrate status --hook`, `conversation_hook names`, `conversation_hook quote`: **every one exits 0**; a 1.0.0 repo is offered the 2.0.0 step | ✓ |

### Retire, never edit

A script compared every `[r<n>]` line of `spec/capabilities/*.md` between `f9807bc8` and `HEAD`. It checked each
line's text with its continuation lines, each group's whole text, and `retired:`.

- **Lost** (gone from Behaviour and not in `retired:`): **none**.
- **Edited in place:** **none**.
- **Group changed:** only migration-tools g14 and g19. In both, the given's `"1.0.0"` became `"2.0.0"`, which D17
  allows under P10. `main` has no codified migration-tools, so those lines were never merged.
- **New:** only migration-tools r24 (D17).
- **Retired:** batch-measurement 17, code-research 6, delivery 11, design-model-check 23, migration-tools 2,
  planning 7, red-green 15, requests 6, review 21, role-boundaries 6, spec-consistency 17, spec-integration 16,
  spec-migration 14, supervision 84, work-queue 26. That is **271**, exactly D2's ids for each capability.
- Every retirement removed whole groups; no group lost only part of its lines.
- Glossary definitions changed only where D17 and D19 say so.
- The helper `plan-9-retire.py.txt` has one commit (`b63d286b`).
- `v15c` (a retired id used again) is still a rule and still tested in `test_model.py`. The deleted
  `test_adding_a_retired_id_is_v15c` tested a proposal's `adds:`, which no longer exists.

### `.shop/` over the range

`git diff --name-status f9807bc8..HEAD -- .shop` shows:
- `M .shop/plugin-version`;
- `A .shop/work/FROZEN.md`;
- `R100 .shop/work/requests/q14.md → .shop/requests/q14.md`;
- the added records, backlog items b1-b4 and the records index rows;
- the plan's ticked boxes, which the plan's own Task 11 asks for.

No record was otherwise edited.

### The 2.0.0 upgrade on scratch clones

| run | result |
|---|---|
| `v1`: clone at `f9807bc8` (1.0.0), no git identity | exit 1 in 0.41 s. stderr: `migrate put the repository back as it was; it could not make every change: Author identity unknown` and git's advice. HEAD unchanged, `status --porcelain --untracked-files=all` empty, no `.shop/requests/` left. The failure came **after** `apply` had moved q14 and written `FROZEN.md`, so this also tests rollback of a half-applied step. |
| `v1` with a local identity | exit 0. One commit `migrate upgrade: 1.0.0 to 2.0.0` with 3 entries (`M plugin-version`, `R100 q14`, `A FROZEN.md`) and 0 deletions. 72 note lines: 12 open initiatives, 30 proposals, 28 internal requests, 1 move. The commit message is **byte-identical** to `f298479d`'s, and the `.shop/work` and `.shop/requests` trees are identical too. Afterwards `model check` gives 0/16/0/0 and `work list` names q14. |
| `v1`, second run | `no upgrade step is pending`, exit 0, HEAD unchanged. Running it again is safe. |
| `v1b`: a tracked `.shop/requests/q14.md` | exit 1: `could not move .shop/work/requests/q14.md onto .shop/requests/q14.md`. HEAD unchanged, tree clean, no `FROZEN.md`. |
| `v1b`: `spec/decisions/index.md` a symlink to `/dev/full` | refused before applying (`it is a symbolic link`). Nothing changed. |
| `v1b`: two request files with unreadable frontmatter | exit 1, naming both files. Nothing changed. |
| `v029`: clone of `main` (`96818f71`, plugin-version `0.25.0`) | exit 0 in 1.5 s. One commit `0.25.0 to 2.0.0` runs the 1.0.0 and 2.0.0 steps together: `A spec/restated.json`, `A FROZEN.md`, `R100 q14`, 1739 `M` (the 1.0.0 step's `@0.29` rewrite and scaffolds), 0 deletions. A second run does nothing. Afterwards `model check` gives 590 violations and `model restates` gives 581 missing. That is expected: the scaffolds are "left for a session to write". But see S5. |

### The new workflow end to end

The scratch repository was `review9/e2e2`, with a bare remote `e2e2.git` and `SHOPSYSTEM_WORK_GH=tests/scripts/stub_gh.py`.
The real remote was never touched. The run went through these steps, and every one exited 0:
1. `work idea` → `shape` → `line --into work-queue` (gave `work-queue#r5`) → `ready`;
2. `batch start` → `batch resume` (the task's worktree) → built: `unbuilt: []` was committed with `Item: b1`;
3. `batch done batch-1 t1` → `batch review` (pull request #1 on the stub) → `batch brief` → findings saved →
   `batch reviewed` (`awaiting-merge`);
4. a merge on `main` → `batch merged` (b1 `delivered`);
5. `measure batch batch-1` (wrote `.shop/records/measurements/2026-11-05-batch-1.md`);
6. `conversation_hook names` (lists b1 and batch-1) and `conversation_hook quote`, both under `-S`;
7. `migrate status --hook`, under `-S`.

`git status --porcelain` was empty after `merged`. `measure batch` leaves its record uncommitted. That is plan 7's
behaviour and not in this range.

## Findings

### Blocking

None.

### Should fix

**S1. `.claude-plugin/marketplace.json:8` still describes the 1.x plugin.**
- *Evidence:* its `description` reads "… deliver an initiative's work-items with work run, implement red-green, …".
  That is the text the `claude plugin marketplace add dstengle/shopsystem-bdd` listing shows, which README's Install
  section points at.
- *Cause:* D22 changed only `plugin.json`. `test_retirement.py::test_no_kept_skill_or_agent_names_a_deleted_one`
  scans `skills/`, `agents/`, `README.md` and `CLAUDE.md`, but not `.claude-plugin/`.
- *Fix:*
  - Set `marketplace.json`'s plugin description to `plugin.json`'s D22 text.
  - Add `.claude-plugin/` to the grep test's paths.
  - Add a test that the two descriptions are equal. 0.8.0's commit `64a60bb1` already made them match once.

**S2. `spec/universal.md`'s U1, U2, U6, U9 and U10 are still live guarantees of the deleted `work run`.**
- *Evidence* (`spec/universal.md:23-32`):
  - U1: "`work run` shall hold at most `workers` worker slots";
  - U2: "`work run` shall not start a stage …";
  - U6: "… `work run` shall discard the stage";
  - U9: "A delivery shall change no file of an initiative …";
  - U10: "When `work run` starts a stage, `work run` shall give the stage only a brief".
- Its frontmatter says `retired: []`. `model logic` still adds each U as an `always` constraint of every check (the
  file's Purpose).
- Neither D2 nor the carried-over table mentions `universal.md`. So the guarantees of a program that 2.0 deletes are
  still stated as true in every trace, which goes against design § Migration ("the old capabilities' requirements
  retired in bulk under one decision").
- U7 ("A worker shall change only files in its worktree") hangs on the term `worker`, which the glossary defines as
  "a session `work run` starts".
- *Fix:*
  - Retire U1, U2, U6, U9 and U10 into `universal.md`'s `retired:`, under 0080 (add them to 0080's list; the
    `## Decision` text is the plan's own, not an older decision's).
  - Keep U3, U4, U5 and U8.
  - Check that `model logic` still gives its 4 L5.
- *Question for the person:* U7, which is still true of a batch's task subagent in its worktree but is worded with a
  1.x term.
  - *Recommended ruling:* keep U7 as it is for now, and leave `worker` in the lexicon with D19's other old kinds
    (open item 26).
  - Retire U7 and give it a new id only when a line about a batch's task subagent is written.

**S3. `tools check` is not clean, but the report says it is.**
- *Evidence:* `tests/scripts/test_request_counter.py:90:58: F811 Redefinition of unused 'repo' from line 15`.
  - Task 6 (`a1a8d953`) added `test_a_new_request_is_numbered_above_the_frozen_ones(repo)`.
  - Line 15 already imports `repo` as a fixture with `# noqa: F401`, but not F811.
  - The plan's Task 11 command exits 1. The report's Final state row says "ruff and vulture clean".
- *Fix:* make line 15 `# noqa: F401, F811`, or move the `repo` fixture into `tests/scripts/conftest.py`. Then rerun
  the Task 11 command and correct the report's row in a new record. Records are never edited, so the correction
  belongs in the rulings record.

**S4. `agents/architecture-reviewer.md` still describes the 1.x branch review, and still writes its findings with Write.**
- *Evidence:*
  - `:3`: "(the initiative's branch review verifies shape and coupling every initiative)". That review was
    `bdd-branch-reviewer`, which is deleted.
  - `:12`, `:14`, `:31`: "the work-items the input prompt names", "Name the work-item each refactor would unblock".
  - `:4`: `tools: Read, Glob, Grep, Bash, Write`, and its job is to write a findings file. Plan-7 Q1/B1 moved
    `pr-reviewer` to "the findings are the reply" because the harness refuses a subagent's Write of the findings
    file. The plan-7 rulings say the old reviewers hit the same refusal. The one reviewer kept besides `pr-reviewer`
    is left on the pattern that failed.
- *Fix:*
  - Reword the description and body for 2.0: "an architecture review when the person asks for one, of the commits or
    the batch the input prompt names; items in place of work-items".
  - *Question for the person*, on Write. *Recommended ruling:* give it `pr-reviewer`'s pattern:
    - tools Read, Glob, Grep and Bash;
    - its reply is the findings, saved by the session;
    - 0083's `enforced_by` test changes to match;
    - README's agent table changes to match.
  - Until then, the agent's first real use is likely to hit the refusal.
- `agents/pr-reviewer.md:78-86`'s example findings ("abandon leaves the initiative started", `work abandon`) are
  domain examples of a fixture and can stay. They would read better as an item example.

**S5. A 0.29 repository that upgrades straight to 2.0.0 (D23, the only real consumer path) gets contradictory notes,
and its only guidance names a deleted skill.**
- *Evidence* (the `v029` run above):
  - The same commit message gives both "left for a session to write: .shop/work/i45/requests.md, a
    capability-proposal that is `awaiting-answer`, in 0.29 lines" and "the lines of proposal .shop/work/i45/… were
    never applied: shape an item with them if still wanted".
  - It also writes `FROZEN.md`, which says "Nothing writes here". The first note comes from
    `scripts/migrate_upgrade_codified.py:250`.
  - The 19 scaffolds are "left for a session to write". The one place that says how, README's 1.0.0 section
    (`README.md:155`), says "Write those with `integrating-a-proposal`", which D12 deleted. README's 2.0.0 section
    says only "A 0.29.x repository reaches 2.0.0 through the 1.0.0 step in the same commit".
  - `docs/capability-format.md:444` has the procedure ("a session writes the codified requirements"), but nothing
    points a consumer there.
- *Fix:*
  1. In `migrate_upgrade.upgrade`, when the 2.0.0 step is among the pending steps, drop the 1.0.0 step's
     `.shop/work/…capability-proposal… in 0.29 lines` notes. The 2.0.0 step's "never applied" note names each of
     them already. Alternatively, have `migrate_upgrade_codified` skip them when the plugin is at 2.0.0 or later.
     Extend `test_a_0_29_repository_reaches_2_0_in_one_commit` to assert that no "left for a session to write:
     .shop/work/" line appears.
  2. Add one sentence to README's 2.0.0 section: "From 0.29.x, write each scaffold's requirements and the typed
     glossary as `docs/capability-format.md` § Converting says, checking with `model parse`, `check`, `logic` and
     `restates`, then `features generate`." The 1.0.0 history section stays as it is (D22).

### Minor

**M1. `migrate upgrade` with no git identity fails with git's raw text.**
- *Evidence:* the `v1` run's stderr is "migrate put the repository back as it was; it could not make every change:
  Author identity unknown *** Please tell me who you are. …". `work` reports the same case as `work: git commit
  failed: Author identity unknown` and changes nothing.
- *Grade:* minor.
  - r15's all-or-nothing holds: the rollback was complete even after the moves.
  - U3 holds: it exits with an error naming the reason and changes nothing.
  - git's text already says how to fix it.
  - Every step has the same behaviour, and it predates 2.0.0.
  - It is a consumer's first command on the new release, though, and the failure spends a full plan-and-apply first.
- *Fix:* in `scripts/migrate_upgrade.py:upgrade`, after the `uncommitted` check (line 138), refuse before planning
  when `git var GIT_COMMITTER_IDENT` exits non-zero. The refusal reads: `migrate changed nothing; git has no identity
  to commit with: set one with git config user.name "…" and git config user.email "…"`, with exit 1. Test it with
  `HOME` pointed at an empty directory and the `GIT_*` identity variables unset. The scenario world sets them (`WHO`
  in `migration_tools_handlers.py:27`), so no test meets this today. `shop_files.committed` could give the same
  sentence for `work`.

**M2. Dead references to deleted things:**
- `ruff.toml:61` (`"tests/scripts/stub_claude.py" = ["EXE001"]`);
- `tests/scenarios/migration_tools_handlers.py:28` (`"`migrate compacting`": "PreCompact"`, a key no feature
  names now);
- `spec/capabilities/migration-tools.md:23`, the term **the PreCompact hook**, which "runs `migrate compacting`".
  The term may stay under D19's open item 26; the other two should go.
- *Fix:* delete the ruff entry and the `HOOKS` key.

**M3. `docs/capability-format.md` still teaches with the old workflow's lines.**
- *Evidence:* the worked example `### [g1] \`work start\` starts a proposed initiative` (`:80-82`), and the grammar
  prose naming `work run` (`:130`, `:151`, `:227`, `:245-247`).
- Deviation 21 keeps the example glossary as an illustration, which is defensible, but a reader of 2.0 meets commands
  that do not exist.
- *Fix:* at the least, add a note above the example ("an example from plugin 1.x's vocabulary"). Better, rewrite it on
  `work shape`/item when the doc is next touched. Add `docs/capability-format.md` to S1's grep with an allowance for
  the example block.

**M4. Collection-diff figure.** The report gives −394 / +72 over the plan. Base-to-head is −393 / +71, and the net is
the same (−322). The per-task sums count one id that one task added and a later task removed. The figures are
consistent; no fix is needed beyond a sentence in the rulings.

### Questions for the person

- **Q1 (from S2): U7.** Recommended ruling: keep it until a batch-task line exists.
- **Q2 (from S4): architecture-reviewer's Write.** Recommended ruling: the reply-as-findings pattern of
  `pr-reviewer`.
- **Q3 (should fix in substance): q14 is not fulfilled the way the report and D20 say.**
  - q14 is `product/missingmass.io/subscriptions-viewer`'s request. It is `accepted` and now lives at
    `.shop/requests/q14.md`.
  - D20 and the report say its fulfilment is "requests go through one shared tool", which `work request` already is,
    so the person only has to `work resolve` it. The file says otherwise: **26 lines, all `accepted`**.
  - Lines 2-3 and 13-22 ask for a carrier port, a second carrier and the identity of askers. That is the deferred
    b1 ("Requests between repositories over GitHub issues"), not built.
  - Lines 19 and 23-26 name `work run`, its `integrate` round and `work status`, all deleted in this range. As
    accepted, they cannot be delivered.
  - Resolving q14 now would tell the asker that accepted lines hold when they do not.
  - *Recommended ruling:*
    - Do not resolve q14 at the merge.
    - Note on b1 that it delivers q14's carrier lines (`work depend` does not take a request, so put it in b1's
      notes).
    - The person tells the asker, through q14's own commands, that lines 19 and 23-26 are withdrawn by the upstream's
      2.0 release, and offers their 2.0 form (items and batches) if still wanted.
    - Resolve the rest when b1 is merged.
    - The plan-9 rulings should correct D20's reason for leaving q14 out.

## The carried-over items

The 22 settled rows check out against their commits. Of the five open rows:
- **2** (`_LineParser`, waits for a Python 3.12 floor): may stay open. It is not tied to the old commands.
- **13** (r52 against decision-tiers r5): may stay open. It is ruled by the "If" precedence.
- **21** (the names table expands no `q<n>`/`r<n>`): may stay open. It needs a conversation line.
- **26** (old terms in the lexicon): may stay open. Removing one could break a kept given.
- **27** (design model v5): may stay open. A v6 is a design session's work.

19 needs nothing below about 50 rows.

**One item is missing from the table:** `spec/universal.md` (S2). It is the one open item that should not stay open,
because it states guarantees of the deleted program as true in every trace.

## The deviations

All 27 are acceptable. Notes on the ones that matter:

- **6 (D4 narrowed to a capability with ids in `retired:`):** right. feature-file-tools r17's example needs an empty
  codified capability to still get its file.
- **7 (`world_fallbacks.py`):** acceptable. The kept Given (`GivenR on`) records nothing. The steps that use it
  (`batches.feature:55`, `backlog.feature:59`, `:129`, `telemetry.feature:22`) are read by their features' own
  handlers or by the When's text. The Thens and Whens that fall through fail and name the step, so nothing passes
  unchecked.
- **5 (`test_spec_retired` written after the helper ran, so its red was not watched):** a process slip. The test was
  checked here by the retirement diff above, which agrees with it.
- **11, 17 (handlers trimmed by `vocab --check` or a key scan):** fine. `vocab --check` and `bindings --unbound` are
  clean.
- **12 (`work answer` loses `--change`/`--accept`; `work show` with no target is `work list`):** fine. They were 1.x
  reviewer flags.
- **14, 18 (no reference to a frozen kind or a frozen request is resolved):** consistent with D5. They settle plan-1
  S10.
- **15, 16:** fine. 16's `shop_frozen` reads frontmatter through `model_parse` to avoid an import cycle, and
  `migrate_upgrade_simplified` does the same.
- **22 (`--from internal` in place of a peer):** right. Requests r32 refuses the plan's version.
- **23, 24 (one extra refusal test; `apply` makes the destination directory; an own-context asker counted as
  internal):** right, and checked here (`v1b`).
- **25, 26 (r24's given index as text; `work_queue_world.matches` reads a backticked path):** acceptable. 26 is named
  in the report's open problems. A capability that later wants its own "write" handler must chain through `local`.
- **27 (no Task 10 commit of its own):** fine.

The rest (1-4, 8-10, 13, 19-21) are bookkeeping or order changes with their reasons given, and none weakens a check.

## Files

- Reviewed: the range `f9807bc8..b1d2f68e` (258 files, +2894 / −14242).
- Scratch:
  - `review9/gate.txt`, the gate's output;
  - `review9/ids-base.txt` and `ids-head.txt`, the collected ids;
  - `review9/v1-noid.txt`, `v1-up.txt` and `v029-up.txt`, the upgrade outputs;
  - the clones `review9/v1`, `v1b` and `v029`;
  - the end-to-end repository `review9/e2e2`, with its bare remote `e2e2.git`;
  - the scripts in `review9/bin/`: `retire_check.py`, `imports.py` and `e2e.sh`.
