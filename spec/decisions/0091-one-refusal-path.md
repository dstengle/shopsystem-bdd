---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/one-refusal-path
summary: "Every refusal of every command reaches one base exception, shop_refused.Refused, and leaves through one catch a tool that exits 1 naming the reason and changes nothing."
date: 2026-11-10
status: accepted
tier: check
enforced_by: [tests/scripts/test_refusal_path.py::test_every_refusal_class_reaches_the_one_base, tests/scripts/test_refusal_path.py::test_a_refused_command_exits_1_naming_the_reason_and_changes_nothing]
verified_by: [check]
rests_on: [U12]
by: "the plan for b145, 2026-11-10"
---

# 0091. One refusal path

## Context

CNL 4's I14b (design 10.3, 13 point 8): five Refused classes, each tool catching only its own; an entailed consequence guaranteed by one code path and tested once (b112, b125).

## Decision

Every refusal of every command is a `shop_refused.Refused` (re-exported as `shop_files.Refused`): the four
other `Refused` classes (`tools_env`, `tools_grammar`, `features_gherkin`, `transcripts`) and
`batch_git.GitFailed` are its subclasses, and each tool (`work`, `tools`, `features`, `measure`) catches the
base once, prints `<tool>: <reason>` and exits 1. A refusal is raised before anything is written, or what was
written is put back (U11). The path is tested once, by tests/scripts/test_refusal_path.py; after every
generated scenario tests/scenarios/vocab.py checks that a refused run changed nothing (decision 0088). No
scenario states U11 again.
