---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/design-model-check
title: Design model check
narrator: a person or session verifying a repository against the design model
group: service
language: codified-1
rests_on: [design-decision/final-layout, design-decision/references-are-ids, design-decision/light-decisions, design-decision/model-check-solves-with-clingo, design-decision/a-scenario-names-one-requirement, design-decision/query-commands-answer-in-their-output, design-decision/retired-ids-in-capability-frontmatter, design-decision/work-file-forms, design-decision/capability-ids-are-context-scoped, design-decision/one-requirement-form, design-decision/review-of-work-items, design-decision/work-items-named-by-ids, design-decision/the-glossary-is-a-target-of-spec-work]
retired: [r8, r9, r12, r13, r14, r15, r16, r17, r18, r21, r26, r27, r29, r31, r32, r33, r34, r35, r37, r39, r45, r46, r53, g73, r73, g72, r72]
unbuilt: [r145, r159]
---

# Design model check

## Purpose
`scripts/model` reads a bounded context's files — spec, feature files, decisions, work and records, in the final
layout and no other — as the facts of design model v5 (`docs/design-model/`), and prints what the model refuses,
each rule by its code and its plain label. It also writes the generated decisions index, lists the rules, and traces
a requirement to why it exists. It does not edit the spec, the work or the records, and it verifies one bounded
context: product-level artifacts are read only where the files contain them.

## Terms
- **rule** (noun): a relation of `scripts/model.lp`, with its code and its plain label: a violation's or a warning's.
- **decisions index** (noun): the generated file `spec/decisions/index.md`. Plural: decisions indexes. Kind of: file.
- **interpreter** (noun): a `python3` that `model` runs under or tries.
- **clingoless** (adjective of interpreter): an interpreter that cannot import clingo, where a `python3` on `PATH` can.
- **unfound** (adjective of interpreter): an interpreter that cannot import clingo, where no interpreter `model` tries can.
- **stale** (adjective of decisions index): a decisions index that is not what `model decisions` would write.
- **sound** (adjective of bounded context): a bounded context in which `model check` finds no violation, unresolved reference or file problem.
- **unmigrated** (adjective of bounded context): a bounded context with `spec/decisions.md`, or with a `decisions/`, `work/` or `records/` directory at its root.
- **unnumbered** (adjective of capability): a capability with a requirement bullet in its Behaviour that has no `[r<n>]`.
- **renumbered** (adjective of capability): a capability two of whose requirements have the same id.
- **reusing** (adjective of capability): a capability that uses an id it lists as retired.
- **misnamed** (adjective of capability): a capability whose `id` is not `capability/<context path>/<file name>`, or that has no `## Behaviour`.
- **untested** (adjective of requirement): a requirement that no scenario names, of a capability that is not of the group `guarantees`.
- **avoiding** (adjective of requirement): a requirement that mentions a word its context's glossary lists after `Not:`.
- **unparsed** (adjective of requirement): a requirement that does not parse in its context's requirement grammar.
- **overtagged** (adjective of scenario): a scenario not tagged `@deprecated` that has more than one `@r<n>` tag.
- **misreferring** (adjective of scenario): a scenario that names a requirement its capability does not have.
- **misfiled** (adjective of feature): a feature that is not `features/<name>.feature` for a capability `<name>`.
- **duplicated** (adjective of term): a term that two glossary entries have as their term.
- **selfavoiding** (adjective of term): a term with a word after `Not:` that is a term of the context, or the term itself.
- **malformed** (adjective of term): a term whose bullet in the `## Glossary` of `spec/index.md` is in no form of a term entry.
- **reaching** (adjective of capability-proposal): a `drafted` or `approved` capability-proposal that changes a requirement no capability has.
- **unformulated** (adjective of capability-proposal): a `formulated` capability-proposal that adds a requirement with no scenario, of a capability that is not of the group `guarantees`.
- **plural** (adjective of capability-proposal): a capability-proposal that argues more than one capability.
- **dangling** (adjective of capability-proposal): a capability-proposal that adds or removes an id its capability neither has nor lists as retired.
- **termless** (adjective of capability-proposal): a capability-proposal whose `adds`, `changes` or `removes` names a `term/<term>` the glossary does not have.
- **termless** (adjective of glossary-proposal): a glossary-proposal whose `adds`, `changes` or `removes` names a `term/<term>` the glossary does not have.
- **parentless** (adjective of work-item): a work-item with no `part_of`.
- **uncommitted** (adjective of work-item): a work-item that is not `withdrawn` and has no `accepts` and no `check`.
- **misnumbered** (adjective of work-item): a work-item whose file name is not `w<n>.md`.
- **alien** (adjective of work-item): a work-item whose `part_of` has another context's path, on a kind kept in `.shop/work/`.
- **misreferenced** (adjective of work-item): a work-item whose `accepts` names a reference that is not `<capability>#r<n>`.
- **unresolving** (adjective of work-item): a work-item whose `under` names nothing in its repository.
- **misidentified** (adjective of work-item): a work-item whose `id` is not `<kind>/<context path>/<name>` with its own kind.
- **homeless** (adjective of work-item): a work-item whose directory has no `initiative.md`.
- **crowded** (adjective of initiative): an initiative that is not a capability-change and has more than one part directly under it.
- **unrequested** (adjective of initiative): an initiative dated after 2026-10-23 that fulfils no request.
- **unwaiting** (adjective of initiative): a `done` initiative while a request whose asker is its context and that names it is not `delivered`.
- **jobbed** (adjective of initiative): an initiative whose kind is `job` or `job-path`.
- **unanchored** (adjective of request): a request that is part of no job-thread, cites no origin and is raised for no request.
- **misresolved** (adjective of request): a `delivered` request whose resolution names a requirement the spec does not have.
- **misformed** (adjective of request): a request that is not of the form `work request` writes.
- **compound** (adjective of requirement group): a requirement group with more than one statement.
- **repeating** (adjective of requirement group): a requirement group whose statement has the features, condition and trigger of another group's statement in its capability.
- **unexampled** (adjective of requirement group): a requirement group with a given line that is not example data.
- **headless** (adjective of design-decision): a design-decision with no `id` or no `## Decision` section.

- **file form** (noun): one kind of file a bounded context keeps, with its path and the command that writes it. Plural: file forms.

- **unattributed** (adjective of record): a record whose `--about` is not one line or is not the id of a node of the design model.

- **objectless** (adjective of requirement): a requirement with a verb whose glossary entry gives it an object, used with no object.
- **recipientless** (adjective of requirement): a requirement with a verb whose glossary entry gives it a recipient, used with no recipient.
- **frameless** (adjective of term): a verb whose glossary entry does not name the kinds of its subject and object, nor say that it takes no object.
- **relational** (adjective of term): a condition whose definition names with `the` a kind other than the kind it is a condition of.
- **negating** (adjective of requirement): a requirement that says with `not` that a verb or a relation between two kinds does not hold.

- **mistyped** (adjective of requirement): a requirement with a verb whose subject, object or recipient is not of the kind the verb's frame names.

- **addressed** (adjective of requirement): a requirement whose trigger is a verb with its object and, after `to`, its recipient.

- **verbal** (adjective of requirement): a requirement whose condition is a verb between two kinds, positive or with `does not`.
- **agentless** (adjective of requirement): a requirement with a verb whose frame has a subject, used in the passive with no subject.

- **unlabelled** (adjective of term): a term whose entry does not name its part of speech.

- **prepositional** (adjective of term): a verb whose frame puts a preposition between the verb and its object, as in `Frame: viewer subscribes to channel.`.
- **prepositioned** (adjective of requirement): a requirement with a prepositional verb followed by its preposition and its object, as in `a viewer subscribes to a channel`.
- **misframed** (adjective of term): a verb whose glossary entry has a `Frame:` that does not read as its subject, the verb and the kinds the verb takes.

- **unpairable** (adjective of capability): a capability two of whose requirements share a named code that `grammar/check.lp` cannot unify, and two others of whose requirements conflict (an L1).

- **rule catalogue** (noun): the generated file `grammar/rules.md`, one entry a rule. Kind of: file.
- **violate** (verb, state): a thing does not meet a rule of the rule catalogue. Forms: violates, violated. Frame: thing violates rule.
- **stale** (adjective of rule catalogue): a rule catalogue that is not what `model rules --write` would write.

- **aspectless** (adjective of term): a verb whose entry says neither `state` nor `action`.
- **multiframed** (adjective of term): a verb whose entry has two `Frame:` lines.
- **polysemous** (adjective of term): a verb with two entries whose frames take kinds that do not overlap.
- **overlapping** (adjective of term): a verb with two entries whose frames take, in every slot, the same kind or one kind under the other.

- **pack** (noun): a file of terms a bounded context imports: `grammar/packs/<name>.md` of the plugin, or `spec/packs/<name>.md` of the bounded context. Kind of: file.
- **importing** (adjective of bounded context): a bounded context whose `spec/index.md` imports a pack.
- **misimporting** (adjective of bounded context): a bounded context whose `spec/index.md` imports a pack that neither the plugin nor the bounded context has.
- **unmarked** (adjective of term): a term that a pack its bounded context imports defines too, whose entry has no `Redefines:`.
- **redefining** (adjective of term): a term whose entry has `Redefines:` naming a pack that defines it.

- **plural** (adjective of requirement): a requirement whose subject is plural and whose verb agrees with it, as in "When sessions write a file".
- **disagreeing** (adjective of requirement): a requirement whose verb does not agree in number with its subject, as in "When sessions writes a file".

- **misaspected** (adjective of requirement): a requirement with an action verb in its While clause or a state verb in its trigger.
- **optioned** (adjective of requirement): a requirement whose trigger runs a command with an option, as in "runs `work backlog` with the `--json` option".

- **genitive** (adjective of requirement): a requirement with "of" or "its" over a relation row or an attribute, as in "the branch of the task".
- **denying** (adjective of requirement): a requirement with "no" before a noun as a subject or an object, as in "a verb has no frame".
- **compound** (adjective of requirement): a requirement with a compound noun that an attribute or a relation row derives, as in "the batch status".
- **restrictive** (adjective of requirement): a requirement with "only" before an object, as in "a worker shall change only files in its worktree".

- **relative** (adjective of requirement): a requirement with a relative clause on a verb's frame, as in "a channel that a viewer subscribes to".
- **possessive** (adjective of requirement): a requirement with "whose" over a relation row or an attribute, as in "a verb whose entry has no frame".
- **ambiguous** (adjective of requirement): a requirement with two readings that mean different things, as in a list that may belong to either of two verbs.

- **logical form** (noun): what a requirement means, as referents, atoms and boxes, printed by `model parse --form`.
- **indexical** (adjective of requirement): a requirement that says "this" before a kind whose entry has `This:`.

- **antecedentless** (adjective of requirement): a requirement with "the" before a noun that no earlier noun phrase, functional relation or declared indexical gives.
- **unquantified** (adjective of requirement): a requirement whose While clause says "does not" before a noun phrase with "a" or "an", as in "an item does not hold a commit".
- **triggerless** (adjective of requirement): a requirement with no trigger and neither "always" nor "never".

- **unfinished** (adjective of requirement): a requirement that stops where its frame needs another word.

- **exemplified** (adjective of requirement): a requirement holding a code or a quoted string that names no actor, command, option, value, rule or named instance.

- **restricting** (adjective of capability): a capability with a line that obliges an agent to change only things of one kind, and a line in which that agent changes a thing of that kind.
- **exhaustive** (adjective of capability): a capability with a line that obliges a tool to print every thing of a kind and a line that forbids it to print a thing of that kind, under one trigger and state.

- **overriding** (adjective of capability): a capability with an If line and a When line of one trigger whose responses differ, where the If line's state holds.
- **contravening** (adjective of capability): a capability with a line whose response a universal condition forbids, under the line's trigger.

- **restating** (adjective of requirement): a requirement each of whose Thens other requirements entail.

- **counted** (adjective of requirement): a requirement with "at least", "at most", "exactly", "more than" or "fewer than" before a number and a noun.
- **overcounted** (adjective of capability): a capability with two lines of one trigger and state whose counts of one kind cannot both hold.

- **timed** (adjective of requirement): a requirement that compares a moment or a duration with "after", "before", "since" or "within the last".
- **clocked** (adjective of requirement): a requirement whose trigger is the clock reaching a moment.
- **historical** (adjective of requirement): a requirement whose While clause says that an agent has done an action, as in "the batch has published a pull request".
- **unitless** (adjective of requirement): a requirement with a number where a duration is due and no unit of the time pack after it.

- **permissive** (adjective of requirement): a requirement that says an agent may do an action.
- **invariant** (adjective of requirement): a requirement with no trigger that says a thing always holds or never holds.
- **forbidding** (adjective of capability): a capability with a line that forbids what another of its lines says an agent may do.

- **recodified** (adjective of capability): a capability whose file has `language: codified-2` in its frontmatter.

- **refusing** (adjective of requirement): a requirement whose response says that a tool shall refuse a command.
- **overridden** (adjective of requirement): a When requirement over which an If requirement of the same trigger takes precedence.

## Behaviour

### [g1] `model check` exits successfully on a sound context
Restates: r1@0.29.
- [r1] When the person runs `model check` on a bounded context that is sound, `model` shall print "0 violations" and exit successfully.

### [g2] `model check` prints a violation under its rule's code
Restates: r2@0.29, r3@0.29, spec-integration#r16@0.29.
- [r2] If the person runs `model check` on a capability that is unnumbered, then `model` shall exit with an error naming `v15a`.

### [g3] Two requirements with one id
Restates: r4@0.29.
- [r3] If the person runs `model check` on a capability that is renumbered, then `model` shall exit with an error naming `v15b`.

### [g4] A retired id used again
Restates: r5@0.29.
- [r4] If the person runs `model check` on a capability that is reusing, then `model` shall exit with an error naming `v15c`.

### [g5] A group with more than one statement
- [r5] If the person runs `model check` on a requirement group that is compound, then `model` shall exit with an error naming `v15l`.

### [g6] Two groups of a capability that share their features, condition and trigger
- [r6] If the person runs `model check` on a requirement group that is repeating, then `model` shall exit with an error naming `v15n`.

### [g7] A given line that is not example data
- [r7] If the person runs `model check` on a requirement group that is unexampled, then `model` shall exit with an error naming `v15m`.

### [g10] A requirement with no scenario
Restates: r8@0.29.
- [r10] If the person runs `model check` on a requirement that is untested, then `model` shall exit with an error naming `v_s3`.

### [g11] A scenario that names more than one requirement
Restates: r107@0.29.
- [r11] If the person runs `model check` on a scenario that is overtagged, then `model` shall exit with an error naming `v_s2`.

### [g19] A request with no origin
Restates: r120@0.29.
- [r19] If the person runs `model check` on a request that is unanchored, then `model` shall exit with an error naming `v17`.

### [g20] A delivered request resolved by no requirement of the spec
Restates: r116@0.29.
- [r20] If the person runs `model check` on a request that is misresolved, then `model` shall exit with an error naming `v3`.

### [g22] A requirement that uses an avoided word
Restates: r52@0.29.
- [r22] If the person runs `model check` on a requirement that is avoiding, then `model` shall exit with an error naming `v_t1`.

### [g23] Two glossary entries with one term
Restates: r53@0.29.
- [r23] If the person runs `model check` on a term that is duplicated, then `model` shall exit with an error naming `v_t2`.

### [g24] An avoided word that is a term
Restates: r54@0.29.
- [r24] If the person runs `model check` on a term that is selfavoiding, then `model` shall exit with an error naming `v_t3`.

### [g25] A requirement that does not parse
Restates: r103@0.29, r104@0.29.
- [r25] If the person runs `model check` on a requirement that is unparsed, then `model` shall exit with an error naming `v_p1`.

### [g28] A request not of the form `work request` writes
Restates: r112@0.29.
- [r28] If the person runs `model check` on a request that is misformed, then `model` shall exit with an error naming the request.

### [g30] A scenario that names a requirement its capability does not have
Restates: r9@0.29.
- [r30] If the person runs `model check` on a scenario that is misreferring, then `model` shall exit with an error naming the scenario.

### [g36] A capability not named by its file
Restates: r25@0.29.
- [r36] If the person runs `model check` on a capability that is misnamed, then `model` shall exit with an error naming the capability.

### [g38] A feature file of no capability
Restates: r26@0.29.
- [r38] If the person runs `model check` on a feature that is misfiled, then `model` shall exit with an error naming the feature.

### [g40] A decision with no id or no Decision section
Restates: r29@0.29.
- [r40] If the person runs `model check` on a design-decision that is headless, then `model` shall exit with an error naming the design-decision.

### [g41] A glossary bullet in no form of a term entry
Restates: r48@0.29, r49@0.29.
- [r41] If the person runs `model check` on a term that is malformed, then `model` shall exit with an error naming the term.

### [g42] A repository not on the final layout
Restates: r61@0.29.
- [r42] If the person runs `model check` on a bounded context that is unmigrated, then `model` shall exit with an error naming `scripts/migrate`.

### [g43] A warning leaves the exit as it is
Restates: r11@0.29.
- [r43] When the person runs `model check` on an observation that is uncited, `model` shall print `w_uncited_obs` and exit successfully.

### [g44] A context with no job has no unserved capability
Restates: r111@0.29.
- [r44] When the person runs `model check`, `model` shall not print `w_unserved_cap`.

### [g47] `model check` tries again under an interpreter that has clingo
Restates: r55@0.29.
- [r47] While an interpreter is clingoless, when the person runs `model check`, `model` shall print "0 violations".

### [g48] No interpreter has clingo
Restates: r12@0.29.
- [r48] While an interpreter is unfound, if the person runs `model check`, then `model` shall exit with an error naming "pip install clingo".

### [g49] `model facts` prints the facts
Restates: r13@0.29.
- [r49] When the person runs `model facts`, `model` shall print every fact.

### [g50] `model decisions` writes the decisions index
Restates: r14@0.29, spec-integration#r22@0.29.
- [r50] When the person runs `model decisions`, `model` shall write a decisions index.

### [g51] `model decisions --check` refuses a stale index
Restates: r15@0.29.
- [r51] Where `--check` is given, if the person runs `model decisions` on a decisions index that is stale, then `model` shall exit with an error naming the decisions index and change nothing.

### [g52] `model decisions --check` passes a current index
Restates: r37@0.29.
- [r52] Where `--check` is given, when the person runs `model decisions` on a decisions index, `model` shall exit successfully.

### [g54] `model rules` prints every rule
Restates: r65@0.29.
- [r54] When the person runs `model rules`, `model` shall print every rule and exit successfully.

### [g55] `model forms` lists every file form
- [r55] When the person runs `model forms`, `model` shall print every file form and exit successfully.

### [g56] `work record` writes and commits a record
- [r56] When the person runs `work record`, `work` shall write a record and commit the record.

### [g57] `work record` refuses an unattributed record
- [r57] If the person runs `work record` on a record that is unattributed, then `work` shall exit with an error naming `--about` and change nothing.

### [g58] `model parse` refuses a verb with no object
- [r58] If the person runs `model parse` on a requirement that is objectless, then `model` shall exit with an error naming the term.

### [g59] `model parse` refuses a verb with no recipient
- [r59] If the person runs `model parse` on a requirement that is recipientless, then `model` shall exit with an error naming the term.

### [g60] `model check` refuses a verb with no frame
- [r60] If the person runs `model check` on a term that is frameless, then `model` shall exit with an error naming the term.

### [g61] `model check` refuses a condition that relates two kinds
- [r61] If the person runs `model check` on a term that is relational, then `model` shall exit with an error naming the term.

### [g62] `model parse` parses a negated verb or relation
- [r62] When the person runs `model parse` on a requirement that is negating, `model` shall exit successfully.

### [g63] `model parse` refuses a verb with a noun of the wrong kind
- [r63] If the person runs `model parse` on a requirement that is mistyped, then `model` shall exit with an error naming the term.

### [g66] `model parse` parses a trigger with a recipient
- [r66] When the person runs `model parse` on a requirement that is addressed, `model` shall exit successfully.

### [g64] `model parse` parses a verb between two kinds in a condition
- [r64] When the person runs `model parse` on a requirement that is verbal, `model` shall exit successfully.

### [g65] `model parse` refuses a passive with no agent
- [r65] If the person runs `model parse` on a requirement that is agentless, then `model` shall exit with an error naming the term.

### [g67] `model check` refuses a term with no part of speech
- [r67] If the person runs `model check` on a term that is unlabelled, then `model` shall exit with an error naming the term.

### [g68] `model check` reads a prepositional verb's frame
- [r68] When the person runs `model check` on a term that is prepositional, `model` shall exit successfully.

### [g69] `model parse` parses a prepositional verb with its preposition
- [r69] When the person runs `model parse` on a requirement that is prepositioned, `model` shall exit successfully.

### [g70] `model check` refuses a frame that does not read
- [r70] If the person runs `model check` on a term that is misframed, then `model` shall exit with an error naming the term.

### [g71] A pair that cannot be unified sets only itself aside
- [r71] When the person runs `model logic` on a capability that is unpairable, `model` shall print a requirement and print "L1".

### [g74] `model rules --write` writes the rule catalogue
- [r74] When the person runs `model rules --write`, `model` shall write the rule catalogue and exit successfully.

### [g75] `model rules --check` refuses a stale rule catalogue
- [r75] If the person runs `model rules --check` on a rule catalogue that is stale, then `model` shall exit with an error naming the rule catalogue and change nothing.

### [g76] `model check` refuses a verb with no aspect
- [r76] If the person runs `model check` on a term that is aspectless, then `model` shall exit with an error naming the term.

### [g77] `model check` passes a verb with two frames
- [r77] When the person runs `model check` on a term that is multiframed, `model` shall exit successfully.

### [g78] `model check` passes a verb with two senses told apart by kinds
- [r78] When the person runs `model check` on a term that is polysemous, `model` shall exit successfully.

### [g79] `model check` refuses two senses that overlap
- [r79] If the person runs `model check` on a term that is overlapping, then `model` shall exit with an error naming the term.

### [g80] `model lexicon` shows the terms of the imported packs
- [r80] When the person runs `model lexicon` on a bounded context that is importing, `model` shall print every term and exit successfully.

### [g81] `model check` refuses an import of no pack
- [r81] If the person runs `model check` on a bounded context that is misimporting, then `model` shall exit with an error naming the pack.

### [g82] `model check` refuses a pack's term redefined without Redefines:
- [r82] If the person runs `model check` on a term that is unmarked, then `model` shall exit with an error naming the term.

### [g83] `model check` passes a term marked Redefines:
- [r83] When the person runs `model check` on a term that is redefining, `model` shall exit successfully.

### [g84] `model parse` passes a plural subject whose verb agrees
- [r84] When the person runs `model parse` on a requirement that is plural, `model` shall exit successfully.

### [g85] `model parse` refuses a verb that does not agree with its subject
- [r85] If the person runs `model parse` on a requirement that is disagreeing, then `model` shall exit with an error naming the term.

### [g86] `model parse` refuses a verb of the wrong aspect for its clause
- [r86] If the person runs `model parse` on a requirement that is misaspected, then `model` shall exit with an error naming the term.

### [g87] `model parse` passes a trigger that runs a command with an option
- [r87] When the person runs `model parse` on a requirement that is optioned, `model` shall exit successfully.

### [g88] `model parse` passes of and its over a relation row or an attribute
- [r88] When the person runs `model parse` on a requirement that is genitive, `model` shall exit successfully.

### [g89] `model parse` passes no before a subject or an object
- [r89] When the person runs `model parse` on a requirement that is denying, `model` shall exit successfully.

### [g90] `model parse` passes a derived compound noun
- [r90] When the person runs `model parse` on a requirement that is compound, `model` shall exit successfully.

### [g91] `model parse` passes only before an object
- [r91] When the person runs `model parse` on a requirement that is restrictive, `model` shall exit successfully.

### [g92] `model parse` passes a relative clause on a verb's frame
- [r92] When the person runs `model parse` on a requirement that is relative, `model` shall exit successfully.

### [g93] `model parse` passes whose over a relation row or an attribute
- [r93] When the person runs `model parse` on a requirement that is possessive, `model` shall exit successfully.

### [g94] `model parse` refuses a requirement with two meanings
- [r94] If the person runs `model parse` on a requirement that is ambiguous, then `model` shall exit with an error naming the requirement.

### [g95] `model parse --form` prints a requirement's logical form
- [r95] When the person runs `model parse --form` on a requirement, `model` shall print a logical form and exit successfully.

### [g96] `model parse` passes this before a kind whose entry has This:
- [r96] When the person runs `model parse` on a requirement that is indexical, `model` shall exit successfully.

### [g97] `model parse` refuses the with no antecedent
- [r97] If the person runs `model parse` on a requirement that is antecedentless, then `model` shall exit with an error naming the term.

### [g98] `model parse` refuses a negated indefinite in a While clause
- [r98] If the person runs `model parse` on a requirement that is unquantified, then `model` shall exit with an error naming the term.

### [g99] `model parse` refuses a requirement with no trigger and neither always nor never
- [r99] If the person runs `model parse` on a requirement that is triggerless, then `model` shall exit with an error naming the requirement.

### [g100] `model parse` refuses an unfinished requirement with the terms that may follow
- [r100] If the person runs `model parse` on a requirement that is unfinished, then `model` shall exit with an error naming the requirement and print a term.

### [g101] `model check` warns of example data in a line
- [r101] When the person runs `model check` on a requirement that is exemplified, `model` shall print the requirement.

### [g131] `model logic` finds no clash between only and a change of that kind
- [r131] When the person runs `model logic` on a capability that is restricting, `model` shall not print "L1".

### [g132] `model logic` finds the clash of every and a forbidden print
- [r132] When the person runs `model logic` on a capability that is exhaustive, `model` shall print "L1".

### [g133] `model logic` reads an If line as taking precedence over a When line
- [r133] When the person runs `model logic` on a capability that is overriding, `model` shall not print "L1".

### [g134] `model logic` pairs a universal condition with the lines it bears on
- [r134] When the person runs `model logic` on a capability that is contravening, `model` shall print the universal condition.

### [g135] `model logic` reports a requirement that other requirements entail
- [r135] When the person runs `model logic` on a requirement that is restating, `model` shall print "L8".

### [g136] `model parse` reads a count
- [r136] When the person runs `model parse` on a requirement that is counted, `model` shall exit successfully.

### [g137] `model logic` finds two counts that cannot both hold
- [r137] When the person runs `model logic` on a capability that is overcounted, `model` shall print "L1".

### [g138] `model parse` reads a comparison of moments
- [r138] When the person runs `model parse` on a requirement that is timed, `model` shall exit successfully.

### [g139] `model parse` reads the clock as a trigger
- [r139] When the person runs `model parse` on a requirement that is clocked, `model` shall exit successfully.

### [g140] `model parse` reads the perfect as history
- [r140] When the person runs `model parse` on a requirement that is historical, `model` shall exit successfully.

### [g141] `model parse` refuses a duration with no unit
- [r141] If the person runs `model parse` on a requirement that is unitless, then `model` shall exit with an error naming the requirement.

### [g142] `model parse` reads a permission
- [r142] When the person runs `model parse` on a requirement that is permissive, `model` shall exit successfully.

### [g143] `model parse` reads always and never with no trigger
- [r143] When the person runs `model parse` on a requirement that is invariant, `model` shall exit successfully.

### [g144] `model logic` finds a line that forbids what another permits
- [r144] When the person runs `model logic` on a capability that is forbidding, `model` shall print "L7".

### [g145] `model logic` checks a capability in the new language
- [r145] When the person runs `model logic` on a capability that is recodified, `model` shall exit successfully.

### [g156] `model explain` prints a requirement
- [r156] When the person runs `model explain` on a requirement, `model` shall print the requirement and exit successfully.

### [g157] `model explain` prints what a refusal entails and where it comes from
- [r157] When the person runs `model explain` on a requirement that is refusing, `model` shall print a universal condition and a term.

### [g158] `model explain` prints the If requirement that takes precedence
- [r158] When the person runs `model explain` on a requirement that is overridden, `model` shall print a requirement that is refusing.

### [g159] `model explain` refuses an id that no capability holds
- [r159] If the person runs `model explain` on a requirement that is nonexistent, then `model` shall exit with an error naming the requirement and change nothing.

## Implementation, may change
- `scripts/model.lp` is design model v5's graph in clingo; facts use its relation names. Each rule's plain label is a
  fact `label("<code>", "<label>")` beside the rule, the one place it is written; `check` and `rules` read the labels
  from the solve, and a unit test fails when a relation has no label or two.
- `model` reads, under `--root` (default the current directory), only `spec/index.md`, `spec/universal.md`,
  `spec/restated.json`, `spec/capabilities/*.md`, every `*.feature` under `features/`, every `spec/decisions/*.md` but
  `index.md` and `README.md`, `.shop/requests/*.md`, the `source` of the frozen `.shop/work/*/initiative.md` and
  `.shop/work/requests/*.md` (as citations of observations), `.shop/records/observations.md` and any other Markdown under `.shop/records/` whose frontmatter has an `id`.
- References: `<name>#r<n>` or `capability/<name>#r<n>` is a requirement of `capability/<context path>/<name>`;
  `<capability>#r<a>-r<b>` in a list is every id from a to b; `<cap>#r<n>@0.29` is resolved through
  `spec/restated.json`. A node is `<kind>/<context path>/<name>` or `<kind>/<name>`, and a bare `<name>` only in a
  field that fixes the kind (`rests_on`, `supersedes`, `argues`, `under`, `depends_on`) or the capability part of a
  reference. A decision's `source`, and not its `by`, is a list of ids.
- The glossary of `spec/index.md` (and each capability's `## Terms`) is read by `spec_lexicon` where the index is
  codified; a term is `term/<context path>/<term>`, and each word after `Not:` a word it avoids. A requirement or a
  scenario mentions a term or avoided word when it contains it as a whole word, whatever its case, with a plural "s"
  allowed, outside code spans, double-quoted strings and `@` tags.
- A scenario's `@g<n>` tag names the group that generates it, and its `@r<n>` tags the group's requirements.
- Output: `<code>  <label>  (<count>)` above a violated relation's rows; `warning <code>  <label>  (<count>)`;
  `rules` prints `<code>  <label>`, the violations first and then the warnings. `--json` adds `"labels": {code: label}`
  for the codes it prints, and `check --json` exits as it would without `--json`.
- Without `--json`, `model check` ends with the counts of violations, warnings, unresolved references and file
  problems. `--limit <n>` (default 10) prints at most n rows of each violated relation and how many more there are.
- If `import clingo` fails, `model check` tries again, once, under the first interpreter that has clingo of
  `$SHOPSYSTEM_MODEL_PYTHON`, each `python3` on `PATH` outside the active virtualenv's `bin/`,
  `/usr/local/bin/python3` and `/usr/bin/python3`, in that order; with none, it names each one it tried.
- An initiative may be `done` when its parts are closed: a `formulated` capability-proposal, an `approved`
  glossary-proposal and any `withdrawn` part count as closed.
- `model facts` prints the facts, one a line in clingo's syntax, using only the standard library.
- `model decisions` writes `spec/decisions/index.md` listing every decision in `spec/decisions/` that has an `id`,
  with its summary, status, what it supersedes and when to revisit it, each linked to its file; `--check` says
  whether the file is current. `model why <capability>#r<n>` prints the requirement's text (or that no capability has
  it), each capability-proposal that adds, changes or removes it in date order with its status and date, the
  `part_of` chain to its initiative and the initiative's sources; given an argument that is not a requirement
  reference it exits 2.
- Exit code: 0 success; 1 a violation, unresolved reference or file problem found, or a decisions index that is
  not current; 2 no interpreter has clingo, or bad usage.

## Not yet
- Product-level artifacts (jobs, the context-map, seams, pins) read from a product repository — trigger: a second bounded context is verified together with this one.

## Dropped
- r18@0.29: the reading of a range is `model`'s implementation, kept under Implementation, may change.
- r19@0.29: the files `model` reads are its implementation, kept under Implementation, may change.
- r20@0.29: a scenario's tags are read as design model v5's generates (C4, C6), kept under Implementation, may change.
- r21@0.29: the reading of a reference is `model`'s implementation, kept under Implementation, may change.
- r43@0.29: the reading of a node's id is `model`'s implementation, kept under Implementation, may change.
- r51@0.29: what counts as a mention is `model`'s implementation, kept under Implementation, may change.
- r64@0.29: the reading of a decision's source is `model`'s implementation, kept under Implementation, may change.
- r105@0.29: restated U3 (a refused command exits with an error and changes nothing).
- r33@0.29: restated U8 (`--json` prints one JSON object), for `model check`.
- r108@0.29: restated U8 (`--json` prints one JSON object), for `model why`.
- r109@0.29: restated U8 (`--json` prints one JSON object), for `model rules`.
- r6@0.29: retired with design-model-check#r8 in 2.0.0 (the-old-workflow-retired).
- r7@0.29: retired with design-model-check#r9 in 2.0.0 (the-old-workflow-retired).
- r10@0.29: retired with design-model-check#r12 in 2.0.0 (the-old-workflow-retired).
- r16@0.29: retired with design-model-check#r53 in 2.0.0 (the-old-workflow-retired).
- r17@0.29: retired with design-model-check#r53 in 2.0.0 (the-old-workflow-retired).
- r22@0.29: retired with design-model-check#r31 in 2.0.0 (the-old-workflow-retired).
- r23@0.29: retired with design-model-check#r32 in 2.0.0 (the-old-workflow-retired).
- r24@0.29: retired with design-model-check#r33 in 2.0.0 (the-old-workflow-retired).
- r34@0.29: retired with design-model-check#r13 in 2.0.0 (the-old-workflow-retired).
- r35@0.29: retired with design-model-check#r14 in 2.0.0 (the-old-workflow-retired).
- r36@0.29: retired with design-model-check#r45 in 2.0.0 (the-old-workflow-retired).
- r46@0.29: retired with design-model-check#r37 in 2.0.0 (the-old-workflow-retired).
- r59@0.29: retired with design-model-check#r15 in 2.0.0 (the-old-workflow-retired).
- r66@0.29: retired with design-model-check#r34 in 2.0.0 (the-old-workflow-retired).
- r106@0.29: retired with design-model-check#r26 in 2.0.0 (the-old-workflow-retired).
- r110@0.29: retired with design-model-check#r27 in 2.0.0 (the-old-workflow-retired).
- r113@0.29: retired with design-model-check#r16 in 2.0.0 (the-old-workflow-retired).
- r114@0.29: retired with design-model-check#r17 in 2.0.0 (the-old-workflow-retired).
- r118@0.29: retired with design-model-check#r29 in 2.0.0 (the-old-workflow-retired).
- r119@0.29: retired with design-model-check#r18 in 2.0.0 (the-old-workflow-retired).
- r121@0.29: retired with design-model-check#r21 in 2.0.0 (the-old-workflow-retired).
- r122@0.29: retired with design-model-check#r35 in 2.0.0 (the-old-workflow-retired).
- r123@0.29: retired with design-model-check#r46 in 2.0.0 (the-old-workflow-retired).
- r124@0.29: retired with design-model-check#r39 in 2.0.0 (the-old-workflow-retired).
