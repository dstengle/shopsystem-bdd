# Stage 1: capability files paired with feature files

Date: 2026-09-29
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
  write_path.feature
  ...
```

The pairing is by name. `capabilities/identity.md` is formulated as
`features/identity.feature`, the capability says so in its frontmatter,
and the feature says so in its header. Nothing else links them.

## The capability file

```markdown
---
id: capability/identity
title: Identity
narrator: a client of the contract
rests_on: [decision/primary-model]
formulated_as: features/identity.feature
---

# Identity

## Purpose
One paragraph: what this is, and what it isn't.

## Behaviour
EARS lines. This is the only section scenarios are formulated from.

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

Tables stay tables: a table of commands or rpcs is a row of implicit
When-lines and doesn't need rewriting. A list of properties (a canonical
format) stays a list.

## The feature file

One feature per capability. One scenario per EARS line; a scenario
outline where the line has a Where and several configurations matter.
The scenario title restates the line's condition, so a reader can find
the line from the scenario and the scenario from the line.

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

- **When** `Create` is called with a title, kb mints `id` as
  `<type>/<slug>` and returns it with `revision` 1.
- **When** a minted id collides with an existing one, kb appends `-2`,
  `-3`, and so on, and returns the id it chose.
- **If** content on `Create`, `Write`, or `Append` carries an identity
  key, `title` included, kb refuses the write with a violation naming the
  key.
- **Where** an item schema declares `title`, **when** an item is appended,
  kb mints its id from the title; otherwise from its position.

### `features/identity.feature`

```gherkin
# formulated from spec/capabilities/identity.md
Feature: Identity
  Narrator: a client of the contract

  Scenario: Create with a title mints the id
    Given a store with a "decision" schema
    When Create is called with type "decision" and title "Use YAML"
    Then the response id is "decision/use-yaml"
    And the response revision is 1

  Scenario: a colliding id gets a suffix
    Given a store holding "decision/use-yaml"
    When Create is called with type "decision" and title "Use YAML"
    Then the response id is "decision/use-yaml-2"

  Scenario: content carrying an identity key is refused
    Given a store with a "decision" schema
    When Write is called on "decision/use-yaml" with content that carries "title"
    Then the write is refused
    And the violation names "title"

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

## decision/primary-model
A graph whose serialization is documents: one file per artifact, parts
inline with ids, references as a schema primitive.
revisit_when: a request needs a traversal the reference index cannot serve

## decision/delete-refuse-only
The only delete rule is `refuse`.
revisit_when: a request asks for cascade or detach
```

An entry is one line and a `revisit_when`. It is never edited; a later
entry names what it supersedes. Write `revisit_when` only where someone
will actually see the signal — in stage 1 that means a request or
something already measured; otherwise leave it out and put the reasoning
in the line itself.

## Doing it

1. Read the note and list its capabilities: clusters of behaviour with one
   narrator. Ten give or take is normal for a component.
2. One file per capability. Move the note's sentences into the four
   sections; cut what fits none.
3. Rewrite Behaviour as EARS lines. Each line you can't give an observable
   response to moves to Implementation. Each condition the note never
   stated becomes either a line or a question — write the questions down.
4. Write `spec/index.md`: purpose, constraints carried, composition (the
   capabilities in reading order), order of building, testing. Any table
   spanning capabilities is rendered from them, not authored.
5. Formulate one feature per capability, one scenario per line.
6. Keep the note as a dated proposal; from here the capability files are
   the spec.

## Not in stage 1

- Relationships between contexts, `@uses` tags, requests. Until the
  partnership with the neighbouring repo ends, cross-citation in feature
  files is fine.
- Capability groups (model / service / operations / guarantees). A column
  to add when the list gets long enough to need it.
- Beliefs. Rationale goes in the decision that carries it.
- Any tooling. The pairing is a naming convention and a header comment.
