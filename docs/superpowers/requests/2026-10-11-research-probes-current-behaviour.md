# Request: task research probes current behaviour (follow-up to predictable batches and analysis tools)

From: shopsystem-kb, 2026-10-11, after batches 38 and 39 of its kb.v2 release. Applied locally in kb's batch 39; requested here so the plugin carries it.

## What happened

Batch 38's research scout read code and ran only the red markers ("nothing built or run beyond single markers"). It was right about where each change landed and why each scenario was red, and no listed test broke. But every miss it made was a question of the form "what does the system answer today when ...":

- A new path that never lands (a set checked only) was said to need "the same draft and checks". One refusal is made only by the storage adapter at landing, so the new path never reached it. Cost: a rejected second copy of the rule, one fix round, two changed precedences.
- A read naming a part was researched as a conversion problem; nobody asked what a read with a place returns today (the whole artifact). Cost: two fix rounds and a module at 247 of 250 lines, split in the next batch.
- A crash on the scenario's own data shape (items with no title, read at a glance) was found by the branch review.

Batch 39's research brief asked for probes through the operator's commands and the contract, in a scratch store, nothing built. It found two live defects before planning (an import landing under a running server; a file filed under another type's place landing), corrected two slice sizings (one from "0 production" to 6), and showed that a slice planned as "remove one check" needed a comparison step.

## Asked for

1. **code-scout, task research:** for each slice, probe current behaviour through the system's real entry points in scratch (never the checkout), and record each probe with its command and what came back, marked as run or as read. The probes are the Givens and Whens of the slice's scenarios against today's code, and the nearest cases the scenarios do not state (the same call with the store already holding something; with the thing asked for missing; with the scenario's data at its edges).
2. **A path that skips a stage:** when a slice adds a way through the system that leaves a stage out (a check that never lands, a read that never opens a transaction, a command that never signs), the research lists every refusal and effect that stage alone produces, so the plan decides each.
3. **Sizes:** the research gives the line count and room of every module the change's path passes through, not only the modules it expects to edit.
4. **slicing-into-increments, hand-off to writing-plans:** "why each scenario is red today" is taken from a run and the probes; a "0 production" Lands line is allowed only with a probe that shows the behaviour already there.
5. **Check against act:** where a system has a dry-run and a real run of one operation (a check and an import; a plan and an apply), the plan's Review Focus carries the property "what the dry run reports is what the real run does" and the batch keeps a randomized agreement test for it. In kb's batch 39 this property, probed by reviewers over tens of thousands of store and directory pairs, found every important defect of the batch; scenario tests found none of them.

## Also learned

- A final review's fix wave is not always one dispatch. In a release's last batch, three rounds each found a store left invalid or a store's own fault on operator input. The rule could be: after a final review, fix rounds continue while a finding is in a named severe class (data left invalid, the system's own fault on input, a landing on a refusal), and everything else is a backlog line.
- A reviewer told to triage strictly ("fix now only for ...") closed the loop in one pass.
