import re, sys

D = ".shop/scratch/8-formulate/drafts/round-1/"


def blocks(path):
    lines = open(path).read().split("\n")
    out, cur = {}, None
    for ln in lines[3:]:
        m = re.match(r"\s+@(r\d+)\s*$", ln)
        if m:
            cur = m.group(1)
            out[cur] = []
        if cur and not ln.strip().startswith("# "):
            out[cur].append(ln)
    return {k: "\n".join(v).rstrip("\n") + "\n" for k, v in out.items()}


def splice(feature, draft, after):
    # after: {new id: (anchor kind, text of Scenario title start of the scenario to insert after)}
    b = blocks(draft)
    text = open(feature).read()
    for rid, anchor in after.items():
        # insert block after the scenario whose title line contains anchor (end at next blank-line + "  @")
        i = text.index(anchor)
        m = re.compile(r"\n\n(?=  @r\d+)").search(text, i)
        pos = m.start() + 2 if m else len(text)
        if not m:
            text = text.rstrip("\n") + "\n"
            pos = len(text)
            text += "\n"
        text = text[:pos] + b[rid] + "\n" + text[pos:]
    open(feature, "w").write(text.rstrip("\n") + "\n")


if sys.argv[1] == "wq":
    splice("features/work-queue.feature", D + "work-queue/work-queue.feature", {
        "r32": "Scenario: add numbers the new work-item one above",
        "r23": "sets the initiative to done (deprecated)",
        "r31": "Scenario: retry that makes an initiative's last open work-item",
    })
else:
    splice("features/supervision.feature", D + "supervision/supervision.feature", {
        "r121": "Scenario: a kept branch review's findings to fix now get one work-item",
        "r75": "Scenario: a kept branch review that ended PARTIAL",
        "r105": "Scenario: an initiative whose work-items are green or withdrawn, whose branch review lists nothing to fix now, whose measurement and analysis record are committed and whose requests are delivered is set done (deprecated)",
    })
