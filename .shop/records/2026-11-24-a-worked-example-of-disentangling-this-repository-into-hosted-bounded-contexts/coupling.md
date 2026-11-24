## 0. Inventory

| area | kind | imports | objects | services | operations | events | actors | vocab entries | capabilities | live lines | capability names |
|---|---|---|---|---|---|---|---|---|---|---|---|
| analysis | generic | specification | 36 | 3 | 12 | 0 | 0 | 58 | 3 | 49 | code-analysis, feature-reading, toolchain |
| execution | supporting | tracking, specification | 21 | 2 | 13 | 0 | 0 | 46 | 3 | 68 | batches, review-guarantees, reviews |
| measurement | generic | execution, tracking, specification | 22 | 1 | 6 | 0 | 0 | 26 | 2 | 14 | measurement, trials |
| specification | core | - | 112 | 5 | 22 | 0 | 0 | 216 | 7 | 180 | checking, consistency, decisions, parsing, reading, records, scenarios |
| tracking | supporting | specification | 48 | 4 | 54 | 0 | 1 | 163 | 7 | 193 | context-requests, directives, drafting, items, quotes, request-watch, shaping-guarantees |
| upgrades | generic | specification, tracking | 36 | 1 | 4 | 0 | 0 | 59 | 1 | 39 | upgrades |
| shared (layer) | - | - |  |  |  |  |  | 79 |  |  |  |

Services and operations per area:

| area | service | operations |
|---|---|---|
| analysis | code analysis | map, trace, screen, locate, lint, size |
| analysis | feature reading | search, count, scan, vet |
| analysis | toolchain | probe, install |
| execution | batches | open, resume, finish, park, submit, merge, abandon, monitor, amend, configure, reopen |
| execution | reviews | review, conclude |
| measurement | measurement | measure, report, view, compare, conduct, hand |
| specification | decisions | enter, rebuild, amend |
| specification | language | parse, explain, look up, preview |
| specification | records | file, file design, file plan, file observation |
| specification | scenarios | generate, audit |
| specification | specification | check, examine, consult, renew, inventory, translate, annotate, describe, prepare |
| tracking | backlog | note idea, shape, rate, link, ready, decline, withdraw, answer, show, list, reopen, annotate, merge, retitle, split |
| tracking | context requests | raise, ask, reply, offer, serve, propose, settle, pass turn, accept, resolve, catch up, watch, survey, inspect, suggest |
| tracking | conversation | quote, prompt, give, promote, drop, read |
| tracking | drafting | draft, recodify, reword, remove, assign, write, declare, apply, expose, withhold, retract, remove model line, reword model line, remove term, reword term, write into pack, take out, replace |
| upgrades | upgrades | query, upgrade, relocate, found |

## a. Shared words and imports

Model imports (area -> areas it imports):

| area | imports | imported by |
|---|---|---|
| analysis | specification | - |
| execution | tracking, specification | measurement |
| measurement | execution, tracking, specification | - |
| specification | - | analysis, execution, measurement, tracking, upgrades |
| tracking | specification | execution, measurement, upgrades |
| upgrades | specification, tracking | - |

Words with entries in more than one layer: 34

| word | layers |
|---|---|
| 0.24.0 | specification, upgrades |
| 0.25.0 | specification, upgrades |
| 0.30.0 | specification, upgrades |
| 0.31.0 | specification, upgrades |
| 0.32.0 | specification, upgrades |
| 0.33.0 | specification, upgrades |
| 0.34.0 | specification, upgrades |
| abandoned | execution, upgrades |
| accepted | specification, tracking, upgrades |
| amend | execution, specification |
| annotate | specification, tracking |
| asker | tracking, upgrades |
| awaiting-asker | tracking, upgrades |
| awaiting-upstream | tracking, upgrades |
| concern | specification, tracking |
| count | analysis, specification |
| delivered | tracking, upgrades |
| done | execution, upgrades |
| drop | execution, tracking |
| exceed | analysis, tracking |
| failed | execution, specification |
| file | shared, specification |
| hand | measurement, specification |
| heading | analysis, specification |
| merge | execution, tracking |
| monitor | execution, specification |
| open | execution, tracking, upgrades |
| proposed | specification, upgrades |
| refused | tracking, upgrades |
| release | shared, specification |
| reopen | execution, tracking |
| reply | measurement, tracking |
| size | analysis, tracking |
| withdrawn | tracking, upgrades |

Vocabulary entries whose element is declared in another area's model (layer -> element's area): 82

| layer | element's area | entries | words |
|---|---|---|---|
| shared | specification | 29 | bounded context, capability, requirement, requirement group, universal condition, term, design-decision, feature, scenario, file, version, text ... |
| shared | tracking | 20 | context request, request line, question, session, item, workspace name, readiness bar, requirement id, chore, observation, thread, entry ... |
| shared | execution | 12 | review finding, workspace, kept change, batch, task, proposed change, `pr-reviewer`, status, status, observation, shared workspace, cite |
| shared | upgrades | 7 | index file, status, release, status, pin, plugin, release |
| shared | analysis | 6 | Python file, function, identifier, feature file, tag, handler |
| shared | measurement | 5 | dispatch, measurement, trial, target, `trial-runner` |
| tracking | specification | 3 | store, taking, rejecting |

## b. Model references to another area's objects

Total: 251

| from area | to area | count |
|---|---|---|
| tracking | specification | 79 |
| analysis | specification | 39 |
| upgrades | specification | 38 |
| specification | tracking | 20 |
| execution | specification | 15 |
| specification | upgrades | 13 |
| measurement | specification | 9 |
| execution | tracking | 8 |
| specification | analysis | 7 |
| execution | measurement | 6 |
| specification | execution | 5 |
| measurement | tracking | 4 |
| analysis | execution | 2 |
| measurement | execution | 2 |
| tracking | execution | 2 |
| tracking | measurement | 1 |
| upgrades | tracking | 1 |

Most referenced foreign objects (relations, attributes):

| object | its area | references |
|---|---|---|
| requirement | specification | 6 |
| requirement id | tracking | 5 |
| file | specification | 4 |
| item | tracking | 4 |
| operation | specification | 4 |
| version | specification | 3 |
| kept change | execution | 3 |
| scenario | specification | 3 |
| batch | execution | 3 |
| workspace | execution | 3 |
| term | specification | 3 |
| test | specification | 2 |
| bounded context | specification | 2 |
| repository | specification | 1 |
| workspace name | tracking | 1 |

All references:

| from | to | what | reference |
|---|---|---|---|
| analysis | execution | relation | base branch holds -> kept change |
| analysis | execution | relation | coverage map has -> kept change |
| analysis | specification | kind of | Python file kind of file |
| analysis | specification | kind of | Python interpreter kind of file |
| analysis | specification | kind of | binding kind of text |
| analysis | specification | kind of | coverage map kind of file |
| analysis | specification | kind of | dependency file kind of file |
| analysis | specification | kind of | docstring kind of text |
| analysis | specification | kind of | examples row kind of text |
| analysis | specification | kind of | feature file kind of file |
| analysis | specification | kind of | finding kind of text |
| analysis | specification | kind of | heading kind of text |
| analysis | specification | kind of | log line kind of text |
| analysis | specification | kind of | pip command kind of text |
| analysis | specification | kind of | replacement kind of scenario |
| analysis | specification | kind of | requirement tag kind of text |
| analysis | specification | kind of | rule block kind of text |
| analysis | specification | kind of | scenario line kind of text |
| analysis | specification | kind of | scenario outline kind of text |
| analysis | specification | kind of | scenario title kind of text |
| analysis | specification | kind of | search text kind of text |
| analysis | specification | kind of | subdirectory kind of file |
| analysis | specification | kind of | tag kind of text |
| analysis | specification | kind of | test module kind of file |
| analysis | specification | operation object | code analysis.lint on file |
| analysis | specification | operation object | code analysis.size on repository |
| analysis | specification | operation object | feature reading.scan on repository |
| analysis | specification | operation object | feature reading.search on repository |
| analysis | specification | operation object | feature reading.vet on repository |
| analysis | specification | parameter | code analysis.lint(file) |
| analysis | specification | parameter | code analysis.lint(repository) |
| analysis | specification | parameter | code analysis.map(repository) |
| analysis | specification | parameter | code analysis.size(repository) |
| analysis | specification | parameter | feature reading.scan(repository) |
| analysis | specification | parameter | feature reading.search(repository) |
| analysis | specification | parameter | feature reading.vet(repository) |
| analysis | specification | relation | Python file holds -> test |
| analysis | specification | relation | analysis tool has -> version |
| analysis | specification | relation | binding binds -> scenario |
| analysis | specification | relation | coverage map holds -> test |
| analysis | specification | relation | feature file has -> scenario |
| execution | measurement | kind of | pr-reviewer kind of dispatch |
| execution | measurement | relation | batch has -> measurement |
| execution | measurement | relation | batch has -> role |
| execution | measurement | relation | batch has -> session time |
| execution | measurement | relation | batch has -> token |
| execution | measurement | relation | batch has -> wall time |
| execution | specification | kind of | batch brief kind of file |
| execution | specification | kind of | batch kind of file |
| execution | specification | kind of | batch plan kind of file |
| execution | specification | kind of | batch rule kind of text |
| execution | specification | kind of | review finding kind of text |
| execution | specification | kind of | review folder kind of file |
| execution | specification | kind of | review kind of text |
| execution | specification | kind of | setting kind of text |
| execution | specification | kind of | setting value kind of text |
| execution | specification | kind of | settings file kind of file |
| execution | specification | kind of | virtual environment kind of file |
| execution | specification | relation | kept change touches -> file |
| execution | specification | relation | workspace holds -> file |
| execution | specification | relation | workspace holds -> repository |
| execution | specification | relation | workspace holds -> requirement |
| execution | tracking | operation object | batches.amend on item |
| execution | tracking | operation object | batches.park on item |
| execution | tracking | parameter | batches.amend(item) |
| execution | tracking | parameter | batches.park(item) |
| execution | tracking | relation | batch brief holds -> chore |
| execution | tracking | relation | batch holds -> item |
| execution | tracking | relation | kept change cites -> item |
| execution | tracking | relation | workspace has -> workspace name |
| measurement | execution | parameter | measurement.measure(batch) |
| measurement | execution | relation | defect for -> batch |
| measurement | specification | kind of | defect kind of file |
| measurement | specification | kind of | measurement kind of record |
| measurement | specification | kind of | ratio kind of text |
| measurement | specification | kind of | reply kind of text |
| measurement | specification | kind of | role kind of text |
| measurement | specification | kind of | session row kind of text |
| measurement | specification | kind of | stage row kind of text |
| measurement | specification | kind of | total row kind of text |
| measurement | specification | relation | target holds -> file |
| measurement | tracking | kind of | dispatch kind of session |
| measurement | tracking | kind of | trial-runner kind of session |
| measurement | tracking | parameter | measurement.hand(session) |
| measurement | tracking | parameter | measurement.report(item) |
| specification | analysis | relation | file holds -> finding |
| specification | analysis | relation | scenario has -> replacement |
| specification | analysis | relation | scenario has -> requirement tag |
| specification | analysis | relation | scenario has -> scenario title |
| specification | analysis | relation | scenario has -> tag |
| specification | analysis | relation | step has -> handler |
| specification | analysis | relation | test executes -> function |
| specification | execution | relation | record concerns -> batch |
| specification | execution | relation | repository rejects -> kept change |
| specification | execution | relation | scenario breaks in -> workspace |
| specification | execution | relation | scenario succeeds in -> workspace |
| specification | execution | relation | text denotes -> batch |
| specification | tracking | operation object | records.file observation on observation |
| specification | tracking | parameter | decisions.enter(title) |
| specification | tracking | parameter | language.preview(item) |
| specification | tracking | parameter | records.file design(title) |
| specification | tracking | parameter | records.file observation(observation) |
| specification | tracking | parameter | records.file plan(title) |
| specification | tracking | parameter | records.file(title) |
| specification | tracking | parameter | specification.describe(item) |
| specification | tracking | relation | bounded context has -> channel |
| specification | tracking | relation | bounded context has -> requirement grammar |
| specification | tracking | relation | bounded context holds -> upstream entry |
| specification | tracking | relation | capability holds -> given block |
| specification | tracking | relation | capability holds -> requirement id |
| specification | tracking | relation | record concerns -> item |
| specification | tracking | relation | requirement has -> requirement id |
| specification | tracking | relation | requirement retires -> requirement id |
| specification | tracking | relation | requirement supports -> requirement id |
| specification | tracking | relation | scenario refers to -> requirement id |
| specification | tracking | relation | text denotes -> item |
| specification | tracking | relation | universal condition has -> universal condition id |
| specification | upgrades | relation | bounded context has -> index file |
| specification | upgrades | relation | capability has -> Behaviour line |
| specification | upgrades | relation | design-decision holds -> qualifier |
| specification | upgrades | relation | repository has -> context scaffold |
| specification | upgrades | relation | repository has -> decision ledger |
| specification | upgrades | relation | repository has -> frozen notice |
| specification | upgrades | relation | repository has -> ignore file |
| specification | upgrades | relation | repository has -> initiative |
| specification | upgrades | relation | repository has -> plugin version file |
| specification | upgrades | relation | repository has -> scenario conftest |
| specification | upgrades | relation | repository has -> shop directory |
| specification | upgrades | relation | repository holds -> old-layout directory |
| specification | upgrades | relation | repository holds -> uncommitted change |
| tracking | execution | relation | item has -> task |
| tracking | execution | relation | session has -> workspace |
| tracking | measurement | relation | item has -> defect |
| tracking | specification | kind of | answer kind of text |
| tracking | specification | kind of | chore kind of text |
| tracking | specification | kind of | context request kind of text |
| tracking | specification | kind of | dependency kind of text |
| tracking | specification | kind of | directive kind of file |
| tracking | specification | kind of | domain model kind of file |
| tracking | specification | kind of | entry kind of text |
| tracking | specification | kind of | field kind of text |
| tracking | specification | kind of | given block kind of text |
| tracking | specification | kind of | item kind of file |
| tracking | specification | kind of | line reason kind of text |
| tracking | specification | kind of | model line kind of text |
| tracking | specification | kind of | question kind of text |
| tracking | specification | kind of | quote kind of file |
| tracking | specification | kind of | relation row kind of text |
| tracking | specification | kind of | request line kind of text |
| tracking | specification | kind of | requirement id kind of text |
| tracking | specification | kind of | resolution kind of text |
| tracking | specification | kind of | retirement list kind of file |
| tracking | specification | kind of | shaping note kind of text |
| tracking | specification | kind of | title kind of text |
| tracking | specification | kind of | transcript kind of file |
| tracking | specification | kind of | universal condition id kind of text |
| tracking | specification | kind of | universal kind of capability |
| tracking | specification | kind of | upstream entry kind of text |
| tracking | specification | kind of | workspace name kind of text |
| tracking | specification | operation object | context requests.watch on bounded context |
| tracking | specification | operation object | drafting.expose on operation table |
| tracking | specification | operation object | drafting.recodify on capability |
| tracking | specification | operation object | drafting.remove on requirement |
| tracking | specification | operation object | drafting.remove term on term |
| tracking | specification | operation object | drafting.retract on capability |
| tracking | specification | operation object | drafting.reword on requirement |
| tracking | specification | operation object | drafting.reword term on term |
| tracking | specification | operation object | drafting.withhold on operation |
| tracking | specification | operation object | drafting.write into pack on term |
| tracking | specification | operation object | drafting.write on term |
| tracking | specification | parameter | backlog.split(requirement) |
| tracking | specification | parameter | context requests.offer(capability) |
| tracking | specification | parameter | context requests.raise(bounded context) |
| tracking | specification | parameter | context requests.raise(text) |
| tracking | specification | parameter | context requests.survey(bounded context) |
| tracking | specification | parameter | context requests.watch(bounded context) |
| tracking | specification | parameter | drafting.draft(capability) |
| tracking | specification | parameter | drafting.draft(requirement) |
| tracking | specification | parameter | drafting.draft(universal condition) |
| tracking | specification | parameter | drafting.expose(operation table) |
| tracking | specification | parameter | drafting.recodify(capability) |
| tracking | specification | parameter | drafting.remove term(term) |
| tracking | specification | parameter | drafting.remove(requirement) |
| tracking | specification | parameter | drafting.replace(universal condition) |
| tracking | specification | parameter | drafting.retract(capability) |
| tracking | specification | parameter | drafting.reword term(term) |
| tracking | specification | parameter | drafting.reword(requirement) |
| tracking | specification | parameter | drafting.take out(universal condition) |
| tracking | specification | parameter | drafting.withhold(operation) |
| tracking | specification | parameter | drafting.write into pack(pack) |
| tracking | specification | parameter | drafting.write into pack(term) |
| tracking | specification | parameter | drafting.write(term) |
| tracking | specification | relation | chore holds -> file |
| tracking | specification | relation | context request addresses -> bounded context |
| tracking | specification | relation | context request originates from -> bounded context |
| tracking | specification | relation | domain model holds -> operation |
| tracking | specification | relation | entry holds -> requirement |
| tracking | specification | relation | entry holds -> term |
| tracking | specification | relation | item has -> requirement |
| tracking | specification | relation | item has -> scenario |
| tracking | specification | relation | item holds -> capability |
| tracking | specification | relation | item holds -> operation |
| tracking | specification | relation | item holds -> operation table |
| tracking | specification | relation | item holds -> requirement |
| tracking | specification | relation | item holds -> requirement group |
| tracking | specification | relation | item holds -> term |
| tracking | specification | relation | item holds -> universal condition |
| tracking | specification | relation | item proposes -> requirement |
| tracking | specification | relation | model line restates -> operation |
| tracking | specification | relation | model line specifies -> operation |
| tracking | specification | relation | retirement list holds -> requirement |
| tracking | specification | relation | term proposal concerns -> term |
| upgrades | specification | kind of | Behaviour line kind of text |
| upgrades | specification | kind of | content kind of text |
| upgrades | specification | kind of | context id kind of text |
| upgrades | specification | kind of | context purpose kind of text |
| upgrades | specification | kind of | context scaffold kind of file |
| upgrades | specification | kind of | decision ledger kind of file |
| upgrades | specification | kind of | frozen notice kind of file |
| upgrades | specification | kind of | frozen request kind of file |
| upgrades | specification | kind of | holds no version kind of text |
| upgrades | specification | kind of | index file kind of file |
| upgrades | specification | kind of | initiative log kind of file |
| upgrades | specification | kind of | ledger entry kind of text |
| upgrades | specification | kind of | ledger number kind of text |
| upgrades | specification | kind of | line id kind of text |
| upgrades | specification | kind of | no upgrade step is pending kind of text |
| upgrades | specification | kind of | old-layout directory kind of file |
| upgrades | specification | kind of | only on the person's yes kind of text |
| upgrades | specification | kind of | plugin version file kind of file |
| upgrades | specification | kind of | qualifier kind of text |
| upgrades | specification | kind of | restated file kind of file |
| upgrades | specification | kind of | shop directory kind of file |
| upgrades | specification | kind of | stage directory kind of file |
| upgrades | specification | kind of | stem kind of text |
| upgrades | specification | kind of | tracked file kind of file |
| upgrades | specification | kind of | uncommitted change kind of text |
| upgrades | specification | kind of | update the plugin kind of text |
| upgrades | specification | kind of | work-item file kind of file |
| upgrades | specification | operation object | upgrades.found on bounded context |
| upgrades | specification | operation object | upgrades.query on repository |
| upgrades | specification | operation object | upgrades.relocate on bounded context |
| upgrades | specification | operation object | upgrades.upgrade on repository |
| upgrades | specification | parameter | upgrades.found(bounded context) |
| upgrades | specification | parameter | upgrades.query(repository) |
| upgrades | specification | parameter | upgrades.relocate(bounded context) |
| upgrades | specification | parameter | upgrades.upgrade(repository) |
| upgrades | specification | relation | ledger entry has -> design-decision |
| upgrades | specification | relation | plugin pins -> version |
| upgrades | specification | relation | plugin version file holds -> version |
| upgrades | tracking | relation | initiative fulfils -> context request |

## c. Capability lines naming another area's words (logical form)

Lines read: 543, unparsed: 0 (-)

A use is counted once a word a line names; a word whose terms are in the line's own layer or a pack is own; one only in `shared` is placed by the area whose model declares its element (`shared>area`; a use of a shared word whose element is the line's own area is own); any other is the area(s) whose layers hold it.

Uses of shared words of the line's own area, counted as own: {'execution': 184, 'specification': 365, 'analysis': 35, 'tracking': 545, 'measurement': 24, 'upgrades': 24}

Uses of the actor `the person` (declared in tracking's model, named by every area), left out below: {'execution': 47, 'specification': 180, 'analysis': 49, 'measurement': 9, 'upgrades': 34}

| line's area | word's area | uses | top words |
|---|---|---|---|
| tracking | shared>specification | 97 | requirement (28), bounded context (19), capability (17), term (11), universal condition (10), repository (5), rule (3), text (1) |
| upgrades | shared>specification | 72 | repository (31), bounded context (17), text (5), file (4), design-decision (3), capability (3), version (2), rule (2) |
| execution | shared>tracking | 60 | meet (18), readiness bar (18), session (13), chore (3), requirement id (3), question (2), entry (1), request line (1) |
| execution | shared>specification/tracking | 43 | item (43) |
| execution | shared>specification | 43 | requirement (12), scenario (6), break (4), succeed (3), capability (3), file (3), corpus (2), rule (2) |
| analysis | shared>specification | 41 | repository (17), scenario (12), test (5), file (5), break (1), version (1) |
| tracking | specification | 31 | the entry form (8), operation (5), operation table (4), translation (4), mention (2), pack (2), identify (1), retire (1) |
| execution | specification | 22 | operation (4), use (3), adapter contract (3), operation table (3), construct catalogue (2), catalogue entry (1), severity (1), pack (1) |
| execution | tracking | 17 | domain model (3), model line (3), dependency (2), restate (2), the review limit (2), ask (1), `universal` (1), resolution (1) |
| analysis | specification | 12 | execute (5), number (4), contain (3) |
| tracking | shared>execution | 11 | cite (5), batch (2), workspace (2), task (1), shared workspace (1) |
| upgrades | specification | 9 | mention (2), decisions index (2), supersede (2), release (2), language (1) |
| execution | shared>measurement | 8 | dispatch (8) |
| measurement | shared>execution | 6 | batch (4), proposed change (1), review finding (1) |
| measurement | shared>tracking | 5 | session (5) |
| upgrades | shared>tracking | 5 | session (5) |
| measurement | specification | 4 | number (4) |
| specification | shared>tracking | 3 | requirement id (3) |
| execution | analysis/tracking | 2 | exceed (2) |
| measurement | execution | 2 | grade (1), review (1) |
| measurement | shared>execution/specification/tracking/upgrades | 2 | status (2) |
| specification | shared>execution | 2 | batch (2) |
| analysis | shared>upgrades | 2 | pin (1), plugin (1) |
| execution | shared>upgrades | 1 | index file (1) |
| measurement | shared>specification/tracking | 1 | item (1) |
| specification | shared>execution/tracking | 1 | observation (1) |
| specification | shared>analysis | 1 | handler (1) |
| measurement | shared>specification | 1 | file (1) |
| upgrades | shared>analysis | 1 | tag (1) |

| area | lines naming a word of another area (the person aside) |
|---|---|
| analysis | 28 |
| execution | 53 |
| measurement | 12 |
| specification | 7 |
| tracking | 95 |
| upgrades | 39 |

Lines naming another area's word:

| line | area | foreign words (area:word) |
|---|---|---|
| batches#r50 | execution | shared>specification/tracking:item |
| batches#r54 | execution | shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar |
| batches#r55 | execution | shared>specification/tracking:item; tracking:dependency |
| batches#r56 | execution | shared>tracking:question; shared>tracking:session; tracking:ask |
| batches#r57 | execution | shared>specification/tracking:item; shared>tracking:question; shared>tracking:session |
| batches#r58 | execution | shared>specification/tracking:item |
| batches#r60 | execution | shared>specification:requirement; shared>specification/tracking:item; shared>tracking:session |
| batches#r61 | execution | shared>specification:break; shared>specification:scenario; shared>specification/tracking:item; shared>tracking:session |
| batches#r62 | execution | shared>specification:scenario; shared>specification:succeed; shared>specification/tracking:item; shared>tracking:session |
| batches#r63 | execution | shared>specification/tracking:item |
| batches#r64 | execution | shared>specification:capability; shared>specification:universal condition; shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar; tracking:`universal` |
| batches#r65 | execution | shared>specification/tracking:item; shared>tracking:context request; shared>tracking:entry; shared>tracking:request line; tracking:resolution |
| batches#r66 | execution | shared>specification:break; shared>specification/tracking:item; shared>tracking:chore; shared>tracking:session |
| batches#r67 | execution | shared>specification:file; shared>specification/tracking:item; shared>tracking:chore; shared>tracking:session |
| batches#r68 | execution | shared>specification/tracking:item; shared>tracking:chore; shared>tracking:meet; shared>tracking:readiness bar |
| batches#r70 | execution | shared>specification:break; shared>specification:requirement; shared>specification:scenario; shared>specification/tracking:item; shared>tracking:session |
| batches#r71 | execution | shared>specification:corpus; shared>specification:logical form; shared>specification:requirement; shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar |
| batches#r72 | execution | shared>specification:corpus; shared>specification:requirement; shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar; shared>tracking:requirement id |
| batches#r73 | execution | shared>specification:requirement; shared>specification:rule; shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar; specification:catalogue entry; specification:use |
| batches#r74 | execution | shared>specification:construct; shared>specification:requirement; shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar; specification:construct catalogue; specification:use |
| batches#r75 | execution | shared>specification:construct; shared>specification:requirement; shared>specification/tracking:item; specification:construct catalogue; specification:use |
| batches#r76 | execution | shared>specification:capability; shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar; shared>upgrades:index file |
| batches#r77 | execution | shared>specification:scenario; shared>specification:succeed; shared>specification/tracking:item; shared>tracking:session |
| batches#r78 | execution | shared>specification:break; shared>specification:capability; shared>specification:feature; shared>specification:scenario; shared>specification/tracking:item; shared>tracking:requirement id; shared>tracking:session |
| batches#r79 | execution | shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar; specification:adapter contract; specification:operation table |
| batches#r80 | execution | shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar; specification:adapter contract; specification:operation; specification:operation table |
| batches#r81 | execution | shared>specification:requirement; shared>specification/tracking:item |
| batches#r83 | execution | shared>specification/tracking:item |
| batches#r87 | execution | shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar; specification:operation; tracking:domain model; tracking:model line; tracking:restate |
| batches#r89 | execution | shared>specification:requirement; shared>specification:rule; shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar; specification:severity |
| batches#r90 | execution | shared>specification:requirement; shared>specification/tracking:item |
| batches#r91 | execution | shared>specification/tracking:item; shared>tracking:session; specification:operation; tracking:domain model; tracking:model line; tracking:restate |
| batches#r92 | execution | shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar; specification:adapter contract; specification:operation; specification:operation table; tracking:domain model; tracking:model line; tracking:specify |
| batches#r93 | execution | analysis/tracking:exceed; shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar; tracking:the review limit |
| batches#r94 | execution | analysis/tracking:exceed; shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar; tracking:dependency; tracking:the review limit |
| batches#r95 | execution | shared>specification:bounded context; shared>specification:term; shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar; specification:import; specification:pack |
| batches#r96 | execution | shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar |
| batches#r97 | execution | shared>specification:requirement; shared>specification:scenario; shared>specification:succeed; shared>specification/tracking:item; shared>tracking:meet; shared>tracking:readiness bar; shared>tracking:requirement id; specification:refer; specification:retire |
| checking#r19 | specification | shared>tracking:requirement id |
| checking#r70 | specification | shared>tracking:requirement id |
| code-analysis#r1 | analysis | shared>specification:break; shared>specification:repository; shared>specification:test |
| code-analysis#r2 | analysis | shared>specification:repository |
| code-analysis#r3 | analysis | shared>specification:test; specification:execute; specification:number |
| code-analysis#r4 | analysis | shared>specification:test; specification:execute |
| code-analysis#r5 | analysis | shared>specification:test; specification:execute |
| code-analysis#r8 | analysis | shared>specification:test; specification:execute |
| code-analysis#r9 | analysis | specification:number |
| code-analysis#r11 | analysis | shared>specification:file |
| code-analysis#r12 | analysis | shared>specification:file |
| code-analysis#r13 | analysis | shared>specification:repository |
| code-analysis#r14 | analysis | shared>specification:repository |
| code-analysis#r15 | analysis | shared>specification:repository |
| code-analysis#r16 | analysis | shared>specification:repository |
| consistency#r13 | specification | shared>tracking:requirement id |
| context-requests#r6 | tracking | shared>specification:bounded context |
| context-requests#r7 | tracking | shared>specification:bounded context; shared>specification:text; specification:identify |
| context-requests#r10 | tracking | shared>specification:bounded context |
| context-requests#r12 | tracking | shared>specification:bounded context |
| context-requests#r14 | tracking | shared>execution:cite; shared>specification:bounded context |
| context-requests#r17 | tracking | shared>specification:bounded context |
| context-requests#r21 | tracking | specification:the entry form |
| context-requests#r26 | tracking | shared>specification:bounded context |
| context-requests#r30 | tracking | shared>specification:repository |
| context-requests#r31 | tracking | shared>specification:repository |
| context-requests#r32 | tracking | shared>specification:repository |
| context-requests#r33 | tracking | shared>specification:bounded context |
| context-requests#r34 | tracking | shared>specification:bounded context |
| context-requests#r35 | tracking | shared>specification:bounded context |
| context-requests#r36 | tracking | shared>specification:bounded context |
| context-requests#r37 | tracking | specification:the entry form |
| context-requests#r38 | tracking | specification:the entry form |
| context-requests#r39 | tracking | shared>specification:bounded context |
| context-requests#r40 | tracking | specification:the entry form |
| context-requests#r46 | tracking | shared>specification:bounded context |
| context-requests#r47 | tracking | shared>specification:capability; shared>specification:requirement |
| context-requests#r48 | tracking | shared>specification:capability; shared>specification:requirement; shared>specification:term; specification:mention |
| context-requests#r49 | tracking | shared>specification:capability |
| context-requests#r50 | tracking | shared>specification:bounded context; shared>specification:capability; shared>specification:requirement; shared>specification:term; specification:mention |
| context-requests#r58 | tracking | shared>specification:term |
| directives#r1 | tracking | shared>execution:cite |
| drafting#r3 | tracking | shared>specification:universal condition |
| drafting#r8 | tracking | shared>specification:requirement |
| drafting#r9 | tracking | shared>specification:requirement |
| drafting#r10 | tracking | shared>specification:capability |
| drafting#r11 | tracking | shared>specification:capability |
| drafting#r12 | tracking | shared>specification:universal condition |
| drafting#r13 | tracking | shared>specification:universal condition |
| drafting#r14 | tracking | shared>specification:requirement |
| drafting#r15 | tracking | shared>specification:capability; shared>specification:requirement |
| drafting#r16 | tracking | shared>specification:capability; shared>specification:requirement |
| drafting#r17 | tracking | shared>specification:requirement |
| drafting#r18 | tracking | shared>specification:requirement |
| drafting#r20 | tracking | shared>specification:requirement |
| drafting#r22 | tracking | shared>specification:capability |
| drafting#r23 | tracking | shared>specification:capability |
| drafting#r24 | tracking | shared>specification:requirement; specification:retire |
| drafting#r25 | tracking | shared>specification:capability; shared>specification:term |
| drafting#r26 | tracking | shared>specification:capability |
| drafting#r27 | tracking | shared>specification:capability; shared>specification:requirement |
| drafting#r28 | tracking | shared>specification:design-decision; shared>specification:requirement; specification:enforce |
| drafting#r29 | tracking | shared>specification:requirement |
| drafting#r30 | tracking | shared>specification:requirement |
| drafting#r31 | tracking | specification:operation table |
| drafting#r32 | tracking | specification:operation; specification:operation table |
| drafting#r33 | tracking | specification:operation; specification:operation table |
| drafting#r34 | tracking | specification:operation |
| drafting#r35 | tracking | shared>specification:capability |
| drafting#r36 | tracking | shared>specification:capability |
| drafting#r37 | tracking | shared>execution:batch; shared>specification:capability; shared>specification:requirement |
| drafting#r38 | tracking | shared>specification:requirement |
| drafting#r39 | tracking | shared>specification:requirement |
| drafting#r40 | tracking | shared>specification:requirement |
| drafting#r41 | tracking | specification:operation |
| drafting#r42 | tracking | specification:operation; specification:operation table |
| drafting#r47 | tracking | shared>specification:term |
| drafting#r48 | tracking | shared>specification:term |
| drafting#r49 | tracking | shared>specification:term |
| drafting#r50 | tracking | shared>specification:term |
| drafting#r51 | tracking | shared>specification:term; specification:pack |
| drafting#r52 | tracking | shared>specification:term; specification:pack |
| drafting#r53 | tracking | shared>specification:universal condition |
| drafting#r56 | tracking | shared>specification:universal condition |
| drafting#r59 | tracking | shared>specification:universal condition |
| drafting#r62 | tracking | shared>specification:universal condition |
| feature-reading#r1 | analysis | shared>specification:scenario; specification:contain; specification:number |
| feature-reading#r2 | analysis | shared>specification:scenario; specification:number |
| feature-reading#r3 | analysis | shared>specification:repository; specification:contain |
| feature-reading#r4 | analysis | shared>specification:repository; shared>specification:scenario |
| feature-reading#r5 | analysis | shared>specification:repository; shared>specification:scenario |
| feature-reading#r6 | analysis | shared>specification:repository; shared>specification:scenario |
| feature-reading#r7 | analysis | shared>specification:repository; shared>specification:scenario; specification:contain |
| feature-reading#r9 | analysis | shared>specification:repository; shared>specification:scenario |
| feature-reading#r10 | analysis | shared>specification:repository; shared>specification:scenario |
| feature-reading#r11 | analysis | shared>specification:repository; shared>specification:scenario |
| feature-reading#r12 | analysis | shared>specification:file; shared>specification:repository; shared>specification:scenario |
| feature-reading#r13 | analysis | shared>specification:repository; shared>specification:scenario |
| feature-reading#r14 | analysis | shared>specification:file; shared>specification:repository; shared>specification:scenario |
| items#r5 | tracking | shared>specification:rule; shared>specification:term |
| items#r6 | tracking | shared>specification:requirement; specification:translation |
| items#r7 | tracking | shared>specification:capability; shared>specification:universal condition; specification:translation |
| items#r8 | tracking | shared>specification:requirement; specification:parse; specification:translation |
| items#r9 | tracking | shared>specification:requirement |
| items#r10 | tracking | shared>specification:requirement group; shared>specification:rule |
| items#r24 | tracking | shared>execution:task; shared>execution:workspace; shared>specification:repository |
| items#r25 | tracking | shared>execution:shared workspace; shared>execution:workspace; shared>specification:repository |
| items#r29 | tracking | shared>execution:batch |
| items#r40 | tracking | shared>specification:construct; shared>specification:requirement; specification:catalogue entry; specification:use |
| items#r41 | tracking | shared>specification:rule |
| items#r50 | tracking | shared>specification:requirement |
| items#r51 | tracking | shared>specification:requirement |
| items#r53 | tracking | shared>specification:requirement; shared>specification:universal condition |
| items#r54 | tracking | shared>specification:requirement; shared>specification:universal condition; specification:translation |
| measurement#r2 | measurement | execution:grade; shared>execution:batch; shared>execution:proposed change; shared>execution:review finding; specification:number |
| measurement#r3 | measurement | shared>execution:batch; shared>execution/specification/tracking/upgrades:status; shared>specification/tracking:item |
| measurement#r5 | measurement | specification:number |
| measurement#r7 | measurement | specification:number |
| measurement#r9 | measurement | specification:number |
| measurement#r10 | measurement | shared>execution:batch |
| measurement#r12 | measurement | shared>execution:batch; shared>execution/specification/tracking/upgrades:status |
| quotes#r1 | tracking | shared>execution:cite |
| quotes#r3 | tracking | shared>execution:cite |
| quotes#r4 | tracking | shared>execution:cite |
| records#r5 | specification | shared>execution:batch |
| records#r6 | specification | shared>execution:batch |
| records#r9 | specification | shared>execution/tracking:observation |
| request-watch#r1 | tracking | shared>specification:bounded context; specification:the entry form |
| request-watch#r2 | tracking | shared>specification:bounded context; specification:the entry form |
| request-watch#r3 | tracking | shared>specification:bounded context |
| request-watch#r4 | tracking | shared>specification:bounded context |
| request-watch#r5 | tracking | shared>specification:bounded context |
| request-watch#r6 | tracking | specification:the entry form |
| request-watch#r7 | tracking | specification:the entry form |
| review-guarantees#r1 | execution | shared>measurement:dispatch |
| review-guarantees#r2 | execution | shared>measurement:dispatch; shared>specification:design-decision; specification:tier |
| review-guarantees#r3 | execution | shared>measurement:dispatch |
| review-guarantees#r4 | execution | shared>measurement:dispatch; shared>specification:requirement; shared>specification/tracking:item; tracking:propose |
| review-guarantees#r5 | execution | shared>measurement:dispatch |
| review-guarantees#r6 | execution | shared>tracking:session |
| review-guarantees#r7 | execution | shared>measurement:dispatch |
| review-guarantees#r8 | execution | shared>tracking:session |
| review-guarantees#r9 | execution | shared>measurement:dispatch |
| review-guarantees#r10 | execution | shared>measurement:dispatch |
| reviews#r1 | execution | shared>specification/tracking:item |
| reviews#r2 | execution | shared>specification/tracking:item |
| reviews#r4 | execution | shared>specification/tracking:item |
| reviews#r7 | execution | shared>specification:file; shared>specification/tracking:item |
| reviews#r8 | execution | shared>specification:file; shared>specification/tracking:item |
| scenarios#r2 | specification | shared>analysis:handler |
| toolchain#r5 | analysis | shared>specification:file; specification:execute |
| toolchain#r11 | analysis | shared>specification:version; shared>upgrades:pin; shared>upgrades:plugin |
| trials#r11 | measurement | shared>tracking:session |
| trials#r12 | measurement | execution:review; shared>specification:file; shared>tracking:session |
| trials#r13 | measurement | shared>tracking:session |
| trials#r14 | measurement | shared>tracking:session |
| trials#r15 | measurement | shared>tracking:session |
| upgrades#r1 | upgrades | shared>specification:bounded context; shared>specification:file; shared>specification:repository; specification:mention |
| upgrades#r2 | upgrades | shared>specification:bounded context; shared>specification:design-decision; shared>specification:repository; specification:decisions index |
| upgrades#r3 | upgrades | shared>specification:bounded context; shared>specification:design-decision; specification:supersede |
| upgrades#r4 | upgrades | shared>specification:bounded context; shared>specification:design-decision; specification:supersede |
| upgrades#r5 | upgrades | shared>specification:bounded context |
| upgrades#r6 | upgrades | shared>specification:bounded context; shared>specification:capability |
| upgrades#r7 | upgrades | shared>specification:bounded context |
| upgrades#r8 | upgrades | shared>specification:bounded context; shared>specification:repository |
| upgrades#r9 | upgrades | shared>specification:repository |
| upgrades#r10 | upgrades | shared>specification:repository; specification:release |
| upgrades#r11 | upgrades | shared>specification:repository |
| upgrades#r12 | upgrades | shared>specification:repository; shared>specification:version |
| upgrades#r13 | upgrades | shared>specification:repository |
| upgrades#r14 | upgrades | shared>specification:repository |
| upgrades#r15 | upgrades | shared>specification:capability; shared>specification:repository; specification:language |
| upgrades#r16 | upgrades | shared>analysis:tag; shared>specification:feature; shared>specification:repository; shared>specification:requirement; shared>specification:scenario; specification:mention |
| upgrades#r17 | upgrades | shared>specification:repository; shared>specification:text; shared>tracking:session; specification:release |
| upgrades#r18 | upgrades | shared>specification:repository; shared>tracking:session |
| upgrades#r19 | upgrades | shared>specification:repository; shared>specification:text; shared>specification:version; shared>tracking:session |
| upgrades#r20 | upgrades | shared>specification:repository; specification:decisions index |
| upgrades#r21 | upgrades | shared>specification:repository |
| upgrades#r22 | upgrades | shared>specification:repository |
| upgrades#r23 | upgrades | shared>specification:repository |
| upgrades#r24 | upgrades | shared>specification:bounded context; shared>specification:repository; shared>specification:rule; shared>specification:term |
| upgrades#r25 | upgrades | shared>specification:bounded context; shared>specification:capability; shared>specification:repository |
| upgrades#r26 | upgrades | shared>specification:repository; shared>specification:rule; shared>specification:term |
| upgrades#r27 | upgrades | shared>specification:file; shared>specification:repository; shared>specification:text |
| upgrades#r28 | upgrades | shared>specification:repository; shared>specification:text; shared>tracking:session |
| upgrades#r29 | upgrades | shared>specification:repository; shared>tracking:session |
| upgrades#r30 | upgrades | shared>specification:repository; shared>specification:text |
| upgrades#r32 | upgrades | shared>specification:bounded context |
| upgrades#r33 | upgrades | shared>specification:bounded context |
| upgrades#r34 | upgrades | shared>specification:bounded context; shared>specification:file |
| upgrades#r35 | upgrades | shared>specification:bounded context; shared>specification:file; shared>specification:repository |
| upgrades#r36 | upgrades | shared>specification:repository |
| upgrades#r37 | upgrades | shared>specification:repository |
| upgrades#r41 | upgrades | shared>specification:bounded context; shared>specification:repository |
| upgrades#r43 | upgrades | shared>specification:bounded context; shared>specification:repository |
| upgrades#r42 | upgrades | shared>specification:bounded context; shared>specification:repository |

## d. Python imports between module groups

Modules per group:

| group | modules | lines |
|---|---|---|
| analysis | 9 | 1092 |
| cli | 7 | 852 |
| execution | 27 | 3592 |
| language | 74 | 10750 |
| measurement | 9 | 896 |
| plumbing | 9 | 998 |
| specification | 33 | 4849 |
| tracking | 55 | 7704 |
| upgrades | 18 | 2278 |

| group | members |
|---|---|
| analysis | features_bindings, features_gherkin, features_report, tools_check, tools_env, tools_grammar, tools_map, tools_refs, tools_size |
| cli | features, measure, migrate, model, spec, tools, work |
| execution | batch_amend, batch_base_merge, batch_brief, batch_catalogues, batch_cli, batch_close, batch_driver, batch_estimate, batch_findings, batch_fix, batch_gh, batch_git, batch_laid, batch_merge, batch_parked, batch_pick, batch_plan, batch_reach, batch_reopen, batch_rerun, batch_review, batch_reviewed, batch_start, batch_tasks, batch_timings, delivery_settings, work_items |
| language | features_generate, features_generate4, features_vocab4, features_vocab4_request, model_catalogue, model_catalogue_entries, model_catalogue_write, model_constructs, model_constructs_table, model_explain, model_rules, spec_catalogued, spec_corpus_write, spec_entail, spec_entail_chain, spec_entail_rules, spec_example, spec_findings, spec_follow4, spec_frames, spec_gf, spec_grammar4, spec_held, spec_language, spec_lexicon, spec_lexicon_problems, spec_lf, spec_lf_clause, spec_lf_compare, spec_lf_core, spec_lf_distinct, spec_lf_exist, spec_lf_facts, spec_lf_facts_atoms, spec_lf_facts_request, spec_lf_ids, spec_lf_member, spec_lf_modal, spec_lf_none, spec_lf_np, spec_lf_number, spec_lf_option, spec_lf_order, spec_lf_ordered, spec_lf_quant, spec_lf_read, spec_lf_request, spec_lf_set, spec_lf_time, spec_lf_values, spec_logic_vocab, spec_meaning, spec_one_thing, spec_packs, spec_parse_cache, spec_prefetch, spec_refusal4, spec_relations, spec_rgl, spec_rgl_np, spec_rgl_ops, spec_rgl_rel, spec_rgl_steps, spec_rgl_time, spec_rgl_vocab, spec_solve, spec_solve_pairs, spec_steps4, spec_steps4_boxes, spec_steps4_bring, spec_steps4_counter, spec_steps4_held, spec_steps4_request, spec_value_kinds |
| measurement | measure_batch, measure_batch_read, measure_batch_sessions, measure_batch_show, measure_cost, measure_defect, measure_show, measure_write, transcripts |
| plumbing | adapter_cli, adapter_cli_probe, adapter_cli_respond, domain_envelope, model_parse, shop_files, shop_refused, store_git, toml_edit |
| specification | adapter_annotate, adapter_cli_check, adapter_tables, contract_form, decision_amend, decision_write, domain_model, domain_model_check, domain_model_parse, domain_model_props, model_check, model_contract, model_decisions, model_domain, model_domain_lines, model_facts, model_forms, model_report, model_requests, model_restates, model_spec, model_work, observation_write, record_design, record_write, spec_context, spec_moves, spec_preview, spec_read, spec_read_given, spec_unbuilt, spec_vocabulary, spec_vocabulary_terms |
| tracking | backlog_adapter, backlog_adapter_ops, backlog_capability, backlog_chore, backlog_cli, backlog_forms, backlog_items, backlog_lines, backlog_model, backlog_model_area, backlog_model_edit, backlog_model_ops, backlog_moves, backlog_note, backlog_pack, backlog_piece_edit, backlog_recodify, backlog_retirements, backlog_retires, backlog_retract, backlog_reword, backlog_section, backlog_split, backlog_universal, backlog_view, conversation_cli, conversation_hook, conversation_names, conversation_prompt, conversation_quote, conversation_read, directive, directive_cli, intake_moves, readiness_bar, readiness_before, request_accept, request_cli, request_form, request_forward, request_gh, request_hook, request_lines, request_moves, request_post, request_side, request_steps, request_sync, request_terms, request_text, request_view, request_watch, request_watch_hook, shop_frozen, shop_ids |
| upgrades | migrate_init, migrate_layout, migrate_ledger, migrate_spec, migrate_upgrade, migrate_upgrade_answers, migrate_upgrade_cnl4, migrate_upgrade_cnl4_report, migrate_upgrade_codified, migrate_upgrade_conftest, migrate_upgrade_domain, migrate_upgrade_domain_report, migrate_upgrade_domain_scaffold, migrate_upgrade_frames, migrate_upgrade_ids, migrate_upgrade_simplified, migrate_upgrade_values, migrate_write |

Import statements from one group to another (static and inside functions): 393

| from group | to group | imports | examples |
|---|---|---|---|
| specification | language | 49 | adapter_annotate->spec_grammar4, adapter_annotate->spec_language, adapter_annotate->spec_lexicon, adapter_annotate->spec_lf, domain_model->spec_held, model_domain->spec_grammar4 ... |
| tracking | plumbing | 38 | backlog_capability->shop_files, backlog_chore->shop_files, backlog_forms->shop_files, backlog_items->shop_files, backlog_model->shop_files, backlog_model_area->shop_files ... |
| execution | tracking | 35 | batch_amend->backlog_items, batch_amend->backlog_lines, batch_amend->readiness_bar, batch_brief->backlog_chore, batch_brief->backlog_items, batch_brief->backlog_lines ... |
| specification | plumbing | 32 | adapter_annotate->adapter_cli, adapter_annotate->shop_refused, adapter_cli_check->adapter_cli, adapter_tables->adapter_cli, adapter_tables->shop_refused, contract_form->model_parse ... |
| execution | plumbing | 28 | batch_amend->shop_files, batch_base_merge->shop_files, batch_brief->shop_files, batch_cli->shop_files, batch_close->shop_files, batch_driver->shop_files ... |
| tracking | specification | 25 | backlog_adapter->adapter_tables, backlog_adapter->domain_model, backlog_adapter_ops->adapter_tables, backlog_adapter_ops->domain_model, backlog_cli->decision_amend, backlog_cli->domain_model ... |
| upgrades | language | 18 | migrate_upgrade_cnl4->spec_frames, migrate_upgrade_cnl4->spec_lexicon, migrate_upgrade_cnl4->spec_packs, migrate_upgrade_cnl4_report->spec_example, migrate_upgrade_cnl4_report->spec_language, migrate_upgrade_cnl4_report->spec_lexicon ... |
| tracking | language | 16 | backlog_forms->spec_lexicon, backlog_lines->spec_held, backlog_lines->spec_lexicon, backlog_pack->spec_packs, readiness_bar->features_generate, readiness_bar->spec_catalogued ... |
| cli | specification | 13 | features->spec_read, features->spec_unbuilt, spec->model_check, spec->model_contract, spec->model_facts, spec->model_forms ... |
| language | specification | 13 | features_generate->spec_context, features_generate->spec_read, features_generate4->spec_read_given, model_explain->spec_context, model_rules->model_check, spec_corpus_write->spec_read ... |
| cli | tracking | 11 | work->backlog_chore, work->backlog_cli, work->backlog_items, work->backlog_note, work->backlog_split, work->backlog_view ... |
| cli | plumbing | 10 | features->adapter_cli_respond, features->model_parse, measure->adapter_cli_respond, migrate->adapter_cli_respond, spec->adapter_cli_respond, spec->model_parse ... |
| measurement | execution | 9 | measure_batch->batch_brief, measure_batch->batch_findings, measure_batch->batch_git, measure_batch->batch_pick, measure_batch->batch_plan, measure_batch->batch_timings ... |
| execution | specification | 8 | batch_amend->spec_unbuilt, batch_start->adapter_annotate, batch_start->model_check, batch_start->model_facts, batch_start->spec_read, batch_start->spec_unbuilt ... |
| cli | analysis | 8 | features->features_bindings, features->features_gherkin, features->features_report, tools->tools_check, tools->tools_env, tools->tools_map ... |
| specification | tracking | 8 | model_domain->backlog_items, model_facts->shop_ids, model_work->shop_frozen, model_work->shop_ids, record_write->shop_ids, spec_preview->backlog_items ... |
| upgrades | plumbing | 7 | migrate_init->shop_files, migrate_init->shop_refused, migrate_upgrade->shop_files, migrate_upgrade_codified->model_parse, migrate_upgrade_domain->model_parse, migrate_upgrade_simplified->model_parse ... |
| cli | language | 6 | features->features_generate, features->features_vocab4, features->spec_gf, features->spec_rgl_steps, spec->model_rules |
| cli | measurement | 6 | measure->measure_batch, measure->measure_batch_show, measure->measure_defect, measure->measure_show, measure->measure_write |
| cli | upgrades | 6 | migrate->migrate_init, migrate->migrate_layout, migrate->migrate_ledger, migrate->migrate_spec, migrate->migrate_upgrade, migrate->migrate_write |
| tracking | execution | 5 | backlog_retract->batch_plan, backlog_view->batch_plan, conversation_names->batch_plan, request_forward->batch_gh, request_gh->batch_gh |
| execution | language | 5 | batch_amend->spec_corpus_write, batch_catalogues->model_constructs, batch_catalogues->model_rules, batch_start->features_generate, batch_start->spec_corpus_write |
| tracking | measurement | 5 | conversation_cli->transcripts, conversation_quote->transcripts, conversation_read->transcripts, directive_cli->transcripts |
| measurement | plumbing | 5 | measure_batch->shop_files, measure_cost->shop_files, measure_defect->shop_files, measure_write->shop_files, transcripts->shop_refused |
| upgrades | specification | 4 | migrate_init->record_write, migrate_upgrade_domain->spec_read, migrate_upgrade_simplified->model_report, migrate_upgrade_values->spec_read |
| language | plumbing | 4 | model_catalogue->model_parse, model_catalogue_write->shop_files, model_catalogue_write->toml_edit, spec_grammar4->model_parse |
| tracking | upgrades | 3 | conversation_names->migrate_write, conversation_prompt->migrate_write, directive->migrate_write |
| analysis | plumbing | 3 | features_gherkin->shop_refused, tools_env->shop_refused, tools_grammar->shop_refused |
| language | analysis | 3 | spec_gf->tools_grammar, spec_grammar4->tools_grammar, spec_rgl_steps->tools_grammar |
| measurement | tracking | 2 | measure_batch->backlog_items, measure_defect->backlog_items |
| language | tracking | 2 | spec_corpus_write->backlog_items, spec_corpus_write->backlog_lines |
| cli | execution | 2 | work->batch_cli, work->delivery_settings |
| execution | measurement | 1 | delivery_settings->measure_cost |
| upgrades | tracking | 1 | migrate_upgrade_simplified->request_text |
| specification | analysis | 1 | model_decisions->tools_env |
| tracking | analysis | 1 | readiness_before->tools_grammar |

Fan-in by group (imports from other groups):

| group | imported from other groups |
|---|---|
| plumbing | 127 |
| language | 94 |
| specification | 63 |
| tracking | 59 |
| execution | 16 |
| analysis | 13 |
| measurement | 12 |
| upgrades | 9 |

