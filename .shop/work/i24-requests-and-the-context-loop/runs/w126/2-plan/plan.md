# Plan of w126: work request, and each side's part by its own command

Work-item `.shop/work/i24-requests-and-the-context-loop/w126.md`, under `requests`, accepts requests#r1-r5.
From the research notes `.shop/work/i24-requests-and-the-context-loop/runs/w126/1-research/notes.md`.

## 1. What goes green

All five are red today for the same reasons (notes, part 1): `features/requests.feature` has no binding (no
`tests/scenarios/test_requests.py`, no steps module), `scripts/work` has no `request`, `outcome` or `turn` command
(each exits with argparse's `invalid choice`), and no module in `scripts/` writes a request.

- requests#r1: "request with <given> writes an open request in the upstream's turn with the lines, asker and
  <where from> given, and prints its id" (two rows: two --source, --thread). Also red because `work request` has no
  `--from`, `--lines`, `--source` or `--thread`.
- requests#r2: "request with a line that <fault> is refused, naming the line, and nothing changes" (five rows). Also
  red because the strict-form check (`model_parse.ears`) is called for capability lines only.
- requests#r3: "request with neither --source nor --thread is refused, and nothing changes". Also red because that
  refusal is not written.
- requests#r4: "outcome writing a line outcome leaves the request's lines as the asker wrote them". Also red because
  there is no `work outcome`.
- requests#r5: "turn passing a request leaves its line outcomes as they were and writes no resolution". Also red
  because there is no `work turn`.

Retires: none (the work-item has no Retires section; r6 is already retired in the capability).

## 2. Where the change lands

- `scripts/work`: the subcommands `request` (title, `--from`, `--lines`, repeatable `--source`, `--thread`),
  `outcome` (request, n, outcome) and `turn` (request), added to the subparsers and the dispatch; refusals go
  through the existing `workqueue.Refused` handler, so they exit with an error (design-decision
  exits-are-successful-or-errors).
- `scripts/workqueue_request.py` (new): the request library: number and write a request under the root's
  `.shop/work/requests/`, check each line's strict form, refuse a request without origin, read a request back,
  write a line outcome, pass the turn.
- `CLAUDE.md`: a module-map row for `scripts/workqueue_request.py` (`work request`, `work outcome`, `work turn`:
  the requests of the context), as its "A new concern gets a new module and a row here" asks. Added to the
  researcher's set for that reason.
- `tests/scenarios/test_requests.py` (new): binds `features/requests.feature`.
- `tests/scenarios/requests_steps.py` (new): the Givens, Whens and Thens of the r1-r5 scenarios. If it nears the 300
  line limit, split by concern (writing a request; the parts of a request), each `requests_*_steps.py`.

Reused unchanged: `scripts/workqueue.py` (`Refused`, `read`, the bounded-context id read from `spec/index.md`,
`frontmatter`), `scripts/model_parse.py` (`ears`). Not touched: `scripts/model_work.py` (D1), `scripts/model_facts.py`,
`scripts/model_check.py`, `scripts/workqueue_status.py`.

## 3. Decisions

1. **`work outcome` and `work turn` come in with this work-item, as far as r4 and r5 need them, and no further.**
   r4 and r5 are accepted here and their scenarios run `work outcome q1 2 accepted` and `work turn q1`; they cannot
   go green without the commands. `work outcome` writes the outcome given as line n's line outcome, and `work turn`
   passes the turn to the other side, exactly as requests#r15 and requests#r7 state them: no reading is chosen, the
   requirements fix what the narrator sees. What stays w127's (requests#r16, r17, r18): no out-of-turn refusal, no
   status change on a turn. Rests on requests#r4, requests#r5, requests#r15, requests#r7, and
   design-decision/requests-written-through-work ("each part is written by its own command … `work turn` only passes
   the turn"). `work resolve` is not added (w128); r5's "writes no resolution" holds because only resolve would write it.
2. **`work request` does not commit in this work-item.** requests#r12 (commit) is accepted by w128, which adds the
   commit to every request command; r1-r5 do not ask for it. The write is still all-or-nothing: every check (r2, r3)
   runs before anything is written, so a refusal changes nothing. The steps' upstream is nevertheless a git
   repository with everything committed, so the same Givens hold once w128 commits. Rests on requests#r1-r3 and on
   requests#r12 being w128's.
3. **The upstream is the root `work` runs on: the existing `--root` (default: the current directory).** No new
   option: the capability's Implementation says the asker writes the request "through the upstream's `work`", i.e.
   `work` run on the upstream's repository; the steps run `work --root <upstream> request …`. The request is written
   at `<root>/.shop/work/requests/q<n>.md`, the directory created when absent, `<n>` one above the highest `q<n>`
   kept there (q1 when none). Rests on requests#r1 and design-decision/requests-written-through-work.
4. **The id printed is `q<n>`, as `work add` prints `w<n>`.** The file's frontmatter keeps the full
   `request/<context path>/q<n>`, the context path read from `spec/index.md` as `work add` reads it; the commands
   address a request by `q<n>` (the scenarios run `work outcome q1 …`). Rests on requests#r1 and work-queue#r1's
   precedent ("with the id `w<n>` … and print the id").
5. **Each text line of the lines file is one line of the request, in file order, numbered from 1.** requests#r1
   says "the file's lines as its lines"; a lines file is plain lines, no bullets or `[r<n>]` (those are a
   capability's form, not a request's). Line n of `work outcome` is the n-th. The step writes lines.md as plain lines.
6. **The strict-form check is `model_parse.ears`, without the solver.** A line is refused when `ears` gives either
   flag false (the first flag is v_e1's pattern check, the second v_e2's one-shall, one-sentence check); this is the
   judgement `model check` holds, as `model_facts` feeds the same function's result to v_e1/v_e2. No clingo need is
   added to `work`. The probe (notes, part 2) shows all five faults flagged and good lines passing; the "two
   sentences" row should use a line with one shall in each sentence only if the implementer confirms `ears` flags
   it (notes: read, not probed). Rests on requests#r2.
7. **The refusal of r2 names the line by its number** ("line 2"), with its text; the first failing line is the one
   named. The refusal of r3 says the request names neither an origin nor a job-thread. Both raise `workqueue.Refused`
   and nothing is written. Rests on requests#r2, requests#r3, design-decision/exits-are-successful-or-errors.
8. **Origins go to the `source` field, a thread to `part_of`; the lines to `## Lines`, line outcomes to
   `## Outcomes`, the sections and fields of the capability's Implementation.** The exact text form inside those
   sections is `work`'s own (design-decision/requests-written-through-work), so the steps read a request back through
   the library's reader, never by matching file text; the Givens of r4 and r5 (a request q1 already with outcomes and
   a turn) write it in that form through a library helper or a fixture the reader accepts.
9. **D1 and design-model-check's red request scenarios stay out.** They are w131's (design-model-check#r19, r112);
   this work-item writes requests only in scratch upstreams in its tests, so it neither fixes nor breaks them.

## 4. Tests the decisions break

None. Verified from the notes (part 4): no test asserts `work`'s usage text or the unknown-command message (grep of
`choose from`, `usage: work`: no hits); `scripts/workqueue.py`, `model_parse.py` and the model modules are not
changed; the tests naming `.shop/work/requests` or `cross-context-request` are migration tests of old paths, which
this change does not touch; `tests/scenarios/test_work_queue.py` is not changed. The researcher's search had no
coverage map, so the implementer runs the whole suite once green. Binding `requests.feature` also ends the
collection abort the notes report as D2 for `--work-item w126` (the work-item then collects its scenarios).

## 5. Open cases

- Both `--source` and `--thread` given.
- Both faults at once: no origin and a line not in strict form (which refusal is given).
- An empty lines file, a blank line inside it, a missing or non-UTF-8 lines file.
- An empty title, or a newline in the title, `--from`, `--source` or `--thread` (`work add` refuses these for its own
  values; notes, part 5).
- `--from` or `--lines` not given (argparse's own error, or a refusal).
- An upstream with no `spec/index.md` or no bounded-context id in it.
- `work outcome` with an n that is not a line of the request, a request that does not exist, or an outcome word
  outside accepted, refused, withdrawn, question.
- `work turn` / `work outcome` on a request not in the `.shop/work/requests/` of the root.
- w127's r15 and r7 scenarios may already pass once this lands (decision 1); its run should expect that.
