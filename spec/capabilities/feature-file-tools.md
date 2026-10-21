---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools
title: Feature file tools
narrator: a session editing feature files
group: service
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs, design-decision/held-scenarios, design-decision/plugin-scenarios-run-as-pytest-bdd]
retired: [r3, r6, r8, r9, r10, r11, r15, r18, r20, r22, r27, r30, r31, r32, r33, r34, r36, r37, r38, r39, r40, r41, r42, r43, r44, r45, r47, r48, r49, r50, r53, r54, r55, r59]
---

# Feature file tools

## Purpose
`scripts/features` reads and edits Gherkin feature files without the test runner: it counts and lists
scenarios by tag or title, adds a requirement tag to a scenario, takes a scenario from one file to another and verifies
it arrived unchanged, deprecates and retires scenarios kept while they still pass, verifies that every scenario has exactly one
test binding it and rewrites the titles test modules bind. It is not a Gherkin runner and does not run any
test; it edits only the feature files, test modules and directory it is pointed at.

## Behaviour
- [r1] The `features` script shall read every `*.feature` under `--dir` (default `features`), recursively, never taking text inside a docstring as a scenario, keyword or tag.
- [r52] **Where** `--file <path>` is given, the `features` script shall look for the scenario's title in that file only, whatever the command.
- [r46] **If** `features` cannot do what it was asked, then `features` shall exit non-zero, say why on stderr, and change nothing.
- [r2] **If** a feature file contains a `Rule:` block outside a docstring, or an edit would leave one, then `features` shall refuse, naming the file, and leave every file as it was.
- [r35] **If** the title given to `features tag`, `move`, `deprecate` or `retire` is in no file, is in several without `--file`, is not exactly once in the file `--file` names, or `--file` or `--to` names a file outside `--dir`, then `features` shall refuse, naming each file that has the title, and change no file.

### Reading
- [r4] **When** `features count --by-tag` is run, `features` shall print the number of scenarios with each tag and a total of every scenario, those with no tag included, counting a Scenario Outline once per Examples row and giving each scenario its feature's tags and its Examples table's tags.
- [r5] **When** `features list --tag <tag>` or `--title <text>` is run, `features` shall print the file and title of each scenario whose tags, its feature's and its Examples' included, include that tag, or whose title contains the text.
- [r7] **When** `features list` matches no scenario, `features` shall print nothing and exit 1.

### Editing
- [r51] **When** `features tag <title> r<n>` is run, `features` shall add `@r<n>` to the scenario's requirement tags and leave its other tags, its other `@r<m>` tags included, and every other line unchanged.
- [r12] **When** `features move <title> --to <file>` is run, `features` shall take the scenario's block unchanged from its file to the end of the destination file.
- [r13] **Where** `--inline-background` is given, **when** `features move` is run, `features` shall put the source Background's steps before the relocated scenario's first step.
- [r14] **Where** `--keep-feature-tags` is given, **when** `features move` is run, `features` shall put the source's feature tags that the destination's feature tags lack on a tag line of their own immediately above the relocated scenario's `Scenario:` line, after any tag line the scenario already has, joined to none.
- [r19] **When** `features deprecate <title>` is run with `--for <new title>` or `--for-removal`, `features` shall give the scenario the tag `@deprecated`, " (deprecated)" at the end of its title and a description line `Deprecated for: <new title>` or `Deprecated for: removal`, whether or not the replacement exists yet, and change nothing else in it.
- [r21] **When** `features deprecated` is run, `features` shall list each deprecated scenario with what it is deprecated for and, for a replacement, the file and `@r<n>` tag of the scenario with that title, saying on its line when it has no `Deprecated for:` line, no scenario has the replacement's title, or the replacement has no `@r<n>` tag.
- [r23] **When** `features retire <title>` is run on a scenario tagged `@deprecated`, `features` shall remove that scenario's block and leave the rest of the file as it was.
- [r24] **If** `features retire` is given a scenario not tagged `@deprecated`, then `features` shall refuse because it is not deprecated, and leave the file as it was.

### Verifying `features move` and bindings
- [r16] **When** `features verify-moved --from <dir>` finds every scenario in the two trees alike by title in its effective tags, description, and Background and own steps, `features` shall print how many scenarios match and exit 0.
- [r17] **If** `features verify-moved` finds a scenario whose effective tags, description or steps differ between the two trees, a title used by more than one scenario in either tree, or a title in one tree and not the other, then `features verify-moved` shall name each, as changed (with what changed), duplicate, missing or added, and exit 1.
- [r57] `features bindings` shall read a `scenarios(<path>, ...)` call under `--tests` as binding every scenario of each feature file it names, and of every feature file under a directory it names.
- [r25] **If** `features bindings` finds a `scenario(<feature>, "<title>")` call under `--tests` (default `tests`) whose title no feature file has, or not the feature it names, then `features` shall print the module, line, title and feature of each, and exit 1.
- [r26] **When** `features bindings` finds every binding names a scenario, `features` shall say so and exit 0.
- [r58] **Where** `--unbound` is given, **if** a scenario in the feature files named after `--unbound` (with none named, every feature file under `--dir`) is bound by no `scenario(...)` or `scenarios(...)` call, or by more than one, then `features bindings` shall print its file and title, with the module and line of each call, and exit 1.
- [r28] **When** `features rebind <old> <new>` is run, `features` shall rewrite `<old>` to `<new>` in each binding call that names it and change nothing else in the module.
- [r56] **Where** `--file <feature path>` is given, **when** `features rebind` is run, `features` shall rewrite only the bindings whose feature argument names that file, the feature argument resolved against `--dir`.
- [r29] **If** the new title given to `features rebind` is no scenario's or several feature files', or a binding call names the old title in a string written over several lines, then `features` shall refuse and change no test module.

## Implementation, may change
- Gherkin is parsed line by line, not by a Gherkin library. A docstring opens and closes on `"""` or three
  backticks. A scenario's block is its tag lines, its `Scenario:` line and everything up to the next
  scenario's tag lines; `move` drops the block's trailing blank lines.
- An edit's output is verified for nothing but a `Rule:` block outside a docstring.
- `tag` adds the `@r<n>` tag to the scenario's last tag line; `deprecate` adds to the last
  tag line; a new tag line takes the scenario's indentation. Background steps inlined by `move` take the
  scenario's step indentation; kept feature tags take the `Scenario:` line's.
- `verify-moved` compares lines stripped of indentation, blank lines and comments; a title only in `--from` is
  missing, one only in the other tree is added.
- `deprecate` writes the description line as `Deprecated for: <title>` or `Deprecated for: removal`, indented
  like the scenario's first following line, and prints the scenario's file and new title.
- `list --tag` takes the tag with its leading `@` or without.
- `rebind` prints how many bindings it rebound, zero included, and names the module and line of a title written
  over several lines; without `--file` it rewrites every binding of the old title.
- Refusals under r46 include: a `tag` argument not written `r<n>` (exit 2, bad usage), a `move` destination that
  does not exist or is the scenario's own file, `deprecate` on a scenario already tagged `@deprecated`, and a test
  module under `--tests` that does not parse (named), for `bindings` and `rebind`.
- `bindings` reads only a title written as a plain string in the call; a feature given as a name is looked up
  among the module's own top-level assignments. A `scenario` or `scenarios` path names a feature file by its
  base name, as it does today, or a directory by every feature file under it.
- Output lines: `list` prints `<path>: <title>`; `deprecated` prints
  `<path>: <title> | for: <what> | <replacement's path> @r<n>` or `none deprecated`; `bindings` prints
  `<path>:<line>: no scenario titled "<title>" in <feature>`, and with `--unbound`
  `<feature path>: <title> | bound by no test` or `<feature path>: <title> | bound by <module>:<line>, <module>:<line>`.
- Exit code: 0 success, 1 a verification failed or an edit was refused, 2 bad usage.

## Not yet
- `Rule:` blocks are refused rather than parsed — trigger: a feature file needs a `Rule:`.
