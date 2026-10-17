---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools
title: Feature file tools
narrator: an agent or session editing feature files
group: service
rests_on: [design-decision/scripts-stdlib-only, design-decision/held-scenarios]
formulated_as: features/feature-file-tools.feature
retired: []
---

# Feature file tools

## Purpose
`scripts/features` reads and edits Gherkin feature files without the test runner: it counts and lists
scenarios by tag or title, retags a scenario's slice, moves a scenario between files and verifies the move,
holds and retires scenarios kept while they still pass, checks and rewrites the titles test modules bind, and
writes the `slice_expectations.py` pytest plugin into a repository. It is not a Gherkin runner and does not run
any test; it edits only the feature files, test modules and directory it is pointed at.

## Behaviour
- [r1] `features` reads every `*.feature` under `--dir` (default `features`), recursively, and text inside a docstring is never taken as a scenario, keyword or tag.
- [r2] **If** a feature file holds a `Rule:` block, `features` refuses, naming the file.
- [r3] **If** an edit would leave a file that `features` cannot read, `features` refuses the edit and leaves every file as it was. `features` reads a file as invalid when it holds a `Rule:` block outside a docstring, and checks nothing else of the result.
- [r4] **When** `features count --by-tag` is run, `features` prints the number of scenarios carrying each tag and a total, counting a Scenario Outline once per Examples row and giving each scenario its feature's tags and its Examples table's tags. The total counts every scenario, those carrying no tag included.
- [r5] **When** `features list --tag <tag>` is run, `features` prints the file and title of each scenario whose tags, its feature's and its Examples' included, hold that tag.
- [r6] **When** `features list --title <text>` is run, `features` prints the file and title of each scenario whose title contains the text.
- [r7] **If** `features list` matches no scenario, `features` prints nothing and exits 1.
- [r8] **When** `features tag <title> <slice>` is run on a title exactly one file holds, `features` makes the scenario's first slice tag the new one, removes any further slice tags, and leaves its other tags and every other line unchanged.
- [r9] **Where** the scenario has no slice tag, **when** `features tag` is run, `features` adds the new slice tag to the scenario's last tag line, or on a tag line of its own above the scenario when it has none.
- [r10] **If** `features tag` is given a title no file holds, or one several files hold, `features` refuses, naming every file that holds it, and changes no file.
- [r11] **If** `features tag` is given a tag not written `slice-<n>`, `slice-<n>.<m>` or `r<n>`, `features` exits 2 as bad usage and changes no file.
- [r12] **When** `features move <title> --to <file>` is run, `features` removes the scenario's block from its file and appends it unchanged to the end of the destination file.
- [r13] **Where** `--inline-background` is given, **when** `features move` is run, `features` puts the source Background's steps before the moved scenario's first step.
- [r14] **Where** `--carry-feature-tags` is given, **when** `features move` is run, `features` puts the source's feature tags that the destination's feature tags lack on a tag line of their own immediately above the moved scenario's `Scenario:` line, after any tag line the scenario already has, and joins them to none.
- [r15] **If** the destination of `features move` does not exist, `features` refuses and changes no file.
- [r16] **When** `features verify-moved --from <dir>` finds every scenario in the two trees alike by title in its effective tags, description, and Background and own steps, `features` prints how many scenarios match and exits 0.
- [r17] **If** a scenario's effective tags, description or steps differ between the two trees, `features verify-moved` names the scenario and which of them changed, and exits 1.
- [r18] **If** a title is held by more than one scenario in either tree, `features verify-moved` names the title as a duplicate and exits 1.
- [r19] **When** `features hold <title> --for <new title>` or `--for-removal` is run, `features` gives the scenario the tag `@holding`, " (held)" at the end of its title and a description line naming what it is held for, and changes nothing else in it, whether or not the replacement exists yet.
- [r20] **If** `features hold` is given a scenario already tagged `@holding`, `features` refuses it.
- [r21] **When** `features holding` is run, `features` lists each held scenario with what it is held for and the slice tag its replacement carries, or says that no scenario has the replacement's title, or that the slice removing the behaviour retires it.
- [r22] **When** `features holding` is run and no scenario is held, `features` says none is held.
- [r23] **When** `features retire <title>` is run on a scenario tagged `@holding`, `features` removes that scenario's block and leaves the rest of the file as it was.
- [r24] **If** `features retire` is given a scenario not tagged `@holding`, `features` refuses because it is not held, and leaves the file as it was.
- [r25] **When** `features bindings` finds a `scenario(<feature>, "<title>")` call under `--tests` (default `tests`) whose title no feature file has, or not the feature it names, `features` reports the module, line, title and feature of each, and exits 1.
- [r26] **When** `features bindings` finds every binding names a scenario, `features` says so and exits 0.
- [r27] **If** a test module under `--tests` does not parse, `features bindings` and `features rebind` refuse, naming the module.
- [r28] **When** `features rebind <old> <new>` is run, `features` rewrites `<old>` to `<new>` in each binding call that names it, changes nothing else in the module, and prints how many bindings it rebound, zero included.
- [r29] **If** `features rebind` is given a new title that is no scenario in a feature file, `features` refuses and changes no test module.
- [r30] **When** `features plugin <directory>` is run, `features` writes `slice_expectations.py` into the directory and prints the line that registers it in the `conftest.py` beside it.
- [r31] **Where** `slice_expectations.py` is registered and one living plan is found, a test tagged to a slice the plan has as planned or blocked is expected to fail: its failure is reported as expected, its pass fails the run, and the run reports how many tests of which slices were expected to fail.
- [r32] **Where** `slice_expectations.py` is registered, a test tagged to a slice that is in progress, green or no longer in the plan runs as it is.
- [r33] **Where** `--slice <n>` is given to pytest, `slice_expectations.py` runs that slice's tests as they are.
- [r34] **Where** no one living plan is found, `slice_expectations.py` expects no test to fail and the run says so.
- [r35] **If** `features move`, `features hold` or `features retire` is given a title no file holds, or one several files hold, `features` refuses, naming every file that holds it, and changes no file.
- [r36] **If** the destination of `features move` is the scenario's own file, `features` refuses and changes no file.
- [r37] **If** a title is in the `--from` tree and not the other, or in the other tree and not `--from`, `features verify-moved` names it as missing or as added, and exits 1.
- [r38] `features list --tag` finds the tag whether it is given with its leading `@` or without.
- [r39] **When** `features hold` has held a scenario, `features` prints its file and its new title.
- [r40] **When** `features holding` finds a held scenario with no `Held for:` line, or whose replacement carries no slice tag, `features` says so on that scenario's line.
- [r41] **If** `features rebind` is given a new title that several feature files hold, `features` refuses and changes no test module.
- [r42] **If** a binding call names the old title of `features rebind` in a string written over several lines, `features` refuses, naming the module and line, and changes no test module.
- [r43] **If** `features plugin` is given a path that is not a directory, `features` refuses and writes nothing.
- [r44] **When** `features plugin` is run, `features` writes over any `slice_expectations.py` already in the directory, and reads no feature file.
- [r45] **Where** the directory given to `features plugin` holds an `__init__.py`, the line `features plugin` prints imports `slice_expectations` relative to the package.
- [r46] **If** `features` refuses a command or an edit, it says why on stderr and exits 1.
- [r47] `slice_expectations.py` reads as the living plan the file the ini value `slice_plan` names under pytest's root directory, or else the one `docs/superpowers/plans/*-slices.md` under it, and finds none when there are none or several.
- [r48] **Where** `--slice` is given to pytest more than once, `slice_expectations.py` runs the tests of every slice named, each written `<n>` or `slice-<n>`, as they are.
- [r49] **Where** `slice_expectations.py` is registered, the run's header names the living plan it read, relative to the root directory, or says no one living plan was found.
- [r50] **If** the ini value `slice_plan` names a file that does not exist, `slice_expectations.py` expects no test to fail, and the run's header names that file.
- [r51] **When** `features tag <title> r<n>` is run on a title exactly one file holds, `features` makes `@r<n>` the scenario's one requirement tag, removing any other `@r<m>` tag it has, and leaves its other tags and every other line unchanged.

## Implementation, may change
- Gherkin is parsed line by line, not by a Gherkin library. A docstring opens and closes on `"""` or three
  backticks. A scenario's block is its tag lines, its `Scenario:` line and everything up to the next
  scenario's tag lines; `move` drops the block's trailing blank lines.
- `tag` and `hold` add to the last tag line; a new tag line takes the scenario's indentation. Background steps
  inlined by `move` take the scenario's step indentation; carried feature tags take the `Scenario:` line's.
- `verify-moved` compares lines stripped of indentation, blank lines and comments, and also reports titles
  missing from or added to the second tree.
- `move` also refuses a destination that is the scenario's own file.
- `hold` writes the description line as `Held for: <title>` or `Held for: removal`, indented like the
  scenario's first following line.
- `bindings` reads only a title written as a plain string in the call; a feature given as a name is looked up
  among the module's own top-level assignments. `rebind` refuses a title written over several lines.
- Output lines: `list` prints `<path>: <title>`; `holding` prints `<path>: <title> | for: <what> | <slice tags>`
  or `none held`; `bindings` prints `<path>:<line>: no scenario titled "<title>" in <feature>`.
- `plugin` prints `from slice_expectations import *` (with a leading `.` when the directory is a package) and
  says the plugin is registered when `python -m pytest --help` lists `--slice`.
- `slice_expectations.py` finds the plan as the one `docs/superpowers/plans/*-slices.md` under pytest's root
  directory, or the ini value `slice_plan`; it marks waiting tests `xfail(strict=True)` and reads each slice's
  `- Status:` word.
- Exit status: 0 success, 1 a check failed or an edit was refused, 2 bad usage.

## Not yet
- `Rule:` blocks are refused rather than parsed — trigger: a feature file needs a `Rule:`.
