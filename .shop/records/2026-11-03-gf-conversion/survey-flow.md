# Survey: the request-to-delivery flow, and what the GF conversion touches

Date: 2026-11-03. Branch `gf-conversion`. Read-only survey; no code changed. Read with `brief.md` beside it.

Question: where in the flow are free-English Behaviour lines or hand-written Gherkin written, read or checked; what
changes if lines are codified requirements GF parses and Gherkin is generated; what can stay as it is.

## 1. The flow as it stands

1. **Raise.** `work request <title> --lines <file>` -> `scripts/workqueue_request.py:130-163` writes
   `.shop/work/requests/q<n>.md` (frontmatter, `## Lines`, `## Questions`, `## Answers`, `## Outcomes`,
   `## Resolution`). Every line must pass `model_parse.ears(line)` (`workqueue_request.py:143-145`), a regex EARS
   shape check (`model_parse.py:216-264`): one `shall`, one sentence, clauses Where/While/When/If in order. This is
   spec `requests#r2` (`spec/capabilities/requests.md:34`). An integrate round that needs an upstream raises a
   request the same way: `supervise_raise.py:41-45` writes the lines to `request-lines-<n>.md` and calls
   `workqueue_request.request`, so the same check applies. Its brief asks for the lines "in strict form, worded in the
   terms of the glossary in that upstream's published spec" (`supervise_brief.py:17-20`).
2. **Intake.** `supervise_intake.py` gives each `open`/`awaiting-upstream` request to an `initiative-round` session
   of kind `intake` (brief at `:51-73`, the lines copied in as text at `:55`). The session judges each line against
   `spec/` and writes `work outcome` / `work turn` (`agents/initiative-round.md:43-44`). Questions go back with
   `workqueue_request.ask` (`supervise_intake.py:91-93`).
   `model_requests.py` reads the request files for `model check`: form and links only, never the line text.
3. **Start.** `work start` (`workqueue_start.py`) makes an initiative that `fulfils` the request.
   `workqueue_request.accepted_lines` (`:39-44`) is what later rounds are given.
4. **Integrate round** (`supervise_rounds.py:116-218`, brief `supervise_brief.py:129-141`): `initiative-round`
   dispatches `capability-writer` (`agents/capability-writer.md`), which writes **free-English EARS Behaviour lines**
   (`capability-writer.md:85-100`) as drafts of capability-file sections, plus a change list of ids. The round
   checks the writer's work by hand (`skills/integrating-a-proposal/SKILL.md` step 2): each line quotes a note
   sentence, ids numbered right, glossary entries in form. `work run` reads only the change list's **ids**
   (`supervise_change.py:17-38`) and writes `drafted` capability-proposals / a glossary-proposal (`:106-161`).
5. **Gate round** (`supervise_rounds.py:160-164`, brief `supervise_brief.py:76-82`): the session gives questions
   (decisions, readings) on the drafted lines; `work run` writes them on the proposal. The person (or a delegation,
   `supervise_answers.py`) answers.
6. **Apply round** (`supervise_rounds.py:165-184`): session copies approved drafts into `spec/`, runs
   `model decisions` and `model check` (rule rows compared before/after, SKILL step 4), commits `spec/`. `work run`
   rewrites the proposal's lists from the applied change list (`supervise_change.py:59-72`).
7. **Formulate round** (`supervise_rounds.py:185-195`): `initiative-round` dispatches one `feature-formulator` per
   capability (`agents/feature-formulator.md`, `skills/formulating-features/SKILL.md`), which **hand-writes Gherkin**
   from the Behaviour lines; the session verifies coverage one-to-one, runs each old scenario alone, deprecates
   passing ones (`features deprecate`, `features rebind`), splices, runs `features bindings` and `model check`,
   commits `features/`. `work run` checks that every added/changed requirement has a non-deprecated scenario
   (`supervise_outputs.py:59-98`, `unformulated`), else asks.
8. **Draft work-items** (`supervise_draft.py:77-97`): one work-item per capability of a `formulated` proposal,
   `accepts: [<cap>#r<n>, ...]`; retirements found from `Deprecated for:` lines of deprecated scenarios (`:26-75`).
9. **Deliver** (`supervise.py`, `supervise_pool.py`, `supervise_worker.py`, `supervise_merge.py`): research
   (`code-scout`, given `Accepted scenarios:` from `supervise_brief.py:184-217`), plan (`bdd-planner`), implement
   (`bdd-implementer` under `bdd-red-green`), task review, merge with `pytest -p work_items --work-item <w>`
   (`supervise_merge.py:20-21`; `work_items.py` selects scenarios by `@r<n>` tag and feature-file stem), branch review
   (`supervise_branch_runs.py`, `supervise_review_read.py`, `bdd-branch-reviewer`), drafting of fix work-items,
   analysis, done (`supervise_done.py`), `work resolve` (`workqueue_request.py:232-253`, the resolution is
   requirement id + version).

## 2. Every place free-English lines or hand Gherkin are written, read or checked

W = written, R = read, C = checked. "Change" is what the conversion needs.

### 2.1 Behaviour lines (free English today)

| Place | W/R/C | Today | Change under GF |
|---|---|---|---|
| `workqueue_request.py:143-145` | C | regex `ears()` per request line | Replace with the GF parse (a line that does not parse is refused naming it). Same refusal shape, so `requests#r2` keeps its meaning; reword it to "does not parse in the requirement grammar". Request lines must also be in the asker's vocabulary: a request to an upstream is parsed with the **upstream's** lexicon (from its published `index.md`), an internal one with ours. |
| `supervise_raise.py:41-45` | W | integrate result's `requests[].lines` written to a file, sent through `request()` | Unchanged code; gains the GF check through `request()`. Brief text `supervise_brief.py:17-20` ("strict form") reworded to "codified, parsing in that upstream's grammar". |
| `supervise_intake.py:51-73` | R | lines copied into the brief | Unchanged; could add each line's parse (AST/normal form) to the brief so the intake session judges a fixed reading. |
| `agents/initiative-round.md:43-44` (intake) | R | session judges English lines | Unchanged in shape; a line now has one reading, so fewer `question` outcomes. |
| `workqueue_request.py:39-44` `accepted_lines` | R | text of accepted lines | Unchanged (text is the codified line). |
| `supervise_brief.py:129-141` `integrate_lines` | R | accepted lines given to the integrate round | Unchanged. Add: the grammar/lexicon path and the `spec parse`/`spec check` command the round must run. |
| `agents/capability-writer.md:85-100` "A Behaviour line" | W | EARS English rules, refusals name reasons, glossary terms, one shall | **Rewrite.** Writer drafts codified requirement groups (spike form: `group <id> "<title>" restates <old>` + codified statements, `.shop/scratch/spike-cnl/cluster.ears`), every word from the lexicon. A word the lexicon lacks is a glossary-proposal entry (the glossary is the lexicon). The writer runs the parser on its drafts (needs a Bash tool or a `spec parse` the round runs for it; today it has Read/Glob/Grep/Write only, `capability-writer.md:4`). |
| `capability-writer.md:79-90`, `docs/capability-format.md:44-192` | W | capability file = Purpose/Behaviour/Implementation/Not yet; `- [r<n>] ...` bullets and tables | Behaviour section holds codified groups. Decide one layout: keep the capability `.md` with a fenced/marked Behaviour block the parser reads, or a sibling file. Keeping the `.md` keeps `supervise_drafts.py`, `supervise_change.unknown` (`:44-50`), `migrate_*` and the proposal machinery unchanged. Tables of commands (`behaviour_items` table rows, `model_parse.py:134-168`) need a codified equivalent (one statement a row). |
| `skills/integrating-a-proposal/SKILL.md` step 2 | C | by-hand: note quote per line, row per diff, id numbering, glossary form | Keep quote/row/id checks; **add**: every drafted line parses, and the logic check (telingo/clingo: resources, exclusivity, U-conditions) passes on spec+drafts; a failure goes back to the writer before the gate. |
| step 3 / `supervise_rounds.py:160-164` / `agents/initiative-round.md:32` (gate) | R | person shown lines in full, questions with readings | Unchanged mechanism. Questions about "two readings of one sentence" mostly vanish; questions left are decisions. Gate text could show the generated scenario beside each group (cheap: it is mechanical). |
| step 4 / apply (`initiative-round.md:34-38`) | C | `model check` before/after, rows `v_s3`/`v_s1`/`v_t1` expected | `model check` gains parse + logic rules. Expected-new rows change: `v_s3` no longer expected after apply if generation runs in the same step (see 2.2). |
| `model_parse.py:134-168` `behaviour_items`, `:216-264` `ears` | R/C | regex reading of bullets, tables, EARS shape | `behaviour_items` replaced/extended by the codified reader; `ears` retired (only callers: `model_facts.py:228`, `workqueue_request.py:144`). |
| `model_facts.py:212-232` | R/C | `req_id`, `has_req`, `req_text`, `ears_other`, `ears_many` facts | Emit facts from parse results: `req_id`/`has_req` same, `unparsed(Q)` in place of `ears_other`/`ears_many`; plus the logic facts (or a separate telingo pass). |
| `model.lp:300-301` `v_e1`, `v_e2` | C | not EARS / not one sentence | Replace with `v_p1` (does not parse). Spec `design-model-check` rows naming v_e1/v_e2 retire for new ids. |
| `model.lp:286-292` `v_t1..v_t3`, `model_facts.read_mentions` | C | avoided glossary word in a line or scenario | On lines: subsumed by the parse (lexicon words only), keep as a cheap pre-check or drop. On scenarios: generated text uses lexicon words, so always clean; the rule stays harmless. |
| `agents/spec-checker.md`, `skills/checking-spec-consistency/SKILL.md:34-64` | R/C | model judges lines vs glossary, wrong EARS pattern, line vs scenario drift | "Wrong pattern", "two readings", "drift", "another line's response" become mechanical or impossible; what stays is "left to infer" and term consistency. Shrink to the semantic residue, or retire spec-consistency's model-judge parts. |
| `bdd-task-reviewer.md:38-39`, `bdd-branch-reviewer.md:48-49`, `architecture-reviewer.md` | R | judge code against Behaviour lines | Unchanged (they read lines, now codified: easier). |
| `bdd-planner.md:29-33`, `code-scout.md:15-18` | R | requirements and scenarios by id | Unchanged. |
| `skills/migrating-to-capabilities`, `scripts/migrate_spec.py` et al. | W | migrate old repos to EARS lines with ids | Out of the request flow. The fresh converted spec (brief decision 4) is a one-off hand migration; `migrate upgrade` gains a step only if older repos must be carried. |

### 2.2 Gherkin (hand-written today)

| Place | W/R/C | Today | Change under GF |
|---|---|---|---|
| `agents/feature-formulator.md` (whole) | W | Opus session writes scenarios per line | **Retired** for generation. Possibly kept for the residue a grammar cannot generate (Background/data tables), but the brief wants it mechanical: retire. |
| `skills/formulating-features/SKILL.md` (whole) | W/C | dispatch, coverage by hand, run old scenario alone, deprecate/rebind/splice, bindings, model check, commit | **Rewrite** as a script step: `features generate` (new module) produces `features/<cap>.feature` from the parsed groups (one scenario a group, title = group title, tag `@r<n>` = group id, steps from the Steps grammar). The deprecate-a-passing-old-scenario rule (`formulation#r4`) still applies: generator must keep `@deprecated` scenarios byte for byte and splice regenerated ones; the "run old scenario alone" step stays (a pytest run, not a judgement) and can be scripted. |
| `agents/initiative-round.md:39-41` (formulate kind) | W/C | session formulates, verifies, commits | Replace the session with a **non-session round** in `supervise_rounds.py`: run generate, the pass/fail run of old scenarios, `features deprecate/rebind`, `features bindings`, `model check`, commit. `SERIAL`/`AFTER` (`supervise_rounds.py:22-23`) and the `approved -> formulated` transition stay; only the worker call at `:131` is swapped for the script for kind `formulate`. Questions from formulation disappear (a parsed group has one reading), so `NOTHING_FORMULATED` (`supervise_brief.py:26-28`), `formulated_nothing`/`sent_back` for formulate (`supervise_outputs.py:41-56`), `route` back from formulate (`supervise_rounds.py:72-76`) become dead paths; keep them inert or remove with their spec lines (supervision r112, r113, r116, r149, r152, r153). |
| `supervise_outputs.py:59-98` `scenario_ids`, `unformulated` | C | every added/changed id has a scenario | Unchanged code; now true by construction, stays as a guard. |
| `supervise_draft.py:26-75` `deprecated`, `retires`, `draft_retires` | R | `Deprecated for:` lines, replacement's tags | Unchanged if the generator writes deprecation the way `features deprecate` does. |
| `supervise_brief.py:196-217` `accepted_scenarios` | R | scenarios by `@r<n>` tag | Unchanged if tags stay `@r<n>`. |
| `scripts/features_*.py` (`features_gherkin.py` parser, `features_edit.py` tag/move/deprecate/retire, `features_bindings.py`, `features_report.py`) | R/W/C | Gherkin tooling | Reader, deprecate, retire, bindings, rebind, list, count, verify-moved all stay. `tag`/`move` lose their formulation use but harm nothing. New concern `features generate` is a new module + CLAUDE.md row (`features_generate.py`), with the GF bridge in its own module (e.g. `spec_grammar.py`: lexicon from glossary, parse, AST). |
| `model_parse.py:171-197` `scenarios`, `model_facts.py:235-266` `read_features`, `model.lp:222-227` `v_s1..v_s3` | R/C | scenario <-> requirement coverage | Unchanged; plus an optional rule "feature file differs from what generate gives" (stale generation) as a cheap `features generate --check`. |
| `work_items.py`, `supervise_merge.py:20-21` | R | select scenarios by `@r<n>` tag and feature stem | Unchanged if id and tag form stay `<cap>#r<n>` / `@r<n>`. |
| `skills/bdd-red-green/SKILL.md:10-64, 81-85, 131` | R | `.feature` is the contract, never edited; HAND-BACK on a wrong Then | Unchanged in substance. A hand-back's ruling "formulation question" (`formulating-features` hand-back template, `formulation#r10`) has no formulator any more: a wrong generated scenario is either a wrong requirement (a spec question -> integrate round) or a wrong Steps grammar/generator (a plugin defect). Update the ruling options accordingly. |
| step definitions `tests/scenarios/` (95 modules; 15 use `scenarios()`, 12 `scenario()` calls by title) | R | bound to hand-written step text and titles | **The big cost.** Generated step text comes from the Steps grammar, one phrasing per AST construct; existing step definitions match today's English. Regenerating the 10 feature files (582 Scenario lines; the other 9 capabilities are `group: guarantees`, no scenarios) changes almost every step and title, so every binding and step pattern is rebuilt. Upside: step definitions become one parser per construct (`parsers.re` per Steps-grammar linearisation), far fewer than today. |

## 3. Ids, the hinge that decides how much stays

Everything downstream keys on `<capability>#r<n>` and `@r<n>`: `supervise_change.entries` (`:17-38`, any string id),
`supervise_draft.REQUIREMENT` (`:12`), `features_gherkin.REQ_TAG` (`:10`), `accepted_scenarios`, `work_items.py`,
`model_work.py:181-221` (`accepts`), `model_requests` resolution, `workqueue_request.resolve`. **If a requirement group
takes the id `r<n>` within its capability** (fresh numbering per brief decision 4, old ids kept as `restates`), none of
these change. Universal conditions `U<n>` (decision 5) live in one file under `spec/` with no scenarios: treat it like
a `group: guarantees` capability (`supervise_outputs.is_guarantees`, `model.lp:227`) so `v_s3` and `work_items`
skip it, and have the logic check apply them to every trace.

## 4. What stays unchanged

- The request file format, its lifecycle and turns: `workqueue_request.py` apart from lines 143-145;
  `model_requests.py` entirely; `work outcome/ask/reply/turn/delegate/resolve`; `supervise_intake.py`.
- Initiatives, proposals and their statuses: `workqueue*.py`, `supervise_change.py`, `supervise_glossary.py`
  (glossary-proposals now carry lexicon entries; same files), `supervise_drafts.py`, `supervise_answers.py`,
  `supervise_raise.py` (apart from brief wording), `supervise_all.py`, `supervise_done.py`, `supervise_analysis.py`.
- The integrate -> gate -> apply sequence and its sessions (integrate's writer rules and the verification change;
  the plumbing does not).
- Delivery entirely: `supervise.py`, `supervise_pool.py`, `supervise_worker.py`, `supervise_merge.py`,
  `supervise_review*.py`, `supervise_branch_runs.py`, `supervise_faults.py`, `supervise_draft.py`, `work_items.py`;
  agents `code-scout`, `bdd-planner`, `bdd-implementer`, `bdd-task-reviewer`, `bdd-branch-reviewer`,
  `architecture-reviewer`, `delegation-answerer`; skill `bdd-red-green` (one paragraph on hand-back rulings).
- `features` tooling except a new `generate`; `model check`'s graph/work/request rules; `measure`; `tools`; hooks.

## 5. What changes, in order of dependency

1. **Grammar bridge** (new module): lexicon built from `spec/index.md` Glossary (spike `lexicon.py`), GF grammars
   (spike `gf/` Ears, Steps) compiled to PGF, `parse(line, context)` -> AST or error. GF + `pgf` Python binding as
   real dependencies (`tools_env.py` probe/install).
2. **Codified reader** in `model_parse`/`model_facts`: groups with ids, `restates`, statements; `v_p1` replaces
   `v_e1`/`v_e2`; logic check (spike `resources.lp`, telingo) as `model check` rules or a `model logic` subcommand.
3. **`work request` gate**: `ears()` -> parse (requests#r2 reworded under a new id).
4. **`features generate`** (new module) + `features generate --check`.
5. **Formulate round as a script** in `supervise_rounds.py` (no session for kind `formulate`); retire
   `feature-formulator`, rewrite `formulating-features` as the description of the script, trim
   `initiative-round.md:39-41`.
6. **capability-writer + integrating-a-proposal** rewritten for codified lines; parse + logic in step 2's verification
   and in the apply's `model check`.
7. **spec-checker / checking-spec-consistency** shrunk to the semantic residue.
8. **The converted spec**: 19 capabilities (~568 `[r<n>]` lines; supervision alone 164) rewritten as codified groups,
   regenerated features, step definitions rebuilt to the Steps grammar's phrasings. This is the bulk of the work and
   the risk to "suite green" by tomorrow.

## 6. Risks and open points

- The writer has no shell (`capability-writer.md:4`): either give it a `spec parse` it can run, or the round parses
  and sends failures back (one more round trip per failure). Recommend the round runs it and loops, as it already does
  for porcelain/change-list failures.
- Requests to an upstream must parse in the **upstream's** grammar; the published spec (`index.md`) gives the glossary,
  so the lexicon must be buildable from a foreign `index.md` alone.
- Grammar coverage: today's lines include tables of commands, code spans, quoted strings and long conditions; the
  spike covers a supervision cluster only. Lines the grammar cannot yet express need either grammar growth or an
  explicit escape (refused until the grammar grows).
- Generated feature files vs `formulation#r7` (byte-for-byte for untouched scenarios): generation must be deterministic
  and stable under unrelated spec edits, else every regeneration touches every scenario and every binding.
- Spec lines about formulation questions, formulator dispatch and formulate-round questions (formulation r1-r23,
  supervision r112-r116, r131-r132, r149-r153) retire with fresh ids in the converted spec.
