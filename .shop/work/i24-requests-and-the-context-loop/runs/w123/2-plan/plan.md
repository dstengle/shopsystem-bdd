# Plan of w123: work status and work note

Accepts work-queue r16-r21 (features/work-queue.feature, lines 239-312). No Retires section, no Rulings.

## 1. What goes green

All six fail today at their first undefined Given (notes section 1). `scripts/work` has no `status` or `note` subcommand: argparse refuses both with exit 2 (notes section 2).

- **work-queue#r16**, "status of an initiative prints where it stands, for a session to start from". Red: the Given "an initiative i1 ... that is neither done nor abandoned, whose capability-proposal p1 is approved" is undefined, and so are the Givens and Thens after it. No `status` command exists.
- **work-queue#r17**, "status with no initiative prints each initiative that is neither done nor abandoned". Red: the Given at feature 261 is undefined. Its Then "work prints what `work status i1` prints and what `work status i2` prints" matches no step. Nothing lists the open initiatives.
- **work-queue#r18**, "status with --json prints its result as one JSON object". Red: the Given at 272 is undefined. "it gives i1's status and w1 with drafted" does not fit the existing `gives` step, which splits on " in ". There is no `--json` on status.
- **work-queue#r19**, "note appends the line, with the date, to the initiative's ledger". Red: the ledger Given (280) is undefined, and so are the Thens at 282 and 283. No `note` command exists.
- **work-queue#r20**, "note commits the ledger on the current branch". Red: the ledger Given is undefined. Correcting the notes' question 5: test_work_queue.py line 22 imports `*` from work_queue_git_steps. So "main has a new last commit, which holds ... as work left it" and "nothing under .shop/work/ differs from main's last commit" are already defined, along with "the repository is a git repository on the branch main, everything in it committed". Once the Given exists, only the command is missing.
- **work-queue#r21**, Outline "note with a line break in it is refused, and nothing changes", 7 examples (newline, U+000B, U+000C, U+000D, U+0085, U+2028, U+2029). Red: the ledger Given is undefined. The When "... with a line of two lines broken by <line break>" matches no step (`run_work_newline` wants other text). "saying that a note is one line", ".shop/work/i1/ledger.md is as it was" and "main's last commit is the one it was" are undefined.

Deprecated scenarios retired: none.

## 2. Where the change lands

- `scripts/work`: adds the subcommands `status` (an optional initiative, `--json`) and `note` (initiative, line) to the parser and the dispatch table.
- `scripts/workqueue_status.py` (new): the r16-r18 reader. Lists the open initiatives. For each one it gives the initiative's status, the proposals and work-items with their statuses, each work-item's open questions, the branch and whether the remote has every commit of it, the checkout's changed and untracked files, the ledger's last ten lines and its last `next:` line. It renders all of this as text or as one JSON object.
- `scripts/workqueue_note.py` (new): the r19-r21 writer. It checks for line breaks with `workqueue_answer.LINE_BREAKS`, checks that the initiative exists, appends with `workqueue.append` and commits with `workqueue.committed`.
- `scripts/model_work.py`: `read_work` no longer reads `ledger.md` as a part (decision D4). One condition beside the existing `initiative.md` exclusion.
- `CLAUDE.md`: one module-map row each for `workqueue_status.py` and `workqueue_note.py`.
- `tests/scenarios/test_work_queue.py`: imports the two new step modules.
- `tests/scenarios/work_queue_status_steps.py` (new): the r16-r18 Givens and Thens.
- `tests/scenarios/work_queue_note_steps.py` (new): the r19-r21 ledger Given, the line-break When for the Outline, and the Thens.

Changes from the researcher's set:
- Added `scripts/model_work.py` (D4).
- Left out `scripts/supervise.py` and `scripts/supervise_faults.py`, which the researcher listed as possible. The status reader rebuilds their small open-question and push-check rules in its own module instead of importing `work run`'s supervisor (D6).
- `scripts/workqueue.py` (262 lines, room for 38) is used but not edited.

## 3. Decisions

- **D1. The initiative branch is the checkout's current branch.** This is the branch `work run` commits on, as supervise takes it, so status prints the name of the HEAD branch. The remote is that branch's upstream remote, else `origin`. "Has every commit" means the branch's head is contained in the remote's branch of the same name. The r16 Given therefore leaves i1-delivery checked out, one commit ahead of a bare remote. Rests on: the glossary in spec/index.md ("initiative branch", "remote"); design-decision/work-file-forms, whose initiative fields include no branch, so there is nowhere to read a recorded name from (the notes' reading B has no form to stand on); work-queue#r16. With several initiatives (r17), every block names that same branch.
- **D2. The ledger line has the same form as `work answer`'s dated line.** That is a bullet, then the ISO date (`YYYY-MM-DD`) of the day the command runs, a colon and a space, then the line as given. "The note" in r16 is the text after that date-and-colon prefix. Rests on: work-queue#r19 ("with the date") and #r16 (the note is the text after the date `work note` writes). The form copies #r13's dated answer line, so the repository has one dated-line form.
- **D3. Status is one block per initiative, and the no-argument form joins those blocks.** `work status <i>` prints one block. `work status` prints, in initiative-name order, exactly the block that `work status <i>` would print for each initiative whose `initiative.md` status is neither `done` nor `abandoned`. The checkout and branch facts repeat in each block. A named initiative is printed whatever its status (r16 excludes none). An unknown initiative is refused with an error that names it. No open initiative at all prints nothing and exits successfully. Rests on: work-queue#r16, #r17 ("what r16 gives for each"), #r7, design-decision/query-commands-answer-in-their-output.
- **D4. `model check` leaves `ledger.md` out of the initiative's parts.** Without this, every note makes `model check` report "needs an id and a kind" for the ledger (notes section 2, probe). Every other non-part `*.md`, p1.md with no id included, stays a file problem. Rests on: design-decision/the-ledger-is-tracked (the ledger is `.shop/work/<initiative>/ledger.md`, which rules out moving it to another name, the notes' reading B), and design-model-check r27, whose file problems are about parts, which a ledger is not.
- **D5. The JSON is one object holding an `initiatives` list, whether or not an initiative is named.** Each entry carries the initiative's id and status, its proposals and work-items (each with id and status, a work-item also with its open questions), its branch with a pushed flag, the uncommitted and untracked files, the ledger's last ten lines and the last `next:` line (null when there is none). The step "it gives i1's status and w1 with drafted" is a new step in work_queue_status_steps.py that reads this object. The feature stays as written (the notes' reading A). Rests on: work-queue#r18; design-decision/query-commands-answer-in-their-output (the keys are Implementation).
- **D6. A question is open by the rule `work run` uses.** The n-th bullet of `## Answers` answers the n-th bullet of `## Questions`, and the open questions are the bullets past the answered ones. workqueue_status reads the sections itself and does not import supervise. Rests on: the supervision capability's Implementation (the n-th answer rule); work-queue#r16 ("its open questions").
- **D7. `note` follows `answer`'s order of refusals and its write path.** The checks run in this order: line break (message: a note is one line), then the initiative name and whether it exists (r7), then the append and the commit inside `workqueue.committed`. If the commit fails, the ledger is put back. A ledger that does not exist yet is created by the first note. Only `ledger.md` is committed. The commit goes on the current branch with a message naming `work note` and the initiative. Rests on: work-queue#r19, #r20, #r21, #r7; design-decision/the-ledger-is-tracked (each initiative keeps one ledger).
- **D8. `status` reads and never transitions.** It reports each work-item's status as its file gives it, as `show` does, and does not apply r6's log agreement check. Rests on: work-queue#r16 (it prints, and moves nothing); work-queue#r6, which concerns transitions only.
- **D9. Uncommitted and untracked files come from git's view of the whole checkout.** Tracked files with changes, staged or not, and untracked files that git does not ignore, listed file by file (git status with untracked files listed in full). Rests on: work-queue#r16.

## 4. Tests the decisions break

None. What was checked:
- The notes' section 4: no test names the refused `status` or `note` choices, and the tests/scripts work tests pass (17).
- D4: no feature or test asserts a file problem for a non-part `*.md` named `ledger.md`. The design-model-check rows "the part p1.md has no id" (feature 300) and "initiative.md has no id" (299) still hold, because only the name `ledger.md` is left out.
- The new Givens do not collide with the existing `with_items` regex, which needs "whose work-item" right after ".shop/work/". "that is neither ..." and "whose ledger ..." do not match it.
- D1-D3 and D5-D9 add code and change no existing test's target.

## 5. Open cases (for the implementer to name, not to choose)

- Status where the checkout is not a git repository, has no commit, has a detached HEAD, or has no remote or no remote branch of that name. The r17 and r18 scenarios run without a remote. Status must still answer and exit successfully (query-commands-answer-in-their-output), so name what it prints for "pushed" in each case.
- Ledger lines not of D2's form, for example lines written by hand: whether they count toward the last ten (r16 says lines, so they would) and how they fare in the `next:` search.
- A ledger with fewer than ten lines, or none: print what there is. No `next:` line: say so, or null in JSON.
- A work-item with `## Answers` bullets beyond its questions.
- `note` with an empty line or only spaces; `note` on a `done` or `abandoned` initiative.
- `note` when the checkout has other uncommitted changes, including other files under `.shop/work/`: only the ledger is committed (D7). Name it if a test touches it.
- Initiative-name order with names like i2 and i10.
