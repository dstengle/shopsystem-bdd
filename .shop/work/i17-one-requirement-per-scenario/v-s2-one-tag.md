---
id: work-item/missingmass.io/shopsystem/shopsystem-bdd/v-s2-one-tag
kind: work-item
part_of: capability-proposal/one-requirement-design-model-check
status: drafted
wkind: capability
under: design-model-check
accepts: [design-model-check#r1, design-model-check#r2, design-model-check#r3, design-model-check#r4, design-model-check#r5, design-model-check#r6, design-model-check#r7, design-model-check#r8, design-model-check#r9, design-model-check#r10, design-model-check#r11, design-model-check#r12, design-model-check#r13, design-model-check#r14, design-model-check#r15, design-model-check#r16, design-model-check#r17, design-model-check#r18, design-model-check#r19, design-model-check#r20, design-model-check#r21, design-model-check#r22, design-model-check#r23, design-model-check#r24, design-model-check#r25, design-model-check#r26, design-model-check#r27, design-model-check#r29, design-model-check#r33, design-model-check#r34, design-model-check#r35, design-model-check#r36, design-model-check#r37, design-model-check#r43, design-model-check#r46, design-model-check#r48, design-model-check#r49, design-model-check#r51, design-model-check#r52, design-model-check#r53, design-model-check#r54, design-model-check#r55, design-model-check#r59, design-model-check#r61, design-model-check#r64, design-model-check#r65, design-model-check#r66, design-model-check#r103, design-model-check#r104, design-model-check#r105, design-model-check#r106, design-model-check#r107]
fileset: [scripts/model, scripts/model.lp, scripts/model_*.py, tests/scripts/test_model.py, tests/scenarios/*design_model_check*.py, features/design-model-check.feature, docs/capability-format.md]
---

# `model check` reports a scenario with more than one `@r<n>` tag

Goes green: design-model-check r20 and r107 as changed: a scenario not tagged `@deprecated` with more than one
`@r<n>` tag, its own and its feature's together, is printed under v_s2 with its plain label (today model.lp's FIX
note says v_s2 is gone, per the superseded decision 0052). docs/capability-format.md's Verifying lists v_s2 once it
is printed.

Owns the whole of features/design-model-check.feature as the blind formulator rewrote it for 0.22.0 (one requirement per scenario, exits in words): every scenario green, retitled bindings rebound, the deprecated ones retired once their replacements are green.
