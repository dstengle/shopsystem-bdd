---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-plan-r2
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# The GF conversion, revision 2: the build plan

This plan builds `design-r2.md`. Every package reads `revision-brief.md`, `design-r2.md` and `brief.md` first, and
`design.md` only where design-r2 points to it. There are **14 packages in 5 layers**, after a layer 0 of
baselines that the orchestrator takes. Design-r2 §13 lists the calls made in the builder check; each package carries
the ones its section names. The packages of one layer own
disjoint files, so each runs in its own worktree off `gf-conversion`. A layer starts only once the layer before it is
merged and its gate has passed. All judgement is delegated. Every package works test first: it writes the failing
test, then the code.

## Rules for every package

- **Ownership.** "Owns" means that only this package may create, change or delete the file in its layer. A file may
  have different owners in different layers. Where a package needs a change to a file it does not own, it codes
  against the interface design-r2 names (§6.1, §8) and puts the request in its report. The orchestrator makes shared
  changes on `gf-conversion` between layers, never during one.
- **Paths.** `$R` is `.shop/records/2026-11-03-gf-conversion`. Commands run from the repository root.
- **The common checks**:
  - `python3 scripts/tools size --limit 300` exits 0;
  - `python3 -m pytest -q -p no:randomly 2>&1 | grep -E '^FAILED' | sort | comm -13 <allowed> -` prints nothing,
    where `<allowed>` is `baseline-failures.txt` joined with the layer's allowance file (below).
- **Allowance (the red window).** R1 changes the shape of every requirement tree (`Shall` takes `VPs`), and R2
  stops reading `Means:` once R5 removes it. Until layer 3 has replaced the old readers, a failure is allowed when
  its traceback passes through `spec_logic.py`, `spec_logic_vocab.py`, `spec_solve.py` or `features_generate.py`.
  - The layer 1 gate writes the failing test ids to `gate-r2-L1-allowed.txt`. Later layers may only shrink that
    file, never add to it.
  - After the layer 3 gate, the file holds at most `tests/scripts/test_e2e_codified.py`.
  - After the layer 4 gate, it is empty.
  - The scenario suite (`tests/scenarios/`) runs the checked-in `features/*.feature` files, and it stays green in
    every layer. So no package before layer 5 removes a Steps fun or a handler that a checked-in feature uses
    (`SCommits`/`ThenCommits` stay until R14; design-r2 §4.4).
- **Frozen in layer 4:** `grammar/*.gf`, `grammar/*.lp`, `scripts/`, `tests/scenarios/conftest.py`, `vocab.py`,
  `world_nodes.py`, `world_run.py`, `spec/index.md`. A layer-4 line that needs a new grammar fun is reworded; if it
  cannot be, the package lists it in its report and R14 adds the fun and finishes the line.
- **Commits.** Each package commits on its branch, and every message ends with
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. The orchestrator merges with `--no-ff`. Each package
  writes `report-R<n>.md` beside this file, with the CLAUDE.md module-map row of each new module. R14 writes those
  rows into CLAUDE.md.
- **Toolchain.** GF, pgf, clingo 5.8.2 and telingo 2.1.3 are installed (`python3 scripts/tools probe`). The
  throwaway spike is at `.shop/scratch/spike-tel/`.

## Layer 0: baselines (the orchestrator, on `gf-conversion`, before layer 1)

1. Move the entry `- **push** (event): …` unchanged from `spec/capabilities/role-boundaries.md` to `spec/index.md`'s
   glossary, so the 50 lines that use `CommitPush`/`RefuseErr` parse as `AndVP` once R1 lands (design-r2 §4.1).
   Check that `python3 scripts/model lexicon --check` prints no new problem.
2. Record `python3 scripts/model logic --json > .shop/records/2026-11-03-gf-conversion/logic-baseline-r2.json` (the
   code of 7e0684d2, check point 21) and its run time.
3. Write `.shop/scratch/unparsed.sh` (gitignored) with this text. It prints `<cap>: <line>` for each Behaviour or U
   line, continuation lines joined, that `model parse` refuses:

   ```sh
   for f in spec/capabilities/*.md spec/universal.md; do c=$(basename "$f" .md)
     awk '/^- \[[rU][0-9]+\] /{if(s)print s; s=$0; next} /^  [^ ]/&&s{sub(/^ +/," "); s=s $0; next}
          {if(s)print s; s=""} END{if(s)print s}' "$f" | sed -E 's/^- \[[rU][0-9]+\] //' > .shop/scratch/l.txt
     python3 scripts/model parse --file .shop/scratch/l.txt | awk -v c="$c" 'NR==FNR{l[FNR]=$0; next}
       /^[0-9]+: /{n=$1; sub(/:/,"",n); if ($2 !~ /^(Ubiq|When|While|Where|IfThen|WhileWhen|WhereWhen|WhereWhile|WhileIf|WhereIf)$/) print c": "l[n]}' .shop/scratch/l.txt -
   done | sort
   ```
4. Run it and save the output as `unparsed-L0.txt` beside this plan.
5. Commit the three records (`logic-baseline-r2.json`, `unparsed-L0.txt`, `gate-r2-L0.md` with the times and counts)
   and the `push` move.

## Layer 1: the foundations (R1, R2, R3 in parallel)

### R1 The grammar: coordination, prepositions, definitions

- **Goal:** design-r2 §4.
  - Add `VPs`/`VPor`/`Resps` and `CondOr`. Delete `RefuseErr` and `CommitPush` from Req in the same change (both
    beside `AndVP` would give two trees). Leave `SCommits` in the Steps grammar.
  - Generate the typed relation funs (modifier and atom) from the lexicon's relation rows, the supertype's own row
    included. No `Prep` class and no `SRelAtom` (check point 3).
  - Generate the `Def`/`DefEng` module in `spec_typed_def.py` (new): one `c_<cond>_<kind>_Def : Cond -> Def` for
    each (condition, kind). `spec_grammar.parse(root, text, grammar="Def")` compiles it by the existing `load`, and
    refuses a tree holding any `_It` fun with the hint "a definition names its subject as the <kind>".
  - `spec_tree.parts` returns the response as a list of `(polarity, subject, VP)` conjuncts.
- **Owns:**
  - `grammar/Core.gf`, `CoreEng.gf`, `Req.gf`, `ReqEng.gf`, `Steps.gf`, `StepsEng.gf`;
  - `grammar/corpus/core.txt` (new) and `grammar/corpus/refused.txt`;
  - `scripts/spec_typed.py`, `scripts/spec_typed_def.py` (new), `scripts/spec_tree.py`, `scripts/spec_grammar.py`,
    `scripts/tools_grammar.py`;
  - `tests/scripts/test_spec_grammar.py`, `test_spec_tree.py`, `test_tools_grammar.py`, `test_spec_typed_def.py`
    (new).
- **Depends on:** nothing. It reads relation rows through `Lexicon.relations()` and `Term.supertype` (design-r2 §8),
  which R2 adds. Until then it tests against a stub lexicon with those two members.
- **Accepts:**
  - `python3 -m pytest -q tests/scripts/test_spec_grammar.py tests/scripts/test_spec_tree.py tests/scripts/test_tools_grammar.py tests/scripts/test_spec_typed_def.py`
    passes, with new tests that:
    - every line of `grammar/corpus/*.txt` has exactly one tree, and each `core.txt` line has its expected tree;
    - `core.txt` holds: one line for each new fun; the risky `and` cases (`print the file and the line count and
      exit successfully`); "commit every transition and push the commit" and "exit with an error naming the reason
      and change nothing" as `AndVP`; a stage "for the work-item w1" and a stage "for a node" with their two typed
      trees (check point 12); q47's line 4 (check point 17);
    - "a `plan` stage for a work-item with the result" has one tree with a stub row (stage, with, result), and is
      refused as ambiguous when a stub row (work-item, with, result) is added; the same for q47's line 4 with a stub
      row (initiative, with, result);
    - the three `Def` lines of design-r2 §4.3 give their expected trees, or the refusal;
    - `parts()` returns two conjuncts for `shall A and B`;
  - `python3 scripts/model parse "While a result is outputless, when a session ends a \`plan\` stage for a work-item with the result, \`work run\` shall set the status of the work-item to \`awaiting-answer\` and ask a question on the work-item."`
    prints one tree whose response is `AndVP`;
  - `! grep -n 'RefuseErr\|CommitPush' grammar/Req.gf grammar/ReqEng.gf`, and `grep -q SCommits grammar/Steps.gf`;
  - `python3 scripts/features vocab --check --tests tests/scenarios` exits 0 (the Steps grammar is additive);
  - `sh .shop/scratch/unparsed.sh | comm -13 $R/unparsed-L0.txt -` prints nothing (no line stops parsing), run with
    layer 0's `push` move in its base.

### R2 The lexicon, the readers and the model rules

- **Goal:** design-r2 §8 and §9.1's rules.
  - Move the given-block reading out of `spec_read.py` into `spec_read_given.py` (new) first, with no change in
    behaviour, then add the example-data shape test there (check point 14; no grammar is compiled).
  - `spec_relations.py` (new) reads `## Relations` tables (in `spec/index.md` and in capabilities), expands
    `Kind of:` (the supertype's row kept), and gives v_t8 and v_t10. `spec_lexicon` calls it, and gives
    `relations()`, `supertype` and `definition(term)`. Legacy relation entries become rows, and `Means:` is still
    read but is now a problem.
  - v_t7 by design-r2 §8's counting rule, and v_t9 (`Means:`).
  - `model_spec` and `model.lp` add v15l (a group with more than one statement), v15m (a given line that is not
    example data, by the shape test) and v15n (two groups of one capability whose statements share features,
    condition and trigger, compared as normalised trees as v15k does).
  - The `model` contract text loses `Means:`, and `model parse --grammar` takes `Req`, `Steps` or `Def`.
- **Owns:** `scripts/spec_lexicon.py`, `scripts/spec_relations.py` (new), `scripts/spec_read.py`,
  `scripts/spec_read_given.py` (new), `scripts/model_spec.py`, `scripts/model.lp`, `scripts/model` (the contract
  text and the parse choices), `tests/scripts/test_spec_lexicon.py`, `test_spec_relations.py` (new),
  `test_spec_read.py`, `test_model_spec.py`.
- **Depends on:** nothing.
- **Accepts:**
  - `python3 -m pytest -q tests/scripts/test_spec_lexicon.py tests/scripts/test_spec_relations.py tests/scripts/test_spec_read.py tests/scripts/test_model_spec.py`
    passes, with:
    - a test for each of v_t7–v_t10, v15l, v15m and v15n firing on a fixture and silent on a clean one;
    - v_t7's cases: a code span holding `.`, `e.g.`, a `:` gloss and a trailing field pass; two sentences and a `;`
      fail;
    - v15m's cases: the line "the file `a.md` holds:" with a docstring after it, and the line "the file `a.md`
      holds "x"", pass; "a result r1" and "the result r1 is outputless" fire;
    - `relations()` expands a `Kind of: node` row to each subkind and keeps the node row;
  - `python3 scripts/model lexicon --check` on the live spec lists the v_t7–v_t10 problems (R5 clears them; the
    counts go in the report);
  - `python3 scripts/model check --json | python3 -c "import json,sys; d=json.load(sys.stdin); print(sorted({r[0] for r in d['violations'] if r[0] in ('v15l','v15m','v15n')}))"`
    prints the rules that fire on the live spec (layer 4 clears them; the counts go in the report), and v15m's
    count equals the given lines that are not example data (65 blocks in supervision alone);
  - `wc -l scripts/spec_lexicon.py scripts/spec_read.py` are each at most 300, and `scripts/model_spec.py` too.

### R3 The solver engine

- **Goal:** design-r2 §6.3 and §5.7's cone, independent of trees. It runs on program text, facts and ids.
  - `Proxy` for `telingo.imain`: externals freed after ground, `on/1` assumptions, `on_core`, optimal models.
  - `solve(text, on_ids, imax, pools, optimise=False) -> Result(sat, horizon, core, models)`. `pools` is
    `{kind: n}`, rendered as `pool_size/2` facts. On UNSAT it solves once more with each pool at n × imax + 1, and
    reports `sat=False` only if that is UNSAT too (check point 10).
  - `minimal_core(…)`, `least(models)` (the least model by its sorted atom strings, refused past 10 000).
  - `grammar/cone.lp` (new) and `cone(facts, gid) -> (ids, edges)`; `horizon_bound(edges, start)` (the longest path
    + 2, or the node count + 2 on a cycle).
- **Owns:** `scripts/spec_engine.py` (new), `grammar/cone.lp` (new), `tests/scripts/test_spec_engine.py` (new).
- **Depends on:** nothing.
- **Accepts:** `python3 -m pytest -q tests/scripts/test_spec_engine.py` passes. Its tests use hand-written `&tel`
  programs from the spike and hand-written signature facts:
  - `test_stops_at_horizon_1`, and `test_chained_stops_at_horizon_2` (a chained statement);
  - `test_core_names_both_ids` (a seeded conflict whose core is exactly its two ids);
  - `test_least_model_is_hash_seed_free` (the same least model in two processes with different `PYTHONHASHSEED`);
  - `test_reachable_value` (`>?` SAT) and `test_unreachable_value` (UNSAT at imax);
  - `test_cycle_bound`;
  - `test_pool_retry` (a program needing four instances of a kind, given a pool of 2, is SAT after the retry);
  - `test_cone_rules` (reachability; a While over used kinds enters, a While over an unused kind does not);
  - `test_engine_uses_imain` (`telingo.imain` patched with a recording wrapper is called once per solve);
  - and `! grep -n 'release_external\|def _ground' scripts/spec_engine.py` (no loop is copied).

**Layer 1 gate:** merge R1, R2 and R3. Run the common checks. Write `gate-r2-L1-allowed.txt` from the failures whose
traceback passes through the four old readers. Check that the merged tree has no stub left: R1's `spec_typed` reads
R2's real `relations()`. `python3 scripts/model parse --file` on `grammar/corpus/supervision.txt` exits 0. Run
`sh .shop/scratch/unparsed.sh > $R/unparsed-L1.txt`; `comm -13 $R/unparsed-L0.txt $R/unparsed-L1.txt` prints nothing,
and `unparsed-L1.txt` is committed as the baseline R5 and layer 4 compare with (check point 23).

## Layer 2: one translation, and the glossary (R4, R5 in parallel)

### R4 The &tel translation and `model logic`

- **Goal:** design-r2 §5 and §6.
  - `spec_logic` is rewritten as one translation per fun, with two renderers (`&tel` for statements, an ASP body
    for definitions). Beside the constraints it emits the labels and the signature facts of §5.7, from the same
    per-fun code.
  - The witness of a group includes the contrast of an `_Every`/`_Pl` with a restriction (§5.4).
  - `spec_logic_np` (new) holds the NP and CN half, and `spec_logic_vocab` the facts and pool sizes.
  - `grammar/background.lp` is rewritten.
  - `spec_solve` is rewritten onto `spec_engine`: the cone from `cone.lp`, L1 with cores, L2, L3 via guarded
    transitions, and L4 by `>?` over the labelled state-0 `attr` atoms of each group's model. `run()` and
    `report()` keep their signatures.
  - The copied imain, `HORIZON`, `_edges`, `l3`'s tree walk and `_reachable` are deleted.
- **Owns:** `scripts/spec_logic.py`, `scripts/spec_logic_np.py` (new), `scripts/spec_logic_vocab.py`,
  `scripts/spec_solve.py`, `grammar/background.lp`, `scripts/model_report.py` (the logic wiring only),
  `tests/scripts/test_spec_logic.py`, `tests/scripts/test_spec_solve.py`, `tests/scripts/fixtures/logic/**`.
- **Depends on:** R1, R2, R3.
- **Accepts:**
  - `python3 -m pytest -q tests/scripts/test_spec_logic.py tests/scripts/test_spec_solve.py` passes, with:
    - a test for each row of design-r2 §5.2–§5.5 (the rule text emitted), among them
      `test_statement_is_a_tel_constraint`;
    - `test_labels` (g13 merged emits `lab` rules for `cond(1)`, `trig`, `resp(1)`, `resp(2)`) and `test_signatures`
      (its `trig`/`eff`/`uses` facts);
    - `test_contrast_in_witness` (an `every … that …` response gives a `contrast` and a `not(1)` label);
    - `test_seeded_conflict`. It builds its conflict **from the live spec**, naming no id: it takes the first service
      group whose program is SAT and whose statement is `When T, S shall V…`, makes the tree `When T (ShallNot S
      (OneVPor V1))` from V's first conjunct, linearises it through Req, appends it as a new group to a temp copy,
      and asserts one L1 whose core names both requirement ids. So it holds on the renumbered final spec too;
    - an L3 through a `T:` guard, an L4 asked of the solver, and a definition rule from a `Def` sentence;
    - tests on the live spec name no codified id; tests of fixed ids use `tests/scripts/fixtures/logic/` (check
      point 19);
  - `! grep -n 'HORIZON = \|def _ground\|_reachable\|def _edges' scripts/spec_solve.py`;
  - `time python3 scripts/model logic` on R4's own base: the time goes in the report (the 60 s limit is the layer 2
    gate's, check point 20);
  - `python3 scripts/model logic --json supervision` compared with `$R/logic-baseline-r2.json`: each L1 not in the
    baseline (by group and core ids) is listed in the report as real, with its core, or fixed (check point 21).

### R5 The glossary rewritten

- **Goal:** design-r2 §8 on the live spec.
  - Every term entry is one sentence by §8's rule.
  - Conditions are `Def` sentences that parse (`model parse --grammar Def`), naming their subject "the <kind>", or
    primitive glosses.
  - Relations go into `## Relations` tables, and preposition entries are deleted. supervision.md's local `for`
    entries that `spec/index.md`'s (stage, for, node) row covers are deleted (v_t10).
  - Content kinds and events (worker brief, tool list, round brief, review brief, output, change list, log, …)
    become one-sentence glosses. Their removed content goes, verbatim, with its capability, into the hand-off file,
    which the layer 4 packages turn into requirements.
  - The words that q47's lines use are kept.
  - For the person's point 3 (check point 16), the report counts: the preposition and relation entries before, the
    `## Relations` rows after, and each word with more than one row and its rows.
- **Owns:** `spec/index.md` (its `## Glossary` and the new `## Relations`), the `## Terms` section and a new
  `## Relations` section of every `spec/capabilities/*.md` (only those sections in this layer), and
  `$R/r5-moved-content.md` (new).
- **Depends on:** R1, R2.
- **Accepts:**
  - `python3 scripts/model lexicon --check` prints `0 problems`;
  - `! grep -rn 'Means:' spec/`;
  - `sed -n '/^## Lines/,/^## Questions/p' .shop/work/requests/q47.md | grep -E '^[0-9]+\. ' | sed 's/^[0-9]*\. //' > .shop/scratch/q47.txt && python3 scripts/model parse --file .shop/scratch/q47.txt`
    exits 0;
  - no Behaviour or U line stops parsing: `sh .shop/scratch/unparsed.sh | comm -13 $R/unparsed-L1.txt -` prints
    nothing (check point 23);
  - the hand-off file names each moved entry with its capability and its old text.

**Layer 2 gate:** merge R4 and R5. Run the common checks, where the allowance may only shrink. Run `time python3 scripts/model logic`
on the merged spec: it finishes in under 60 s, or the gate hands R4's cache (design-r2 §6.4) back to R4 before layer
3. Record its time and findings in `gate-r2-L2.md`.

## Layer 3: Gherkin from traces, and the docs (R6, R7 in parallel)

### R6 The generator reads traces

- **Goal:** design-r2 §7.
  - First, with no change in behaviour, move `features_vocab.modules(lex)` (with `attributes` and `_relation_text`)
    into `features_vocab_gf.py` (new), so that `features_vocab.py` (299 lines) has room (check point 18).
  - `spec_trace` (new) builds a group's scenario program from `spec_logic`'s output and solves it with optN on
    `spec_engine`, takes the least model, names the instances, and reads Givens, When and Thens by the atom table
    of design-r2 §7.3. It reads `lab/3` and state-0 atoms only: it imports neither `spec_tree` nor `spec_grammar`
    (check point 5).
  - `features_generate` keeps only the file writing. It reads given blocks by `spec_read_given`'s shape test: an
    example-data line goes first, as today; any other given line is left out with a line on stderr, never refused
    (check point 4).
  - `features_vocab` replaces `_relation_text` by the relations table and drops the non-example Given templates
    from given blocks. It keeps `SCommits`/`ThenCommits` (R14 deletes them).
  - The old rule engine (`Scenario.resolve`/`choose`/`constraints`/`condition`/`precondition`/`becomes`/`then`, and
    the `CommitPush`/`RefuseErr` action map) is deleted.
- **Owns:** `scripts/spec_trace.py` (new), `scripts/features_generate.py`, `scripts/features_vocab.py`,
  `scripts/features_vocab_gf.py` (new), `scripts/features` (the generate and vocab subcommands only),
  `tests/scenarios/vocab.py`, `tests/scripts/test_spec_trace.py` (new), `test_features_generate.py`,
  `test_features_vocab.py`.
- **Depends on:** R4.
- **Accepts:**
  - `python3 -m pytest -q tests/scripts/test_spec_trace.py tests/scripts/test_features_generate.py tests/scripts/test_features_vocab.py`
    passes, with:
    - `test_byte_stable` and `test_related_while_enters` as design-r2 §7.4 states them;
    - a test that a temp copy of supervision with g2's given block deleted gives the step "Given a work-item w1
      that is `drafted`";
    - a test that g13 merged gives two Thens, and that a commit-and-push response gives two Thens (`SDoes`);
    - a test that an `every … that …` response gives its contrast's `SDoesNot` Then from one solve;
    - a test that a given block with a non-example line generates, without that line, and writes one stderr line;
  - `! grep -n 'def choose\|def resolve\|def precondition\|\.means' scripts/features_generate.py`;
    `! grep -n 'import spec_tree\|import spec_grammar' scripts/spec_trace.py`; and
    `wc -l < scripts/features_generate.py` is at most 120;
  - `python3 scripts/features generate --preview <temp copy of spec/capabilities/supervision.md>` exits 0 on the
    live file, with its 65 non-example given blocks (they are left out; a crash is a failure).

### R7 The docs, skills and agents

- **Goal:** design-r2 §4, §8 and §9.1 in the words the sessions read:
  - one statement per group, with `and`, and one statement per (features, condition, trigger) in a capability
    (v15n);
  - one sentence per term, counted by design-r2 §8's rule;
  - the relations table and `Kind of:`;
  - conditions as `Def` sentences that name their subject "the <kind>", or primitive;
  - given blocks only for example data;
  - `model logic` described by its new checks.

  `docs/design-model/grammar.md` lists the new funs. The raising-a-request skill shows `and`.
- **Owns:** `docs/design-model/grammar.md`, `docs/design-model/design-model.md`, `docs/capability-format.md`,
  `agents/capability-writer.md`, `agents/spec-checker.md`, `agents/initiative-round.md`,
  `skills/checking-spec-consistency/SKILL.md`, `skills/formulating-features/SKILL.md`,
  `skills/raising-a-request/SKILL.md`, `skills/integrating-a-proposal/SKILL.md`.
- **Depends on:** R1, R2 (it describes their interfaces).
- **Accepts:**
  - `! grep -rn 'Means:' docs skills agents`;
  - `! grep -rniE 'one .?shall.?\b' docs/design-model/grammar.md`;
  - `grep -q '## Relations' docs/capability-format.md`;
  - `grep -q 'example data' docs/capability-format.md`;
  - the full suite (some tests read the skills' text).

**Layer 3 gate:** merge R6 and R7. Run the common checks. The allowance now holds at most `test_e2e_codified.py`.
`python3 scripts/features generate --check` is run and its output recorded. It may differ from the checked-in features
(they are regenerated in layer 4), but it must not crash. The scenario suite still runs the checked-in features and
is green.

## Layer 4: the spec rewritten by capability groups (R8–R13 in parallel)

Each package applies design-r2 §9.2 to each of its capabilities C:

1. Rewrite `## Terms`, `## Relations` and `## Behaviour`.
2. Turn its part of `r5-moved-content.md` into requirements.
3. Merge the groups v15n names (one statement per (features, condition, trigger) in C).
4. Renumber so that g<n> = r<n>, and write `$R/ids-C.tsv` (old codified id, tab, new id; a merged-away id maps to
   the id it went into).
5. Regenerate `features/C.feature`, and make the scenarios pass through C's handlers and world modules.

It may add local terms and relation rows only in its own capability files. A term that two packages both add is
moved into `spec/index.md` by the orchestrator at the gate. The files frozen in this layer are listed under "Rules
for every package".

**The per-capability accepts** (each package runs them for each C it owns):
- `sh .shop/scratch/unparsed.sh | grep "^C: "` prints nothing (continuation lines joined; check point 23);
- `python3 scripts/model logic C` exits 0, and each L4 warning is listed in the report;
- `python3 scripts/model restates C` reports `0 missing`;
- `python3 scripts/model check --json | python3 -c "import json,sys; v=[r for r in json.load(sys.stdin)['violations'] if r[0] in ('v15k','v15l','v15m','v15n') and any('/C#' in a for a in r[1])]; print(v); sys.exit(bool(v))"`
  exits 0;
- for a service capability: `python3 scripts/features generate --check C` exits 0, and
  `python3 -m pytest -q -p no:randomly tests/scenarios/test_<c>.py` passes;
- `grep -c '^- \[r' spec/capabilities/C.md` equals `grep -c '^### \[g' spec/capabilities/C.md`;
- `$R/ids-C.tsv` exists and has a row for every codified id of C at the layer's base.

### R8 supervision

- **Owns:** `spec/capabilities/supervision.md`, `features/supervision.feature`, `grammar/corpus/supervision.txt`,
  `tests/scenarios/supervision_*.py` (with `supervision_build.py`, whose `work-queue#r1` names an id in the spec its
  own scenario writes, design-r2 §9.1), `tests/scenarios/test_supervision.py`. It keeps the `ThenCommits` handler in
  `supervision_handlers_what.py` (R14 deletes it).
- **Depends on:** layer 3. It is the largest package: 86 groups, 139 statements, 65 given blocks, 28 conditions,
  and the content kinds of R5's hand-off.
- **Accepts:** the per-capability accepts for supervision.

### R9 design-model-check

- **Owns:** `spec/capabilities/design-model-check.md`, `features/design-model-check.feature`,
  `grammar/corpus/design-model-check.txt`, `tests/scenarios/design_model_check_*.py`,
  `tests/scenarios/test_design_model_check.py`.
- **Depends on:** layer 3. 55 groups, 45 given blocks, 40 conditions (mostly primitive, design-r2 §4.3).
- **Accepts:** the per-capability accepts for design-model-check.

### R10 migration-tools and feature-file-tools

- **Owns:** both capability files, both features, both corpus files, `tests/scenarios/migration_*.py`,
  `tests/scenarios/feature_file_tools_*.py`, `tests/scenarios/test_migration_tools.py`,
  `tests/scenarios/test_feature_file_tools.py`.
- **Depends on:** layer 3. 48 groups, 48 given blocks; most of the file-content blocks are example data and stay.
- **Accepts:** the per-capability accepts for both.

### R11 analysis-tools and batch-measurement

- **Owns:** both capability files, both features, both corpus files, `tests/scenarios/analysis_tools_*.py`,
  `tests/scenarios/batch_measurement_*.py`, `tests/scenarios/test_analysis_tools.py`,
  `tests/scenarios/test_batch_measurement.py`.
- **Depends on:** layer 3. 62 groups, 54 given blocks.
- **Accepts:** the per-capability accepts for both.

### R12 work-queue and requests, and the end-to-end fixture

- **Owns:**
  - both capability files, both features, both corpus files;
  - `spec/decisions/0072-work-list-and-work-show-replace-work-status.md`: its six `work-queue#r34`–`r39` sources
    are 0.29 ids and are written `…#r34@0.29` … (design-r2 §9.1). If `model check` does not resolve an `@0.29` id in
    a decision's `source`, the report says so, and the rows stay as in `baseline-model-check.txt`;
  - `tests/scenarios/work_queue_*.py`, `tests/scenarios/requests_handlers.py`,
    `tests/scenarios/test_work_queue.py`, `tests/scenarios/test_requests.py`;
  - `tests/scripts/fixtures/e2e/**`, `tests/scripts/test_e2e_codified.py`, `tests/scripts/stub_claude.py`.
- **Goal, beyond the shared one:** the P15 fixture context's spec in the new format (`## Relations`, one-sentence
  terms, no non-example given blocks, one statement per group). Its test's lines (`GOOD`, the drafts it seeds) parse,
  and the test runs the new `model logic` and `features generate`.
- **Depends on:** layer 3. 53 groups, 22 given blocks.
- **Accepts:** the per-capability accepts for both, and `python3 -m pytest -q tests/scripts/test_e2e_codified.py`
  passes.

### R13 the guarantees capabilities and the universal conditions

- **Owns:**
  - `spec/capabilities/{code-research,delivery,formulation,planning,red-green,review,role-boundaries,spec-consistency,spec-integration,spec-migration,trials}.md`
    and their corpus files;
  - `spec/universal.md` and `grammar/corpus/universal.txt`;
  - `tests/scripts/test_spec_guarantees.py`.
- **Goal, beyond the shared one:** U1–U10 rewritten (U3 and U4 by VP coordination; U7 with `or` where it fits).
  These capabilities have no scenarios, so their accepts have no generate step.
- **Depends on:** layer 3. 128 groups, 248 statements, no given blocks.
- **Accepts:**
  - the per-capability accepts for each of the eleven (without the features step);
  - `python3 scripts/model logic` exits 0 with every U on;
  - `python3 -m pytest -q tests/scripts/test_spec_guarantees.py` passes.

**Layer 4 gate:**
1. Merge R8–R13.
2. Move any local term that two packages defined into `spec/index.md`.
3. The references (check point 19): for each capability C,
   `git grep -nE '\bC#[rg][0-9]+\b' -- ':!spec/capabilities' ':!features' ':!.shop/records' ':!.shop/work'` finds only
   the files design-r2 §9.1 lists, and each hit is either one of the kinds listed there or is rewritten through
   `$R/ids-C.tsv` by the orchestrator; `.shop/work/` is checked by the `model check` rows of step 4.
4. Run `python3 scripts/model lexicon --check`, `python3 scripts/model restates` (`0 missing`),
   `python3 scripts/features generate --check`, `sh .shop/scratch/unparsed.sh` (prints nothing), `python3 scripts/model
   check` (no `file:` or `unresolved:` row outside `baseline-model-check.txt`) and the full suite. The allowance file
   is now empty.

## Layer 5: the revision verified (R14)

### R14 Legacy removed, map written, "Done means" measured

- **Goal:**
  - Delete what only the red window needed: `Term.means` and the legacy relation entries in `spec_lexicon`, and any
    shim left in `spec_tree`.
  - Delete `SCommits` (check point 1): from `grammar/Steps.gf` and `StepsEng.gf`, its `ThenCommits` mapping and its
    argument rules in `features_vocab.py`, and the `ThenCommits` handler in `tests/scenarios/supervision_handlers_what.py`,
    after `! grep -rn 'and pushes the commit' features/` shows no step uses it.
  - Add any grammar fun a layer-4 report handed back, and finish the lines that needed it.
  - Write the CLAUDE.md module-map rows from every report: `spec_engine`, `spec_trace`, `spec_logic_np`,
    `spec_relations`, `spec_read_given`, `spec_typed_def`, `features_vocab_gf`, `grammar/cone.lp`, plus the `spec_*`
    rows the map has always lacked.
  - Run every measurement of design-r2 §2 and record the outcomes in `gate-r2-done.md`, each with its command, its
    exit code and its output.
  - Write into `gate-r2-done.md`, as an open point for the person, R5's relation counts and design-r2 §13 call 16:
    why `## Relations` rows remain, and what they are not (check point 16).
  - Fix what fails, or hand it back to the orchestrator.
- **Owns:** `scripts/spec_lexicon.py`, `scripts/spec_tree.py`, `grammar/Steps.gf`, `grammar/StepsEng.gf`,
  `scripts/features_vocab.py`, `tests/scenarios/supervision_handlers_what.py`, the grammar files and capability
  lines a layer-4 report handed back, `CLAUDE.md` (the module map only), `tests/scripts/test_revision_done.py` (new:
  the §2 measurements as tests), and `$R/gate-r2-done.md`.
- **Depends on:** layer 4.
- **Accepts** (these are the brief's "Done means"; check point 22: named tests, not positive greps):
  1. **No non-example given block:** no `v15m` row in `python3 scripts/model check --json`.
  2. **No repeated trigger:** no `v15k`, `v15l` or `v15n` row in `python3 scripts/model check --json`.
  3. **Terms:**
     - `python3 scripts/model lexicon --check` prints `0 problems` (v_t4–v_t10, v_t7 by design-r2 §8's rule);
     - `! grep -rn 'Means:' spec/`;
     - the relation counts and call 16 are in `gate-r2-done.md` for the person.
  4. **One translation, conflicts found:**
     `python3 -m pytest -q "tests/scripts/test_spec_logic.py::test_statement_is_a_tel_constraint" "tests/scripts/test_spec_engine.py::test_stops_at_horizon_1" "tests/scripts/test_spec_engine.py::test_chained_stops_at_horizon_2" "tests/scripts/test_spec_engine.py::test_engine_uses_imain" "tests/scripts/test_spec_solve.py::test_seeded_conflict"`
     passes on the final spec, and `! grep -rn 'HORIZON = ' scripts/`.
  5. **Gherkin from traces, byte-stable:**
     - `PYTHONHASHSEED=1 python3 scripts/features generate --check && PYTHONHASHSEED=2 python3 scripts/features generate --check`;
     - `git diff --exit-code features/`;
     - `python3 -m pytest -q tests/scripts/test_spec_trace.py -k 'byte_stable or related_while'` (amended at the layer 5
       gate: R6 put those tests in test_spec_trace.py, not test_features_generate.py).
  6. **New requests go through it:**
     - `python3 -m pytest -q tests/scripts/test_e2e_codified.py`;
     - q47's lines parse (the R5 command).
  7. **Suite and size:**
     - `python3 -m pytest -q -p no:randomly` has no failure outside `baseline-failures.txt`;
     - `python3 scripts/tools size --limit 300` exits 0;
     - every `scripts/*.py` has a map row (the P14 one-liner in plan.md, line 438);
     - `python3 scripts/features vocab --check --tests tests/scenarios` exits 0 and `! grep -n SCommits grammar/*.gf scripts/*.py`.
  8. `time python3 scripts/model logic` is under 60 s, and its findings (L4 warnings only) are listed.
  9. `python3 scripts/model check` prints no `file:` or `unresolved:` row outside `baseline-model-check.txt`, except
     rows naming `.shop/work/` files of abandoned initiatives, each listed in `gate-r2-done.md`.

## Summary

| layer | packages (parallel) | what it gives the next |
|---|---|---|
| 0 | the orchestrator | `push` in the index; the logic and unparsed baselines |
| 1 | R1 grammar, R2 lexicon and rules, R3 engine | trees with `and`/prepositions/definitions; relations and new rules; a solver with cores, an incremental horizon and the cone |
| 2 | R4 &tel translation and checks, R5 glossary | one translation; `model logic` on `&tel`; a lexicon of one-sentence terms |
| 3 | R6 generator from traces, R7 docs | `features generate` from traces, byte-stable; sessions told the new format |
| 4 | R8 supervision, R9 design-model-check, R10 migration/feature-file tools, R11 analysis/batch, R12 work-queue/requests and e2e, R13 guarantees and U's | the spec rewritten and renumbered, with features and handlers green |
| 5 | R14 | legacy and `SCommits` removed, the map written, "Done means" measured, point 3's substance put to the person |

The critical path is R1 → R4 → R6 → R8 (supervision). If R8 cannot finish in one package, the orchestrator splits it
by section (stages; rounds; pool and resources; branch review and done) into R8a–R8d at the layer 4 start. Each part
owns its own handler modules, and only the orchestrator merges the capability file between them.
