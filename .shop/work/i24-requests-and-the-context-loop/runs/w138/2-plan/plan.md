# Plan of w138: work run drafts a formulated proposal's work-items with their Retires, and a work-item for a branch review's fix-now findings

## 1. What goes green

- **supervision#r72**: "a formulated capability-proposal gets one work-item for each capability it adds or changes, accepting every requirement it names on that capability" (features/supervision.feature:890). Red today because its first Given has no step definition (no supervision step writes a capability-proposal), and its Then has none either. Underneath that, no code in `scripts/supervise*.py` reads a capability-proposal or drafts anything: probe P1 ran `work run i1` on a formulated p1, got exit 0 and no work-item, and a branch review ran over an initiative with no work-items at all.
- **supervision#r73**: "a work-item drafted for a formulated capability-proposal lists under its Retires each deprecated scenario of a requirement it accepts" (line 898). Red because the Given "its changes naming thing#r2" and the Then "lists ... under its ## Retires" have no steps. Underneath, `workqueue.add` writes no `## Retires`, and nothing reads a scenario's own `@r` tags for drafting. `features deprecated --json` gives no tag (P3).
- **supervision#r74**: "a kept branch review's findings to fix now get one work-item, naming the findings file, under the capability-proposal of the work-item they concern" (line 907). Red because its first Given, the one with the comma ("w1 is green, part of the capability-proposal p1, and w2 is withdrawn"), matches no step (`supervision_given.py:54` takes no comma), and `supervision_review_steps.py:21` has no reviewer that lists fix-now findings. Underneath, `Reviews.branch_review` keeps the review's directory but nothing reads its `result.json`, so nothing gets drafted (P4).
- Retired: none (the work-item has no Retires section).

## 2. Where the change lands

- `scripts/supervise_draft.py`: **new**. Drafting gets its own module. It reads the initiative's `formulated` capability-proposals (frontmatter `kind: capability-proposal`, `status`, `adds`, `changes`) and drafts one work-item per capability that does not already have one (decisions 1 to 3). It reads `features/<capability>.feature` for the deprecated scenarios a draft retires (decisions 4 and 5). It reads the last kept branch review's `result.json` and drafts the fix work-item (decisions 6 to 9). Drafting goes through the function behind `work add`, then pushes (decision 10). It is a part of `supervise.Run`, as `Reviews` is.
- `scripts/supervise.py`: `Run.run` gets two changes. It drafts for formulated proposals before the work-items are pulled. After a kept branch review whose result lists findings, it drafts the fix work-item and goes back to pulling (decision 11). The file is at 218 lines, so 82 lines are left.
- `scripts/supervise_review.py`: `branch_review` tells its caller which review it kept (its number or its kept directory), or that none ran, so the run can read the kept review's result. No other change here.
- `scripts/workqueue.py`: `add` gets two optional keyword parameters, both defaulting to nothing, so every positional caller stays as it is. One is the scenarios to retire, each written as a bullet under `## Retires`. The other is the findings file, written as a `findings:` frontmatter field. The file is at 279 lines with 21 left; the change must stay inside that. If it cannot, `add` and `highest` move into a module of their own first, with a row in CLAUDE.md, and the report says so.
- `CLAUDE.md`: one module-map row for `scripts/supervise_draft.py`. CLAUDE.md gives a new concern a new row.
- `tests/scenarios/supervision_proposal_steps.py`: **new**. The steps of the three scenarios: the formulated-proposal Givens (adds and changes), the comma Given of r74 (w1 green and part of p1, w2 withdrawn), the reviewer whose result lists fix-now findings concerning w1, and the three Thens.
- `tests/scenarios/test_supervision.py`: one import line for the new step module, beside the star-imports at lines 25-32. 246 lines, 54 left.
- `tests/scenarios/supervision_review_steps.py`: `reviewer_does` (line 21) is changed only if the new reviewer phrase cannot sit in the new module without two steps matching the same text. If it is changed, every phrase it takes today keeps working.

Taken out of the researcher's set:
- `scripts/work`: decision 10 adds no CLI option.
- `scripts/features_gherkin.py`, `model_*.py`, `supervise_pool.py`, `tests/scripts/stub_claude.py`, `agents/bdd-branch-reviewer.md`: these are only read.
- `supervision_world.py`, `supervision_given.py`: the new Givens go in the new module.
- `test_work_item_ids.py`, `test_work_add_title.py`, `test_work_queue.py`: they keep passing without an edit.

None of these is claimed.

## 3. Decisions

1. **What r72 drafts.** For each formulated capability-proposal of the initiative, every entry of `adds` and `changes` that names a capability's requirement (`<capability>#r<n>`, a range as written) is grouped by its capability. Each group becomes one work-item: `part_of: capability-proposal/<name>`, `under: <capability>`, its accepts the group's entries in the order given. An entry naming no capability's requirement (a `term/...`) drafts nothing, and `removes` is not read. The title names the proposal and the capability. Rests on supervision#r72 (C4 of the notes).
2. **A proposal is drafted once.** A capability gets no draft when a work-item of the initiative is already `part_of` that proposal and `under` that capability, whatever its status. Without this, every later `work run` would draft again, and i24's own formulated proposals, whose work-items exist, would be drafted twice. Rests on supervision#r72, "one work-item for each capability".
3. **When r72 drafts.** At the start of each pass of `Run.run`, before the pull, so the pull takes the drafts through research and onward in the same run. Rests on supervision#r1 (pull until no work-item can make a transition) and r66.
4. **Which scenarios r73 lists.** The scenarios of `features/<under>.feature` that carry `@deprecated` and an `@r<n>` tag which, read on that capability, is a requirement the draft accepts (a range included). The tags come from the scenario's own tags, through the Gherkin reader in `scripts/features_gherkin.py`, not from `features deprecated`. Each is written as a bullet in the existing items' form: the quoted title, then its `(@r<n>)` tag. Rests on supervision#r73 and design-decision/scenario-names-requirement-by-tag (the feature file is the capability's).
5. **No deprecated scenario, no section.** A draft with nothing to retire gets no `## Retires`. The agents read "a Retires section, if it has one", so leaving the section out is how "none" is already said. Rests on supervision#r73 (it lists each one, and here there are none) (C2).
6. **Where "findings to fix now" are read.** From the kept review's `result.json`: its `questions` lines are the findings it lists to fix now. A result with no `questions`, an empty list, or no result file lists nothing. `findings.md` is not read; that would be parsing a worker's prose. Rests on design-decision/worker-results-are-files and the reviewer's result contract (`questions`: each fix-now or Critical finding, one line each, naming its work-item) (C1).
7. **Which review r74 drafts for.** The last kept branch review, and only while no work-item of the initiative names its findings file. That one review is drafted for once, also when the run that kept it stopped before drafting (for example, a failed push, r53). Rests on supervision#r74 and r75 ("its kept branch review").
8. **What the fix work-item is.** One work-item for all the lines. Its `part_of` is the proposal of the work-item the lines name: the initiative's work-item named in each line's work-item field. It takes `under` and `accepts` from that work-item, so the fix's merge runs that work-item's scenarios. It names the findings file as `findings: <the kept review's findings path, relative to the repository>`, taken from the result's `findings` field, else `findings.md` in the kept directory. The title names the review's number and the initiative. Rests on supervision#r74, design-decision/review-of-work-items (a fix work-item has `findings:`), and supervision#r4, r22 and r56: a work-item's scenarios are its accepted ones, and one with none is refused. No `fixes:` field is written, because no line asks for it.
9. **The drafted item is unread by the next review.** The draft's `work add` commit is not a kept review's own commit. So once the fix work-item is green, r27 starts a new review over it, and `Reviews.unread` stays as it is. Rests on supervision#r27 and r50 (C3).
10. **Drafting goes through `workqueue.add` in-process.** That is the function `work add` runs: its refusals, its numbering and its commit `work add: <initiative>/<name> drafted`. It gets new keyword parameters, not new `work add` options, because no line asks for a `--retires` or `--findings` on the command. After the drafting commits, the run pushes the initiative branch. Rests on supervision#r72 ("with `work add`") and r38 (push after each commit), as the notes' section 5 shows `work add` does not push.
11. **The run goes on after a fix draft.** After the review is kept and the fix work-item drafted, `Run.run` goes back to the pull. It exits as r9, r32 and r52 say once no work-item can move and no review is due. Rests on supervision#r1 and r27.

## 4. Tests the decisions break

None. What I verified, from the notes' section 4 and by reading `workqueue.add`, `Run.run` and `Reviews.branch_review`:

- `tests/scripts/test_work_item_ids.py:66,73` and `test_work_add_title.py:35` call `add` positionally. Decision 10's parameters are keywords with defaults, so the calls stay as they are.
- The reviewers in `supervision_review_steps.py` give status DONE with "Nothing found." and no `questions`. Under decision 6 they list nothing, nothing is drafted and the loop of decision 11 ends after one review. So the review counts and exits in `test_supervision.py` (r27, r47-r51, r75, r76) hold.
- No supervision step writes a formulated proposal, so decisions 1 to 3 draft nothing in any existing scenario. The exit scenarios of r9, r81 and r82 hold.
- The `work add` scenarios in `test_work_queue.py` take the same path as before.

## 5. Open cases

The implementer names these in the report; the scenarios do not settle them.

- The findings' lines name work-items of different proposals, name no work-item of the initiative, or name one with no `part_of`.
- A reviewer that lists fix-now findings at every review. The r74 scenario's reviewer must not do this, or decision 11's loop would draft a second fix work-item and the Then "one work-item was drafted" would fail. How the step's stub reviewer behaves at a second review, or what stops the fix work-item first, is the implementer's to name.
- The push after a draft fails (decision 10). Today's push failures say why and exit with an error (r53, r10); which of these a failed draft push follows is not given.
- A kept review with no result file, or with `questions` given as one string: decision 6, and the Implementation note that one string is one question. Defect D1 of the notes (a review that ends at its turn limit is kept and exits 0) is not this work-item's to fix.
- A branch review over an initiative with no work-items and no formulated proposal (defect D2) is r27 as written, and stays as it is.
- An `adds` or `changes` entry that names a range (`thing#r3-r6`), when matched against a deprecated scenario's single `@r` tag.
