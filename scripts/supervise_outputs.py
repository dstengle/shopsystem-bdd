"""What a stage's result must give for `work run` to take its work as done (supervision r131, r132, design-decision
0038): the stage's output, and the question that says it is missing. The one word a result's status gives decides no
transition (r133). An integrate round's output is codified drafts: `uncodified` parses each drafted requirement and
runs the logic check on the spec with the drafts (the GF conversion's design §13). Standard library, and the grammar
modules once drafts are checked."""
import re
import shutil
import tempfile
from pathlib import Path

from spec_read import is_guarantees  # noqa: F401  (supervise_formulate imports it from here)

UNCODIFIED = "The drafted requirements are refused by the grammar or the logic check"


def given(data, field):
    """Whether the result `data` gives `field`: a list with something in it, or a text that is not blank."""
    value = data.get(field)
    return bool(value) and (not isinstance(value, str) or bool(value.strip()))


def missing(role, data):
    """What the stage of `role` (researcher, planner, reviewer) was to deliver and its result `data` does not give, as
    words (the researcher's file set), else None. The implementer's output is commits the tests pass on; the merge says
    if they are missing."""
    if role == "researcher" and not isinstance(data.get("fileset"), list) and not given(data, "fileset"):     # [] says no file changes
        return "the researcher's file set"
    if role == "planner":
        if not given(data, "plan"):
            return "the planner's plan"
        if not given(data, "fileset"):
            return "the planner's file set"
    if role == "reviewer" and not given(data, "findings"):
        return "the reviewer's findings"
    return None


def says(data, field):
    """Whether the result `data` gives `field` as a sentence and gives no question."""
    said = data.get(field) if isinstance(data, dict) else None
    return isinstance(said, str) and bool(said.strip()) and not data.get("questions")


def gives_nothing(data):
    """Whether an apply round's result gives that it applied nothing, because the proposal's answers give what its drafts
    do not hold: its `nothing_applied` field, with no question and no change list (r147)."""
    return says(data, "nothing_applied") and data.get("changes") in (None, [])


def sent_back(kind, data):
    """Whether the result `data` of a round of `kind` sends the proposal back to integration: an apply round that gives
    an answer its drafts do not hold, as `unheld_answers` or as `nothing_applied` (r150). A formulate round is a script
    and sends nothing back (design §13.1)."""
    if kind == "apply":
        unheld = data.get("unheld_answers") if isinstance(data, dict) else None
        return gives_nothing(data) or (isinstance(unheld, list) and bool(unheld))
    return False


def question(role, what):
    """The question that names `what` as missing from the result of the stage of `role`, which gave no question."""
    return "%s is missing: the %s's result gave no question and does not give it" % (what, role)


def overlay(live, draft):
    """The text of a spec file `live` with the drafted sections of `draft` in place: a drafted frontmatter replaces
    the file's, a drafted `## <heading>` section replaces the one of that heading or is added after the last. A draft
    with a frontmatter and a `# ` title is a whole file."""
    def split(text):
        head, body = "", text
        if text.startswith("---\n") and "\n---\n" in text[4:]:
            end = text.index("\n---\n", 4) + 5
            head, body = text[:end], text[end:]
        parts = re.split(r"(?m)^(?=## )", body)
        return head, parts[0], {p.split("\n", 1)[0].strip(): p for p in parts[1:]}, [p.split("\n", 1)[0].strip() for p in parts[1:]]
    d_head, d_lead, d_secs, d_order = split(draft)
    if not live or (d_head and re.search(r"(?m)^# ", d_lead)):
        return draft
    head, lead, secs, order = split(live)
    for name in d_order:
        if name not in secs:
            order.append(name)
        secs[name] = d_secs[name]
    body = "".join(secs[n].rstrip("\n") + "\n\n" for n in order)
    return (d_head or head) + lead.rstrip("\n") + "\n\n" + body.rstrip("\n") + "\n"


def drafted(root, drafts, into):
    """`spec/` of `root` copied to `into`, each round's drafts under `drafts` (`round-<n>/spec/...`) laid over it in
    round order; the capability names drafted."""
    root, into = Path(root), Path(into)
    shutil.copytree(root / "spec", into / "spec", dirs_exist_ok=True)
    rounds = sorted((p for p in Path(drafts).glob("round-*") if p.name[6:].isdigit()), key=lambda p: int(p.name[6:]))
    names = []
    for rnd in rounds:
        for path in sorted((rnd / "spec").rglob("*.md")):
            target = into / path.relative_to(rnd)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(overlay(target.read_text() if target.is_file() else "", path.read_text()))
            if path.parent.name == "capabilities" and path.stem not in names:
                names.append(path.stem)
    return names


def uncodified(root, drafts):
    """What refuses the codified drafts under `drafts` (an integrate round's drafts path): a file problem
    (`<cap>.md: ...`), a requirement that does not parse in the context's grammar with the drafted terms
    (`<cap>#r<n>: ...` with the hint), and each L1 or L3 of the logic check on the spec with the drafts. A draft of a
    capability that is not codified is not checked. Empty when nothing refuses them."""
    if not Path(drafts).is_dir():
        return []
    import spec_grammar
    import spec_read
    import spec_solve
    tmp = Path(tempfile.mkdtemp(prefix="uncodified-"))
    try:
        names = drafted(root, drafts, tmp)
        caps = [n for n in names if spec_read.codified(tmp / "spec" / "capabilities" / ("%s.md" % n))]
        refused = []
        for name in caps:
            cap = spec_read.capability(tmp / "spec" / "capabilities" / ("%s.md" % name))
            refused += ["%s.md: %s" % (name, p) for p in cap.problems]
            for req in (r for g in cap.groups for r in g.requirements):
                parsed = spec_grammar.parse(tmp, req.text)
                if parsed.tree is None:
                    hint = spec_grammar.hint(tmp, req.text)
                    refused.append("%s#%s: %s; parsed up to: %s; nearest words: %s" % (
                        name, req.id, parsed.refusal, hint["prefix"] or "nothing", ", ".join(hint["near"]) or "none"))
        if refused:
            return refused
        return ["%s %s" % (f.code, f.text) for name in caps for f in spec_solve.run(tmp, name)
                if f.code in spec_solve.ERRORS]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def uncodified_question(refused, send_backs):
    """The question on drafts still refused after `send_backs` send-backs, else None; its answer goes back to
    integration."""
    if not refused:
        return None
    return ("%s after %d send-backs: %s. Readings: reword the refused requirements as your answer says, and integration "
            "drafts them again (recommended); or drop them from the proposal." % (UNCODIFIED, send_backs, "; ".join(refused)))


def refused_proposals(paths, refused):
    """The names of the capability-proposals among `paths` that a refusal names, else of all of them."""
    mine = [p.stem for p in map(Path, paths) if p.suffix == ".md" and p.is_file()
            and re.search(r"(?m)^kind: capability-proposal$", p.read_text())]
    named = [m for m in mine if any(r.startswith((m + "#", m + ".md")) or (" %s#" % m) in r for r in refused)]
    return named or mine
