---
id: capability/missingmass.io/shopsystem/shopsystem-bdd/trials
title: Trials
narrator: the session that started a trial
group: guarantees
area: measurement
specifies: guarantees of a trial
language: codified-2
retired: []
unbuilt: []
---

# Trials

## Purpose
One trial conducted by `trial-runner` on its target, changing nothing but the measurement it keeps.

## Behaviour

### [g11] A trial handed to `trial-runner` is conducted
Restates: trials#r1@0.29.
- [r11] When a session hands a trial to `trial-runner`, `trial-runner` shall conduct the trial.

### [g12] A trial reads only its target
Restates: trials#r2@0.29.
- [r12] `trial-runner` shall review only files in the target of a trial.

### [g13] A trial changes only its measurement
Restates: trials#r3@0.29.
- [r13] `trial-runner` shall change only the measurement of a trial.

### [g14] A trial's measurement names its target
Restates: trials#r4@0.29.
- [r14] When `trial-runner` conducts a trial, `trial-runner` shall change a measurement of the trial that includes the
  target of the trial.

### [g15] A trial's reply names its measurement
Restates: trials#r5@0.29.
- [r15] While a trial has a measurement, when `trial-runner` conducts the trial, `trial-runner` shall name the
  measurement of the trial.
