---
id: product/missingmass.io/shopsystem/domain
form: domain map
---

# Domain map

## Subdomains

The problem space, declared by the product (decision 0128); each subdomain's type and the jobs it serves.

| subdomain | type | problem | jobs |
|---|---|---|---|
| s1 requirements specification | core | One context's behaviour kept as a model, a vocabulary, lines and decisions; its scenarios generated. | j1, j4 |
| s2 controlled requirements language | supporting | A line read to one meaning or refused; contradictions and entailments found. | j1, j4 |
| s3 work planning | supporting | Ideas becoming shaped, ranked, ready items with lines. | j1 |
| s4 collaboration between contexts | supporting | One context asking another for behaviour until it is settled. | j3, j4 |
| s5 the person's direction | supporting | What the person said, kept and cited; short-term directions every session follows. | |
| s6 delivery | supporting | Ready work built in batches, reviewed once as one change, merged. | j2 |
| s7 delivery economics | generic | What work cost and what escaped. | j6 |
| s8 codebase insight | generic | Toolchain, coverage, references, the Gherkin of features. | |
| s9 release adoption | generic | A repository moved between releases; a context founded. | j5 |

## Bounded contexts

The solution space: each context, the subdomains it addresses (many to many) and the shop hosting it. `today` says
which part of this repository's one context holds it now (an area, or a capability named `cap:`), for the checks to
read until the contexts are split.

| context | addresses | shop | today |
|---|---|---|---|
| bounded-context/missingmass.io/shopsystem/specification | s1 | shop/missingmass.io/shopsystem-bdd | area:specification |
| bounded-context/missingmass.io/shopsystem/language | s2 | shop/missingmass.io/shopsystem-bdd | cap:parsing cap:reading cap:consistency |
| bounded-context/missingmass.io/shopsystem/work-management | s3, s4, s5, s6, s7 | shop/missingmass.io/shopsystem-bdd | area:tracking area:execution area:measurement |
| bounded-context/missingmass.io/shopsystem/analysis | s8, s1 | shop/missingmass.io/shopsystem-bdd | area:analysis |
| bounded-context/missingmass.io/shopsystem/upgrades | s9 | shop/missingmass.io/shopsystem-bdd | area:upgrades |

Decisions this map stands on: 0130 (the language a context of a supporting subdomain), 0131 (measurement in
execution), 0133 (tracking and execution one context, two modules).

## Assignments

The product's decision of which context each job is assigned to. The context's own capability that serves it says so
in its frontmatter (`serves: job/missingmass.io/shopsystem/j<n>`); the product never asks the context.

| job | assigned to |
|---|---|
| j1 | bounded-context/missingmass.io/shopsystem/work-management |
| j2 | bounded-context/missingmass.io/shopsystem/work-management |
| j3 | bounded-context/missingmass.io/shopsystem/work-management |
| j4 | bounded-context/missingmass.io/shopsystem/specification |
| j5 | bounded-context/missingmass.io/shopsystem/upgrades |
| j6 | bounded-context/missingmass.io/shopsystem/work-management |

## Relations between contexts

Derived, not written here: from each context's obtained contracts (adapter specs of its providers), its driven ports
and its requests. Today none is derivable: the five are one context and reach each other through state, not requests.
