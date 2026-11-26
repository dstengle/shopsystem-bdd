---
id: design-decision/missingmass.io/shopsystem/shopsystem-bdd/an-area-s-module-group-is-declared-in-the-shop-s-modules-table
summary: "Which Python files carry an area's code is declared in .shop/modules.toml, one table an area with the path patterns of its files, read by spec coupling and kept in step with the import contracts."
date: 2026-11-26
status: accepted
tier: judgement
---

# 0151. An area's module group is declared in the shop's modules table

## Context

b744 reports the code imports between the areas of the domain model (decisions 0129-0133) and b614 keeps an import boundary per area; neither the module map (rows of concerns) nor the capabilities' handlers say which files are an area's code.

## Decision

A shop declares its areas' module groups in .shop/modules.toml: a table [<area>] an area of spec/model/ with modules, a list of path patterns relative to the repository's root (glob, ** across folders). A Python file matched by the patterns of two areas is the first table's in file order. A Python file no table matches belongs to no area and couples none. The table is the shop's configuration (decision 0129), not the specification: the domain model keeps no file paths. Once an area's files are a package of their own (b614), its pattern is that package's folder.

## Alternatives

Derived from the module map or the capabilities' handlers: rejected, the module map names concerns and many modules serve several areas, so the derivation would guess. A modules: list in each spec/model/<area>.md frontmatter: rejected, it puts file paths of the code into the domain model.
