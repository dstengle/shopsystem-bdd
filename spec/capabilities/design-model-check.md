---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/design-model-check
title: Design model check
narrator: a person or session verifying a repository against the design model
group: service
language: codified-2
rests_on: [design-decision/final-layout, design-decision/references-are-ids, design-decision/light-decisions, design-decision/model-check-solves-with-clingo, design-decision/a-scenario-names-one-requirement, design-decision/query-commands-answer-in-their-output, design-decision/retired-ids-in-capability-frontmatter, design-decision/work-file-forms, design-decision/capability-ids-are-context-scoped, design-decision/one-requirement-form, design-decision/review-of-work-items, design-decision/work-items-named-by-ids, design-decision/the-glossary-is-a-target-of-spec-work]
retired: [r8, r9, r12, r13, r14, r15, r16, r17, r18, r21, r26, r27, r29, r31, r32, r33, r34, r35, r37, r39, r45, r46, r53, g73, r73, g72, r72, g1, r1, g2, r2, g3, r3, g4, r4, g5, r5, g6, r6, g7, r7, g10, r10, g11, r11, g19, r19, g20, r20, g22, r22, g23, r23, g24, r24, g25, r25, g28, r28, g30, r30, g36, r36, g38, r38, g40, r40, g41, r41, g42, r42, g43, r43, g44, r44, g47, r47, g48, r48, g49, r49, g51, r51, g52, r52, g57, r57, g58, r58, g59, r59, g60, r60, g61, r61, g62, r62, g63, r63, g64, r64, g65, r65, g66, r66, g67, r67, g68, r68, g69, r69, g70, r70, g71, r71, g74, r74, g75, r75, g76, r76, g77, r77, g78, r78, g79, r79, g80, r80, g81, r81, g82, r82, g83, r83, g84, r84, g85, r85, g86, r86, g87, r87, g88, r88, g89, r89, g90, r90, g91, r91, g92, r92, g93, r93, g94, r94, g95, r95, g96, r96, g97, r97, g98, r98, g99, r99, g100, r100, g101, r101, g131, r131, g132, r132, g133, r133, g134, r134, g135, r135, g136, r136, g137, r137, g138, r138, g139, r139, g140, r140, g141, r141, g142, r142, g143, r143, g144, r144, g145, r145, g157, r157, g158, r158, g159, r159, g160, r160, g161, r161, g162, r162, g163, r163, g164, r164, g165, r165, g166, r166, g167, r167, g168, r168, g169, r169, g170, r170, g171, r171, g172, r172, g173, r173]
unbuilt: []
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

- **duplicated** (adjective of term): a term that two glossary entries have as their term.
- **file form** (noun): one kind of file a bounded context keeps, with its path and the command that writes it. Plural: file forms.

- **rule catalogue** (noun): the generated file `grammar/rules.md`, one entry a rule. Kind of: file.

- **pack** (noun): a file of terms a bounded context imports: `grammar/packs/<name>.md` of the plugin, or `spec/packs/<name>.md` of the bounded context. Kind of: file.

- **logical form** (noun): what a requirement means, as referents, atoms and boxes, printed by `model parse --form`.

- **recodified** (adjective of capability): a capability whose file has `language: codified-2` in its frontmatter.

- **embedding** (adjective of requirement): a requirement of a capability whose file has `language: codified-2`, with "the" before a noun inside a modifier of a noun phrase of the same kind, where an earlier noun phrase of that kind gives it, as in "When the person runs `work request --raised-for` on a request, `work` shall write a request raised for the request.".

- **intransitive** (adjective of requirement): a requirement of a capability whose file has `language: codified-2`, whose While clause has a state verb whose frame takes no object, as in "a test fails" under `Frame: test fails.`.

- **self-relating** (adjective of requirement): a requirement of a capability whose file has `language: codified-2`, with "the K of X" inside a relative clause on a noun phrase of kind K, as in "When the person runs `work batch review` on a batch, `work` shall write a review that lists the review of the pull request.".
- **relation reading** (noun): a logical form in which "the K of X" inside a relative clause on a noun phrase of kind K is a referent of its own, the K of X, and not the referent of that noun phrase. Plural: relation readings. Kind of: logical form.
- **distributive** (adjective of requirement): a requirement of a capability whose file has `language: codified-2`, with "the K of every Y" in its response, as in "When the person runs `work batch status`, `work` shall print the pull request of every batch.".
- **distributed reading** (noun): a logical form in which "the K of every Y" is a referent inside the box of "every Y", one K of each Y, and not one K of all of them. Plural: distributed readings. Kind of: logical form.

- **shadowed** (adjective of requirement): a requirement of a capability whose file has `language: codified-2`, with "the K" after a noun phrase of kind K inside a "no", "not", "every" or "only" box that does not hold "the K", and after a noun phrase of kind K outside that box, as in "While an item has no dependency on an item whose status is not `delivered`, when the person runs `work batch start`, `work` shall pick the item.".
- **accessible reading** (noun): a logical form in which "the K" is the latest earlier referent of kind K that is not inside a "no", "not", "every" or "only" box which does not hold "the K", and not a referent inside such a box. Plural: accessible readings. Kind of: logical form.

- **setting** (adjective of requirement): a requirement of a capability whose file has `language: codified-2`, whose response says that an agent shall set an attribute of a thing the line names earlier to a value, as in "set the status of the request to `delivered`" or "set its status to `delivered`".

- **violate** (verb, state): a thing does not meet a rule of the rule catalogue. Forms: violates, violated. Frame: thing violates rule.
- **frame** (noun): one `Frame:` of a verb's entry: the kinds its subject, object and recipient take. Kind of: text.
- **subject** (noun): the noun phrase before a verb in a clause, or the kind a frame names before its verb. Kind of: thing.
- **object** (noun): the noun phrase a verb takes after it, or the kind a frame names after its verb. Kind of: thing.
- **recipient** (noun): the noun phrase a verb takes after its object and a preposition, or the kind a frame names there. Kind of: thing.
- **preposition** (noun): a word such as `to` or `on` that a frame puts before an object or a recipient. Kind of: thing.
- **omit** (verb, state): a requirement uses a term and leaves out a word that a frame of the term needs. Forms: omits, omitted. Frame: requirement omits thing.
- **job** (noun): a job of the product that a capability of a bounded context serves. Kind of: thing.
- **`clingo`** (proper noun): the answer set solver that `model` imports. Kind of: thing.
- **import** (verb, state): an interpreter can import a Python module. Forms: imports, imported. Frame: interpreter imports thing.
- **import** (verb, state): the `spec/index.md` of a bounded context names a pack under `imports:`. Forms: imports, imported. Frame: bounded context imports pack.
- **index entry** (noun): the row of the decisions index for one design-decision, as `model decisions` writes it from the design-decision's file now. Plural: index entries. Kind of: text.
- **catalogue entry** (noun): the entry of the rule catalogue for one rule, as `model rules --write` writes it from the rule now. Plural: catalogue entries. Kind of: text.
- **aspect** (attribute of term): whether a verb says a lasting condition or an event. Values: `state`, `action`.
- **precondition** (noun): the While clause of a requirement: the condition its trigger happens in. Kind of: text.
- **trigger** (noun): the When or If clause of a requirement: the event it answers. Kind of: text.
- **negation** (noun): "not" before a verb or a relation, as in "a session does not follow a stage". Kind of: thing.
- **noun phrase** (noun): a noun with its determiner and modifiers, given to a verb as its subject, object or recipient. Kind of: thing.
- **take** (verb, state): a frame names, in a slot, the kind of a noun phrase or a kind above it. Forms: takes, taken. Frame: frame takes noun phrase.
- **passive form** (noun): a verb in the passive, as in "a file is written". Kind of: thing.
- **by-phrase** (noun): "by" and a noun phrase after a passive form, naming who does the action. Kind of: thing.
- **sense** (noun): one entry of a term that has several entries, with its frames. Kind of: text.
- **redefine** (verb, state): a term's entry has `Redefines:` naming a pack that defines the term too. Forms: redefines, redefined. Frame: term redefines pack.
- **plural subject** (noun): a subject of more than one thing, its verb in the plural, as in "sessions write". Kind of: thing.
- **agree** (verb, state): a verb is in the number of its subject, as in "a session writes" and "sessions write". Forms: agrees, agreed. Frame: term agrees with subject.
- **genitive** (noun): "of" or "its" over a relation row or an attribute, as in "the branch of the task". Kind of: thing.
- **negative quantifier** (noun): "no" before a noun as a subject or an object, as in "a verb has no frame". Kind of: thing.
- **compound noun** (noun): two nouns read as one, which an attribute or a relation row derives, as in "the batch status". Kind of: thing.
- **restriction** (noun): "only" before an object, as in "a worker shall change only files in its worktree". Kind of: thing.
- **relative clause** (noun): a clause on a noun that says a verb of a frame, as in "a channel that a viewer subscribes to". Kind of: thing.
- **whose clause** (noun): "whose" over a relation row or an attribute, as in "a verb whose entry has no frame". Kind of: thing.
- **demonstrative** (noun): "this" before a kind whose entry has `This:`, naming the run's own thing. Kind of: thing.
- **definite noun phrase** (noun): "the" before a noun. Kind of: noun phrase.
- **antecedent** (noun): what a definite noun phrase refers back to: an earlier noun phrase, a functional relation or a declared indexical. Kind of: thing.
- **negated indefinite** (noun): "does not" before a verb whose object has "a" or "an", as in "an item does not hold a commit". Kind of: thing.
- **modal adverb** (noun): "always" or "never" in a requirement. Kind of: thing.
- **fragment** (noun): a requirement that stops where a frame of its verb needs another word, as in "When a session writes". Kind of: text.
- **unification failure** (noun): two requirements of a capability that share a code `grammar/check.lp` cannot unify. Kind of: thing.
- **clash** (noun): two requirements of a capability that oblige and forbid one act under one trigger and condition, which `model logic` reports as `L1`. Plural: clashes. Kind of: thing.
- **act** (noun): what a requirement's response says an agent does: a verb with its noun phrases. Kind of: thing.
- **allow** (verb, state): a restriction leaves an act inside what it restricts the act to. Forms: allows, allowed. Frame: restriction allows act.
- **universal quantifier** (noun): "every" before a noun in a response, as in "print every file". Kind of: thing.
- **oblige** (verb, state): a text or a part of one says with "shall" that an agent does an act. Forms: obliges, obliged. Frame: thing obliges act.
- **forbid** (verb, state): a text says with "shall not" that an agent does not do an act. Forms: forbids, forbade, forbidden. Frame: text forbids act.
- **override** (verb, state): an If requirement takes precedence over a When requirement of the same trigger whose response differs, where the If requirement's condition holds. Forms: overrides, overrode, overridden. Frame: requirement overrides requirement.
- **consequence** (noun): a response that a requirement obliges: a Then of its scenario. Kind of: thing.
- **premise** (noun): the universal conditions, the definitions of the imported packs and the other requirements of a bounded context, taken together, as what a requirement's consequence may follow from. Kind of: thing.
- **entail** (verb, state): a premise says a consequence already. Forms: entails, entailed. Frame: premise entails consequence.
- **count** (noun): "at least", "at most", "exactly", "more than" or "fewer than" before a number and a noun. Kind of: thing.
- **contradict** (verb, state): no number of things meets both of two counts of one act under one trigger and condition. Forms: contradicts, contradicted. Frame: count contradicts count.
- **comparison** (noun): "after", "before", "since" or "within the last" between a moment or a duration and another. Kind of: thing.
- **clock trigger** (noun): a trigger in which the clock reaches a moment. Kind of: thing.
- **perfect** (noun): "has" before the participle of an action verb, saying that an agent has done the action, as in "the batch has published a pull request". Kind of: thing.
- **number** (noun): a number in a requirement where a duration is due, as the `7` of "within the last 7 days". Kind of: thing.
- **unit** (noun): a unit of the time pack after a number, such as `days`. Kind of: thing.
- **permission** (noun): "may" before an act, saying that an agent may do it. Kind of: thing.
- **permit** (verb, state): a requirement says with "may" that an agent may do an act. Forms: permits, permitted. Frame: requirement permits act.
- **language** (attribute of capability): the controlled language a capability's file is written in, by the `language:` of its frontmatter. Values: `codified-1`, `codified-2`.
- **refusal** (noun): a response in which a tool refuses a command. Kind of: thing.
- **requirement id** (noun): an id `<capability>#r<n>`. Kind of: text.
- **conform** (verb, state): a thing has the form that a file form, an entry form or a layout gives. Forms: conforms, conformed. Frame: thing conforms to thing.
- **the final layout** (proper noun): the files and directories a bounded context keeps, as design-decision/final-layout gives them. Kind of: thing.
- **`v15a`** (proper noun): the rule of the rule catalogue: a requirement has no id. Kind of: rule.
- **`v15b`** (proper noun): the rule of the rule catalogue: two requirements share an id. Kind of: rule.
- **`v15c`** (proper noun): the rule of the rule catalogue: a retired id is used again. Kind of: rule.
- **`v15l`** (proper noun): the rule of the rule catalogue: a group has more than one statement. Kind of: rule.
- **`v15n`** (proper noun): the rule of the rule catalogue: two groups of a capability share features, condition and trigger. Kind of: rule.
- **`v15m`** (proper noun): the rule of the rule catalogue: a given line is not example data. Kind of: rule.
- **`v_s3`** (proper noun): the rule of the rule catalogue: a group has no scenario. Kind of: rule.
- **`v_s2`** (proper noun): the rule of the rule catalogue: a scenario is generated from more than one group. Kind of: rule.
- **`v17`** (proper noun): the rule of the rule catalogue: a request that is part of no job-thread, cites no origin and is raised for no request. Kind of: rule.
- **`v3`** (proper noun): the rule of the rule catalogue: a request's resolution names something that is not a requirement of the spec. Kind of: rule.
- **`v_t1`** (proper noun): the rule of the rule catalogue: a word the glossary avoids. Kind of: rule.
- **`v_t2`** (proper noun): the rule of the rule catalogue: a term has two entries, other than the senses of one verb. Kind of: rule.
- **`v_t3`** (proper noun): the rule of the rule catalogue: an avoided word is a term. Kind of: rule.
- **`v_p1`** (proper noun): the rule of the rule catalogue: a requirement does not parse. Kind of: rule.
- **`w_uncited_obs`** (proper noun): the rule of the rule catalogue: an observation no initiative cites. Kind of: rule.
- **`w_unserved_cap`** (proper noun): the rule of the rule catalogue: a capability serves no job. Kind of: rule.
- **`v_t11`** (proper noun): the rule of the rule catalogue: a verb's entry gives no frame: the kinds of its subject and object, or that it takes no object. Kind of: rule.
- **`v_t12`** (proper noun): the rule of the rule catalogue: a condition names another kind with the: a relation between two kinds is a verb. Kind of: rule.
- **`v_t4`** (proper noun): the rule of the rule catalogue: a term of a typed glossary does not name its part of speech. Kind of: rule.
- **`v_t13`** (proper noun): the rule of the rule catalogue: a verb's Frame: does not read as its subject, the verb and the kinds it takes. Kind of: rule.
- **`v_t14`** (proper noun): the rule of the rule catalogue: a verb's entry says neither state nor action. Kind of: rule.
- **`v_t15`** (proper noun): the rule of the rule catalogue: two entries of one verb take, in every slot, the same kind or one kind under the other. Kind of: rule.
- **`v_t17`** (proper noun): the rule of the rule catalogue: spec/index.md imports a pack that neither the plugin nor the bounded context has. Kind of: rule.
- **`v_t16`** (proper noun): the rule of the rule catalogue: a term an imported pack defines too has no Redefines: naming the pack. Kind of: rule.
- **`w_example`** (proper noun): the rule of the rule catalogue: a requirement holds example data: a code or quoted string that names no declared constant. Kind of: rule.
- **`L1`** (proper noun): the code under which `model logic` prints a clash. Kind of: thing.
- **`L7`** (proper noun): the code under which `model logic` prints a requirement that forbids what another permits. Kind of: thing.
- **`L8`** (proper noun): the code under which `model logic` prints a requirement whose every consequence a premise entails. Kind of: thing.
- **the design model** (proper noun): design model v5 (`docs/design-model/`), a bounded context conforming to it when nothing of it violates a rule of the rule catalogue. Kind of: thing.
- **the request form** (proper noun): the form `work request` writes a request in. Kind of: thing.
- **the entry form** (proper noun): the forms of a term entry that `spec_lexicon` reads. Kind of: thing.
- **the capability id form** (proper noun): `capability/<context path>/<file name>` as the `id` of a capability's frontmatter, its file's name the last part. Kind of: thing.
- **the capability section form** (proper noun): the sections of a capability's file, a `## Behaviour` section among them. Kind of: thing.
- **the feature form** (proper noun): the path `features/<name>.feature` of a capability `<name>`. Kind of: thing.
- **the decision form** (proper noun): an `id` in a design-decision's frontmatter and a `## Decision` section. Kind of: thing.
- **the node id form** (proper noun): one line that is the id of a node of the design model. Kind of: thing.
- **lack** (verb, state): a decisions index does not hold an index entry that `model decisions` would write now. Forms: lacks, lacked. Frame: decisions index lacks index entry.
- **add** (verb, state): a requirement has a consequence that no premise entails. Forms: adds, added. Frame: requirement adds consequence.
- **mismatch** (verb, state): a requirement gives a term a noun phrase that no frame of the term takes. Forms: mismatches, mismatched. Frame: noun phrase mismatches term.
- **disagree** (verb, state): a verb is not in the number of its subject, as in "sessions writes". Forms: disagrees, disagreed. Frame: term disagrees with subject.
- **refer** (verb, state): a scenario names a requirement by its id in an `@r<n>` tag. Forms: refers, referred. Frame: scenario refers to requirement id.
- **oblique recipient** (noun): a recipient that a frame puts behind a preposition other than `to`, as the file of `Frame: agent records thing in file.`. Kind of: recipient.
- **later sense** (noun): a sense of a verb whose entry is not the first entry of the verb, as "`trial-runner` shall name the target" reads `Frame: agent names thing.` when an entry `Frame: text names thing.` comes before it. Kind of: sense.
- **self-reference** (noun): a definite noun phrase inside a modifier of a noun phrase of its own kind, as "the request" in "a request raised for the request". Plural: self-references. Kind of: definite noun phrase.
- **inner genitive** (noun): a genitive "the K of X" inside a relative clause on a noun phrase of kind K, as "the review of the pull request" in "a review that lists the review of the pull request". Kind of: genitive.
- **distributive genitive** (noun): a genitive "the K of every Y", as "the pull request of every batch" in "print the pull request of every batch". Kind of: genitive.
- **boxed noun phrase** (noun): a noun phrase inside a "no", "not", "every" or "only" box that does not hold a later definite noun phrase of its kind, as "no item" before "the item" in "While no item is `ready`, when the person runs `work batch start`, `work` shall print the item.". Kind of: noun phrase.
- **assignment** (noun): a response in which an agent sets an attribute of a thing that the requirement names earlier to a value, as "set the status of the request to `delivered`". Kind of: thing.
- **`initiates`** (proper noun): the predicate under which a logical form says that an act changes the value of an attribute. Kind of: thing.
- **negated modifier** (noun): a relative clause or a whose clause with "not" on the object of an act, as "an item whose status is not `done`". Kind of: thing.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| subject | of | term |  |
| object | of | term |  |
| recipient | of | term |  |
| frame | of | term |  |
| sense | of | term |  |
| preposition | of | frame |  |
| job | of | bounded context |  |
| fact | of | bounded context |  |
| interpreter | of | command | one |
| index entry | of | design-decision | one |
| index entry | in | decisions index |  |
| catalogue entry | of | rule | one |
| catalogue entry | in | rule catalogue |  |
| precondition | of | requirement | one |
| trigger | of | requirement | one |
| noun phrase | of | term |  |
| by-phrase | of | passive form | one |
| logical form | of | requirement |  |
| antecedent | of | definite noun phrase |  |
| unit | of | number | one |
| term | of | pack |  |
| requirement | of | capability | one |
| requirement id | in | capability |  |
| clash | in | capability |  |
| unification failure | in | capability |  |
| count | in | capability |  |
| consequence | of | requirement |  |
| capability | of | scenario | one |

## Behaviour

### [g50] `model decisions` writes the decisions index
Restates: r14@0.29, spec-integration#r22@0.29.
- [r50] When the person runs `model decisions`, `model` shall write a decisions index.

### [g54] `model rules` prints every rule
Restates: r65@0.29.
- [r54] When the person runs `model rules`, `model` shall print every rule and exit successfully.

### [g55] `model forms` lists every file form
- [r55] When the person runs `model forms`, `model` shall print every file form and exit successfully.

### [g56] `work record` writes and commits a record
- [r56] When the person runs `work record`, `work` shall write a record and commit the record.

### [g156] `model explain` prints a requirement
- [r156] When the person runs `model explain` on a requirement, `model` shall print the requirement and exit successfully.

### [g174] `model check` exits successfully when nothing violates a rule
Restates: r1@0.29.
- [r174] While this bounded context conforms to the design model, when the person runs `model check`, `model` shall print no violation and exit successfully.

### [g175] `model check` prints a violation under its rule's code
Restates: r2@0.29, r3@0.29, spec-integration#r16@0.29.
- [r175] While a capability violates `v15a`, if the person runs `model check`, then `model` shall exit with an error naming `v15a`.

### [g176] Two requirements with one id
Restates: r4@0.29.
- [r176] While a capability violates `v15b`, if the person runs `model check`, then `model` shall exit with an error naming `v15b`.

### [g177] A retired id used again
Restates: r5@0.29.
- [r177] While a capability violates `v15c`, if the person runs `model check`, then `model` shall exit with an error naming `v15c`.

### [g178] A group with more than one statement
- [r178] While a requirement group violates `v15l`, if the person runs `model check`, then `model` shall exit with an error naming `v15l`.

### [g179] Two groups of a capability that share their features, condition and trigger
- [r179] While a requirement group violates `v15n`, if the person runs `model check`, then `model` shall exit with an error naming `v15n`.

### [g180] A given line that is not example data
- [r180] While a requirement group violates `v15m`, if the person runs `model check`, then `model` shall exit with an error naming `v15m`.

### [g181] A requirement with no scenario
Restates: r8@0.29.
- [r181] While a requirement group violates `v_s3`, if the person runs `model check`, then `model` shall exit with an error naming `v_s3`.

### [g182] A scenario that names more than one requirement
Restates: r107@0.29.
- [r182] While a scenario violates `v_s2`, if the person runs `model check`, then `model` shall exit with an error naming `v_s2`.

### [g183] A request with no origin
Restates: r120@0.29.
- [r183] While a request violates `v17`, if the person runs `model check`, then `model` shall exit with an error naming `v17`.

### [g184] A delivered request resolved by no requirement of the spec
Restates: r116@0.29.
- [r184] While a request violates `v3`, if the person runs `model check`, then `model` shall exit with an error naming `v3`.

### [g185] A requirement that uses an avoided word
Restates: r52@0.29.
- [r185] While a requirement violates `v_t1`, if the person runs `model check`, then `model` shall exit with an error naming `v_t1`.

### [g186] Two glossary entries with one term
Restates: r53@0.29.
- [r186] While a term violates `v_t2`, if the person runs `model check`, then `model` shall exit with an error naming `v_t2`.

### [g187] An avoided word that is a term
Restates: r54@0.29.
- [r187] While a term violates `v_t3`, if the person runs `model check`, then `model` shall exit with an error naming `v_t3`.

### [g188] A requirement that does not parse
Restates: r103@0.29, r104@0.29.
- [r188] While a requirement violates `v_p1`, if the person runs `model check`, then `model` shall exit with an error naming `v_p1`.

### [g189] A request not of the form `work request` writes
Restates: r112@0.29.
- [r189] While a request does not conform to the request form, if the person runs `model check`, then `model` shall exit with an error naming the request.

### [g190] A scenario that names a requirement its capability does not have
Restates: r9@0.29.
- [r190] While a scenario refers to a requirement id that the capability of the scenario does not hold, if the person runs `model check`, then `model` shall exit with an error naming the scenario.

### [g191] A capability with no capability id
Restates: r25@0.29.
- [r191] While a capability does not conform to the capability id form, if the person runs `model check`, then `model` shall exit with an error naming the capability.

### [g192] A capability with no Behaviour section
- [r192] While a capability does not conform to the capability section form, if the person runs `model check`, then `model` shall exit with an error naming the capability.

### [g193] A feature file of no capability
Restates: r26@0.29.
- [r193] While a feature does not conform to the feature form, if the person runs `model check`, then `model` shall exit with an error naming the feature.

### [g194] A decision with no id or no Decision section
Restates: r29@0.29.
- [r194] While a design-decision does not conform to the decision form, if the person runs `model check`, then `model` shall exit with an error naming the design-decision.

### [g195] A glossary bullet in no form of a term entry
Restates: r48@0.29, r49@0.29.
- [r195] While a term does not conform to the entry form, if the person runs `model check`, then `model` shall exit with an error naming the term.

### [g196] A repository not on the final layout
Restates: r61@0.29.
- [r196] While this bounded context does not conform to the final layout, if the person runs `model check`, then `model` shall exit with an error naming `scripts/migrate`.

### [g197] A warning leaves the exit as it is
Restates: r11@0.29.
- [r197] While an observation violates `w_uncited_obs`, when the person runs `model check`, `model` shall print `w_uncited_obs` and exit successfully.

### [g198] A context with no job has no unserved capability
Restates: r111@0.29.
- [r198] While this bounded context has no job, when the person runs `model check`, `model` shall not print `w_unserved_cap`.

### [g199] `model check` tries again under an interpreter that has clingo
Restates: r55@0.29.
- [r199] While `model check` has an interpreter that does not import `clingo`, when the person runs `model check`, `model` shall use an interpreter that imports `clingo`.

### [g200] No interpreter has clingo
Restates: r12@0.29.
- [r200] While no interpreter imports `clingo`, if the person runs `model check`, then `model` shall refuse the command and name `pip install clingo`.

### [g201] `model facts` prints the facts
Restates: r13@0.29.
- [r201] When the person runs `model facts`, `model` shall print every fact of this bounded context.

### [g202] `model decisions --check` refuses an index that lacks an index entry
Restates: r15@0.29.
- [r202] While a design-decision has an index entry that a decisions index does not hold, if the person runs `model decisions --check`, then `model` shall exit with an error naming the decisions index and change no file.

### [g203] `model decisions --check` passes a current index
Restates: r37@0.29.
- [r203] While no decisions index lacks an index entry, when the person runs `model decisions --check`, `model` shall exit successfully.

### [g204] `work record` refuses an `--about` that identifies nothing
- [r204] If the person runs `work record --about` on a text that does not conform to the node id form, then `work` shall refuse the command and name `--about`.

### [g205] `model parse` refuses a verb with no object
- [r205] If the person runs `model parse` on a requirement that omits an object of a term, then `model` shall refuse the command and name the term.

### [g206] `model parse` refuses a verb with no recipient
- [r206] If the person runs `model parse` on a requirement that omits a recipient of a term, then `model` shall refuse the command and name the term.

### [g207] `model check` refuses a verb with no frame
- [r207] While a term violates `v_t11`, if the person runs `model check`, then `model` shall exit with an error naming the term.

### [g208] `model check` refuses a condition that relates two kinds
- [r208] While a term violates `v_t12`, if the person runs `model check`, then `model` shall exit with an error naming the term.

### [g209] `model parse` parses a negated verb or relation
- [r209] When the person runs `model parse` on a requirement that uses a negation, `model` shall exit successfully.

### [g210] `model parse` refuses a verb with a noun of the wrong kind
- [r210] If the person runs `model parse` on a requirement that uses a noun phrase that mismatches a term, then `model` shall refuse the command and name the term.

### [g211] `model parse` parses a verb between two kinds in a condition
- [r211] When the person runs `model parse` on a requirement whose precondition uses a term whose aspect is `state`, `model` shall exit successfully.

### [g212] `model parse` refuses a passive with no agent
- [r212] If the person runs `model parse` on a requirement that uses a passive form that has no by-phrase, then `model` shall refuse the command and name the passive form.

### [g213] `model parse` parses a trigger with a recipient
- [r213] When the person runs `model parse` on a requirement whose trigger uses a recipient, `model` shall exit successfully.

### [g214] `model check` refuses a term with no part of speech
- [r214] While a term violates `v_t4`, if the person runs `model check`, then `model` shall exit with an error naming the term.

### [g215] `model check` reads a frame with a preposition
- [r215] While a frame of a term has a preposition, when the person runs `model check`, `model` shall exit successfully.

### [g216] `model parse` parses a verb whose frame has a preposition
- [r216] When the person runs `model parse` on a requirement that uses a term whose frame has a preposition, `model` shall exit successfully.

### [g217] `model check` refuses a frame that does not read
- [r217] While a term violates `v_t13`, if the person runs `model check`, then `model` shall exit with an error naming the term.

### [g218] A pair that cannot be unified sets only itself aside
- [r218] While a capability holds a unification failure and the capability holds a clash, when the person runs `model logic`, `model` shall print the clash and print `L1`.

### [g219] `model rules --write` writes the rule catalogue
- [r219] When the person runs `model rules --write`, `model` shall write a rule catalogue and exit successfully.

### [g220] `model rules --check` refuses a catalogue that lacks a catalogue entry
- [r220] While a rule has a catalogue entry that a rule catalogue does not hold, if the person runs `model rules --check`, then `model` shall exit with an error naming the rule catalogue and change no file.

### [g221] `model check` refuses a verb with no aspect
- [r221] While a term violates `v_t14`, if the person runs `model check`, then `model` shall exit with an error naming the term.

### [g222] `model check` passes a verb with two frames
- [r222] While a term has more than one frame, when the person runs `model check`, `model` shall exit successfully.

### [g223] `model check` passes a verb with two senses told apart by kinds
- [r223] While a term has more than one sense, when the person runs `model check`, `model` shall exit successfully.

### [g224] `model check` refuses two senses that overlap
- [r224] While a term violates `v_t15`, if the person runs `model check`, then `model` shall exit with an error naming the term.

### [g225] `model lexicon` shows the terms of the imported packs
- [r225] While this bounded context imports a pack, when the person runs `model lexicon`, `model` shall print every term of the pack and exit successfully.

### [g226] `model check` refuses an import of no pack
- [r226] While this bounded context imports a pack that violates `v_t17`, if the person runs `model check`, then `model` shall exit with an error naming the pack.

### [g227] `model check` refuses a pack's term redefined without Redefines:
- [r227] While a term violates `v_t16`, if the person runs `model check`, then `model` shall exit with an error naming the term.

### [g228] `model check` passes a term marked Redefines:
- [r228] While a term redefines a pack, when the person runs `model check`, `model` shall exit successfully.

### [g229] `model parse` passes a plural subject whose verb agrees
- [r229] When the person runs `model parse` on a requirement that uses a plural subject, `model` shall exit successfully.

### [g230] `model parse` refuses a verb that does not agree with its subject
- [r230] If the person runs `model parse` on a requirement that uses a term that disagrees with its subject, then `model` shall refuse the command and name the term.

### [g231] `model parse` refuses a verb of the wrong aspect for its clause
- [r231] While a precondition of a requirement uses a term whose aspect is `action` or the trigger of the requirement uses a term whose aspect is `state`, if the person runs `model parse` on the requirement, then `model` shall refuse the command and name the requirement.

### [g232] `model parse` passes a trigger that runs a command with an option
- [r232] When the person runs `model parse` on a requirement whose trigger uses an option, `model` shall exit successfully.

### [g233] `model parse` passes of and its over a relation row or an attribute
- [r233] When the person runs `model parse` on a requirement that uses a genitive, `model` shall exit successfully.

### [g234] `model parse` passes no before a subject or an object
- [r234] When the person runs `model parse` on a requirement that uses a negative quantifier, `model` shall exit successfully.

### [g235] `model parse` passes a derived compound noun
- [r235] When the person runs `model parse` on a requirement that uses a compound noun, `model` shall exit successfully.

### [g236] `model parse` passes only before an object
- [r236] When the person runs `model parse` on a requirement that uses a restriction, `model` shall exit successfully.

### [g237] `model parse` passes a relative clause on a verb's frame
- [r237] When the person runs `model parse` on a requirement that uses a relative clause, `model` shall exit successfully.

### [g238] `model parse` passes whose over a relation row or an attribute
- [r238] When the person runs `model parse` on a requirement that uses a whose clause, `model` shall exit successfully.

### [g239] `model parse` refuses a requirement with two meanings
- [r239] If the person runs `model parse` on a requirement that has more than one logical form, then `model` shall refuse the command and name the requirement.

### [g240] `model parse --form` prints a requirement's logical form
- [r240] When the person runs `model parse --form` on a requirement, `model` shall print the logical form of the requirement and exit successfully.

### [g241] `model parse` passes this before a kind whose entry has This:
- [r241] When the person runs `model parse` on a requirement that uses a demonstrative, `model` shall exit successfully.

### [g242] `model parse` refuses the with no antecedent
- [r242] If the person runs `model parse` on a requirement that uses a definite noun phrase that has no antecedent, then `model` shall refuse the command and name the definite noun phrase.

### [g243] `model parse` refuses a negated indefinite in a While clause
- [r243] If the person runs `model parse` on a requirement whose precondition uses a negated indefinite, then `model` shall refuse the command and name the negated indefinite.

### [g244] `model parse` refuses a requirement with no trigger and neither always nor never
- [r244] While a requirement has no trigger and the requirement uses no modal adverb, if the person runs `model parse` on the requirement, then `model` shall refuse the command and name the requirement.

### [g245] `model parse` refuses a fragment with the terms that may follow
- [r245] If the person runs `model parse` on a fragment, then `model` shall refuse the command, name the fragment and print a term.

### [g246] `model check` warns of example data in a line
- [r246] While a requirement violates `w_example`, when the person runs `model check`, `model` shall print the requirement.

### [g247] `model logic` finds no clash between only and a change of that kind
- [r247] While a requirement of a capability uses a restriction and a requirement of the capability uses an act that the restriction allows, when the person runs `model logic`, `model` shall exit successfully.

### [g248] `model logic` finds the clash of every and a forbidden print
- [r248] While a requirement of a capability uses a universal quantifier and a requirement of the capability forbids an act that the universal quantifier obliges, when the person runs `model logic`, `model` shall print `L1`.

### [g249] `model logic` reads an If line as taking precedence over a When line
- [r249] While a requirement of a capability overrides a requirement of the capability, when the person runs `model logic`, `model` shall exit successfully.

### [g250] `model logic` pairs a universal condition with the lines it bears on
- [r250] While a universal condition forbids an act that a requirement of a capability obliges, when the person runs `model logic`, `model` shall print the universal condition.

### [g251] `model logic` reports a requirement that other requirements entail
- [r251] While a requirement has a consequence and the requirement adds no consequence, when the person runs `model logic`, `model` shall print `L8`.

### [g252] `model parse` reads a count
- [r252] When the person runs `model parse` on a requirement that uses a count, `model` shall exit successfully.

### [g253] `model logic` finds two counts that cannot both hold
- [r253] While a capability holds a count that contradicts a count, when the person runs `model logic`, `model` shall print `L1`.

### [g254] `model parse` reads a comparison of moments
- [r254] When the person runs `model parse` on a requirement that uses a comparison, `model` shall exit successfully.

### [g255] `model parse` reads the clock as a trigger
- [r255] When the person runs `model parse` on a requirement that uses a clock trigger, `model` shall exit successfully.

### [g256] `model parse` reads the perfect as history
- [r256] When the person runs `model parse` on a requirement whose precondition uses a perfect, `model` shall exit successfully.

### [g257] `model parse` refuses a duration with no unit
- [r257] If the person runs `model parse` on a requirement that uses a number that has no unit, then `model` shall refuse the command and name the requirement.

### [g258] `model parse` reads a permission
- [r258] When the person runs `model parse` on a requirement that uses a permission, `model` shall exit successfully.

### [g259] `model parse` reads always and never with no trigger
- [r259] When the person runs `model parse` on a requirement that uses a modal adverb, `model` shall exit successfully.

### [g260] `model logic` finds a line that forbids what another permits
- [r260] While a requirement of a capability forbids an act that a requirement of the capability permits, when the person runs `model logic`, `model` shall print `L7`.

### [g261] `model logic` checks a capability in the new language
- [r261] While the language of a capability is `codified-2`, when the person runs `model logic`, `model` shall exit successfully.

### [g262] `model explain` prints what a refusal entails and where it comes from
- [r262] When the person runs `model explain` on a requirement that uses a refusal, `model` shall print a universal condition and a term.

### [g263] `model explain` prints the If requirement that takes precedence
- [r263] When the person runs `model explain` on a requirement that a requirement overrides, `model` shall print a requirement that uses a refusal.

### [g264] `model explain` refuses an id that no capability holds
- [r264] If the person runs `model explain` on a requirement id that no capability holds, then `model` shall refuse the command and name the requirement id.

### [g265] `model check` reads a frame with a recipient behind a preposition other than to
- [r265] While a term has an oblique recipient, when the person runs `model check`, `model` shall exit successfully.

### [g266] `model parse` reads a codified-1 line in a verb's later sense
- [r266] While the language of a capability is `codified-1` and a requirement of the capability uses a later sense, when the person runs `model parse` on the requirement, `model` shall exit successfully.

### [g267] `model parse` refuses a definite that only the noun phrase it modifies gives
- [r267] If the person runs `model parse` on a requirement that uses a self-reference that has no antecedent, then `model` shall refuse the command and name the self-reference.

### [g268] `model logic` reads a state verb that takes no object
- [r268] When the person runs `model logic` on a requirement whose precondition uses a term that has no object, `model` shall exit successfully.

### [g269] `model parse --form` reads "the K of X" in a relative clause on a K as its own referent
- [r269] When the person runs `model parse --form` on a requirement that uses an inner genitive, `model` shall print a relation reading and exit successfully.

### [g270] `model parse --form` reads "the K of every Y" inside the box of every Y
- [r270] When the person runs `model parse --form` on a requirement that uses a distributive genitive, `model` shall print a distributed reading and exit successfully.

### [g271] `model parse --form` binds "the K" to a referent outside a no, not, every or only box
- [r271] While a requirement uses a boxed noun phrase and the requirement uses a definite noun phrase that has an antecedent, when the person runs `model parse --form` on the requirement, `model` shall print an accessible reading and exit successfully.

### [g272] `model parse` refuses "the K" that only a referent inside a no, not, every or only box gives
- [r272] While a requirement uses a boxed noun phrase and the requirement uses a definite noun phrase that has no antecedent, if the person runs `model parse` on the requirement, then `model` shall refuse the command and name the definite noun phrase.

### [g273] `model parse` reads a response that sets an attribute to a value
- [r273] When the person runs `model parse` on a requirement that uses an assignment, `model` shall exit successfully.

### [g274] `model parse --form` reads setting an attribute as a change of its value
- [r274] When the person runs `model parse --form` on a requirement that uses an assignment, `model` shall print `initiates`.

### [g275] `model logic` finds no clash in a response that sets an attribute
- [r275] When the person runs `model logic` on a requirement that uses an assignment, `model` shall exit successfully.

### [g276] `model logic` reads every in a While clause
- [r276] While a requirement whose precondition uses a universal quantifier obliges an act and a requirement forbids the act, when the person runs `model logic`, `model` shall print `L1`.

### [g277] `model logic` reads a count in a While clause
- [r277] While a requirement whose precondition uses a count obliges an act and a requirement forbids the act, when the person runs `model logic`, `model` shall print `L1`.

### [g278] `model logic` reads a negated restriction on an object
- [r278] While a requirement that uses a negated modifier obliges an act and a requirement forbids the act, when the person runs `model logic`, `model` shall print `L1`.

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
