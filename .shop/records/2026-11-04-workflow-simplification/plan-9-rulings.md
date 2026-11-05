---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-04-workflow-simplification-plan-9-rulings
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-05
status: done
---

# Plan 9 of the workflow simplification: rulings on the review, and what was done with each finding

`plan-9-review.md` (committed in `6c6c7cf8`) asked the person three questions. The person was not available. Each
ruling below was **ruled by the main session without the person, 2026-11-05; revisit.** The fixes are on branch
`workflow-simplification`, from `604d4ded` to this record's commit, and are not pushed. Every new test failed before
its fix.

## Rulings

| # | Question | Ruling (main session, without the person, 2026-11-05; revisit) | What was done |
|---|---|---|---|
| Q1 | U7 ("A worker shall change only files in its worktree") | Keep U7 for now. Retire U1, U2, U6, U9 and U10 under 0080, the retire-never-edit way. | `bf12133a`: the five lines leave `spec/universal.md`'s Behaviour, and their ids go into its `retired:` and into 0080's list (the plan's own decision). The Purpose says why, and the Reading drops their bullets. `spec_read.read_universal` reports a retired U<n> used again. `grammar/corpus/universal.txt` keeps all ten sentences, because it is the grammar's corpus and not the spec. `worker` stays in the lexicon with D19's old kinds (open item 26). |
| Q2 | architecture-reviewer's Write | Use `pr-reviewer`'s pattern: no Write, and the reply is the findings. Rewrite its description for the 2.0 workflow. | `3575aeb2`: tools are Read, Glob, Grep and Bash (it still runs the suite and the size check). The agent changes nothing, and the session that started it saves its reply. Its description and body name the commits or the batch it is given, and items. 0083's summary and table now say "no Edit or Write", and the decisions index and README's agent table follow. `test_agents` gains `test_architecture_reviewer_has_no_write_and_replies_with_its_findings`. |
| Q3 | q14 | Do not resolve q14. Note on b1 that it delivers q14's carrier and identity lines. Tell the asker that lines 19 and 23-26 are withdrawn by 2.0, using the request mechanism if one fits, in-repo only. | `a6b1adc2`, `ab8a62c7`, `2aa77e10`, `b15d8307`, `465177a6`: `work outcome q14 <n> withdrawn --reason …` for lines 19 and 23-26. The line outcome `withdrawn` is one of the upstream's values. Each reason names the-old-workflow-retired and the 2.0 form: `work intake`, or `work request` with the item waiting in the backlog. The request stays `accepted` and in the upstream's turn. Nothing was sent outside the repository. `b1fe9f51`: b1's Notes say it delivers q14's lines 2-3 and 13-22 (line 19 is withdrawn, and its take-in is b1's to restate), and that q14 is resolved when b1 is merged. No command writes a note on an item without changing its status, so the note was written into the file and committed. |

**D20's reason corrected.** D20 and `plan-9-implementation.md` say q14's fulfilment is "requests go through one
shared tool, which `work request` already is", so it only had to be resolved. That is wrong. q14 has 26 accepted
lines. Lines 2-3 and 13-22 ask for a carrier port, a GitHub-issue carrier and askers' identities, which is b1 and not
built. Lines 19 and 23-26 name `work run`, its `integrate` rounds and `work status`, which 2.0 deletes. q14 was
rightly left unresolved, but for this reason.

## The findings

| # | What was done |
|---|---|
| S1 | Fixed in `604d4ded`. `.claude-plugin/marketplace.json`'s description is now plugin.json's D22 text. `test_the_marketplace_describes_the_plugin_as_plugin_json_does` holds the two equal. `test_no_kept_skill_or_agent_names_a_deleted_one` now also reads `.claude-plugin/*` and `docs/capability-format.md` (M3). |
| S2 | Fixed in `bf12133a`, as ruled in Q1. Tests: `test_the_universal_conditions_of_work_run_are_retired` and `test_a_retired_universal_condition_used_again_is_a_problem`. `model logic` is unchanged at **4 findings: 4 L5** (U4 ×2, U7, U8). The five retired conditions gave no finding before, so the expected figures stay as they were. |
| S3 | Fixed in `07b2d0b4`. `# noqa: F811` sits where ruff reports the redefinition (`test_request_counter.py:90`, the test's `repo` parameter). The import's `F401` is unchanged. **Correction of `plan-9-implementation.md`'s Final state row:** at `b1d2f68e`, `python3 scripts/tools check $(git diff --name-only --diff-filter=d 19e9fee5 -- '*.py' scripts/work scripts/model scripts/measure scripts/migrate scripts/features)` exited 1 on that F811. It was not clean. After the fix, the same invocation prints `All checks passed!` / vulture `clean` / `the project states no import contracts` and exits 0. |
| S4 | Fixed in `3575aeb2`, as ruled in Q2. |
| S5 | Fixed in `10e1a0f6`. When the 2.0.0 step is among the pending steps, `migrate_upgrade.upgrade` drops the 1.0.0 step's notes that start "left for a session to write: .shop/work/" (`migrate_upgrade_simplified.superseded`). The 2.0.0 step's "never applied" note already names each of those proposals, and `FROZEN.md` says nothing writes there. `test_a_0_29_repository_reaches_2_0_in_one_commit` gains an `awaiting-answer` proposal and asserts the note is gone from both the output and the commit message. README's 2.0.0 section now says how a 0.29 repository writes its scaffolds: `docs/capability-format.md` § Doing it, `model parse`/`check`/`logic`/`restates`, then `features generate`. The 1.0.0 history section is unchanged. migration-tools' Implementation notes both changes. |
| M1 | Fixed in `10e1a0f6`. After the uncommitted check and once a step is pending, `migrate upgrade` refuses when `git var GIT_AUTHOR_IDENT` or `GIT_COMMITTER_IDENT` fails. The refusal is `migrate changed nothing; git has no identity to commit with: set one with git config user.name "…" and git config user.email "…"`, with exit 1. It plans nothing and changes nothing. Test: `NoIdentity::test_no_identity_is_refused_before_any_step_naming_git_config` (`HOME`/`XDG_CONFIG_HOME` empty, `GIT_*` and `EMAIL` unset, `user.useConfigOnly` so that git does not guess an identity from the host). The same sentence for `work` (`shop_files.committed`) was not done. |
| M2 | Fixed in `07b2d0b4`. `ruff.toml` loses the `[lint.per-file-ignores]` entry for the deleted `stub_claude.py`, and migration-tools' `HOOKS` loses the key for `migrate compacting`. The term **the PreCompact hook** stays with D19's old terms (open item 26). |
| M3 | Fixed in `604d4ded`. `docs/capability-format.md`'s capability-file example is now the backlog: `work shape` on an item that is `idea` (it parses). The prose examples (one statement, only lexicon words, a value's slot, exclusivity, a gloss) use 2.0 words. The exclusivity example no longer leans on U2, which is retired. The glossary example keeps 1.x's words under a note naming "plugin 1.x's vocabulary", and the grep test allows a fenced block under such a note. |
| M4 | No change. Base to head is −393 / +71. The report's per-task sums give −394 / +72, because they count one id that one task added and a later task removed. The net is −322 both ways. |

**One more fix.** `093ce9a5`: `plan-9-review.md` was written with `kind: review`, which `model check` refuses as a
file problem (0 → 1). It is now `kind: analysis`, as the reviews of plans 1-8 are. No other text of it changed.

## Verification after the fixes

| Check | Before (review, `b1d2f68e`) | After |
|---|---|---|
| `python3 -m pytest -q -p no:cacheprovider` | 1260 passed, 1 skipped, 77 subtests | **1265 passed, 1 skipped, 80 subtests** (24.2 s, 24.5 s in two runs). The 5 new tests are S1's, S2's two, Q2's and M1's; the 3 new subtests are the words of Q2's test. 1266 ids. |
| `python3 -m pytest -m timing -n 0 -q` | 4 passed | 4 passed, 1266 deselected |
| `model check` | 0 / 16 / 0 / 0 | 0 / 16 / 0 / 0 (with the review record committed and its kind corrected) |
| `model logic` | 4 findings: 4 L5 | 4 findings: 4 L5 (U4 ×2, U7, U8): unchanged, see S2 |
| `model lexicon --check` | 402 terms, 0 problems | same |
| `model decisions --check` | 5 hold, 0 failing | 5 hold, 0 failing; index current (0083's summary rewritten) |
| `model restates` | 581: 140 / 441 / 0 / 0 | same |
| `features generate --check`, `vocab --check`, `bindings --unbound` | exit 0; one handler each; every binding names a scenario | same |
| `tools size --limit 300` | silent | silent, exit 0 (`migrate_upgrade.py` 197) |
| `tools check $(git diff --name-only --diff-filter=d 19e9fee5 -- '*.py' scripts/work scripts/model scripts/measure scripts/migrate scripts/features)` | exit 1 (F811) | ruff `All checks passed!`, vulture clean, no import contracts; exit 0 |
| unbuilt | `{} 0 []` | `{} 0 []` |

## Left for the person

- **q14:** pass its turn to the asker (`work turn q14`) when the person wants the asker shown the five withdrawn lines
  and their reasons. Until then they sit in `.shop/requests/q14.md` in the upstream's turn. Resolve the rest
  (`work resolve`) when b1 is merged. Offer the asker the 2.0 form of lines 19 and 23-26 if still wanted.
- **U7:** retire it and give it a new id when a line about a batch's task subagent is written.
- **The rulings above**, all made without the person.
- M1's sentence for `work`'s own commits, if wanted.
