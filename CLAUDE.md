# CLAUDE.md

## Size limit

Code and test files, every tracked Python file, stay at 300 lines or fewer. `python3 scripts/tools size --limit 300` prints each one over it with its line count and exits 1 when there is any. A change does not push a file over the limit; a file that is over it already is split by the work that names it.

## Module map

| Module | Concern |
|---|---|
| `scripts/tools` | the `tools` command: its contract and argument parsing |
| `scripts/tools_env.py` | the project's interpreter, `probe` and `install` |
| `scripts/tools_grammar.py` | the grammar tools: GF 3.12 and the pinned pgf, clingo and telingo wheels, installed (`tools install`) and probed (`tools probe`'s grammar block, `--json`), and GF's lookup (`gf_binary`) |
| `scripts/tools_map.py` | the coverage map: `map`, `tests-of`, `untested` |
| `scripts/tools_refs.py` | `refs` |
| `scripts/tools_check.py` | `check`: ruff, vulture, import-linter |
| `scripts/tools_size.py` | `size`: tracked Python files over a line limit |
| `scripts/features*.py` | the `features` command: Gherkin reading, bindings, reports |
| `scripts/features_generate.py` | `features generate`: a codified capability's groups written as scenarios read off their traces (`spec_trace`), example data first, byte-stable; an uncodified capability refused, naming `migrate upgrade` |
| `scripts/features_vocab.py` | the step vocabulary: a step read back into its template, kind and term, the (template, kind) patterns (design §14.1, §14.3) |
| `scripts/features_vocab_gf.py` | the generated StepsTyped module: for each kind its instance mention and Given templates, and for each attribute slot its Given (design-r2 §4.4) |
| `grammar/` | the plugin's GF sources: the core requirement grammar (`Core`, `Req`) and the step grammar (`Steps`), each with its English; `background.lp`, the background theory of `model logic` (instances, creation, frame, running sessions, resources, `free`); `cone.lp`, a group's cone and horizon edges; `corpus/`, the sentences the grammar must parse and refuse |
| `scripts/spec_lexicon.py` | the lexicon of a bounded context, the one reader of term entries: the typed `## Glossary` of `spec/index.md` and each capability's `## Terms`, identifiers (`ident`), a condition's definition sentence and the lexicon's problems (v_t4-v_t7, v_t9) |
| `scripts/spec_relations.py` | the relations of a context: the `## Relations` tables, `Kind of:` expanded to subkinds, and v_t8 (a relation entry) and v_t10 (design-r2 §4.2, §8) |
| `scripts/spec_typed.py` | the generated GF modules of a lexicon: `Lex` and `Typed`, each with its English, a relation row's modifier and clause funs |
| `scripts/spec_typed_def.py` | the generated Def grammar: a condition defined in the controlled language, and the refusal of a definition that says "it" (design-r2 §4.3) |
| `scripts/spec_grammar.py` | a context's requirement grammar: compile and cache, tokenise, parse with the guards, linearise, and the hint a refusal carries |
| `scripts/spec_tree.py` | requirement trees: the post-parse guards, normalised trees and `logic_only` |
| `scripts/spec_read.py` | the codified spec files read: a capability's groups, requirements, `Restates:` and `## Dropped`; `spec/universal.md`; `spec/restated.json`; the per-file marker `language: codified-1` |
| `scripts/spec_read_given.py` | a codified group's given block read for spec_read, and the shape test of example data (v15m; design-r2 §9.1) |
| `scripts/spec_logic.py` with `scripts/spec_logic_np.py` | `model logic`'s translation: a requirement tree into telingo `&tel` formulas, its labels and signatures, the witness of a group, condition definitions (design-r2 §5) |
| `scripts/spec_logic_vocab.py` | the lexicon's side of the logic: typed funs traced to their lexicon entries, the context's facts for the background theory, guarded transitions, pool sizes, and `domain`, the lexicon's facts for `grammar/check.lp` (kinds, values, transitions, initial values) |
| `scripts/spec_facts.py` with `scripts/spec_facts_np.py` | a requirement tree as ground facts, one translation per fun (design-r3 §3): roles, pre-state, trigger, responses, sets, `every`, `none`; a choice split into `R#n` (`split`); a `Def` condition recorded (`define`) and followed where it is positive; an unknown fun refused naming it |
| `scripts/spec_context.py` | a context read once per state of its files (`load`): the vocabulary, the codified capabilities with drafted files laid over them, each statement parsed and translated into facts, the refused requirements, the domain facts |
| `scripts/spec_engine.py` | the solver of the codified spec: `telingo.imain` through a proxy (its own incremental horizon), cores over the `on/1` assumptions, optimal models and the least of them, the pool retry, a group's cone and its horizon bound with `grammar/cone.lp` (design-r2 §6.3) |
| `scripts/spec_solve.py` | `model logic`: L1-L4 on `spec_engine`, groups solved side by side, the text and JSON reports (design-r2 §6.4) |
| `scripts/spec_trace.py` | a group's trace for `features generate`: its cone, an optN solve projected on its labels and state-0 fluents, groups solved side by side, labels read into Givens, When and Thens (design-r2 §7) |
| `scripts/spec_trace_steps.py` | a trace's atoms as steps: the table from atom predicate to Steps fun, instances named in order of first mention (design-r2 §7.3) |
| `scripts/migrate_session.py` | the hooks' text about initiatives: `work status` at SessionStart, `migrate compacting` at PreCompact |
| `scripts/migrate_prompt.py` | the UserPromptSubmit hook's text (`migrate prompting`): a session writes a delegation the person gives with `work delegate` (requests r72) |
| `scripts/model*.py` | the `model` command: parsing, facts, checks, work, reports |
| `scripts/model_requests.py` | the reading of requests by `model`: `.shop/work/requests/q<n>.md` |
| `scripts/model_spec.py` | `model`'s reading of the codified spec: groups, requirements and their parse, universal conditions, `restated.json`, the typed glossary, generated scenarios (`@g<n>`), and a file without `language: codified-1` (v_p0) |
| `scripts/model_restates.py` | `model restates`: the coverage of the 0.29 ids by groups, `## Dropped` and moves |
| `scripts/work` with `scripts/workqueue.py` | the `work` command: the work-item queue, its statuses and log |
| `scripts/workqueue_answer.py` | `work answer` |
| `scripts/workqueue_status.py` | `work status` |
| `scripts/workqueue_list.py` | `work list` and `work show <target>`: the queue listed, an initiative or a work-item shown, the record of raised requests (`raised.jsonl`) |
| `scripts/workqueue_note.py` | `work note` |
| `scripts/workqueue_start.py` | `work start`: the initiative an accepted request begins |
| `scripts/workqueue_done.py` | an initiative done: the condition and the rewrite `work withdraw` and `work resolve` commit |
| `scripts/workqueue_request.py` | the requests of a context: `work request`, `outcome`, `ask`, `reply`, `turn`, `resolve`, `delegate` |
| `scripts/workqueue_lines.py` | `work request`'s check of its lines: each parsed in the upstream's requirement grammar, with the hint on a refusal; an upstream whose spec is not codified refused, naming `migrate upgrade` |
| `scripts/supervise.py` with `scripts/supervise*.py` | `work run`: briefs, workers, the pool of workers side by side (`supervise_pool.py`), merging, faults, the branch review, a capability-proposal's apply and formulate rounds and the integrate round's ending in drafted proposals (r91, r96), all three one at a time across initiatives (r95) (`supervise_rounds.py`) |
| `scripts/supervise_formulate.py` | `work run`'s formulate round, a script with no session: `features generate` for the proposal's service capabilities, then `--check` and `model check` with no new row, then `features/` committed; and the gate's preview of the scenarios the drafts would generate |
| `scripts/supervise_raise.py` | `work run`'s raising of the lines an integrate round gives into an upstream, its record (`raised.jsonl`) and the hold of a proposal while a request raised with it is not delivered (r135, r136) |
| `scripts/supervise_outputs.py` | `work run`'s reading of what a stage's result must give (its output) and the question naming it when missing (r131, r132); the check of an integrate round's codified drafts, parsed and logic-checked on `spec/` with the drafts laid over it |
| `scripts/supervise_branch_runs.py` | `work run`'s runs before a branch review (the suite, scenarios, checks, `tools`, `features`) and their text in the reviewer's brief (r154, r155) |
| `scripts/supervise_review_read.py` | what `work run` gives a branch review to read: its commits with their work-items, the change less `.shop/`, the files to read (r156, r157) |
| `scripts/supervise_change.py` | `work run`'s reading of an integrate round's change list and its writing of one drafted capability-proposal for each capability it names and of one drafted glossary-proposal for its glossary entries |
| `scripts/supervise_all.py` | `work run` with no initiative: every open initiative taken side by side, one `Run` each, and the exit on their statuses |
| `scripts/supervise_answers.py` | `work run`'s answers under a request's delegation: a session for each question, the answer naming the delegation |
| `scripts/supervise_glossary.py` | `work run`'s reading of an initiative's glossary-proposals: the terms of those not approved, withheld from an apply round (spec-integration r55), and the questions under a delegation that name a term or a glossary-proposal, left for the person (supervision r162) |
| `scripts/supervise_drafts.py` | `work run`'s reading of the requirement ids other initiatives' kept drafts add, given to an integrate round |
| `scripts/supervise_analysis.py` | `work run`'s measure of a finished initiative (`measure initiative`) and the analysis session that follows it |
| `scripts/supervise_done.py` | `work run`'s done: an initiative whose delivery is closed set `done` and committed |
| `scripts/supervise_intake.py` | `work run`'s intake rounds: a request this context is the upstream of, given to a session that writes its line outcomes and passes its turn |
| `scripts/supervise_draft.py` | `work run`'s drafting: the work-items of a formulated capability-proposal and of a branch review's fix-now findings |
| `scripts/work_items.py` | the pytest plugin of `--work-item`, loaded by `work run`'s tests and this repository's conftest |
| `scripts/measure` with `scripts/measure_*.py` | the `measure` command: `initiative` (reading `measure_read.py`, figures `measure_build.py`, the record `measure_write.py`) and `show`, `compare` (`measure_show.py`) |
| `scripts/migrate*.py` | the `migrate` command |
| `scripts/migrate_upgrade*.py` | `migrate status` and `migrate upgrade`: the upgrade steps between plugin releases, one module a step |
| `scripts/migrate_upgrade_codified.py` | the 1.0.0 upgrade step "codified requirements": `spec/restated.json`, the scaffold of each uncodified capability, `@deprecated` scenarios deleted, old references written `<cap>#r<n>@0.29`, and what is left reported |
| `hooks/hooks.json` | the plugin's SessionStart hook, running `migrate status --hook` |
| `tests/scenarios/` | the generated features' tests: one `test_<capability>.py` a capability, its handlers in `<capability>_handlers*.py` |
| `tests/scenarios/vocab.py` | the vocabulary in pytest-bdd: step definitions matched by grammar, the handler registry (`from vocab import handler`), the marks from the spec, the U3/U8 checks after a generated scenario |
| `tests/scenarios/world_*.py` | shared handlers: the domain kinds' nodes and files (`world_nodes.py`), running a command and reading its result (`world_run.py`) |
| `tests/scenarios/<capability>_handlers*.py` | the handlers of a capability's generated feature (analysis-tools, batch-measurement, design-model-check, feature-file-tools, migration-tools, requests, supervision, work-queue) |
| `tests/scenarios/supervision_handlers_more.py` | supervision's Thens on what `work run` merged, logged, took, pushed, drafted, raised and removed, and the Givens of what a stage holds |
| `tests/scenarios/migration_tools_handlers_conditions.py` | migration-tools' condition Givens: a repository's primitive conditions checked against the scenario's example data, and the untracked file built |
| `tests/scenarios/<capability>_world.py` and the like | a capability's scenario repository: `analysis_tools_world.py`; `work_queue_world.py` (the repository in version control, noun phrases matched against files, `bind_all`); `supervision_world.py`, `supervision_build.py` and `supervision_plans.py` (the repository `work run` runs in, built from the Givens, and what the stand-in claude does in it) |
| `tests/toolchain.py` | the grammar tools the suite needs: `require()` fails a test, never skips it, naming `tools install` |
| `tests/scripts/` | tests of the scripts that no scenario drives |

A new concern gets a new module and a row here.
