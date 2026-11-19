---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/code-analysis
title: Code analysis
narrator: the person
group: service
area: analysis
specifies: service code analysis
language: codified-2
retired: []
unbuilt: []
---

# Code analysis

## Purpose
This repository's code read: test coverage mapped and traced, untested functions screened, references located, files
linted and sized.

## Behaviour

### [g1] A coverage map is kept while a test breaks
Restates: analysis-tools#r8@0.29.
- [r1] While a test breaks, when the person maps this repository, the code analysis service shall keep a coverage map
  and complete the request.

### [g2] Mapping replaces the coverage map
Restates: analysis-tools#r8@0.29.
- [r2] While a coverage map exists, when the person maps this repository, the code analysis service shall keep a
  different coverage map.

### [g3] A function traced gives the tests that execute it
Restates: analysis-tools#r9@0.29.
- [r3] While a coverage map exists, when the person traces a function, the code analysis service shall return every test
  that executes the function, the number of tests that execute the function and the revision of the coverage map.

### [g4] A function traced by file gives the Python files of its tests
Restates: analysis-tools#r10@0.29.
- [r4] While a coverage map exists, when the person traces a function with the file view, the code analysis service
  shall return every Python file that holds a test that executes the function.

### [g5] A function no test executes traced gives the coverage map's commit
Restates: analysis-tools#r11@0.29.
- [r5] While a coverage map exists, when the person traces a function that no test executes, the code analysis service
  shall return the revision of the coverage map and complete the request.

### [g6] An identifier no Python file defines is not traced
Restates: analysis-tools#r49@0.29, analysis-tools#r57@0.29.
- [r6] While a coverage map exists, if the person traces an identifier that no Python file defines, then the code
  analysis service shall refuse the request and name the identifier.

### [g7] A function is not traced with no coverage map
Restates: analysis-tools#r49@0.29.
- [r7] While no coverage map exists, if the person traces a function, then the code analysis service shall refuse the
  request and name the coverage map.

### [g8] A Python file screened gives its functions no test executes
Restates: analysis-tools#r13@0.29.
- [r8] While a coverage map exists, when the person screens a Python file, the code analysis service shall return every
  function of the Python file that no test executes and the revision of the coverage map and complete the request.

### [g9] An identifier located gives its references
Restates: analysis-tools#r14@0.29.
- [r9] When the person locates an identifier that a Python file defines, the code analysis service shall return every
  reference to the identifier and the number of references to the identifier and complete the request.

### [g10] An identifier no Python file defines is not located
Restates: analysis-tools#r49@0.29.
- [r10] If the person locates an identifier that no Python file defines, then the code analysis service shall refuse the
  request and name the identifier.

### [g11] A file linted gives each finding under its analysis tool and fails
Restates: analysis-tools#r16@0.29.
- [r11] While a file holds a finding of an analysis tool, when the person lints the file, the code analysis service
  shall return the heading of the analysis tool and the finding, fail the check and name the finding.

### [g12] Linting fails while `vulture` is missing
Restates: analysis-tools#r17@0.29.
- [r12] While `vulture` is `missing`, when the person lints a file, the code analysis service shall fail the check and
  name `vulture`.

### [g13] A Python file over the size limit fails the sizing
Restates: analysis-tools#r50@0.29, analysis-tools#r51@0.29, analysis-tools#r52@0.29.
- [r13] While a Python file exceeds a size limit, when the person sizes this repository with the size limit, the code
  analysis service shall return the Python file, fail the check and name the Python file.

### [g14] Sizing passes when no Python file exceeds the default limit
Restates: analysis-tools#r52@0.29.
- [r14] While no Python file exceeds the `300` size limit, when the person sizes this repository without a size limit,
  the code analysis service shall complete the request.
