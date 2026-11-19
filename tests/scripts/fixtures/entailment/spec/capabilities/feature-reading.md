---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/feature-reading
title: Feature reading
narrator: the person
group: service
area: analysis
specifies: service feature reading
language: codified-2
retired: []
unbuilt: []
---

# Feature reading

## Purpose
The Gherkin of feature files read: scenarios searched, counted by tag, deprecated ones scanned and bindings vetted.

## Behaviour

### [g1] Counting by tag counts the scenarios of a feature file whose docstring holds a tag
Restates: feature-file-tools#r1@0.29, feature-file-tools#r4@0.29.
- [r1] While a docstring of a feature file contains a tag and a scenario line, when the person counts the feature file,
  the feature reading service shall return the number of scenarios of the feature file.

### [g2] Counting by tag counts the examples rows of a scenario outline
Restates: feature-file-tools#r4@0.29.
- [r2] While a feature file has a scenario outline and the feature file has no scenario, when the person counts the
  feature file, the feature reading service shall return the number of examples rows of the scenario outline.

### [g3] A tag only in a docstring finds no feature file
Restates: feature-file-tools#r1@0.29, feature-file-tools#r7@0.29.
- [r3] While a docstring of a feature file contains a tag and the feature file does not have the tag, when the person
  searches this repository with the tag, the feature reading service shall complete the request and not return the
  feature file.

### [g4] A search by title finds a feature file in a subdirectory
Restates: feature-file-tools#r1@0.29.
- [r4] While a feature file in a subdirectory has a scenario, when the person searches this repository with the scenario
  title of the scenario, the feature reading service shall return the feature file.

### [g5] A search by a feature file's tag finds its every scenario
Restates: feature-file-tools#r5@0.29.
- [r5] While a feature file has a tag, when the person searches this repository with the tag, the feature reading
  service shall return every scenario of the feature file.

### [g6] A search by a scenario's tag finds the scenario
Restates: feature-file-tools#r5@0.29.
- [r6] While a scenario has a tag, when the person searches this repository with the tag, the feature reading service
  shall return the scenario.

### [g7] A search by a search text finds each scenario whose title contains it
Restates: feature-file-tools#r5@0.29.
- [r7] When the person searches this repository with a search text, the feature reading service shall return every
  scenario whose scenario title contains the search text.

### [g8] Counting by tag refuses a feature file with a rule block
Restates: feature-file-tools#r2@0.29, feature-file-tools#r46@0.29.
- [r8] While a feature file has a rule block, if the person counts the feature file, then the feature reading service
  shall refuse the request and name the feature file.

### [g9] A scan gives each deprecated scenario with its replacement's requirement tags
Restates: feature-file-tools#r21@0.29.
- [r9] While a replacement of a scenario has a requirement tag and the scenario has the `@deprecated` tag, when the
  person scans this repository, the feature reading service shall return the scenario and every requirement tag of the
  replacement.

### [g10] A scan with no deprecated scenario says so
Restates: feature-file-tools#r21@0.29.
- [r10] While no scenario has the `@deprecated` tag, when the person scans this repository, the feature reading service
  shall return `none deprecated`.

### [g11] Vetting passes when every binding binds a scenario
Restates: feature-file-tools#r26@0.29.
- [r11] While every binding binds a scenario, when the person vets this repository, the feature reading service shall
  return `every binding names a scenario` and complete the request.

### [g12] Vetting fails on a binding that binds no scenario
Restates: feature-file-tools#r25@0.29.
- [r12] While a binding of a test module binds no scenario, if the person vets this repository, then the feature reading
  service shall fail the check, name the test module and change no file.

### [g13] Vetting the unbound scenarios passes when a scenarios call binds them
Restates: feature-file-tools#r57@0.29.
- [r13] While a scenarios call binds a scenario of a feature file, when the person vets this repository with the unbound
  listing, the feature reading service shall complete the request and not return a scenario of the feature file.

### [g14] Vetting the unbound scenarios fails on a scenario no binding binds
Restates: feature-file-tools#r58@0.29.
- [r14] While a feature file has a scenario that no binding binds, if the person vets this repository with the unbound
  listing, then the feature reading service shall fail the check, name the scenario and change no file.
