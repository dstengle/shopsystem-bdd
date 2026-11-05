# CLAUDE.md

## Size limit

Code and test files, every tracked Python file, stay at 300 lines or fewer. `python3 scripts/tools size --limit 300` prints each one over it with its line count and exits 1 when there is any. A change does not push a file over the limit; a file that is over it already is split by the work that names it.

## Module map

| Module | Concern |
|---|---|
| `scripts/tools` | the `tools` command: its contract and argument parsing |
| `scripts/tools_env.py` | the project's interpreter, `probe` and `install` |
| `scripts/tools_grammar.py` | the grammar tools: GF 3.12 and the pinned pgf and clingo wheels, installed (`tools install`) and probed (`tools probe`'s grammar block, `--json`), and GF's lookup (`gf_binary`) |
| `scripts/tools_map.py` | the coverage map: `map`, `tests-of`, `untested` |
| `scripts/tools_refs.py` | `refs` |
| `scripts/tools_check.py` | `check`: ruff, vulture, import-linter |
| `scripts/tools_size.py` | `size`: tracked Python files over a line limit |
| `scripts/features*.py` | the `features` command: Gherkin reading, bindings, reports |
| `scripts/features_generate.py` | `features generate`: a codified capability's groups written as scenarios read off their facts by `spec_steps`, with no solver, example data first, byte-stable, and the groups no step words given to a caller (`skipped`); an uncodified capability refused, naming `migrate upgrade` |
| `scripts/features_vocab.py` | the step vocabulary: a step read back into its template, kind and term, the (template, kind) patterns (design §14.1, §14.3) |
| `scripts/features_vocab_gf.py` | the generated StepsTyped module: for each kind its instance mention and Given templates, and for each attribute slot its Given (design-r2 §4.4) |
| `grammar/` | the plugin's GF sources: the core requirement grammar (`Core`, `Req`) and the step grammar (`Steps`), each with its English; `check.lp`, the fixed meta-encoding of `model logic` over a context's facts (two states, candidate pairs, unification with functional relations and definites, `every`/`no` read through a `Def`, L1, L3-L6); `corpus/`, the sentences the grammar must parse and refuse |
| `scripts/spec_lexicon.py` | the lexicon of a bounded context, the one reader of term entries: the typed `## Glossary` of `spec/index.md` and each capability's `## Terms`, identifiers (`ident`), a condition's definition sentence and the lexicon's problems (v_t4-v_t7, v_t9) |
| `scripts/spec_relations.py` | the relations of a context: the `## Relations` tables, `Kind of:` expanded to subkinds, and v_t8 (a relation entry) and v_t10 (design-r2 §4.2, §8) |
| `scripts/spec_typed.py` | the generated GF modules of a lexicon: `Lex` and `Typed`, each with its English, a relation row's modifier and clause funs |
| `scripts/spec_typed_def.py` | the generated Def grammar: a condition defined in the controlled language, and the refusal of a definition that says "it" (design-r2 §4.3) |
| `scripts/spec_grammar.py` | a context's requirement grammar: compile and cache, tokenise, parse with the guards, linearise, and the hint a refusal carries |
| `scripts/spec_parse_cache.py` | GF's parse of a line kept on disk for `spec_grammar`, shared by processes, keyed by the grammar's sources, the grammar, the lexicon's words and the text |
| `scripts/spec_tree.py` | requirement trees: the post-parse guards, normalised trees and `logic_only` |
| `scripts/spec_read.py` | the codified spec files read: a capability's groups, requirements, `Restates:` and `## Dropped`; `spec/universal.md`; `spec/restated.json`; the per-file marker `language: codified-1` |
| `scripts/spec_read_given.py` | a codified group's given block read for spec_read, and the shape test of example data (v15m; design-r2 §9.1) |
| `scripts/spec_unbuilt.py` | a capability's `unbuilt:` ids, their problems, the strict xfail mark the pytest plugin puts on their scenarios, and ids appended to a capability file's `unbuilt:` (`with_unbuilt`) |
| `scripts/spec_logic_vocab.py` | the lexicon's side of the logic: typed funs traced to their lexicon entries, and `domain`, the domain facts for `grammar/check.lp` (kinds, sub-kinds, actors, values, transitions, `initial/3`, `fun/1` for a functional relation) |
| `scripts/spec_facts.py` with `scripts/spec_facts_np.py` | a requirement tree as ground facts, one translation per fun (design-r3 §3): roles, pre-state, trigger, responses, sets, `every`, `none`, `the` (a definite with no antecedent), a universal under `every` in a clause; a choice split into `R#n` (`split`); a `Def` condition recorded (`define`) and followed where it is positive, and as domain facts (`def_facts`: `prose`, `dalt`, `dlit`); an unknown fun refused naming it |
| `scripts/spec_context.py` | a context read once per state of its files (`load`): the vocabulary, the codified capabilities with drafted files laid over them, each statement parsed and translated into facts, the refused requirements, the domain facts |
| `scripts/spec_solve.py` | `model logic`, facts → `check.lp` → findings, L1-L6: one brave clingo solve of the context's facts and `grammar/check.lp` (`solve`, its 20 s limit and L0) and each L1's (L6's) witness a solve of that one grounding with the external `focus` (`focusm`) set, the shown atoms read into L1, L3-L6, L2 on normalised trees, the text and JSON reports (design-r3 §6) |
| `scripts/spec_findings.py` | the words of `model logic`'s findings: a shown atom of `check.lp` written with the lexicon's terms, an L1's trigger, merged pre-state and why, an L6's prose condition |
| `scripts/spec_steps.py` with `scripts/spec_steps_facts.py` | a group's requirements as Gherkin steps (design-r3 §5): each requirement's facts read into atoms (`spec_steps_facts`: instances, fluents, the trigger, responses, the contrast of an `every` role) and the atoms into Givens, a When and Thens by the table from atom predicate to Steps fun, instances named in order of first mention |
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
| `scripts/backlog_items.py` | one item of the backlog: its file `.shop/backlog/b<n>.md` read (`parse`, a malformed file refused naming the file and the field) and written (`render`), its label `b<n> "<title>"`, numbering and its one-path commit; the request an item was taken in from (`request`, `asked_by`) |
| `scripts/backlog_moves.py` | the commands that change an item (`work idea`, `shape`, `refuse`, `withdraw`, `answer`, `rate`, `depend` and its `--drop`, `ready`), each one commit of its file; a dependency that closes a cycle refused, and `work ready` refused with the bar's reasons |
| `scripts/backlog_cli.py` | the backlog's commands of `work`: their parsers, dispatch and what they print, `work show b<n>` |
| `scripts/backlog_view.py` | `work backlog`: the score, the rank within a state, an item's blockers, how far an in-batch item's batch is along (`progress`), the tables by state and the JSON |
| `scripts/backlog_lines.py` | an item's requirement lines: its `## Requirements` blocks read and written, `work line` giving a line (or a term bullet) the next ids of its codified capability, the blocks laid over a copy of `spec/` (`lay`, with other items under it) or over a spec in place (`lay_onto`), and its ids renumbered past a capability's and other items' (`renumber`) |
| `scripts/readiness_bar.py` | the readiness bar: an item's request lines settled, and its lines well-formed (they parse, `model logic` finds no L0 nor an L1 naming them, `features generate` writes their groups' scenarios), checked on a temporary copy of `spec/` with the lines laid in; the reasons `work ready` names |
| `scripts/intake_moves.py` | intake: `work intake`, a request of this context taken in as a `shaped` item (its provenance read off the asker), the item a request was taken in from (`linked`), and the item side of `work outcome`; this context's own request to its upstream, and a word that is not a line outcome, refused |
| `scripts/batch_git.py` | a batch's git plumbing: `git` and `GitFailed` (moved from `supervise_worker`, which imports them back), `.shop/delivery.toml` (`delivery`), the lock every committing batch command holds (`locked`), the worktrees directory and its worktrees, the remote and the push |
| `scripts/batch_gh.py` | a batch's `gh` calls through `$SHOPSYSTEM_WORK_GH`: a draft pull request created, its state and merge commit read, it closed |
| `scripts/batch_plan.py` | the batch and its plan, `.shop/batches/<n>/plan.md`: read (`parse`, a malformed file refused naming the file and the field) and written (`render`), the batches found by name, the open one and an item's, the base-branch check, and the commit of the plan with the items it moves |
| `scripts/batch_pick.py` | the pick of `work batch start`: the `ready` items in rank order up to `batch_size`, a blocked item passed over unless what blocks it is picked first, the bar checked again alone and laid over the items picked before (`readiness_bar.check`'s `others`), ids renumbered (`backlog_lines.renumber`); it writes nothing |
| `scripts/batch_start.py` | `work batch start`: under the lock, the pick laid on a new branch `batch-<n>` in its own worktree (lines into `spec/`, ids into `unbuilt:`, features generated, one commit citing each item), then the batch file with the moved items committed on the base; the branch and worktree removed on a failure |
| `scripts/batch_tasks.py` | `work batch resume`, `done` and `park`: one task an item in its worktree `batch-<n>-t<k>` on its branch, a lost worktree given back, a task done once its worktree is clean, its commits cite the item and leave `.shop/` alone, its ids are built and the tests pass (run outside the lock), an item parked with its question; the checks `work batch review` shares |
| `scripts/batch_review.py` | `work batch review`: every task of an in-batch item done and its commits cited, their branches merged into `batch-<n>` in the batch's worktree, the tests, the push and the draft pull request (its title and body), the batch `in-review`; a refusal while merging, testing, pushing or creating puts the branches back |
| `scripts/batch_merge.py` | the merge of an item's branch into the batch branch, `--no-ff` citing the item, with the conflict of two items' `unbuilt:` lines of one capability settled |
| `scripts/batch_close.py` | `work batch merged` (gh says the pull request is merged and its merge commit is in the base: the in-batch items delivered, the batch merged, its worktrees and merged item branches removed) and `work batch abandon` (its pull request closed, its in-batch items ready again) |
| `scripts/batch_cli.py` | the batches' commands of `work`: `work batch <command>`'s parsers, dispatch and what each prints, `work batch status` (text and `--json`) |
| `scripts/work_items.py` | the pytest plugin of `--work-item`, loaded by `work run`'s tests and this repository's conftest |
| `scripts/measure` with `scripts/measure_*.py` | the `measure` command: `initiative` (reading `measure_read.py`, figures `measure_build.py`, the record `measure_write.py`) and `show`, `compare` (`measure_show.py`) |
| `scripts/migrate*.py` | the `migrate` command |
| `scripts/migrate_upgrade*.py` | `migrate status` and `migrate upgrade`: the upgrade steps between plugin releases, one module a step |
| `scripts/migrate_upgrade_codified.py` | the 1.0.0 upgrade step "codified requirements": `spec/restated.json`, the scaffold of each uncodified capability, `@deprecated` scenarios deleted, old references written `<cap>#r<n>@0.29`, and what is left reported |
| `hooks/hooks.json` | the plugin's SessionStart hook, running `migrate status --hook` |
| `tests/scenarios/` | the generated features' tests: one `test_<capability>.py` a capability, its handlers in `<capability>_handlers*.py` |
| `tests/scenarios/vocab.py` | the vocabulary in pytest-bdd: step definitions matched by grammar, the handler registry (`from vocab import handler`), the marks from the spec, the U3/U8 checks after a generated scenario |
| `tests/scenarios/world_*.py` | shared handlers: the domain kinds' nodes and files (`world_nodes.py`), running a command and reading its result (`world_run.py`) |
| `tests/scenarios/<capability>_handlers*.py` | the handlers of a capability's generated feature (analysis-tools, backlog, batch-measurement, batches, design-model-check, feature-file-tools, intake, migration-tools, readiness, requests, supervision, work-queue) |
| `tests/scenarios/supervision_handlers_more.py` | supervision's Thens on what `work run` merged, logged, took, pushed, drafted, raised and removed, and the Givens of what a stage holds |
| `tests/scenarios/migration_tools_handlers_conditions.py` | migration-tools' condition Givens: a repository's primitive conditions checked against the scenario's example data, and the untracked file built |
| `tests/scenarios/<capability>_world.py` and the like | a capability's scenario repository: `analysis_tools_world.py`; `work_queue_world.py` (the repository in version control, noun phrases matched against files, `bind_all`, `local` handlers that chain); `supervision_world.py`, `supervision_build.py` and `supervision_plans.py` (the repository `work run` runs in, built from the Givens, and what the stand-in claude does in it); `backlog_world.py` (items written as `.shop/backlog/` files, the scenario's `i<n>` as `b<n>`, the items a scenario names written before its command); `readiness_world.py` (the codified spec of the generate fixture written over `spec/`, an item given requirement lines, `work` run with no input); `batches_world.py` (a bare remote and the stand-in gh beside the repository, and the batches, tasks, commits and pull requests a scenario names built before its command) |
| `tests/toolchain.py` | the grammar tools the suite needs: `require()` fails a test, never skips it, naming `tools install` |
| `tests/scripts/` | tests of the scripts that no scenario drives; `stub_gh.py`, the stand-in `gh` the batch tests run as `$SHOPSYSTEM_WORK_GH`, and `batch_testing.py`, what they share |

A new concern gets a new module and a row here.
