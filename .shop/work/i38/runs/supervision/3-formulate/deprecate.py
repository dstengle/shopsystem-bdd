import subprocess, sys
F = "/home/vscode/.claude/plugins/cache/shopsystem-bdd/shopsystem-bdd/0.26.0/scripts/features"
R4 = "an implementer whose result gives no question has its branch merged only if the work-item's scenarios and the whole suite pass on it: <case>"
rows = [
 ("a worker's outcome DONE makes the work-item's transition to its next status", None),
 ("an implementer's DONE is merged into the initiative branch when the work-item's scenarios and the whole suite pass on its branch", R4),
 ("an implementer's DONE whose <tests> fail is not merged", R4),
 ("an implementer's DONE whose scenarios pass only on a file it left uncommitted is not merged", R4),
 ("an implementer's DONE whose whole suite fails only on a scenario r43 counts as expected is merged", R4),
 ("an implementer's DONE whose <tests> fail makes the work-item's transition to awaiting-answer", None),
 ("a researcher that gives <outcome> makes the work-item's transition to awaiting-answer", None),
 ("a researcher's DONE with questions puts those questions into the planner's brief", None),
 ("when the formulate round `work run` started for a capability-proposal gives questions, each is written under the proposal's ## Questions", None),
 ("when the formulate round `work run` started for a capability-proposal gives a question, the proposal is awaiting-answer", None),
 ("implementers working at the same time that end with DONE have their branches merged one at a time, in the order they ended", "implementers working at the same time have the branches r4 merges merged one at a time, in the order they ended"),
 ("a planner's DONE with a `fileset` writes that file set into the work-item as it makes the transition to planned", "a planner's result with a `fileset` writes that file set into the work-item as it makes the transition to planned"),
 ("a worker whose session <ending> makes the work-item's transition to failed, whatever its result says", "a worker whose session <ending> makes the work-item's transition to failed, recording how the session ended"),
 ("when a round `work run` started for a capability-proposal gives an outcome other than DONE, no transition is made from it", "the <kind> round of <node> that <ending> brings no transition"),
 ("when a round `work run` started for a capability-proposal leaves no result it can read, `work run` exits with an error naming the round and how it ended", "the <kind> round of <node> that <ending> ends `work run` with an error naming the round and how it ended"),
 ("when a session started under a delegation to answer a question ends at its turn limit, the question is left unanswered for the person", "when a session started under a delegation to answer a question <ending>, the question is left unanswered for the person"),
 ("when a session started under a delegation to answer a question ends in an error, its stage directory and log lines are committed", "when a session started under a delegation to answer a question <ending>, its stage directory and log lines are committed"),
 ("when the gate round of a capability-proposal <ending>, the initiative's other nodes are taken through their transitions before `work run` exits with an error", "when the gate round of a capability-proposal <ending>, the initiative's other nodes are taken through their transitions before `work run` exits with an error"),
]
for old, new in rows:
    if new == old:
        # same title: deprecate for the new scenario of the same title
        pass
    cmd = [sys.executable, F, "deprecate", old, "--file", "features/supervision.feature"] + (["--for", new] if new else ["--for-removal"])
    r = subprocess.run(cmd, capture_output=True, text=True)
    print(r.returncode, old[:60], r.stdout.strip()[:120], r.stderr.strip()[:200])
    if r.returncode: sys.exit(1)
    r = subprocess.run([sys.executable, F, "rebind", "--file", "features/supervision.feature", old, old + " (deprecated)"], capture_output=True, text=True)
    print("  rebind", r.returncode, r.stdout.strip()[:120], r.stderr.strip()[:200])
