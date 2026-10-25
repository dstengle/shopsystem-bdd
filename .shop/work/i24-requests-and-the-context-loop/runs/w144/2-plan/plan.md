# Plan of w144: initiative-round appends its ledger line with work note

## 1. What goes green

- **spec-integration#r40**: when `initiative-round` finishes a round, it appends one line to the initiative's
  ledger with `work note`, naming the kind, the round, and what the round ended with or the answers it applied.
  - Scenarios: none. w144 is a guarantees work-item (spec-integration is `group: guarantees`,
    design-decision/workflow-capabilities-are-guarantees). Its review judges it.
  - Why it fails today (notes §2, §3): agents/initiative-round.md "The ledger" still sends the line to
    `.shop/scratch/run/ledger-<initiative>.md`, which is never committed. And a round started by `work run` could not run
    `work note` anyway: scripts/supervise_worker.py gives the round kinds' Bash no `work` script at all.
- Retires: nothing (the work-item has no Retires section and no Rulings).

## 2. Where the change lands

- `agents/initiative-round.md`: rewrite "The ledger". The round appends its line with
  `python3 <Scripts>/work note <initiative> "<line>"` into `.shop/work/<initiative>/ledger.md`, after its job's
  own commit and before it replies. Say where the initiative's name comes from (decision 2), that the line is a single
  line, and what goes in the line for each kind (the existing wording stays: counts and path for `integrate`/`gate`,
  the answers applied for `apply`, the commit for `formulate`). Drop "create it if it is not there".
- `scripts/supervise_worker.py`: give every kind in `ROUNDS` a Bash allowance for `work note` alone, under the
  plugin's script path. Rewrite the comment above `STAGE_SCRIPTS` (it says "never `work`"): no stage gets `work`; a
  round gets only its `note` subcommand, which moves no status. 238 lines now, so there is room.
- `skills/integrating-a-proposal/SKILL.md`: the dispatch steps (1, the answers round, 3) also give the round the
  initiative's name. The "If you are `initiative-round`" paragraph says the round ends with its ledger line by
  `work note` (see the agent's "The ledger").
- `skills/formulating-features/SKILL.md`: the same two changes for its formulation-round dispatch and its
  "If you are `initiative-round`" paragraph.

Differences from the researcher's set (agent file and supervise_worker.py): I add the two skills. The work-item
names them, and decision 2 needs their dispatches to carry the initiative's name. I leave out
`.shop/delivery.toml`: the file does not exist in this repository. I also leave out
`skills/delivering-an-initiative/SKILL.md` (its old path belongs to delivery r15, another work-item) and decision 0059,
which is historical.

## 3. Decisions

1. **A round may run `work note` and no other `work` subcommand.** The allowance names the `note` subcommand,
   so it does not cover all of `work`. Rests on spec-integration#r40 (the round writes with `work note`),
   design-decision/the-ledger-is-tracked (`initiative-round` writes the ledger with `work note`) and
   design-decision/the-context-runs-without-a-coordinator (`work run` alone moves nodes through their transitions,
   so a worker that could run `work` broadly could move statuses).
2. **The initiative's name comes from the round's input.**
   - Rounds started by `work run`: the brief already has a `Capability-proposal: .shop/work/<initiative>/<name>.md`
     line (notes §2, supervise_brief.py), and the initiative is that path's directory. supervise_brief.py does not
     change.
   - Rounds the skills dispatch: the dispatch names the initiative.
   - Rests on spec-integration#r40 ("the initiative's ledger") and the-ledger-is-tracked.
3. **The ledger line is written after the round's own commit, as a separate commit.** `work note` commits only the
   ledger, by pathspec (notes §2: other staged files stay staged), so `apply` still commits `spec/` alone
   (spec-integration#r6) and `formulate` still commits its feature files with their test files. The line goes on the
   branch the round runs on, which is the round's worktree branch under `work run` (notes §2 probe).
4. **The line is a single line.** `work note` refuses a line break (notes §2). The round collapses its summary to one
   line. Rests on spec-integration#r40 ("one line").

## 4. Tests the decisions break

None. I checked this from the notes §4, by search over tests/ for `ledger`, `initiative-round` and `allowedTools`:
- test_agents.py's r1 and r5 tests read initiative-round's `Agent` tool and its model, and neither changes.
- `ResultFirst` does not read initiative-round.
- supervision_rounds_steps.py finds rounds by their brief title, not by their tool list.
- supervision_then_workers.py checks the researcher's list and that no stage has a bare Write or Edit. Decision 1
  adds a Bash entry and no Write or Edit.
- The work_queue_note and migration_session steps test `work note` itself, which does not change.

## 5. Open cases

- A round whose input gives no initiative, for example an older dispatch or a brief with no `Capability-proposal:`
  line. It cannot write the line. Whether it replies `BLOCKED` or replies with its work and says the line was not
  written is for the implementer to name in the agent file.
- `work note` refusing the line (a missing initiative directory, or a run outside a repository). What the round does
  with that refusal, and whether its reply says so.
- A round that ends `BLOCKED`. Does it still append a line naming the block? r40 says "finishes a round".
- Defect D1 (notes §6): `work note` accepts an empty text. This is not w144's to fix. The implementer may name it in
  their report.
