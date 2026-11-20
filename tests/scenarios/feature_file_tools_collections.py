"""feature-file-tools' capabilities of every, only, counts and two (b273): the lines of the collections review
(.shop/records/2026-11-15-collections-review.md, its c1, c6, c7, c10, c11, c12, c15, c19, c20) said in the construct
catalogue's context (`grammar/corpus/constructs/`), one group each, and what the scenario `features generate` writes of
each must hold.

`kind` picks the lines a scenario's Givens describe (`LINES`' key); `check` reads the feature back for its Then: a
counter-example (r117-r119, r128, r134), the precondition satisfied (r114, r129), the boundary of a count (r115), each instance a Given
introduces (r116; of a printed thing's holds and of an order, r131, r132; of a thing a response names by its
owner, scenarios#r33, an indexical, r34) and no step that asserts an act `only` allows (r118)."""
import re

# (line, [patterns its scenario must hold], [patterns it must not])
COUNTER = r"(?:Then|And) `work` does not print the %s\n"
LINES = {
    "every": [
        ("When the person runs `work status` on a worktree, `work` shall print every file in the worktree.",
         [r"And the worktree w1 does not hold the file f3\n", COUNTER % "file f3", r"`work` prints the file f1\n"], []),
        ("When the person runs `work status`, `work` shall print every stage whose status is `done`.",
         [r"And the status of the stage s3 is `open`\n", COUNTER % "stage s3", r"`work` prints the stage s2\n"], [])],
    "only": [
        ("When the person runs `work status` on a worktree, `work` shall print only files in the worktree.",
         [r"And the worktree w1 does not hold the file f1\n", COUNTER % "file f1"], [r"`work` prints the file"]),
        ("When the person runs `work status`, `work` shall print only stages whose status is `done`.",
         [r"And the status of the stage s1 is `open`\n", COUNTER % "stage s1"], [r"`work` prints the stage"])],
    "upper": [
        ("When the person runs `work status`, `work` shall print exactly three files.",
         [r"And a file f4\n", r"Then `work` prints exactly three files\n"], [r"a file f5", r"prints the file"]),
        ("When the person runs `work status`, `work` shall print one file.",
         [r"And a file f2\n", r"Then `work` prints one file\n"], [r"a file f3", r"prints the file"]),
        ("When the person runs `work status`, `work` shall print fewer than three files.",
         [r"And a file f3\n", r"Then `work` prints fewer than three files\n"], [r"a file f4", r"print the file"]),
        ("When the person runs `work status` on a worktree, `work` shall print at most three files in the worktree.",
         [r"And the worktree w1 holds the file f4\n", r"Then `work` prints at most three files in the worktree w1\n"],
         [r"a file f5", r"print the file"])],
    "capped": [     # b296: one K2 past the bound of a count over the row of a response's object, held by no step
        ("When the person runs `work status`, `work` shall print a worktree that holds at most three files.",
         [r"Given a file f1\n", r"And a file f4\n",
          r"Then `work` prints the worktree w1\n    And the worktree w1 holds at most three files\n"],
         [r"a file f5", r"holds the file"]),
        (("When the person runs `work status`, `work` shall print a worktree that holds fewer than three files "
          "whose version is `2.0.0`."),
         [r"Given a file f1\n", r"And a file f3\n", r"And the version of the file f3 is `2.0.0`\n",
          r"And the worktree w1 holds fewer than three files whose version is `2.0.0`\n"],
         [r"a file f4", r"holds the file"])],
    "satisfy": [
        (("While a stage has a line and every line of the stage is `accepted`, when the person runs `work status`, "
         "`work` shall print the stage."),
         [r"And the outcome of the line l1 is `accepted`\n"], [r"line l2"])],
    "negated": [     # b310: every over a negated value, satisfied by a Given of the value negated
        (("While a stage has a line and every line of the stage is not `refused`, when the person runs `work status`, "
         "`work` shall print the stage."),
         [r"And the outcome of the line l1 is not `refused`\n", r"Then `work` prints the stage s1\n"], [r"line l2"])],
    "boundary": [
        (("While a worktree holds at least two files, when the person runs `work status`, `work` shall print the "
         "worktree."), 2),
        (("While a worktree holds at most two files, when the person runs `work status`, `work` shall print the "
         "worktree."), 2),
        (("While a worktree holds exactly two files, when the person runs `work status`, `work` shall print the "
         "worktree."), 2),
        (("While a worktree holds more than two files, when the person runs `work status`, `work` shall print the "
         "worktree."), 3),
        (("While a worktree holds fewer than two files, when the person runs `work status`, `work` shall print the "
         "worktree."), 1),
        (("While a worktree holds a file and the number of files in the worktree is more than three, when the person "
         "runs `work status`, `work` shall print the worktree."), 4)],
    "noholds": [     # b299: the counter-example a file the worktree does not hold, the Then said of no file
        ("When the person runs `work status`, `work` shall print a worktree that holds no file.",
         [r"Given a file f1\n", r"Then `work` prints the worktree w1\n", r"And the worktree w1 holds no file\n"],
         [r"holds the file f1", r"Given a worktree"])],
    "two": [
        ("When the person runs `work status`, `work` shall print two files.", [], []),
        ("When the person runs `work status`, `work` shall print a worktree that holds two files.", [], [])],
    "held": [       # b286: the held thing of a printed thing's holds Then brought in
        ("When the person runs `work status`, `work` shall print a worktree that holds a file.", [], [])],
    "ordered": [    # b286: the order-by example, each member brought in
        (("When the person runs `work start`, `work` shall print a worktree that holds a file, ordered by version, in "
          "descending order."), [], [])],
    "owned": [      # b416: the thing a response names by its owner, a trigger's thing, brought in with its row
        ("When the person runs `work status` on a stage, `work` shall print the lines of the stage.", [], []),
        ("When the person runs `work status` on a session, `work` shall print the worktree of the session.", [], [])],
    "owned-this": [     # b421: the owner an indexical, this K
        ("When the person runs `work status`, `work` shall print the push of this command.", [], [])],
}


def kind(w, K):
    """The lines the Givens describe: a precondition that uses every or holds a count, a requirement that uses two,
    every or only with a restriction, or no-noun (b299), or has an upper bound (of a count over a row of a response's
    object: b296), a precondition of every over a not
    (b310); None for none of these."""
    facts = {(v, K(w, a), b if str(b).startswith("`") else K(w, b)) for v, a, b, pos in w["facts"] if pos}
    if {("use", "precondition", "`every`"), ("use", "precondition", "`not-condition`")} <= facts:
        return "negated"
    if {("use", "requirement", "`count`"), ("use", "requirement", "`holds-relation`"),
            ("has", "requirement", "upper bound")} <= facts:     # b296
        return "capped"
    if ("mention", "step", "instance") in facts:     # b286: a step that mentions an instance no Given introduces
        if ("use", "requirement", "`order-by`") in facts:
            return "ordered"
        if {("use", "requirement", "`holds-relation`"), ("use", "requirement", "`rc-subject`")} <= facts:
            return "held"
        if ("use", "requirement", "`of-relation`") in facts:     # b416, b421
            for code in ("this",):
                if ("use", "requirement", "`%s`" % code) in facts:
                    return "owned-" + code
            return "owned"
    for fact, name in ((("use", "precondition", "`every`"), "satisfy"), (("use", "requirement", "`no-noun`"), "noholds"),
                       (("holds", "precondition", "count"), "boundary"),
                       (("use", "requirement", "`two`"), "two"), (("has", "requirement", "upper bound"), "upper"),
                       (("use", "requirement", "`only`"), "only"), (("use", "requirement", "`every`"), "every")):
        if fact in facts:
            return name
    return None


def groups(name):
    """The groups of a capability of the lines `name` picks."""
    return "\n".join("### [g%d] %s %d\n- [r%d] %s\n" % (k, name, k, k, line[0])
                     for k, line in enumerate(LINES[name], 1))


def scenarios(text):
    """[(group number, the scenario's text)] of a feature."""
    parts = re.split(r"^  @g(\d+) ", text, flags=re.MULTILINE)[1:]
    return [(int(parts[k]), parts[k + 1]) for k in range(0, len(parts), 2)]


def introduced(text):
    """Each instance a scenario mentions that no Given brings in."""
    brought = set(re.findall(r"^    (?:Given|And) an? [a-z ]+? ([a-z]\d+)$", text, re.MULTILINE))
    named = set(re.findall(r"\bthe [a-z]+ ([a-z]\d+)\b", text))
    return named - brought


def check(name, text, what):
    """AssertionError naming the group and the pattern when a scenario of the feature lacks what `what` asks:
    "counter-example", "satisfy", "boundary", "introduce" or "assert" (no step asserting what only allows)."""
    found = dict(scenarios(text))
    assert len(found) == len(LINES[name]), text
    for g, line in enumerate(LINES[name], 1):
        s = found[g]
        if what == "boundary":
            held = re.findall(r"^    And the worktree w1 holds the file f\d+$", s, re.MULTILINE)
            assert len(held) == line[1], (g, line[1], s)
            assert not introduced(s), (g, introduced(s), s)
        elif what == "introduce":
            assert not introduced(s), (g, introduced(s), s)
        elif what == "assert":
            assert not any(re.search(p, s) for p in line[2]), (g, line[2], s)
        else:
            missing = [p for p in line[1] if not re.search(p, s)] + [p for p in line[2] if re.search(p, s)]
            assert not missing, (g, missing, s)
