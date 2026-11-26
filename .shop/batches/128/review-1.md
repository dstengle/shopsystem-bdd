---
id: review/missingmass.io/shopsystem/shopsystem-bdd/batch-128/review-1
kind: review
batch: batch-128
pull_request: https://github.com/dstengle/shopsystem-bdd/pull/151
head: fd4cb104a5ce0d06cac9c3bb95a40fa336327d7d
range: 7873550ea7da0f04c30ecbe701c3e6f13ec6e96d..fd4cb104a5ce0d06cac9c3bb95a40fa336327d7d
result: clean
---

# batch-128 review 1

## Verdict

The batch builds b724's three lines: checking#r125, consistency#r44 and scenarios#r44. Nothing needs fixing before the merge; there are two minor observations.

- **checking#r125:** `model_bound` now emits `on_reply(Q, K, O)` for a core line whose trigger is a reply to the request of operation O. In `model.lp`, `handled(X)` joins on it, and a refusal reply counts as handling every refusal reason. `reason_stated` covers v_m4 for those reasons.
- **Requests in `model_domain_lines` and `model_bound`:** both now skip the request a reply is on, so a reply trigger does not count as requesting or governing the port operation.
- **The check's world:** checking_handlers_reply builds the domain-model fixture with the driven port `stock`. It asks `stock.reserve` in notebook#r10 and handles each outcome with a reply trigger (r11 on completion, r12 on refusal). It then runs `features generate` and `spec check`, and both must exit 0.
- **consistency#r44:** `spec_lf_facts_request.reply` translates the trigger as `trig(R,reply(K),req(O,()),D,X)`. The scenario is mapped to design-model-check's handlers in requested.py, and b626's existing world (design_model_check_worlds_response, `replying`) feeds it.
- **scenarios#r44:** `spec_steps4_request.reply` brings in the replied request's object with a Given and states the core's request as a Given. `np` then says "the request to <verb> <np>". feature_file_tools_request checks that every instance a step mentions is brought in by a given or a when step.
- **Tests:** none were removed or weakened. test_construct_twins goes from `LATER` holding reply-trigger to `LATER = ()`, so the twins check now covers reply-trigger.
- **The rest of the change:**
  - The `.feature` changes pass `features generate --check`.
  - Every run exits 0.
  - The size is +389 -30, under the limit of 1000.
  - The module-map rows of the changed modules are updated, and the new test file has a row.
  - The change goes against no judgement decision. Two lines on one reply clash on one trigger, as decision 0121 says.

## Findings

### f1 Minor observation: checking_handlers_reply has a `spec logic` path that no scenario reaches
- item: b724
- where: tests/scenarios/checking_handlers_reply.py:677
`GROUPS` is only `{"g125"}`, and checking#r125's scenario runs only `spec check` and has only the Then "completes this request". So `runs`' `spec logic` branch and `then_returns`, which is registered as a `ThenDoes` local, never run. The module docstring still says the When runs `spec check` or `spec logic` and that the Thens read `no findings`. That is dead test code with a misleading description; it can go, or move to a group that uses it. The consistency scenario reaches `spec logic` through design-model-check's world, not this file.

### f2 Minor observation: a reply trigger fails generation when no response doer fits the frame's subject
- item: b724
- where: scripts/spec_steps4_request.py:446
`reply` picks the core's requester from the response's doers: the first doer whose kind is under the operation frame's subject. If none fits, it raises `TraceError("no step of the request of %s a reply is on")`, and `features generate` then refuses the group. One example is a reply trigger whose response's acts are all by an agent the frame's `<actor>` slot does not take. Separately, when a different service makes the response, the Given names that service as the requester, which may not be who asked. No line of the batch names either case, and the batch's worlds do not hit it. Reproduction: write a reply-trigger line whose response's only act is by an agent outside the reserve frame's subject kind, then run `features generate`.
