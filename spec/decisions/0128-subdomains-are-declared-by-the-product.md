---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/subdomains-are-declared-by-the-product
summary: "A subdomain (problem space, core, supporting or generic) is declared at the product level; a bounded context (solution space) addresses one or more subdomains and a subdomain may be addressed by several bounded contexts."
date: 2026-11-24
status: accepted
tier: judgement
source: [quote-80]
---

# 0128. Subdomains are declared by the product

## Context

The term area mixed a subdomain's classification with parts of a bounded context's model; the person placed subdomains at the product level, as the business problems they are.

## Decision

Subdomains and their classification belong to the product, never to a bounded context's model. The relationship between bounded contexts and subdomains is many to many: a context may address one subdomain, be one of several addressing a subdomain, or, in a repository that is many things at once, address several. A bounded context's model carries no core, supporting or generic kind of its own.
