# The domain model and its vocabulary

A bounded context's specification has four parts: the **domain model** (`spec/model/`), the **vocabulary**
(`spec/vocabulary/`), the **requirements** (`spec/capabilities/` and `spec/universal.md`) and the **design-decisions**
(`spec/decisions/`). Beside them sit the **adapter contracts** (`spec/adapters/`, [adapter contracts](adapters.md)).
This page is the reference of the first two. The example context
[`docs/examples/notes-cli/`](../examples/notes-cli/README.md) has one of each.

The model says what there is and what can be asked: objects, their attributes and lifecycles, relations, services
with their operations, events and actors. It holds **no rules**. Every rule (what an operation does, when it
refuses, what follows) is a requirement line, and `spec check` holds each line to what the model declares. The
vocabulary gives each element of the model its word, so a line can say it.

## `spec/model/<area>.md`

One file per area of the context (a core, supporting or generic subdomain):

````markdown
---
id: model/example.org/notes/notes-cli/notes-cli
area: notes-cli
kind: core
imports: []
---

# notes

## Purpose

The notes the person keeps, the tags they are filed under, and the notes service that answers the person's requests.

```model
object note
  attributes: title (text); status: kept | removed
  lifecycle status: kept → removed
  relations: under → tag (many)

object tag

service notes
  operation add(title, tag)  outcomes: done → the note | refused: no title
  operation list()  outcomes: returned → every note
  operation remove(note)  outcomes: done

actor the person kind of agent
```
````

- **Frontmatter:** `id: model/<context path>/<area>`, `area:` (the area's name, which a capability's `area:` names),
  `kind:` (`core`, `supporting` or `generic`) and `imports:` (the areas whose elements and words this one reads).
- **`## Purpose`** is a paragraph for people; nothing reads it.
- **One ` ```model ` block** holds the area's elements, in the syntax below. Two spaces indent a member; a line
  indented deeper continues the one before; `#` starts a comment.

### The syntax

```text
block      = { element } ;
element    = object | service | event | actor ;
object     = "object" name [ "kind of" name ] NL { "  " ( attrs | lifecycle | relations ) NL } ;
attrs      = "attributes:" attr { (";" | ",") attr } ;
attr       = name [ ":" values | "(" type ")" | "→" name ] ;
type       = "text" | "number" | "time" | "version" ;
values     = value { "|" value } ;                     (ordered: value { "<" value })
lifecycle  = "lifecycle" name ":" trans { ";" trans } ;
trans      = value "→" value ;
relations  = "relations:" rel { ";" rel } ;
rel        = phrase "→" name { "|" name } "(" card ")" ;
card       = "one" | "many" | "one, optional" ;
service    = "service" name NL { "  operation" op [ "by" actor { "," actor } ] [ "outcomes:" outcomes ] NL
                                 [ "    outcomes:" outcomes NL ] } ;
op         = name "(" [ param { "," param } ] ")" ;
param      = name [ ":" values | "(flag)" ] ;
outcomes   = outcome { "|" outcome } ;
outcome    = ( "done" | "returned" | "passed" | "failed" | "notifies" ) [ "→" phrase ]
           | "refused" [ ":" reason { "," reason } ] ;
event      = "event" phrase ":" "raised by" service "." operation ;
actor      = "actor" name [ "kind of" name ] ;
```

- **An object** is a thing of the domain. `kind of` places it under another object or a pack's kind (`object
  session kind of agent`).
- **An attribute** is text, a number, a time or a version (`title (text)`), one of a list of values (`status: kept
  | removed`; written `a < b < c`, the values are ordered as listed) or a reference to an object (`area → area`).
- **A lifecycle** names a status attribute and its allowed transitions. Its states are the attribute's values.
- **A relation** is a phrase, its target objects and a cardinality. `has → K` reads "the K of x" and "its K";
  `holds → K` reads "x holds a K"; a single preposition (`under → tag`) reads "a note under a tag"; any other phrase
  is a state verb's, named in the vocabulary.
- **A service** answers requests; **an operation** is what an actor may ask of it, with its parameters and the
  kinds of outcome it has. A parameter named as an attribute of the operation's object takes that attribute's
  values; one named as an object (`note`) is that object; `(flag)` is a boolean ("with the reminder", "without the
  reminder"); any other is text. `by` names the actors that may request it (any, when absent).
- **An outcome** is `done` (a change), `returned` (content), `passed` or `failed` (a check), `notifies` (an event
  told, unasked), or `refused` with its reasons, each a short business phrase. Every reason must be stated by a line
  (`v_m4`).
- **An event** is something that happened, raised by an operation; **an actor** is someone who makes requests.

### What `spec check` holds the model to

| code | what it catches |
|---|---|
| `v_m1` | a line's word names no element of the model (through the vocabulary of its capability's area) |
| `v_m2` | a request names a parameter its operation does not declare, or a value outside the parameter's values |
| `v_m3` | a requester the operation's `by` does not include |
| `v_m4` | a refusal reason no line states |
| `w_m5` | a lifecycle transition no line causes (a warning) |
| `v_m6` | a line sets a status by a transition the lifecycle does not allow |
| `v_m7` | an operation no line requests |
| `v_m8` | the model's own: a relation to an undeclared object, a transition over an undeclared value, two operations of one name in a service, an event raised by no operation |

`spec rules` prints every rule with its label; [`grammar/rules.md`](../../grammar/rules.md) has each with the
examples it fails and passes.

## `spec/vocabulary/<area>.md` and `shared.md`

One file per area, its frontmatter `id: vocabulary/<context path>/<area>` and `area:`, and `shared.md`, the words
every area reads (its actors, usually). Each entry names one element of the model after the arrow:

```markdown
- **note** (noun) → object note. One short text the person keeps, with a title.
- **status** (attribute) → attribute note.status. Whether a note is kept or removed.
- **removed** (adjective) → value note.status removed.
- **add** (verb, action) → operation notes.add. Forms: adds, added. Frame: <actor> adds <note>.
- **the notes service** (proper noun) → service notes. What answers the person's requests about notes.
- **the person** (proper noun) → actor the person. The human at the terminal.
```

- **The part of speech** in brackets: `noun`, `proper noun`, `adjective`, `attribute`, `verb, action` (something
  that happens) or `verb, state` (something that holds, which can stand in a While clause).
- **The element** after `→`: `object <name>`, `attribute <object>.<attribute>`, `value <object>.<attribute>
  <value>`, `relation <object>.<phrase>`, `operation <service>.<operation>`, `service <name>` or `actor <name>`.
- **A value** is an adjective or a noun. An adjective may be said the short way ("a note is `removed`"); a noun only
  the full way ("the status of the item is `idea`").
- **`Frame:`** is thin: the word order and the prepositions, its slots in angle brackets. `<actor>` is any agent;
  `<from>` and `<to>` are a relation's ends; `<note>` is the object or parameter of that name. A verb with no frame
  reads `<actor> <verb> <object>` for an operation and `<from> <verb> <to>` for a relation. An operation's parameters
  need no frame: a line says them after its object, "with a title", "with the title `x`", "without a title", "with
  the reminder" (a flag).
- **`Forms:`**, **`Plural:`**, **`Not:`**, **`This:`** and **`Redefines:`** are read as before; a definition sentence
  stays prose. `Values:`, `Transitions:`, `Kind of:`, `Order:` and `Type:` are the model's now.

An area reads its own layer, the layers of the areas its model file imports, then `shared`. A word may name two
elements in two areas (this repository's "finding" of a check and of an analysis); a line uses the one its area
reads.

| code | what it catches |
|---|---|
| `v_t18` | an entry names no element (no `→`) |
| `v_t19` | an entry names an element the model does not declare |
| `v_t20` | two entries of one layer name one element, and neither is a form of the other |
| `v_t21` | `spec/index.md` imports the retired CLI pack: import `request` and run `migrate upgrade` |

## The request pack

Every context with a model imports [`grammar/packs/request.md`](../../grammar/packs/request.md) (`imports:
[request]`): the words of a request and its response that no model declares, *request*, *parameter*, *service*,
*reason*, *response*, *check*, and the acts *refuse*, *name*, *return*, *notify*, *complete*, *fail*, *keep*,
*change*, *conform* and *start*. "The request" is the request the trigger makes; "the check" is a request whose
outcomes are passed or failed. In the example's context:

<!-- docs: context docs/examples/notes-cli -->
```requirement
If the person adds a note without a title, then the notes service shall refuse the request and name the title.
```

A request of `notes.add` with no `title`, refused, the title named. Which command and option that request is, and
how its refusal shows (exit 1, the reason on stderr), is the [CLI adapter's](adapters.md).
