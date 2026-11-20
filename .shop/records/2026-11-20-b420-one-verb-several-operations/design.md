# b420: one verb naming several operations, told apart by its frames

Design, 2026-11-20, settled with the person in the session d0999860 (quote-63). Grounded in `main` at `c3f18b9a0`
(plugin 0.41.0). A small change by size; written short.

## Intent

UX trial 2 (0.40.0): the person asked to "list all my checklists" after "list" already named `checklists.list` (the
items of one checklist). The session coined the verb `browse`, and the CLI got a `browse` command the person never
said. The person's word should be kept.

The person (quote-63): "list the checklists vs list a checklist makes sense because a checklist is a container of
things ... you would not list a note ... but you could possibly list the characters in a note." Listing takes a
container: the service's collection ("the checklists"), one container ("a checklist"), or a collection a frame's
fixed words name ("the characters of a note").

## What works today and what does not

Tried on a copy of docs/examples/notes-cli: two vocabulary entries of one word naming two operations pass `spec
check`, each read by its frame. `Frame: <actor> lists the characters of <note>` and `Frame: <actor> lists the notes`
each read one way. The trial's pair does not: with `Frame: <actor> lists <checklist>` beside `Frame: <actor> lists
the checklists`, "the person lists the checklists" reads two ways (the fixed words, or "the checklists" a plural
object of the first frame), and the refusal says `"" reads 2 ways`, naming no words.

## Goals, non-goals

- Goal: "list a checklist" and "list the checklists" are two requests of one verb, each line one reading.
- Goal: a line that does read two ways is refused naming the words and both readings.
- Goal: a session keeps the person's word and gives it a second frame, never coining a verb.
- Non-goal: the notes-cli example app grows (the docs get a recipe, not new operations in the example).
- Non-goal: a request on several objects at once.

## Approaches

1. **A request's object is one thing (chosen).** The object slot of a request (a verb naming an operation) takes one
   thing: a plural ("the checklists", "every checklist", "two checklists") is no argument there. One request acts on
   one container; "the checklists" is only the fixed words of the operation on the service's collection. No
   tie-break; the ambiguity is not generated.
2. The exact fixed words win over a reading through an object slot: a tie-break in spec_meaning, smaller, but a
   special case that leaves other collisions.
3. Guidance only: the line stays refused.

## The design

- **Grammar.** spec_rgl_ops' request funs take the object slot as one thing's noun phrase, no plural or quantified
  one. Other frames (a verb naming no operation, a state, a response's act) are unchanged. A design-decision states
  it.
- **The refusal.** spec_meaning's `split` of two meanings names the words that read two ways and, when the two
  trees are two frames of one verb, both frames (and their operations); never an empty quote.
- **The skill.** shaping-items: a word the person uses again for another operation keeps the word and gets a
  frame that tells it apart ("list a checklist", "list the checklists", "list the characters of a note"); never a
  coined verb.
- **The docs.** A recipe in docs/recipes.md, "One verb for several operations": the vocabulary entries of the
  checklist pair and of "list the characters of a note" and "show the length of a note", their lines parsed with
  `spec parse` in a sketch context, as the docs test reads every line on the page.

## Left to the builder

- Whether a live line of this repository or the docs uses a plural object of a request; if one does, the session
  names it and its rewording.
- Where the one-thing restriction lives in the generated grammar (a request's own argument category or a check in
  spec_meaning) as long as the plural is no reading, not a refused one.
