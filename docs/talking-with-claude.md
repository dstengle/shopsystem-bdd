# Talking with Claude

This page is for the person who talks with Claude: you say what you want in your own words, and Claude does the
rest. It covers what to say, what happens next, and the few things you're asked to do. You don't need to run the
plugin's tools: the session works out what to run.

## What you say, and what follows

| you say | the skill that takes it | you're asked to |
|---|---|---|
| "Set up this repository for the plugin." | [shaping-items](../skills/shaping-items/SKILL.md) | give the context's id, and a GitHub repository |
| "I want an app that keeps my notes." | [shaping-items](../skills/shaping-items/SKILL.md), then [building-a-batch](../skills/building-a-batch/SKILL.md) | answer a question or two, merge the pull request |
| "I'd like `shop work show` to print the status too." | [shaping-items](../skills/shaping-items/SKILL.md), then [building-a-batch](../skills/building-a-batch/SKILL.md) | merge the pull request |
| "It's for a writer, who wants to note a thought down and find it later." | [shaping-items](../skills/shaping-items/SKILL.md) ([your product and its jobs](#your-product-and-its-jobs)) | say who it's for and what they want done |
| "Build what's ready." | [building-a-batch](../skills/building-a-batch/SKILL.md) | merge the pull request |
| "Check your requests." | [taking-in-a-request](../skills/taking-in-a-request/SKILL.md) | accept a request |
| "Ask the payments context for refunds." | [raising-a-request](../skills/raising-a-request/SKILL.md) | read the proposed lines |
| "What did that batch cost?" | [analyzing-a-batch](../skills/analyzing-a-batch/SKILL.md) | nothing |

A skill is the set of instructions Claude follows for one kind of work. The links show exactly what Claude is told.

Take the third row. You say you'd like `shop work show` to print an item's status. Claude makes an item (a piece of work
in the backlog) and writes what you asked for as a requirement line, one sentence the plugin can parse:

```requirement
When the person shows an item, the backlog service shall return the status of the item.
```

Claude checks the line, readies the item and builds it in a batch. The next thing you see is a pull request,
reviewed and ready to merge. [The tour](tour.md) follows this exact feature from start to finish.

## Each skill, in plain words

**Shaping items.** You describe behaviour you want. Claude turns it into an item with requirement lines and checks
them against the readiness bar: every line parses to one meaning, the logic check finds no clash, and the lines
generate scenarios. Then it readies the item. If you're mid-brainstorm, the conversation ends in items with lines,
not a long design document.

**Building a batch.** A batch builds several ready items together, like a sprint, on one branch. Claude hands the
batch to one fresh agent, the driver, which builds each item in parallel and opens one pull request. The pull
request is reviewed and fixed before you see it. You read it and merge it; Claude then marks the items delivered,
measures the batch and starts the next one if anything else is ready.

**Taking in a request.** Another context (another team's repository, or the product) asks this one for something,
on a GitHub issue. Claude offers what it already has, then judges each line the asker proposes: accept it into a
capability, refuse it with a reason, or propose a better wording. Claude never accepts a request on its own. When
the lines are settled it tells you, and the request waits for your word.

**Raising a request.** It's the other way round: you want something of another context. Claude opens a request on
that context's repository in your words, waits for its offer, then writes lines in *its* vocabulary, not ours. It
shows you each line beside your English, with what it means. The lines are yours to change.

**Analyzing a batch.** After a batch closes, Claude reads its measurement (wall time, tokens and cost by role,
review findings, defects) and compares it with the batch before. It writes a short report with at most three things
to try, each with the figure that would show it worked. You don't need to do anything with it.

## What Claude won't ask you

**To approve the lines.** The readiness bar is the check, and it's stricter than a skim: a line that could mean two
things, or that clashes with another line, is refused before anyone builds it. Claude tells you afterwards which
items are ready and what their lines say. You can read them in the backlog (`shop work show b<n>`) and again in the pull
request, and change them there.

**To start a batch.** Readying an item is the decision to build it. When an item is `ready` and no batch is open,
Claude starts one. Nothing waits on you between the start of a batch and its reviewed pull request.

What it will ask: to merge a pull request, to accept a request, and to upgrade the repository when the plugin is
newer (see below). Those are yours.

## Your product and its jobs

A bounded context is built for a product: the people it serves and the jobs they want done. You say that in your own
words, once, and whenever it changes. Claude keeps it in the shop's product file, `.shop/product/product.toml`, and
from then on can tell you which requirements do each job. This section walks it through on the notes tool, as
[`docs/examples/notes-cli/`](examples/notes-cli/README.md) keeps it. That folder is where these steps **end**: its
product file and the `serves:` lines of its capability are what they write. To replay them from their start, copy the
folder into a git repository of its own, take out `.shop/product/`, every `serves:` line and the group g5 of
`spec/capabilities/notes.md`, run `shop spec annotate` and `shop features generate`, and commit. Every output below is
pasted from a real run on such a copy (plugin 0.44.0, 2026-11-26).

### What you say: who it's for and what they want done

```text
The notes tool is for a writer. When a thought comes up, they want to note it down so they can find it later.
When they sit down to write, they want to see every note they kept. And they clear out the notes they're done with.
```

Claude names the product and its one actor, then writes each thing the writer wants done as a **job**, its statement
in the one form `When <situation>, <actor> wants <motivation>, so they can <outcome>.`. Finding notes and clearing
them out make no sense before notes are kept, so those two jobs **need** `keep-notes`:

```console
$ shop spec product example.org/notes --purpose "Keep a writer's passing thoughts at hand."
declared the product example.org/notes
$ shop spec actor "the writer"
declared the product actor the writer
$ shop spec job keep-notes --actor "the writer" --statement "When a thought comes up, the writer wants to note it down, so they can find it later."
declared the job keep-notes
$ shop spec job find-notes --actor "the writer" --statement "When the writer sits down to write, the writer wants to see every note they kept, so they can pick one up." --needs keep-notes
declared the job find-notes
$ shop spec job clear-notes --actor "the writer" --statement "When a note is done with, the writer wants to remove it, so they can keep the list short." --needs keep-notes
declared the job clear-notes
```

Then the product's domain map: one core subdomain for the three jobs (each job given with its own `--serves`), this
bounded context addressing it under the id `shop migrate init` gave it, each job assigned to it, and the writer
mapped to the actor this context's model already calls "the person":

```console
$ shop spec subdomain note-keeping --type core --serves keep-notes --serves find-notes --serves clear-notes
declared the subdomain note-keeping
$ shop spec context bounded-context/example.org/notes/notes-cli --addresses note-keeping --shop example.org/notes/shop
declared the bounded context bounded-context/example.org/notes/notes-cli kept by example.org/notes/shop
$ shop spec assign keep-notes --to bounded-context/example.org/notes/notes-cli
assigned the job keep-notes to the bounded context bounded-context/example.org/notes/notes-cli
$ shop spec assign find-notes --to bounded-context/example.org/notes/notes-cli
assigned the job find-notes to the bounded context bounded-context/example.org/notes/notes-cli
$ shop spec assign clear-notes --to bounded-context/example.org/notes/notes-cli
assigned the job clear-notes to the bounded context bounded-context/example.org/notes/notes-cli
$ shop spec plays "the writer" --in bounded-context/example.org/notes/notes-cli --as "the person"
mapped the product actor the writer to the person in the bounded context bounded-context/example.org/notes/notes-cli
```

Each command is one commit of the product file. If what you said leaves a gap (a job's situation, say, or who does
it), Claude asks before it declares the job.

A few things the session takes care of, which you may meet if you run the steps yourself:

- **The ids have fixed forms.** The product's id is a dotted domain and a path (`example.org/notes`); a bounded
  context's is `bounded-context/<domain>/<path>`, exactly as `shop migrate init` was given it. Any other form is
  refused.
- **`spec plays` needs the actor in the domain model.** The notes context's model has "the person" already. In a new
  context the actor arrives with the first batch, so the mapping waits until that batch is merged; until then the
  command is refused, saying the model holds no such actor.
- **Nothing is edited by hand.** A declaration made wrongly is taken back with `shop spec unassign` or
  `shop spec drop job`, `drop actor`, `drop subdomain` or `drop context`, each refused while something still refers to
  what it drops; then it is declared again.

### What you see: what nothing does yet

Claude runs the check and tells you what it says. With the product declared and no group dedicated to a job, every
job is unserved:

```console
$ shop spec check
warning w_unreached_sub  a subdomain of a job held here whose trace reaches no bounded context that addresses it  (3)
    clear-notes, note-keeping
    find-notes, note-keeping
    keep-notes, note-keeping
warning w_unserved_cap  a capability serves no job  (1)
    capability/example.org/notes/notes-cli/notes
warning w_unserved_job  a job nothing serves  (3)
    job/example.org/notes/notes-cli/clear-notes
    job/example.org/notes/notes-cli/find-notes
    job/example.org/notes/notes-cli/keep-notes
warning w_untriggered_actor  a product actor of a job held here whose actor here triggers no line of the job's trace  (3)
    clear-notes, the writer
    find-notes, the writer
    keep-notes, the writer
0 violations, 10 warnings, 0 unresolved references, 0 file problems
```

These are warnings, not errors: they say what is still to do, and they all go once each job has the groups that do
it.

### What Claude does: each group to the job it does

Claude dedicates each existing group to its job on an item, by the group's id. If you add behaviour at the same time,
the new line's group gets its job too:

```text
And a note that's already removed can't be removed again.
```

<!-- docs: context docs/examples/notes-cli -->
```console
$ shop work idea "The notes serve the writer's jobs"
b1 "The notes serve the writer's jobs" idea
$ shop work shape b1 --note "Dedicate each group of notes to the job it does, and refuse removing a removed note."
b1 "The notes serve the writer's jobs" shaped
$ shop work line b1 --serves notes#g1 keep-notes
b1 "The notes serve the writer's jobs": notes#g1 serves keep-notes
$ shop work line b1 --serves notes#g2 keep-notes
b1 "The notes serve the writer's jobs": notes#g2 serves keep-notes
$ shop work line b1 --serves notes#g3 find-notes
b1 "The notes serve the writer's jobs": notes#g3 serves find-notes
$ shop work line b1 --serves notes#g4 clear-notes
b1 "The notes serve the writer's jobs": notes#g4 serves clear-notes
$ shop work line b1 --into notes --group "A removed note is not removed again" 'If the person removes a note whose status is `removed`, then the notes service shall refuse the request.' --serves clear-notes
b1 "The notes serve the writer's jobs": notes#r5 If the person removes a note whose status is `removed`, then the notes service shall refuse the request.
b1 "The notes serve the writer's jobs": notes#g5 serves clear-notes
```

`shop work ready` takes a shaped item, never an idea, so the idea is shaped first: `shop work shape` gives it its
shaping note, the sentence that says what the item is to do. Without `--note` it is refused, naming the option
(`has no shaping note; give it one with the --note option`).

`--serves <job>` goes with the line it dedicates: after the line's text, as here, or before it. A job the product does
not hold is refused, so a typo in a job's id can't slip through:

<!-- docs: context docs/examples/notes-cli -->
```console
$ shop work line b1 --serves notes#g1 write-notes
work line: --serves: the product holds no job write-notes
```

An item whose only lines are `--serves` pairs is ready too: the pairs alone would pass the readiness bar. Here the
item also holds r5, the behaviour you added.

### What you see: the trace, before the batch

The pairs are on the item, not yet in `spec/`, so a plain `shop spec trace` says nothing serves the job and points at
the item. With `--item`, the session reads the trace with the item applied to a copy, and checks it the same way;
nothing in `spec/` changes:

<!-- docs: context docs/examples/notes-cli -->
```console
$ shop spec trace keep-notes
spec: job keep-notes is served by no requirement group; the item b1 holds one that serves it: trace it with --item b1
$ shop spec check --item b1
0 violations, 0 warnings, 0 unresolved references, 0 file problems
$ shop spec trace clear-notes --item b1
the trace of the job clear-notes:
  notes#r4 (served by notes#g4): When the person removes a note, the notes service shall set the status of the note to `removed`.
  notes#r5 (served by notes#g5): If the person removes a note whose status is `removed`, then the notes service shall refuse the request.
  notes#r1 (needed job keep-notes: served by notes#g1): When the person adds a note with a title and a tag, the notes service shall keep the note under the tag.
  notes#r2 (needed job keep-notes: served by notes#g2): If the person adds a note without a title, then the notes service shall refuse the request and name the title.
```

Ten warnings down to none: every job is served, every actor's job is triggered by a line, and the capability does a
job. A job's trace holds the lines of the groups that serve it, then those of each job it needs, each with why it's
there.

### The outcome: each job traced to its requirements

Claude readies the item and starts its batch, and you merge its pull request as for any other item:

```console
$ shop work ready b1
b1 "The notes serve the writer's jobs" ready
$ shop work batch start
batch-1 building: t1 b1 "The notes serve the writer's jobs"
batch brief: .../.shop/worktrees/batch-1-driver/brief.md
```

The batch writes each pair as its group's `serves:` line in the capability file, and r5 with its scenario:

<!-- docs: context docs/examples/notes-cli -->
```markdown
### [g4] Removing a note sets its status to removed
serves: clear-notes
- [r4] When the person removes a note, the notes service shall set the status of the note to `removed`.

### [g5] A removed note is not removed again
serves: clear-notes
- [r5] If the person removes a note whose status is `removed`, then the notes service shall refuse the request.
```

Once it's merged, ask "what does finding notes rest on?" and the session answers from the trace, with no `--item`.
On the example as it's kept:

<!-- docs: context docs/examples/notes-cli -->
```console
$ shop spec --root docs/examples/notes-cli trace keep-notes
the trace of the job keep-notes:
  notes#r1 (served by notes#g1): When the person adds a note with a title and a tag, the notes service shall keep the note under the tag.
  notes#r2 (served by notes#g2): If the person adds a note without a title, then the notes service shall refuse the request and name the title.
$ shop spec --root docs/examples/notes-cli trace find-notes
the trace of the job find-notes:
  notes#r3 (served by notes#g3): When the person lists the notes, the notes service shall return every note.
  notes#r1 (needed job keep-notes: served by notes#g1): When the person adds a note with a title and a tag, the notes service shall keep the note under the tag.
  notes#r2 (needed job keep-notes: served by notes#g2): If the person adds a note without a title, then the notes service shall refuse the request and name the title.
```

The trace is never written down: it is derived from the `serves:` lines and the jobs' needs each time, so it can't
drift from the spec. When a line changes or a group's job does, the next trace says so.
[Concepts](concepts.md#product-job-and-trace) has the product's words, and
[the commands](reference/commands.md#shop-spec-product) every option.

## What you see when a session starts

Three hooks run as a session starts. Each prints nothing when there's nothing to say.

**A pending upgrade.** `shop migrate status --hook` speaks only when the repository is behind the plugin:

```text
This repository is on plugin version 0.37.0 and the plugin is on 0.38.0. Offer the person the upgrade from 0.37.0 to 0.38.0, which applies:
  0.38.0 "the domain contract": scaffold the domain model, the vocabulary and the CLI contract from the glossary, the relations and the commands the lines run, import the request pack, and name by file and id each line a session rewords in the request's words
Run `migrate upgrade` (python3 .../scripts/migrate upgrade) only on the person's yes.
```

Claude offers the upgrade and runs it only when you say yes. [Upgrading](upgrading.md) walks through it.

**The names table.** Every item and batch with its name, so Claude says `b7 "Close the generator gaps in
spec_steps"`, never a bare `b7`:

```text
The names of this repository's items and batches: tell the person each by its name beside its id (b3 "Fix the parser"), never by its id alone.
| id | name | status |
|---|---|---|
| b1 | Requests between repositories over GitHub issues | withdrawn |
| b2 | Request lines into an upstream in the downstream's own terms | idea |
...
```

**Requests waiting on the other side.** One line for each, and a note telling Claude to watch for the answer:

```text
q15 awaiting-upstream: Refunds for a cancelled order (https://github.com/ex/payments/issues/7)
A request waits on the other side: start `work watch --forward` with the Monitor tool, and run `work sync` when it wakes.
```

Claude then watches the issue and picks the conversation up as soon as the other side posts.

## Why your words are kept

When an item rests on something you said, Claude keeps your exact words with `shop work quote`. A quote is a small file
under `.shop/quotes/` with your message and the turns around it, committed with everything else. Months later,
anyone can see why an item exists, in your words rather than a summary of them.

```console
$ shop work quote "I trust you to make some delightful docs."
quote-24 "I trust you to make some delightful docs."
$ shop work show quote-20
quote-20 "Once 4.0 is done, take a new backlog item to make some nice …"
  session: 72e23fa5-6dee-49f3-a1d1-7e79096a0501
  date: 2026-11-10
...
the person, 2026-11-10T04:19:13.250000+00:00, cited:
I'm going offline. Please take care of pull requests and getting to 4.0.

Once 4.0 is done, take a new backlog item to make some nice user documentation for the plugin and then get to work on the backlog item. I trust you to make some delightful docs.
```

That's the quote these docs were written from.

## The three agents

- [`pr-reviewer`](../agents/pr-reviewer.md) reviews a batch's pull request once, adversarially, and fresh each time;
  what it finds is fixed before the pull request reaches you.
- [`architecture-reviewer`](../agents/architecture-reviewer.md) checks the code's shape against the repository's
  `CLAUDE.md`, and runs only when you ask for one.
- [`trial-runner`](../agents/trial-runner.md) runs one trial of a plugin command on a real repository or a fixture
  and records what it measured.

## Redirecting, or saying "stop"

You can redirect Claude any time in plain words. Inside a batch there's a better channel too. When a task can't go
on without an answer, its item is parked with the question and leaves the batch as `needs-input`; the rest of the
batch carries on. `shop work backlog` lists it under its own heading:

```console
$ shop work backlog
...
## needs-input (1)

| rank | item | title | provenance | value | urgency | size | score | waiting on |
|---|---|---|---|---|---|---|---|---|
| 1 | b7 | Close the generator gaps in spec_steps | own | high-value | medium-urgency | large | 1.67 | question: The item's lines fail the suite as applied, before any code: ... How are the gloss and r20 reworded? ... |
```

Tell Claude your answer, or record it yourself. The item goes back to `shaped`, the question and its answer kept on
it, and it's shaped and readied again:

```console
$ shop work answer b7 "Reword the gloss as one sentence and give g20 its own trigger; retire readiness#r12; yes, change the three asserts."
b7 "Close the generator gaps in spec_steps" shaped
```

To stop work you don't want, say so: Claude withdraws an item (`shop work withdraw`) or abandons a batch
(`shop work batch abandon`). [Recipes](recipes.md) has the steps.

Next: [the tour](tour.md) · [recipes](recipes.md) · [concepts](concepts.md)
