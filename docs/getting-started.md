<!--
The spec and feature on this page are docs/examples/notes-cli/'s, which the docs test checks; the example keeps no
test module, so the step bindings of step 6 are a sketch of the module a first batch writes. The pytest outputs are
from real runs on 2026-11-19: plugin 0.38.0, Python 3.11, pytest 9.1.1, pytest-bdd 8.1.0, in a scratch repository
built from docs/examples/notes-cli/ with that module. The outputs of steps 3, 4 and 8 are from runs on 2026-11-26,
plugin 0.44.0; step 8's on a copy of docs/examples/notes-cli/ replayed as talking-with-claude.md says, and its
before-the-first-batch check in a context `migrate init` had just founded. The home directory is written as ~, and
long paths are cut with "...".
-->

# Getting started

This page takes you from an empty folder to a first green scenario, by talking with Claude Code. You say a few
things in plain words; the session works out what to run. You don't run the plugin's tools yourself: they are
scripts inside the plugin, not commands on your `PATH`, and the session knows where they are.

Each step below is one thing to say, what the session does with it, and what you see. The example is a small notes
tool, the one kept whole in [`docs/examples/notes-cli/`](examples/notes-cli/README.md).

Here is where you're heading. You say what you want, and the session writes it as lines like this one:

```markdown
- [r4] When the person removes a note, the notes service shall set the status of the note to `removed`.
```

and the plugin writes its test scenario from it:

```gherkin
Feature: Notes
  Narrator: the person

  @g4 @r4
  Scenario: Removing a note sets its status to removed
    Given a note n1
    When the person removes the note n1
    Then the notes service sets the status of the note n1 to `removed`
```

## 1. What you need

- **Linux on x86_64**, where the session can download the grammar tools. Elsewhere, build GF 3.12 yourself and set
  `$SHOPSYSTEM_GF` to its `gf`.
- **Python 3.**
- **git, and `gh` logged in** (`gh auth login`), for a batch's pull request and a request's issue.
- **Claude Code.**

The session installs the rest: a virtualenv for your project with pytest 9.1 and pytest-bdd 8.1 (with pytest-bdd 9,
an id the spec has not built yet is no longer an expected failure), and the grammar tools.

## 2. Install the plugin

In an empty folder for your project, start Claude Code and type these two commands into it:

```text
/plugin marketplace add dstengle/shopsystem-bdd
/plugin install shopsystem-bdd@shopsystem-bdd
```

Restart the session once it says the plugin is installed, so its skills and hooks load.

## 3. Say: "Set up this repository for the plugin"

The session:

- makes the folder a git repository, if it isn't one, and a virtualenv `.venv` with pytest and pytest-bdd;
- installs the grammar tools once: GF (the Grammatical Framework, which parses requirement lines), clingo (which
  checks them against each other), the pinned pgf wheel and GF's resource grammar library. In an empty folder there
  is no code yet, and that's fine: the grammar tools are installed all the same;
- asks you for the context's id, `bounded-context/<domain>/<path>` (say `bounded-context/example.org/notes/notes-cli`),
  and for its purpose, what the context is for in a sentence or two, and founds the context with them
  (`shop migrate init --id <id> --purpose "<purpose>"`): `spec/index.md` with the purpose under `## Purpose`,
  `spec/universal.md`, the empty `spec/model/`, `spec/vocabulary/` and `spec/capabilities/`, `.shop/` for the backlog
  and records, `features/` and `tests/scenarios/conftest.py`, in one commit;
- asks for, or creates with `gh`, the GitHub repository it pushes to, since a batch ends in a pull request there.

What you see is the grammar tools it found, and the commit:

```text
no Python file: the analysis tools are not probed or installed; agents search by text, and say so
grammar:
  gf 3.12.0 (~/.local/share/shopsystem-bdd/gf-3.12/bin/gf)
  pgf 1.1
  clingo 5.8.2
  gf-rgl 20250812 (~/.local/share/shopsystem-bdd/gf-rgl-20250812)
```

The first line is the analysis tools' (the coverage map and the reference finder of `shop tools`): with no Python
file in the folder there is nothing for them to read yet, so they are left out and the agents search the code by
text. A tool that is missing says so on its line, with what can't be done without it. Setting up is once a repository; a
repository that already has a `spec/index.md` or a `.shop/` is never founded again.

The new `spec/index.md` imports two of the plugin's packs, `imports: [base, request]`: `request` holds the words of
a request and its response (*request*, *service*, *refuse*, *return* and the rest), and `base` the kinds most contexts
name (*text*, *file*, *version*, *repository*, *bounded context*). The plugin keeps `time`, `spec` and the deprecated
`cli` too. A word of your own spelled as a pack's collides with it (`shop spec lexicon --check` says `v_t16`) until its
entry says `Redefines: base.` or `Redefines: request.`; [Vocabulary and packs](concepts.md#vocabulary-and-packs) shows
one.

## 4. Say what you want

Say it in your own words, as you would to a colleague:

```text
I want a command-line notes tool. I add a note with a title and a tag, I list the notes, and I remove one.
A note without a title is refused.
```

The session takes this up with its `shaping-items` skill. It keeps your words (a quote under `.shop/quotes/`), makes
an item in the backlog, and writes on it everything the context needs, in the four parts of a spec:

- the **domain model**: what there is and what can be asked of it. Here, a note with a title, a status and its
  tags, and a notes service you request three operations of:

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

- the **vocabulary**: the words a line may use, each naming one element of the model. A verb that names an
  operation is how a line says a request:

  ```markdown
  - **note** (noun) → object note. One short text the person keeps, with a title.
  - **add** (verb, action) → operation notes.add. Forms: adds, added. Frame: <actor> adds <note>.
  - **the notes service** (proper noun) → service notes. What answers the person's requests about notes.
  ```

  A verb the request pack has already, such as `return`, can name one of your operations too, with `Redefines:
  request.` on its entry; its frame then names the actor that does it, `Frame: the person returns <note>.`, not a
  bare `<actor>`, so it is told apart from the pack's "the notes service returns ...". The recipe
  [A word a pack already has](recipes.md#add-a-word-to-the-vocabulary) shows it.

- the **requirements**: the rules, one line each, in a new capability `notes`:

  ```markdown
  ### [g1] A note added with a title and a tag is kept
  - [r1] When the person adds a note with a title and a tag, the notes service shall keep the note under the tag.

  ### [g2] A note added without a title is refused
  - [r2] If the person adds a note without a title, then the notes service shall refuse the request and name the title.

  ### [g3] Listing the notes returns every note
  - [r3] When the person lists the notes, the notes service shall return every note.

  ### [g4] Removing a note sets its status to removed
  - [r4] When the person removes a note, the notes service shall set the status of the note to `removed`.
  ```

- the **decisions**, the choices behind them, which a tool this small doesn't need yet.

No line names a command, an option or an exit code: those belong to the CLI adapter, which the first batch writes
(step 6). Then the session readies the item: every line parses to exactly one meaning, no two lines clash, and each
group can be written as a scenario. It may ask you a question first, when what you said leaves a choice open ("may
two notes have the same title?"). It won't ask you to approve the lines; it tells you afterwards which item is ready
and what its lines say.

The item's lines stay on the item until its batch merges. [The capability file](reference/capability-file.md),
[the domain model](reference/domain-model.md) and [the vocabulary](concepts.md#vocabulary-and-packs) have every field of these files.

Keeping your words needs a live session: `shop work quote` finds your message in the transcript the session's
UserPromptSubmit hook names. Run by hand in a plain shell, with no session, it is refused and keeps nothing:

```console
$ shop work quote "I want a command-line notes tool."
work quote: no session is known: the UserPromptSubmit hook keeps it (work quote --hook), or give --session <id>
```

Give it the session's id with `--session <id>` if you quote by hand; in a session the hook does it for you.

## 5. Ask what a line means

Ask about any line, in plain words: "what does r4 say exactly?" The session reads it back from its logical form, the
one meaning the plugin parsed it to:

```text
shall [x1: agent the person (constant), x3: service the notes service (constant)]
  when [x2: note]
    request(e1, notes.remove, subject: x1, object: x2)
  response
    initiates(e2, subject: x3, status(x2) = `removed`)
```

**When** the person requests `notes.remove` of a note x2, the notes service **shall** set the status of that same x2
to `removed`. A line that could be read two ways, or that leaves something out, is refused before anyone builds it.
Say "the note" where nothing gave a note, and the plugin won't guess which:

```refused
When the person removes the note, the notes service shall set the status of the note to `removed`.
```

The session rewords such a line itself, from what the refusal says. If you want a line changed, say so: "a removed
note should be kept for a week". [Writing requirements](writing-requirements.md) has more pairs like this.

## 6. The session builds it

Readying an item is the decision to build it, so the session starts a batch without asking. The batch lays the
item's lines into `spec/`, writes the feature file from them, and hands the work to one fresh agent, which builds
what the lines say and opens one pull request. Nobody writes the feature file by hand:

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
```

In a new context the first batch also makes three things nothing has made yet:

- **the program**, here `notes.py`, a small command-line tool;
- **the adapter contract**, `spec/adapters/cli.toml`, which maps each operation of the model to the program's
  command and options (`notes.add` is `notes add --title ... --tag ...`) and lists under each operation the lines
  that govern it, its refusal among them. The plugin checks the contract against the program's argparse both ways;
  [adapter contracts](reference/adapters.md) has its form;
- **the step bindings**, `tests/scenarios/test_notes.py`: plain pytest-bdd steps, one step definition a step text.
  A When makes the request through the adapter, here by running `notes.py` with the command and options the
  contract names; a Then reads the response: the exit code, what it printed, what it kept.

The shape of the bindings:

```python
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("../../features/notes.feature")


@given(parsers.parse("a note {n}"))
def a_note(world, n):
    world["notes"].append(n)


@when(parsers.parse("the person removes the note {n}"))
def remove(world, n):
    kept(world)
    notes(world, "remove", str(world["notes"].index(n) + 1))


@then(parsers.parse("the notes service sets the status of the note {n} to `{value}`"))
def sets_status(world, n, value):
    assert saved(world)[world["notes"].index(n)]["status"] == value
```

<details>
<summary>The whole file (94 lines)</summary>

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
    return {"dir": tmp_path, "notes": [], "tags": {}}


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


@given(parsers.parse("a note {n}"))
def a_note(world, n):
    world["notes"].append(n)


@given(parsers.parse("a tag {t}"))
def a_tag(world, t):
    world["tags"][t] = "tag-" + t


@when(parsers.parse("the person adds the note {n} with a title and the tag {t}"))
def add_with_tag(world, n, t):
    notes(world, "add", "--title", "Note " + n, "--tag", world["tags"][t])


@when(parsers.parse("the person adds the note {n} without a title"))
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

</details>

### Red, then green

While the lines are laid and the code is not written, the batch keeps their ids in the capability's `unbuilt:` list,
and the plugin's pytest plugin runs those scenarios as strict expected failures. The `tests/scenarios/conftest.py`
that `shop migrate init` wrote loads that plugin, so plain pytest in the project folder runs them, with each `@g` and
`@r` tag a registered mark:

```console
$ .venv/bin/python -m pytest -q tests
```

The spec is ahead of the code, and the suite says so honestly:

```text
xxxx                                                                     [100%]
XFAIL tests/scenarios/test_notes.py::test_removing_a_note_sets_its_status_to_removed - unbuilt: notes#r4
4 xfailed in 0.27s
```

As each line's code lands, its id leaves `unbuilt:` (a scenario that passes while still listed fails the suite, with
`[XPASS(strict)] unbuilt: notes#r1`). Once the batch is built:

```text
....                                                                     [100%]
4 passed in 0.22s
```

Green: four lines of spec, four scenarios, four passing tests.

## 7. Review and merge

The batch's pull request is reviewed once by a fresh reviewer, and what it finds is fixed before the pull request
reaches you. The session tells you when it is ready. Read it on GitHub (the lines, the feature, the code) and merge
it. Then say:

```text
The pull request is merged.
```

The session marks the item delivered, cleans up the batch's branches, runs `shop spec check` on the merged spec, and
runs any `shop spec plays` that waited for the merge (step 8). Then it starts the next batch if anything else is
ready.

## 8. Say what the product is for

The notes tool is a bounded context, and a bounded context is built for a product: someone it serves and the jobs
they want done. Say it, in your own words:

```text
The notes tool is for a writer. When a thought comes up, they want to note it down so they can find it later.
When they sit down to write, they want to see every note they kept. And they clear out the notes they're done with.
```

The session keeps the product in the shop's product file, `.shop/product/product.toml`: the product, the writer, each
job with its statement (finding and clearing notes **need** keeping them first), and the domain map that gives the
jobs to this bounded context. Each declaration is one command and one commit:

<!-- docs: context docs/examples/notes-cli -->
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

- **`--shop`** names the shop that keeps the bounded context: the repositories of one product kept together, here
  this one alone. Its id is a name you choose, and the plugin checks no form of it; the notes example writes the
  product's id followed by `/shop`. A bounded context with no `--shop` is a third-party provider, one no shop of the
  product keeps.
- **`spec plays` waits for the first merged batch.** It maps the product's actor, "the writer", to the actor this
  context's domain model calls the person, and the model holds that actor only once the first batch is merged (step
  7). Here the batch is merged, so it passes. Said earlier, in a new context, before its first batch, the same
  declarations are kept but `spec plays` is refused, and `shop spec check` warns that no actor here plays the writer;
  the session runs `spec plays` again after the merge:

  ```console
  $ shop spec plays "the writer" --in bounded-context/example.org/notes/notes-cli --as "the person"
  spec: --as 'the person' is no actor of the domain model of bounded-context/example.org/notes/notes-cli; it holds no actor
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

With the product declared after the merge, `shop spec check` warns of each job nothing serves yet and of the
capability that serves none: what is still to do, not errors.
[Talking with Claude](talking-with-claude.md#your-product-and-its-jobs) replays this step from its start on a copy of
the example, with every check's output.

Then the session dedicates each group of the capability to the job it does, on an item, and the batch writes that
as the group's `serves:` line. The example's g5, "a removed note is not removed again", came on that same item, from
one more thing said ("a note that's already removed can't be removed again"), its group given the job `clear-notes`. From then on, ask "what does keeping notes rest on?" and the session
answers with the job's **trace**, every requirement that does it:

<!-- docs: context docs/examples/notes-cli -->
```console
$ shop spec trace keep-notes
the trace of the job keep-notes:
  notes#r1 (served by notes#g1): When the person adds a note with a title and a tag, the notes service shall keep the note under the tag.
  notes#r2 (served by notes#g2): If the person adds a note without a title, then the notes service shall refuse the request and name the title.
```

[Talking with Claude](talking-with-claude.md#your-product-and-its-jobs) walks the whole conversation, with what the
session runs and what you see at each step. [`docs/examples/notes-cli/`](examples/notes-cli/README.md) keeps the
result: its product file and its capability with each group's job. [Concepts](concepts.md#product-job-and-trace) has
the product's words, and [the commands](reference/commands.md#shop-spec-product) every option.

## 9. From here, keep saying what you want

You've seen the whole loop once. From now on it's the same: say what you want, in your own words ("listing the notes
should give their tags too"), and the session shapes an item, readies it and builds it in a batch that ends in one
pull request for you to merge.

Next:

- [Talking with Claude](talking-with-claude.md): what to say, what follows, and the few things you're asked.
- [The tour](tour.md): one feature from an idea to a merged batch, with every command the session runs.
- [Writing requirements](writing-requirements.md): the language, with "this, not that" pairs.
- [Commands](reference/commands.md): every command the session runs, for when you want to look or do a step by
  hand.
