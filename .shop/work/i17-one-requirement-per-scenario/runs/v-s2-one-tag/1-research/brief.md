# research of v-s2-one-tag

Work-item: .shop/work/i17-one-requirement-per-scenario/v-s2-one-tag.md
Agent: code-scout
Scripts: /home/vscode/shopsystem-bdd/scripts
Base: b392b457242a3eb0369fc06bc8afa68c5821984f
Worktree: /tmp/work-run-i17-one-requirement-per-scenario-hgpd58tk/v-s2-one-tag-1-research
Branch: none (a detached checkout)
File set: scripts/model, scripts/model.lp, scripts/model_*.py, tests/scripts/test_model.py, tests/scenarios/*design_model_check*.py, features/design-model-check.feature, docs/capability-format.md
Accepted scenarios:
- features/design-model-check.feature: a repository the grammar accepts passes
- features/design-model-check.feature: violations are printed by their grammar name and make `model check` exit with an error
- features/design-model-check.feature: a requirement bullet without an id is refused
- features/design-model-check.feature: two requirements with one id are refused
- features/design-model-check.feature: a retired id used again is refused
- features/design-model-check.feature: a proposal changing a requirement no capability has is refused
- features/design-model-check.feature: a proposal formulated before its requirement has a scenario is refused
- features/design-model-check.feature: a guarantees capability needs no scenarios
- features/design-model-check.feature: references that name nothing are printed
- features/design-model-check.feature: a part that reaches no initiative is refused
- features/design-model-check.feature: warnings are counted and do not change whether `model check` exits successfully
- features/design-model-check.feature: without clingo `model check` says how to install it
- features/design-model-check.feature: facts are printed in clingo's syntax
- features/design-model-check.feature: the decisions index lists every decision
- features/design-model-check.feature: a stale decisions index is printed as not current and left alone
- features/design-model-check.feature: why traces a requirement to its initiative's sources
- features/design-model-check.feature: why with no proposal says so
- features/design-model-check.feature: a range of ids stands for each id in it
- features/design-model-check.feature: model reads the repository's files under its root
- features/design-model-check.feature: a scenario names a requirement by its tag in its capability's feature file
- features/design-model-check.feature: a reference written name#r<n> is that capability's requirement
- features/design-model-check.feature: a reference in neither requirement form, or a reversed range, is unresolved
- features/design-model-check.feature: a proposal adding or removing a requirement no capability has is unresolved, unless it adds a retired id
- features/design-model-check.feature: a proposal's list naming a term the glossary lacks is unresolved, unless a merged proposal removes it
- features/design-model-check.feature: a frontmatter reference to nothing, or to the wrong kind, is unresolved
- features/design-model-check.feature: a malformed index or capability file is a file problem
- features/design-model-check.feature: a path of the old layout is a file problem naming scripts/migrate
- features/design-model-check.feature: a feature file no capability is formulated as, with a title twice, or with a scenario tagged @holding, is a file problem
- features/design-model-check.feature: a malformed work directory or work file is a file problem
- features/design-model-check.feature: a work-item accepting a requirement no scenario names is a file problem
- features/design-model-check.feature: a malformed decision, record or frontmatter is a file problem
- features/design-model-check.feature: file problems are each printed and make `model check` exit with an error
- features/design-model-check.feature: with --json `model check`'s findings are one JSON object
- features/design-model-check.feature: only a capability-change initiative may have several parts directly
- features/design-model-check.feature: a proposal arguing two capabilities is refused
- features/design-model-check.feature: an initiative may be `done` when its proposal is formulated
- features/design-model-check.feature: a current decisions index passes `model decisions --check`
- features/design-model-check.feature: writing the decisions index leaves out decisions with no id
- features/design-model-check.feature: why refuses an argument that is not a requirement reference
- features/design-model-check.feature: why on a requirement no capability has still lists its proposals
- features/design-model-check.feature: why lists every proposal naming the requirement by date, each with its status and date
- features/design-model-check.feature: why fails when the only proposals naming the requirement remove it
- features/design-model-check.feature: a node may be written in short where its field allows it
- features/design-model-check.feature: a deprecated scenario names no requirement
- features/design-model-check.feature: a decision's source is a list of ids and its by is not read
- features/design-model-check.feature: a node whose id is not in type-first form is a file problem
- features/design-model-check.feature: a reference in a refused form is unresolved
- features/design-model-check.feature: a glossary bullet is a term of the bounded context
- features/design-model-check.feature: a glossary bullet not in the entry form is a file problem
- features/design-model-check.feature: facts give each term its kind, its context and its avoided words
- features/design-model-check.feature: a mention is a whole word in any case, plural allowed
- features/design-model-check.feature: a requirement or scenario using an avoided word is v_t1
- features/design-model-check.feature: two entries for one term are v_t2
- features/design-model-check.feature: an avoided word that is a term is v_t3
- features/design-model-check.feature: without clingo `model check` tries again under the first interpreter that has it
- features/design-model-check.feature: `model check` tries again only once
- features/design-model-check.feature: with no interpreter that has clingo `model check` names each one it tried
- features/design-model-check.feature: a withdrawn part is closed
- features/design-model-check.feature: an abandoned initiative with an open part is v_d2
- features/design-model-check.feature: a table row with an id is a requirement, and its header, separator and lead sentence are not
- features/design-model-check.feature: a Behaviour line in none of EARS's patterns is v_e1
- features/design-model-check.feature: a table row is judged by its lead sentence
- features/design-model-check.feature: a Behaviour line with two shalls or two sentences is v_e2
- features/design-model-check.feature: a merged capability-proposal adding an id its capability lists as retired is not v15c
- features/design-model-check.feature: a merged capability-proposal may add or remove an id its capability lists as retired
- features/design-model-check.feature: a scenario tagged with several requirements names each of them (deprecated)
- features/design-model-check.feature: a scenario with more than one requirement tag, its own and its feature's together, is v_s2
- features/design-model-check.feature: a work-item with no accepts and no check is v_w4, unless it is withdrawn
- features/design-model-check.feature: a code span, a double-quoted string and a tag are no mention
- features/design-model-check.feature: a table row whose id lost its brackets is a line with no id
- features/design-model-check.feature: a table is led only by the sentence just before it
- features/design-model-check.feature: `model rules` prints every rule with its plain label
- features/design-model-check.feature: the decisions index is written when there is no decision yet

Read (paths in your worktree):
- .shop/work/i17-one-requirement-per-scenario/v-s2-one-tag.md
- spec/capabilities/design-model-check.md

Run directory: /tmp/work-run-i17-one-requirement-per-scenario-hgpd58tk/v-s2-one-tag-1-research/.shop/scratch/1-research
Result file: /tmp/work-run-i17-one-requirement-per-scenario-hgpd58tk/v-s2-one-tag-1-research/.shop/scratch/1-research/result.json

You start in your worktree, /tmp/work-run-i17-one-requirement-per-scenario-hgpd58tk/v-s2-one-tag-1-research: run every command from there, as it is, and never change directory (no `cd`, no `git -C`); a command that does is refused.

Write your notes, plan, report or findings in the run directory and, last, the result file: JSON with `status`, `summary` (under fifteen lines) and `questions` (a list of strings).
