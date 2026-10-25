# w167 research: capability-proposals from a change list get distinct ids (supervision#r92)

Method: `tools map` has no map here (`tools tests-of` answers "no map"; not made). Tests are found by search. `tools refs` ran for `entries`, `Changes`, `write_proposals`; `write_proposals` shows 0 refs because `Rounds` calls it as `self.write_proposals` (text search found supervise_rounds.py:108). Probes run with `python3 -m pytest -q -s -n 0` on files in `.shop/scratch/w167-1-research/`.

## 1. Why each accepted scenario is red today

Scenario A, "an integrate round's change list gives one drafted capability-proposal for each capability it names ...": **green today**.
- Run: `python3 -m pytest -q "tests/scenarios/test_supervision.py::test_an_integrate_rounds_change_list_gives_one_drafted_capabilityproposal_for_each_capability_it_names_with_what_it_adds_changes_and_removes_on_that_capability` → 1 passed.
- Its assertions check kind, status and the three lists, not the id. The code path is `supervise_change.py:write_proposals`, called from `supervise_rounds.py:108`.

Scenario B, "the change lists of two initiatives that name the same capability give two drafted capability-proposals with different ids": **red**.
- Run: same node id style, `test_the_change_lists_of_two_initiatives_..._with_different_ids` → `StepDefinitionNotFoundError: Given "an initiative i2 under .shop/work/, proposed, that fulfils the request q2, whose line 1 has the line outcome accepted"` (feature line 1145).
- Missing step definitions (by search, `grep` of tests/): no step for an `i2` proposed fulfilling q2 (`proposed_fulfilling`, supervision_rounds_steps.py:113, writes the fixed `DIR/initiative.md` of i1 only); no step for "the integrate round for i1 gives DONE with a change list that adds thing#r4 on thing, and the integrate round for i2 gives DONE ..." (`integrate_with_changes`, supervision_integrate_steps.py:40, needs ` on other` at the end); no Then for "i1 has one drafted capability-proposal for thing ..." or "the two capability-proposals have different ids".
- Missing in the stand-in: `tests/scripts/stub_claude.py:187` keys a plan by round kind only (`round:` + kind, read from `# <kind> of <name>`), so i1's and i2's integrate rounds cannot get different change lists.
- Missing in code, once the steps exist: `supervise_change.py:47` writes `id: capability-proposal/<context path>/<capability>` with no initiative name. Both initiatives write the same id (probe 1 below). `supervise_change.py:41-42` derive the context prefix from the initiative id.

## 2. What the system answers today (probes)

Probe file: `.shop/scratch/w167-1-research/probe_ids.py` (through `work run`, no initiative, stand-in claude, a scratch repo with a remote, tests.py passing).

Probe 1, two initiatives i1 (q1) and i2 (q2), each change list `adds thing#r4 on thing`: `run`.
- Result: both `.shop/work/i1/thing.md` and `.shop/work/i2/thing.md` carry `id: capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/thing`, `status: formulated`. Same id, exit 0.
- The `measure initiative` refusals on stderr come from the stand-in's session.json having no usage figures: a stand-in artefact, not a product finding.

Probe 2, control: one initiative i1, same change list: `run`. Id `capability-proposal/missingmass.io/shopsystem/shopsystem-bdd/thing`, formulated, exit 0.

Probe 3, one initiative whose list names `thing` twice (`adds thing#r4`, then `changes thing#r2`): `run`.
- Result: `thing.md` has `adds: []`, `changes: [thing#r2]`. The first entry is overwritten silently. Exit 0. See defect D1.

Probe 4, capability named `other/x`: `run`.
- Result: `FileNotFoundError: .../.shop/work/i1/other/x.md`, traceback on stderr, exit 0; the initiative is committed `proposed -> started` and no proposal is written. See D2.

Probe 5 (`probe_have.py`), a hand-written formulated proposal `thing.md` whose id is `capability-proposal/.../i1-thing` (the id form the fix would need), initiative started, `work run i1` twice: `run`.
- Result: `work add: i1/w1 drafted` and `work add: i1/w2 drafted`. Two work-items for one capability. See part 3, row 2.

Nearest cases not probed: a change list naming a capability that spec/ does not hold (read: `write_proposals` checks nothing against spec/); a requirement id that is malformed (read: `entries` only checks strings).

## 3. Old assumptions

The old form: a proposal's id is `capability-proposal/<context>/<capability>`, its file name is the capability, and the work-item drafter treats the two as one.

| place (file:function) | what it does today | what the requirement makes of it | tests that execute it | found by |
|---|---|---|---|---|
| supervise_change.py:write_proposals, line 47 | id = `<context>/<capability>`, no initiative name | must differ between initiatives: id must carry the initiative (e.g. `<capability-proposal>/<context>/<initiative>-<capability>`, the form decision 0029 gives: `first-spec-<capability>`) | by search: test_supervision.py, the two r92 scenarios (A passes, B red); none asserts the id today | read; probe 1 |
| supervise_draft.py:draft_proposals, line 40 | `have` keys work-items by the last segment of `part_of` and compares it with the proposal's file stem | with the new id, last segment is `<initiative>-<capability>`, never the stem, so no work-item is ever seen as drafted: a second one per run | none found: no scenario asserts that a capability with a work-item gets no second one (by search, features/supervision.feature) | read; probe 5 shows duplicates |
| supervise_draft.py:draft_proposals, line 53 | `part_of` = `data.get("id", name)`, the full id | unchanged, but the id it carries changes | by search: supervision_proposal_steps.py `two_drafted` (fixture p1 only) | read |
| supervise_draft.py:fix_work_item, line 78 | copies `part_of` of the work-item it fixes | unchanged | none found (by search) | read |
| supervise_change.py, lines 41-42 | context prefix of the id taken from initiative.md's id | the initiative's own name must also be read (initiative.md id or `self.dir.name`) | by search: scenario A | read |
| supervise_change.py, line 45 | one file per list entry, `<capability>.md`; a repeated capability overwrites | r92: one proposal per capability; a repeat must be merged or refused | none (no test names a repeated capability) | probe 3 (D1) |
| supervise_change.py, line 45 | a capability with `/` makes a path outside the initiative's directory | none stated; the id would be malformed (decision 0027: `<name>` is `[a-z0-9]+(-[a-z0-9]+)*`) | none | probe 4 (D2) |
| model.lp:211 (v_b1) | a work-item's `part_of` must name a node of kind capability-proposal | ids must stay unique across the context; two nodes with one id resolve to both | none run (`model` check not run) | read |
| supervise_rounds.py:22-29 `proposals()` | names proposals by file stem, not id | unchanged: the stem stays the capability name | by search: test_supervision.py gate/apply scenarios | read |
| supervise_answers.py:49-53 | selects by `kind`, not id | unchanged | none found | read |

## 4. Tests the requirement makes impossible to keep

`tools tests-of` has no map, so every list here is `by search`.
- tests/scenarios/supervision_integrate_steps.py `proposals_written` (the step behind scenario A): asserts file names, kind, status and the three lists; not the id. Keeps passing: verified by run.
- tests/scenarios/supervision_proposal_steps.py:63 `two_drafted`: asserts each drafted work-item's `part_of` ends `/p1` (the fixture id). Unaffected by the change to write_proposals; it breaks only if draft_proposals changes the `part_of` it writes.
- No test asserts that a second integrate round of another initiative gives the same id, so none can be made impossible to keep except through the draft check (table row 2), which no test covers.
- Found sound: scenario A (run, passes); the `entries` form checks (read: supervise_change.py:13-32, BadChanges cases are covered by the r96 scenarios by search, not run here).

## 5. A step the work-item skips

Existing way: a proposal is written by `work add` or the gate/apply rounds through workqueue functions, which validate the node. The integrate path writes the file itself (supervise_change.py:45-51) and commits it (`self.commit(... also=...)`, supervise_rounds.py:108-109).
- read: no check that the capability exists under spec/capabilities/, that the requirement ids named are well formed or exist, or that a name is a valid `<name>`. The model check (`scripts/model`) would find these later, not `work run`.
- read: no uniqueness check on the id before the write (the step that would catch probe 1).
- run (probe 3, 4): the effects the existing way does not produce: a silently lost entry (D1) and a traceback with exit 0 leaving the initiative `started` (D2).

## 6. Defects

D1. A change list naming one capability twice keeps only the second entry.
- `.shop/scratch/w167-1-research/probe_ids.py::test_one_initiative_same_capability_twice_in_list`: change list `[{"capability":"thing","adds":["thing#r4"]}, {"capability":"thing","changes":["thing#r2"]}]`, `work run`.
- Came back: exit 0; `.shop/work/i1/thing.md` has `adds: []`, `changes: [thing#r2]`.

D2. A capability name with `/` ends `work run` with an unhandled traceback.
- `probe_ids.py::test_one_initiative_capability_with_slash`: change list naming `other/x`, `work run`.
- Came back: `FileNotFoundError: ... .shop/work/i1/other/x.md` from supervise_change.py:47; exit 0; log's last commit `proposed -> started`; no proposal; no round commit. r96-style error naming the round is not given.

D3 (the r92 defect, scenario B): two initiatives naming one capability write one id. Probe 1 above.

## 7. The file set

Changes needed for the scenarios and what passes today:
- scripts/supervise_change.py (52 lines; room 248) — id on line 47 gets the initiative's name, prefix read from initiative (lines 41-42); reject or merge a repeated capability (D1) and a `/` name (D2) if in scope. Shown by: read, probes 1, 3, 4.
- scripts/supervise_draft.py (81; room 219) — `have` (line 40) must match on the proposal's id rather than its file stem, else duplicate drafting (probe 5). Shown by: read, probe 5.
- tests/scenarios/supervision_integrate_steps.py (91; room 209) — steps for i2 proposed fulfilling q2, two-initiative change-list Given, the two Thens. Shown by: search (step grep, run of scenario B).
- tests/scripts/stub_claude.py (268; room 32) — plan key per initiative for `round:integrate` (line 187), or a per-initiative key in the steps. Shown by: read of lines 9-12, 187.
- tests/scenarios/supervision_rounds_steps.py (263; room 37) — `proposed_fulfilling` writes only `i1`'s initiative.md (line 113-122). Put the i2 variant in supervision_integrate_steps.py instead to keep room. Shown by: read.

Read, not changed: scripts/supervise_rounds.py (134; room 166; calls write_proposals at 108, names by stem); scripts/supervise.py (248; room 52); scripts/workqueue.py (290; room 10; used by draft via workqueue.add); scripts/model.lp (not sized); tests/scenarios/supervision_proposal_steps.py (82; room 218; asserts `/p1`); tests/scenarios/test_supervision.py (258; room 42; star-imports the integrate steps); scripts/work (151); scripts/supervise_worker.py (247; room 53).

Size: every file on the path is under 300. `scripts/workqueue.py` (290) and `tests/scenarios/supervision_rounds_steps.py` (263, 37 room) are the tight ones; `tests/scripts/stub_claude.py` is 268.
