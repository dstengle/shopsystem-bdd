---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-24-a-worked-example-of-disentangling-this-repository-into-hosted-bounded-contexts
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-24
---

# A worked example of disentangling this repository into hosted bounded contexts

## Summary

This repository already has proto-bounded contexts: six areas (`spec/model/<area>.md`), each with its own model
file, its own vocabulary layer and its own capabilities. They are not yet separable, for four reasons. Each one is
measured below by `support/coupling.py`:

- **The shared vocabulary layer acts as a shared kernel.** `spec/vocabulary/shared.md` holds 79 entries naming
  elements of all six areas. It hides most cross-area use: 234 of the 543 live lines name a word another area owns
  (`the person` set aside).
- **The model points the wrong way in places.** The core area `specification` refers to `tracking` 20 times and to
  `upgrades` 13 times. The cause is objects declared in the wrong area: `requirement id`, `universal condition id`,
  `given block` and `upstream entry` sit in tracking, and `index file` and `Behaviour line` sit in upgrades.
- **Execution writes tracking's state directly.** 10 of execution's 68 lines set the status of an item or a context
  request. Its code makes 35 imports into tracking's modules and writes item files itself (`batch_start.py`,
  `batch_close.py`, `batch_plan.py`). Tracking's item lifecycle has four transitions that no tracking operation
  performs: `ready → in-batch`, `in-batch → delivered`, `in-batch → ready` and `in-batch → needs-input`.
- **The language toolchain is used by everyone.** It is 74 modules (10,750 lines, the largest group). It has 88
  imports from other groups, and specification and language import each other: 49 imports one way, 13 the other.

The working proposal holds up with two changes:

1. **Use flat, product-level ids for hosted contexts, not ids nested under the repository.** A nested id would change
   on the day the context moves out of the repository.
2. **Keep the language inside the specification context, as a module, for now.** Other contexts reach it only through
   specification's published operations. Since Shared Kernel is not allowed, the language cannot be shared directly.

The walk-through in section 4 splits work tracking from work execution:

- A driven port, `supply`, written in execution's own words, with four operations: claim, fulfil, relinquish, defer.
- Four new operations on tracking's backlog service: allocate, discharge, restore, suspend.
- An in-process adapter that maps one onto the other.
- 13 lines rewritten in the new terms. All 13 parse in grammar 4, on a copy of `spec/` in the scratchpad with the port
  added.

## 1. Inventory

### 1.1 Areas

Read from `spec/model/*.md` with `domain_model.load`, `spec/vocabulary/*.md` with `spec_vocabulary.entries`, and
the capabilities' `area:` frontmatter (full tables in `support/coupling.md` §0).

| area | kind | imports | objects | services | operations | vocab entries | capabilities (live lines) |
|---|---|---|---|---|---|---|---|
| specification | core | – | 112 | 5 | 22 | 216 | checking, consistency, decisions, parsing, reading, records, scenarios (180) |
| tracking | supporting | specification | 48 | 4 | 54 | 163 | items, drafting, context-requests, request-watch, quotes, directives, shaping-guarantees (193) |
| execution | supporting | tracking, specification | 21 | 2 | 13 | 46 | batches, reviews, review-guarantees (68) |
| measurement | generic | execution, tracking, specification | 22 | 1 | 6 | 26 | measurement, trials (14) |
| analysis | generic | specification | 36 | 3 | 12 | 58 | toolchain, code-analysis, feature-reading (49) |
| upgrades | generic | specification, tracking | 36 | 1 | 4 | 59 | upgrades (39) |
| *shared layer* | – | – | – | – | – | 79 | – |

Services: specification has `decisions`, `language`, `records`, `scenarios` and `specification`. Tracking has
`backlog` (15 operations), `context requests` (15), `conversation` (6) and `drafting` (18). Execution has `batches`
(11) and `reviews` (2). The model declares no events. Its one actor, `the person`, is declared in tracking.

Things to fix whatever is decided:

- `spec/index.md` lists `parsing` under "Retired in 0.31.0", but `spec/capabilities/parsing.md` is live with
  `area: specification`.
- The index's `## Composition` still uses the old `### <area> (<kind>)` sub-tables. That is not the index form that
  batches#r76 lays for consumers (`| area | kind | capabilities |`).
- Every model file still carries `kind: core|supporting|generic`. Decision 0128 says a context's model carries none.
- `spec/vocabulary/shared.md` has no `area:` in its frontmatter. It is a layer of no part of the model.

### 1.2 Code, by module group

The groups are defined in `support/groups.py`. A module goes in the group of the capabilities whose handlers and
module-map row it serves. Lines are physical lines.

| group | modules | lines | what it is |
|---|---|---|---|
| language | 74 | 10,750 | **Language toolchain**: grammar 4 (`spec_rgl*`, `spec_grammar4`, `spec_gf`), logical form (`spec_lf*`), logic and entailment checks (`spec_solve*`, `spec_entail*`), step grammar and scenario writer (`spec_steps4*`, `features_generate*`, `features_vocab4*`), catalogues (`model_constructs*`, `model_rules`, `model_catalogue*`). Implements specification's parsing, reading, consistency and scenarios. |
| specification | 33 | 4,849 | domain model and vocabulary readers, `spec` checks (`model_*`), decisions, records, contract form, adapter checks |
| tracking | 53 | 7,632 | `backlog_*`, `request_*`, `conversation_*`, `directive*`, `readiness_*`, `intake_moves`, `shop_ids` |
| execution | 27 | 3,592 | `batch_*`, `delivery_settings`, `work_items` (the pytest plugin) |
| measurement | 9 | 896 | `measure_*`, `transcripts` |
| analysis | 9 | 1,092 | `tools_*`, `features`' Gherkin reading (`features_bindings`, `_gherkin`, `_report`) |
| upgrades | 18 | 2,278 | `migrate_*` |
| plumbing | 9 | 998 | **Shared plumbing**: `shop_files` (commit and push), `shop_refused`, `toml_edit`, `store_git`, `domain_envelope`, `adapter_cli*` (the CLI adapter), `model_parse` (frontmatter) |
| cli | 7 | 852 | the entry scripts `work`, `spec`, `features`, `measure`, `migrate`, `tools`, `model` |

`work` spans tracking, conversation and execution. `features` spans analysis and the language.

The scenario tests are one shared world. They include `vocab.py`, `world_*.py`, and `work_queue_world.py`, which
every feature binds through. Their handler modules are still named after the retired 0.37 capabilities:
`batches_handlers*` has 27 modules, `design_model_check*` 20, `requests*` 10, `drafting*` 10. They reach the 0.38
capabilities through `spec/moves.json` (`requested.py`'s `origin`).

## 2. Subdomains and candidate bounded contexts

### 2.1 Subdomains (problem space, declared by the product: decision 0128)

| subdomain | type | the business problem |
|---|---|---|
| S1 Requirements specification | core | Keeping one context's behaviour as a model, a vocabulary, requirement lines and decisions, and generating its acceptance scenarios from them. |
| S2 Controlled requirements language | core | Reading a requirement line to exactly one meaning, refusing what does not read, and finding contradictions and entailments between lines. |
| S3 Work planning | supporting | Ideas becoming shaped, ready items with requirement lines, ranked and readied against a bar. |
| S4 Collaboration between contexts | supporting | One context asking another for behaviour, and the exchange until it is settled. |
| S5 The person's direction | supporting | What the person said, kept and cited, and the short-term directions sessions follow. |
| S6 Delivery | supporting | Ready work built in batches, reviewed once as one change, and merged. |
| S7 Delivery economics | generic | What work cost and what escaped: measurement, defects, trials. |
| S8 Codebase insight | generic | Toolchain, coverage, references, lint, size, the Gherkin of features. |
| S9 Release adoption | generic | A repository moved between plugin releases, and a new context founded. |

### 2.2 Candidate bounded contexts (solution space)

| context | made of today | addresses |
|---|---|---|
| **specification** | the area `specification`, including the language toolchain and `grammar/` | S1, S2 |
| **tracking** | the area `tracking`: backlog, drafting, readiness, context requests, quotes, directives | S3, S4, S5 |
| **execution** | the area `execution` | S6 |
| **measurement** | the area `measurement` | S7, S6 (reads delivery's history) |
| **analysis** | the area `analysis` | S8, S1 (feature reading serves the scenarios) |
| **upgrades** | the area `upgrades` | S9, and every subdomain whose files a step rewrites |

### 2.3 The many-to-many relation

| | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 | S9 |
|---|---|---|---|---|---|---|---|---|---|
| specification | ● | ● | | | | | | | |
| tracking | | | ● | ● | ● | | | | |
| execution | | | | | | ● | | | |
| measurement | | | | | | ○ | ● | | |
| analysis | ○ | | | | | | | ● | |
| upgrades | ○ | ○ | ○ | | | ○ | | | ● |

● the context's own subdomain. ○ it serves that subdomain too.

### 2.4 Where an area is a context, two areas are one, and an area spans subdomains

- **One area, one context:** execution, analysis and upgrades. Each has its own service(s), its own words and a
  small, one-way dependency.
- **One area across several subdomains:**
  - Specification covers S1 and S2.
  - Tracking covers S3, S4 and S5. Its four services are three problems: `backlog` and `drafting` are S3,
    `context requests` is S4, `conversation` is S5.
  - Tracking is the second candidate to split later: context requests into their own context. The coupling inside it
    is low: `request_*` imports `backlog_*` only in `request_accept` and `request_terms`. That is not needed for
    the first split.
- **Two areas, one context?** Measurement is the only real candidate to fold into execution:
  - Its model imports execution.
  - `measure_batch` imports nine `batch_*` modules.
  - Its only batch-facing operation (`measure`) reads the batch's window, findings and timings.
  - Recommendation: keep it a separate context, downstream of execution. Execution publishes "a batch merged", with
    its window, findings and timings, as an event with properties (b547's `followed by`). Then measurement needs no
    batch module.
  - If the person prefers fewer contexts, measurement folds into execution as its second module. It is the cheapest
    merge.
- **Upgrades spans everything** because its steps rewrite every context's files. After a split each context should
  own the upgrade steps for its own files. The upgrades context keeps the ordering, `migrate status` and founding
  (`migrate init`).

### 2.5 `grammar/` and the language toolchain

Three readings, and what each would mean:

| reading | what it means here | verdict |
|---|---|---|
| A generic subdomain's library | GF, the RGL and clingo are the generic library, pinned as third-party tools (`tools_grammar.py`). Grammar 4 is not generic: it is generated from each context's vocabulary and carries this product's reading rules. | Only the third-party tools are a library. |
| A shared kernel | Today the language is shared in effect: tracking's readiness bar imports it 16 times, execution 5, upgrades 18, analysis 0. | Not allowed. |
| A context, or a module of one | The language serves S2 for every consumer, through `spec parse`, `spec explain`, `spec logic`, `features generate` and the packs. | Yes: a module of specification now; its own context later, if the module boundary holds. |

Because **Shared Kernel and Conformist are not allowed**, five things follow:

1. **Tracking, execution and upgrades stop importing `spec_*` modules.** They request what they need from
   specification's published operations:
   - "check an item's lines against the bar"
   - "lay a proposal" and "withdraw a proposal"
   - "generate the scenarios"
   - "write the corpus"

   These become ports in each downstream (§4.7). Tracking's readiness bar is the biggest client: it is the bar, but
   every check behind it is specification's.
2. **The shared layer is dissolved.** Each of its 79 entries moves to the layer of the area whose model declares its
   element. A downstream that needs the idea writes its own word behind a port, as `assignment` in §4.
3. **`the person` is declared by each context that has the person as an actor.** It is in tracking today and named by
   every area. b544, one actor across two vocabularies, already lets two layers name one element. Across contexts
   each context declares its own actor, and the adapter maps them.
4. **The base kinds stop being objects of the specification model.** 91 of the 251 cross-area model references are
   `kind of text` (58) or `kind of file` (33), whose objects specification declares. They belong in a pack.
5. **The packs need a ruling: published language or conformist?** Packs are `request`, `cli`, `spec`, `time`, and
   would include such a base pack. A context imports a pack's words verbatim, which looks like Conformist. They are
   the platform's published language, versioned with the plugin, not another context's model. This report treats
   them as the language's Published Language and treats packs as the one sanctioned "import as is". That needs the
   person's ruling (question Q3).

## 3. Coupling report

`python3 support/coupling.py /home/vscode/shopsystem-bdd > support/coupling.md` runs in about 1.5 s and is
read-only. Full tables are in `support/coupling.md` (769 lines). Section (c) uses the **real logical form**: each live
line is run through `spec_language.parse`, then `spec_lf.form`, then `model_domain.uses`, the same reading v_m1 uses.
All 543 lines parsed and none failed.

### 3.1 (a) Shared words and model imports

The import graph has no cycles. Specification is imported by all five other areas, and tracking by execution,
measurement and upgrades.

- **34 words have entries in more than one layer.** `status` is one attribute word naming 8 elements across 5 areas.
  Others: `open`, `merge`, `reopen` (execution and tracking), `amend`, `monitor`, `failed`, `delivered`, `accepted`,
  and seven release numbers in both specification and upgrades.
- **82 vocabulary entries name an element of another area.** 79 are the shared layer:

| element's area | shared entries | examples |
|---|---|---|
| specification | 29 | bounded context, capability, requirement, scenario, file, version, text |
| tracking | 20 | context request, item, session, readiness bar, chore, observation |
| execution | 12 | batch, task, workspace, kept change, review finding, proposed change |
| upgrades | 7 | index file, release, plugin, pin |
| analysis | 6 | Python file, function, feature file, tag, handler |
| measurement | 5 | dispatch, measurement, trial, `trial-runner` |

The other 3 are tracking entries naming specification elements: `store`, `taking`, `rejecting`.

### 3.2 (b) Model references to another area's objects

There are 251 in all. 91 of them are `kind of text|file`, which a base pack would remove (§2.5, point 4). The rest
are 86 relations, 45 operation parameters and 23 operation objects.

| from → to | count | what drives it |
|---|---|---|
| tracking → specification | 79 | parameters naming `term`, `requirement`, `capability`, `universal condition`; kind of text/file |
| analysis → specification | 39 | kind of file, `test`, `scenario` |
| upgrades → specification | 38 | kind of file/text, `repository` |
| **specification → tracking** | 20 | `requirement id`, `universal condition id`, `given block`, `upstream entry`, `channel`, `requirement grammar` declared in tracking; `record concerns → item`; `decisions.enter(title)` (title is tracking's) |
| execution → specification | 15 | kind of file, `requirement`, `operation` |
| **specification → upgrades** | 13 | `index file`, `Behaviour line`, `qualifier`, and the repository's scaffold parts declared in upgrades |
| execution → tracking | 8 | `batch holds → item`, `kept change cites → item`, `batch brief holds → chore`, `park(item)`, `amend(item)` |
| execution → measurement | 6 | `batch has → measurement / wall time / session time / token / role` |
| specification → execution | 5 | `record concerns → batch`, `scenario succeeds in → workspace` |
| tracking → execution | 2 | `item has → task`, `session has → workspace` |

**The top offenders are misplacements, not real dependencies.** The core points at supporting and generic areas only
because elements it owns were declared elsewhere:

- `requirement id`, `universal condition id`, `given block`, `upstream entry` and `requirement grammar` are
  specification's.
- `index file` and `Behaviour line` are specification's.
- `item exceeds → review limit` is execution's: the estimate is `batch_estimate`.

Moving them is step 1 of any split (§4.10).

### 3.3 (c) Lines that name another area's words, by logical form

Placement rule: a word is **own** when its terms are in the line's own layer or a pack. A word only in `shared` is
placed by the area whose model declares its element (an attribute naming several elements counts as own when one of
them is the line's area). `the person` is counted separately: 319 uses across five areas, all foreign to tracking,
where it is declared.

| line's area | lines naming another area's word | main sources |
|---|---|---|
| tracking (193 lines) | 95 | specification: `requirement` 28, `bounded context` 19, `capability` 17, `term` 11, `universal condition` 10, `the entry form` 8, `operation` 5 |
| execution (68) | 53 | tracking: `item` 43, `meet` 18, `readiness bar` 18, `session` 13, `chore`, `model line`, `dependency`; specification: `requirement` 12, `operation table`, `adapter contract`, `construct catalogue` |
| upgrades (39) | 39 | specification: `repository` 31, `bounded context` 17 |
| analysis (49) | 28 | specification: `repository` 17, `scenario` 12, `test`, `execute`, `number` |
| measurement (14) | 12 | execution: `batch`, `review finding`, `grade`; tracking: `session` |
| specification (180) | 7 | tracking: `requirement id` 3 (a misplacement); execution: `batch` 2 |

Specification is nearly clean once misplacements are fixed. Execution's lines are mostly about tracking's items, so
they are the split's real work. Upgrades and analysis use `repository` and `bounded context`, which are platform
words that every context will need. Those belong in the base pack, not in specification.

### 3.4 (d) Python imports between module groups

There are 331 import statements across groups. The table excludes `cli` and plumbing.

| from → to | imports | examples |
|---|---|---|
| specification → language | 49 | `adapter_annotate → spec_grammar4`, `model_domain → spec_lf` |
| **execution → tracking** | 35 | `batch_amend → backlog_lines, readiness_bar`, `batch_brief → backlog_chore`, `batch_start → backlog_items` |
| tracking → specification | 25 | `backlog_adapter → adapter_tables, domain_model`, `backlog_cli → decision_amend` |
| upgrades → language | 18 | `migrate_upgrade_cnl4* → spec_frames, spec_lexicon, spec_language` |
| tracking → language | 16 | `readiness_bar → features_generate, spec_catalogued`, `backlog_lines → spec_lexicon` |
| language → specification | 13 | `features_generate → spec_context, spec_read` (a cycle with the first row) |
| measurement → execution | 9 | `measure_batch → batch_brief, batch_findings, batch_git, batch_pick, batch_plan, batch_timings` |
| execution → specification | 8 | `batch_start → model_check, model_facts, adapter_annotate` |
| specification → tracking | 8 | `model_domain → backlog_items`, `spec_preview → backlog_items`, `record_write → shop_ids` |
| tracking → execution | 5 | `backlog_view → batch_plan`, `request_gh → batch_gh` |
| tracking → measurement | 5 | `conversation_* → transcripts` |
| execution → language | 5 | `batch_start → features_generate, spec_corpus_write` |
| tracking → upgrades | 3 | `conversation_* → migrate_write` |

Fan-in from other groups: plumbing 117, language 88, specification 50, tracking 48, execution 14.

Some of these edges are plumbing in the wrong place, not domain coupling:

- `batch_gh` (the gh wrapper)
- `transcripts` (the transcript reader)
- `migrate_write`

All three belong in plumbing, which removes 13 cross-group imports without touching a model.

A shared *code* library is not a Shared Kernel. The Shared Kernel ban concerns shared model and words. Plumbing can
stay a library each context depends on, or become the store adapter each context wires in (decision 0124).

## 4. Walk-through: work tracking out of work execution

Tracking is the upstream: backlog, items, drafting and requests. Execution is the downstream: batches and reviews.

### 4.1 What execution uses of tracking today

**In code** (calls counted by grep over `batch_*.py`, `delivery_settings.py` and `work_items.py`):

| execution's need | tracking function used today | count |
|---|---|---|
| name and find an item | `backlog_items.label`, `.find`, `.rel_of`, `.parse`, `.items`, `.is_item` | 80 |
| change an item's status | sets `item.status` and writes the file with `backlog_items.render` (`batch_start.py:115,168,207`, `batch_close.py:94,117`, `batch_tasks.py:271`, `batch_pick.py:67`, `batch_plan.py:192`) | 9 writes |
| the ready items in rank order | `backlog_view.ordered` | 1 |
| re-check the bar | `readiness_bar.check`, `.well_formed`, `.unsettled`, `.decision_reasons` | 5 |
| an item's lines, and laying them into `spec/` | `backlog_lines.read`, `.ids`, `.renumber`, `.capability_file`, `.lay_onto`, `.unlay` | 25 |
| an item's chore | `backlog_chore.said`, `.passes`, `.in_scope` | 5 |
| a question kept on park | `backlog_moves.add_note`, `.text_line` | 5 |
| the request resolved on merge | `request_moves.resolve`, `.path_of`, `.field`, `request_lines.items` | 5 |

**In the spec** (`support/execution-lines.md`, classified by text pattern):

- **10 lines write tracking's state.** batches#r50, r54, r55, r57, r58, r65, r89, r93, r94 and r97 set an item's
  status (`in-batch`, `delivered`, `shaped`, `ready`, `needs-input`), or a context request's status and side.
- **29 more lines read tracking state in a condition:** an item's status, the bar, a dependency, the review limit, a
  chore.
- **26 lines need the specification laid or checked:** requirements in a workspace, corpus, catalogue, operation
  table.
- **26 lines are execution's own.**

**The gap in tracking's contract.** `python3 scripts/spec prepare --contract 1.0.0` was saved as
`support/contract-1.0.0.toml`. It gives `item.status` the lifecycle
`idea → shaped → ready → in-batch → delivered | needs-input | ready` and more. No `backlog.*` operation performs
`ready → in-batch`, `in-batch → delivered`, `in-batch → ready` or `in-batch → needs-input`: execution's operations do.
A contract that cannot move its own object through its own lifecycle cannot be published. This is the first thing
the split must fix.

### 4.2 Tracking gains four operations, in its own terms

These are written on a copy of `spec/` in the scratchpad. The diff is `support/sandbox-overlay/tracking-model.diff`.

```model
service backlog
  operation allocate(item)  outcomes: done | refused: item not ready, bar check unmet
  operation discharge(item)  outcomes: done
  operation restore(item)  outcomes: done
  operation suspend(item, question)  outcomes: done
```

Tracking's lines for them. All four parse (`support/lines-parsed.md`):

| id | line | replaces |
|---|---|---|
| T1 | While an item is `ready` and the item meets the readiness bar, when a session allocates the item, the backlog service shall set the status of the item to `in-batch`. | batches#r94's status half |
| T2 | While an item is `ready` and the item does not meet the readiness bar, if a session allocates the item, then the backlog service shall refuse the request and set the status of the item to `shaped`. | batches#r54, and r89 with a rule's reason |
| T3 | While an item is `in-batch`, when a session discharges the item, the backlog service shall set the status of the item to `delivered`. | batches#r50's item half |
| T4 | While an item is `in-batch`, when a session restores the item, the backlog service shall set the status of the item to `ready`. | batches#r58's item half |

Four more of execution's lines move upstream unchanged in meaning, restated in tracking with new ids:

- batches#r65: a delivered item's context request resolved. Tracking does this itself on `discharge`.
- batches#r55: an item another ready item depends on, refused on `allocate`.
- batches#r64: `universal` made when an item holds a universal condition. This is really specification's lay, §4.7.
- The bar-related halves of r93 and r94.

The review limit stays with execution. `item exceeds → review limit` becomes `assignment exceeds → review limit` in
execution's model.

### 4.3 Execution's driven port, in execution's terms

Execution never says "item". Its word is **assignment**: the piece of work a batch holds as the supply gave it, done
by one task. `assignment` is an object of execution's own model, so its lines can use it without importing the port.
The port area holds the service and its verbs. Files: `support/sandbox-overlay/model-supply.md` and
`vocabulary-supply.md`.

```model
# spec/model/supply.md — area: supply, kind: port, imports: [execution]
object claim kind of request
  relations: for → assignment (one)

service supply
  operation claim(assignment)  outcomes: done → the claim | refused: assignment not claimable
  operation fulfil(assignment)  outcomes: done
  operation relinquish(assignment)  outcomes: done
  operation suspend(assignment)  outcomes: done
```

Vocabulary: **the work supply** (proper noun) → service supply. **claim**, **fulfil**, **relinquish**, **defer**
(verbs, action) → the four operations, each with frame `<actor> <verb>s <assignment>`. **claim** (noun) → object
claim.

Port lines (port capability `supply`, narrator: the batches service):

| id | line | parses | Relied on by |
|---|---|---|---|
| P1 | When the batches service claims an assignment, the work supply shall complete the request. | yes | – (the bound check sees E3 request it) |
| P2 | While a batch holds an assignment, if the batches service claims the assignment, then the work supply shall refuse the request. | yes | `Relied on by: batches#<new r94>`. Execution relies on no assignment being in two batches. That is meaning, not visible in any core line's text, so decision 0126 needs the citation. |
| P3 | When the batches service fulfils an assignment, the work supply shall complete the request. | yes | – |

Decision 0127 requires every outcome the supply *may* give on an operation execution requests to reach a core line
(When for an outcome, If for a refusal), in each status the assignment can be in while the request is outstanding. For
`claim`, that means a `done` line (E3's batch goes on) and the `If` line E4.

### 4.4 Real lines rewritten in execution's terms

Each line was checked with `python3 scripts/spec --root <copy> parse "<line>"`. The copy is this repository's `spec/`
and `grammar/` with the overlay laid; the repository itself is unchanged.

| id | was | rewritten (execution's terms) | parses |
|---|---|---|---|
| E1 | batches#r50 | While an assignment is in a batch, when the person merges the proposed change of the batch, the batches service shall fulfil the assignment and set the status of the batch to `merged`. | yes |
| E2 | batches#r58 | While an assignment is in a batch, when the person abandons the batch, the batches service shall relinquish the assignment. | yes |
| E3 | batches#r94 | When the person opens a batch, the batches service shall claim an assignment. | yes |
| E4 | batches#r54, r89, r93 | If the work supply refuses a claim for an assignment, then the batches service shall keep no task of the assignment. | yes |
| E5 | batches#r57 | While a task of an assignment is `running`, when the person parks the assignment, the batches service shall defer the assignment. | yes (after `park(item)` became `park(assignment)`) |
| E6 | (variant of E1) | When the person merges the proposed change of a batch, the batches service shall fulfil every assignment in the batch. | yes |

Two parses failed first and taught something:

- **"If the work supply refuses an assignment"** was refused: `refuse` takes a request. The port needs a request
  object (`claim kind of request`), as checking#r72's fixture has `reservation`.
- **"parks the assignment"** was refused while `park`'s frame named `item`. Every execution verb whose frame names
  `item` today must be reframed: `park` and `amend`.

**A finding for the tooling.** In the logical form (`support/lines-forms.txt`), E1's response act is
`fulfil(e2, subject: x5, object: x1)`, a plain event, not `request(e2, supply.fulfil, ...)`. A response's act of a
port operation is read as a request (`response-request`, b543) only when it is said with parameters. Without one,
the bound check, v_m7 and the entailment chain (b545) will not see execution's request of the port. Either:

- the four port operations each take a parameter, or
- a response's act of an operation verb with no parameters is read as a request too (a candidate item, §5.8).

### 4.5 Tracking's published contract (excerpt)

Today's `spec prepare --contract` prints the whole repository's contract (3,505 lines, `area = ...` on each object).
After the split it must print one hosted context's. The excerpt execution's adapter would pin, with today's
`backlog.ready` and `backlog.list` and the proposed operations:

```toml
context = "bounded-context/missingmass.io/shopsystem/tracking"   # flat id, §5.3
version = "1.0.0"

[objects."item"]
attributes = ["status: shaped | ready | in-batch | delivered | refused | withdrawn | idea | needs-input", ...]
lifecycles = ["status: ... ready → in-batch; in-batch → delivered; in-batch → needs-input; in-batch → ready ..."]

[operations."backlog.list"]
outcomes = ["returned → every item"]

[operations."backlog.allocate"]                       # proposed
parameters = ["item (object: item)"]
outcomes = ["done", "refused"]
reasons = ["item not ready", "bar check unmet"]
requirements = ["items#<T1>: While an item is `ready` and the item meets the readiness bar, when a session allocates the item, ...",
                "items#<T2>: ... if a session allocates the item, then the backlog service shall refuse the request and set the status of the item to `shaped`."]
properties = ["idempotent by item"]                   # b547's property; P2 relies on it

[operations."backlog.discharge"]                      # proposed; also resolves the item's accepted context request
parameters = ["item (object: item)"]
outcomes = ["done"]
```

### 4.6 The in-process adapter

Per decision 0123 it is a nested context, `adapters/supply-tracking/`, with id `<execution's id>/adapter/tracking`.
It holds its realisation lines and an `adr/`, reads execution's port at execution's commit, and pins tracking's
contract at 1.0.0.

| port (execution's words) | realised by (tracking's contract) | outcome mapping |
|---|---|---|
| claim(assignment) | `backlog.allocate(item)`, the item the assignment was offered as | done → done; refused (item not ready, bar check unmet) → refused: assignment not claimable |
| fulfil(assignment) | `backlog.discharge(item)` | done → done |
| relinquish(assignment) | `backlog.restore(item)` | done → done |
| suspend(assignment) | `backlog.suspend(item, question)` | done → done |
| (the offer) | `backlog.list` filtered to `ready`, in rank order | each item → an assignment, with its label, chore and lines |

In code, execution's `batch_*` modules call one module, `supply.py` in execution's group. Its in-process
implementation calls tracking's backlog functions. Swapping it for a remote adapter changes only that module and the
wiring decision (0125). Mechanisms such as one commit or two, and branch or main checkout, are decided in the
adapter's `adr/` (decision 0124), never in a line.

### 4.7 The second port: execution needs the specification

Twenty-six execution lines need the spec laid or checked. In code that is `backlog_lines.lay_onto`/`unlay`,
`model_check`, `features_generate`, `spec_corpus_write` and the catalogues. That is not tracking's business: applying
the change an item proposes to a spec is specification's. Execution declares a second port, `workbench`, in its own
words:

- lay an assignment's proposal on a workspace
- take it out
- check the laid workspace against the rules
- generate its scenarios

Specification publishes the matching operations. Tracking's readiness bar gets the same treatment: a port to
specification, "check a proposal against the bar's checks". Without this second port the split leaves 13 execution →
specification/language imports and 16 tracking → language imports in place.

### 4.8 What moves

| what | from | to |
|---|---|---|
| model | `item exceeds → review limit`, `review limit` (tracking) | execution, as `assignment exceeds → review limit` |
| model | `batch holds → item`, `kept change cites → item`, `park(item)`, `amend(item)` | `→ assignment` in execution |
| model | `item has → task`, `session has → workspace` (tracking) | execution, as `assignment has → task`, `session has → workspace` |
| model | lifecycle transitions out of `in-batch` | performed by tracking's new operations |
| vocabulary | shared's `batch`, `task`, `workspace`, `kept change`, `review finding`, `proposed change`, `cite` (12) | execution's layer |
| vocabulary | shared's `item`, `readiness bar`, `meet`, `chore`, `session`, `question` (20) | tracking's layer; execution writes `assignment` and its own words |
| requirements | batches#r50, r54, r55, r57, r58, r65, r89, r93, r94, r97 | retired; new ids in batches (E1-E5) and items (T1-T4, r55, r65 restated). Never edited in place. |
| store | `.shop/batches/` | execution's; the plan names assignments by the item id tracking gave |
| store | `.shop/backlog/`, `.shop/requests/`, `.shop/quotes/`, `.shop/directives/` | tracking's; only tracking's code writes them |
| code | `batch_*`, `delivery_settings`, `work_items` | execution's group; no `backlog_*`, `readiness_*` or `request_*` import |
| code | `batch_gh`, `transcripts`, `migrate_write` | plumbing |
| tests | `batches_handlers*`, `review*` scenario modules; the batch world's item fixtures | execution's test world; items made through tracking's operations or a stub of the port (b554) |

### 4.9 What breaks

- **One commit becomes several.** `work batch start` today commits moved items and the batch plan together
  (`batch_plan.commit` with `files`). Through the port, tracking commits each allocation and execution commits the
  plan, so a failure in between leaves items `in-batch` with no batch. This is a saga: on failure, relinquish each
  claimed assignment. Decision 0121 (told apart by execution's own statuses) and b546 (saga checks) apply. Whether
  the in-process adapter may still make one commit is an adapter decision (0124).
- **The shared `.shop/` store.** Both contexts write under one `.shop/`, on one branch, under one lock
  (`batch_git.locked`). In one shop that can stay as it is: the store is an adapter. But who may write which folder
  must become a rule, and the lock becomes the adapter's concern.
- **Git as the store.** Item lines are laid on the batch branch (`batch-<n>`) while items live on `main`.
  `batch_parked.as_laid` and `batch_amend` read item files at the base's commit. Through the port, execution must
  keep the proposal it was given (the assignment's lines) rather than re-read tracking's file at a commit.
- **The `work` CLI spans both.** `work batch ...` and `work ready ...` share one program and one
  `spec/adapters/cli.toml`. Proposal: each context has its own CLI contract, and one program may front several
  contexts' contracts (`[programs]` already maps first words to programs). Consumers keep typing the same commands.
- **The readiness bar runs inside `work batch start` and `work batch amend`** (`readiness_bar.check` with `others`),
  laying several items together. Through the ports, "check these proposals together" has to be one specification
  operation, or the bar's cross-item part (`others`) stays with execution's pick.
- **The scenario world is shared.** `vocab.py`, `world_*.py` and `work_queue_world.py` serve every feature. Each
  context needs its own world, or a shared test library that holds no model.

### 4.10 The steps in order, and what each leaves green

| # | step | green afterwards |
|---|---|---|
| 0 | Baseline: `spec check`, `python3 -m pytest`, `tools check` | as today |
| 1 | Move misplaced elements: `requirement id`, `universal condition id`, `given block`, `upstream entry`, `requirement grammar` → specification; `index file`, `Behaviour line` → specification; `review limit` → execution. Base kinds into a pack. | `spec check` (vocabulary entries name elements, not areas); no line changes |
| 2 | Dissolve `shared.md` into the owning layers; add each import the lines then need | `spec check`; v_m1 now names each cross-area word, which is the coupling made visible |
| 3 | Tracking gains allocate, discharge, restore, suspend, with T1-T4 and restated r55 and r65; `backlog_*` implements them | tracking's scenarios; execution unchanged, still writing items directly |
| 4 | Execution's code calls the tracking functions of step 3 instead of writing item files | all scenarios; one writer per folder |
| 5 | Execution declares `assignment`, the `supply` port and its lines; the old lines retire into E1-E5; `supply.py` with the in-process adapter | execution's scenarios through the adapter; port lines bound (bound check b549) |
| 6 | The `workbench` port to specification; tracking's bar port to specification | all scenarios; no `batch_* → spec_*` or `backlog_* → spec_*` import |
| 7 | An import-linter contract per group (`tools check` already runs import-linter) | `tools check` fails on any new cross-context import |
| 8 | Split `cli.toml` per context; `work` fronts both | `spec check` v_a1-v_a4 per contract |
| 9 | The shop declares its hosted contexts; files move under each context; ids (§5) | `migrate upgrade` dry run on the docs example; suite |
| 10 | (Later, optional) execution in its own repository: the remote adapter replaces the in-process one (0125) | the port's conformance scenarios pass with the remote adapter (b555) |

Steps 1-2 are cheap and worth doing even if no split ever happens.

## 5. What the model and the tooling need (proposals only)

### 5.1 Where subdomains and the context map are declared

In the **product**. A product repository holds `product/subdomains.md` (each subdomain: name, type, purpose) and
`product/context-map.md` (each context: its id, the subdomains it addresses, the shop that hosts it, and each relation
with its pattern).

The allowed patterns are:

- customer–supplier through a port and a pinned published contract
- open host with published language (the plugin's packs)
- separate ways

Shared kernel and conformist are refused by the check.

Until a product repository exists, a shop can carry a `product:` id in its index and a local copy of the map that the
product later takes over (question Q11).

### 5.2 How a shop declares the contexts it hosts

`spec/index.md` becomes the shop index: `kind: shop`, its id, `hosts: [<context ids>]`. Each hosted context gets a
folder, `contexts/<name>/` with its own `spec/` (index, model, vocabulary, capabilities, decisions, adapters). Shop-wide
things stay at the root: `.shop/`, the plugin version, delivery settings, records.

A shop hosting **one** context keeps today's flat `spec/`. That is every consumer today, including
`docs/examples/notes-cli/`, so they need no move (question Q9).

### 5.3 Ids

Recommendation: **hosted contexts get flat, product-level ids**, for example
`bounded-context/missingmass.io/shopsystem/tracking`. The shop has `shop/missingmass.io/shopsystem/shopsystem-bdd`.

A nested id such as `.../shopsystem-bdd/tracking` names the repository. It would change when step 10 moves the
context out, breaking every pinned contract and every request that cites it.

Adapters keep 0123's nesting under their context, because an adapter never moves without its context.

Element ids (`model/<domain>/<path>/<area>`, `vocabulary/...`) become `model/<context path>` and
`vocabulary/<context path>`.

### 5.4 Retiring the word "area"

Every place, from `support/area-occurrences.md` (git grep, whole word):

| where | occurrences | what |
|---|---|---|
| spec frontmatter | 35 | `area:` in 23 capabilities, 6 model files, 6 vocabulary files |
| spec text | 18 lines | checking#r69 ("an area whose kind is `port`"), batches g76 title, decisions 0122/0123/0128, `spec/index.md` §Composition, `object area` (specification.md:341), vocabulary `area`, `kind`, `port` (specification.md:222-224), `the capability form`, `the index form`, `model line`, `domain model` glosses |
| commands | 1 option help, 3 file forms | `work line --model` help; `spec forms`' "item's model lines" (`### <area> model`), "domain model area", "vocabulary term" (`spec/vocabulary/<area>.md`) |
| item blocks | – | `### <area> model` blocks in `.shop/backlog/b<n>.md` (backlog_model, backlog_section) |
| rules | 3 | model.lp v_m1's label and example; `grammar/rules.md`, `catalogue-entries.toml` purpose |
| scripts | 213 lines in 26 files | most in `backlog_model.py` (36), `backlog_model_area.py` (30), `backlog_capability.py` (26), `domain_model.py` (19), `migrate_upgrade_domain.py` (12), `domain_model_parse.py` (12) |
| corpus | 7 lines | `grammar/corpus/constructs/request/spec/` (index table, model and vocabulary `area:`), `grammar/corpus/spec/checking.md` |
| docs | 61 lines | `docs/reference/domain-model.md` (13), `capability-file.md` (10), CHANGELOG (9), notes-cli example (10), `concepts.md` (7), `recipes.md` (6), `commands.md` (5) |
| skills | 5 | `shaping-items` (3), `taking-in-a-request`, `raising-a-request` |
| tests | 124 lines | handlers and fixtures |

The proposed renaming:

- An area of kind core, supporting or generic becomes a **context** (one per model file after the split).
- An area of kind `port` becomes a **port**: `spec/ports/<port>.md` and `spec/vocabulary/<port>.md`, with `port:` in a
  port capability's frontmatter.
- A capability's `area:` is dropped: the capability belongs to the context whose folder holds it.
- If a context keeps several model files before it is split, they are **model files** for now. DDD's "module" is
  deferred, as agreed.
- `kind:` leaves the model files (0128) and moves to the product's subdomains.

### 5.5 The `migrate upgrade` step ("hosted contexts")

For a consumer:

1. Drop `kind:` from each `spec/model/*.md`, and print a proposed subdomain list for the product, keyed by the old
   kinds.
2. A shop with one model file and one layer gets no other change. This is the common case.
3. For a shop with several model files:
   - Write the shop index.
   - Move each core, supporting or generic model file, with its vocabulary layer and capabilities, into
     `contexts/<name>/`.
   - Turn each `kind: port` file into a port of the context it imports.
   - Split `shared.md` by element.
   - Give ids as in §5.3.
   - Rewrite `spec/moves.json` references.
4. Report, without rewording, every line that names another context's word. That is coupling.py's section (c) as
   `spec check` would print it, with the port it suggests.
5. Rewrite item blocks `### <area> model` to `### <context> model`.

The step rewords no requirement line, as the 0.33 and 0.38 steps do.

### 5.6 Existing decisions and items that need rewording

| id | what changes |
|---|---|
| 0122 | "A core area never imports a provider area" becomes "A context's domain never imports a provider's model"; "port area" becomes "port". **"Core" is overloaded**: 0122's core is the hexagonal domain core, while 0128's core is a subdomain type. Proposal: say "domain" (or "the context's core") for the hexagon and keep "core" for the subdomain type. |
| 0123 | "never an area of the parent's model" becomes "never part of the parent context's model"; "reads the parent's port area" becomes "reads the parent's port". Its id rule must say "parent context's id" once contexts are hosted. |
| 0128 | Rationale: "the term area mixed..." stays as history. Its decision should name the shop ("a repository that is many things at once" becomes "a shop hosting several contexts") and say where subdomains are declared (§5.1). It is enforced only once `kind:` leaves the model files. |
| 0126 | "core lines" is fine; "the bound check" should say it works per hosted context. |
| b540 | Mostly fine (it speaks of the port and the core). Its "nested context id" must follow §5.3. |
| b550 | "the adapter spec's provider area and provider capabilities" becomes "provider model and provider capabilities". |
| checking#r69 | "an area whose kind is `port`" retires for a line about "a port". |
| batches g76 / r76 | The capability and index forms name `area:` and `\| area \| kind \| capabilities \|`; both forms change. |
| v_m1 | Label "the vocabulary its capability's area reads" becomes "...its context reads"; across hosted contexts, v_m1 is the coupling check. |

### 5.7 Candidate design-decisions (not written)

1. **A repository is a shop that hosts bounded contexts.** A shop declares the contexts it hosts. Each context has its
   own index, model, vocabulary, capabilities, decisions and adapter contracts, and a shop with one context keeps the
   flat layout.
2. **A hosted context's id names the product, not the shop.** The id survives the context moving to another shop;
   only adapters nest under their context.
3. **The product's context map names each relation's pattern.** Allowed: customer–supplier through a port and a
   pinned contract, open host with published language, and separate ways. Shared kernel and conformist are refused.
4. **The plugin's packs are the published language every context may import.** Importing a pack is not a conformist
   relation, because a pack is the platform's language, not another context's model.
5. **Base kinds come from a pack.** `file`, `text`, `repository`, `bounded context` and the like are declared once in
   a pack, so `kind of file` couples no context to another.
6. **Each context declares its own actors.** `the person` is an actor of every context that serves the person; an
   adapter maps one context's actor to another's.
7. **Only a context's own operations move its objects through their lifecycle.** A transition of a lifecycle that no
   operation of the same context performs is a violation.
8. **A step that crosses contexts is a saga, not one commit.** Each context keeps its own changes; a failure part way
   is compensated by the requester, told apart by its own statuses (0121).
9. **A context's code reaches another context only through its port's adapter.** An import boundary per context is
   checked by `tools check`'s import-linter.
10. **The word "area" is retired.** It becomes "context" for a part with its own subdomain, "port" for a driven port,
    and "model file" for a file of a context's model.
11. **Upgrade steps belong to the context whose files they rewrite.** The upgrades context orders them and founds
    contexts.

### 5.8 Candidate backlog items (not written)

1. **The specification reports cross-context use.** A `spec` report of the four couplings of §3 per pair of contexts,
   with the top words, as v_m1 reads them.
2. **Misplaced elements moved to the area that owns them.** `requirement id`, `universal condition id`, `given
   block`, `upstream entry`, `requirement grammar`, `index file`, `Behaviour line` and `review limit` move, with no
   line changed.
3. **The shared vocabulary layer split by element.** Each shared entry moves to the layer of its element's area, and
   imports are added where lines need them.
4. **Base kinds in a pack.** `text`, `file`, `repository`, `bounded context` and `version` move to a pack every
   context imports.
5. **A lifecycle transition no own operation performs is a violation.** A new rule names each such transition (today
   item's four `in-batch` transitions).
6. **The backlog allocates, discharges, restores and suspends items.** Tracking's operations for the transitions
   batches perform today, with T1-T4 and r55 and r65 restated.
7. **Execution works on assignments through the work supply.** The `supply` port, `assignment`, E1-E5 retiring their
   batches lines, and the in-process adapter `adapters/supply-tracking/`.
8. **Execution lays and checks proposals through the workbench.** The second port, and specification's operations
   lay, withdraw, check and generate for a proposal.
9. **A response's act of an operation with no parameters is a request.** E1's `fulfil` should be read as
   `request(e, supply.fulfil, ...)` so the bound and entailment checks see it.
10. **A published contract per hosted context.** `spec prepare --contract <version> --context <name>` prints one
    context's contract.
11. **Import boundaries per context.** An import-linter contract per module group, with `batch_gh`, `transcripts` and
    `migrate_write` moved to plumbing first.
12. **A shop index that hosts contexts, and the upgrade step "hosted contexts"** (§5.5).
13. **Subdomain kinds leave the model files** (0128), shown by the product's subdomains.
14. **This repository's index in its own index form.** The Composition table form, and `parsing`'s contradictory
    listing fixed.
15. **A scenario world per context.** The shared `vocab.py` and `world_*` split so each context's features bind
    without another context's handlers.

## 6. Risks and open questions

Each question can be answered with a choice.

| # | question | options (recommendation first) |
|---|---|---|
| Q1 | Hosted context ids: flat under the product, or nested under the shop? | flat (survives a move) / nested (shows where it lives) |
| Q2 | Is the language its own context now, or a module of specification? | module now, context later / its own context now (49 + 13 imports to cut) |
| Q3 | Are the plugin's packs a published language every context may import, or a conformist relation? | published language / conformist, so each context copies the words it needs |
| Q4 | Measurement: a context downstream of execution's published "batch merged", or a module of execution? | separate context / module of execution |
| Q5 | Context requests and the person's quotes and directives: stay in the tracking context, or contexts of their own? | stay, split later / split now |
| Q6 | Upgrade steps: owned by each context, or all by the upgrades context? | each context / upgrades owns all |
| Q7 | Batch opening: accept a saga (claims then plan, compensated), or let the in-process adapter keep one commit? | saga, with the commit count left to the adapter's adr / one commit as a rule |
| Q8 | `the person`: declared by each context, or one product-level actor list? | each context / product list |
| Q9 | Does a shop with one context keep the flat `spec/` (no consumer moves)? | yes / always `contexts/<name>/` |
| Q10 | Is `work` one program fronting several contexts' CLI contracts acceptable, or does each context get its own command? | one program / one command per context |
| Q11 | Until a product repository exists, where do subdomains and the context map live? | a `product/` folder in this shop, taken over later / wait for the product repository |
| Q12 | Execution's word for the work it is given: `assignment`, or another? (Grammar collisions found: `job`, `release`, `take` and `schedule` already have meanings.) | assignment / the person's word |
| Q13 | The overloaded "core" in 0122 (hexagon) versus 0128 (subdomain type): which word changes? | hexagon becomes "domain" / subdomain type becomes "core domain" |

Risks:

- **Line churn.** About 40 execution lines (the 39 that write or read tracking's state) and some tracking lines retire and get new ids. Every retired id is
  carried in `spec/moves.json`-style maps, and each item's request lines must follow.
- **The readiness bar crossing ports.** Its "laid over the items picked before" (`others`) is cross-item and may not
  fit one specification operation. If it does not, execution's pick keeps a copy of the bar logic.
- **Grammar size.** More layers and more `<noun>_<context>` kinds grow grammar 4. The guards in
  `tests/scripts/test_grammar4_guards.py` will show it.
- **The shared scenario world.** It is the hardest code to split. Splitting it late means the import boundary (step
  7) cannot cover `tests/`.

## Support files

All are in `support/`, and all were generated read-only against this repository's `main`.

| file | what |
|---|---|
| `coupling.py`, `groups.py` | the coupling report and the module groups; `python3 coupling.py <repo>` |
| `coupling.md` | its output: inventory, sections a-d, every reference, every line with foreign words |
| `execution_lines.py`, `execution-lines.md` | execution's 68 lines classified W/R/S/E by text pattern |
| `contract-1.0.0.toml` | `spec prepare --contract 1.0.0` as printed today (whole repository) |
| `lines.txt`, `lines-parsed.md`, `lines-forms.txt` | the 13 rewritten lines, their parse results, and two logical forms |
| `sandbox-overlay/` | the port model and vocabulary, and the diffs to execution's and tracking's model and vocabulary, laid on a scratch copy of `spec/` for the parses |
| `area-occurrences.md` | every occurrence of "area" by place |
