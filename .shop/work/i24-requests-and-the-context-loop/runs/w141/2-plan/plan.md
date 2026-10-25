# Plan of w141: delivering-an-initiative only starts work run

## 1. What goes green

No scenario. delivery is `group: guarantees` (design-decision/workflow-capabilities-are-guarantees); no feature
file carries a delivery id (notes §1), so nothing is red and nothing turns green by a test. The review judges each
accepted line against `skills/delivering-an-initiative/SKILL.md`:

- delivery#r4: the skill starts `work run` when asked. Today it is out of line because it starts `work run` only
  after drafting and committing work-items (notes §3, the "Drafting", "Commit them, alone" and "Run work run" rows).
- delivery#r10: the skill drafts a trial's fix as a work-item. Today it is out of line because it drafts a review's
  fixes as well as a trial's ("Fixes" bullet 1).
- delivery#r19, delivery#r20: the skill starts no `claude -p` session and merges no branch. Today the skill says
  neither in so many words, and nothing in it forbids either.
- delivery#r21: the skill puts a tool `work run` disallowed to the person as a question, naming the stage. Today it
  is absent.
- delivery#r22: the skill puts a change `work run` cannot deliver to the person as a question, changing nothing.
  Today it is absent.

Retired ids r1, r2, r3, r8, r9, r17, r18 lose their text in the skill. The work-item has no `## Retires` section, and
no deprecated scenario is retired.

## 2. Where the change lands

- `skills/delivering-an-initiative/SKILL.md`: the frontmatter description and the Overview say that the skill starts
  `work run` and shows what it printed, and that `work run` does the drafting. The "Drafting" section (steps 1-5,
  the refusal clean-up and the table) goes, and so does "Commit them, alone". "Before anything" loses the
  formulated-proposal condition (decision 1). "Run work run" starts on the ask. "When it exits" says `awaiting-answer`
  and gains the r21 and r22 questions. "Fixes" narrows to a trial's fix (r10). The Red Flags follow the new text.

This is the researcher's file set, unchanged. No script and no test changes: `work run` and `work add` already do
what the skill relies on (notes §2), and no test reads the skill (notes §4). README.md still describes the drafting
skill (notes §7). It stays out of the set because no requirement or test names it (see Open cases).

## 3. Decisions

1. **Start `work run` on the ask, whatever the proposals' statuses.** The precondition "no capability-proposal is
   `formulated`" goes. With nothing to draft, the skill does not stop and does not commit: it starts `work run`.
   The precondition is dropped because `work run` takes every transition of the initiative's nodes, including its
   rounds and its drafting, and delivery#r4 has no condition. Rests on delivery#r4 and
   design-decision/the-context-runs-without-a-coordinator. The other stop conditions remain under delivery#r7:
   uncommitted changes, no such initiative, and no `work` with `run`.
2. **The skill drafts nothing itself, with one exception: a trial's fix.** Nothing in the skill drafts work-items
   from proposals. Nothing checks reworded scenarios against accepts. Nothing writes `## Retires`, and the skill
   makes no commit of its own. A trial's fix is drafted with `work add` as today: one `--accepts` for each id, the id
   that `work add` prints, and the commit that `work add` makes. A review's fix-now findings are `work run`'s to
   draft, and the skill does not draft them. Rests on delivery#r10, the retirement of r1-r3, r8, r9, r17 and r18,
   and design-decision/the-context-runs-without-a-coordinator ("drafts the work-items of a formulated proposal and
   of a branch review's fix-now findings").
3. **An explicit prohibition.** The skill says that it starts no `claude -p` session and merges no branch, even when
   `work run` fails. Each prohibition is also a Red Flag. Rests on delivery#r19, delivery#r20 and
   design-decision/the-context-runs-without-a-coordinator.
4. **r21 acts on what `work run` printed.** The skill puts a tool to the person as a question only when `work run`'s
   printout says that a worker needed a tool it does not allow. The question names the tool and the stage as
   printed. The skill does not infer a refused tool from a fault line, a worker's file or a stage directory. Rests on
   delivery#r5 and delivery#r6. Whether `work run` prints a refused tool is a matter for supervision, not for this
   skill (notes D3; see Open cases).
5. **r22 covers what `work run` reported, and r7 covers the skill's own stops.** After the printout (r6), the skill
   handles each `failed` work-item, and a `work: <why>` stop of `work run`, as one question to the person. The
   question names the work-item or the change and its fault or reason, as printed. The skill does not retry, does
   not re-run `work run`, edits no file and dispatches nobody to deliver the change. delivery#r7 stays for the
   conditions the skill checks before it starts `work run`, and there the skill stops and says why. The split
   follows the two lines' wording: "`work run` cannot deliver a change" against "`delivering-an-initiative` cannot do
   what it was asked". Rests on delivery#r22, delivery#r7 and design-decision/the-context-runs-without-a-coordinator.
6. **`awaiting-answer`, not `awaiting-ruling`.** The exit text names the status that `work run` prints (notes D2).
   Rests on delivery#r6 ("as `work run` printed them").
7. **Lines this work-item does not accept stay as they are.** The `formulate`-round bullet (r12), the dispatch
   bullets (r13, r14) and the ledger bullets (r15) are left for their own work-items: notes §3 gives r15 to w142.
   The skill text keeps "change no code yourself" (r11) and the rule that it reads no source
   (design-decision/spec-writers-blind-to-code).

## 4. Tests the decisions break

None. Notes §4 searched tests/ for `SKILL`, `skills/` and `delivering`. The only matches are `Skill(...)` strings in
allowedTools, in the supervision steps and in stub_claude.py, and neither reads this skill. The callers of `work add`
(test_work_add_title.py, test_work_item_ids.py, test_work_withdraw.py, test_work_queue.py) do not assert the
skill's text. No decision changes a script, so no script test is touched.

## 5. Open cases

- Today `work run` prints nothing that says a worker was refused a tool: a refusal becomes a `failed` work-item with
  a fault (notes D3). Until supervision prints a refused tool, r21's question can never fire. Name this in the
  report, and do not work around it in the skill.
- Today `work run` on an initiative whose formulated proposal has no work-item exits 0 and prints nothing (notes D1).
  Supervision r72 (w138) is not in code yet. The skill shows the empty printout and exit 0 as printed. Name whether
  the exit-code line ("0, every work-item green") reads right over an empty list.
- Writing no `## Retires` relies on supervision r73 (w138). w141 has no `blocked_by` on w138.
- A trial's fix has `--part-of` and `--under` values to give `work add`. Name which proposal the text points to, or
  leave the current invocation's wording.
- `work run` can refuse to start, for example when it is started from a worker (notes §2). Name whether the skill
  treats this as an r22 question or an r7 stop.
- The drafting lines in README.md (57, 149, 206, 229 and 250) go stale. Name them in the report.
- Name whether "What you read" still needs `spec/` and `features/` once the skill no longer drafts from proposals.
