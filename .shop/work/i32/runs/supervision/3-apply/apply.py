d = ".shop/work/i32/runs/i32/1-integrate/drafts/round-1/spec"
p = "spec/capabilities/supervision.md"
s = open(p).read().split("\n")
dr = open(d + "/capabilities/supervision.md").read().split("\n")
new = [l for l in dr if l.startswith("- [r118]") or l.startswith("- [r119]")]
assert len(new) == 2
i = [k for k, l in enumerate(s) if l.startswith("- [r78]")][0]
s[i + 1:i + 1] = new
t = "\n".join(s)
a = "design-decision/requests-written-through-work]"
assert a in t
t = t.replace(a, "design-decision/requests-written-through-work, design-decision/an-answer-to-a-reviewer-returns-to-ready-or-done]", 1)
open(p, "w").write(t)
