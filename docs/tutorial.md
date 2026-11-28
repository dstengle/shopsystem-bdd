<!--
The commands and files on this page are replayed by tests/scripts/test_docs_tutorial.py, in order, in an empty
temporary folder: each `$ ` line runs and prints what is shown (`...` cuts a path or a line that changes run to run),
each block after a `tutorial: file` comment is written whole at the path it names, and the `tutorial: merge` comment
is the person's merge, made on a stand-in for GitHub (tests/scripts/stub_gh.py, whose pull request URLs are
github.com/ex/ctx's). The folder it ends with is compared with docs/examples/notes-cli/. Outputs are from those runs,
on 2026-11-28, from the plugin's main.
-->

# Tutorial: the notes product from an empty folder

This tutorial builds a small product, a command-line notes tool, from an empty folder to the context kept whole in
[`docs/examples/notes-cli/`](examples/notes-cli/README.md). It goes in the order the work goes: the product, its actor
and jobs, the bounded context that does them, a capability, its domain model, its requirement lines, the batch that
builds them, the merge, and the actor the context plays.

Each step has three parts:

- **You say**: your side of the conversation, the one thing you type to Claude Code.
- **The session does**: the commands it runs for you, with what they print. You never type these; they are here so you
  can see what happens underneath.
- **The files**: what the step writes or changes in your folder.

[Getting started](getting-started.md) is the short version of the same walk; this page shows every command and every
file. Commands are written as `shop ...`; [how the commands are run](reference/commands.md#how-the-commands-are-run)
shows how to run one yourself.

## Before you start: an empty folder

Install the plugin as [getting started](getting-started.md#2-install-the-plugin) says, in an empty folder, and restart
the session.

**You say:**

> Set up this repository for the plugin. It's the notes CLI, bounded-context/example.org/notes/notes-cli: a
> command-line tool that keeps short notes, where the person adds a note, lists them and removes one. It is not an
> editor and not a sync service. Push it to https://github.com/example/notes-cli.

**The session does:** it makes the folder a git repository with the GitHub remote you named, and founds the context
with its id and purpose.

```console
$ git init -q -b main
$ git remote add origin https://github.com/example/notes-cli.git
$ shop migrate init --id bounded-context/example.org/notes/notes-cli --purpose "A command-line tool that keeps short notes: the person adds a note, lists them and removes one. It is not an editor and not a sync service."
wrote .gitignore
wrote .shop/backlog/.gitkeep
wrote .shop/delivery.toml
wrote .shop/plugin-version
wrote .shop/records/README.md
wrote features/.gitkeep
wrote spec/capabilities/.gitkeep
wrote spec/index.md
wrote spec/model/.gitkeep
wrote spec/universal.md
wrote spec/vocabulary/.gitkeep
wrote tests/scenarios/conftest.py
```

**The files:** `spec/index.md` (the context's id, language and purpose), `spec/universal.md` (no universal condition
yet), the empty `spec/model/`, `spec/vocabulary/` and `spec/capabilities/`, `features/`, `.shop/` for the backlog and
records, and `tests/scenarios/conftest.py`, in one commit.

## 1. The product

**You say:**

> The notes tool is a product of its own, example.org/notes. It's there to keep a writer's passing thoughts at hand.

**The session does:** it declares the product in the shop's product file.

```console
$ shop spec product example.org/notes --purpose "Keep a writer's passing thoughts at hand."
declared the product example.org/notes
```

**The files:** `.shop/product/product.toml`, the product's id and purpose. Every product command is one commit of this
file, pushed; nothing writes it by hand.

## 2. The actor and the jobs

**You say:**

> It's for a writer. When a thought comes up, they want to note it down so they can find it later. When they sit down
> to write, they want to see every note they kept. And they clear out the notes they're done with.

**The session does:** it names the product's actor, the writer, and writes each thing the writer wants done as a
**job**, its statement in the one form `When <situation>, <actor> wants <motivation>, so they can <outcome>.`.
Finding notes and clearing them out make no sense before notes are kept, so those two jobs **need** `keep-notes`.

```console
$ shop spec actor "the writer"
declared the product actor the writer
$ shop spec job keep-notes --actor "the writer" --statement "When a thought comes up, the writer wants to note it down, so they can find it later."
declared the job keep-notes
$ shop spec job find-notes --actor "the writer" --statement "When the writer sits down to write, the writer wants to see every note they kept, so they can pick one up." --needs keep-notes
declared the job find-notes
$ shop spec job clear-notes --actor "the writer" --statement "When a note is done with, the writer wants to remove it, so they can keep the list short." --needs keep-notes
declared the job clear-notes
```

**The files:** the actor and the three jobs in `.shop/product/product.toml`, one commit each.

## 3. The context

**You say:**

> Keeping, finding and clearing notes is the core of it, and this repository does all three. It's kept on its own,
> in the shop example.org/notes/shop. It only needs the request words, nothing of the base pack.

**The session does:** it draws the product's domain map: one core subdomain for the three jobs, this bounded context
addressing it, and each job given to the context.

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
```

Then it gives the context's index its short title, `notes`, and the one pack you asked for: `migrate init` imports
`base` and `request`, and the notes words need only `request` (*request*, *service*, *refuse*, *return* and the rest).
No command writes these two fields, so the session writes the file and commits it:

<!-- tutorial: file spec/index.md -->
```markdown
---
id: bounded-context/example.org/notes/notes-cli
title: notes
language: codified-2
imports: [request]
---

# notes

## Purpose

A command-line tool that keeps short notes: the person adds a note, lists them and removes one. It is not an editor
and not a sync service.

## Composition
```

```console
$ git add spec/index.md
$ git commit -q -m "The notes context: its title and the request pack"
$ git push -q origin main
```

`shop spec check` says what is still to do, as warnings: no actor here plays the writer yet, and nothing serves the
jobs.

```console
$ shop spec check
warning w_unplayed_actor  a product actor of a job held here that no actor of this bounded context plays  (3)
    clear-notes, the writer
    find-notes, the writer
    keep-notes, the writer
warning w_unreached_sub  a subdomain of a job held here whose trace reaches no bounded context that addresses it  (3)
    clear-notes, note-keeping
    find-notes, note-keeping
    keep-notes, note-keeping
warning w_unserved_job  a job nothing serves  (3)
    job/example.org/notes/notes-cli/clear-notes
    job/example.org/notes/notes-cli/find-notes
    job/example.org/notes/notes-cli/keep-notes
0 violations, 9 warnings, 0 unresolved references, 0 file problems
```

**The files:** the subdomain, the context and its three jobs in `.shop/product/product.toml`; `spec/index.md`.

## 4. The capability

**You say:**

> I want a command-line notes tool. I add a note with a title and a tag, I list the notes, and I remove one. A note
> without a title is refused, and a note that's already removed can't be removed again.

**The session does:** its `shaping-items` skill takes this up. It keeps your words as a quote (`shop work quote`,
which reads your message from the session's transcript, so it is not run here), writes the idea down as an item in
the backlog, shapes it, and opens on the item a new capability, `notes`, in a new area of the model, `notes-cli`.

```console
$ shop work idea "A command-line notes tool"
b1 "A command-line notes tool" idea
$ shop work shape b1 --note "the person adds a note with a title and a tag, lists the notes and removes one; a note without a title is refused, and a removed note is not removed again"
b1 "A command-line notes tool" shaped
$ shop work line b1 --capability notes --narrator "the person" --area notes-cli "Adding, listing and removing notes."
b1 "A command-line notes tool": a new capability notes
```

**The files:** `.shop/backlog/b1.md`, the item, with its notes and the capability's block under `## Requirements`.
Nothing under `spec/` changes until the item's batch applies it (step 7).

## 5. The model

**The session does:** it writes on the item what there is and what can be asked of it, the domain model of the area
`notes-cli`: a note with a title, a status and its tags, and the notes service with its three operations, each
operation's outcomes, and the person who asks.

```console
$ shop work line b1 --into notes --model "object note
  attributes: title (text); status: kept | removed
  lifecycle status: kept → removed
  relations: under → tag (many)

object tag

service notes
  operation add(title, tag)  outcomes: done → the note | refused: no title
  operation list()  outcomes: returned → every note
  operation remove(note)  outcomes: done

actor the person kind of agent"
b1 "A command-line notes tool": model lines of notes-cli
```

Then the words a line may use, each naming one element of the model. A verb that names an operation is how a line
says a request:

```console
$ shop work line b1 --into notes --term="- **the notes service** (proper noun) → service notes. What answers the person's requests about notes." --term="- **note** (noun) → object note. One short text the person keeps, with a title." --term="- **tag** (noun) → object tag. A word the person files a note under." --term="- **title** (attribute) → attribute note.title. The one line that names a note." --term="- **status** (attribute) → attribute note.status. Whether a note is kept or removed." --term="- **kept** (adjective) → value note.status kept." --term="- **removed** (adjective) → value note.status removed." --term="- **add** (verb, action) → operation notes.add. Forms: adds, added. Frame: <actor> adds <note>." --term="- **list** (verb, action) → operation notes.list. Forms: lists, listed. Frame: <actor> lists the notes." --term="- **remove** (verb, action) → operation notes.remove. Forms: removes, removed. Frame: <actor> removes <note>."
b1 "A command-line notes tool": 10 vocabulary entries of notes-cli:
...
```

The person is a word every area reads, so it goes into the shared layer, `spec/vocabulary/shared.md`. No command writes
that layer yet, so the session writes it and commits it:

<!-- tutorial: file spec/vocabulary/shared.md -->
```markdown
---
id: vocabulary/example.org/notes/notes-cli/shared
---

# Shared words

## Terms

- **the person** (proper noun) → actor the person. The human at the terminal.
```

```console
$ git add spec/vocabulary/shared.md
$ git commit -q -m "The shared words: the person"
$ git push -q origin main
```

**The files:** the item's `### notes-cli model` block and its vocabulary entries in `.shop/backlog/b1.md`;
`spec/vocabulary/shared.md`. [The domain model](reference/domain-model.md) has the syntax of both.

## 6. The lines

**The session does:** it writes what you said as requirement lines, one group each, and dedicates each group to the
job it does (`--serves`). No line names a command, an option or an exit code: they say what the person asks of the
notes service and what it answers.

<!-- docs: context docs/examples/notes-cli -->
```console
$ shop work line b1 --into notes --group "A note added with a title and a tag is kept" "When the person adds a note with a title and a tag, the notes service shall keep the note under the tag." --serves keep-notes
b1 "A command-line notes tool": notes#r1 When the person adds a note with a title and a tag, the notes service shall keep the note under the tag.
b1 "A command-line notes tool": notes#g1 serves keep-notes
$ shop work line b1 --into notes --group "A note added without a title is refused" "If the person adds a note without a title, then the notes service shall refuse the request and name the title." --serves keep-notes
b1 "A command-line notes tool": notes#r2 If the person adds a note without a title, then the notes service shall refuse the request and name the title.
b1 "A command-line notes tool": notes#g2 serves keep-notes
$ shop work line b1 --into notes --group "Listing the notes returns every note" "When the person lists the notes, the notes service shall return every note." --serves find-notes
b1 "A command-line notes tool": notes#r3 When the person lists the notes, the notes service shall return every note.
b1 "A command-line notes tool": notes#g3 serves find-notes
$ shop work line b1 --into notes --group "Removing a note sets its status to removed" 'When the person removes a note, the notes service shall set the status of the note to `removed`.' --serves clear-notes
b1 "A command-line notes tool": notes#r4 When the person removes a note, the notes service shall set the status of the note to `removed`.
b1 "A command-line notes tool": notes#g4 serves clear-notes
$ shop work line b1 --into notes --group "A removed note is not removed again" 'If the person removes a note whose status is `removed`, then the notes service shall refuse the request.' --serves clear-notes
b1 "A command-line notes tool": notes#r5 If the person removes a note whose status is `removed`, then the notes service shall refuse the request.
b1 "A command-line notes tool": notes#g5 serves clear-notes
```

Then it rates the item and readies it: on a copy of `spec/` with the item applied, every line parses to one meaning,
no two lines clash, every operation of the model is requested by a line and its refusal stated by one, and each group
can be written as a scenario.

```console
$ shop work rate b1 --value high-value --urgency high-urgency --size small
b1 "A command-line notes tool" shaped
$ shop work ready b1
b1 "A command-line notes tool" ready
```

The session doesn't ask you to approve the lines; it tells you the item is ready and what its lines say. Ask "what does
r2 say exactly?" and it reads the line back from its logical form ([the example](examples/notes-cli/README.md#what-a-line-means)
shows it).

**The files:** the item's groups and lines in `.shop/backlog/b1.md`, its rating, and its status `ready`.

## 7. The batch

Readying an item is the decision to build it, so the session starts a batch without asking. If it doesn't, **you
say:**

> Build what's ready.

**The session does:** it starts the batch, which applies the item to `spec/` on the batch's branch, and hands the
batch brief to one fresh agent, the batch's driver.

```console
$ shop work batch start
batch-1 building: t1 b1 "A command-line notes tool"
batch brief: .../.shop/worktrees/batch-1-driver/brief.md
```

The start's commit on the task's branch wrote `spec/capabilities/notes.md` with the five lines in its `unbuilt:` list,
`spec/model/notes-cli.md` and `spec/vocabulary/notes-cli.md`, the area's row under `spec/index.md`'s `## Composition`,
and the scenarios, `features/notes.feature`, which nobody writes by hand:

<!-- docs: context docs/examples/notes-cli -->
```gherkin
# generated from spec/capabilities/notes.md by features generate; do not edit
Feature: Notes
  Narrator: the person

  @g1 @r1
  Scenario: A note added with a title and a tag is kept
    Given a tag t1
    When the person adds a note n1 with a title and the tag t1
    Then the note n1 is under the tag t1
    And the notes service keeps the note n1

  @g2 @r2
  Scenario: A note added without a title is refused
    When the person adds a note n1 without a title
    Then the notes service refuses this request
    And the notes service names the title

  @g3 @r3
  Scenario: Listing the notes returns every note
    Given a note n1
    And a note n2
    When the person lists the notes
    Then the notes service returns the note n1
    And the notes service returns the note n2

  @g4 @r4
  Scenario: Removing a note sets its status to removed
    Given a note n1
    When the person removes the note n1
    Then the notes service sets the status of the note n1 to `removed`

  @g5 @r5
  Scenario: A removed note is not removed again
    Given a note n1
    And the status of the note n1 is `removed`
    When the person removes the note n1
    Then the notes service refuses this request
```

The driver gives the task its worktree, and the task's agent builds the item there,
`.shop/worktrees/batch-1-t1`:

```console
$ shop work batch resume batch-1
batch-1 building: plan .shop/batches/1/plan.md
t1 b1 "A command-line notes tool": running in .shop/worktrees/batch-1-t1 on batch-1-b1: build notes#r1, notes#r2, notes#r3, notes#r4, notes#r5; then shop work batch done batch-1 t1, or shop work batch park batch-1 b1 --question <text>
```

A first batch makes what nothing has made yet. The agent writes the program, `notes.py`: one argparse subcommand an
operation, the notes kept in `notes.json` beside it, a refusal exiting 1 with its reason on stderr.

<!-- tutorial: file .shop/worktrees/batch-1-t1/notes.py -->
```python
#!/usr/bin/env python3
"""notes: the example's program, the CLI adapter of the notes service. Each command is a request of one operation
(spec/adapters/cli.toml): `notes add --title T --tag G`, `notes list`, `notes remove N`. The notes are kept in
notes.json beside it; a refusal exits 1 and names what is missing."""
import argparse
import json
import sys
from pathlib import Path


def load(root):
    path = Path(root) / "notes.json"
    return json.loads(path.read_text()) if path.is_file() else []


def save(root, notes):
    (Path(root) / "notes.json").write_text(json.dumps(notes, indent=1) + "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="notes")
    parser.add_argument("--root", default=".")
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("add")
    add.add_argument("--title")
    add.add_argument("--tag", action="append", default=[])
    sub.add_parser("list")
    sub.add_parser("remove").add_argument("note", type=int)
    args = parser.parse_args(argv)
    notes = load(args.root)
    if args.command == "add":
        if not args.title:
            print("notes add: a note needs --title", file=sys.stderr)
            return 1
        notes.append({"title": args.title, "tags": args.tag, "status": "kept"})
    elif args.command == "list":
        for n, note in enumerate(notes, 1):
            if note["status"] == "kept":
                print("%d %s %s" % (n, note["title"], " ".join("#" + t for t in note["tags"])))
        return 0
    else:
        if notes[args.note - 1]["status"] == "removed":
            print("notes remove: note %d is removed already" % args.note, file=sys.stderr)
            return 1
        notes[args.note - 1]["status"] = "removed"
    save(args.root, notes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

It writes the adapter contract, `spec/adapters/cli.toml`, which maps each operation of the model to the program's
command and options; `shop spec check` holds the two to each other both ways:

<!-- tutorial: file .shop/worktrees/batch-1-t1/spec/adapters/cli.toml -->
```toml
# The CLI adapter's contract of the notes service: each operation of the domain model with the command that requests
# it and the option or argument of each parameter, checked both ways against notes.py's argparse by `spec check`.
adapter = "cli"
json = "--json"

[programs]
notes = "notes.py"

[outcomes]
done = { exit = 0 }
returned = { exit = 0, content = "stdout" }
refused = { exit = 1, errors = "stderr" }
broken = { exit = 1, errors = "stderr" }

[cli-only]
options = ["--root", "--json"]

[operations."notes.add"]
command = "notes add"
[operations."notes.add".parameters]
title = { option = "--title", example = "Buy milk" }
tag = { option = "--tag", repeat = true }

[operations."notes.list"]
command = "notes list"

[operations."notes.remove"]
command = "notes remove"
[operations."notes.remove".parameters]
note = { positional = 1, example = "1" }
```

and has `shop spec annotate` write under each operation the lines that govern it:

```console
$ shop spec --root .shop/worktrees/batch-1-t1 annotate
annotated spec/adapters/cli.toml
```

It writes the step bindings, `tests/scenarios/test_notes.py`: one step definition a step text, a When running
`notes.py` with the command and options the contract names, a Then reading its exit, its output and the notes it kept.

<!-- tutorial: file .shop/worktrees/batch-1-t1/tests/scenarios/test_notes.py -->
```python
import json
import pathlib
import subprocess
import sys

import pytest
from pytest_bdd import given, parsers, scenarios, then, when

NOTES = pathlib.Path(__file__).parents[2] / "notes.py"
scenarios("../../features/notes.feature")


@pytest.fixture
def world(tmp_path):
    return {"dir": tmp_path, "notes": [], "tags": {}, "removed": []}


def notes(world, *args):
    world["run"] = subprocess.run([sys.executable, NOTES, *args], cwd=world["dir"],
                                  capture_output=True, text=True)
    return world["run"]


def saved(world):
    path = world["dir"] / "notes.json"
    return json.loads(path.read_text()) if path.exists() else []


def kept(world):
    """The notes the Givens name, added before a request that reads them."""
    for n in world["notes"]:
        notes(world, "add", "--title", "Note " + n)
    for n in world["removed"]:
        notes(world, "remove", str(world["notes"].index(n) + 1))


@given(parsers.parse("a note {n}"))
def a_note(world, n):
    world["notes"].append(n)


@given(parsers.parse("the status of the note {n} is `removed`"))
def removed_already(world, n):
    world["removed"].append(n)


@given(parsers.parse("a tag {t}"))
def a_tag(world, t):
    world["tags"][t] = "tag-" + t


@when(parsers.parse("the person adds a note {n} with a title and the tag {t}"))
def add_with_tag(world, n, t):
    notes(world, "add", "--title", "Note " + n, "--tag", world["tags"][t])


@when(parsers.parse("the person adds a note {n} without a title"))
def add_without_title(world, n):
    notes(world, "add")


@when("the person lists the notes")
def list_notes(world):
    kept(world)
    notes(world, "list")


@when(parsers.parse("the person removes the note {n}"))
def remove(world, n):
    kept(world)
    notes(world, "remove", str(world["notes"].index(n) + 1))


@then(parsers.parse("the note {n} is under the tag {t}"))
def under_tag(world, n, t):
    assert saved(world)[-1]["tags"] == [world["tags"][t]]


@then(parsers.parse("the notes service keeps the note {n}"))
def keeps(world, n):
    assert world["run"].returncode == 0 and saved(world)[-1]["title"] == "Note " + n


@then("the notes service refuses this request")
def refuses(world):
    assert world["run"].returncode == 1


@then("the notes service names the title")
def names_title(world):
    assert "--title" in world["run"].stderr


@then(parsers.parse("the notes service returns the note {n}"))
def returns(world, n):
    assert world["run"].returncode == 0 and "Note " + n in world["run"].stdout


@then(parsers.parse("the notes service sets the status of the note {n} to `{value}`"))
def sets_status(world, n, value):
    assert saved(world)[world["notes"].index(n)]["status"] == value
```

With each scenario red first and then green, it takes the five ids out of the capability's `unbuilt:`. The capability
it leaves, with its `rests_on:` and its empty `## Dropped`:

<!-- tutorial: file .shop/worktrees/batch-1-t1/spec/capabilities/notes.md -->
<!-- docs: context docs/examples/notes-cli -->
````markdown
---
id: capability/example.org/notes/notes-cli/notes
title: Notes
narrator: the person
group: service
area: notes-cli
specifies: service notes
language: codified-2
rests_on: []
retired: []
unbuilt: []
---

# Notes

## Purpose

Adding, listing and removing notes.

## Behaviour

### [g1] A note added with a title and a tag is kept
serves: keep-notes
- [r1] When the person adds a note with a title and a tag, the notes service shall keep the note under the tag.

### [g2] A note added without a title is refused
serves: keep-notes
- [r2] If the person adds a note without a title, then the notes service shall refuse the request and name the title.

### [g3] Listing the notes returns every note
serves: find-notes
- [r3] When the person lists the notes, the notes service shall return every note.

### [g4] Removing a note sets its status to removed
serves: clear-notes
- [r4] When the person removes a note, the notes service shall set the status of the note to `removed`.

### [g5] A removed note is not removed again
serves: clear-notes
- [r5] If the person removes a note whose status is `removed`, then the notes service shall refuse the request.

## Dropped
````

It gives the area's model file its title and a purpose of its own, in place of the heading `Notes cli` and the
capability's purpose that the start wrote there:

<!-- tutorial: file .shop/worktrees/batch-1-t1/spec/model/notes-cli.md -->
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

and `spec/moves.json`, the context's capability moves, of which there are none:

<!-- tutorial: file .shop/worktrees/batch-1-t1/spec/moves.json -->
```json
{}
```

It commits, citing the item, and the driver marks the task done once the whole suite passes in the worktree:

```console
$ git -C .shop/worktrees/batch-1-t1 add -A
$ git -C .shop/worktrees/batch-1-t1 commit -q -m "The notes tool: notes.py, its CLI contract and its scenarios' steps" --trailer "Item: b1"
$ shop work batch done batch-1 t1
batch-1 t1 b1 "A command-line notes tool": done
```

Then it opens the pull request, writes the reviewer's brief and has one fresh `pr-reviewer` read it:

```console
$ shop work batch review batch-1
next: shop work batch brief batch-1, the pr-reviewer on it, then shop work batch reviewed batch-1
https://github.com/.../pull/1
$ shop work batch brief batch-1
.shop/worktrees/batch-1-review-1/brief.md
```

The reviewer's reply is saved as the findings file:

<!-- tutorial: file .shop/worktrees/batch-1-review-1/findings.md -->
```markdown
## Verdict

The batch builds b1: the notes tool, its CLI contract and the steps of its five scenarios, which pass. No finding holds the merge.

## Findings
```

```console
$ shop work batch reviewed batch-1
batch-1 review 1: 0 findings -> awaiting-merge; the pull request https://github.com/.../pull/1 is ready for the person's merge
```

**The files:** on the batch's branch, `notes.py`, `spec/adapters/cli.toml`, `tests/scenarios/test_notes.py`, the
capability, the model, the vocabulary and `features/notes.feature`; under `.shop/batches/1/`, the batch's plan and its
review. The driver stops here: it never merges.

## 8. The merge

**You do:** read the pull request on GitHub (the lines, the feature, the code) and merge it. This step is always yours.

<!-- tutorial: merge batch-1 -->

**You say:**

> The pull request is merged.

**The session does:** it records the merge: the item is delivered, the batch's worktrees and branches are cleaned up,
and the batch's summary is printed.

```console
$ shop work batch merged batch-1
batch-1 merged
batch summary of batch-1
...
```

**The files:** `main` holds the batch's work; `.shop/backlog/b1.md` is `delivered`.

## 9. The plays

**The session does:** the product's actor, the writer, is the person this context's model now declares, so the
session maps one to the other, and runs the check on the merged spec:

```console
$ shop spec plays "the writer" --in bounded-context/example.org/notes/notes-cli --as "the person"
mapped the product actor the writer to the person in the bounded context bounded-context/example.org/notes/notes-cli
$ shop spec check
0 violations, 0 warnings, 0 unresolved references, 0 file problems
```

No warning is left: every job is served, the writer is played, and every capability serves a job. Ask "what does
clearing notes rest on?" and the session answers with the job's **trace**, every requirement that does it, the job it
needs bringing its own:

<!-- docs: context docs/examples/notes-cli -->
```console
$ shop spec trace clear-notes
the trace of the job clear-notes:
  notes#r4 (served by notes#g4): When the person removes a note, the notes service shall set the status of the note to `removed`.
  notes#r5 (served by notes#g5): If the person removes a note whose status is `removed`, then the notes service shall refuse the request.
  notes#r1 (needed job keep-notes: served by notes#g1): When the person adds a note with a title and a tag, the notes service shall keep the note under the tag.
  notes#r2 (needed job keep-notes: served by notes#g2): If the person adds a note without a title, then the notes service shall refuse the request and name the title.
```

**The files:** the context's actor mapping in `.shop/product/product.toml`.

## Where you are

Your folder's `spec/`, `features/`, `notes.py` and `.shop/product/product.toml` are now
[`docs/examples/notes-cli/`](examples/notes-cli/README.md)'s, file for file; the example reads each of them through.
From here it is the same loop: say what you want ("listing the notes should give their tags too"), and the session
shapes an item, readies it and builds it in a batch that ends in one pull request for you to merge.

Next:

- [Talking with Claude](talking-with-claude.md): what to say, what follows, and the few things you're asked.
- [Writing requirements](writing-requirements.md): the language, with "this, not that" pairs.
- [A tour of the internals](internals-tour.md): the batch's machinery, stop by stop.
