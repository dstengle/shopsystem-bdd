<!--
Outputs on this page are from real runs on 2026-11-19: plugin 0.38.0, its scripts as at branch domain-contract,
Python 3.11, pytest 9.1.1, pytest-bdd 8.1.0, in a scratch repository built from docs/examples/notes-cli/. The home
directory is written as ~, and long paths are cut with "...".
-->

# Getting started

This page takes you from an empty folder to a first green scenario. It's written for the developer setting up a
repository. You'll write a tiny spec for a notes tool, let the plugin check it and turn it into Gherkin, bind the
scenarios with pytest-bdd, and watch them go from red to green.

Here is where you're heading. You write one line like this:

```markdown
- [r4] When the person removes a note, the notes service shall set the status of the note to `removed`.
```

and the plugin writes its test scenario for you:

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

- **Linux on x86_64**, for `tools install`, which downloads the grammar tools. Elsewhere, build GF 3.12 yourself
  and set `$SHOPSYSTEM_GF` to its `gf`.
- **Python 3**, in a virtualenv for your project.
- **pytest and pytest-bdd.** The plugin's own suite runs on pytest 9.1 with pytest-bdd 8.1. Use those: with
  pytest-bdd 9, `unbuilt:` ids are no longer marked as expected failures (step 7).
- **`gh`, logged in**, for a batch's pull request and a request's issue. You won't need it on this page.
- **Claude Code.**

## 2. Install the plugin and its grammar tools

```console
$ claude plugin marketplace add dstengle/shopsystem-bdd
$ claude plugin install shopsystem-bdd@shopsystem-bdd
```

The commands below run from the plugin's `scripts/` folder. Keep its path in `$SHOP` (step 3 explains this line
and gives the tools short names):

```console
$ export SHOP="$(claude plugin list --json | python3 -c 'import json, sys; print(next(p["installPath"] for p in json.load(sys.stdin) if p["id"] == "shopsystem-bdd@shopsystem-bdd"))')"
```

Make a folder for your project, with its own virtualenv and test tools:

```console
$ mkdir notes && cd notes && git init -b main
$ python3 -m venv .venv && source .venv/bin/activate
$ pip install 'pytest==9.1.1' 'pytest-bdd==8.1.0'
```

The plugin parses requirement lines with GF (the Grammatical Framework) and checks them with clingo. `tools
install` installs both, with the pinned pgf wheel and GF's resource grammar library. On this machine GF and the
library were there already; on a fresh one they're downloaded first.

```console
$ python3 "$SHOP/scripts/tools" install
coverage installed
...
pgf 1.1 installed
clingo 5.8.2 installed
gf 3.12 already installed
gf-rgl 20250812 already installed
```

`tools probe` shows what you have. The block that matters is the last one, `grammar:`:

```console
$ python3 "$SHOP/scripts/tools" probe
...
python: .../notes/.venv/bin/python (the project's virtualenv)
grammar:
  gf 3.12.0 (~/.local/share/shopsystem-bdd/gf-3.12/bin/gf)
  pgf 1.1
  clingo 5.8.2
  gf-rgl 20250812 (~/.local/share/shopsystem-bdd/gf-rgl-20250812)
```

A tool that is missing says so on its line, with what you can't do without it.

## 3. How commands are run

Most days you won't type these commands. You talk with Claude, and Claude runs them from the plugin's `scripts/`
folder. To run one yourself, you need that folder's path, which is why step 2 asked `claude plugin list --json`
for the plugin's `installPath` and kept it in `$SHOP`. It's a path that ends in the version, such as
`~/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.38.0`. If you load a checkout with `claude --plugin-dir`, set `SHOP` to that checkout instead.

Then give each tool a short name:

```console
$ alias work='python3 "$SHOP/scripts/work"' spec='python3 "$SHOP/scripts/spec"' features='python3 "$SHOP/scripts/features"'
$ alias tools='python3 "$SHOP/scripts/tools"' measure='python3 "$SHOP/scripts/measure"' migrate='python3 "$SHOP/scripts/migrate"'
```

Put the `export` and the two `alias` lines in your shell's profile to keep them. The rest of the docs write
commands this way: `work backlog` for `python3 "$SHOP/scripts/work" backlog`.

## 4. The smallest context

A bounded context is one repository's part of a product, with its own words. Its spec lives in `spec/`. You'll use
the example context in [`docs/examples/notes-cli/`](examples/notes-cli/README.md): a notes service the person asks to
add a note, list the notes and remove one, with `notes.py` as its command-line program. Today you write these files by
hand; Claude writes later lines for you.

Copy them in, or type them from below:

```console
$ cp -r "$SHOP/docs/examples/notes-cli/spec" "$SHOP/docs/examples/notes-cli/notes.py" .
```

**`spec/index.md`** names the context, its language and the pack it imports:

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

| area | kind | capabilities |
|---|---|---|
| notes-cli | core | notes |
```

`language: codified-2` says the lines are in the plugin's controlled language. `imports: [request]` brings in the
words every context needs to say a request and its response (*request*, *service*, *refuse*, *name*, *return*,
*keep* ...), so you don't define them.

**`spec/model/notes-cli.md`** is the domain model: the things, their attributes, a lifecycle, and the service with
the operations a person can request of it. No rules here, only the shape:

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

**`spec/vocabulary/notes-cli.md`** and **`shared.md`** give each element of the model its word. A verb that names an
operation is how a line says a request:

```markdown
- **note** (noun) → object note. One short text the person keeps, with a title.
- **add** (verb, action) → operation notes.add. Forms: adds, added. Frame: <actor> adds <note>.
- **the notes service** (proper noun) → service notes. What answers the person's requests about notes.
```

**`spec/capabilities/notes.md`** holds the lines:

```markdown
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
- [r1] When the person adds a note with a title and a tag, the notes service shall keep the note under the tag.

### [g2] A note added without a title is refused
- [r2] If the person adds a note without a title, then the notes service shall refuse the request and name the title.

### [g3] Listing the notes returns every note
- [r3] When the person lists the notes, the notes service shall return every note.

### [g4] Removing a note sets its status to removed
- [r4] When the person removes a note, the notes service shall set the status of the note to `removed`.

## Dropped
```

Each `### [g<n>]` is a group and each `- [r<n>]` a requirement line. No line names a command, an option or an exit
code: those belong to the CLI adapter, **`spec/adapters/cli.toml`**, which maps each operation to the command and
options of `notes.py` (`notes add --title ... --tag ...`). The [capability file reference](reference/capability-file.md)
has every field; [the domain model](reference/domain-model.md) and [adapter contracts](reference/adapters.md) have the
other two forms.

## 5. Ask what the words are, and what a line means

`spec lexicon` lists every word a line may use. The pack's are marked:

```console
$ spec lexicon
actor (2)
  the notes service
  the person
kind (9)
  request  [pack request]
  ...
  note
  tag
attribute (3)
  ...
  status (of note): `kept` (adjective), `removed` (adjective)
event (13)
  refuse  [pack request]
  ...
  add
  list
  remove
```

`spec parse` parses one line. It prints the tree it found:

```console
$ spec parse "When the person removes a note, the notes service shall set the status of the note to \`removed\`."
When NoPre (k_agent_Event (k_agent_One (k_agent_Simple a_the_person_2)) (e_remove_action_13_1 (k_note_One (k_note_Simple (k_note_Det DetA (k_note_UseN k_note_n)))))) (OneResp (k_service_Shall a_the_notes_service_1 (k_service_OneAct (k_service_Act_k_agent PPos (t_status_3_Set (t_status_3_Of_k_note (k_note_Simple (k_note_Det DetThe (k_note_UseN k_note_n)))) t_status_3_v_removed)))))
```

A tree says the line parsed. `--form` says what it means, which is easier to read:

```console
$ spec parse --form "When the person removes a note, the notes service shall set the status of the note to \`removed\`."
shall [x1: agent the person (constant), x3: service the notes service (constant)]
  when [x2: note]
    request(e1, notes.remove, subject: x1, object: x2)
  response
    initiates(e2, subject: x3, status(x2) = `removed`)
```

**When** the person requests `notes.remove` of a note x2, the notes service **shall** set the status of that same x2
to `removed`. Now leave out where the note comes from, and the line is refused (a counter-example):

```console
$ spec parse "When the person removes the note, the notes service shall set the status of the note to \`removed\`."
refused: "the note" has no antecedent: no earlier noun phrase, functional relation or declared indexical gives a note
  tree: ...
```

Which note? The plugin won't guess. [Writing requirements](writing-requirements.md) has more pairs like this.

## 6. Check the spec, and generate the feature

`spec check` holds the whole repository to the design model's rules, and the adapter contract to `notes.py`'s
argparse. Run it now:

```console
$ spec check
v_s3  a group has no scenario  (4)
    capability/example.org/notes/notes-cli/notes#g1
    capability/example.org/notes/notes-cli/notes#g2
    capability/example.org/notes/notes-cli/notes#g3
    capability/example.org/notes/notes-cli/notes#g4
4 violations, 0 warnings, 0 unresolved references, 0 file problems
```

Every group needs a scenario, and there's no feature file yet. Before writing it, `spec logic` checks that no two
lines clash (say, one that keeps a note where another refuses the same request):

```console
$ spec logic
no findings
$ features generate
wrote features/notes.feature
$ spec check
0 violations, 0 warnings, 0 unresolved references, 0 file problems
```

Here's what it wrote, one scenario a group, tagged with the group and its lines:

```gherkin
# generated from spec/capabilities/notes.md by features generate; do not edit
Feature: Notes
  Narrator: the person

  @g1 @r1
  Scenario: A note added with a title and a tag is kept
    Given a note n1
    And a tag t1
    When the person adds the note n1 with a title and the tag t1
    Then the note n1 is under the tag t1
    And the notes service keeps the note n1

  @g2 @r2
  Scenario: A note added without a title is refused
    Given a note n1
    When the person adds the note n1 without a title
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

## 7. Bind the feature, see red, then green

The steps are plain pytest-bdd steps. Every step comes from a small step grammar, and `features vocab` lists its
functions; those that end in `Step` are the shapes a step can take:

```console
$ features vocab | grep -E '^(k_note|k_service)_.*Step$'
k_note_Given : k_note_N -> Name -> Step
k_note_HoldsBlock : k_note_N -> Name -> Step
k_note_HoldsText : k_note_N -> Name -> Quoted -> Step
k_service_Does : Pol -> k_service_Arg -> k_service_V -> Step
...
```

`k_note_Given` is the step "a note n1"; `k_service_Does` is "the notes service keeps the note n1" and every other act
of a service. You'll mostly read the feature file itself. Write `tests/scenarios/test_notes.py`, one step
definition a step text. A When is a request: the step definition makes it through the adapter, here by running
`notes.py` with the command and options `cli.toml` names. A Then reads the response: the exit code, what it printed,
what it kept. The shape of it:

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

pytest-bdd turns the tags `@g1 @r1` into marks; a `pytest.ini` keeps it from warning about them:

```ini
[pytest]
filterwarnings = ignore::pytest.PytestUnknownMarkWarning
```

Run the suite with the plugin's pytest plugin, `-p work_items`, which lives in `$SHOP/scripts`. Take `notes.py` out
of the folder for a moment, as if the code were not written yet, and it's red:

```console
$ PYTHONPATH="$SHOP/scripts" pytest -p work_items -q
FFFF                                                                     [100%]
...
FAILED tests/scenarios/test_notes.py::test_removing_a_note_sets_its_status_to_removed
4 failed in 0.27s
```

That red is honest: the spec is ahead of the code. A capability says so in its `unbuilt:` list, and `-p work_items`
then runs those scenarios as strict expected failures. Put `unbuilt: [r1, r2, r3, r4]` in the frontmatter of
`notes.md` and run again:

```console
$ PYTHONPATH="$SHOP/scripts" pytest -p work_items -q -rx
xxxx                                                                     [100%]
...
XFAIL tests/scenarios/test_notes.py::test_removing_a_note_sets_its_status_to_removed - unbuilt: notes#r4
4 xfailed in 0.27s
```

In your day-to-day, a batch fills `unbuilt:` when it lays new lines and empties it as the code lands. Now put
`notes.py` back. With the ids still listed, each passing scenario fails the suite with `[XPASS(strict)] unbuilt:
notes#r1`: built work must leave `unbuilt:`. Set it back to `unbuilt: []`:

```console
$ PYTHONPATH="$SHOP/scripts" pytest -p work_items -q
....                                                                     [100%]
4 passed in 0.22s
```

Green. Four lines of spec, four scenarios, four passing tests.

## 8. From here, tell Claude what you want

You've done by hand what Claude does for you from now on. Start Claude Code in the repository and say what you
want, in your own words: "listing the notes should give their tags too." Claude shapes an item with lines like the ones
above, checks them, and builds ready items in a batch that ends in one pull request for you to review and merge.

Next:

- [The tour](tour.md): one feature from an idea to a merged batch.
- [Writing requirements](writing-requirements.md): the language, with "this, not that" pairs.
- [The capability file](reference/capability-file.md): every section of these files.
- [Commands](reference/commands.md): every command and its options.
