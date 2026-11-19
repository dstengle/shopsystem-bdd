# The contract artifact, 2026-11-19: the business contract and its interface contracts

A version of the contract artifact for b348 (a bounded context asks another for its context) and b42 (terms
negotiated between contexts), made after plugin 0.38.0 with the forms it introduced. It revises
`../2026-11-17-rest-contract/design.md` (that design stays as written; `design.md` here says what it supersedes).

## The files

| file | what it is |
|---|---|
| `design.md` | the revised design: what changed from 2026-11-17 (no HTTP pack, schemas made from the model, OpenAPI as the HTTP adapter's contract), the contract (b348) and term proposals (b42), the rules from model to schema, the CLI and HTTP mapping side by side, the decisions to write; the session's calls marked |
| `business-contract.md` | the business contract as it stands on the items: the model lines (` ```model `), the vocabulary entries and the requirement lines of b348 (a new capability `contracts`, its model in the specification area) and of b42 (in `context-requests`, its model in the tracking area); a copy, the items are the source |
| `schemas/model.schema.json` | the objects the operations take and give (contract, term proposal, request line), JSON Schema 2020-12, made from the domain model |
| `schemas/envelope.schema.json` | the standard response envelope (outcome, content, errors, notices), from `scripts/domain_envelope.py` |
| `schemas/operations.schema.json` | each operation's request (its parameters by business name) and response (the envelope, its content the domain object, its refusal reasons the ones the model declares) |
| `schemas/events.schema.json` | the notification of the event *contract published* |
| `examples.json` | instances validated against the schemas, one of them a negative (a refusal reason the model does not declare) |
| `generate_schemas.py` | makes `schemas/` from the model with b348 and b42 laid over a copy of `spec/`; `--check` makes them again, compares, and validates `examples.json` |
| `http-adapter.openapi.yaml` | the HTTP interface contract, OpenAPI 3.1: each operation a method and path (`operationId` the model's operation id), each parameter a path, query or body field, each outcome and refusal reason a status (`x-outcome`, `x-reasons`), each actor a security scheme, the event a webhook; every schema a `$ref` into `schemas/` |
| `cli-adapter.toml` | the CLI interface contract of the same operations in the form of `spec/adapters/cli.toml`, for comparison (commands proposed, not built) |
| `check_adapters.py` | both interface contracts checked both ways against the model, as `spec check`'s v_a1-v_a4 check cli.toml: every operation mapped once, every field a declared parameter and every parameter a field, every declared refusal reason carried by exactly one status, every `$ref` resolving |

Run from this folder: `python3 generate_schemas.py --check && python3 check_adapters.py` (both exit 0 at this
commit; each was shown to catch a broken copy).

## Where the lines stand

Every requirement line was parsed in grammar 4 (`scripts/spec --root <copy> parse`) on a copy of `spec/` with the
items' model lines and vocabulary entries laid in, and put on the items with `scripts/work line` (`--capability`,
`--model`, `--term`, lines with `--group`). The readiness bar (`readiness_bar.check`, read-only, neither item moved to
`ready`) on each item: see "Readiness bar" below.

## Still open

- **The commands and the server.** Nothing here is built: no `spec contract publish|show`, `work obtain`,
  `work suggest`, no HTTP server. When the items are built, each new operation needs its table in
  `spec/adapters/cli.toml` (v_a1) or a place under `[unexposed]`; `cli-adapter.toml` holds the proposed tables, and
  the adapter contract form has no `work line` writer yet.
- **The channel of a fetch.** A downstream's fetch reaches the upstream through the issue host today and HTTP once a
  context serves its contract; which one a context uses, and how a contract is pinned and compared with a later
  version, are not settled (the design-decisions of `design.md` §6 are not written).
- **The model's gaps the schemas show** (b366): the things a contract holds (term, requirement, design-decision)
  have no attributes in the model, so they travel as `{reference, text}`; whether a parameter passes data or a
  reference is written in the generator (`PASSED`), not the model.
- **Plugin commands** (b366): schema generation and the OpenAPI check are record scripts here; in the plugin they
  would be a `spec` command writing `spec/schemas/` and `spec check` reading `spec/adapters/http.openapi.yaml`.
- **A version as an attribute** (b365): grammar 4 reads no `(version)` attribute, so the contract's version is a
  relation to the object `version`.
- **`work line --capability` gives no area** (b364): b348's model lines went in through `--into checking`; the new
  capability's file will lack `area:` and `specifies:` until that is fixed or set when it is built.
- **Taking a model line out of an item** (b367): one row of b42 had to be removed from the item file by hand.
- **Not covered:** the product as a party to term negotiation (b42's "and with the product"); a term proposal that
  collides with a term the upstream has (whether it is refused, or must be `rewritten`); the scenarios of HTTP lines
  and how a test driver for HTTP builds its world (the 2026-11-17 seeding endpoint is dropped, nothing replaces it
  yet); OpenAPI's own meta-schema validation (no validator is installed; the check is structural).

## Readiness bar

Both items pass the bar at this commit (`readiness_bar.check` on each, no reason and no warning): every line
parses, no model.lp rule is broken by them, `spec logic` reads each and finds no L0 or L1 naming them, and
`features generate` writes their groups. On the way it refused, and the lines were changed for it: groups of more
than one statement (v15k, v15l: each line is its own group), two groups of one trigger and condition (v15n: two
lines made one), and b42's row "context request holds term proposal" (v_t10, taken out by hand: b367). Neither item
was moved to `ready`: b348 is an `idea`, b42 `shaped`; that is the person's call.
