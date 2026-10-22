---
id: initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-16-script-capabilities-drafts-round-2
kind: initiative-archive
about: [capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools, capability/missingmass.io/shopsystem/shopsystem-bdd/batch-measurement, capability/missingmass.io/shopsystem/shopsystem-bdd/design-model-check, capability/missingmass.io/shopsystem/shopsystem-bdd/feature-file-tools, bounded-context/missingmass.io/shopsystem/shopsystem-bdd]
date: 2026-10-16
---

# Script capabilities formulation, round 2: feature drafts and brief template (superseded)

The round-2 drafts of 2026-10-16, new scenarios only, for the lines reworded after round 1's questions (analysis-tools r1 r14, batch-measurement r10 r34, slice-plan-tool r8 r10 r23, design-model-check r23 r26 r27 r41, feature-file-tools r3 r4 r14), and the brief template the controller filled for each formulator dispatch. slice-plan-tool has since been removed from the spec. The reply is in review-findings/2026-10-16-script-capabilities-formulation-round-2.

Archived from git-ignored scratch; each file's text as it was.

## `.superpowers/spec-drafts/2026-10-16-script-capabilities/round-2/brief-template.txt`

~~~~~~
Formulate spec/capabilities/<NAME>.md as features/<NAME>.feature.
The approved changes to formulate: <THE CHANGE LIST ROWS, OR "every line">.
You may read anything under spec/ and anything under features/. Nothing else:
not docs/, not the source.

The file has this shape:

- File name: features/<NAME>.feature, the capability's own name.
- Line 1: `# formulated from spec/capabilities/<NAME>.md`
- Line 2: `Feature: <the capability's title>`
- Line 3: `  Narrator: <the capability's narrator>`
- A Background only for a fixed date or shared products, nothing else.
- One scenario per Behaviour line, in the lines' order, and no others.
  Each scenario has a tag line `@r<n>`, the id of the line it formulates, directly above `Scenario:`; its
  title is free, and restating the line's condition makes a good one. A line with a Where and several
  configurations, or with several cases, is one Scenario Outline with an
  Examples table, never a scenario per case. A table of commands in
  Behaviour is one scenario per row. A boundary the line does not state is
  not a scenario. A line every call or command must keep is one scenario
  per reason it gives, with one representative call, never a row per call.
- Every scenario carries a one-line description between its title and its
  first step: what it pins, in plain words. It is not a step and does not
  restate the steps.
- Formulate from Behaviour only. Purpose and Not yet are context.
  Implementation, may change is never formulated, however testable it looks.
- Steps: Given is the state of the world in the narrator's words. When is one
  action by one named role, in the third person (`the customer applies`,
  never `I apply` or `my cart`). Then is an outcome the narrator can observe.
  A refusal reads `Then the code is rejected because <the reason the line
  names>`, never the message text, status code, or field name.
- Data tables and step arguments use the narrator's words: product, price,
  quantity, code, expiry. Amounts are plain decimals with no currency symbol.
- A line that admits two readings gets no scenario, including one written to
  hold under both. Return it as a question.

Write to <DRAFTS PATH>/round-<N>/, and nowhere else: (1) for a new feature, the file;
for an existing one, only the new and changed scenarios, each headed by the
line it formulates. Reply with (2) a coverage table with one row per line:
the line's id, the line (quoted) and the scenario title that formulates it; (3) questions:
each line with two readings, quoted, and the two readings, one line each;
(4) cases you noticed that no line mentions, one line each, with no scenario
written for them; and the drafts' paths. Write that same reply, last of all,
to <DRAFTS PATH>/round-<N>/<NAME>.reply.md.
~~~~~~

## `.superpowers/spec-drafts/2026-10-16-script-capabilities/round-2/analysis-tools.feature`

~~~~~~
# drafts for features/analysis-tools.feature, round 2: r1, r14

  # [r1] **When** `tools` needs an interpreter, it uses the first of these, in this order: the one `--python` gives, used as given; `.venv/bin/python` under the current directory, if that file exists; `venv/bin/python` under the current directory, if that file exists; `$VIRTUAL_ENV/bin/python`, if that file exists, wherever `$VIRTUAL_ENV` points; and else the interpreter running the script. Unless `--log` is given, `tools probe` prints that interpreter's path and which of these it came from.
  @r1
  Scenario Outline: the interpreter is the first of --python, .venv, venv, $VIRTUAL_ENV and the running one
    Pins the order in which tools picks its interpreter, and that probe says which one it picked and why.
    Given a Python project in the current directory
    And <setting>
    When the agent runs `tools probe <option>`
    Then tools prints the path of <interpreter>
    And it says the interpreter came from <source>

    Examples:
      | setting                                                                                                         | option                         | interpreter                                     | source                          |
      | the project has .venv/bin/python and venv/bin/python, and $VIRTUAL_ENV points at /opt/env, which has bin/python | --python /opt/py/bin/python    | /opt/py/bin/python                              | --python                        |
      | the project has .venv/bin/python and venv/bin/python, and $VIRTUAL_ENV points at /opt/env, which has bin/python |                                | .venv/bin/python under the current directory    | .venv                           |
      | the project has venv/bin/python and no .venv/bin/python, and $VIRTUAL_ENV points at /opt/env, which has bin/python |                             | venv/bin/python under the current directory     | venv                            |
      | the project has neither .venv/bin/python nor venv/bin/python, and $VIRTUAL_ENV points at /opt/env, outside the project, which has bin/python | |  /opt/env/bin/python                         | $VIRTUAL_ENV                    |
      | the project has neither .venv/bin/python nor venv/bin/python, and $VIRTUAL_ENV points at /opt/env, which has no bin/python |                    | the interpreter running the script              | the interpreter running the script |

  # [r14] **When** `tools refs <name>` is run, `tools` prints every reference to that function, class or name defined in the project as `path:line`, including uses through an import or an alias, then one summary line with the number of references, the number of production files holding them and, as a separate number, the number of test files holding them, and where the name is defined.
  @r14
  Scenario: refs prints each reference as path:line, through imports and aliases, then one summary line
    Pins that a use under another file's import or an alias is still found, and that the summary keeps production and test files apart.
    Given a Python project that defines the function total in src/cart.py
    And src/checkout.py imports total and calls it
    And src/report.py imports total under the alias cart_total and calls cart_total
    And tests/test_cart.py imports total and calls it
    When the agent runs `tools refs total`
    Then tools prints each reference as `path:line`
    And the references printed include the calls in src/checkout.py, src/report.py and tests/test_cart.py
    And then it prints one summary line giving the number of references printed, 2 production files, 1 test file, and src/cart.py as where total is defined
~~~~~~

## `.superpowers/spec-drafts/2026-10-16-script-capabilities/round-2/batch-measurement.feature`

~~~~~~
# drafts for features/batch-measurement.feature, round 2: r10, r34

  # [r10] A request's usage is counted once in the facts, however many transcript rows carry it, and its reasoning tokens are a part of its output tokens: the facts report reasoning as "of which" the output figure and never add it to that figure.
  @r10
  Scenario: a request's usage is counted once, and its reasoning is part of its output
    A request repeated across transcript rows is not counted again, and reasoning tokens are shown inside the output figure, not on top of it.
    Given a batch with one dispatch that made one request
    And the request's usage, 500 new input and 1200 output tokens of which 300 are reasoning, is carried by three transcript rows
    When the session runs measure batch for the batch
    Then the facts count the request's 500 new input and 1200 output tokens once
    And the facts give its output as 1200, of which 300 reasoning
    And no output figure in the facts is 1500

  # [r34] The facts count the dispatches given more than one prompt as resumed; they give the share of building time from the first branch review on, where building time is the dispatches' own durations summed and not wall-clock time, and a scout's dispatches are left out of both that time and the part of it from the first branch review on; and they give the mean and summed starting context of the dispatches.
  @r34
  Scenario: the facts count resumed dispatches, the late share of building time without scouts, and starting context
    Building time is the dispatches' own durations added up, scouts aside, and the share after the first branch review is taken of that.
    Given a batch whose dispatches are
      | dispatch      | role          | prompts | starts               | own duration in minutes | starting context |
      | implementer 1 | implementer   | 1       | before any review    | 30                      | 20000            |
      | implementer 2 | implementer   | 1       | with implementer 1   | 30                      | 30000            |
      | review 1      | branch review | 1       | after both           | 10                      | 40000            |
      | fix 1         | implementer   | 2       | after review 1       | 30                      | 10000            |
      | scout 1       | scout         | 1       | after review 1       | 15                      | 50000            |
    And implementer 1 and implementer 2 ran at the same time
    When the session runs measure batch for the batch
    Then the facts count 1 dispatch as resumed
    And the facts give 0.4 as the share of building time from the first branch review on
    And the facts give a mean starting context of 30000 and a summed starting context of 150000
~~~~~~

## `.superpowers/spec-drafts/2026-10-16-script-capabilities/round-2/design-model-check.feature`

~~~~~~
# drafts for features/design-model-check.feature, round 2: r23, r26, r27, r41

  # [r23] **If** a capability-proposal adds or removes a requirement no capability has, `model check` reports it as unresolved, except that adding an id the capability lists as retired is reported under v15c. Removing an id the capability lists as retired is reported as unresolved like any other.
  @r23
  Scenario Outline: a proposal adding or removing a requirement no capability has is unresolved, unless it adds a retired id
    Pins that an absent requirement is an unresolved reference whether added or removed, and that adding a retired id is a v15c instead.
    Given a capability thing with requirement r1 that lists r4 as retired
    And a capability-proposal that <change> thing#<id>
    When model check is run
    Then thing#<id> is <reported>

    Examples:
      | change  | id | reported                                  |
      | adds    | r9 | reported as unresolved                    |
      | removes | r9 | reported as unresolved                    |
      | adds    | r4 | reported under v15c and not as unresolved |
      | removes | r4 | reported as unresolved                    |

  # [r26] **If** a feature file is not the `formulated_as` of any capability, where a capability that gives none has `features/<its name>.feature`, or two of its scenarios share a title, `model check` reports a file problem naming the file. A scenario tagged `@holding` is not counted in the title check.
  @r26
  Scenario Outline: a feature file no capability is formulated as, or with a title twice, is a file problem
    Pins which feature files belong to a capability, and that titles are unique among the scenarios not held.
    Given a capability thing, <formulated as>
    And a feature file <file> in which <titles>
    When model check is run
    Then it <reports> a file problem naming <file>

    Examples:
      | formulated as                                  | file                   | titles                                                                     | reports         |
      | formulated_as features/thing.feature           | features/stray.feature | every scenario has its own title                                           | reports         |
      | giving no formulated_as                        | features/thing.feature | every scenario has its own title                                           | does not report |
      | formulated_as features/sub/thing-flow.feature  | features/thing.feature | every scenario has its own title                                           | reports         |
      | formulated_as features/thing.feature           | features/thing.feature | two scenarios are titled "Apply a code"                                    | reports         |
      | formulated_as features/thing.feature           | features/thing.feature | two scenarios are titled "Apply a code" and one of them is tagged @holding | does not report |

  # [r27] **If** a work directory has no `initiative.md`, an initiative or part has no `id`, a part's kind is not a part kind, a status is missing or not in its kind's lifecycle, a priority is not a number or a date is not `YYYY-MM-DD`, `model check` reports a file problem naming the file; for a work directory with no `initiative.md` it names the directory, not the missing file.
  @r27
  Scenario Outline: a malformed work directory or work file is a file problem
    Pins the shape each initiative and part file must have, and that a missing initiative.md is charged to its directory.
    Given a repository with a work directory work/i1 in which <case>
    When model check is run
    Then it reports a file problem naming <named>

    Examples:
      | case                                                  | named                                     |
      | there is no initiative.md                             | work/i1, and not work/i1/initiative.md    |
      | initiative.md has no id                               | work/i1/initiative.md                     |
      | the part p1.md has no id                              | work/i1/p1.md                             |
      | the part p1.md has the kind banana                    | work/i1/p1.md                             |
      | the part p1.md has no status                          | work/i1/p1.md                             |
      | the part p1.md has a status not in its kind's lifecycle | work/i1/p1.md                           |
      | the part p1.md has the priority high                  | work/i1/p1.md                             |
      | the part p1.md has a date written 16/10/2026          | work/i1/p1.md                             |

  # [r41] **When** `model why` is run, it lists each capability-proposal that adds, changes or removes the requirement, in date order with its status and date. **If** no capability-proposal adds or changes it, including when every one that names it only removes it, `model why` exits 1; one proposal that adds or changes it is enough for exit 0.
  @r41
  Scenario Outline: why lists every proposal naming the requirement by date, and fails when none adds or changes it
    Pins that removing proposals are listed too, in date order with status and date, but only one that adds or changes the requirement makes why succeed.
    Given a capability thing with requirement r2
    And <proposals>
    When model why is run for thing#r2
    Then it lists <listed>, in that order, each with its status and date
    And it exits <status>

    Examples:
      | proposals                                                                                                   | listed      | status |
      | a capability-proposal p2 dated 2026-10-01 that removes thing#r2 and a capability-proposal p1 dated 2026-09-01 that adds thing#r2    | p1 then p2  | 0      |
      | a capability-proposal p2 dated 2026-10-01 that removes thing#r2 and a capability-proposal p1 dated 2026-09-01 that changes thing#r2 | p1 then p2  | 0      |
      | a capability-proposal p2 dated 2026-10-01 that removes thing#r2 and a capability-proposal p1 dated 2026-09-01 that removes thing#r2 | p1 then p2  | 1      |
      | only a capability-proposal p2 dated 2026-10-01 that removes thing#r2                                        | p2          | 1      |
~~~~~~

## `.superpowers/spec-drafts/2026-10-16-script-capabilities/round-2/feature-file-tools.feature`

~~~~~~
# drafts for features/feature-file-tools.feature, round 2: r3, r4, r14

  # [r3] **If** an edit would leave a file that `features` cannot read, `features` refuses the edit and leaves every file as it was. `features` reads a file as invalid when it holds a `Rule:` block outside a docstring, and checks nothing else of the result.
  @r3
  Scenario Outline: an edit is refused only when it would leave a Rule: block outside a docstring
    Pins that the one thing an edit's result is checked for is a Rule: block outside a docstring, and that a refused edit changes no file.
    Given an edit by features that would leave features/cart.feature holding <result>
    When the agent runs that edit
    Then <outcome>

    Examples:
      | result                                       | outcome                                                                                                      |
      | a Rule: block outside a docstring            | the edit is rejected because features could not read features/cart.feature, and every file is as it was     |
      | a Rule: line inside a docstring              | the edit is made                                                                                             |
      | two scenarios titled "Apply a code"          | the edit is made                                                                                             |

  # [r4] **When** `features count --by-tag` is run, `features` prints the number of scenarios carrying each tag and a total, counting a Scenario Outline once per Examples row and giving each scenario its feature's tags and its Examples table's tags. The total counts every scenario, those carrying no tag included.
  @r4
  Scenario: counting by tag counts outline rows, inherited tags and untagged scenarios
    Pins that each Examples row is a scenario carrying its feature's and its own table's tags, and that the total leaves no scenario out.
    Given a feature file features/cart.feature tagged @cart
    And it has a scenario "Plain" with no tags of its own
    And it has a scenario "Own tag" tagged @slice-1
    And it has a Scenario Outline "Outlined" tagged @slice-2 with an Examples table tagged @r3 of 2 rows and an untagged Examples table of 1 row
    And a feature file features/misc.feature with no tags has a scenario "Untagged" with no tags
    When the agent runs features count --by-tag
    Then it prints 5 scenarios for cart, 1 for slice-1, 3 for slice-2 and 2 for r3
    And it prints a total of 6

  # [r14] **Where** `--carry-feature-tags` is given, **when** `features move` is run, `features` puts the source's feature tags that the destination's feature tags lack on a tag line of their own immediately above the moved scenario's `Scenario:` line, after any tag line the scenario already has, and joins them to none.
  @r14
  Scenario Outline: moving with feature tags carried adds the missing ones on a tag line of their own
    Pins that only the feature tags the destination lacks are carried, on their own line just above the Scenario: line, with the scenario's own tag lines left as they were.
    Given a feature file features/old.feature with the feature tags @cart and @checkout
    And its scenario "Apply a code" has <own tag lines>
    And a feature file features/cart.feature with the feature tag @cart
    When the agent runs features move "Apply a code" --to features/cart.feature --carry-feature-tags
    Then the moved "Apply a code" has the tag lines <tag lines after>, the last directly above its Scenario: line

    Examples:
      | own tag lines         | tag lines after                  |
      | the tag line "@slice-2" | "@slice-2" then "@checkout"    |
      | no tag line           | "@checkout"                      |
~~~~~~

## `.superpowers/spec-drafts/2026-10-16-script-capabilities/round-2/slice-plan-tool.feature`

~~~~~~
# drafts for features/slice-plan-tool.feature, round 2: r8, r10, r23

  # [r8] **If** `plan status` is given a status that is not `planned`, `in progress` or `green`, each with an optional `: <note>`, or `blocked: <why>`, `plan` refuses and leaves the file as it was.
  @r8
  Scenario Outline: a status plan does not know is refused
    Pins that only planned, in progress and green, each with an optional note, or blocked with its reason, can be set.
    Given a valid plan whose slice 2 has Status planned
    When the agent runs `plan status 2 "<status>"`
    Then the command is rejected because <status> is not a status a slice may have
    And the plan file is unchanged

    Examples:
      | status        |
      | done          |
      | done: merged  |
      | blocked       |

  # [r10] **When** `plan add-slice <n> <name>` is run, `plan` writes the slice in number order, with Status planned. It compares dotted numbers part by part as whole numbers, so `2.10` follows `2.9` and `1` precedes `1.1`.
  @r10
  Scenario Outline: an added slice goes in number order with Status planned
    Pins where a new slice lands among dotted numbers, compared part by part as whole numbers.
    Given a valid plan with slices <slices before>, in that order
    When the agent runs `plan add-slice <number> "Checkout"`
    Then the plan's slices are <slices after>, in that order
    And slice <number> has Status planned

    Examples:
      | slices before | number | slices after         |
      | 1, 2.9 and 3  | 2.10   | 1, 2.9, 2.10 and 3   |
      | 1.1 and 2     | 1      | 1, 1.1 and 2         |
      | 1 and 3       | 2      | 1, 2 and 3           |

  # [r23] **When** `plan archive <batch>` is run, `plan` writes the green slices and the whole Log to `archive/<plan file name without .md>-<batch>.md` beside the plan, so `foo-slices.md` archives to `archive/foo-slices-<batch>.md`, and removes those slices from the plan.
  @r23
  Scenario: archiving writes the green slices and the Log beside the plan and removes those slices
    Pins the archive file's name and place, what goes into it, and that the archived slices leave the plan.
    Given a valid plan docs/superpowers/plans/foo-slices.md with slice 1 green, slice 2 planned and slice 3 green
    And its Log holds three entries
    When the agent runs `plan archive batch-1`
    Then docs/superpowers/plans/archive/foo-slices-batch-1.md holds slices 1 and 3 and not slice 2
    And it holds the three entries the Log held
    And the plan holds slice 2 and not slices 1 or 3
~~~~~~
