# b418: a request parameter whose value is another thing's value (a value in use)

Design, 2026-11-20, settled with the person in the session d0999860 (quote-60, quote-61, quote-62). Grounded in
`main` at `153ab65cd` (plugin 0.41.0). A small change by size; written short.

## Intent

A first application nearly always has a rule that a name is unique: "no two checklists with one title". UX trial 2
(0.40.0) could only say it with example data ("While the title of a checklist is `groceries`, if the person creates
a checklist with the title `groceries`, ..."), which `spec check` warns of (`w_example`) and whose scenario checks one
value. Every natural wording was refused, because "the title" in a request is the request's parameter and a
parameter's value can only be a code, a listed value or a thing.

## Goals, non-goals, anti-goals

- Goal: a line says that a request whose parameter has the value another thing already has is refused, in words a
  person would use, and its scenario tests the service's business logic.
- Goal (the person: "Build around the abstract general case", quote-60): the work is built on the general meaning,
  a parameter's value as a referent with conditions on it; the first wording is one way into it.
- Non-goal: the second wording, a condition on the parameter itself ("with a title and another checklist has the
  title"); b427, which rests on this core.
- Non-goal: comparisons other than the same value ("a due date after the due date of ...").
- Anti-goal (quote-61): a scenario that reads the store as a collection and compares two things in the test. The
  scenario sets the service's state up, makes one request and checks its response; an implementation that exposes
  its whole store to pass it is not what the test asks for.

## Approaches

1. **The general core, the first wording on it (chosen).** A parameter's value is a referent; "with the T of <np>"
   gives `param(e, T, v)` with `T(x) = v`. Every later wording translates to the same meaning, so lines written now
   keep their meaning and the checks, entailment and steps built now serve the later wording unchanged.
2. A special atom for the one phrase (`param_from(e, T, x)`): quicker now, but the second wording would need a
   second translation and `spec logic` would have to learn the two are one. Rejected.
3. Keep example data and document it, silencing `w_example` for the pattern: the cheapest, but the rule stays one
   example. Rejected.

## The design

### The meaning (design-decision)

A request parameter's value is a referent of the logical form. Each wording of it translates to that referent and
conditions on it: a code, a listed value, a thing, and now another thing's value of the attribute the parameter
names. "If the person creates a checklist with the title of another checklist" reads:

```
if [x3: checklist, x1: checklist, v: title value]
  request(e1, checklists.create, subject: person, object: x3)
  param(e1, title, v)
  title(x1) = v
  distinct(x1, x3)
```

`another` is b240's (`distinct`), "the T of x" spec_lf_np's attribute image.

### The wording

In a request's parameters (spec_rgl_ops' Params), a parameter that names an attribute T (domain_model's parameter
type) takes, beside a code and a listed value, "the T of <noun phrase>" of a kind that has T. A new construct in
the construct catalogue (`param-of`, its example the line above), a section in `grammar/language.md`, a recipe in
the docs ("a value already in use").

### The checks

spec_lf_facts_request gives the parameter's value as the check's term of the value of x1's attribute, so that two
triggers are one request when their operation and parameter values unify: "with the title `groceries`" and "with
the title of a checklist whose title is `groceries`" meet in `spec logic`, and their clashes are found. The
entailment check reads the same facts.

### The scenario

```gherkin
@g5 @r5
Scenario: A checklist created with the title of another checklist is refused
  Given a checklist c1
  And the title of the checklist c1 is `t1`
  When the person creates a checklist c2 with the title `t1`
  Then the checklists service refuses this request
  And the checklists service names the title
```

- The Givens are the service's state, built through the core's own operations; the When is one request with the
  concrete value, made up as b413 makes a text value up; the Thens read only its response. Nothing reads a
  collection.
- **The created object in the When (folded in).** An operation whose object is only its `done →` outcome, no
  parameter, makes its object: its object is introduced in the When ("creates a checklist c2"), never by a Given,
  which a binding could take as c2 put in the store first (here, a clash of its own). An operation whose object is a
  parameter (`remove(note)`, `rename(note, title)`) or a `returned →` outcome keeps its Given, as today. The
  existing features of creating operations change once (notes' r1 and r2: "When the person adds a note n1 with a
  title and the tag t1"); the release notes say so.
- The scenarios capability's lines that say a step mentions no instance "that no given step introduces" (r14, r26,
  r27, r33, r34, r35) are retired and restated with "no given step and no when step"; a new line says the created
  object is introduced in the When.

## Left to the builder

- The fun names and where the Params value slot's new branch lives in spec_rgl_ops.
- The check's term of a parameter's value from a thing's attribute, and its unification with a code.
- How spec_steps4_request picks the made-up value and puts it on both the Given and the When.

## Related

- b426: a core driver, so that the scenarios reach the service's operations in process, not through the CLI
  adapter (quote-62); b418's scenarios need nothing of it.
- b427: the second wording, a condition on a request's parameter, on this core.
