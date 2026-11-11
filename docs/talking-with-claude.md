# Talking with Claude

This page is for the person who talks with Claude: you say what you want in your own words, and Claude does the
rest. It covers what to say, what happens next, and the few things you're asked to do. You'll rarely type a command.

## What you say, and what follows

| you say | the skill that takes it | you're asked to |
|---|---|---|
| "I'd like `work show` to print the status too." | [shaping-items](../skills/shaping-items/SKILL.md), then [building-a-batch](../skills/building-a-batch/SKILL.md) | merge the pull request |
| "Build what's ready." | [building-a-batch](../skills/building-a-batch/SKILL.md) | merge the pull request |
| "Check your requests." | [taking-in-a-request](../skills/taking-in-a-request/SKILL.md) | accept a request |
| "Ask the payments context for refunds." | [raising-a-request](../skills/raising-a-request/SKILL.md) | read the proposed lines |
| "What did that batch cost?" | [analyzing-a-batch](../skills/analyzing-a-batch/SKILL.md) | nothing |

A skill is the set of instructions Claude follows for one kind of work. The links show exactly what Claude is told.

Take the first row. You say you'd like `work show` to print an item's status. Claude makes an item (a piece of work
in the backlog) and writes what you asked for as a requirement line, one sentence the plugin can parse:

```requirement
When the person runs `work show` on an item, `work` shall print the status of the item.
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
that context's repository in your words, waits for its offer, then writes lines in *its* glossary, not ours. It
shows you each line beside your English, with what it means. The lines are yours to change.

**Analyzing a batch.** After a batch closes, Claude reads its measurement (wall time, tokens and cost by role,
review findings, defects) and compares it with the batch before. It writes a short report with at most three things
to try, each with the figure that would show it worked. You don't need to do anything with it.

## What Claude won't ask you

**To approve the lines.** The readiness bar is the check, and it's stricter than a skim: a line that could mean two
things, or that clashes with another line, is refused before anyone builds it. Claude tells you afterwards which
items are ready and what their lines say. You can read them in the backlog (`work show b<n>`) and again in the pull
request, and change them there.

**To start a batch.** Readying an item is the decision to build it. When an item is `ready` and no batch is open,
Claude starts one. Nothing waits on you between the start of a batch and its reviewed pull request.

What it will ask: to merge a pull request, to accept a request, and to upgrade the repository when the plugin is
newer (see below). Those are yours.

## What you see when a session starts

Three hooks run as a session starts. Each prints nothing when there's nothing to say.

**A pending upgrade.** `migrate status --hook` speaks only when the repository is behind the plugin:

```text
This repository is on plugin version 0.32.0 and the plugin is on 0.33.0. Offer the person the upgrade from 0.32.0 to 0.33.0, which applies:
  0.33.0 "the controlled language 4": write each file's marker codified-2, import the CLI pack and give each verb its aspect where its lines decide it, and name by file and id each line that no longer parses and what else a session rewords
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

When an item rests on something you said, Claude keeps your exact words with `work quote`. A quote is a small file
under `.shop/quotes/` with your message and the turns around it, committed with everything else. Months later,
anyone can see why an item exists, in your words rather than a summary of them.

```console
$ work quote "I trust you to make some delightful docs."
quote-24 "I trust you to make some delightful docs."
$ work show quote-20
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
batch carries on. `work backlog` lists it under its own heading:

```console
$ work backlog
...
## needs-input (1)

| rank | item | title | provenance | value | urgency | size | score | waiting on |
|---|---|---|---|---|---|---|---|---|
| 1 | b7 | Close the generator gaps in spec_steps | own | high-value | medium-urgency | large | 1.67 | question: The item's lines fail the suite as laid, before any code: ... How are the gloss and r20 reworded? ... |
```

Tell Claude your answer, or record it yourself. The item goes back to `shaped`, the question and its answer kept on
it, and it's shaped and readied again:

```console
$ work answer b7 "Reword the gloss as one sentence and give g20 its own trigger; retire readiness#r12; yes, change the three asserts."
b7 "Close the generator gaps in spec_steps" shaped
```

To stop work you don't want, say so: Claude withdraws an item (`work withdraw`) or abandons a batch
(`work batch abandon`). [Recipes](recipes.md) has the steps.

Next: [the tour](tour.md) · [recipes](recipes.md) · [concepts](concepts.md)
