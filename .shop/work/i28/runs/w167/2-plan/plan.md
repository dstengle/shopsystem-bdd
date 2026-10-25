# w167 plan: capability-proposals written from a change list have ids no other initiative's proposal has (supervision#r92)

## 1. What goes green

supervision#r92, two scenarios in features/supervision.feature:

- "an integrate round's change list gives one drafted capability-proposal for each capability it names, with what it adds, changes and removes on that capability": green today (notes §1, run). It must stay green: it asserts file names `.shop/work/i1/thing.md` and `other.md`, kind, status and the three lists, not the id.
- "the change lists of two initiatives that name the same capability give two drafted capability-proposals with different ids": red. Today it stops at a missing step ("an initiative i2 under .shop/work/, proposed, that fulfils the request q2 ..."); the two-initiative change-list Given and both Thens are also undefined; the stand-in `claude` keys a plan by round kind only, so i1's and i2's integrate rounds cannot give different change lists; and once those exist, `write_proposals` writes `capability-proposal/<context path>/thing` for both initiatives (notes probe 1).

No `Retires` section: no deprecated scenario is retired.

## 2. Where the change lands

- `scripts/supervise_change.py`: the id `write_proposals` writes carries the initiative's name (decision 1); the file name stays `<capability>.md`.
- `scripts/supervise_draft.py`: `draft_proposals` recognises a proposal's existing work-items by the proposal's id, not its file stem (decision 2), so the new id does not make it draft a second work-item every run (notes probe 5).
- `tests/scenarios/supervision_integrate_steps.py`: the Given for i2 proposed, fulfilling q2 (its `initiative.md` under `.shop/work/i2/` and the request q2 with line 1 accepted, committed); the Given giving i1's and i2's integrate rounds their own change lists; the Then on each initiative's one drafted proposal for thing and its adds; the Then that the two proposals' ids differ.
- `tests/scripts/stub_claude.py`: a plan key for one round of one node, the round's kind and the name from the brief's `# <kind> of <name>` heading, taking precedence over the kind-only `round:<kind>` key; the module docstring says so. File is at 268 lines: the change must stay within its 32 lines of room.

Removed from the researcher's set: `tests/scenarios/supervision_rounds_steps.py` (263 lines). Its `proposed_fulfilling` stays i1-only; the i2 Given goes in the integrate steps module as the notes suggest, which has room (91 lines), and may reuse that module's helpers rather than widen `proposed_fulfilling`.

Read, not changed: `scripts/supervise_rounds.py` (names proposals by file stem, which is unchanged), `tests/scenarios/supervision_proposal_steps.py`, `tests/scenarios/test_supervision.py` (already star-imports the integrate steps; the implementer confirms the new steps are reached).

## 3. Decisions

1. **The id of a proposal written from a change list is `capability-proposal/<context path>/<initiative>-<capability>`** (e.g. `.../i1-thing`), the context path read from the initiative's id as today and the initiative's name being the name of the initiative the round was for. Rests on supervision#r92 (one proposal per capability per change list; its second scenario pins that two initiatives never share an id), design-decision/capability-ids-are-context-scoped (0027: `<kind>/<context path>/<name>`, a `<name>` matching `[a-z0-9]+(-[a-z0-9]+)*`, which `i1-thing` does) and the naming already used for per-capability proposals of one initiative (design-decision/one-capability-per-proposal, `first-spec-<capability>`; 0050, `migrated-<capability>`). The narrator observes only that the ids differ, which the scenario fixes; the form within 0027 is not a narrator-visible choice between readings.
2. **`draft_proposals` matches a work-item to a proposal by the name segment of the work-item's `part_of` against the name segment of the proposal's id** (the file stem where the proposal has no id), with `under` as today. Rests on supervision#r72 (one work-item per capability a formulated proposal names; the docstring's "a capability that has one already gets none"). Comparing name segments, not full ids, keeps the short form `capability-proposal/p1` that existing fixtures (`supervision_world.py`) and decision 0027 allow in `part_of`.
3. **The stand-in's per-node round key** is a test-harness choice, not behaviour; it rests on nothing in the capability and changes no existing key's meaning.

## 4. Tests the decisions break

None. Verified:
- Decision 1: no test asserts the id of a proposal `write_proposals` writes (search of tests/ for a `thing`/`other` capability-proposal id: no match); scenario A asserts no id (notes §4, run).
- Decision 2: `supervision_proposal_steps.py` `two_drafted` and the fix-now Then assert `part_of` ending `/p1`; the fixture proposal p1 has id `.../p1` and file `p1.md`, so the name segment equals the stem and nothing changes for it. Work-item fixtures with `part_of: capability-proposal/p1` still match p1.
- Decision 3: the kind-only key keeps its meaning and precedence below the new key; no existing plan uses a key with a name.

## 5. Open cases

For the implementer to name in the report, not to settle here:
- D1: a change list naming one capability twice; today the second entry overwrites the first silently (notes probe 3). r92 does not say whether the entries merge or the list is refused.
- D2: a capability name containing `/` (or otherwise not a `<name>`); today an unhandled `FileNotFoundError`, exit 0, initiative left `started` with no proposal (notes probe 4).
- A change list naming a capability spec/ does not hold, or a malformed requirement id: `write_proposals` checks neither (notes §5).
- An initiative whose `initiative.md` has no id: where the context path and the initiative's name then come from.
- Proposals already written under the old id form (`<context path>/<capability>`) in existing initiatives: decision 2 still matches them by stem-equal name; whether they are renamed is not this work-item's.
