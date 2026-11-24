# The word 'area' in the repository (grep, 2026-11-24)

## counts of lines by top folder
   381 .shop
   213 scripts
   124 tests
    61 docs
    53 spec
    16 CLAUDE.md
    11 grammar
     9 CHANGELOG.md
     5 skills
     4 features
     3 README.md

## spec/ frontmatter keys
     23 spec/capabilities
      6 spec/model
      6 spec/vocabulary

## spec/ text (not frontmatter)
spec/adapters/cli.toml:128:  "checking#r69: While an area whose kind is `port` holds an operation and no adapter contract holds an operation table of the operation, when the person validates this specification, the speci
spec/capabilities/batches.md:124:### [g76] A new capability is laid in 0.38's form: area:, specifies:, no empty ## Terms, one ## Composition
spec/capabilities/checking.md:192:- [r69] While an area whose kind is `port` holds an operation and no adapter contract holds an operation table of the operation, when the person validates this specification, the specifi
spec/decisions/0122-the-downstream-keeps-its-terms-behind-a-driven-port.md:3:summary: "The core reads no upstream word; each upstream is reached through a port area in the downstream's own words."
spec/decisions/0122-the-downstream-keeps-its-terms-behind-a-driven-port.md:18:A core area never imports a provider area or an upstream's vocabulary. Each upstream is reached through a driven port, an area of kind port, w
spec/decisions/0123-an-adapter-is-a-nested-context-with-its-own-spec.md:18:Its id is the parent's id with /adapter/<name>. It reads the parent's port area and port contract at the parent's commit, holds its providers, it
spec/decisions/0128-subdomains-are-declared-by-the-product.md:14:The term area mixed a subdomain's classification with parts of a bounded context's model; the person placed subdomains at the product level, as the busines
spec/decisions/index.md:128:| [design-decision/missingmass.io/shopsystem/shopsystem-bdd/the-downstream-keeps-its-terms-behind-a-driven-port](0122-the-downstream-keeps-its-terms-behind-a-driven-port.md) | The core reads n
spec/index.md:44:model (`spec/model/<area>.md`), the vocabulary naming its elements (`spec/vocabulary/`), the requirements of the
spec/index.md:45:capabilities below, grouped by area, and the decisions (`spec/decisions/`); the CLI is an adapter, specified by
spec/model/specification.md:341:object area
spec/vocabulary/execution.md:43:- **the capability form** (proper noun) → object capability form. A capability file as 0.38 keeps it: its frontmatter names its `area:` and what it `specifies:`, and it holds no empty se
spec/vocabulary/execution.md:44:- **the index form** (proper noun) → object index form. `spec/index.md` as 0.38 keeps it: one `## Composition` section, whose table `| area | kind | capabilities |` has a row for each ar
spec/vocabulary/specification.md:222:- **area** (noun) → object area. One part of the domain model, a file `spec/model/<area>.md` with its `kind:`: a core, supporting or generic part of the business, or a driven port, 
spec/vocabulary/specification.md:223:- **kind** (attribute) → attribute area.kind. What an area is, the `kind:` of its model file.
spec/vocabulary/specification.md:224:- **port** (noun) → value area.kind port.
spec/vocabulary/tracking.md:138:- **model line** (noun) → object model line. A line of the domain model's syntax, an element with its members or a relation, that an item keeps for the area of one of its capabilities un
spec/vocabulary/tracking.md:149:- **domain model** (noun) → object domain model. The files `spec/model/<area>.md` of this bounded context, each declaring the objects, services and operations of one area. This: the doma

## argparse options and help in scripts
scripts/backlog_cli.py:79:    p.add_argument("--model", help="with a domain model: model lines for the area of the capability --into names")

## model_forms (file forms)
scripts/model_forms.py:58:    Form("item's model lines", ".shop/backlog/b<n>.md ## Requirements ### <area> model",
scripts/model_forms.py:60:    Form("domain model area", "spec/model/<area>.md", "plugin item b398 (no command yet)"),
scripts/model_forms.py:61:    Form("vocabulary term", "spec/vocabulary/<area>.md", "plugin item b398 (no command yet)"),

## grammar and packs
grammar/catalogue-entries.toml:297:purpose = "A requirement uses only words its area can see, so each capability stays within its part of the domain."
grammar/corpus/constructs/request/spec/index.md:17:| area | kind | capabilities |
grammar/corpus/constructs/request/spec/model/decisions.md:3:area: decisions
grammar/corpus/constructs/request/spec/model/registry.md:3:area: registry
grammar/corpus/constructs/request/spec/vocabulary/decisions.md:3:area: decisions
grammar/corpus/constructs/request/spec/vocabulary/registry.md:3:area: registry
grammar/corpus/spec/checking.md:729:While an area whose kind is `port` holds an operation and no adapter contract holds an operation table of the operation, when the person validates this specificatio
grammar/corpus/spec/checking.md:731:  while [x1: area, x2: operation]
grammar/rules.md:1340:a requirement uses a word that names no element through the vocabulary its capability's area reads
grammar/rules.md:1342:- Purpose: A requirement uses only words its area can see, so each capability stays within its part of the domain.
grammar/rules.md:1350:  foreign_term("c#r1","finding","finding is a word of analysis, which the area notes does not read").

## scripts files mentioning area, with counts
scripts/backlog_model.py:36
scripts/backlog_model_area.py:30
scripts/backlog_capability.py:26
scripts/domain_model.py:19
scripts/migrate_upgrade_domain.py:12
scripts/domain_model_parse.py:12
scripts/spec_vocabulary.py:9
scripts/model_domain.py:8
scripts/backlog_model_edit.py:8
scripts/backlog_retract.py:7
scripts/spec_vocabulary_terms.py:4
scripts/spec_packs.py:4
scripts/spec_moves.py:4
scripts/request_terms.py:4
scripts/migrate_upgrade_domain_scaffold.py:4
scripts/contract_form.py:4
scripts/adapter_cli_check.py:4
scripts/model_forms.py:3
scripts/model.lp:3
scripts/backlog_section.py:3
scripts/backlog_cli.py:3
scripts/spec_lexicon.py:2
scripts/spec_rgl_vocab.py:1
scripts/spec_lf_ids.py:1
scripts/readiness_bar.py:1
scripts/backlog_model_ops.py:1

## docs
docs/reference/domain-model.md:13
docs/reference/capability-file.md:10
CHANGELOG.md:9
docs/examples/notes-cli/README.md:7
docs/concepts.md:7
docs/recipes.md:6
docs/reference/commands.md:5
docs/upgrading.md:4
docs/reference/design-model.md:3
README.md:3
docs/writing-requirements.md:1
docs/how-it-works.md:1
docs/examples/notes-cli/spec/vocabulary/notes-cli.md:1
docs/examples/notes-cli/spec/model/notes-cli.md:1
docs/examples/notes-cli/spec/index.md:1
docs/examples/notes-cli/spec/capabilities/notes.md:1

## skills/agents
skills/shaping-items/SKILL.md:3
skills/taking-in-a-request/SKILL.md:1
skills/raising-a-request/SKILL.md:1

## model.lp facts
scripts/model.lp:50:#defined foreign_term/3.          % foreign_term(Q, W, Why): Q uses W, a word of no vocabulary layer its area reads
scripts/model.lp:423:label("v_m1", "a requirement uses a word that names no element through the vocabulary its capability's area reads").
scripts/model.lp:424:% fail v_m1: foreign_term("c#r1","finding","finding is a word of analysis, which the area notes does not read").
