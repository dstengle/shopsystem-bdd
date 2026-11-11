<!--
Outputs on this page are from real runs on 2026-11-10: plugin 4.0.0, its scripts as at commit 7f60e57de
(branch plan-docs), Python 3.11, pytest 9.1.1, pytest-bdd 8.1.0, in a scratch repository built from
docs/examples/notes-cli/. The home directory is written as ~, and long paths are cut with "...".
-->

# Getting started

This page takes you from an empty folder to a first green scenario. It's written for the developer setting up a
repository. You'll write a tiny spec for a notes tool, let the plugin check it and turn it into Gherkin, bind the
scenarios with pytest-bdd, and watch them go from red to green.

Here is where you're heading. You write one line like this:

```markdown
- [r4] When the person runs `notes remove` on a note, `notes` shall delete the note.
```

and the plugin writes its test scenario for you:

```gherkin
Feature: Notes
  Narrator: the person

  @g4 @r4
  Scenario: `notes remove` deletes a note
    Given a note n1
    When the person runs `notes remove` on the note n1
    Then `notes` deletes the note n1
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
`~/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/4.1.0`. If you load a checkout with `claude --plugin-dir`, set `SHOP` to that checkout instead.

Then give each tool a short name:

```console
$ alias work='python3 "$SHOP/scripts/work"' model='python3 "$SHOP/scripts/model"' features='python3 "$SHOP/scripts/features"'
$ alias tools='python3 "$SHOP/scripts/tools"' measure='python3 "$SHOP/scripts/measure"' migrate='python3 "$SHOP/scripts/migrate"'
```

Put the `export` and the two `alias` lines in your shell's profile to keep them. The rest of the docs write
commands this way: `work backlog` for `python3 "$SHOP/scripts/work" backlog`.

## 4. The smallest context

A bounded context is one repository's part of a product, with its own words. Its spec lives in `spec/`. You'll use
the example context in [`docs/examples/notes-cli/`](examples/notes-cli/README.md): a notes tool with `notes add`,
`notes list` and `notes remove`. Today you write these files by hand; Claude writes later lines for you.

Copy them in, or type them from below:

```console
$ cp -r "$SHOP/docs/examples/notes-cli/spec" .
```

**`spec/index.md`** names the context, its language and its words:

```markdown
---
id: bounded-context/example.org/notes/notes-cli
title: notes
language: codified-2
imports: [cli]
---

# notes

## Purpose

A command-line tool that keeps short notes in one file: `notes add` writes a note, `notes list` prints them and
`notes remove` deletes one. It is not an editor and not a sync service.

## Relations

| from | word | to | cardinality |
|---|---|---|---|
| note | under | tag | many |
| title | of | note | one |

## Glossary

- **the person** (proper noun): the human at the terminal. Kind of: agent.
- **`notes`** (proper noun): the notes tool. Kind of: tool.
- **note** (noun): one short text the person keeps, with a title.
- **title** (noun): the one line that names a note.
- **tag** (noun): a word the person files a note under.
- **file** (noun): the one file on disk where `notes` keeps every note.
- **add** (verb, action): a tool keeps a new thing. Frame: tool adds note.
- **delete** (verb, action): a tool removes a thing for good. Frame: tool deletes note.
```

`language: codified-2` says the lines are in the plugin's controlled language. `imports: [cli]` brings in the
words every command-line tool needs (*command*, *option*, *run*, *print*, *refuse* ...), so you don't define them.
A `Frame:` says who does a verb to what: only a tool adds, and what it adds is a note.

**`spec/capabilities/notes.md`** is one capability: a set of things the tool does, in groups of lines.

````markdown
---
id: capability/example.org/notes/notes-cli/notes
title: Notes
narrator: the person
group: service
language: codified-2
rests_on: []
retired: []
unbuilt: []
---

# Notes

## Purpose

Adding, listing and removing notes.

## Behaviour

### [g1] `notes add` adds a note under a tag
- [r1] When the person runs `notes add` with the `--title` option and the `--tag` option, `notes` shall add a note under a tag and exit successfully.

### [g2] `notes add` refuses a note with no title
- [r2] If the person runs `notes add` without the `--title` option, then `notes` shall refuse the command and name `--title`.

### [g3] `notes list` prints every note
- [r3] When the person runs `notes list`, `notes` shall print the title of every note.

```given
the file `notes.json` holds:
  [{"title": "Buy milk", "tags": ["home"]},
   {"title": "Call the bank", "tags": []}]
```

### [g4] `notes remove` deletes a note
- [r4] When the person runs `notes remove` on a note, `notes` shall delete the note.

## Dropped
````

Each `### [g<n>]` is a group and each `- [r<n>]` a requirement line. The `given` block holds g3's sample data, so
the line itself stays free of it. The [capability file reference](reference/capability-file.md) has every field.

## 5. Ask what the words are, and what a line means

`model lexicon` lists every word a line may use. The pack's are marked:

```console
$ model lexicon
actor (2)
  the person
  `notes`
kind (10)
  tool  [pack cli]
  ...
  note
  title
  tag
  file
event (9)
  run  [pack cli]
  ...
  add
  delete
```

`model parse` parses one line. It prints the tree it found:

```console
$ model parse "When the person runs \`notes remove\` on a note, \`notes\` shall delete the note."
When NoPre (k_agent_Event (k_agent_One (k_agent_Simple a_the_person_1)) (e_run_action_1_3 (k_command_One (k_command_Code (CodeLit "`notesremove`"))) (k_thing_One (k_note_Up_k_thing (k_note_Det DetA (k_note_UseN k_note_n)))))) (OneResp (k_tool_Shall a_notes_2 (k_tool_OneAct (k_tool_Act_k_tool PPos (e_delete_action_9_1 (k_note_One (k_note_Simple (k_note_Det DetThe (k_note_UseN k_note_n)))))))))
```

A tree says the line parsed. `--form` says what it means, which is easier to read:

```console
$ model parse --form "When the person runs \`notes remove\` on a note, \`notes\` shall delete the note."
shall [x1: agent the person (constant), x2: command `notes remove` (parameter), x4: tool `notes` (constant)]
  when [x3: note]
    run(e1, subject: x1, object: x2, on: x3)
  response
    delete(e2, subject: x4, object: x3)
```

**When** the person runs `notes remove` on a note x3, `notes` **shall** delete that same x3. Now leave out where
the note comes from, and the line is refused (a counter-example):

```console
$ model parse "When the person runs \`notes remove\`, \`notes\` shall delete the note."
refused: "the note" has no antecedent: no earlier noun phrase, functional relation or declared indexical gives a note
  tree: ...
```

Which note? The plugin won't guess. [Writing requirements](writing-requirements.md) has more pairs like this.

## 6. Check the spec, and generate the feature

`model check` holds the whole repository to the design model's rules. Run it now:

```console
$ model check
v_s3  a group has no scenario  (4)
    capability/example.org/notes/notes-cli/notes#g1
    capability/example.org/notes/notes-cli/notes#g2
    capability/example.org/notes/notes-cli/notes#g3
    capability/example.org/notes/notes-cli/notes#g4
4 violations, 0 warnings, 0 unresolved references, 0 file problems
```

Every group needs a scenario, and there's no feature file yet. Before writing it, `model logic` checks that no two
lines clash (say, one that adds where another refuses):

```console
$ model logic
no findings
$ features generate
wrote features/notes.feature
$ model check
0 violations, 0 warnings, 0 unresolved references, 0 file problems
```

Here's what it wrote, one scenario a group, tagged with the group and its lines:

```gherkin
# generated from spec/capabilities/notes.md by features generate; do not edit
Feature: Notes
  Narrator: the person

  @g1 @r1
  Scenario: `notes add` adds a note under a tag
    When the person runs `notes add` with the `--title` and `--tag` options
    Then the note n1 is under the tag t1
    And `notes` adds the note n1
    And `notes` exits successfully

  @g2 @r2
  Scenario: `notes add` refuses a note with no title
    When the person runs `notes add` without the `--title` option
    Then `notes` refuses `notes add`
    And `notes` names the `--title` option

  @g3 @r3
  Scenario: `notes list` prints every note
    Given the file `notes.json` holds:
      """
      [{"title": "Buy milk", "tags": ["home"]},
       {"title": "Call the bank", "tags": []}]
      """
    And a note n1
    And a note n2
    When the person runs `notes list`
    Then the note n1 has the title t1
    And `notes` prints the title t1
    And the note n2 has the title t2
    And `notes` prints the title t2

  @g4 @r4
  Scenario: `notes remove` deletes a note
    Given a note n1
    When the person runs `notes remove` on the note n1
    Then `notes` deletes the note n1
```

You never edit this file. When a line changes, `features generate` writes it again; `features generate --check`
says whether it is current. Names like `n1` and `t1` stand for the things a line talks about. "Every note" became
two notes, since a scenario can't test every note there is.

## 7. Bind the feature, see red, then green

The steps are plain pytest-bdd steps. Every step comes from a small step grammar, and `features vocab` lists its
functions; those that end in `Step` are the shapes a step can take:

```console
$ features vocab | grep -E '^(k_note|k_tool)_.*Step$'
k_note_Given : k_note_N -> Name -> Step
k_note_HoldsBlock : k_note_N -> Name -> Step
k_note_HoldsText : k_note_N -> Name -> Quoted -> Step
k_tool_Does : Pol -> k_tool_Arg -> k_tool_V -> Step
...
```

`k_note_Given` is the step "a note n1"; `k_tool_Does` is "`notes` deletes the note n1" and every other act of a
tool. Every step of the feature is one of these shapes. You'll mostly read the feature file itself. Write `tests/scenarios/test_notes.py`, one step definition a step
text. The shape of it:

```python
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("../../features/notes.feature")


@given(parsers.parse("a note {n}"))
def a_note(world, n):
    if len(saved(world)) <= len(world["names"]):
        notes(world, "add", "--title", "Note " + n)
    world["names"][n] = saved(world)[len(world["names"])]["title"]


@when(parsers.parse("the person runs `notes remove` on the note {n}"))
def remove(world, n):
    notes(world, "remove", world["names"][n])


@then(parsers.parse("`notes` deletes the note {n}"))
def deletes(world, n):
    assert world["run"].returncode == 0
    assert world["names"][n] not in [note["title"] for note in saved(world)]
```

<details>
<summary>The whole file (99 lines)</summary>

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
    return {"dir": tmp_path, "names": {}}


def notes(world, *args):
    world["run"] = subprocess.run([sys.executable, NOTES, *args], cwd=world["dir"],
                                  capture_output=True, text=True)
    return world["run"]


def saved(world):
    path = world["dir"] / "notes.json"
    return json.loads(path.read_text()) if path.exists() else []


@given(parsers.parse("the file `{name}` holds:"))
def file_holds(world, name, docstring):
    (world["dir"] / name).write_text(docstring)


@given(parsers.parse("a note {n}"))
def a_note(world, n):
    if len(saved(world)) <= len(world["names"]):
        notes(world, "add", "--title", "Note " + n)
    world["names"][n] = saved(world)[len(world["names"])]["title"]


@when("the person runs `notes add` with the `--title` and `--tag` options")
def add_with_tag(world):
    notes(world, "add", "--title", "Buy milk", "--tag", "home")


@when("the person runs `notes add` without the `--title` option")
def add_without_title(world):
    notes(world, "add", "--tag", "home")


@when("the person runs `notes list`")
def list_notes(world):
    notes(world, "list")


@when(parsers.parse("the person runs `notes remove` on the note {n}"))
def remove(world, n):
    notes(world, "remove", world["names"][n])


@then(parsers.parse("the note {n} is under the tag {t}"))
def under_tag(world, n, t):
    assert saved(world)[-1]["tags"] == ["home"]


@then(parsers.parse("`notes` adds the note {n}"))
def adds(world, n):
    assert world["run"].returncode == 0 and saved(world)[-1]["title"] == "Buy milk"


@then(parsers.parse("`notes` deletes the note {n}"))
def deletes(world, n):
    assert world["run"].returncode == 0
    assert world["names"][n] not in [note["title"] for note in saved(world)]


@then("`notes` exits successfully")
def exits_ok(world):
    assert world["run"].returncode == 0


@then("`notes` refuses `notes add`")
def refuses(world):
    assert world["run"].returncode != 0


@then(parsers.parse("`notes` names the `{option}` option"))
def names_option(world, option):
    assert option in world["run"].stderr


@then(parsers.parse("the note {n} has the title {t}"))
def has_title(world, n, t):
    world["names"][t] = world["names"][n]


@then(parsers.parse("`notes` prints the title {t}"))
def prints_title(world, t):
    assert world["names"][t] in world["run"].stdout
```

</details>

pytest-bdd turns the tags `@g1 @r1` into marks; a `pytest.ini` keeps it from warning about them:

```ini
[pytest]
filterwarnings = ignore::pytest.PytestUnknownMarkWarning
```

Run the suite with the plugin's pytest plugin, `-p work_items`, which lives in `$SHOP/scripts`. There's no
`notes.py` yet, so it's red:

```console
$ PYTHONPATH="$SHOP/scripts" pytest -p work_items -q
FFFF                                                                     [100%]
...
FAILED tests/scenarios/test_notes.py::test_notes_remove_deletes_a_note - asse...
4 failed in 0.20s
```

That red is honest: the spec is ahead of the code. A capability says so in its `unbuilt:` list, and `-p work_items`
then runs those scenarios as strict expected failures. Put `unbuilt: [r1, r2, r3, r4]` in the frontmatter of
`notes.md` and run again:

```console
$ PYTHONPATH="$SHOP/scripts" pytest -p work_items -q -rx
xxxx                                                                     [100%]
...
XFAIL tests/scenarios/test_notes.py::test_notes_remove_deletes_a_note - unbuilt: notes#r4
4 xfailed in 0.23s
```

In your day-to-day, a batch fills `unbuilt:` when it lays new lines and empties it as the code lands. Now write
`notes.py`, a small argparse tool that keeps `notes.json`. With the ids still listed, each passing scenario fails
the suite with `[XPASS(strict)] unbuilt: notes#r1`: built work must leave `unbuilt:`. Set it back to
`unbuilt: []`:

```console
$ PYTHONPATH="$SHOP/scripts" pytest -p work_items -q
....                                                                     [100%]
4 passed in 0.22s
```

Green. Four lines of spec, four scenarios, four passing tests.

## 8. From here, tell Claude what you want

You've done by hand what Claude does for you from now on. Start Claude Code in the repository and say what you
want, in your own words: "`notes list` should print the tags too." Claude shapes an item with lines like the ones
above, checks them, and builds ready items in a batch that ends in one pull request for you to review and merge.

Next:

- [The tour](tour.md): one feature from an idea to a merged batch.
- [Writing requirements](writing-requirements.md): the language, with "this, not that" pairs.
- [The capability file](reference/capability-file.md): every section of these files.
- [Commands](reference/commands.md): every command and its options.
