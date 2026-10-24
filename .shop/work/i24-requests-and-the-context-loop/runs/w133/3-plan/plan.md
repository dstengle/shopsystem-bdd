# Plan of w133: measure gives whether the initiative's request is internal or external

Accepts batch-measurement#r63 and #r64. Planned from the research notes of stages 1 and 2
(`runs/w133/1-research/notes.md`, `runs/w133/2-research/notes.md`). Stage 1's session ended at its turn limit. Its
notes are used only where stage 2 or the spec confirms them.

## 1. What goes green

- **batch-measurement#r63**, the outline "the request an initiative fulfils is given as <origin> when its asker is
  <asker>", in two examples: `this bounded context` gives `internal`, `another bounded context` gives `external`.
  Red today with StepDefinitionNotFoundError at the Given "i7-cart fulfils the request q3, whose asker is …" (feature
  line 174). Behind that step, the Then "the measurement gives the request q3 as <origin>" has no step either. In
  code, `measure_build.figures_of` gives no request figure, and nothing in `measure` reads an initiative's link to a
  request. Probes P1–P3 and A–C show exit 0 with no origin given.
- **batch-measurement#r64**, "an initiative that fulfils no request is measured without saying internal or external".
  Red today with StepDefinitionNotFoundError at the Given "i7-cart fulfils no request" (line 189). The Thens "the
  measurement gives the stage of cart-1's research" (line 192) and "the measurement gives no request as internal or
  external" (line 193) also match no step. The code already gives this measurement (probe P4/D), so only the steps
  are missing.
- Retires: none. The work-item has no Retires section.

## 2. Where the change lands

- `scripts/measure_read.py` (182 lines): a reader of the initiative's link and of the linked request's asker. It
  returns no request when `initiative.md` is absent or has no `fulfils`. It refuses as decision 4 says. There is no
  new module, so CLAUDE.md does not change: this is reading for `measure`, which is this module's concern.
- `scripts/workqueue_request.py` (114 lines): its lookup of a request by id (`_path`) and its reading of a
  frontmatter field (`_field`) become the public reader that `measure` uses (decision 3). Its own callers are renamed
  with them.
- `scripts/measure_build.py` (139 lines): `figures_of` adds the request figure (the request's id and its origin) when
  the initiative fulfils a request, and leaves the figure out otherwise.
- `scripts/measure_show.py` (110 lines): prints the request and its origin when the measurement gives one (decision 6).
- `scripts/measure` (92 lines): the CONTRACT text names the optional request figure.
- `tests/scenarios/batch_measurement_world.py` (141 lines): `flush` writes `initiative.md` with its `fulfils` and the
  request file `.shop/work/requests/q3.md` when the world holds them. It writes neither otherwise.
- New `tests/scenarios/batch_measurement_request_steps.py`: the Givens "i7-cart fulfils the request q3, whose asker
  is <asker>" and "i7-cart fulfils no request", and the three new Thens. They go in a new module because
  `batch_measurement_given_steps.py` has 24 lines of room.
- `tests/scenarios/test_batch_measurement.py` (15 lines): star-imports the new step module, as it does the others.

Unchanged: `scripts/measure_write.py`, `scripts/workqueue.py` (28 lines of room; read only), `features/`,
`tests/scripts/test_measure_runs.py` and `batch_measurement_then_steps.py`. That last file stays unchanged unless the
implementer puts the Thens there instead; they fit in its 98 lines of room.

## 3. Decisions

1. **The link sits on the initiative.** The initiative names its request in a frontmatter field `fulfils` in its
   `initiative.md`, which holds one request id. The request does not point back with `part_of` or `source`. This
   rests on design-decision/plugin-adopts-the-design-model. The design model's initiative table
   (`docs/design-model/design-model.md`, "fulfils: exactly one request, of this context, accepted") and grammar.md's
   `fulfils(I, Q)` edge (initiative → request) settle stage 2's question 1. The request's `part_of` is a job-thread
   and its `source` is its origins (requests.md Implementation), so neither names an initiative. work-queue#r22
   (`work start`, a drafted work-item not yet built) writes the same field. Whichever of the two lands second follows
   the first.
2. **The form of the value.** `fulfils` holds the request's id in the reference form the work files already use
   (`request/q3`, as `part_of: initiative/i24`). The reader takes the request number from the last segment of the id,
   so a full `request/<context path>/q3` reads the same. This rests on design-decision/references-are-ids
   (0047) and requests.md's id form.
3. **Who reads the request: `work`'s own reader.** `measure` reads the request through `workqueue_request`'s lookup
   and field reader, not by opening `.shop/work/requests/` itself. How `work` keeps a request stays `work`'s own and
   may change. This rests on design-decision/requests-written-through-work (0067). Nothing stands in the way:
   design-decision/plugin-takes-the-dependencies-it-needs (0035) supersedes the stdlib-only rule that stage 2
   believed blocked using the model's reader. `model_requests.py` is still not used, because its form checks belong
   to `model check`.
4. **Internal or external** (batch-measurement#r63 "its asker being this bounded context"):
   - The request is internal when its `asker` is `internal`, or is this context's own id as `spec/index.md` gives it
     (read the way `workqueue.context_path` reads it).
   - It is external for any other asker: another context's id, or the product level.
   - requests.md's Implementation lists the three asker forms (a context id, `internal`, the product level), and the
     design model calls a request internal when "its asker is the context itself". Nothing in r63 lets the product
     level count as this bounded context.
   - The context id is read only when a request is linked and its asker is not `internal`. That keeps
     `tests/scripts/test_measure_runs.py`, which has no `spec/index.md`, off that path.
5. **A link that cannot be read is refused.** `measure initiative` refuses, writing nothing, naming the file, and
   exits with an error (batch-measurement#r50) in these cases:
   - `fulfils` names a request that `work`'s reader cannot find;
   - the request has no `asker`;
   - `fulfils` holds more than one id.

   An initiative with `fulfils` does fulfil a request, so r64 does not cover it, and r63 requires the origin. This
   rests on the capability's Purpose ("refuses rather than guesses when its inputs are not of a shape it knows") and
   design-decision/measure-refuses-unknown-shapes. It covers stage 2's questions 4 and 5. Two requests naming one
   initiative cannot arise once the link is on the initiative (decision 1); a list in `fulfils` is the one form left,
   and it is refused here.
6. **`measure show` prints the origin.** It prints the request's id and origin when the measurement gives them,
   because batch-measurement#r44 says show prints "the measurement's figures", and the origin is now one of them. It
   prints nothing for a measurement without one, which also covers every measurement written before this change.
7. **The scenario steps.**
   - "this bounded context" writes the request's asker as `internal`. "another bounded context" writes
     `bounded-context/ex.com/prod/other`, a context other than the one `flush` already writes into `spec/index.md`.
   - The request file has the frontmatter requests.md gives (id, `kind: request`, `asker`, `source`,
     `status: accepted`, `turn`). The initiative's `initiative.md` names it in `fulfils`.
   - "i7-cart fulfils no request" writes no `fulfils` (and no request).
   - Basis: batch-measurement#r63 and #r64, and decisions 1, 2 and 4.

## 4. Tests the decisions break

None. Checked:
- `tests/scripts/test_measure_runs.py` (two tests): calls `figures_of` with no `initiative.md` and no
  `spec/index.md`. With no link there is no request (decision 1) and the context id is never read (decision 4), so it
  passes as it is.
- The other 28 tests of `test_batch_measurement.py`: their Givens write no `initiative.md` and no requests, and
  their Thens read named keys only. No test asserts the exact set of figure keys (notes stage 2, part 4).
- The tests of `workqueue_request.py`'s commands (`work request`, `outcome`, `turn`, `resolve`) drive the commands,
  not the private names that decision 3 renames, so they are unaffected. The implementer confirms this with
  `tools refs` and a search once the names change.

## 5. Open cases (for the implementer to name, not to choose)

- A request linked by `fulfils` whose status is not `accepted`, or whose id is of another context: `model check`
  holds these (v16d, design model "of this context, accepted"). The scenarios are silent on what `measure` does.
- A `fulfils` value that is not a request id at all, such as an observation id.
- What "the measurement gives no request as internal or external" checks: that the figure is absent, or also that
  the record's text has neither word.
- Whether "the measurement gives the stage of cart-1's research" gets a step of its own or a wider match of the
  existing "the measurement gives the stage".
- How `measure show` lays out the origin line, and whether `measure compare` says anything about two measurements'
  origins (no requirement asks it to).
