# Domain-model extraction: tool capabilities

Sources: `spec/index.md` Glossary (lines 88-140); `spec/capabilities/` feature-file-tools, analysis-tools,
batch-measurement, trials, migration-tools (Behaviour lines only, unless marked *impl* = "Implementation, may change").
Extraction only; nothing designed. Citations `<capability>#r<n>`.

---

## 1. Entities

### 1.1 feature-file-tools

| Entity | Identity | Attributes | Value sets / constraints | Ids |
|---|---|---|---|---|
| Features directory (`--dir`) | path; default `features` | the `*.feature` files under it, recursively | files named by `--file`/`--to` must be inside it | feature-file-tools#r1, #r35, #r56, #r58 |
| Feature file | path under `--dir` | feature tags; Background (steps); scenarios; docstrings | must contain no `Rule:` block outside a docstring, before or after an edit | feature-file-tools#r1, #r2, #r4, #r13, #r14 |
| Docstring | position in a feature file | text | text inside is never a scenario, keyword or tag | feature-file-tools#r1, #r2 |
| `Rule:` block | position | — | forbidden outside docstring | feature-file-tools#r2 |
| Scenario | **title** (within a file; must be unique across `--dir` unless `--file`; exactly once in `--file`) | title; own tags; effective tags (own + feature's + Examples'); requirement tag; description lines; Background steps (inherited); own steps; block | deprecated / not deprecated; title may end " (deprecated)" | feature-file-tools#r4, #r5, #r16, #r17, #r19, #r35, #r51 |
| Scenario Outline / Examples table | (part of a scenario) | Examples rows; Examples tags | counted once per Examples row | feature-file-tools#r4, #r5 |
| Scenario block | the scenario's text lines | — | moved/removed as a unit, unchanged | feature-file-tools#r12, #r23 |
| Tag | `@<name>` | — | kinds: requirement tag `@r<n>`, `@deprecated`, feature tag, Examples tag, (old) `@holding` | feature-file-tools#r4, #r19, #r51; migration-tools#r3 |
| Requirement tag | `@r<n>` | n | at most one per scenario (tag replaces any `@r<m>`) | feature-file-tools#r51, #r21 |
| Description line `Deprecated for:` | — | `<new title>` or `removal` | two values | feature-file-tools#r19, #r21 |
| Replacement | title of another scenario | file, `@r<n>` | may not exist; may lack `@r<n>` | feature-file-tools#r19, #r21, #r61 |
| Step | position | text | Background step vs own step | feature-file-tools#r13, #r16 |
| Tree (verify-moved) | directory: `--from <dir>` vs the `--dir` tree | scenarios by title | per scenario: match, changed (with what), duplicate, missing, added | feature-file-tools#r16, #r17 |
| Test directory (`--tests`) | path; default `tests` | test modules | — | feature-file-tools#r25, #r57 |
| Test module | path under `--tests` | binding calls | must parse (*impl*) | feature-file-tools#r25, #r28 |
| Binding (call) | module + line | form `scenario(<feature>, "<title>")` or `scenarios(<path>, ...)`; feature argument; title (plain string; one line) | valid / names no scenario / names wrong feature; title written over several lines = refusal | feature-file-tools#r25, #r29, #r57, #r58 |
| JSON result | — | one JSON object | — | feature-file-tools#r60, #r61, #r62 |

### 1.2 analysis-tools

| Entity | Identity | Attributes | Value sets | Ids |
|---|---|---|---|---|
| Project | current directory | interpreter; virtualenv; import contracts; tracked Python files | Python project or not (*impl*) | analysis-tools#r1, #r16 |
| Interpreter | path | origin; is-virtualenv | origin ∈ {`--python`, `.venv/bin/python`, `venv/bin/python`, `$VIRTUAL_ENV/bin/python`, the running interpreter} (ordered); reported origin ∈ {`--python`, project's virtualenv, neither} | analysis-tools#r1, #r3, #r6 |
| Analysis tool | name | version or missing; what it is for; what the workflow does without it | present / missing; *impl* set: coverage, pytest-cov, jedi, ast-grep, ruff, vulture, import-linter, hypothesis; ruff = one pinned version | analysis-tools#r3, #r4, #r7, #r17, #r58 |
| Dependency file | path | — | never edited | analysis-tools#r5 |
| Coverage map | location `.shop/scratch/tools/coverage` (one) | commit made at; test count; context per test | replaced by each `map`; "the last map" | analysis-tools#r8, #r9, #r13, #r56 |
| Test (in map) | test id | test file | — | analysis-tools#r9, #r10 |
| Target (tests-of) | `<file>[:<function \| Class.method \| line range>]` | — | readable / not (no such function) | analysis-tools#r9, #r11, #r57 |
| Function | path:line name | executed by some test or not | untested | analysis-tools#r13 |
| Name | identifier the project defines | definition location; references | defined / not | analysis-tools#r14 |
| Reference | `path:line` | via import / alias | definition is not a reference; in production file or test file | analysis-tools#r14 |
| Import contracts | project's | — | present / none | analysis-tools#r16 |
| Changed files since `--base` | git diff | — | not deleted | analysis-tools#r16 |
| Tracked Python file | path in working tree | line count | `.py` extension or `python` shebang; tests included | analysis-tools#r50, #r51 |
| Size limit | integer n | — | default 300, `--limit <n>` | analysis-tools#r52 |
| Suite | (glossary) | — | run once under coverage | analysis-tools#r8 |

### 1.3 batch-measurement

| Entity | Identity | Attributes | Value sets | Ids |
|---|---|---|---|---|
| Initiative | name | `log.jsonl`; fulfilled request(s); window; work-items; stages | has `log.jsonl` or not; fulfils 0 or 1 request (≥2 refused) | batch-measurement#r39, #r46, #r64, #r67 |
| `log.jsonl` | per initiative | stage starts/ends; transitions; times | time ending `Z` = UTC | batch-measurement#r40, #r51, #r59 |
| Request (fulfilled) | id | asker | held by queue or not; has asker or not; internal (asker = this bounded context) / external | batch-measurement#r63, #r65, #r66 |
| Measurement | path `.shop/records/measurements/<date>-<initiative>.md` | date = day run; stage rows; work-item rows; totals; internal/external; session rows | exists / not; no prompt, reply or tool content | batch-measurement#r39, #r48, #r49 |
| Stage row | (work-item, stage) from `log.jsonl` | work-item, stage, agent, session id, duration, turns, output tokens, new input tokens, cache-read tokens, cost, round trips | start+end; start-no-end (no duration); empty `session.json` (no figures, flagged); no transcript (no round trips) | batch-measurement#r40, #r51, #r53, #r55, #r57 |
| `session.json` | per stage directory | turns, tokens, cost (*impl*) | empty / known shape / unknown shape (refused) | batch-measurement#r47, #r57 |
| Transcript | file | lines; assistant messages with request ids; tool uses; compactions | known shape / unknown (refused); lines may hold U+2028 inside JSON strings | batch-measurement#r47, #r53, #r58, #r60 |
| Work-item row | work-item | transitions; count to `awaiting-answer`; count to `failed`; commits merged into initiative branch | — | batch-measurement#r41 |
| Totals | per measurement | stages, sessions, turns, round trips, tokens per kind, cost, time first→last transition | — | batch-measurement#r42 |
| Token kind | — | — | {output, new input, cache-read} | batch-measurement#r40, #r42, #r43 |
| Sessions directory (`--sessions <dir>`) | path | transcripts | — | batch-measurement#r43, #r60 |
| Session row (from `--sessions`) | session id | tokens per kind; round trips; tool uses by tool name; dispatched sessions; compactions | active inside window (starting inside, or before with a message inside); or dispatched by one | batch-measurement#r43, #r60 |
| Initiative's window | interval | — | first→last transition (*impl*) | batch-measurement#r43 |
| Comparison | (a, b) | totals side by side; ratio b/a | — | batch-measurement#r45, #r62 |

### 1.4 trials

| Entity | Identity | Attributes | Value sets | Ids |
|---|---|---|---|---|
| `trial-runner` | agent name | — | — | trials#r1 |
| Trial input | — | subject; target; what to measure | subject ∈ {a plugin tool, `work run`}; target ∈ {real target, fixture repository} | trials#r1 |
| Trial | one run | — | exactly one per start | trials#r1 |
| Measurement record | under `.shop/records/measurements/` | what ran; target; what measured | one per trial | trials#r4, #r5 |
| Starting repository | the repository the runner was started in | — | unchanged except the record | trials#r3 |

### 1.5 migration-tools

| Entity | Identity | Attributes | Value sets | Ids |
|---|---|---|---|---|
| Repository | path | layout; uncommitted changes; has `.shop/`; plugin version; tracked text files | layout ∈ {old system, final layout}; `.shop/` present/absent | migration-tools#r6, #r15, #r19, #r28 |
| Context path | `--context <path>` | — | gives `bounded-context/<path>` | migration-tools#r1, #r4, #r12 |
| Old-layout location → final location | — | — | `decisions/`→`spec/decisions/`; `work/`→`.shop/work/`; `records/<x>`→`.shop/records/<x>`; `docs/superpowers/plans/`→`.shop/records/archive/plans/`; `docs/superpowers/specs/`→`.shop/records/archive/design-notes/`; `docs/superpowers/requests/`→`.shop/records/archive/requests/`; `adrs/`→`.shop/records/decision-arguments/` | migration-tools#r1, #r8, #r14 |
| Ledger (decision ledger) `spec/decisions.md` | file | title; entries | removed when only title + entries remain and all replaced | migration-tools#r2, #r11 |
| Ledger entry | heading `## decision/<nnnn>-<slug>` or `## decision/<slug>` | first paragraph; whole text; `date`, `by`, `supersedes` (maybe with qualifier), `revisit_when`; number | numbered / unnumbered (numbered in ledger order above highest) | migration-tools#r2, #r13, #r17 |
| Decision file | `spec/decisions/<nnnn>-<slug>.md` | summary; Decision; status; date; by; supersedes; revisit_when | status ∈ {`superseded`, `accepted`} | migration-tools#r2 |
| Decisions index | `spec/decisions/index.md` | — | written by migrate run | migration-tools#r16 |
| Id | `<kind>/<path>/<name>` | kind; name = stem minus decision number | kind ∈ {`capability`, `design-decision`, `initiative-archive` (plan, request), `decision-argument` (design note, ADR), `measurement` (`*-test-log.md`)}; plus `bounded-context/<path>`, `work-item/<context path>/w<n>` | migration-tools#r4, #r9, #r26 |
| Record (relocated) | id | `about` | default `about: bounded-context/<path>` | migration-tools#r12 |
| Reference | — | — | kind ∈ {repository-relative path, relative Markdown link, frontmatter id} | migration-tools#r5 |
| Behaviour line id | `[r<n>]` | — | numbered from one above the highest ever used by the capability | migration-tools#r10 |
| `@holding` scenario (old) | title | " (held)" title suffix; `Held for:` | → `@deprecated`, " (deprecated)", `Deprecated for:` | migration-tools#r3 |
| Plugin version (repository's) | `.shop/plugin-version` one line | version | holds version / empty / other text; default 0.23.1 when file absent and `.shop/` present | migration-tools#r19, #r30, #r31 |
| Plugin's version | plugin release | — | compared: repository version above / not above | migration-tools#r18, #r23 |
| Upgrade step | version + description | pending (glossary) | ordered oldest first; known: 0.24.0 "work-items named by ids"; "the step of the plugin version after 0.24.0" (awaiting-ruling→awaiting-answer) | migration-tools#r18, #r20, #r25, #r29 |
| Upgrade commit | one commit | names each step | — | migration-tools#r20 |
| Work-item (as renamed) | old name → `w<n>` | file `w<n>.md`; `runs/w<n>/`; frontmatter id; `# ` heading; `blocked_by`, `depends_on`, `for`; `log.jsonl` `work-item` fields | numbered from 1 by initiative number then file name; name ambiguity resolved to the naming item's initiative | migration-tools#r25, #r26 |
| Initiative (open) | — | status | "neither `done` nor `abandoned`" | migration-tools#r24, #r32, #r33, #r34 |
| Ledger (initiative) | `.shop/work/<initiative>/ledger.md` | entries | `compacted` + time | migration-tools#r33 |
| Hook | name | — | {SessionStart, PreCompact} | migration-tools#r22–#r24, #r28, #r31–#r34 |
| Session | (glossary) | starts; is about to be compacted | — | migration-tools#r22, #r33 |
| Hand-off | — | written with `work note` | — | migration-tools#r34 |

---

## 2. Relations

| Relation | From | To | Cardinality | Ids |
|---|---|---|---|---|
| contains | features dir | feature file | 1 : 0..* (recursive) | feature-file-tools#r1 |
| contains | feature file | scenario | 1 : 0..* | feature-file-tools#r1 |
| has-title-in | title | feature file | must be 1 (without `--file`); exactly once in `--file` | feature-file-tools#r35 |
| has-background | feature file | Background steps | 1 : 0..1 | feature-file-tools#r13, #r16 |
| inherits-tags-of | scenario | feature, Examples table | scenario : 1 feature, 0..* Examples | feature-file-tools#r4, #r5 |
| has-requirement-tag | scenario | requirement (`@r<n>`) | 0..1 | feature-file-tools#r51 |
| deprecated-for | deprecated scenario | replacement title or `removal` | 1 : 1 (may be absent → reported) | feature-file-tools#r19, #r21 |
| replacement-resolves-to | replacement title | scenario | 0..1 (0 reported) | feature-file-tools#r21 |
| binds | binding call | scenario | `scenario(...)`: 1:1; `scenarios(path)`: 1 : all in file/dir | feature-file-tools#r25, #r57 |
| bound-by | scenario | binding call | must be exactly 1 | feature-file-tools#r58; Purpose |
| contains | test module | binding call | 1 : 0..* | feature-file-tools#r25, #r28 |
| moved-from/to | scenario | source file, destination file | 1 : 1, destination ≠ source (*impl*), inside `--dir` | feature-file-tools#r12, #r35 |
| matches-across-trees | scenario (tree A) | scenario (tree B) | by title, 1:1 | feature-file-tools#r16, #r17 |
| uses | `tools` | interpreter | 1 : 1 (first in precedence) | analysis-tools#r1 |
| installed-into | analysis tool | interpreter | — | analysis-tools#r5 |
| made-at | coverage map | commit | 1 : 1 | analysis-tools#r9, #r56 |
| executed | test | code target / function | * : * (recorded in the map) | analysis-tools#r9, #r13 |
| refers-to | reference | name | * : 1 | analysis-tools#r14 |
| defined-in | name | file/location | 1 : 1 | analysis-tools#r14 |
| over-limit | tracked Python file | size limit | — | analysis-tools#r50 |
| measures | measurement | initiative | 1 : 1 per date (path) | batch-measurement#r39 |
| fulfils | initiative | request | 0..1 (more refused) | batch-measurement#r63, #r64, #r67 |
| asked-by | request | asker (bounded context) | 1 : 1 required | batch-measurement#r63, #r66 |
| held-by | request | queue | required | batch-measurement#r65 |
| has-stage | work-item | stage (row) | 1 : 0..* | batch-measurement#r40 |
| ran-as | stage | session (via `session.json`) | 1 : 0..1 | batch-measurement#r40, #r57 |
| has-transcript | session | transcript | 0..1 | batch-measurement#r53, #r55 |
| merged-for | commit | work-item | * : 1 | batch-measurement#r41 |
| dispatched | session | session | 1 : 0..* | batch-measurement#r43, #r60 |
| active-in | session | initiative's window | — | batch-measurement#r43 |
| compares | comparison | measurement a, measurement b | 1 : 2 ordered | batch-measurement#r45 |
| runs-on | trial | target | 1 : 1 | trials#r1 |
| records | measurement record | trial | 1 : 1 | trials#r4 |
| relocates | old location | final location | 1 : 1 | migration-tools#r1, #r8, #r14 |
| replaces | decision file | ledger entry | 1 : 1 | migration-tools#r2 |
| supersedes | ledger entry / decision | decision | 0..* | migration-tools#r2, #r17 |
| names | reference | file / id | * : 1 | migration-tools#r5 |
| on-version | repository | plugin version | 1 : 1 | migration-tools#r18, #r19 |
| introduced-by | upgrade step | version | 1 : 1 | migration-tools#r18 (glossary) |
| pending-for | upgrade step | repository | repo.version < step.version ≤ plugin's (glossary) | migration-tools#r18, #r20 |
| has-id | work-item | `w<n>` | 1 : 1, unique per context | migration-tools#r25, #r26 |
| refers-to (by name) | work-item (`blocked_by`, `depends_on`, `for`) | work-item | * : * | migration-tools#r26 |
| has-ledger | initiative | ledger | 1 : 1 | migration-tools#r33 |

---

## 3. Events and actions

Global flags: features `--dir` (#r1), `--file` (#r52, #r56), `--tests` (#r25), `--json` (#r60–#r62); tools `--python` (#r1), `--json` (#r53–#r56).
Actor: for features/tools/measure/migrate the narrator session or person runs the command; the script acts. Refusal = exit with error, say why, change nothing (feature-file-tools#r46, analysis-tools#r49, batch-measurement#r50, migration-tools#r7).

### features
| Command | Object | Before | After | Refuses / errors | Ids |
|---|---|---|---|---|---|
| `count --by-tag` | all scenarios | — | prints count per tag + total (untagged included; outline per row) | — | feature-file-tools#r4 |
| `list --tag <t>` / `--title <x>` [`--json`] | scenarios | — | prints file + title of matches; none → prints nothing, exit 0 (non-JSON) | — | feature-file-tools#r5, #r7, #r60 |
| `tag <title> r<n>` | scenario | title resolves to 1 | `@r<n>` sole requirement tag; all else unchanged | title unresolved (r35); arg not `r<n>` (exit 2, *impl*) | feature-file-tools#r51, #r35 |
| `move <title> --to <file>` [`--inline-background`] [`--keep-feature-tags`] | scenario block | title resolves; dest in `--dir` | block at end of dest unchanged; optional inlined Background steps; optional missing feature tags on own line | unresolved title; dest outside `--dir`; (impl) dest missing or same file; result with `Rule:` | feature-file-tools#r12–#r14, #r35, #r2 |
| `deprecate <title> --for <new>` / `--for-removal` | scenario | not deprecated (*impl*) | `@deprecated`, " (deprecated)" suffix, `Deprecated for:` line; nothing else changed | unresolved; already deprecated (*impl*) | feature-file-tools#r19, #r35 |
| `deprecated` [`--json`] | deprecated scenarios | — | lists each with what for + replacement file/`@r<n>`, flags missing line/replacement/tag | — | feature-file-tools#r21, #r61 |
| `retire <title>` | deprecated scenario | tagged `@deprecated` | block removed, rest unchanged | not deprecated; unresolved | feature-file-tools#r23, #r24, #r35 |
| `verify-moved --from <dir>` | two trees | — | all match → prints count, exit 0 | changed/duplicate/missing/added → names each, exit error | feature-file-tools#r16, #r17 |
| `bindings` [`--unbound [files]`] [`--json`] | binding calls / scenarios | — | all valid → says so, exit 0 | wrong title/feature → print module, line, title, feature, exit error; unbound/multiply bound → print, exit error; unparsable module (*impl*) | feature-file-tools#r25, #r26, #r57, #r58, #r62 |
| `rebind <old> <new>` [`--file`] | binding calls | new title is exactly one scenario's | `<old>`→`<new>` in calls (only those of `--file`'s feature) | new title nobody's or several files'; multi-line title string → change no test module | feature-file-tools#r28, #r29, #r56 |

### tools
| Command | Object | Before | After | Refuses / errors | Ids |
|---|---|---|---|---|---|
| (any) | interpreter | — | chosen by precedence; re-exec under it (*impl*) | interpreter does not start (*impl*) | analysis-tools#r1, #r49 |
| `probe` [`--log`] | tools | — | prints tools with versions / missing + purpose, interpreter path and origin; `--log` one line `Probe: tools -> ...` | exit error when any missing | analysis-tools#r3, #r4 |
| `install` | missing tools | — | each missing installed with pip; ruff at pinned version; no dependency file edited | not a virtualenv → installs nothing, says so, error; still missing → prints tool, purpose, consequence, failing command + error, error | analysis-tools#r5, #r6, #r7, #r58 |
| `map` [`-- args`] [`--json`] | suite | — | suite run once under coverage with per-test context; map replaced; exit 0 regardless of test results | no map made (*impl*, keeps last) | analysis-tools#r8, #r56 |
| `tests-of <target>` [`--by-file`] [`--json`] | code target | a map exists | prints tests (or counts per file), count, map commit; none → says so, exit 0 | no such function → "cannot be read"; no map; file missing; coverage missing | analysis-tools#r9–#r11, #r53, #r57, #r17 |
| `untested <file>...` [`--json`] | functions | a map exists | prints untested functions, count, commit; exit 0 | no map; file missing; coverage missing | analysis-tools#r13, #r54, #r17 |
| `refs <name>` [`--json`] | name | name defined in project | prints refs `path:line` + summary (count, prod files, test files, definition) | undefined name (*impl*); jedi missing | analysis-tools#r14, #r55, #r17 |
| `check [paths] [--base]` | Python files | — | ruff + vulture (+ import-linter when contracts), headings; error when any finds | `--base` git cannot compare (*impl*); tool missing | analysis-tools#r16, #r17 |
| `size [--limit n]` | tracked Python files | — | prints those over limit with line count | exit error when any over | analysis-tools#r50–#r52 |

### measure
| Command | Object | Before | After | Refuses | Ids |
|---|---|---|---|---|---|
| `initiative <i>` [`--replace`] [`--sessions <dir>`] | initiative | `log.jsonl` exists; ≤1 request, held, with asker; measurement absent unless `--replace`; inputs of known shape | measurement written at dated path (stage rows, work-item rows, totals, internal/external, session rows) | no `log.jsonl`; request not held; no asker; >1 request; unknown `session.json`/transcript shape; measurement exists | batch-measurement#r39–#r43, #r46–#r53, #r55, #r57–#r60, #r63–#r67 |
| `show <record>` | measurement | — | tables; round trips beside turns (omitted if absent); session figures | — | batch-measurement#r44, #r54, #r56, #r61 |
| `compare <a> <b>` | 2 measurements | — | totals side by side + ratio b/a; session totals (round trips, tool uses, compactions) with ratio | — | batch-measurement#r45, #r62 |

### trial
| Event | Actor | Object | Before | After | Limits | Ids |
|---|---|---|---|---|---|---|
| start trial | session → `trial-runner` | input (tool/`work run`, target, what to measure) | — | one trial run | — | trials#r1 |
| run | `trial-runner` | target | — | — | reads only target + plugin scripts; changes only the record | trials#r2, #r3 |
| write record | `trial-runner` | measurement record | trial has run | one record naming run/target/measured | — | trials#r4 |
| reply | `trial-runner` | starting session | record written | reply names the record | — | trials#r5 |

### migrate and hooks
| Command / event | Actor | Object | Before | After | Refuses | Ids |
|---|---|---|---|---|---|---|
| `migrate run --context <path>` | person/session | repository on old system | no uncommitted changes | relocations (git), ledger → decision files, `@holding`→`@deprecated` + rebind, index id, references rewritten, ids written, Behaviour lines numbered, ledger removed, `about` added, files `git add`ed, `spec/decisions/index.md` written; `model check` clean; not committed (*impl*) | uncommitted changes; any change it cannot make → names each, changes no file | migration-tools#r1–#r17 |
| `migrate status` | person/hook | repository | — | prints repo version, plugin's version, pending steps (version + description), exit 0 | plugin-version holds no version | migration-tools#r18, #r19, #r30 |
| `migrate upgrade` | person (on yes) | repository on final layout | no uncommitted changes; plugin-version readable | pending steps applied oldest first; version written; one commit naming each step; none pending → says so, exit 0, no change | uncommitted changes; no version | migration-tools#r15, #r20, #r25–#r27, #r29, #r30 |
| step 0.24.0 "work-items named by ids" | migrate | work-items | — | ids `w<n>`, files/runs renamed, frontmatter id, heading, `log.jsonl` + cross-refs rewritten, free text untouched | — | migration-tools#r25, #r26 |
| step after 0.24.0 | migrate | work-item files, `log.jsonl` | — | `awaiting-ruling`→`awaiting-answer`, `## Rulings`→`## Answers` | — | migration-tools#r29 |
| session start | SessionStart hook | session | repo state | offer upgrade (pending) / tell person to update plugin (repo ahead) / say file holds no version / give `work status` per open initiative / nothing (no `.shop/`, or nothing pending + not ahead + no open initiative) | — | migration-tools#r22–#r24, #r28, #r31, #r32 |
| session about to be compacted | PreCompact hook | session, open initiatives' ledgers | open initiative exists | `compacted` + time appended to each ledger; session told to write hand-off with `work note` and end | — | migration-tools#r33, #r34 |

---

## 4. Exclusivity, ownership and limits

- One requirement tag per scenario. feature-file-tools#r51
- Exactly one binding per scenario (Purpose; checked by `--unbound`). feature-file-tools#r58
- A scenario title addressed by an edit must be unique across `--dir` (or exactly once in `--file`). feature-file-tools#r35; titles unique per tree in verify-moved. feature-file-tools#r17
- No `Rule:` block outside docstrings, ever. feature-file-tools#r2
- `features` writes only within `--dir` (and test modules under `--tests` for `rebind`); Purpose; feature-file-tools#r35
- `retire` only on `@deprecated`. feature-file-tools#r23, #r24
- Interpreter: first of a fixed precedence, exactly one. analysis-tools#r1
- `tools` edits no dependency file; installs only into a virtualenv. analysis-tools#r5, #r6
- One version of ruff (the plugin's pin). analysis-tools#r58
- At most one coverage map (replaced). analysis-tools#r8
- Size limit: 300 lines default, `--limit` overrides. analysis-tools#r52
- One measurement per initiative per date; overwriting only with `--replace`. batch-measurement#r39, #r48, #r52
- An initiative fulfils at most one request (measurement refuses otherwise). batch-measurement#r67
- Measurement holds no prompt, reply or tool content. batch-measurement#r49
- trial-runner: one trial per start; read scope = target + plugin's scripts; write scope = one measurement record. trials#r1–#r4
- `migrate` is the only code knowing the old layout (Purpose, not a line).
- Migration is all-or-nothing. migration-tools#r7; upgrade is one commit. migration-tools#r20
- Clean working tree required for `migrate run`/`upgrade`. migration-tools#r15
- `migrate upgrade` only on the person's yes (via the hook's instruction). migration-tools#r22
- Work-item ids `w<n>` unique per context, numbering order fixed. migration-tools#r25
- Repository without plugin-version but with `.shop/` taken as 0.23.1. migration-tools#r19

---

## 5. Repeated qualifiers (candidate universal conditions)

| Qualifier | Lines (approx.) | Count |
|---|---|---|
| Atomic refusal: "refuse / exit with an error … and change nothing / leave every file as it was / change no file / writing nothing" | feature-file-tools#r46, #r2, #r35, #r24, #r29; analysis-tools#r49, #r6; batch-measurement#r46, #r47, #r48, #r65, #r66, #r67; migration-tools#r7, #r15, #r30 | ~16 |
| Frame condition on success: "and change nothing else / leave its other tags and every other line unchanged / leave the rest as it was / edit no dependency file" | feature-file-tools#r12, #r19, #r23, #r28, #r51; analysis-tools#r5; batch-measurement#r49; trials#r3; migration-tools#r26 (free text), #r27 | ~10 |
| "exit with an error" | feature-file-tools#r17, #r25, #r46, #r58; analysis-tools#r3, #r6, #r7, #r16, #r17, #r49, #r51, #r57; batch-measurement#r50; migration-tools#r7, #r30 | ~15 |
| "exit successfully" (incl. "whether or not … / however many") | feature-file-tools#r7, #r16, #r26; analysis-tools#r8, #r11, #r13; migration-tools#r18, #r27 | ~8 |
| Reason in the refusal: "say why / naming the file / naming each / because …" | feature-file-tools#r2, #r17, #r24, #r35, #r46; analysis-tools#r6, #r17, #r49, #r57; batch-measurement#r46, #r47, #r48, #r65–#r67; migration-tools#r7, #r15, #r30 | ~18 |
| "Where `--json` is given, X shall print its result, …, as one JSON object" | feature-file-tools#r60, #r61, #r62; analysis-tools#r53, #r54, #r55, #r56 | 7 |
| "with the commit the map was made at" / "the map's commit" | analysis-tools#r9, #r11, #r13, #r53, #r54, #r56 | 6 |
| "a tool … missing → name it, exit error" | analysis-tools#r3, #r6, #r7, #r17 | 4 |
| Effective tags "(its feature's and its Examples' included)" | feature-file-tools#r4, #r5, #r16, #r17 | 4 |
| Output format `path:line`, `<path>: <title>` (Behaviour only mentions format in r14; rest in *impl*) | analysis-tools#r14; *impl* of feature-file-tools, analysis-tools | 1 + impl |
| "When a session starts in a repository with `.shop/` …, the plugin's SessionStart hook shall tell the session …" | migration-tools#r22, #r23, #r24, #r28, #r31, #r32 | 6 |
| "an initiative that is neither `done` nor `abandoned`" (open initiative) | migration-tools#r24, #r32, #r33, #r34 | 4 |
| "relocate with git" | migration-tools#r1, #r8, #r14, #r26 ("rename with git") | 4 |
| "for each session it gives: round trips, tool uses by tool name, sessions dispatched, compactions" | batch-measurement#r60, #r61, #r62 | 3 |
| "tokens of each kind" / list of the three token kinds | batch-measurement#r40, #r42, #r43 | 3 |
| "--help is its contract" | none in these five files | 0 |
| Exit codes (0/1/2) | only *impl* of feature-file-tools, analysis-tools | 0 Behaviour |

---

## 6. Terms used but not defined; inconsistencies and synonyms

### Not in the glossary (used in Behaviour lines)
- feature-file-tools: feature file, feature tag, tag, requirement tag, effective tags (#r16, #r17, never defined; #r4/#r5 explain inline), Background, Scenario Outline, Examples (row, table), docstring, `Rule:` block, keyword, block (#r12, #r23), title, description (line), step, tree, source / destination, relocated scenario, replacement, binding / binding call (glossary "scenario" says "the one test that binds it" but binding is undefined), test module, deprecated (as a tag/state; glossary has only "deprecated scenario"), retire.
- analysis-tools: tool / analysis tool, interpreter, virtualenv, dependency file, map / coverage map / "last map", context per test, target, test file vs production file, reference, definition, alias, import contracts, heading, tracked Python file, size limit, line count, project.
- batch-measurement: initiative (glossary has initiative branch, not initiative), bounded context, queue, asker/upstream (only inside "request"), internal/external request, `log.jsonl`, `session.json`, transcript, turns (of a session), tokens (output, new input, cache-read), cost, totals, ratio, window, active, found session, shape (of a file), stage row.
- trials: target, real target, fixture repository, plugin tool, measurement record.
- migration-tools: old system, final layout, ledger entry, decision, decision file, decision status (`superseded`, `accepted`; not in the glossary's status list), qualifier, `supersedes`/`by`/`revisit_when`, Behaviour line, id, kind, `about`, context path, repository-relative path, tracked text files, unresolved reference / file problem (from `model check`), plugin's version (vs plugin version), hook, SessionStart, PreCompact, hand-off, `@holding`, open initiative.

### Inconsistent / synonyms / collisions
- **ledger**: glossary = `.shop/work/<initiative>/ledger.md` (used so in migration-tools#r33); migration-tools#r2, #r11, #r13, #r17 use "ledger" for the old `spec/decisions.md`. Homonym.
- **turn**: glossary = side of a request; batch-measurement#r40, #r42, #r54 use "turns" for `session.json` `num_turns`; glossary "round trip" is the `--max-turns` unit. Three meanings near each other.
- **target**: analysis-tools#r11 (code a test executed) vs trials#r1 (repository a trial runs on).
- **measurement / measurement record / record**: trials#r4 "measurement record"; batch-measurement#r44 `measure show <record>`; glossary "measurement" is a record.
- **refuse vs exit with an error**: feature-file-tools#r2, #r24, #r29, #r35 say "refuse" while #r46 says "exit with an error"; only batch-measurement#r50 links refuse→error explicitly; analysis-tools never says "refuse" in Behaviour.
- **change nothing** has ≥7 wordings: change nothing, change no file, leave every file as it was, leave the file as it was, change no test module, writing nothing, writing no measurement, install nothing, edit no dependency file.
- **Subject of the shall**: `features` vs `features verify-moved` / `features bindings` / `features list` (#r17, #r57, #r58, #r60–#r62); `tools` vs `tools size` (#r51, #r52); `measure` vs `measure initiative`; `migrate` vs `migrate run`/`migrate upgrade`; hooks; `trial-runner`.
- **say / print / name / list / tell**: output verbs are interchangeable (feature-file-tools#r21 "list", #r26 "say so", analysis-tools#r11 "print that", migration-tools#r27 "say so").
- **project vs repository**: analysis-tools speaks of the project, migration-tools/trials of the repository.
- **plugin version vs plugin's version vs version vs release**: migration-tools#r18–#r31.
- **test vs binding call**: Purpose of feature-file-tools "exactly one test binding it" vs #r58 "bound by no `scenario(...)` or `scenarios(...)` call".
- **stage**: glossary = a session; batch-measurement treats a stage as a `log.jsonl` start/end pair with or without a session (#r51, #r57).
- **session found / session it gives / stage's session / dispatched session**: batch-measurement#r43, #r60 — no term for "sessions from `--sessions`".
- **open initiative**: spelled out four times as "neither `done` nor `abandoned`" (migration-tools#r24, #r32–#r34); CLAUDE.md says "open initiative".
- **work-item name vs id**: migration-tools#r26 ("old name") — name undefined.
- **upgrade step identity**: migration-tools#r25 names a step by version + quoted description; #r29 by "the plugin version after 0.24.0" (relative, no number).
- **Python file**: defined inline in analysis-tools#r50; "tracked" undefined.
- **suite**: analysis-tools#r8 runs "the suite" but passes extra pytest arguments, which may change what the glossary calls the suite.
- **deprecated scenario**: glossary says kept "until its replacement passes"; feature-file-tools#r23 lets `retire` remove any `@deprecated` scenario regardless of the replacement.
- **EARS form**: bold `**then**` in batch-measurement vs plain `then` elsewhere; compound `Where … when` / `Where … if` (feature-file-tools#r7, #r13, #r14, #r56, #r58; analysis-tools#r10); negative feature "Where `--json` is not given" (feature-file-tools#r7); ubiquitous lines with no trigger (feature-file-tools#r57; batch-measurement#r40, #r41, #r42, #r49, #r51, #r53, #r63); a postcondition phrased "shall have left it so that" (migration-tools#r6); hook lines whose response is an instruction to another actor ("tell the session to offer the person", migration-tools#r22).

---

## 7. Lines packing several rules (id: approx. count)

feature-file-tools
- #r1: 3 (scan `--dir` recursively; default `features`; docstrings excluded)
- #r2: 3 (no `Rule:` in input; none in output; refuse naming file, no change)
- #r4: 5 (count per tag; total incl. untagged; outline per row; feature tags inherited; Examples tags inherited)
- #r5: 3 (by tag; by title substring; effective tags)
- #r7: 2 (prints nothing; exit 0)
- #r14: 4 (only missing tags; own line; position; not joined)
- #r16: 3 (comparison criteria; print count; exit 0)
- #r17: 5 (changed; duplicate; missing; added; exit error)
- #r19: 5 (tag; title suffix; description line ×2 forms; regardless of replacement; nothing else)
- #r21: 5 (list; what-for; replacement file+tag; 3 kinds of warning)
- #r25: 3 (title missing; wrong feature; print 4 fields + exit)
- #r35: 6 (no file; several files; not once in `--file`; `--file` outside; `--to` outside; refuse naming files)
- #r46: 3 (exit error; stderr reason; no change)
- #r58: 4 (default scope; unbound; multiply bound; print + exit)
- #r29: 3 (new title nobody's; several files'; multi-line string)
- #r51: 2 (sets/replaces requirement tag; frame)

analysis-tools
- #r1: 6 (five-step precedence + "used as given")
- #r3: 5 (versions; missing with purpose; interpreter path; origin; exit on missing)
- #r6: 3 (install nothing; say per tool; exit)
- #r7: 6 (tool; purpose; consequence; failed command; error tail; exit)
- #r8: 5 (once; coverage per-test context; passthrough args; replace map; exit 0 regardless)
- #r9: 3 (tests; count; commit)
- #r13: 4 (functions; count; commit; exit 0)
- #r14: 6 (all refs; imports/aliases; definitions excluded; format; summary of 4 parts; defined-where)
- #r16: 6 (ruff+vulture; paths or changed-since-base; not deleted; import-linter conditional; headings; exit on findings)
- #r49: 3; #r17: 2; #r50: 4 (print; Python file definition; tests included; line count)

batch-measurement
- #r39: 2 (one measurement; path with date of run)
- #r40: 2 (row exists when start+end; 10 fields)
- #r41: 4 (transitions; awaiting-answer count; failed count; commits merged)
- #r42: 7 totals
- #r43: 4 (sessions in dir; window rule; dispatched sessions; tokens)
- #r47: 3 (non-empty `session.json`; transcript; refuse naming file)
- #r60: 4; #r61: 4; #r62: 4 (three totals + ratio)
- #r63: 2 (internal/external; definition of internal)

trials
- #r1: 2 (input shape; one trial); others single.

migration-tools
- #r1: 3 relocations
- #r2: 7 (replace; summary; Decision; status rule; date; by; supersedes/revisit_when)
- #r3: 5 (tag; title; description; rebind; no `@holding` left)
- #r5: 3 reference kinds
- #r8: 3 relocations
- #r9: 8 (id format; name = stem; number stripped; 5 kind mappings)
- #r11: 2 (condition; removal)
- #r16: 2 (git add; write index)
- #r18: 4 (repo version; plugin's version; pending steps with version+description; exit 0)
- #r20: 3 (apply oldest first; write version; one commit naming steps)
- #r22: 4 (offer; name both versions; name steps; run only on yes)
- #r24: 1 with a 3-part conjunctive condition
- #r25: 3 (id form; order by initiative number; then file name)
- #r26: 9 (rename file; rename runs dir; frontmatter id; keep/write heading; `log.jsonl`; `blocked_by`/`depends_on`/`for`; ambiguity rule; free text untouched; "with git")
- #r27: 3 (say so; exit 0; no change)
- #r29: 3 (status in files; in `log.jsonl`; heading rename)
- #r30: 4 (exit; message; empty variant; other-text variant; + no change)
- #r31: 3; #r34: 2 (write hand-off; end instead of compacting)
