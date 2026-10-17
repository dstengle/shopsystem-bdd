# Capability files paired with feature files

Date: 2026-09-29 (stage 1; adopted by the plugin in 0.8.0); requirement ids 2026-10-16 (0.19.0, design model v3)
Scope: one context, on its own. Nothing here needs agreement with another
repo, a product level, or any tooling beyond markdown and Gherkin.

## What stage 1 is

Replace one design note with a set of capability files, and formulate one
feature file per capability. That's all. Relationships, requests, threads,
and the corpus come later, each when something asks for it.

What you get immediately: every behaviour sentence has a condition and an
observable response, so gaps show up while writing; and every sentence
maps to one scenario, so features stop drifting from the spec.

## Layout

```
spec/
  index.md              the context: purpose, constraints, composition, order of building, testing
  decisions.md          one entry per decision, addressed by heading
  capabilities/
    identity.md         one file per capability
    write-path.md
    ...
features/
  identity.feature      one per capability, same name
  write-path.feature
  ...
```

The pairing is by name, hyphenated on both sides. `capabilities/identity.md` is formulated as
`features/identity.feature`, the capability says so in its frontmatter,
and the feature says so in its header. Nothing else links them.

## The capability file

```markdown
---
id: capability/missingmass.io/shopsystem/shop-kb/identity
title: Identity
narrator: a client of the contract
rests_on: [design-decision/primary-model]
formulated_as: features/identity.feature
retired: []
---

# Identity

## Purpose
One paragraph: what this is, and what it isn't.

## Behaviour
EARS lines, each with its id: `- [r1] **When** ...`. This is the only section scenarios are formulated from.

## Implementation, may change
Mechanism. Non-binding. Nothing here gets a scenario.

## Not yet
Deferrals, each with the trigger that promotes it.
```

Every sentence in the file is one of four kinds, and the section it sits
in says which:

| kind | section | falsified by |
|---|---|---|
| decision | `decisions.md`, cited by `rests_on` | argument, or its `revisit_when` |
| requirement | Behaviour | a scenario |
| implementation | Implementation, may change | measurement |
| scope | Not yet | its trigger firing |

A sentence that is none of these — rationale, intent, a comparison to what
was rejected — is cut from the capability. If it matters, it goes in the
decision it explains.

## Writing the behaviour section

EARS, with two adaptations.

**The patterns.** Preconditions first, then at most one trigger, then the
response.

| keyword | pattern | use it for |
|---|---|---|
| *(none)* | ubiquitous | invariants that always hold |
| When | event-driven | a call, a command, an input |
| While | state-driven | something true for a period: stale, locked, unreachable |
| If | unwanted behaviour | refusals and faults |
| Where | optional feature | "where the schema declares…" — behaviour that depends on configuration |

**Adaptation 1: no "shall".** Present indicative, in the narrator's voice.
*When `Create` is called with a title, kb mints the id and returns it*,
not *the system shall mint*.

**Adaptation 2: the response is observable by the narrator.** A value
returned, a refusal and what it names, a file at a path. If you can't
write the response that way, the sentence is implementation and moves
down a section. This is the rule that keeps mechanism out of behaviour.
A refusal names its reason (*kb refuses the code because it has
expired*); the words of a message, a status code and a field name are
implementation.

Tables stay tables: a table of commands or rpcs is a row of implicit
When-lines and doesn't need rewriting. A list of properties (a canonical
format) stays a list.

## Requirement ids

Every Behaviour line carries an id, `[r<n>]`, written first: `- [r3] **If** ...`. The id is the line's
name for good: scenarios, proposals and commits point at it, and it survives re-wording.

- A new line takes the id one above every id the capability has used or retired, wherever it sits in the
  section. Ids are never renumbered, so they need not be in order.
- A changed line keeps its id. A line whose meaning is replaced by a different rule is a removal and an
  addition, not a change.
- A removed line's id goes into the frontmatter's `retired: [r<n>, ...]` and is never taken again.
- A requirement is named `capability/<context path>/<name>#r<n>`, `capability/<name>#r<n>` or `<name>#r<n>` inside its own context.

Ids are type-first, as in shopsystem-knowledge's IRIs: `<kind>/<context path>/<name>`. The context path is
the owner's domain, the product and the context name, such as `missingmass.io/shopsystem/shop-kb`. The
bounded context is `bounded-context/<context path>`, and it is `spec/index.md`'s `id`. A capability is
`capability/<context path>/<name>`, `<name>` being its file's name, and that is its `id`. A ledger entry's heading
is `## design-decision/<slug>`. A frontmatter `id` is always written in full.

A reference may be shorter. `<kind>/<name>` names a node of the same context, as `design-decision/primary-model`.
A field that fixes the kind (`rests_on`, `supersedes`, `argues`, `under`, `depends_on`) and the capability part
of a `#r<n>` reference may write the bare `<name>`. Any other field, `about:` for one, needs `<kind>/<name>`.
`<context name>/<name>`, `decision/<name>` and `obs/<name>` are not ids; `model check` reports them as
unresolved.

A requirement `capability/<context path>/<name>#r<n>` is short for the part `capability/<context path>/<name>#behaviour/r<n>`.
The IRI of an id is shopsystem-knowledge's base followed by the id.

`spec/index.md` begins with the context's id:

```markdown
---
id: bounded-context/missingmass.io/shopsystem/shop-kb
title: shop-kb
---

# shop-kb
```

## Glossary

A bounded context's terms are its ubiquitous language: the one word its lines and scenarios use for each
thing the narrator names. Each term is a bullet of `spec/index.md`'s `## Glossary`, in exactly this form:

```markdown
## Glossary

- **revision**: the count of writes an item has had, 1 when it is created. Not: version.
- **journal**: the record of every write to the store, oldest first. Not: history, log.
- **schema**: the declaration of an item type's fields.
```

`- **<term>**: <one-sentence definition>. Not: <word>, <word>.` The definition is one sentence. The `Not:`
part is optional: it lists the words the context avoids for that thing, and it is split from the definition
at `. Not:` only, so a definition may hold a period. A bullet in that section of any other form is a file
problem.

A term is standing, like a Behaviour line, and is approved at the gate like one. Its id is
`term/<context path>/<term>`, the term lowercased with spaces as hyphens (`term/missingmass.io/shopsystem/shop-kb/revision`);
inside its context, `term/<term>`. A term holds letters, digits and hyphens once lowercased; any other character in it is a file problem. Renaming a term is removing one entry and adding another. A glossary
change is shown at the gate with the lines it comes with, and the spec commit names each term added,
changed and removed. In a repository that keeps `work/`, a term change rides with the capability-proposal
that needs it, which lists the term in `adds`, `changes` or `removes` (`adds: [term/revision]`).

`model check` reads every Behaviour line and every scenario not held for the terms and the avoided words,
matched as whole words, whatever their case, with a plural "s" allowed. A scenario's mentions come from its title and its steps, not its Background, description, docstrings or tables: "restore" is no mention of "store".
It reports:

| rule | what it found |
|---|---|
| `v_t1` | a line or a scenario uses a word its context's glossary lists after `Not:`; the row names the line or scenario, the word and the term |
| `v_t2` | two glossary entries have one term |
| `v_t3` | a word one term lists after `Not:` is another term of the context, or the term itself |

A word used for two things, or two words used for one thing that no `Not:` lists yet, is a judgment of
meaning, not a word match: `checking-spec-consistency` finds it, on demand.

## The feature file

One feature per capability. One scenario per EARS line; a scenario
outline where the line has a Where and several configurations matter.
Each scenario is tagged `@r<n>` with the id of the line it formulates, on the scenario's tag line; the tag is
what binds them. The title is free; restating the line's condition is still a good title. A held scenario
(tagged `@holding`) keeps the tag it had and formulates no line.

```gherkin
# formulated from spec/capabilities/identity.md
Feature: Identity
  Narrator: a client of the contract
```

EARS to Gherkin:

| EARS | Gherkin |
|---|---|
| Where / While (precondition) | Given |
| When (trigger) | When |
| If (unwanted) | When, with the invalid input |
| response | Then |
| ubiquitous | a property scenario, or Background |

## Worked pair

From kb's design note, the identity section. Four of its lines and their
scenarios; the other four follow the same shape.

### `spec/capabilities/identity.md` — Behaviour

- [r1] **When** `Create` is called with a title, kb mints `id` as
  `<type>/<slug>` and returns it with `revision` 1.
- [r2] **When** a minted id collides with an existing one, kb appends `-2`,
  `-3`, and so on, and returns the id it chose.
- [r3] **If** content on `Create`, `Write`, or `Append` carries an identity
  key, `title` included, kb refuses the write with a violation naming the
  key.
- [r4] **Where** an item schema declares `title`, **when** an item is appended,
  kb mints its id from the title; otherwise from its position.

### `features/identity.feature`

```gherkin
# formulated from spec/capabilities/identity.md
Feature: Identity
  Narrator: a client of the contract

  @r1
  Scenario: Create with a title mints the id
    Given a store with a "decision" schema
    When Create is called with type "decision" and title "Use YAML"
    Then the response id is "decision/use-yaml"
    And the response revision is 1

  @r2
  Scenario: a colliding id gets a suffix
    Given a store holding "decision/use-yaml"
    When Create is called with type "decision" and title "Use YAML"
    Then the response id is "decision/use-yaml-2"

  @r3
  Scenario: content carrying an identity key is refused
    Given a store with a "decision" schema
    When Write is called on "decision/use-yaml" with content that carries "title"
    Then the write is refused
    And the violation names "title"

  @r4
  Scenario Outline: an item id is minted from title where the schema declares one
    Given a "process" schema whose step items <declare> a title
    When Append is called on "process/review#steps" with <item>
    Then the item id is <id>

    Examples:
      | declare | item                      | id      |
      | declare | title "Draft the note"    | draft-the-note |
      | omit    | no title                  | 0       |
```

## The decisions file

```markdown
# Decisions

## design-decision/primary-model
A graph whose serialization is documents: one file per artifact, parts
inline with ids, references as a schema primitive.
date: 2026-09-23
revisit_when: a request needs a traversal the reference index cannot serve
source: docs/superpowers/specs/2026-09-23-kb-design.md

## design-decision/delete-refuse-only
The only delete rule is `refuse`.
date: 2026-09-23
revisit_when: a request asks for cascade or detach
```

The file is a ledger. An entry is a heading id, one line, and property
lines: `date` always; `revisit_when`, `supersedes` and `source` (the note
or ADR it came from) when they apply. Properties are one per line, so the
ledger can later be rendered from a query over them. An entry is never
edited; a later entry names what it supersedes. Write `revisit_when` only where someone
will actually see the signal — in stage 1 that means a request or
something already measured; otherwise leave it out and put the reasoning
in the line itself.

## Checking

`scripts/model check` (this plugin; needs `python3 -m pip install clingo`) reads `spec/`, `features/` and
the ledger, and reports by rule name: a line with no id (`v15a`), two lines with one id (`v15b`), a retired
id taken again (`v15c`), a line with no scenario (`v_s3`), a scenario that names no line or two (`v_s1`,
`v_s2`), a word the glossary avoids, or a glossary at odds with itself (`v_t1`, `v_t2`, `v_t3`), and
references that name nothing. It exits 0 when everything holds. When the interpreter running it lacks
clingo, it looks for one that has it (`$SHOPSYSTEM_MODEL_PYTHON`, each `python3` on `PATH` outside the
active virtualenv's `bin/`, `/usr/local/bin/python3`, `/usr/bin/python3`) and runs again under the first it
finds. When none has it, it exits 2 with a message that names clingo, `pip install clingo` and each
interpreter it tried; the coverage check is then done by hand.

## Doing it

1. Read the note and list its capabilities: clusters of behaviour with one
   narrator. Ten give or take is normal for a component.
2. One file per capability. Move the note's sentences into the four
   sections; cut what fits none.
3. Rewrite Behaviour as EARS lines. Each line you can't give an observable
   response to moves to Implementation. Each condition the note never
   stated becomes either a line or a question — write the questions down.
   Number the lines `[r1]` on in each capability.
4. Write `spec/index.md`: frontmatter `id: bounded-context/<context path>`, the context path
   being `<owner domain>/<product>/<context name>` (ask the person when you do
   not know them) and `title`; then purpose, constraints carried,
   composition (the capabilities in reading order), order of building,
   testing, and the Glossary in the form above. Any table spanning capabilities is rendered from them, not
   authored.
5. Formulate one feature per capability, one scenario per line.
6. Keep the note as a dated proposal; from here the capability files are
   the spec. A later note is integrated into the same `spec/`: it never
   starts a second one.

## Not in stage 1

- Relationships between contexts, `@uses` tags, requests. Until the
  partnership with the neighbouring repo ends, cross-citation in feature
  files is fine.
- Capability groups (model / service / operations / guarantees). A column
  to add when the list gets long enough to need it.
- Beliefs. Rationale goes in the decision that carries it.
- Tooling beyond scripts/features and scripts/model. The pairing is a naming convention, a header comment and the @r<n> tags.
