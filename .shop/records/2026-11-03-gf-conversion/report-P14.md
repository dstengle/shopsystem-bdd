# P14 report: the release (legacy removal, v_p0, 1.0.0, docs, smoke)

Branch `gfc/P14`, from `gf-conversion` at cff877b2. Written test first, with `SHOPSYSTEM_GF` unset (P1's installer).

## What changed

- **The 0.29 reader is gone.**
  - `scripts/model_legacy.py` is deleted. `model_parse` loses `glossary_entry`, `bullets`, `RID`, `ENTRY` and
    `CATEGORY`.
  - `model_facts` no longer reads a 0.29 glossary, Behaviour or `@r<n>` scenario.
  - `model.lp` loses v_e1/v_e2, `has_sc`, `legacy_req` and the LEGACY clauses of v2, v15f, v_s1–v_s3 and `ctx_of`.
    The v_s2 and v_s3 labels now speak of groups only.
- **v_p0** ("a spec file is not codified (no `language: codified-1`): run `migrate upgrade`"). A capability file,
  `spec/index.md` or `spec/universal.md` without the marker gives `uncodified(F)`, and that file is not read.
- **Refusals that name `migrate upgrade`:**
  - `work request` (`workqueue_lines.check`) refuses an upstream whose `spec/index.md` or any capability file is not
    codified. The 0.29 EARS branch is gone.
  - `features generate`, named or not, `--check` or not, exits 2 on an uncodified service capability, through
    `features_generate.uncodified`. The `skipped <c>: not codified` line is gone.
- **v15a/v15b on codified files.** The design-model-check spec (r3, r4) needs both, and the codified reader had made
  them unreachable. `spec_read.Group.odd` keeps each statement left out of a group's requirements, either one with no
  id or one whose id came earlier, next to its file problem. `model_spec` makes it a requirement node:
  `<cap>#line<n>`, with no `req_id`, gives v15a; `<cap>#r<n>~<line>` gives v15b.
- **Mentions.** A statement that does not parse is now read for words, so an avoided word in it gives v_t1
  (design-model-check r20). Parsed statements and generated scenarios still give no mentions.
- **0.29 ids are history.** `model_facts.resolve_req` accepts any `<cap>#r<n>@0.29`, which was the gate L4 call. About
  650 rewritten references name ids that were retired before `restated.json` was frozen. `model_work` checks for
  `@0.29` explicitly instead of relying on `Model.nodes`. As a result, `test_model_spec` now expects no unresolved
  `@0.29` reference.
- **`migrate upgrade` run here.**
  - `.claude-plugin/plugin.json` is now 1.0.0, committed first.
  - `python3 scripts/migrate upgrade` took `.shop/plugin-version` from 0.25.0 to 1.0.0. The 1.0.0 step skipped every
    capability, since all are codified, and rewrote the old references in `.shop/work/**` (1715 files).
  - The step lists 25 open capability-proposals still in 0.29 lines, left for re-integration by a session: i45, i47,
    i52, i53, i55, i56, i58, i59 and i61.
- **Docs:**
  - README.md: a 1.0.0 section with the upgrade notes. The header, Requires, workflow, Scripts and Agents table now
    describe the codified flow. `feature-formulator` is gone from the file.
  - CLAUDE.md: module-map rows for every module from P1–P13, plus `supervise.py` by name. The `features*.py` row no
    longer says "editing". The `tests/scenarios/` rows now describe handlers.
- **Sweep (`tools check`, vulture):**
  - `features_gherkin.locate`, `locate_in` and `background_steps` were dead, and are removed.
  - The `tests/scenarios/migration_upgrade_steps.py` shim is deleted, since nothing imported it.
  - An unused lambda parameter in `test_model_output.py` was fixed. Stale `noqa` comments were removed.
- **Smoke test** `tests/scripts/test_tools_codified_smoke.py` (design §18 point 22). It runs on the live repo:
  - `measure show` of the first kept measurement it can read;
  - `tools map --json -- tests/scripts/test_spec_read.py`, kept to one module so it stays cheap;
  - `tools tests-of scripts/work` and `tools untested --json scripts/spec_read.py`;
  - `features count --by-tag`, `features list --tag @g1` and `features bindings`.

  Each must exit 0 with output. The plan's bare `features count` and `features list` need these flags.

## Files outside P14's list (needed by the sweep)

- `scripts/features`: the generate refusal, and its contract text.
- `scripts/model`: the contract text, which no longer names model_legacy.
- `scripts/model_work.py`: the explicit `@0.29` check.
- `scripts/features_gherkin.py`: the dead code.
- Fixtures moved to codified, because model check and work request no longer read 0.29 files:
  - `tests/scripts/test_model.py` (its builders moved to a new `tests/scripts/model_fixture.py`, for the size limit);
  - `test_model_reading.py`, `test_model_output.py`, `test_model_glossary.py` (rewritten for what v5 reads for words)
    and `test_model_withdrawn.py` (`noqa` only);
  - `test_workqueue_request_asker.py`;
  - the handlers `tests/scenarios/design_model_check_handlers.py` and `_conditions.py`, `requests_handlers.py` and
    `supervision_plans.py`. Their indexes are now codified with the fixture glossary, and their statements parse.
- `agents/bdd-implementer.md` and `skills/bdd-red-green/SKILL.md` no longer name `features retire`.
  `skills/migrating-to-capabilities/SKILL.md` gains a note that the feature-editing commands are gone and their edits
  are made by hand before the 1.0.0 upgrade.

## Checks (all run on gfc/P14, SHOPSYSTEM_GF unset)

- `python3 -m pytest -q tests/scripts/test_tools_codified_smoke.py`: 5 passed.
- `! grep -rn 'model_legacy\|def ears' scripts`: PASS.
- `! grep -n 'feature-formulator' README.md`: PASS.
- `grep -q '"version": "1.0.0"' .claude-plugin/plugin.json`: PASS.
- `python3 scripts/tools check`: exit 0. Run on every changed Python file outside `.shop/`, ruff and vulture are clean.
  With `--base gf-conversion` it also lists `.shop/work/i26/runs/.../mk.py`, a run artifact the reference rewrite
  touched. It is left as it was.
- The CLAUDE.md row loop: no row missing. PASS.
- `! python3 scripts/model check 2>&1 | grep -E '^(v_p[0-9]|v15[g-k]|v_t[4-6]|v_s[1-3]|v15f) '`: PASS.
  - Rows left: v10a 19, v17 24, v_d1 9 and w_uncited_obs 16, as in earlier layers. v3 is gone.
  - Unresolved references fall from about 650 to 34: i57's backlog proposal, decision 0072's capability references,
    and person/record sources.
- Layer 5 gate:
  - `python3 -m pytest -q` (-n 6): 769 passed, 1 skipped, 0 failed.
  - `tools size --limit 300`: exit 0.
  - `model logic`: exit 0, with 7 L2 notes, as at L4.
  - `model restates`: 581 ids, 516 restated, 65 dropped, 0 pending, 0 missing, exit 0.
  - `features generate --check`: exit 0.

## Left undone, and calls made

- **v16a's date cutoff stays.** design-model-check's `unrequested` condition defines it as "dated after 2026-10-23"
  (r14). Dropping the cutoff would contradict the codified spec, and would report every initiative from before
  requests. Changing that is a spec change, for a request.
- **The work run fault P12 found is not fixed.** A refused integrate raise is followed by a failing commit:
  "pathspec .shop/work/i1/runs/i1", in `supervise_rounds.raise_before_merge` and `undo_round`. It is outside P14's
  files and should be raised as a fix with a test. While the suite was red, it surfaced once more, as the failure mode
  of the supervision raising scenario before its upstream was codified.
- The `spec_grammar` helpers are not made public (optional).
- P13's scenarios already use the plugin itself once it is at 1.0.0 (`migration_old.plugin()` returns it), so no
  change was needed there.
- `migrate_session.py` names no formulation, so it is unchanged.

## Module-map rows

Written in CLAUDE.md. The only new module is `tests/scripts/model_fixture.py`, the model tests' file builders, which
the `tests/scripts/` row covers.
