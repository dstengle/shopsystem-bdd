---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-27-applying-items-to-a-specification-in-place-of-laying
kind: design
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-27
---

# Applying items to a specification in place of laying

The design of b861 (quote-108, quote-117, quote-118): the laying area retired into the specification service's `apply`, each task's workspace holding only its own item's lines, the batch's specification rebuilt from the base at submit, and nothing lifted. Drafted by a fresh agent from main at c1dd6a240; the session settled its open questions as below.

## Settled

- `apply` is kept; its homonym with tracking's `apply` (a retirement list) passes v_t15 and is only a coupling-report entry.
- Amending a blocker applies it again on each dependent task's workspace too, in the same command (E2 option a); a blocker reopened at opening reopens its dependents.
- No adapter seam: `$SHOPSYSTEM_LAYING` goes; the batches scenarios use real failing worlds (readiness_world's `v_zz`, `$SHOPSYSTEM_GENERATE_TIMEOUT`); a technical-architecture decision supersedes 0150.
- Readiness and `spec check --item` call the whole `apply`; its cost is measured in item 1 and `lay_only` dropped once it holds.
- `done` refuses a task commit under `features/` (E1), so the rebuild never drops a hand edit.
- Opening time is measured with `measure batch` before item 4 and after it (directive-11).
- b773 (the laying package's import contract) becomes item 6's "execution imports only `spec_apply` from specification".



The design keeps the names you asked for. **`apply(item, specification)`** and the widened **`check(specification, capability, item)`** both fit the lexicon. The widened check is said "validates this specification with the item", as checking r152–r155 and r160 already say it.

One wrinkle: `apply` is already a verb in the tracking layer (`→ operation drafting.apply`, "applies <retirement list> to <item>"). The new frame, "<actor> applies <item> to <specification>", takes different kinds in its slots, so v_t15 passes and the grammar reads it one way. `spec coupling` will list it as a homonym between tracking and specification. That is harmless, but if you would rather avoid it, `admit` is the nearest other word. I recommend keeping `apply`.

## A. Requirement lines

### laying (all 47 live lines retire; the capability is deleted)
- **Lift lines: retire, no replacement.** r2 (lifted item no longer held), r5 (lift keeps out another retiring requirement), r43 (lift restores restated operation), r44 (lift keeps another item's member line), r45 (lift of another item keeps port area), r46 (lift takes out the port import), r47 (lift leaves out a retired line's Relied on by).
- **Lay lines: retire and replace in a new capability `applying`.** That capability has area `specification`, specifies `service specification`, and is narrated by the batches service. The rewrite is the same for each line: "when the batches service lays the item in a workspace, the laying service shall keep …" becomes "when the batches service applies the item to a specification, the specification service shall keep …".
  - This covers r7, r8, r21–r41, r48 and r49. The rest of each line is unchanged, for example:
    - r22: "While `universal` does not exist and a universal condition is in an item, when the batches service applies the item to a specification, the specification service shall keep `universal` and set the language of `universal` to `codified-2`."
    - r32: "…applies the item to a specification, the specification service shall keep the model line in the domain model and keep a domain model that does not hold the operation."
  - r21 becomes: "While an item holds a requirement, when the batches service applies the item to a specification, the specification service shall keep the specification that holds the requirement." This needs the new relation `specification holds → requirement` (section B).
- **Prepare lines: retire and replace in `applying`,** with prepare folded into apply and the "batch holds an item" premise dropped.
  - r6 → "While an item holds a requirement, when the batches service applies the item to a specification, the specification service shall keep a scenario that refers to the requirement id of the requirement."
  - r9 → "While a requirement of an item has a logical form, when the batches service applies the item to a specification, the specification service shall keep the logical form in the corpus."
  - r10 → "While a requirement id is in an item and a requirement in the corpus has the requirement id, when … applies the item to a specification, the specification service shall keep a corpus that does not hold the requirement."
  - r11 and r12: same rewrite.
  - r13 → "While no requirement of an item uses a construct and no construct catalogue exists, when … applies the item to a specification, the specification service shall keep no construct catalogue."
  - r14 → "When the batches service applies an item to a specification, the specification service shall keep an index file that conforms to the index form."
  - r15 and r16 → "While a capability has no requirement (has a requirement), when the batches service applies an item to a specification, the specification service shall keep an index file that does not hold (holds) the capability."
  - r17 and r18: premises unchanged, trigger and response rewritten as above.
- **Check lines: retire, moved to `checking` under validate.**
  - r3: retire with no replacement; checking#r155 already says it.
  - r4 → checking: "While an item holds no requirement that violates a rule whose severity is `error`, when the person validates this specification with the item, the specification service shall return no requirement that violates a rule whose severity is `error`."
  - r19 → checking: "While an item holds a port line that governs an operation and every port line that governs the operation is in the item and the operation has an operation outcome and no core line handles the operation outcome and no port line excludes the operation outcome, if the person validates this specification with the item, then the specification service shall fail the check and name the operation outcome."
  - r20 → checking: same premises as r20, "…if the person validates this specification with the item, then the specification service shall fail the check and name the core line and `v_m9`."
- **New checking line for "less what the root violated before":** "While a requirement of this specification violates a rule whose severity is `error` and no item holds the requirement, when the person validates this specification with an item, the specification service shall return no requirement that violates the rule."

### batches
- **Retire, no replacement:**
  - r180, r188, r189: "lay completes → check", "lay completes → prepare", "prepare completes → check". These become apply's own behaviour.
  - r182 (park lifts from the batch's workspace) and r183 (lift completes → kept change). Nothing is lifted any more.
  - r176 (park refused while the generator is unresponsive). Park no longer generates anything.
- **Retire and replace:**
  - r179 → "…when the person opens a batch, the batches service shall allocate the item, keep a batch that holds the item, keep a batch plan of the batch and apply the item to the specification of the workspace of the task of the item."
  - New: "When the specification service completes the request to apply an item to a specification, the batches service shall validate the specification with the item."
  - r181 → "When the specification service fails the check of a specification with an item, the batches service shall reopen the item and name every rule that a requirement of the item violates."
  - r184 → "When the specification service completes the request to apply an item to the specification of the workspace of a task, the batches service shall keep a kept change that cites the item."
  - r185 → "While an item in a batch is `in-batch` and a task of the item is `running`, when the person amends the item, the batches service shall apply the item to the specification of the workspace of the task."
  - r170 and r172: "workspace of the batch" becomes "workspace of the task".
  - r175: "the workspace of the batch has a feature generator" becomes "the workspace of the task has a feature generator".
  - r174 and r178 (a park re-accepts the decision) move to submit time: "While the status of an item in a batch is `needs-input` and the item holds a requirement that retires the requirement id of a requirement that enforces a design-decision, when the person submits the batch, the batches service shall keep a proposed change of the batch that holds no design-decision that supersedes the design-decision." r178's two-item case becomes the same line with "and another item in the batch is `in-batch` and holds another requirement that retires …", ending "… that holds a design-decision that supersedes the design-decision".
- **New lines (dependencies):**
  - "While an item in a batch is `in-batch` and the item has a dependency on another item in the batch, when the person opens the batch, the batches service shall keep the workspace of the task of the item that holds the requirement of the other item."
  - "While an item in a batch is `in-batch` and the item has a dependency on another item in the batch, when a session parks the other item, the batches service shall suspend the item with a question."
- **Unchanged text, realisation changes:** r61, r62, r70 and r78 now hold without the tested tree, because a task's workspace never holds another item's lines. r109's "a workspace of a batch" is now the task's. r150, r173, r177 and r190–r192 now happen on the task's workspace. r83, r96, r111, r125, r143, r158, r161–r163 and r171 do not change.

### reviews
- r13: retire and replace. "…and the workspace of a task of the item holds an amendment that cites the item and a scenario of the item succeeds in the workspace of the batch, when the person submits the batch, …" Today the amendment sits on the batch's workspace; it no longer will.
- **New (rebuild):** "While an item in a batch is `in-batch`, when the person submits the batch, the batches service shall apply the item to the specification of the workspace of the batch."
- **New:** "While the status of an item in a batch is `needs-input` and the item holds a requirement, when the person submits the batch, the batches service shall keep a proposed change of the batch that does not hold the requirement."
- **Unchanged:** r1–r12 and r14. r2 now holds because a parked task is never merged. r7 and r8 now concern only code files.

### readiness / items, checking, drafting, parsing, product
- **Unchanged.** This covers the bar lines, checking r152–r155 and r160, parsing r19, r20 and r22, product r58 and every drafting line. Only their implementation moves onto apply.
- readiness.md's prose at lines 17–60 says "laid over". It is Purpose and notes, not requirements, so it can be reworded in place.
- No design-decision's `enforced_by` names a laying id or batches r179–r189, so decision_successor fires on none of these retirements.

## B. Model and vocabulary

- **Retire `spec/model/laying.md`** and its Composition row (`| laying | port | laying |`). Drop `laying` from execution.md's `imports:`.
- **specification.md, `service specification`:**
  - Add `operation apply(item, specification)  outcomes: done → the specification | refused: feature generator unresponsive`. Several items are one request per item, applied in pick order. A batch's specification is the workspace's; readiness's is a copy.
  - `check(specification, capability, item)` keeps its signature. Its meaning is widened: with an item, it checks only the error-severity violations the item's requirements bring that the specification without the item does not have.
  - `object specification` gains `relations: holds → requirement | capability | feature | corpus | index file | adapter contract (many)`. Today it has none.
- **execution.md:** `object workspace` gains `relations: has → specification (one)`. Its `batches` operations are unchanged; park and amend are still operations, they just do less.
- **Vocabulary:**
  - Retire the whole laying layer: **the laying service**, **lay**, **lift**, **check** (verb → laying.check), **prepare** (verb → laying.prepare).
  - Add to specification's layer: **apply** (verb, action) → operation specification.apply. "An item's lines, model lines, terms and other pieces taken into a specification, and the specification made whole there: its features, corpus, catalogues, Composition, annotations and the successors of the decisions it leaves unenforced. Forms: applies, applied. Frame: <actor> applies <item> to <specification>."
  - Reword in execution: **amend** ("An item's lines applied again to the specification of its task's workspace after they changed") and **amendment** ("…applying an amended item's requirements again on its task's workspace").
  - Reword in measurement: **opening time** ("…its application of each item to its task's workspace and its run of their scenarios").
- **Decisions:**
  - Supersede 0150 ("the laying port is wired to the in-process adapter") with a technical-architecture decision: "Execution reaches the specification through the specification service's module `spec_apply`, in process; there is no adapter seam."
  - Alternatively, if the batches scenarios still need to fail a check on demand, keep the seam as one environment variable named in that decision. I recommend dropping it: readiness_world's `v_zz` line already makes a real check fail.
  - 0125 stays as it is.

## C. Code

**New**
- `spec_apply.py`: `apply(root, items)` lays each item (`backlog_lines.lay_onto` plus `unbuilt:`), then prepares once for all of them. The prepare code moves here from laying_inprocess: generate, corpus, `decision_successor.lay`, `batch_reached`, Composition, annotate and catalogues. It answers with a domain_envelope Response.
- The widened check, `violating` past `before`, moves from laying_inprocess into `spec_apply` or a sibling `spec_apply_check.py` to stay under 300 lines. The violations of the base's committed state (`readiness_bound.before`) are kept on disk keyed by the base's sha, so the parallel per-task applies solve it once.

**Delete**
- `laying.py`, `laying_inprocess.py` (contents moved to spec_apply), `batch_parked.py` (take-out, tested tree, `amended`, `base_of`), `backlog_area_move_unlay.py` (all of it is unlay, plus `put_element`, which only the retire unlay uses).
- Tests and scenarios: `tests/scenarios/stand_in_laying.py`, `laying_handlers_lift.py`, `laying_handlers_retire.py`, `batches_handlers_relaid.py`, `batches_handlers_laying.py` (or rewritten over a real failing world), `test_laying.py`, `features/laying.feature`, `tests/scripts/test_batch_parked.py`, `test_backlog_adapter_unlay.py`. The unlay cases in test_backlog_{retires,retires_dropped,retires_group,adapter,adapter_ops,capability,retire,relied,forms,forms_tidy,port,pack,universal,recodify,serves}.py, test_decision_successor.py and test_readiness_lay_model.py go too.

**Change**
- **backlog_lines, backlog_{adapter,adapter_ops,capability,forms,import,model,model_area,model_elements,model_ops,pack,port,recodify,retire_lay,retires,serves,universal}:** delete their unlay halves, about 550 lines.
  - `backlog_model_ops.held` and `at_base` are also read by the unrestate path only, so they go.
  - What still needs a reverse: nothing in the batch. backlog_reword's `_unretiring` edits the item, not a spec, so it stays.
- **decision_successor:** drop `unlay` and the relay to a later lay. The rebuild computes successors once from the surviving items.
- **batch_start:** for each picked item, create its task's worktree at open: from the base, or from the blocker's task branch when there is a dependency. Then apply, check, run batch_laid's passing-scenario check and commit, with the tasks in parallel. A failed item is reopened and the others are not laid again, because the pick's ids already avoid collisions. There is no lay commit on `batch-<n>`.
- **batch_tasks:** `resume` reuses the worktree the open made. `lines_commit` becomes "the task's apply commit". `done`'s tested tree goes. `park` becomes: no take-out, the item and every in-batch item that depends on it suspended, the branch kept.
- **batch_review:** the rebuild. Reset the batch worktree to the base, apply the surviving items in pick order, then merge each surviving task branch with `--no-commit`. Restore the apply-owned paths from the rebuild: every path apply reported changing, plus `spec/` and `features/`. Drop from `unbuilt:` each id the task branch no longer lists (`batch_merge.built`). Commit. `_take_out_parked` goes.
- **batch_merge:** drop `reconciled`, `settled`, `MARK` and the `unbuilt:` conflict handling. Keep `clashes` and `clashing`, but for code paths only, and keep `built`.
- **batch_amend:** on the task branch only, restore the apply-owned paths from the base, apply the blockers then the item, and make one commit. There is no `Laid:` line, no base commit and no batch-branch relay, and `_based` goes.
- **batch_next / batch_broken / batch_fix:** small changes. The "fix task" conflict check (`_conflict`) now covers code files only.
- **Unchanged or nearly so:** `batch_laid` and `batch_reached` (now run per workspace), `batch_close` (mostly unchanged).
- **batch_driver:** rewrite the brief's lay bookkeeping text per task.
- **readiness_bar, spec_preview:** call `spec_apply.apply` on their copy. If apply's prepare runs (generate and annotate), spec_preview's `lay_only` carve-out (v_s3, v_a5) can go. This is a behaviour-preserving simplification of checking r153 and r154. product_trace_cli and `spec parse --item` reach it through `spec_preview.rooted`.
- **.importlinter:** remove `laying` and `laying_inprocess`. b773's contract becomes "execution imports, from specification, only `spec_apply`".
- **docs/reference/modules.md:** rows for the deleted modules out, new rows in. Also docs pages that say "lay" or "lift".

## D. Items, in build order

Each is estimated at 1000 changed lines or fewer. Generated features count, at about 14 lines per requirement.

1. **"The specification service applies an item to a specification and checks only what the item brings."** Adds `spec_apply` with `apply` and the widened check, extracted from laying_inprocess, which now delegates to it. Moves readiness_bar, spec_preview, `spec check/parse/trace --item` onto it. Adds the model's `apply`, the `specification holds` and `workspace has → specification` relations, and the vocabulary entry `apply`. New checking lines: r4's, r19's and r20's replacements plus the "less before" line. Retires laying r3, r4, r19 and r20. About 700 lines. Depends on nothing.
2. **"Applying an item keeps its pieces in the specification."** Retires laying r7, r8, r21–r41, r48 and r49 and restates them in the new capability `applying`. Moves laying_handlers_{pieces,model,model_then,areas} and laying_handlers.py's lay part to applying_handlers_*, with the When being apply. Most of the roughly 900 lines are the feature moving and handler renames. Depends on 1.
3. **"Applying an item prepares the specification: scenarios, corpus, catalogues, index."** Retires laying r6 and r9–r18, restates them in `applying`, and moves laying_handlers_{prepare,reached}. About 500 lines. Depends on 2.
4. **"Each task's workspace holds only its own item's lines, and the batch's specification is rebuilt from the base at submit."** This item and the next must ship together for the batch to work; I kept them apart for size. Covers batch_start per task (in parallel), batch_tasks (resume, park with dependents, no tested tree), batch_review's rebuild, batch_merge simplified, and batch_amend on the task only. Retires and replaces batches r179–r185, r188 and r189, and reviews r13. Adds the batches dependency lines, the reviews rebuild lines, and r174/r178 at submit. Moves batches handlers to per-task worlds. About 1000 lines, tight. If it runs over, take the amend part (r170, r172, r175, r185 and batch_amend) out as 4b, and make `work batch amend` refuse during 4a's window rather than leave it half-wired.
5. **"Nothing is lifted: a parked item is simply not merged."** Deletes batch_parked, `lift` and `unlay_lines`, every backlog_* unlay half, decision_successor.unlay and backlog_area_move_unlay, with their tests. Retires laying r2, r5 and r43–r47, and batches r176. Mostly deletions, about 1000 lines. Split per module family if needed: 5a covers model, ops, elements, move and retire; 5b covers lines, forms, capability, port, adapter, pack, serves, universal and retires. Depends on 4.
6. **"The laying area is retired."** Deletes laying.md and its vocabulary layer, the Composition row, `laying.py`, `laying_inprocess`, the stand-in, test_laying and laying.feature (by now empty or nearly). Changes the execution imports and `.importlinter`. Writes the decision superseding 0150. Rewords the amend, amendment and opening-time glosses and the docs. About 400 lines. Depends on 5.

## E. Risks and open questions

1. **Which paths apply owns at rebuild.**
   - Taking all of `spec/` and `features/` from the rebuild is safe, because task commits may not touch them; a chore already refuses `spec/`. The one exception is the task's `unbuilt:` removal, which `built` carries over.
   - `grammar/` is code in the plugin's own repository, so the rebuild must take only the paths apply reported changing (corpus, rules.md, constructs.md), never the whole folder.
   - If a task's handler commit hand-edits a feature (it shouldn't), the rebuild silently drops the edit. `done` should refuse a task commit under `features/`.
2. **Dependent task branches.** B branches from A's apply commit and sees A's code only if it merges A's branch, which `citable` already allows.
   - If A is amended, B's branch holds A's old lines. Options: (a) amending A re-applies on B too (restore, then apply A then B); (b) refuse amending A while B is running. I suggest (a), done in the same command.
   - If A is reopened at opening, B should be reopened too rather than applied alone; this needs a line.
   - Parking A parks B. Abandoning goes through as today.
3. **Opening time (directive-11).**
   - Applies run in parallel per task, so wall time is roughly one prepare plus fan-out overhead.
   - Each item that changes grammar 4's inputs (terms, model lines) compiles its own GF grammar, because the cache key is the vocabulary sha. The single lay today compiles once, so k vocabulary-changing items can mean k compiles. Mitigation: compile on N cores and share the base's `before` solve on disk.
   - Worktree creation moves from resume to open, so it is not new cost.
   - The win: a reopened item no longer re-lays the whole pick.
   - Measure with `measure batch`'s `opening_time_seconds` before item 4 and after it.
4. **Review time.** The rebuild adds one full apply and prepare (about one of today's openings) plus a grammar compile to every `work batch review`, including base-merge resubmits. The rebuilt branch's spec is deterministic from base plus items, so a resubmit after a base merge should rebuild on the new base rather than git-merge `spec/`.
5. **Decision successors and numbering.** Two task branches may each write successor 0NNN with the same number. That is harmless because the rebuild recomputes successors, but the brief and the per-task `work batch status` should not present a task's successor as final.
6. **Seam or no seam (directive-7).** Dropping `$SHOPSYSTEM_LAYING` means batches scenarios need real worlds for a failing check (available) and an unresponsive generator (r175: `$SHOPSYSTEM_GENERATE_TIMEOUT` already does it). Confirm you want no seam rather than keeping one under the new decision.
7. **Readiness speed.** If apply always prepares (annotate, catalogues, Composition), `work ready` and `spec check --item` get slower. Either accept it and drop `lay_only`, or let readiness call apply's lay half only. The second keeps two paths, which goes against the "one operation" decision; I'd measure first.
8. **The homonym `apply`** (tracking vs specification). It is only a coupling-report entry, but item 1 should check it against v_t15 as soon as the term is written.
