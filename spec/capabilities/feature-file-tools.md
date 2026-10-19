---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools
title: Feature file tools
narrator: an agent or session editing feature files
group: service
rests_on: [design-decision/plugin-takes-the-dependencies-it-needs, design-decision/held-scenarios, design-decision/plugin-scenarios-run-as-pytest-bdd]
retired: [r8, r9, r30, r31, r32, r33, r34, r43, r44, r45, r47, r48, r49, r50]
---

# Feature file tools

## Purpose
`scripts/features` reads and edits Gherkin feature files without the test runner: it counts and lists
scenarios by tag or title, sets a scenario's requirement tag, moves a scenario between files and verifies the
move, deprecates and retires scenarios kept while they still pass, checks that every scenario has exactly one
test binding it and rewrites the titles test modules bind. It is not a Gherkin runner and does not run any
test; it edits only the feature files, test modules and directory it is pointed at.

## Behaviour
- [r1] `features` reads every `*.feature` under `--dir` (default `features`), recursively, and text inside a docstring is never taken as a scenario, keyword or tag.
- [r2] **If** a feature file contains a `Rule:` block, `features` refuses, naming the file.
- [r3] **If** an edit would leave a file that `features` cannot read, `features` refuses the edit and leaves every file as it was. `features` reads a file as invalid when it contains a `Rule:` block outside a docstring, and checks nothing else of the result.
- [r4] **When** `features count --by-tag` is run, `features` prints the number of scenarios with each tag and a total, counting a Scenario Outline once per Examples row and giving each scenario its feature's tags and its Examples table's tags. The total counts every scenario, those with no tag included.
- [r5] **When** `features list --tag <tag>` is run, `features` prints the file and title of each scenario whose tags, its feature's and its Examples' included, include that tag.
- [r6] **When** `features list --title <text>` is run, `features` prints the file and title of each scenario whose title contains the text.
- [r7] **If** `features list` matches no scenario, `features` prints nothing and exits 1.
- [r10] **If** `features tag` is given a title no file has, or one several files have, `features` refuses, naming every file that has it, and changes no file.
- [r11] **If** `features tag` is given a tag not written `r<n>`, `features` exits 2 as bad usage and changes no file.
- [r12] **When** `features move <title> --to <file>` is run, `features` removes the scenario's block from its file and appends it unchanged to the end of the destination file.
- [r13] **Where** `--inline-background` is given, **when** `features move` is run, `features` puts the source Background's steps before the moved scenario's first step.
- [r14] **Where** `--keep-feature-tags` is given, **when** `features move` is run, `features` puts the source's feature tags that the destination's feature tags lack on a tag line of their own immediately above the moved scenario's `Scenario:` line, after any tag line the scenario already has, and joins them to none.
- [r15] **If** the destination of `features move` does not exist, `features` refuses and changes no file.
- [r16] **When** `features verify-moved --from <dir>` finds every scenario in the two trees alike by title in its effective tags, description, and Background and own steps, `features` prints how many scenarios match and exits 0.
- [r17] **If** a scenario's effective tags, description or steps differ between the two trees, `features verify-moved` names the scenario and which of them changed, and exits 1.
- [r18] **If** a title is used by more than one scenario in either tree, `features verify-moved` names the title as a duplicate and exits 1.
- [r19] **When** `features deprecate <title> --for <new title>` or `--for-removal` is run, `features` gives the scenario the tag `@deprecated`, " (deprecated)" at the end of its title and a description line `Deprecated for: <new title>` or `Deprecated for: removal`, and changes nothing else in it, whether or not the replacement exists yet.
- [r20] **If** `features deprecate` is given a scenario already tagged `@deprecated`, `features` refuses it.
- [r21] **When** `features deprecated` is run, `features` lists each deprecated scenario with what it is deprecated for and, for a replacement, the file and `@r<n>` tag of the scenario with that title, or says that no scenario has the replacement's title, or that the scenario is deprecated for removal.
- [r22] **When** `features deprecated` is run and no scenario is deprecated, `features` says none is deprecated.
- [r23] **When** `features retire <title>` is run on a scenario tagged `@deprecated`, `features` removes that scenario's block and leaves the rest of the file as it was.
- [r24] **If** `features retire` is given a scenario not tagged `@deprecated`, `features` refuses because it is not deprecated, and leaves the file as it was.
- [r25] **When** `features bindings` finds a `scenario(<feature>, "<title>")` call under `--tests` (default `tests`) whose title no feature file has, or not the feature it names, `features` reports the module, line, title and feature of each, and exits 1.
- [r26] **When** `features bindings` finds every binding names a scenario, `features` says so and exits 0.
- [r27] **If** a test module under `--tests` does not parse, `features bindings` and `features rebind` refuse, naming the module.
- [r28] **When** `features rebind <old> <new>` is run, `features` rewrites `<old>` to `<new>` in each binding call that names it, changes nothing else in the module, and prints how many bindings it rebound, zero included.
- [r29] **If** `features rebind` is given a new title that is no scenario in a feature file, `features` refuses and changes no test module.
- [r35] **If** `features move`, `features deprecate` or `features retire` is given a title no file has, or, without `--file`, one several files have, `features` refuses, naming every file that has it, and changes no file.
- [r36] **If** the destination of `features move` is the scenario's own file, `features` refuses and changes no file.
- [r37] **If** a title is in the `--from` tree and not the other, or in the other tree and not `--from`, `features verify-moved` names it as missing or as added, and exits 1.
- [r38] `features list --tag` finds the tag whether it is given with its leading `@` or without.
- [r39] **When** `features deprecate` has deprecated a scenario, `features` prints its file and its new title.
- [r40] **When** `features deprecated` finds a deprecated scenario with no `Deprecated for:` line, or whose replacement has no `@r<n>` tag, `features` says so on that scenario's line.
- [r41] **If** `features rebind` is given a new title that several feature files have, `features` refuses and changes no test module.
- [r42] **If** a binding call names the old title of `features rebind` in a string written over several lines, `features` refuses, naming the module and line, and changes no test module.
- [r46] **If** `features` refuses a command or an edit, it says why on stderr and exits 1.
- [r51] **When** `features tag <title> r<n>` is run on a title exactly one file has, `features` makes `@r<n>` the scenario's one requirement tag, removing any other `@r<m>` tag it has, and leaves its other tags and every other line unchanged.
- [r52] **Where** `--file <path>` is given, the `features` script looks for the scenario's title in that file only, whatever the command.
- [r53] **If** `--file` names a file that does not have the title, `features` refuses, naming the file, and changes no file.
- [r54] **If** `--file` names a file that has the title twice, `features` refuses, naming the file, and changes no file.
- [r55] **If** `--file` names a file outside `--dir`, `features` refuses and changes no file.
- [r56] **Where** `--file <feature path>` is given, **when** `features rebind` is run, `features` rewrites only the bindings whose feature argument names that file, the feature argument resolved against `--dir`; without `--file` it rewrites every binding of the old title.
- [r57] `features bindings` reads a `scenarios(<path>, ...)` call under `--tests` as binding every scenario of each feature file it names, and of every feature file under a directory it names.
- [r58] **Where** `--unbound` is given, **when** `features bindings` is run, it also reports the file and title of each scenario that no `scenario(...)` or `scenarios(...)` call binds, in the feature files named after `--unbound` or, with none named, every feature file under `--dir`, and exits 1 when there is one.
- [r59] **Where** `--unbound` is given, **if** a scenario is bound by more than one call, `features bindings` reports its file and title with the module and line of each call, and exits 1.

## Implementation, may change
- Gherkin is parsed line by line, not by a Gherkin library. A docstring opens and closes on `"""` or three
  backticks. A scenario's block is its tag lines, its `Scenario:` line and everything up to the next
  scenario's tag lines; `move` drops the block's trailing blank lines.
- `tag` replaces the scenario's first `@r<n>` tag or adds one to its last tag line; `deprecate` adds to the last
  tag line; a new tag line takes the scenario's indentation. Background steps inlined by `move` take the
  scenario's step indentation; kept feature tags take the `Scenario:` line's.
- `verify-moved` compares lines stripped of indentation, blank lines and comments, and also reports titles
  missing from or added to the second tree.
- `move` also refuses a destination that is the scenario's own file.
- `deprecate` writes the description line as `Deprecated for: <title>` or `Deprecated for: removal`, indented
  like the scenario's first following line.
- `bindings` reads only a title written as a plain string in the call; a feature given as a name is looked up
  among the module's own top-level assignments. A `scenario` or `scenarios` path names a feature file by its
  base name, as it does today, or a directory by every feature file under it. `rebind` refuses a title written
  over several lines.
- Output lines: `list` prints `<path>: <title>`; `deprecated` prints
  `<path>: <title> | for: <what> | <replacement's path> @r<n>` or `none deprecated`; `bindings` prints
  `<path>:<line>: no scenario titled "<title>" in <feature>`, and with `--unbound`
  `<feature path>: <title> | bound by no test` or `<feature path>: <title> | bound by <module>:<line>, <module>:<line>`.
- Exit status: 0 success, 1 a check failed or an edit was refused, 2 bad usage.

## Not yet
- `Rule:` blocks are refused rather than parsed — trigger: a feature file needs a `Rule:`.
