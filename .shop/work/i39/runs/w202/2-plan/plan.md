# Plan of w202: spec-integration#r44

Inputs: `.shop/work/i39/w202.md` (accepts spec-integration#r44, no Retires, no Rulings), `spec/capabilities/spec-integration.md`,
`.shop/work/i39/runs/w202/1-research/notes.md` and `result.json`, `features/spec-integration.feature`, decisions 0047
(references-are-ids) and 0068 (the-context-runs-without-a-coordinator), `docs/design-model/design-model.md` §3 (the request
carries the upstream's published spec), supervision#r135 and the integrate steps of supervision (to stay in line with them).

## 1. What goes green

- **spec-integration#r44**, scenario "a round of the kind integrate that drafts a line needing what the named upstream does
  not yet give gives a request into that upstream, in its terms" (`features/spec-integration.feature` l.5-15).
  Red today because (notes §1, §2):
  - nothing binds the feature: no test module calls `scenarios` on `spec-integration.feature`, and none of its steps exist;
  - nothing reads an upstream from `spec/index.md` (`model_facts.py` reads only the id and the glossary; `model check`
    accepts and ignores an upstream section, Probe A);
  - the integrate brief (`Briefs.brief`, `Briefs.integrate_lines` in `scripts/supervise_brief.py`) names neither an
    upstream nor where its terms are, does not ask for request lines, and the round's agent and skill
    (`agents/initiative-round.md`, `skills/integrating-a-proposal/SKILL.md`) give a change list only.
- No deprecated scenario is retired by this work-item.

## 2. Where the change lands

- `scripts/supervise_brief.py`: a small reader of the upstreams that `spec/index.md` names (see decision 1); when there
  is at least one, the integrate brief gains a line for each upstream (its id and the absolute path of its published spec),
  that spec path joins the brief's Read list, and a line gives the request-lines form (decision 2). With no upstream named,
  the integrate brief is exactly as today.
- `agents/initiative-round.md`: the integrate step says that where the brief names an upstream, a drafted line needing
  what that upstream does not yet give leads to the lines of a request into it, worded in the upstream's glossary terms
  and narrator, given in the result's field of decision 2, alongside the change list.
- `skills/integrating-a-proposal/SKILL.md`: the reply (l.59, "reply with the change list") gains the request lines, one
  set per upstream, in strict EARS and the upstream's terms. Its note-vs-initiative wording (l.40) is left as is (not r44).
- `docs/capability-format.md`: the `spec/index.md` part (l.169-200) documents the upstreams section of decision 1, so the
  person and the capability-writer know the form.
- `tests/scenarios/test_spec_integration.py` (new): binds `spec-integration.feature`.
- `tests/scenarios/spec_integration_steps.py` (new): the Givens, When and Thens (decision 4).

Removed from the researcher's set: `scripts/supervise_rounds.py`. r44 requires only that the round *give* the lines in its
result; reading them and raising them with `work request` is supervision#r135, another requirement not accepted here.
The round's `result.json` is already kept with its stage directory under `.shop/work/<i>/runs/<i>/<n>-integrate/`
(as for i39 itself), so nothing in `work run` must change for the lines to be observable. `supervise_change.py` and
`supervise_outputs.py` (the researcher's "may change") are not touched, for the same reason.

Size: `supervise_brief.py` is 171 lines; the reader and brief lines fit well under 300. The new step module stays under 300.

## 3. Decisions

1. **How `spec/index.md` names an upstream.** A body section `## Upstreams` in `spec/index.md`, one bullet per upstream:
   its id `bounded-context/<context path>`, then where its published spec is read (a path to the upstream's `spec/`
   directory; a relative path taken from the repository root). Not a frontmatter field: frontmatter names other things by
   id only and carries no path but a work-item's `fileset` (design-decision/references-are-ids); the id in the bullet keeps
   the bounded-context's id form. The published spec is what crosses with a request (design-model §3, "its published spec
   at a pinned version"). `model check` ignores the section today (Probe A), and `model_facts.py` is not changed (13 lines
   of room). Rests on spec-integration#r44 ("Where `spec/index.md` names an upstream bounded-context").
2. **Where the round gives the request lines.** In its result, a field `requests`: a list with one entry for each upstream,
   each naming the upstream by its bounded-context id and giving its lines (strict EARS, in order), beside `changes`. The
   brief gives this form the way `CHANGE_LIST` gives the change list. Rests on spec-integration#r44 ("give in its result
   the lines of a request into that upstream") and keeps the shape supervision#r135's work will read (an upstream and its
   lines, the form `work request --lines` takes).
3. **What the round is told, in which terms.** `work run` resolves each upstream's spec path to an absolute path (the round
   runs in a worktree, where a relative path would not reach it) and lists it among the files to read; the brief tells the
   round to word the lines in that spec's glossary terms. The round reads; it writes nothing into the upstream. Rests on
   spec-integration#r44 ("in the upstream's terms") and requests#r28 (no checkout of the upstream's repository is made).
4. **How the scenario is bound.** The round is the stand-in session (`tests/scripts/stub_claude.py`), whose result the
   scenario scripts, so the Thens must observe what `work run` makes of the setting, not the stand-in's choice alone:
   - Givens: a repository like supervision's with `spec/index.md` naming `bounded-context/.../billing` under `## Upstreams`
     with a path to a billing `spec/` kept beside the repository; billing's capabilities with no line giving a refund; its
     glossary with a bullet naming the credit note as the refund of an order. "An approved note asks that the customer sees
     the refund of a returned order" stands as the request i1 fulfils, its line 1 that text with the line outcome accepted:
     today the integrate round's input is the initiative and the accepted lines of its request (`integrate_lines`), and the
     notes find both readings give the round the same lines. The stand-in's integrate step writes a draft line needing a
     refund under its drafts path and gives DONE with `changes` and `requests` (billing: one line asking for a credit note).
   - When: `work run i1`, as supervision's integrate scenarios run it.
   - Thens: "drafts a line that needs a refund": the kept draft under the integrate stage directory holds such a line.
     "result gives the lines of a request into billing": the integrate round's brief named billing as an upstream and asked
     for the `requests` form, and the kept `result.json` has a `requests` entry for billing. "ask for a credit note, in
     billing's terms": the brief listed billing's published spec (absolute path) to read and asked for its terms, and the
     kept lines say "credit note" and not "refund".
   Rests on spec-integration#r44 and the existing supervision integrate steps' practice (`rounds(...)` brief reads).

## 4. Tests the decisions break

None. Verified: with no `## Upstreams` in `spec/index.md` the integrate brief is unchanged (decision 1, §2), so
`tests/scenarios/supervision_integrate_steps.py`, `supervision_rounds_steps.py` and `supervision_proposal_steps.py` (which
assert named brief lines and stubbed `changes`, none the brief's whole text, notes §4) keep passing;
`tests/scripts/test_agents.py` asserts frontmatter and ResultFirst text only, untouched by body edits to
`initiative-round.md`; `tests/scripts/test_supervise_change.py` covers `entries`, which is not changed.
`supervise_rounds.py` is not changed, so the r135 xfail in `test_supervision.py` stays as it is.

## 5. Open cases

- `spec/index.md` names an upstream whose spec path does not exist or is not a directory: refuse the round, name it in the
  brief as missing, or leave it out?
- An `## Upstreams` bullet with an id but no path, or a malformed id.
- More than one upstream, and a drafted line that needs two of them.
- The "pinned version" of the upstream's spec (design-model §3): read as the path stands today, or at a pin?
- A round that gives `requests` naming an upstream the index does not name, or gives `requests` when the index names none.
- Whether a `requests` entry should also name the capability (or drafted line) needing it: supervision#r136 reading 2 would
  need that tie; it is a question still open on supervision.
- The round's tool permissions for reading an absolute path outside its worktree.
- `spec/index.md` naming this context itself under `## Upstreams`.
- Defects the research found in `work request` (D1-D3: `--source` from a non-upstream asker accepted, no `--raised-for`,
  the refusal's wording) are requests#r29-r31 and supervision#r135 work, not this item's.
