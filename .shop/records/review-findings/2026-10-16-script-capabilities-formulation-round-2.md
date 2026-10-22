---
id: review-finding/missingmass.io/shopsystem/shopsystem-bdd/2026-10-16-script-capabilities-formulation-round-2
kind: review-finding
about: [capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools, capability/missingmass.io/shopsystem/shopsystem-bdd/batch-measurement, capability/missingmass.io/shopsystem/shopsystem-bdd/design-model-check, capability/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools, bounded-context/missingmass.io/shopsystem/shopsystem-bdd]
date: 2026-10-16
---

# Script capabilities formulation, round 2: formulator reply

The feature-formulator's single round-2 reply for the five script capabilities of 2026-10-16 (analysis-tools, batch-measurement, slice-plan-tool, design-model-check, feature-file-tools), formulating the lines reworded after round 1's questions: coverage, no further questions, and the cases no line mentions. slice-plan-tool has since been removed from the spec, hence the bounded context. The round's drafts and brief template are archived in archive/2026-10-16-script-capabilities-drafts-round-2.

Archived from `.superpowers/spec-drafts/2026-10-16-script-capabilities/round-2/all.reply.md` (git-ignored scratch), text as it was.

---

# Round 2 reply: analysis-tools, batch-measurement, slice-plan-tool, design-model-check, feature-file-tools

Each draft holds only new scenarios. Each one has a comment above it quoting the line it formulates. None of the five feature files had a scenario for these ids, and no new title repeats an existing one.

## analysis-tools

### Coverage

| id | line | scenario |
|---|---|---|
| r1 | "**When** `tools` needs an interpreter, it uses the first of these, in this order: the one `--python` gives, used as given; `.venv/bin/python` under the current directory, if that file exists; `venv/bin/python` under the current directory, if that file exists; `$VIRTUAL_ENV/bin/python`, if that file exists, wherever `$VIRTUAL_ENV` points; and else the interpreter running the script. Unless `--log` is given, `tools probe` prints that interpreter's path and which of these it came from." | Scenario Outline: the interpreter is the first of --python, .venv, venv, $VIRTUAL_ENV and the running one |
| r14 | "**When** `tools refs <name>` is run, `tools` prints every reference to that function, class or name defined in the project as `path:line`, including uses through an import or an alias, then one summary line with the number of references, the number of production files holding them and, as a separate number, the number of test files holding them, and where the name is defined." | refs prints each reference as path:line, through imports and aliases, then one summary line |

### Questions
None.

### Cases no line mentions
- r1: a `--python` path that does not exist. "Used as given" implies tools does not fall back to the next choice, and r21 refuses an interpreter that does not run. No line says this outright.
- r1: whether probe prints the interpreter's path as given or resolved to an absolute path.
- r1: the "unless `--log`" part has no row of its own here. The existing r4 scenario ("exactly one line") already rules out the interpreter line under `--log`.
- r14: whether the import statement that names the name counts as a reference, as well as the uses after it. The draft pins the file counts but not an exact number of references for this reason.
- r14: a file that holds both the definition and a use, and whether it counts as a production file holding references.
- r14: a name defined in more than one place in the project.

## batch-measurement

### Coverage

| id | line | scenario |
|---|---|---|
| r10 | "A request's usage is counted once in the facts, however many transcript rows carry it, and its reasoning tokens are a part of its output tokens: the facts report reasoning as "of which" the output figure and never add it to that figure." | a request's usage is counted once, and its reasoning is part of its output |
| r34 | "The facts count the dispatches given more than one prompt as resumed; they give the share of building time from the first branch review on, where building time is the dispatches' own durations summed and not wall-clock time, and a scout's dispatches are left out of both that time and the part of it from the first branch review on; and they give the mean and summed starting context of the dispatches." | the facts count resumed dispatches, the late share of building time without scouts, and starting context |

### Questions
None. For r34, the line limits the scout's exclusion to building time, so the draft keeps the scout in the mean and summed starting context (30000 and 150000 across five dispatches).

### Cases no line mentions
- r10: two separate requests whose usage figures happen to be the same. No line says how they are told apart from one request carried twice.
- r34: a dispatch that is already running when the first branch review starts. No line says how its time is split.
- r34: a batch with no branch review, and what the share is then.
- r34: what a resumed dispatch's "own duration" is, either its active spans added up or first start to last end.
- r34: whether a scout given more than one prompt counts as resumed.

## slice-plan-tool

### Coverage

| id | line | scenario |
|---|---|---|
| r8 | "**If** `plan status` is given a status that is not `planned`, `in progress` or `green`, each with an optional `: <note>`, or `blocked: <why>`, `plan` refuses and leaves the file as it was." | Scenario Outline: a status plan does not know is refused |
| r10 | "**When** `plan add-slice <n> <name>` is run, `plan` writes the slice in number order, with Status planned. It compares dotted numbers part by part as whole numbers, so `2.10` follows `2.9` and `1` precedes `1.1`." | Scenario Outline: an added slice goes in number order with Status planned |
| r23 | "**When** `plan archive <batch>` is run, `plan` writes the green slices and the whole Log to `archive/<plan file name without .md>-<batch>.md` beside the plan, so `foo-slices.md` archives to `archive/foo-slices-<batch>.md`, and removes those slices from the plan." | archiving writes the green slices and the Log beside the plan and removes those slices |

### Questions
None.

### Cases no line mentions
- r8: case in status words, for example `Green` or `In progress`.
- r8: `blocked:` with an empty reason, or `green:` with an empty note.
- r10: a slice number with a leading zero or a part that is not a number, for example `2.a`.
- r23: whether the archive's copy of the Log also holds the new line naming the archive (r24), or only the entries from before archiving.
- r23: a plan file whose name does not end in `-slices.md` when it is named with `--file`.

## design-model-check

### Coverage

| id | line | scenario |
|---|---|---|
| r23 | "**If** a capability-proposal adds or removes a requirement no capability has, `model check` reports it as unresolved, except that adding an id the capability lists as retired is reported under v15c. Removing an id the capability lists as retired is reported as unresolved like any other." | Scenario Outline: a proposal adding or removing a requirement no capability has is unresolved, unless it adds a retired id |
| r26 | "**If** a feature file is not the `formulated_as` of any capability, where a capability that gives none has `features/<its name>.feature`, or two of its scenarios share a title, `model check` reports a file problem naming the file. A scenario tagged `@holding` is not counted in the title check." | Scenario Outline: a feature file no capability is formulated as, or with a title twice, is a file problem |
| r27 | "**If** a work directory has no `initiative.md`, an initiative or part has no `id`, a part's kind is not a part kind, a status is missing or not in its kind's lifecycle, a priority is not a number or a date is not `YYYY-MM-DD`, `model check` reports a file problem naming the file; for a work directory with no `initiative.md` it names the directory, not the missing file." | Scenario Outline: a malformed work directory or work file is a file problem |
| r41 | "**When** `model why` is run, it lists each capability-proposal that adds, changes or removes the requirement, in date order with its status and date. **If** no capability-proposal adds or changes it, including when every one that names it only removes it, `model why` exits 1; one proposal that adds or changes it is enough for exit 0." | Scenario Outline: why lists every proposal naming the requirement by date, and fails when none adds or changes it |

### Questions
None.

### Cases no line mentions
- r23: a proposal that changes, rather than adds or removes, an id the capability lists as retired. r6 (v15e) and r5/r23 (v15c) could each claim it.
- r26: a `*.feature` file in a subdirectory of `features/` that only matches a capability's name in a different directory.
- r26: three scenarios sharing one title, one of them held. The draft only shows two, one held.
- r27: which frontmatter fields count as "a date" for the `YYYY-MM-DD` check. The draft says only "a date written 16/10/2026".
- r27: a work file other than `initiative.md` in a directory that has no `initiative.md`, and whether it is also reported.
- r41: two proposals with the same date, and the order they are listed in.
- r41: a proposal with no date, and where it falls in date order.

## feature-file-tools

### Coverage

| id | line | scenario |
|---|---|---|
| r3 | "**If** an edit would leave a file that `features` cannot read, `features` refuses the edit and leaves every file as it was. `features` reads a file as invalid when it holds a `Rule:` block outside a docstring, and checks nothing else of the result." | Scenario Outline: an edit is refused only when it would leave a Rule: block outside a docstring |
| r4 | "**When** `features count --by-tag` is run, `features` prints the number of scenarios carrying each tag and a total, counting a Scenario Outline once per Examples row and giving each scenario its feature's tags and its Examples table's tags. The total counts every scenario, those carrying no tag included." | counting by tag counts outline rows, inherited tags and untagged scenarios |
| r14 | "**Where** `--carry-feature-tags` is given, **when** `features move` is run, `features` puts the source's feature tags that the destination's feature tags lack on a tag line of their own immediately above the moved scenario's `Scenario:` line, after any tag line the scenario already has, and joins them to none." | Scenario Outline: moving with feature tags carried adds the missing ones on a tag line of their own |

### Questions
None.

### Cases no line mentions
- r3: the draft describes the edit in the abstract ("an edit by features that would leave ..."). No line says which command can produce a `Rule:` block outside a docstring. A step definition will have to pick one, for example a move into a file that ends inside an unclosed docstring.
- r3: a file left with a docstring that is never closed, and whether `features` can read it.
- r4: a scenario that carries the same tag both itself and through its feature or Examples table, and whether it is counted once or twice for that tag.
- r4: whether the printed tags carry their leading `@`.
- r14: the order of the carried tags on their new line when several are carried.
- r14: a source feature with no tags, or a destination that already has every source feature tag. The line implies nothing is added, but neither case is stated.
- r14: `--carry-feature-tags` given together with `--inline-background`.

## Drafts
- /home/vscode/shopsystem-bdd/.superpowers/spec-drafts/2026-10-16-script-capabilities/round-2/analysis-tools.feature
- /home/vscode/shopsystem-bdd/.superpowers/spec-drafts/2026-10-16-script-capabilities/round-2/batch-measurement.feature
- /home/vscode/shopsystem-bdd/.superpowers/spec-drafts/2026-10-16-script-capabilities/round-2/slice-plan-tool.feature
- /home/vscode/shopsystem-bdd/.superpowers/spec-drafts/2026-10-16-script-capabilities/round-2/design-model-check.feature
- /home/vscode/shopsystem-bdd/.superpowers/spec-drafts/2026-10-16-script-capabilities/round-2/feature-file-tools.feature
