# Research: migrate-kb (migration-tools r1-r17)

Method: `tools refs` for names (no `tools map`, so `tests-of`/`untested` say "no map"; tests are listed by search, marked `by search`). `refs` skips `scripts/migrate` (no `.py`): its callers were read by hand. No CLAUDE.md in the checkout; the size limit is the work-item's "under 300 lines" (the one stated). Probes in `.shop/scratch/migrate-kb-1-research/` (ignored by git).

Probe commands used:
- `python3 -m pytest -q -s -p no:cacheprovider .shop/scratch/migrate-kb-1-research/probe_migrate.py` (p01-p28; `-k pNN` for one) — run
- `python3 -m pytest -q -s -p no:cacheprovider .shop/scratch/migrate-kb-1-research/probe_migrate2.py` (p29) — run
- Red scenarios: `python3 -m pytest -q --tb=line -p no:cacheprovider tests/scenarios/test_migration_tools.py` → 22 failed, 16 passed — run

## 1. Why each scenario is red today

Test ids are `tests/scenarios/test_migration_tools.py::test_...`. Red = 22; passing = 16 (r1 x2, r2 x5, r3, r4, r5, r7 x4, r10).

Undefined step = the feature's wording has no step definition (`StepDefinitionNotFoundError`), so the scenario never reaches its code. Each red scenario's code cause is in part 2.

- r2 supersedes / status superseded: undefined Then "spec/decisions/0007-a.md's status is accepted"; also `decision_text` hard-codes `status: accepted` (`scripts/migrate_ledger.py:64-76`), so 0003-b is never superseded (p01).
- r17 qualified supersedes: undefined Given "the entry 0007-a's source is alice and its supersedes is decision/0003-b (for artifacts)"; code: raw qualified `supersedes` (`migrate_ledger.py:70-71`, p02).
- r11 "its entries": Given "nothing but the entry" only sets `context["entry"]` (`migration_ledger_steps.py:7-9`); the next Given reads `context["ledger"]` → `KeyError: 'ledger'` (`migration_ledger_steps.py:117-119`). Test-side defect; the code passes (p03b).
- r11 "title and its entries": Given text "starts with the title" does not match the feature's "has the title ... and a blank line" → undefined. Code passes (p03).
- r13 x2: Given "has, in order, the entries ..." undefined (the ledger regex takes one entry only). Code refuses unnumbered headings (`migrate_ledger.py:7,18-27`, p04, p05).
- r7 "would land on" x4: Given "has, in order, the entries ..., and <there>" undefined (`migration_ledger_steps.py:47-49` takes one entry only); row 4 also needs r13. Code refuses correctly for rows 1-3 (p06-p08), row 4 refuses on the unnumbered `## decision/b` (p09).
- r6 model check x4: row 1 Given undefined; row 2 (`formulated_as`) Given undefined; row 3 (`capability/thing`) Given undefined; row 4 Given undefined. The Then "it reports no unresolved reference and no file problem" is not defined either (`migration_spec_steps.py:150` says "no violation, no unresolved reference and no file problem"). Code: row 1 already passes (p12); row 2 keeps `formulated_as` (`migrate_spec.py` never removes it; `scripts/model:550-552` reports it, p13); row 3 keeps `capability/thing` (`with_id` keeps an existing id, p14); row 4 leaves a qualifier unresolved (p15). Rows 2-4 also report `spec/index.md is missing` (p13b), and their Givens create no `spec/index.md` (see part 4, conflict C2).
- r8 plans/specs/requests: undefined Given (adds `docs/superpowers/requests/q1.md`); code: `DIRECTORY_MOVES` has no requests entry (`migrate_layout.py:8-14`, p16).
- r14 adrs: undefined Given "with adrs/0001-use-x.md"; code: no `adrs/` move (p18).
- r9 kinds: undefined Given "it has docs/superpowers/plans/p1.md, docs/superpowers/requests/q1.md, ... adrs/0001-use-x.md ..."; code: ids right for plan, design note, log, decision, capability (p17), but the ADR does not move, so no `decision-argument` id.
- r9 short form: undefined Given "a capability ... whose id is capability/thing"; code: `with_id` leaves it (`migrate_layout.py:59-60`, p14).
- r12 about: undefined Given "none with an about" (with requests and adrs); code: abouts right for plan/design/log (p17); no ADR/request.
- r15 x2: undefined Givens "a tracked README.md changed since the last commit" and "an untracked notes/n2.md"; code: no dirty check, so the run proceeds (p19, p20).
- r16: undefined Given "its spec/decisions.md has nothing but the entry"; code: `write()` never stages written texts and writes no index (`migrate_layout.py:124-138`, p22).

Passing (16, `run`): r1 moves x2, r2 entry/first paragraph/date-source/whole-text/outline x3, r3 holding, r4 index, r5 rewrite, r7 two changes, r7 untracked w2, r7 ledger text x2, r10 numbering.

## 2. What the system answers today

Each probe is `run` from the commands above; rc = exit code.

- p01 r2 supersedes: rc 0. 0007-a gets `supersedes: design-decision/.../b` and `revisit_when`; 0003-b's `status` is `accepted` (should be superseded).
- p02 r17 qualified: rc 0; `supersedes: decision/0003-b (for artifacts)` (raw, not an id); `by: "alice"` with no qualifier.
- p03 r11 title+entries: rc 0; ledger gone; title dropped; 0007-a has its summary and `by`.
- p03b r11 entries only: rc 0; ledger gone.
- p04 r13 among numbered (`0007-a`, `b`, `0003-c`, `d`): rc 1; refuses naming `## decision/b` and `## decision/d` ("its heading is not `## decision/<nnnn>-<slug>`"); nothing changed.
- p05 r13 no numbered (`b`, `d`): rc 1; same refusal.
- p06 r7 `decisions/0007-a.md` moves onto the new file: rc 1, "could not write spec/decisions/0007-a.md for the ledger entry ...: decisions/0007-a.md moves there"; tree unchanged.
- p07 tracked `spec/decisions/0007-a.md`: rc 1, "a file is there".
- p08 untracked `spec/decisions/0007-a.md`: rc 1, "a file is there"; `git status` shows `?? spec/decisions/` (already dirty).
- p09 `decisions/0008-b.md` + unnumbered `## decision/b`: rc 1, refuses on `## decision/b`.
- p10 text before entries: rc 1, named.
- p11 same entry twice: rc 1, named.
- p12 r6 row 1 (full example with requests and adrs): rc 0; model check reports no violation, unresolved or problem. Requests and `adrs/` are NOT moved (r8, r14 unmet) and the model does not read them.
- p13 r6 row 2 (`formulated_as`): rc 0; `formulated_as: features/thing.feature` kept; model check reports `formulated_as is not read` and `spec/index.md is missing`.
- p13b (no `formulated_as`): model check still reports `spec/index.md is missing`.
- p14 r9 short id `capability/thing`: rc 0; id kept as `capability/thing`; model check: only the index problem.
- p15 r6 row 4 qualified supersedes: rc 0; model check: `decision/0003-b (for artifacts) is not a design-decision` (unresolved) and the index problem.
- p16 r8: rc 0; `docs/superpowers/requests/q1.md` stays; plan `RM` (id written but unstaged).
- p17 r9/r12: rc 0; plan `initiative-archive/.../p1`, design note `decision-argument/.../s1`, log `measurement/.../run1-test-log`, decision `design-decision/.../a`, capability `capability/.../thing`; each moved record `about: bounded-context/...`. `adrs/0001-use-x.md` stays.
- p18 r14: rc 0; `adrs/0001-use-x.md` stays, no git change.
- p19 r15 tracked README changed: rc 0; migrates anyway (`R work/...`, ` M README.md`).
- p20 r15 untracked `notes/n2.md`: rc 0; migrates anyway.
- p21 r7 untracked `.shop/work/i1/w2.md` (tree dirty): rc 1; "could not move work/i1/w2.md onto .shop/work/i1/w2.md"; the untracked file is not named as uncommitted.
- p22 r16: rc 0; `R work/...` staged, `D spec/decisions.md` staged, `?? spec/` (the decision file untracked); `spec/decisions/index.md` not written.
- p23 nearest, no ledger and no decisions: rc 0; only the work move.
- p24 nearest, `--context shop` (not owner/product/context): rc 0; writes `capability/shop/thing` and `bounded-context/shop`; no refusal.
- p25 nearest, `retired: [rx]`: rc 1; traceback `ValueError: invalid literal for int()` at `migrate_spec.py:39`; nothing changed.
- p26 nearest, second run on an uncommitted migrated tree: rc 0 both; second run is a no-op; no dirty refusal.
- p27 r3 `@r1 @holding`: rc 0; becomes `@r1 @deprecated`, title `s1 (deprecated)`, `Deprecated for: removal`; no `@holding` left.
- p28 nearest, entry with no date or source: rc 0; `date: ` (empty) and `by: ""`.
- p29 r3 refusals (probe2): `@holding @deprecated` s1 and a twice-titled s2: rc 1, "could not deprecate 's1' ...: 's1' is already deprecated" and "... has the title 's2' twice" (named twice); nothing changed. `features deprecate` run directly on the same file gives the same two refusals (rc 1).

## 3. Old assumptions

No `CLAUDE.md`; `refs` counts are its own. "tests executing" = by search (no map), by name in the test modules; `none` = searched, none.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| migrate_layout.py:with_id (52) | keeps an existing `id:`, returns text unchanged | r9: a short capability id must be rewritten; r4 rewrites `spec/index.md` id | by search: test_run_gives_specindexmd (r4), test_run_moves_decisions (r1, decision keeps id), test_run_numbers_each_behaviour (r10 via plan_capabilities); r9 red | refs: layout 87, 91; spec 40, 80 |
| migrate_layout.py:record_kind (67) | kinds only for `.shop/records/archive/plans`, `design-notes`, `*-test-log.md` | r9/r14: ADR under `.shop/records/decision-arguments/` gets `decision-argument` | tests/scripts/test_migrate_layout.py:26,29,30,31 (refs); by search: test_run_gives_a_capability... (red) | refs: layout 85; tests 26-31 |
| migrate_layout.py:DIRECTORY_MOVES (8-14), destination (38) | moves decisions, work, plans, specs, records | r8 adds `docs/superpowers/requests/` → `.shop/records/archive/requests/`; r14 adds `adrs/` → `.shop/records/decision-arguments/` | by search: test_run_moves_decisions (r1, passes; no requests/adrs); r8/r14 red | refs: destination 47 |
| migrate_ledger.py:ENTRY regex (7), ledger_entries (11) | `## decision/<nnnn>-<slug>` only; any other heading refused | r13: an unnumbered `## decision/<slug>` is numbered from one above the highest | by search: test_run_replaces… (r2), test_run_ends… (r2), test_run_writes… outline (r2), test_run_puts… (r2), test_run_gives… (r2 supersedes, red), r11, r13 (red), r7 ledger rows (passing 2) | refs: ledger_entries 82 |
| migrate_ledger.py:decision_text (64) | status always `accepted`; supersedes via `plan.renamed.get(value, value)`; by = source | r2: status superseded when another entry supersedes it; r17: supersedes keeps id alone, qualifier to `by` | by search: test_run_replaces… (r2, status accepted, passes), test_run_writes… outline (passes), test_run_gives… (r2, red), test_run_writes_a_qualified… (r17, red) | refs: decision_text 88 |
| migrate_ledger.py:plan_ledger (79) and plan.renamed (layout 26) | renamed map from ledger entries only | r17 qualified id is not in the map, so it is written raw; r5 for renamed capability ids (r9) would need the same map | by search: test_run_gives… (r2 red), test_run_writes_a_qualified… (r17 red), test_run_after_run… (r6 row 4 red) | refs: plan_ledger 0 (called from scripts/migrate:21, by hand) |
| migrate_layout.py:write (124) | `git mv` moves and `git rm` ledger, then writes texts; no `git add` for texts; no index | r16: every written or moved file added to git; `spec/decisions/index.md` written with `model decisions` | by search: test_run_adds… (r16 red); r1 git status test (R x3, passes, unaffected) | refs: write 0 production (called from scripts/migrate:33) |
| migrate_layout.py:check_moves (105) | refuses moves/writes onto present or moved files (tracked or not), reports all failures | r15: dirty tree refused before this; r7 untracked-move case (p21) reads as a dirty tree | by search: test_run_that_would_move… (r7 untracked, passes today), test_run_that_cannot_make… (r7, passes), r7 ledger rows | refs: check_moves 0 (called from scripts/migrate:27, by hand) |
| migrate_layout.py:tracked (33) | `git ls-files`; the only view of the tree migrate reads | r15 needs `git status --porcelain`: a new check with no caller yet | by search: every migrate test (through migrate_layout.plan_moves) | refs: tracked 9 (layout 46, 108; ledger 4, 80; spec 10, 35, 59, 79, 114) |
| migrate_spec.py:number_behaviour retired parse (39) | `int(str(r).lstrip("r"))` on each retired entry | none in the accepted set; a malformed `retired` crashes instead of being named (p25) | by search: test_run_numbers_each_behaviour (r10, passes); no test with a malformed retired | refs: number_behaviour 40 |
| migrate_spec.py:rewrite_text (86) and plan.renamed (decisions only) | rewrites paths, links and decision ids in frontmatter | r5 with r9: a changed capability id (`capability/thing` → full) needs rewriting in references; `plan.renamed` has decision ids only | by search: test_run_rewrites… (r5, passes; decisions only) | refs: rewrite_text 122 |
| migrate_spec.py:plan_capabilities (33) | id and Behaviour numbering; no `formulated_as` handling | r6 row 2: remove `formulated_as` (model reports it, scripts/model:550-552) | by search: test_run_numbers… (r10), test_run_gives_a_capability… (r9, red); tests/scenarios/test_design_model_check.py:213-215 assert the model's report (model unchanged) — sound | by search (migrate_spec.py) |
| migrate_spec.py:plan_index (80) | id only when `spec/index.md` is tracked; no index otherwise | r6 rows 2-4 Givens create no `spec/index.md`, and the model reports it missing (p13b) — conflict C2 | by search: test_run_gives_specindexmd (r4, passes) | refs: plan_index 0 (called by hand) |
| scripts/model:OLD_LAYOUT (119) and read_decisions (610-631) | reads `supersedes` as bare ids; reports spec/decisions.md, decisions/, work/, records/ as file problems | migrate must leave no qualifier (r17) and no old layout (r6); model itself unchanged | by search: tests/scenarios/test_design_model_check.py (r61 cases, 653-655; supersedes 728) — sound | by search (scripts/model) |
| scripts/model:render_decisions (944), cmd_decisions (967) | `model decisions` writes `spec/decisions/index.md` from files on disk | r16: migrate must write the index after its decision files exist; no caller in migrate | by search: tests/scenarios/test_design_model_check.py:745-768, 1216 (model's own) | by search (grep "render_decisions\|decisions/index") |

## 4. Tests the requirements make impossible to keep

`tests-of` has no map, so these are by search over `tests/`. Checked and sound: test_migrate_layout.py (4 tests: record_kind and plan_ids; a new decision-arguments branch keeps them); test_migration_tools.py r1 (decision id already set; `R` count stays 3 after r16 staging); r2 'status accepted' Then (no entry superseded there); r3 (copy comparison unchanged); r4; r10; r7 two-changes (the second Given commits, so the tree is clean under r15); the 'about' Then step.

Impossible or conflicting as written:

- C1 test_migration_tools.py::test_run_that_would_move_a_file_onto_an_untracked_file_names_the_move_exits_nonzero_and_changes_no_file (passes today). Its Given (migration_old.py:38-41, `untracked`) leaves the tree dirty, so r15 refuses before the move check; its Then wants "could not move work/i1/w2.md onto .shop/work/i1/w2.md". Keeps only if the refusal prints both the dirt and the move failure. Reads: A) r15 refusal alone → test fails. B) both messages → test passes.
- C1' migration_ledger_steps.py:47-59, the "an untracked spec/decisions/0007-a.md" row (red, undefined step). Same conflict: refusal for dirt vs "could not write ... for the ledger entry".
- C2 test_migration_tools.py r6 rows 2-4 (migration_spec_steps.py:139-154): Givens create no `spec/index.md`; the model reports it missing (scripts/model file problem; test_design_model_check.py:202-203 treats it as one). r4 only gives an id to an existing index. Reads: A) migrate creates `spec/index.md` when absent (not in any requirement). B) the Givens get a `spec/index.md` (test-side change). Both needed for rows 2-4 to pass.
- C3 Labels: the work-item says "(r7)" for the dirty-tree refusal (spec: r15), "(r6)" for `formulated_as` and the decisions index (spec: r16 for the index; `formulated_as` has no own requirement, r6 implies it), "(r2)" for the qualifier (spec: r17). The spec text is taken as the authority here.
- Step-text mismatches (not impossible, but red for wording): migration_spec_steps.py:150 "no violation, ..." vs the feature's "no unresolved reference and no file problem"; migration_ledger_steps.py:111 "starts with the title" vs the feature's "has the title".

## 5. A stage the work-item skips

- r16 staging. The existing moves are staged by `git mv` and the ledger by `git rm` (migrate_layout.py:128, 135). The written texts (ids, decision files) are never staged: p16 `RM`, p22 `?? spec/`. Effect only a `git add` produces: index state. Shown by p16 and p22 (run).
- r3 deprecate stage. `features deprecate` runs in a copy (migrate_spec.py:66-75) and its `write_checked` validates that each file parses before writing (`scripts/features:273-280`). migrate then writes the file itself through `drop_holding` (migrate_spec.py:44-51, 75) with no parse. Read; no probe shows a parse failure. The refusals `features deprecate` gives (already deprecated, title twice) are reached and shown by migrate (p29, run).
- r16 index. The existing way to write the index is `model decisions` (`scripts/model:967-980`), which reads the decision files on disk; migrate's plan is in memory, so the index must be written after the decision files exist. Read.
- r15 dirty-tree refusal. A new stage before planning; no existing migrate stage counterpart (check_moves is r7). Shown absent by p19, p20 (run).

## 6. Defects

Each is a probe of today's behaviour on a requirement-free or existing line.

D1 A dirty tree is not refused (should be refused, r15): probe p19, p20, p26 — `python3 -m pytest -q -s -p no:cacheprovider .shop/scratch/migrate-kb-1-research/probe_migrate.py -k "p19 or p20 or p26"`. rc 0 each; the tracked change and untracked file are left, the work file is moved.

D2 `retired: [rx]` crashes with a traceback (should be a named refusal, r7): p25 — rc 1, `ValueError: invalid literal for int() with base 10: 'x'` at `scripts/migrate_spec.py:39`; nothing changed.

D3 A qualified `supersedes` is written raw, and the model reports it unresolved: p02, p15 — `supersedes: decision/0003-b (for artifacts)`; `model check` → unresolved `decision/0003-b (for artifacts) is not a design-decision`.

D4 A malformed `--context` is accepted: p24 — `--context shop` gives `capability/shop/thing` and `bounded-context/shop`; rc 0.

D5 The superseded entry's status is not superseded: p01 — 0003-b `status: accepted` after 0007-a supersedes it.

D6 An entry with no date or source writes empty fields: p28 — `date: ` and `by: ""`; rc 0.

D7 A short capability id is kept (r9's trial defect): p14 — `id: capability/thing`; rc 0.

D8 Written texts stay unstaged and the index is missing (r16): p16, p22 — `RM`, `?? spec/`; no `spec/decisions/index.md`.

## 7. The file set

Production:
- scripts/migrate — cmd_run: dirty-tree check before planning (r15); call the index write after `write()` (r16). Found: read of `scripts/migrate`.
- scripts/migrate_layout.py — DIRECTORY_MOVES + requests (r8), adrs (r14); record_kind for decision-arguments (r9); with_id rewrites a short capability id (r9); write() stages written files (r16); tracked-tree helper for `git status` (r15). Found: read; refs (with_id, record_kind, tracked, destination, write).
- scripts/migrate_ledger.py — numbering of unnumbered entries (r13: ENTRY regex, ledger_entries); status superseded (r2); qualifier split into `supersedes` and `by` (r17) and the renamed map used for qualified ids. Found: read; refs (ledger_entries, decision_text, quoted).
- scripts/migrate_spec.py — formulated_as removal (r6); capability id rewrite into the renamed map (r5 with r9); spec/index.md creation when absent (only if C2 reading A). Found: read; refs (rewrite_text, number_behaviour, plan_index).
- Retired-parse crash (D2) is in this module; not an accepted scenario, so the plan decides.

Tests (scenario steps; the feature file stays as it is):
- tests/scenarios/test_migration_tools.py — 153 lines; new Then steps for r8, r14, r9 about, r15, r16 and the r2 status Then (undefined today). Found: `--collect-only`, red run.
- tests/scenarios/migration_ledger_steps.py — 140 lines; undefined Givens: "has, in order, the entries ..." (r13 rows and r7 'there' rows), title wording (`:111`), r17 "source is alice and its supersedes", the "nothing but" miswiring (`:7-9`, KeyError `:117-119`). Found: red run.
- tests/scenarios/migration_spec_steps.py — 176 lines; undefined Givens for requests, adrs, `capability/thing`, `formulated_as`, README/notes dirty states; Then wording (`:150`). Found: red run.
- tests/scenarios/migration_old.py — 76 lines; `untracked` (C1) and possibly a `spec/index.md` helper (C2). Found: read; by search (migrate tests).
- tests/scripts/test_migrate_layout.py — keep passing; add an ADR record_kind case if r14 goes through record_kind. Found: refs (record_kind).

Modules on the change's path, edited or not (line count; room under the 300-line limit in the work-item, since no CLAUDE.md states one):
- scripts/migrate — 47 lines; room 253 (edited)
- scripts/migrate_layout.py — 138 lines; room 162 (edited)
- scripts/migrate_ledger.py — 89 lines; room 211 (edited)
- scripts/migrate_spec.py — 124 lines; room 176 (edited)
- scripts/model — 1035 lines; room −735, over the limit (loaded by path by migrate's `load_model`; read only)
- scripts/features — 657 lines; room −357, over the limit (run by migrate for @holding; read only)
- tests/scenarios/test_migration_tools.py — 153 lines; room 147 (edited)
- tests/scenarios/migration_ledger_steps.py — 140 lines; room 160 (edited)
- tests/scenarios/migration_spec_steps.py — 176 lines; room 124 (edited)
- tests/scenarios/migration_old.py — 76 lines; room 224 (edited, maybe)
- tests/scripts/test_migrate_layout.py — 42 lines; room 258 (maybe edited)

Workspace note: running the scripts wrote `__pycache__/` under `scripts/` and `tests/`; these are ignored by `.gitignore`.
