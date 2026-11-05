---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-03-gf-conversion-plan
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-03
status: draft
---

# The GF conversion: the build plan

This plan builds `design.md` (beside this file), and every package reads that design and `brief.md` first. Design §18
lists the calls made after the builder check (`builder-check.md`), and this plan applies them. There are 16 packages
in 6 layers. Packages in one layer own disjoint files, so each runs in its own worktree off `gf-conversion`. A layer
starts only when the layer before it is merged and its gate passes.

"Owns" means that only this package may create, change or delete the file in its layer. Ownership is per layer, so a
file can be owned by different packages in different layers. A package that needs a change to a file it does not own
codes against the interface the design names, and asks the orchestrator if that is not enough. The orchestrator makes
shared changes (a grammar fun, a world handler) on `gf-conversion` between layers, never inside one.

All commands run from the repository root. Besides its own checks, every package passes:

- `python3 scripts/tools size --limit 300` exits 0;
- `python3 -m pytest -q -p no:randomly 2>&1 | grep -E '^FAILED' | sort | comm -13 .shop/records/2026-11-03-gf-conversion/baseline-failures.txt -`
  prints nothing (no failure outside the baseline), except as the package says.

Each package reports the CLAUDE.md module-map row of each new module, and P14 writes the rows. Each package commits
on its branch with the attribution lines, and the orchestrator merges.

Codified is a property of each file (design §13.4): a capability file is converted when its own frontmatter has
`language: codified-1`. Unconverted capabilities stay on the legacy reader until P14, so every package's checks run in
its own worktree.

## Before layer 1 (orchestrator, not a package)

1. Install the grammar wheels into the suite's interpreter, so layer 1 can test before P1 automates it:
   `python3 -m pip install --user pgf==1.1 clingo==5.8.2 telingo==2.1.3`. For layers 1 and 2, export
   `SHOPSYSTEM_GF=/home/vscode/shopsystem-bdd/.shop/scratch/spike-cnl/gfc`.
2. Record the baselines. The recorded files are authoritative; the surveys' "23" is not.
   - `python3 -m pytest -q -p no:randomly 2>&1 | grep -E '^FAILED' | sort > .shop/records/2026-11-03-gf-conversion/baseline-failures.txt`
   - `python3 scripts/model check 2>&1 | grep -vE '^[0-9]+ violations' | sort > .shop/records/2026-11-03-gf-conversion/baseline-model-check.txt`
3. Commit both on `gf-conversion`.

## Layer 1: foundations

### P1 Grammar toolchain
- **Goal:** design §11.1–§11.2.
  - `tools install` installs GF 3.12: download, sha256 check, `dpkg-deb -x`, and a `bin/gf` wrapper. There is no
    other unpacker: without `dpkg-deb`, it exits 1 naming `dpkg-deb` and `$SHOPSYSTEM_GF`.
  - It installs the pinned pgf, clingo and telingo wheels.
  - It prints the `downloaded` / `installed` / `already installed` lines.
  - On anything but Linux x86_64 it exits 1, naming `$SHOPSYSTEM_GF`.
  - `tools probe` gains the `grammar` block. `tools probe --json` is new.
- **Owns:** `scripts/tools_grammar.py` (new), `scripts/tools_env.py`, `scripts/tools`,
  `tests/scripts/test_tools_grammar.py` (new), `tests/scripts/test_tools.py`,
  `tests/scenarios/analysis_tools_probe_steps.py` (only to keep today's probe scenarios green).
- **Depends on:** nothing.
- **Accept:**
  - `python3 -m pytest -q tests/scripts/test_tools_grammar.py tests/scripts/test_tools.py`. The download is tested
    against a local file, a wrong digest is refused, and an unsupported platform is refused.
  - `python3 scripts/tools install && python3 scripts/tools probe --json | python3 -c "import json,sys; g=json.load(sys.stdin)['grammar']; assert g['gf'].startswith('3.12') and g['pgf']=='1.1' and g['clingo']=='5.8.2' and g['telingo']=='2.1.3'"`
  - `~/.local/share/shopsystem-bdd/gf-3.12/bin/gf --version | grep -q 'version 3.12'`
  - `out=$(python3 scripts/tools install); echo "$out" | grep -q 'gf 3.12 already installed' && ! echo "$out" | grep -q 'downloaded'`

### P2 Requirement grammar, lexicon and parser
- **Goal:**
  - the core `Req` grammar (design §9.2, all six forms);
  - the generated `Lex`/`Typed` modules from a glossary (§10.1), with identifiers by `ident` (§9.6);
  - compile and cache, with the atomic rename (§11.3);
  - `tokenise`, `parse` (tree, refusal with token and position, ambiguity counted after the guard) and `linearise`;
  - the over-generation and literal guards (§9.3, §9.4), normalised trees and `logic_only` (§14.2);
  - the corpus;
  - `tests/toolchain.py` `require()` (§11.3).
  - `spec_lexicon` is the only reader of term entries (§10.1).
- **Owns:** `grammar/Req.gf`, `grammar/ReqEng.gf`, `grammar/corpus/`, `scripts/spec_lexicon.py`,
  `scripts/spec_grammar.py`, `scripts/spec_tree.py`, `tests/toolchain.py`, `tests/scripts/test_spec_lexicon.py`,
  `tests/scripts/test_spec_grammar.py`, `tests/scripts/test_spec_tree.py`, `tests/scripts/fixtures/glossary/` (a
  glossary from DOM §1–§8), `.shop/records/2026-11-03-gf-conversion/p2-grammar.md` (all new).
- **Depends on:** nothing. It uses `$SHOPSYSTEM_GF` until P1 lands. The spike's sources in
  `.shop/scratch/spike-cnl/gf-src/` are a reference.
- **Interface it provides:**
  - `spec_lexicon.read(root) -> Lexicon` (the `## Glossary` of `spec/index.md` plus every capability's `## Terms`),
    `spec_lexicon.entry(bullet, where)`, `spec_lexicon.ident(term, category)`, `spec_lexicon.problems(lexicon)`
    (v_t4–v_t6);
  - `spec_grammar.load(root, grammar="Req"|"Steps")`, `parse(root, line, grammar="Req") -> Parse(tree|None, refusal,
    trees)`, `linearise(root, tree, grammar)`, `tokenise(line)`, `gf_binary()`, `hint(root, line)` (longest parsed
    prefix and nearest lexicon words, §15);
  - `spec_tree.normal(tree)` and `spec_tree.logic_only(trees)`.
- **Accept:**
  - `python3 -m pytest -q tests/scripts/test_spec_grammar.py tests/scripts/test_spec_lexicon.py tests/scripts/test_spec_tree.py`.
    The tests cover:
    - the corpus: at least 8 sentences for each of the 19 capabilities, all six EARS forms, U1–U10, backticked lexicon
      words and code literals. Every sentence parses to exactly one tree and linearises back to its normalised text;
    - `grammar/corpus/refused.txt`, all refused: free phrasing, a value in the wrong attribute slot (an initiative that
      is `drafted`), repeated list members, a dangling "it";
    - `ident` on `work-item`, `` `work run` `` and `spec lock`;
    - a second `load` of one glossary runs no gf (a cache hit);
    - two processes loading one new glossary at once both get a working PGF (the race).
  - `p2-grammar.md` records the cold compile time of the fixture glossary's grammar and the number of corpus lines with
    more than one tree before the guard.

### P3 Spec format, typed glossary, universal conditions, design model v5 docs
- **Goal:**
  - the capability-file format and its reader, with the per-file marker, `## Dropped`, `given` blocks with indented
    data, and `Restates:` in both forms (design §8.3, §10.2, §13.4);
  - `spec/index.md`'s glossary converted to typed terms from DOM (§10.1), with `language: codified-1` set in its
    frontmatter (meaning only "the glossary is typed");
  - `model_parse.glossary_entry` widened to accept `(category …)`, so the legacy `model check` keeps reading the
    glossary;
  - `spec/universal.md` with U1–U10 and its own marker;
  - `spec/restated.json` frozen from 96818f71, keyed `<cap>#r<n>`;
  - `docs/design-model/` rewritten as v5 (§7, the full change table);
  - `docs/capability-format.md` rewritten.
  - No `Not:` word may hit an unconverted line (the no-new-rows check).
- **Owns:** `scripts/spec_read.py` (new), `tests/scripts/test_spec_read.py` (new), `spec/index.md`,
  `spec/universal.md` (new), `spec/restated.json` (new), `docs/design-model/*.md`, `docs/capability-format.md`,
  `scripts/model_parse.py` (only `glossary_entry`), `tests/scripts/test_model_glossary.py`.
- **Depends on:** nothing.
- **Interface it provides:** `spec_read.capability(path) -> Capability(groups[Group(id, title, restates[(cap, n)],
  given[(line, block)], requirements[(id, text, line_no)])], dropped[(cap, n, reason)], retired, frontmatter)`,
  `spec_read.codified(path) -> bool`, `spec_read.universal(root)`, `spec_read.restated(root)`.
- **Accept:**
  - `python3 -m pytest -q tests/scripts/test_spec_read.py tests/scripts/test_model_glossary.py`. The tests cover groups,
    ids, both `Restates:` forms, the `given` fence with a docstring and a table, `## Dropped`, the marker,
    `universal.md`, and malformed input reported with line numbers.
  - `python3 -c "import json; d=json.load(open('spec/restated.json')); assert len(d)==581 and all('#r' in k for k in d)"`
  - `grep -q 'design model v5' spec/index.md`
  - `grep -q 'design model v5' docs/design-model/README.md`
  - `test "$(grep -c '^| C[0-9]' docs/design-model/design-model.md)" -ge 32`
  - No new `model check` rows: `python3 scripts/model check 2>&1 | grep -vE '^[0-9]+ violations' | sort | comm -13 .shop/records/2026-11-03-gf-conversion/baseline-model-check.txt -`
    prints nothing.

### P4 `model check` graph rules to v5
- **Goal:** design §7.1 C1, C5–C7 (as kinds and edges only), C10, C11, C13–C19, C21–C24 and C26–C28 (as rules over
  facts that P5 will emit, `#defined` until then), and §7.2.
  - `model_work.py`: statuses, part kinds, record kinds `design` and `analysis`, `accepts` of groups.
  - `model_requests.py`: `line/3`, `outcome/3` and `upstream/2` facts.
  - Cross-context-request and the retired v3 rules are removed.
- **Owns:** `scripts/model.lp`, `scripts/model_work.py`, `scripts/model_requests.py`, `scripts/model_check.py`,
  `tests/scripts/test_model.py`, `tests/scripts/test_model_reading.py`, `tests/scripts/test_model_output.py`,
  `tests/scripts/test_model_withdrawn.py`, `features/design-model-check.feature`, `tests/scenarios/design_model_check_*.py`,
  `tests/scenarios/test_design_model_check.py` (the last three only to follow renamed codes; P11 rewrites them).
- **Depends on:** nothing.
- **Accept:**
  - `python3 -m pytest -q tests/scripts/test_model.py tests/scripts/test_model_reading.py tests/scripts/test_model_output.py tests/scripts/test_model_withdrawn.py tests/scenarios/test_design_model_check.py`
  - `! python3 scripts/model check 2>&1 | grep -q "kind 'design'"`
  - `! grep -nE 'cross-context-request|needs\(|v_k1|v_k2|v_b2' scripts/model.lp`
  - `python3 scripts/model rules | grep -q v_d5 && python3 scripts/model rules | grep -q w_stale_proposed`

**Layer 1 gate (orchestrator, after merging P1–P4):**
- `python3 scripts/tools install`, then `unset SHOPSYSTEM_GF`;
- `python3 -c "import sys; sys.path.insert(0,'scripts'); import spec_lexicon as L; p=L.problems(L.read('.')); print(p); assert p==[]"`;
- `python3 -c "import sys; sys.path.insert(0,'scripts'); import spec_read as R, spec_grammar as G; bad=[u for u in R.universal('.') if G.parse('.', u.text).tree is None]; assert not bad, bad"`;
- the suite is at baseline.

## Layer 2: the language in the tools

### P5 `model` reads the codified spec
- **Goal:**
  - the new `model_spec.py`. It dispatches per file on `spec_read.codified` and emits groups, `member_of`, `in(G,C)`,
    `restates`, `generates` from `@g<n>`, `parsed/unparsed/ambiguous`, U nodes, `logic_only` (via `spec_tree`) and term
    categories (via `spec_lexicon`);
  - `model_legacy.py` takes the 0.29 bullet reader and `model_parse.ears`, for uncodified files and uncodified
    upstreams;
  - `model_facts.py` split below 300 lines;
  - the v_p1/v_p2/v_p3 rules;
  - references `<cap>#r<n>@0.29` resolved through `restated.json` (§13.4);
  - the subcommands `parse` (with `hint`), `lexicon`, `logic` (calling P6's `spec_solve.run`/`report`), and
    `restates` (§15, new `model_restates.py`);
  - `why` follows `restates`;
  - `work request` parses with `Req` when the upstream root's index is codified, and its refusal carries the hint
    (new `workqueue_lines.py`, which keeps `workqueue_request.py` under 300 lines).
- **Owns:** `scripts/model_spec.py`, `scripts/model_legacy.py`, `scripts/model_restates.py`,
  `scripts/workqueue_lines.py` (new), `scripts/model_facts.py`, `scripts/model_parse.py`, `scripts/model`,
  `scripts/model_report.py`, `scripts/model.lp`, `scripts/model_check.py`, `scripts/workqueue_request.py`,
  `tests/scripts/test_model_spec.py`, `tests/scripts/test_model_restates.py`,
  `tests/scripts/test_workqueue_request_parse.py` (new), `tests/scripts/test_model.py`,
  `tests/scripts/test_model_reading.py`, `tests/scripts/test_model_output.py`, `tests/scripts/test_model_withdrawn.py`,
  `tests/scripts/test_model_glossary.py`, `tests/scripts/test_workqueue_request_asker.py`,
  `tests/scenarios/design_model_check_*.py`, `tests/scenarios/test_design_model_check.py` (only to follow output changes).
- **Depends on:** P2, P3, P4.
- **Accept:**
  - `python3 -m pytest -q tests/scripts/test_model_spec.py tests/scripts/test_model_restates.py tests/scripts/test_workqueue_request_parse.py`
  - `python3 scripts/model parse "When the person runs \`work start\` on an initiative that is \`proposed\`, \`work\` shall set its status to \`started\`."`
    exits 0 and prints one tree.
  - `python3 scripts/model parse "When the person runs \`work start\` on an initiative that is \`drafted\`, \`work\` shall set its status to \`started\`."`
    exits 1, and its output contains `` `drafted` ``.
  - `python3 scripts/model lexicon --check` exits 0 on the live repo.
  - `python3 scripts/model restates spec-migration` exits 1 on the live repo (nothing restated yet), and names
    `spec-migration#r1`.
  - In a fixture repo whose index is codified, `work request` with a non-parsing line exits 1, names the line, and
    writes no file (in `test_workqueue_request_parse.py`).
  - The no-new-rows check of P3 passes against the live repo.

### P6 The logic check
- **Goal:** design §12.
  - `spec_logic.py`: one translation per core and typed fun, and the guards `on(r<n>)`/`on(U<n>)`.
  - `spec_solve.py`: the copied grounding loop (telingo's MIT notice kept), one solve at H = 3 with assumptions and
    `on_core`, the per-group witness, L1–L3, L4 as a graph search, and text and JSON reports.
  - `grammar/background.lp`: frame axioms with stutter steps, resources and transitions. The lexicon facts are
    generated.
- **Owns:** `scripts/spec_logic.py`, `scripts/spec_solve.py`, `grammar/background.lp`,
  `tests/scripts/test_spec_logic.py`, `tests/scripts/test_spec_solve.py`, `tests/scripts/fixtures/logic/` (all new).
- **Depends on:** P2, P3.
- **Interface it provides:** `spec_solve.run(root, capability=None, extra=None) -> [Finding(code, ids, text)]`
  (`extra`: drafted capability files, for the integrate check), and `spec_solve.report(findings, as_json) -> (text,
  exit)`.
- **Accept:**
  - `python3 -m pytest -q tests/scripts/test_spec_logic.py tests/scripts/test_spec_solve.py`. The fixture is the
    spike's cluster rewritten in the codified language (`tests/scripts/fixtures/logic/cluster/`), and the tests find:
    - the r66/r95 restatements as an L2 duplicate;
    - "one stage of an initiative at a time" against "start the research stages together" as an L1, with the core
      naming both ids;
    - no L1 finding for the resource formulation (spec lock and initiative lock held, U2);
    - a `Set` off the transition table as L3;
    - a pre-state value with no incoming transition path as L4.
  - On a 40-group fixture, `run` finishes in under 10 s (asserted in the test).

### P7 Gherkin generation and the step vocabulary
- **Goal:** design §14.
  - `grammar/Steps*.gf`: templates, with kind words in every instance mention, and `GivenCodeText` for indented
    blocks.
  - `features_generate.py`: deterministic, witnesses by rule, the `given` fence with docstrings and tables,
    logic-only groups via `spec_tree`, per-file dispatch, `--check` and `--preview`, with the exit codes of §13.4.
  - `features_vocab.py`: Steps funs → (template, kind) patterns, and `vocab --check [<feature>…]`.
  - `features generate` and `features vocab` in `scripts/features`.
  - `tests/scenarios/vocab.py`: pytest-bdd registration and the handler registry.
  - Shared world handlers for the domain kinds (initiative, work-item, request, capability-proposal,
    glossary-proposal, capability, term, design-decision, record), copied from today's world helpers. Today's step
    modules are not edited.
  - `conftest.py`: marks registered from the spec, `*_handlers*.py` imported by glob, and the U3/U8 checks after each
    scenario.
  - After this layer, `conftest.py`, `vocab.py` and `world_*.py` are frozen (§14.3).
- **Owns:** `grammar/Steps.gf`, `grammar/StepsEng.gf`, `scripts/features_generate.py`, `scripts/features_vocab.py`
  (new), `scripts/features`, `tests/scenarios/vocab.py`, `tests/scenarios/world_*.py` (new),
  `tests/scenarios/conftest.py`, `tests/scripts/test_features_generate.py`, `tests/scripts/test_features_vocab.py`,
  `tests/scripts/fixtures/generate/` (new), `tests/scripts/test_bound.py`.
- **Depends on:** P2, P3.
- **Accept:**
  - `python3 -m pytest -q tests/scripts/test_features_generate.py tests/scripts/test_features_vocab.py`. The tests
    cover:
    - a fixture codified capability generates byte-identical output twice;
    - editing one group changes only that scenario's lines;
    - `--check` exits 1 after a hand edit;
    - naming an uncodified capability exits 2 and writes nothing;
    - the spike's G1 gives the four-initiative witness;
    - an `If` group gives the invalid input;
    - a `given` block with a table and a docstring;
    - two kinds with the same template give two distinct patterns;
    - a fixture repo with one generated feature plus `<cap>_handlers.py` passes under pytest, end to end;
    - `features vocab --check` names a missing handler.
  - `tests/scripts/fixtures/generate/broken/` is a codified fixture repo with one non-parsing requirement, for the layer
    gate.
  - `python3 scripts/features generate --check` on the live repo exits 0, and prints one `skipped <c>: not codified`
    line per service capability (10 today).

**Layer 2 gate:**
- `python3 scripts/model --root tests/scripts/fixtures/logic/cluster logic --json` gives the findings P6's test asserts;
- `python3 scripts/model --root tests/scripts/fixtures/generate/broken check 2>&1 | grep -q '^v_p1 '` (P7's fixture
  has one non-parsing line);
- `python3 scripts/features generate --check` exits 0 on the live repo;
- the suite is at baseline.

## Layer 3: the flow, and 18 of 19 capabilities

Moved lines follow design §16.2's rule in every package: a spec-integration line goes to the capability owning the
script it names (`model` → design-model-check, `features` → feature-file-tools, `work run` → supervision). P9 lists
the move, and the target's package restates it. Both sides apply the rule on their own, and the layer gate's
`model restates` catches a mismatch, which the orchestrator fixes on `gf-conversion`. A conversion package puts its
handlers in `tests/scenarios/<cap>_handlers*.py` and does not touch `conftest.py`, `vocab.py` or `world_*.py`.

### P8 The flow: integrate check, scripted formulate, drafting, agents and skills
- **Goal:** design §13.
  - `uncodified()` in `supervise_outputs.py`: parse plus `spec_solve.run(extra=drafts)` after an integrate round, with
    send-back and then a question;
  - `supervise_formulate.py` and its call from `supervise_rounds.py` for kind `formulate`, with no session;
  - removal of the formulation-question paths;
  - `supervise_draft.py`: retires from `removes`;
  - `supervise_brief.py`: codified wording, the normal form of each line for intake, the gate preview;
  - `work_items.py`: `accepts` of groups and marks from the spec;
  - the agent and skill changes of §13.1–§13.2, the new `raising-a-request` skill, and every mention of
    `feature-formulator` outside README.md.
- **Owns:** `scripts/supervise_formulate.py` (new), `scripts/supervise_rounds.py`, `scripts/supervise_outputs.py`,
  `scripts/supervise_brief.py`, `scripts/supervise_draft.py`, `scripts/supervise_intake.py`,
  `scripts/supervise_worker.py`, `scripts/work_items.py`, `agents/capability-writer.md`, `agents/initiative-round.md`,
  `agents/feature-formulator.md` (delete), `agents/spec-checker.md`, `skills/formulating-features/`,
  `skills/integrating-a-proposal/`, `skills/checking-spec-consistency/`, `skills/bdd-red-green/`,
  `skills/delivering-an-initiative/`, `skills/migrating-to-capabilities/`, `skills/raising-a-request/` (new),
  `tests/scripts/test_supervise_formulate.py` (new), `tests/scripts/test_supervise_draft.py` (new),
  `tests/scripts/test_supervise_outputs.py`, `tests/scripts/test_work_items.py`, `tests/scripts/test_work_items_worker.py`,
  `tests/scripts/test_agents.py`, `.shop/records/2026-11-03-gf-conversion/p8-broken.md` (new).
- **Depends on:** P5, P6, P7.
- **Accept:**
  - `python3 -m pytest -q tests/scripts/test_supervise_formulate.py tests/scripts/test_supervise_draft.py tests/scripts/test_supervise_outputs.py tests/scripts/test_work_items.py tests/scripts/test_work_items_worker.py tests/scripts/test_agents.py`
  - The suite is at baseline except in `tests/scenarios/test_supervision.py`, which P12 rewrites. Each supervision
    failure P8 adds is listed in `p8-broken.md`.
  - `! grep -rn 'feature-formulator' agents skills scripts tests`
  - `! grep -n NOTHING_FORMULATED scripts/*.py`
  - `test -f skills/raising-a-request/SKILL.md && grep -q 'model parse' skills/raising-a-request/SKILL.md`

### P9 Convert the 11 guarantees capabilities
- **Goal:** design §16.
  - Convert code-research, delivery, formulation, planning, red-green, review, role-boundaries, spec-consistency,
    spec-integration, spec-migration and trials to codified groups. Each file gets fresh ids, `Restates:`,
    `## Dropped` and its marker, and no feature.
  - formulation's lines are dropped or `moved to supervision`, and spec-integration's script lines are moved by the
    rule above.
  - Delete `features/spec-consistency.feature` (unbound today) and `features/spec-integration.feature`, with its step
    modules and test file.
- **Owns:** those 11 `spec/capabilities/*.md`, `features/spec-consistency.feature`, `features/spec-integration.feature`,
  `tests/scenarios/spec_integration_*.py`, `tests/scenarios/test_spec_integration.py` (all deleted),
  `tests/scripts/test_spec_guarantees.py` (new: the 11 files parse, are codified and are logic-clean).
- **Depends on:** P5, P6.
- **Accept:**
  - for each of the 11: `python3 scripts/model parse --file spec/capabilities/<c>.md`, `python3 scripts/model logic <c>`
    and `python3 scripts/model restates <c>` exit 0;
  - `python3 -m pytest -q tests/scripts/test_spec_guarantees.py`.

### P10 Convert the small service capabilities, and remove `features`' editing commands
- **Goal:**
  - Convert analysis-tools, batch-measurement, feature-file-tools and migration-tools: codified spec, generated
    features, handlers, and the old step modules deleted. feature-file-tools restates the spec-integration lines the
    rule moves to it.
  - Remove `tag`, `move`, `deprecate`, `retire`, `rebind` and `verify-moved`, with their requirements, code and tests.
- **Owns:** those 4 `spec/capabilities/*.md` and `features/*.feature`; `tests/scenarios/analysis_tools_*`,
  `batch_measurement_*`, `feature_file_tools_*`, `migration_*`, the `<cap>_handlers*.py` of the four, and
  `test_analysis_tools.py`, `test_batch_measurement.py`, `test_feature_file_tools.py`, `test_migration_tools.py`;
  `scripts/features`, `scripts/features_edit.py`, `scripts/features_bindings.py`, `scripts/features_report.py`;
  `tests/scripts/test_features.py`, `tests/scripts/test_features_deprecating.py`, `tests/scripts/test_features_scenarios.py`.
- **Depends on:** P5, P6, P7.
- **Accept:**
  - for each of the 4: `python3 scripts/model parse --file spec/capabilities/<c>.md`, `python3 scripts/model logic <c>`,
    `python3 scripts/model restates <c>` and `python3 scripts/features generate --check <c>` exit 0;
  - `python3 -m pytest -q tests/scenarios/test_analysis_tools.py tests/scenarios/test_batch_measurement.py tests/scenarios/test_feature_file_tools.py tests/scenarios/test_migration_tools.py tests/scripts/test_features.py tests/scripts/test_features_deprecating.py tests/scripts/test_features_scenarios.py`
  - `python3 scripts/features vocab --check --tests tests/scenarios features/analysis-tools.feature features/batch-measurement.feature features/feature-file-tools.feature features/migration-tools.feature`
  - `for c in tag move deprecate retire rebind verify-moved; do ! python3 scripts/features $c --help >/dev/null 2>&1 || exit 1; done`

### P11 Convert the core service capabilities
- **Goal:** convert work-queue, requests and design-model-check. design-model-check is rewritten against v5, its table
  rows become statements, and it restates the spec-integration lines the rule moves to it.
- **Owns:** those 3 `spec/capabilities/*.md` and `features/*.feature`; `tests/scenarios/work_queue_*`, `requests_*`,
  `design_model_check_*`, their `<cap>_handlers*.py`, and `test_work_queue.py`, `test_requests.py`,
  `test_design_model_check.py`.
- **Depends on:** P5, P6, P7.
- **Accept:**
  - for each of the 3: `python3 scripts/model parse --file spec/capabilities/<c>.md`, `python3 scripts/model logic <c>`,
    `python3 scripts/model restates <c>` and `python3 scripts/features generate --check <c>` exit 0;
  - `python3 -m pytest -q tests/scenarios/test_work_queue.py tests/scenarios/test_requests.py tests/scenarios/test_design_model_check.py`
  - `python3 scripts/features vocab --check --tests tests/scenarios features/work-queue.feature features/requests.feature features/design-model-check.feature`

**Layer 3 gate:**
- `! python3 scripts/model check 2>&1 | grep -E '^(v_p[0-9]|v15[g-k]|v_t[4-6]) '`;
- `for c in $(ls spec/capabilities | sed 's/\.md$//' | grep -vx supervision); do python3 scripts/model logic $c || exit 1; done`;
- `python3 scripts/model restates` exits 0 (moves into supervision show as pending);
- `python3 scripts/features generate --check` exits 0 and skips only supervision;
- a cold compile of the live grammar takes under 180 s:
  `XDG_CACHE_HOME=$(mktemp -d) timeout 180 python3 scripts/model parse --file spec/capabilities/work-queue.md`.
  Otherwise the orchestrator splits `Typed` per kind before layer 4;
- the suite is green except the failures listed in `p8-broken.md`.

## Layer 4: supervision, and the upgrade step

### P12 Convert supervision
- **Goal:** convert supervision's 164 lines to codified groups, with the marker and `## Dropped`.
  - They include the formulate script, the integrate check, and the resource formulation of r20/r59/r66/r95 (spec
    lock, initiative lock, worker slots, under U1/U2).
  - Restate formulation's and spec-integration's lines moved to supervision (`formulation#r<n>@0.29`).
  - Generated feature and handlers, so `test_supervision.py` is green against P8's flow.
- **Owns:** `spec/capabilities/supervision.md`, `features/supervision.feature`, `tests/scenarios/supervision_*.py`
  (including `supervision_handlers*.py`), `tests/scenarios/test_supervision.py`.
- **Depends on:** P8, P9, P10, P11.
- **Accept:**
  - `python3 scripts/model parse --file spec/capabilities/supervision.md`, `python3 scripts/model logic supervision`,
    `python3 scripts/model restates supervision` and `python3 scripts/features generate --check supervision` exit 0;
  - `python3 -m pytest -q tests/scenarios/test_supervision.py`
  - `python3 scripts/features vocab --check --tests tests/scenarios features/supervision.feature`

### P13 The 1.0.0 upgrade step
- **Goal:** `migrate upgrade` step 1.0.0 (`migrate_upgrade_codified.py`, design §13.4, §15). It:
  - writes `spec/restated.json` when it is missing;
  - scaffolds each uncodified capability's Behaviour (one group per old line, `Restates:` filled, the old text as an
    HTML comment, no requirement bullets, no marker), and skips codified files;
  - deletes `@deprecated` scenarios;
  - rewrites pre-conversion `<cap>#r<n>` references in `.shop/work/**` to `<cap>#r<n>@0.29`;
  - reports what is left for a session to write (the capabilities and the untyped glossary).
  - Its requirement group goes into `migration-tools.md`, with the generated scenario and a handler.
- **Owns:** `scripts/migrate_upgrade.py`, `scripts/migrate_upgrade_codified.py` (new),
  `tests/scripts/test_migrate_upgrade_codified.py` (new), `tests/scripts/test_migrate_upgrade.py`,
  `spec/capabilities/migration-tools.md`, `features/migration-tools.feature`, `tests/scenarios/migration_*.py`
  (including `migration_tools_handlers*.py`), `tests/scenarios/test_migration_tools.py`.
- **Depends on:** P10, P11.
- **Accept:**
  - `python3 -m pytest -q tests/scripts/test_migrate_upgrade_codified.py tests/scripts/test_migrate_upgrade.py tests/scenarios/test_migration_tools.py`.
    The tests cover a copy of the repo at 96818f71: one commit writes the scaffold and `spec/restated.json`, rewrites
    the references and reports the capabilities left. They also cover a run on an already-converted fixture that
    changes only references and the plugin version;
  - `python3 scripts/model parse --file spec/capabilities/migration-tools.md`, `python3 scripts/model logic migration-tools`
    and `python3 scripts/features generate --check migration-tools` exit 0.

**Layer 4 gate:**
- `! python3 scripts/model check 2>&1 | grep -E '^(v_p[0-9]|v15[g-k]|v_t[4-6]) '`;
- `python3 scripts/model logic` exits 0;
- `python3 scripts/model restates` exits 0 with nothing pending;
- `python3 scripts/features generate --check` exits 0, and `! python3 scripts/features generate --check | grep -q skipped`;
- `python3 -m pytest -q` is all green.

## Layer 5: the release

### P14 The release: legacy removal, v_p0, version, docs, smoke
- **Goal:**
  - delete `model_legacy.py` and every uncodified path, and add v_p0 (§13.4). `work request` and `features generate`
    refuse an uncodified file, naming `migrate upgrade`;
  - run `python3 scripts/migrate upgrade` on this repository (old references and `.shop/plugin-version`);
  - set `.claude-plugin/plugin.json` to 1.0.0;
  - add a README section with the upgrade notes, and remove `feature-formulator` from README.md;
  - write the CLAUDE.md module map rows for every new module (from P1–P13's reports);
  - update the `migrate_session.py` text if it names formulation;
  - sweep with `tools check` for dead code;
  - add the smoke test of the other tools on the converted spec (design §18, point 22).
  - P14 is alone in its layer. Its list below is what it expects to change; any other file the sweep needs is listed
    in its report.
- **Owns:** `scripts/model.lp`, `scripts/model_check.py`, `scripts/model_spec.py`, `scripts/model_parse.py`,
  `scripts/model_legacy.py` (delete), `scripts/model_facts.py`, `scripts/workqueue_request.py`,
  `scripts/workqueue_lines.py`, `scripts/features_generate.py`, `scripts/spec_read.py`, their tests under
  `tests/scripts/`, `tests/scripts/test_tools_codified_smoke.py` (new), `.shop/work/**` and `.shop/plugin-version` (by
  the upgrade run), `.claude-plugin/plugin.json`, `README.md`, `CLAUDE.md`, `scripts/migrate_session.py`.
- **Depends on:** P12, P13.
- **Accept:**
  - `python3 -m pytest -q tests/scripts/test_tools_codified_smoke.py`. It runs, on the live repo:
    `measure show .shop/records/measurements/<first kept record>`, `tools map --json`, `tools tests-of scripts/work`,
    `tools untested --json`, `features count`, `features list` and `features bindings`. Each must exit 0 with
    non-empty output;
  - `! grep -rn 'model_legacy\|def ears' scripts`
  - `! grep -n 'feature-formulator' README.md`
  - `grep -q '"version": "1.0.0"' .claude-plugin/plugin.json`
  - `python3 scripts/tools check` exits 0;
  - every Python module in `scripts/` has a CLAUDE.md row, by name or by a `<prefix>*` row (today `supervise.py` has
    none, so P14 adds it): `for m in $(ls scripts | grep -E '\.py$'); do grep -q "$m" CLAUDE.md || grep -q "$(echo $m | sed 's/_.*//')\*" CLAUDE.md || { echo "no row: $m"; exit 1; }; done`;
  - `python3 scripts/model check` reports no violation that the 1.0.0 conversion introduced:
    `! python3 scripts/model check 2>&1 | grep -E '^(v_p[0-9]|v15[g-k]|v_t[4-6]|v_s[1-3]|v15f) '`.

**Layer 5 gate:**
- `python3 -m pytest -q` is all green;
- `python3 scripts/tools size --limit 300` exits 0;
- the P14 `model check` grep, and `python3 scripts/model logic`, `python3 scripts/model restates` and
  `python3 scripts/features generate --check` all exit 0 on the live repo.

## Layer 6: end to end

### P15 A new request through the new requirements system (the test)
- **Goal:** prove the brief's "done means" with a test. `tests/scripts/test_e2e_codified.py` runs in a temporary clone
  of a small codified fixture context (two capabilities, `universal.md`), with the stand-in claude
  (`SHOPSYSTEM_WORK_CLAUDE`, `STUB_CLAUDE_PLAN`):
  1. `work request` with one non-parsing line is refused, with the hint;
  2. `work request` with codified lines is accepted;
  3. `work run`'s intake round, whose stub writes accepted outcomes, then `work start`;
  4. the integrate round, whose stub drafts a group with one line the logic check refuses. It is sent back, and then
     drafts a clean group;
  5. the gate, with the person's approval given through `work answer`;
  6. the apply round;
  7. the scripted formulate: the real GF parses, and `features generate` writes the scenario tagged `@g<n> @r<n>`;
  8. a work-item drafted with `accepts` from the change list;
  9. delivery through the stub research, plan and implement stages, where the implementer stub adds the handler and
     code, then the merge with `--work-item`, the branch review, and done;
  10. `work resolve`.
  The final assertions cover the request's `delivered` status, the generated feature, clean `model check` and
  `model logic`, and the initiative `done`.
- **Owns:** `tests/scripts/test_e2e_codified.py`, `tests/scripts/fixtures/e2e/` (new).
- **Depends on:** P14.
- **Accept:** `python3 -m pytest -q tests/scripts/test_e2e_codified.py`, and the full suite stays green.

### P16 The live run (evidence, not a gate)
- **Goal:** on a scratch branch off `gf-conversion`, never pushed or merged:
  - write a real one-line request with the `raising-a-request` skill;
  - raise it with `work request`;
  - run `work run` with the real `claude`;
  - record what happened, with costs, in `e2e.md`. If the run cannot finish (for example, the budget runs out),
    `e2e.md` says where it stopped.
- **Owns:** `.shop/records/2026-11-03-gf-conversion/e2e.md` (new), on `gf-conversion`. Everything else stays on the
  scratch branch.
- **Depends on:** P14.
- **Accept:** `grep -qE 'q[0-9]+' .shop/records/2026-11-03-gf-conversion/e2e.md && grep -qE 'i[0-9]+' .shop/records/2026-11-03-gf-conversion/e2e.md`
  (the request id and the initiative id are named).

## Summary

| layer | packages (parallel) | what it gives |
|---|---|---|
| 1 | P1 toolchain, P2 grammar and parser, P3 format, glossary and v5 docs, P4 graph rules v5 | the language and the model, apart |
| 2 | P5 model reads codified, P6 logic check, P7 generation and vocabulary | the tools speak the language |
| 3 | P8 flow, P9 guarantees, P10 small service, P11 core service | the flow, and 18 of 19 capabilities |
| 4 | P12 supervision, P13 upgrade step | the whole spec |
| 5 | P14 release | legacy gone, 1.0.0 |
| 6 | P15 end-to-end test, P16 live run | a request through the new system |

Risks to watch, in order:

1. **Grammar coverage during conversion.** The grammar is frozen inside a layer, under the growth rule. A missing
   construct needed by two or more packages is raised to the orchestrator, which makes one grammar change on
   `gf-conversion` and rebases the layer.
2. **Size of P12.** If supervision cannot be done in one package, split it by section (rounds; pool and resources;
   merge and review) into P12a–c. Each sub-package owns disjoint `supervision_*` modules, and one of them keeps the
   spec file.
3. **Grammar size.** P2 records cold compile time and pre-guard ambiguity, and the layer 3 gate bounds the live
   compile.
4. **Determinism of generation.** P7's byte-identity test is the guard.
5. **Platform.** Linux x86_64 only, by design (§11.2).
