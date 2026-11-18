---
id: record/missingmass.io/shopsystem/shopsystem-bdd/2026-11-18-cli-as-port
kind: analysis
about: bounded-context/missingmass.io/shopsystem/shopsystem-bdd
date: 2026-11-18
---

# The CLI as a port: decision-tiers worked through

Research, 2026-11-18, for the person's direction (quote-50, and their correction later that day): a business-logic
contract and separate interface contracts, the CLI and HTTP as adapters in the hexagonal style, so that business
requirements never change when an interface does. Asked: what changing everything, CLIs included, would mean, worked
through a subset. The subset is decision-tiers (15 live lines, both `work` and `model`). Everything was tried on a
scratch copy of `spec/`; nothing in `spec/` changed. Supporting files are in `2026-11-18-cli-as-port/`.

## The person's framing (their correction, 2026-11-18)

A return code or a response is business behaviour, not CLI behaviour. An option is not a CLI thing: it is a
parameter of a request, CLI-shaped only because business logic has so far only been defined through a CLI. The
requirements are mostly business logic and its contract, plus the ways different data and requests are fed into it.

The session first counted every refusal, exit, print and option as CLI-only (146, 133, 105 and 93 lines). Under the
framing above that was wrong, and the numbers below replace those counts.

## What was tried

**Variant A: inputs made attributes of domain things** (`variant-a-decision-tiers.md`, `.feature`). "runs `work
decision` without the `--tier` option" became "While a design-decision has no tier, if the person enters the
design-decision, then `work` shall decline the design-decision and name the tier of the design-decision". It needed
10 new terms (enter, examine, audit, flag, decline, execute, spec with `This:`, summary, wording, successor) and 2
relation rows, and three rounds of parsing before all 15 lines read. It had these costs:
- "replacement" was already a term in feature-file-tools with another meaning (v_t2). Business words share one
  namespace with every capability.
- r31 parses, but its scenario is wrong: "the design-decision" in the response binds to the successor (a kind of
  design-decision), so the scenario sets the successor's own status to `superseded`. R2's binding over a kind and its
  subkind gives the wrong referent without refusing.
- The request disappears as a concept. Parameters become facts about domain things, and nothing says what was asked.
  This is the opposite of the framing.
- Time: every new term recompiles grammar 4 and misses every cached parse (b351). The parses took 6.5 min, 44 s and
  39 s, and `features generate` took 7 min 50 s.

**Variant B: today's lines with the CLI spelling taken out** (`variant-b-decision-tiers.md`, `.feature`,
`variant-b-cli-adapter.sketch.yaml`). Each command code became an operation's business name (`work decision` became
`enter decision`, `model check` became `check spec`, `model decisions --check` became `audit decisions`). Each option
code became the parameter's business name (`--tier` became `tier`, `--decision` became `wording`). Nothing else
changed: the outcomes ("refuse the command and name `tier`", "exit with an error naming `v_d6`", "print `w_untiered`")
stay in the lines as business behaviour. Results:
- All 15 lines parse with no new term, in 10 s.
- `model logic` reads every line and finds nothing.
- `features generate` takes 1.6 s, and its feature is byte-identical to today's once the codes are re-spelled. Only
  two group titles, which name commands, were left un-spelled.
- The CLI spelling lives only in the adapter sketch: operation to command, parameter to option or position, refused
  to exit 1 with a message on stderr, returned content to stdout.

**Conclusion:** the spec is already business logic in request/response shape. The CLI shows only in the spelling of
codes and in the pack's words.

## What is CLI-only in the 455 live lines

- **About 440 lines name a command code.** Each needs re-spelling to an operation name: about 70 operations and 39
  parameter codes. Given an adapter table this is mechanical, so a `migrate upgrade` step could do it, unlike the
  CNL 4 migration's rewording. Group titles that name commands need the same treatment.
- **8 lines with `--json`.** These choose a representation of the response. Open question: is a JSON object business
  data, or the CLI adapter's format? HTTP would negotiate this differently.
- **About 11 lines driven by a hook** (SessionStart, UserPromptSubmit). These are a second driving adapter that
  already exists: Claude Code's hooks call the same operations in a mode (`--hook`) of their own.
- **2 lines naming environment variables** (`$VIRTUAL_ENV`). This is configuration fed in by the environment, so it
  is an adapter input.
- **Driven side, not looked at here:** git (about 64 lines name commit, push, branch or worktree) and GitHub (about
  26). These are outgoing ports. For this plugin, a commit is what a client observes.

## What would change in the plugin

1. **The pack's words.** The CLI pack's run, command, option, print, exit and refuse's definition are the core
   request/response meaning. They are hardcoded by name in `spec_lexicon` (CORE_VERBS), `spec_lf_option`,
   `spec_lf_facts` with `spec_lf_facts_atoms`, `features_vocab4` (WhenRuns), `spec_example`, `spec_findings` and
   `spec_rgl`. A neutral pack keeps that meaning under neutral words. Possible words: invoke an operation with a
   parameter, return, succeed or fail, refuse; "request" and "call" are taken. The CLI's spelling moves to the
   adapter. Either the words are renamed in the machinery, or "run", "option" and "print" are kept as the neutral
   words. That is the person's call.
2. **An adapter contract for each interface**, as in `variant-b-cli-adapter.sketch.yaml`:
   - operation to command;
   - parameter to option or positional argument;
   - outcomes to exit code and stream;
   - names in messages translated (a refusal naming `tier` shows `--tier`).
   It is checked both ways against the code: argparse's parsers are already caught by `test_docs`. Prior art for the
   format: OpenCLI (opencli.org, a draft modelled on OpenAPI) and jdx's usage spec (KDL). For HTTP, the OpenAPI
   document becomes this adapter contract, holding paths, methods and status codes, while the schemas are the core
   data model shared by every adapter.
3. **Scenarios through protocol drivers.** This is Farley's four-layer acceptance test: test cases in the domain
   language, then a DSL, then a protocol driver for each channel. Today 27 handler files key `WhenRuns` on the command
   code. A CLI driver reading the adapter contract lets handlers key on the operation, and a later HTTP or in-process
   driver runs the same scenarios. An in-process driver needs core functions callable without argparse. Today
   `decision_write.write` takes an argparse Namespace and its refusal names `--summary`. Under the framing, the core
   should name the parameter and the adapter should spell it.
4. **Spec and docs migration.** Re-spell the codes in about 440 lines and their group titles, and update the docs'
   lines, the notes-cli example, and every consuming context. All of this is mechanical from each context's adapter
   table.

## Bearing on the REST contract design (2026-11-17)

Under this framing the HTTP pack ("a client calls `GET /feed`") is not needed in lines. A feed line names its
operation and parameters the way a CLI line would. The OpenAPI document is the HTTP adapter's contract, mapping
operations to methods and paths and outcomes to statuses. The schemas are the core data model, read into the lexicon,
and every adapter shares them. That design needs revising before approval.

## Open questions for the person

1. **The neutral words:** rename run, command, option, print and exit, or keep them as the business words?
2. **`--json`:** business data format, or adapter format?
3. **Operation and parameter names:** chosen per context in business terms (`enter decision`, `wording`), or kept as
   today's command names minus the tool (`decision`, `decision` for the parameter)? The first reads better. The
   second makes the migration a pure strip.
4. **Driven ports** (git, GitHub): in this change, or a later one?
