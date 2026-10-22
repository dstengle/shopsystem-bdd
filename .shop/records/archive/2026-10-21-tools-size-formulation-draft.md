---
id: initiative-archive/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-tools-size-formulation-draft
kind: initiative-archive
about: capability/missingmass.io/shopsystem/shopsystem-bdd/analysis-tools
date: 2026-10-21
---

# analysis-tools: draft scenarios for tools size (r50-r52)

The blind feature-formulator's draft of three scenarios for analysis-tools r50-r52 (`tools size`), each under the EARS Behaviour line it accepts, written 2026-10-21 (00:10 UTC) for release 0.21.0. Their later form, with `tools size` exiting with an error in words and the narrator a session, is in the 2026-10-21-one-requirement round's analysis-tools draft. The round's questions and findings are the matching review-finding record review-finding/missingmass.io/shopsystem/shopsystem-bdd/2026-10-21-tools-size-formulation.

Archived from `.shop/scratch/drafts/2026-10-21-tools-size/analysis-tools.feature` (git-ignored scratch), text as it was.

```gherkin
  # [r50] **When** `tools size` is run, `tools` shall print each tracked Python file over the size limit in the working tree, a Python file being one with a `.py` extension or a `python` shebang, tests included, with its line count.
  @r50
  Scenario: size prints each tracked Python file over the limit in the working tree, with its line count
    Pins which files count as Python, that tests are included, that the working tree is counted, and that no other file is printed.
    Given a Python project in git
    And it tracks src/cart.py of 301 lines, tests/test_cart.py of 320 lines, src/total.py of 300 lines and README.md of 900 lines
    And it tracks bin/reprice, with no extension, a python shebang and 400 lines
    And it tracks src/report.py, committed at 200 lines and edited in the working tree to 350 lines
    And it has an untracked src/draft.py of 500 lines
    When the agent runs `tools size`
    Then tools prints src/cart.py with 301 lines, tests/test_cart.py with 320 lines, bin/reprice with 400 lines and src/report.py with 350 lines
    And it prints no other file

  # [r51] **If** any tracked Python file is over the size limit, then `tools size` shall exit 1.
  @r51
  Scenario: size fails when one tracked Python file is over the limit
    Pins that a single file over the limit fails the command.
    Given a Python project in git
    And it tracks src/cart.py of 301 lines and src/total.py of 120 lines
    When the agent runs `tools size`
    Then it exits 1

  # [r52] **Where** `tools size --limit <n>` is given, `tools size` shall use `<n>` lines as the size limit, and 300 lines otherwise.
  @r52
  Scenario Outline: size uses the limit --limit gives, and 300 lines without it
    Pins the limit at its edge: a file of exactly the limit is within it, one line more is over.
    Given a Python project in git
    And it tracks src/total.py of <within> lines and src/cart.py of <over> lines
    When the agent runs `tools size <option>`
    Then tools prints src/cart.py with <over> lines
    And it does not print src/total.py

    Examples:
      | option      | within | over |
      | --limit 250 | 250    | 251  |
      |             | 300    | 301  |
```
