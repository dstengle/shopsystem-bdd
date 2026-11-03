---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-gate-r2-l3
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: done
---

# The GF conversion, revision 2: the layer 3 gate

**Passed.** On `gf-conversion`, after the layer 2 gate (`gate-r2-L2.md`, 3590bd9f).

## Merges

`gfr/R6` (cd00b9a6; 9bfdd47b, 42e08f36, 7d9d0184, cd00b9a6) and `gfr/R7` (b83cd1b7), in plan order, `--no-ff`. No
conflicts: the packages own disjoint files.

## Shared changes made by the gate

1. **`spec_tree.guard`'s relation rule deleted** (R6's ask). The rule dropped an `SAtom` over `rel_*_Atom`, kept
   only for the relation `_Given` fun R6 deleted; the wrapper in `features_vocab._guard` that stepped past it is
   gone too. Test first: `test_spec_tree.py`'s relation test now asserts the guard keeps a relation step as its
   row's clause (it was red against the rule).
2. **Relation entries as rows** (R5's ask 1, through R6). The 8 relation entries became `## Relations` rows:
   fulfils (`one`), adds, blocked by, on, for, with and proposed in (`one`) in `spec/index.md`; kept in (`one`) in
   work-queue's table. Supervision's 3 `on` entries are deleted (the index's `question on node` row covers them).
   The cardinalities are the entries' own words ("exactly one", a line of one request, a file in one directory).
   - `model lexicon --check`: 337 terms, 9 problems -> **326 terms, 0 problems**;
   - `features vocab --check`: "every step has one handler";
   - `model check --json` and `model logic --json` byte-identical before and after.
3. **The fixture glossary** (`tests/scripts/fixtures/glossary/spec/index.md`, the layer 1 plan amendment). Its 26
   relation entries are a `## Relations` table before the Glossary (so tests that add entries under `## Glossary`
   still land in it), and its 6 `Means:` conditions are glosses (primitive; R2 had stopped reading `Means:`, so no
   reading changes). `model --root <fixture> lexicon --check`: 154 terms, 24 problems -> 128 terms, 0 problems.
   `test_model_spec_terms.py` replaced the old `Means:` line, so its two tests now name the new text (the first went
   red on the fixture change and is green again). The supervision corpus check against the fixture still exits 0.
4. **R7's wording of `features generate` checked against R6** (R7's ask 2). One mismatch: R7 (after design-r2 §7.1)
   wrote that a group whose trace cannot happen is refused, exit 1; R6 ships a group with no trace to read (its L1,
   an undetermined trace, a step with no template) left out with a stderr line, exit 0. The gate keeps R6's
   behaviour: it is what lets the plan's own accept (`generate --preview` on the live supervision, with R4's 8 real
   L1s, exits 0) and this gate's `--check` run; it gives the rule one owner as for v15m (`model logic`'s L1); and
   `model check` already reports a group with no scenario (`v_s3` in `model.lp`), so a formulate round still fails
   on it. Reworded: `docs/capability-format.md` (The feature file), `docs/design-model/grammar.md` (§7) and
   `skills/formulating-features/SKILL.md` (When generation refuses). Exit 1 stays for a requirement that does not
   parse and an example line the step grammar refuses. Note: grammar.md's own rule listing numbers that rule
   `v_s2`, `model.lp` numbers it `v_s3` (an older drift, left to R14).
5. **The allowance shrinks** from 20 ids to 1: `test_e2e_codified.py`'s test (its fixture is still the old format:
   v15l and v15m on its work-queue g1, g2; layer 4/R14).
6. **Package reports.** `report-R6.md` and `report-R7.md` could not be written: the harness refused the write from
   this gate session too ("Subagents should return findings as text"). Their content was returned to the
   orchestrator with this gate's result; the main session writes them. The parts the later layers need are here:
   - R6's module-map rows for R14: `spec_trace.py` (a group's cone, an optN solve projected on its labels and
     state-0 fluents, groups solved side by side, labels read into Givens, When and Thens), `spec_trace_steps.py`
     (the atom table, instances named in order of first mention), `features_vocab_gf.py` (the generated StepsTyped
     module). R7 added no module.
   - R6's ask for R14 / `background.lp`'s owner: the `#minimize` counts an instance once per state it is used in,
     so the least trace prefers things first used late (Givens like "an initiative i1 that is `abandoned`" for the
     work run initiative; Thens on an instance no Given names, e.g. supervision g1's "the work-item w2 is `green`").
     Counting `ever(X)` once and minimising fluents created after state 0 would read closer to the spec; the
     generator needs no change.
   - R6's calls: optN projected onto what the reader reads (`--project`, `seen/3`, `init/1`; 18–36 models where
     the full enumeration exceeds 10 000); labels `no(i)` and `mod(0,j)` (R4's names); a relation step is its row's
     `SAtom`, read as GivenR/ThenR keyed by the row's word; supervision g3 gives a scenario with no Then.

## The gate's checks

| Check | Result |
|---|---|
| layer tests (`test_spec_trace`, `test_features_generate`, `test_features_vocab`, `test_spec_tree`) | 54 passed |
| `tools size --limit 300` | exit 0 |
| full suite | 1 failed (`test_e2e_codified`), 835 passed, 1 skipped |
| common check against `baseline-failures.txt` + `gate-r2-L1-allowed.txt` (1 id) | prints nothing |
| scenario suite (`tests/scenarios`, checked-in features) | 300 passed |
| `features generate --check` | exit 1, no traceback, 31 s: 8 features differ (analysis-tools, batch-measurement, design-model-check, feature-file-tools, migration-tools, requests, supervision, work-queue); 337 non-example given lines left out with a stderr line; 8 groups with no scenario (supervision g2, g6, g34, g35, g40, g42, g50, g51: R4's real L1s) |
| `model lexicon --check` | 326 terms, 0 problems |
| `features vocab --check` | every step has one handler |
| `model check --json`, `model logic --json` | byte-identical before and after change 2 (logic 26 s) |
| R6's greps (`def choose\|def resolve\|def precondition\|.means`; `import spec_tree\|import spec_grammar` in spec_trace) | nothing |
| `wc -l scripts/features_generate.py` | 112 |
| R7's greps (`Means:` in docs/skills/agents; "one shall" in grammar.md; `## Relations`, "example data" in capability-format.md) | pass |
| `test_agents.py` | 15 passed |
| `unparsed.sh \| comm -13 unparsed-L1.txt -` | nothing |
| supervision corpus, `model --root tests/scripts/fixtures/glossary parse --file` | exit 0 |
| `tools check` on the changed and new scripts and tests | clean |

## Left for layer 4 and R14

- The 8 differing features are regenerated by R8–R13; R4's 8 supervision L1s go when R8 moves the given-block
  conditions into the statements.
- `test_e2e_codified` (the only allowed id) must pass by the layer 4 gate.
- R14: the module-map rows above (with R4's in `report-R4.md`), the `background.lp` minimisation ask, the v_s2/v_s3
  numbering in grammar.md, `SCommits`/`ThenCommits`.
