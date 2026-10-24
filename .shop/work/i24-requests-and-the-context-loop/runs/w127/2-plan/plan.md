# Plan of w127: work outcome and work turn

Accepts requests#r7, r15, r16, r17, r18. Rests on design-decision/requests-written-through-work (0067) and
design-decision/exits-are-successful-or-errors (0055). Planned from `runs/w127/1-research/notes.md`.

## 1. What goes green

All of them are red today for the same two reasons. No test module binds `features/requests.feature`, so every Given
is undefined (notes §1). And `scripts/work` has no `outcome` or `turn` subcommand, so each When gets argparse's
"invalid choice" and exits 2 (notes §2).

- requests#r15: "outcome in the upstream's turn writes the outcome given as the line outcome of the line named".
- requests#r16: "a side writing a part of a request in the other side's turn is refused, and nothing changes". Today
  the When exits 2 from argparse, not with the refusal.
- requests#r7: "turn passes the request's turn from the <side> to the <other side>" (Outline: upstream→asker,
  asker→upstream).
- requests#r17: "turn passing a request to its asker with a line that has <line 2> sets the request's status to
  awaiting-asker". This is an Outline with **no Examples table**, so `<line 2>` reaches the step as literal text
  (notes D2). It is the question below.
- requests#r18: "turn passing a request to its upstream sets the request's status to awaiting-upstream".

The work-item has no Retires section, so it retires no deprecated scenarios.

## 2. Where the change lands

- `scripts/work`: adds the `outcome <request> <n> <outcome>` and `turn <request>` subparsers and their dispatch in
  `main`. `request` and `resolve` are not added here: they belong to w126 and w128.
- `scripts/workqueue_request.py` (new; a new concern, per CLAUDE.md): keeps a request in the Implementation's form,
  `.shop/work/requests/q<n>.md` with frontmatter `status` and `turn` and the sections `## Lines` and `## Outcomes`.
  It reads a request by its id, writes a line outcome, passes the turn and sets the awaiting statuses. It raises the
  existing `Refused` from `workqueue.py`, which is imported and not changed.
- `CLAUDE.md`: a module-map row for `scripts/workqueue_request.py` (requests: the request file, line outcomes, turns).
- `tests/scenarios/test_requests.py` (new): binds `requests.feature`, as the other binding modules bind theirs.
- `tests/scenarios/requests_turn_steps.py` (new) has:
  - the Givens that write a request q1 for the asker ctx-a with a given turn, status and line outcomes;
  - the Whens that run `work outcome` and `work turn` under `--root`;
  - the Thens on line outcome, turn, status, refusal and "q1 is as it was".

Removed from the researcher's set: `scripts/workqueue.py` (only `Refused` is imported; `committed` is not used, see
D1), `scripts/model_work.py` and `scripts/model.lp` (no scenario of w127 needs the model to know request statuses),
and `tests/scenarios/conftest.py` (no helper is needed).

**Overlap with w126 (r1–r5), researched at the same time:** w126 writes the same request file, through the same kind
of module, and its r4/r5 scenarios use the same "a request q1 from the asker ctx-a whose turn is …" Givens. If w126 has
landed on the branch when this work starts, extend its request module, binding and step module, and do not make
second ones.

## 3. Decisions

- **D1. No commit yet.** `work outcome` and `work turn` write the request file but do not wrap the write in
  `workqueue.committed`. Committing is requests#r12, which w128 accepts. It is outside w127's accepts, and
  `committed` would refuse in the non-git directories the r15–r18 Givens use. To leave w128 one seam to wrap, put
  each command's write in a single call (notes §5, reading b).
- **D2. Which side runs a command comes from the command, not from a flag.** `work outcome` is the upstream's
  command (requests#r5: the upstream writes line outcomes only through `outcome` and `resolve`). So `outcome` in
  the asker's turn is refused, exits with an error (0055, via `Refused`) and names the asker's turn. The file is
  left byte for byte as it was (requests#r16).
- **D3. `work turn` is never refused on whose turn it is.** It writes neither side's part; it only passes the turn
  (0067; requests#r7). It flips `turn` between `asker` and `upstream` whatever the caller.
- **D4. `work outcome` writes any outcome word.** It writes the word it is given, without checking it against a
  vocabulary (requests#r15: "write `<outcome>`"). The scenarios use `accepted` and `question`. It writes only line
  n's outcome and leaves the other lines' outcomes and the `## Lines` section as they were (requests#r15, r4).
- **D5. Statuses set by `turn`:**
  - Passing to the asker sets `awaiting-asker` when any line has no line outcome, or an outcome other than accepted,
    refused or withdrawn (requests#r17).
  - Passing to the upstream always sets `awaiting-upstream` (requests#r18).
  - Passing to the asker when every line is settled leaves the status unchanged in w127. The accepted and refused
    statuses are requests#r8 and r9, which w128 accepts.
- **D6. Where a request is found.** A request id `q<n>` names `.shop/work/requests/q<n>.md` under `--root`, the
  file form in the capability's Implementation section. The form is `work`'s own (0067).

## 4. Tests the decisions break

None. Here is what was checked (notes §4):

- No test pins `work`'s subcommand list or help: a search for `invalid choice`, `choose from` and `usage:` found
  nothing.
- `tests/scenarios/test_work_queue.py` drives `work show`, which these changes leave alone: request files stay
  outside the queue's items.
- The xfail rows of w131 (`.shop/work/requests/q1.md` in test_design_model_check.py) and of w135 (intake
  `[awaiting-upstream]`) belong to those work-items. Nothing in w127 flips them.
- The `w_many_requests` rule in model.lp counts `open` requests. Moving a request to `awaiting-*` changes what it
  counts, but no test asserts it, and it is design-model-check's to settle (w131).

## 5. Open cases (for the implementer to name, not to choose)

- `work outcome` or `work turn` on a request id that has no file.
- `work outcome` with a line number that is not one of the request's lines.
- The exact wording of the r16 refusal, beyond naming the asker's turn.
- How `## Outcomes` writes "no line outcome" for a line, inside the file form.
- If the question below is answered with "no spec change", how the Given reads the literal text `<line 2>`.

## Question (r17)

Requests#r17's scenario is a Scenario Outline with no Examples table. The implementer may not change `features/`, so
the step receives the literal `<line 2>`, and the plan cannot pick which line-2 cases the scenario pins. See
`result.json` for the readings.
