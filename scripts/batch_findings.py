"""The pull request review's findings (capability pr-review r8; workflow simplification plan 5, D9, D10, D13, D22):
the findings file (`pr-reviewer`'s reply, saved by the batch session), parsed and refused when a finding is ungraded
or malformed, and the record `.shop/batches/<n>/review-<k>.md` that `work batch reviewed` renders from it.

A finding is `### <grade> <triage>: <title>` with `- item:` and `- where:` lines and free text; the record numbers it
`### f<m> ...`. A finding is open from its review on while it is `fix now`, until a later review says `fixed` or its
item leaves the batch. `parse(render(review), rel) == review`."""
import re
from dataclasses import dataclass, field
from pathlib import Path

import backlog_items
import batch_git
import batch_plan
import shop_files
from shop_files import Refused

GRADES = ("Critical", "Important", "Minor")
TRIAGES = ("fix now", "observation", "drop")
RESULTS = ("fix-now", "clean")
SECTIONS = ("Verdict", "Findings", "Earlier findings")
HEADING = re.compile(r"^### (?:(f[1-9]\d*) )?(\S+) (.+?):(?: (.*))?$")
EARLIER = re.compile(r"^- (f[1-9]\d*): (fixed|not fixed: \S.*)$")


@dataclass
class Finding:
    fid: str | None
    grade: str
    triage: str
    title: str
    item: str | None
    where: str | None
    body: str


@dataclass
class Review:
    number: int
    batch: str
    ident: str
    pull_request: str
    head: str
    range: str
    result: str
    verdict: str
    findings: list = field(default_factory=list)
    earlier: dict = field(default_factory=dict)


def _name(batch):
    return getattr(batch, "name", batch)


def quoted(subject):
    """A commit's subject in one pair of quotes, a `"` or `\\` in it escaped (review M4)."""
    return '"%s"' % subject.replace("\\", "\\\\").replace('"', '\\"')


def rel_of(batch_name, k):
    return (batch_plan.BATCHES / str(batch_plan.number(_name(batch_name))) / ("review-%d.md" % k)).as_posix()


def scratch(root, batch, k):
    """The review's scratch directory in the ignored worktrees directory: its brief, change and findings file."""
    return batch_git.trees_dir(root) / ("%s-review-%d" % (_name(batch), k))


def _fenced(lines):
    """(line, whether it is text in a fenced block) of each line; a fence's own lines are text too (review S2)."""
    fence = None
    for line in lines:
        mark = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
        if fence is None and mark:
            fence = mark.group(1)
            yield line, True
        elif fence is not None:
            if mark and mark.group(1)[0] == fence[0] and len(mark.group(1)) >= len(fence) and \
                    not line.strip()[len(mark.group(1)):].strip():
                fence = None
            yield line, True
        else:
            yield line, False


def _sections(text, rel):
    found, heading = {}, None
    for line, fenced in _fenced(text.split("\n")):
        if line.startswith("## ") and not fenced:
            heading = line[3:].strip()
            if heading not in SECTIONS:
                raise Refused("%s: ## %s is not a section of a findings file (%s)" % (
                    rel, heading, ", ".join("## %s" % s for s in SECTIONS)))
            if heading in found:
                raise Refused("%s: ## %s is there twice" % (rel, heading))
            found[heading] = []
        elif heading is not None:
            found[heading].append(line)
        elif line.strip() and not line.startswith("# "):
            raise Refused("%s: a line before the first `## ` section: %s" % (rel, line))
    return {h: "\n".join(b).strip("\n") for h, b in found.items()}


def _value(line, key, rel):
    if not line.startswith("- %s: " % key):
        raise Refused("%s: the line %r is not `- %s: <value>` (or `- %s: -`)" % (rel, line, key, key))
    value = line[len("- %s: " % key):].strip()
    return None if value in ("", "-") else value


def _findings(text, rel, numbered):
    if text.strip() == "None.":
        return []
    found, current = [], None
    for line, fenced in _fenced(text.split("\n")):
        if line.startswith("### ") and not fenced:
            m = HEADING.match(line)
            if not m or (numbered and not m.group(1)) or (not numbered and m.group(1)):
                raise Refused("%s: the heading %r is not `### %s<grade> <triage>: <title>`" % (
                    rel, line, "f<m> " if numbered else ""))
            fid, grade, triage, title = m.groups()
            if grade not in GRADES:
                raise Refused("%s: %s: the grade %r is not one of %s" % (rel, line, grade, ", ".join(GRADES)))
            if triage not in TRIAGES:
                raise Refused("%s: %s: the triage %r is not one of %s" % (rel, line, triage, ", ".join(TRIAGES)))
            if not (title or "").strip():
                raise Refused("%s: %s: the finding has no title" % (rel, line))
            current = [line, fid, grade, triage, title.strip(), []]
            found.append(current)
        elif current is None:
            if line.strip():
                raise Refused("%s: ## Findings: a line that is not under a `### ` heading: %s" % (rel, line))
        else:
            current[5].append(line)
    out = []
    for line, fid, grade, triage, title, rest in found:
        while rest and not rest[0].strip():
            rest.pop(0)
        if len(rest) < 2:
            raise Refused("%s: %s: the finding has no `- item:` and `- where:` lines" % (rel, line))
        item, where = _value(rest[0], "item", rel), _value(rest[1], "where", rel)
        body = "\n".join(rest[2:]).strip("\n")
        if triage == "fix now" and not body.strip():
            raise Refused("%s: %s: a fix now finding has no text after its `- where:` line: say what is wrong, why it "
                          "matters and the fix" % (rel, line))
        out.append(Finding(fid, grade, triage, title, item, where, body))
    return out


def _earlier(text, rel):
    earlier = {}
    for line in text.split("\n"):
        if not line.strip() or line.strip() == "None.":
            continue
        m = EARLIER.match(line)
        if not m:
            raise Refused("%s: ## Earlier findings: the line %r is not `- f<m>: fixed` or `- f<m>: not fixed: <why>`"
                          % (rel, line))
        if m.group(1) in earlier:
            raise Refused("%s: ## Earlier findings: %s is there twice" % (rel, m.group(1)))
        earlier[m.group(1)] = m.group(2)
    return earlier


def parse_findings(text, rel, items, in_batch, open_ids):
    """(verdict, findings, earlier) of the agent's findings file (D9), checked against the batch's items, those still
    `in-batch`, and the open findings it must answer; refused as `<rel>: <what>`, naming the line."""
    sections = _sections(text, rel)
    verdict = sections.get("Verdict", "").strip()
    if not verdict:
        raise Refused("%s: ## Verdict is missing or empty" % rel)
    if "Findings" not in sections:
        raise Refused("%s: ## Findings is missing (write `None.` under it when there are none)" % rel)
    findings = _findings(sections["Findings"], rel, numbered=False)
    for f in findings:
        if f.item is not None and f.item not in items:
            raise Refused("%s: %s: - item: %s is not an item of the batch" % (rel, f.title, f.item))
        if f.triage == "fix now" and f.item not in in_batch:
            raise Refused("%s: %s: a fix now finding names - item: %s, not an item in-batch, whose branch its fix "
                          "goes on" % (rel, f.title, f.item or "-"))
    earlier = _earlier(sections.get("Earlier findings", ""), rel)
    stray = sorted(set(earlier) - set(open_ids), key=lambda f: int(f[1:]))
    if stray:
        raise Refused("%s: ## Earlier findings names %s, which is not an open finding of the brief" % (
            rel, ", ".join(stray)))
    missing = sorted(set(open_ids) - set(earlier), key=lambda f: int(f[1:]))
    if missing:
        raise Refused("%s: ## Earlier findings does not answer %s (`- f<m>: fixed` or `- f<m>: not fixed: <why>`)"
                      % (rel, ", ".join(missing)))
    return verdict, findings, earlier


def _finding_text(f):
    head = "### %s%s %s: %s\n- item: %s\n- where: %s" % (
        "%s " % f.fid if f.fid else "", f.grade, f.triage, f.title, f.item or "-", f.where or "-")
    return head + ("\n%s" % f.body if f.body else "")


def render(review):
    head = ["id: %s" % review.ident, "kind: review", "batch: %s" % review.batch,
            "pull_request: %s" % review.pull_request, "head: %s" % review.head, "range: %s" % review.range,
            "result: %s" % review.result]
    findings = "\n\n".join(_finding_text(f) for f in review.findings) or "None."
    text = "---\n%s\n---\n\n# %s review %d\n\n## Verdict\n\n%s\n\n## Findings\n\n%s\n" % (
        "\n".join(head), review.batch, review.number, review.verdict, findings)
    if review.earlier:
        text += "\n## Earlier findings\n%s\n" % "".join("- %s: %s\n" % e for e in review.earlier.items()).rstrip("\n")
    return text


def parse(text, rel):
    data, body = shop_files.frontmatter(text)
    ident = data.get("id")
    m = re.fullmatch(r"review/.+/(batch-[1-9]\d*)/review-([1-9]\d*)", ident or "") if isinstance(ident, str) else None
    if not m:
        raise Refused("%s: id %r is not review/<context path>/batch-<n>/review-<k>" % (rel, ident))
    if data.get("kind") != "review":
        raise Refused("%s: kind %r is not review" % (rel, data.get("kind")))
    if data.get("batch") != m.group(1):
        raise Refused("%s: batch %r is not %s" % (rel, data.get("batch"), m.group(1)))
    if data.get("result") not in RESULTS:
        raise Refused("%s: result %r is not one of %s" % (rel, data.get("result"), ", ".join(RESULTS)))
    for key in ("pull_request", "head", "range"):
        if not isinstance(data.get(key), str) or not data[key]:
            raise Refused("%s: %s is not given" % (rel, key))
    title = "# %s review %s" % (m.group(1), m.group(2))
    if body.split("\n", 1)[0].strip() != title:
        raise Refused("%s: title: the body does not start with %r" % (rel, title))
    sections = _sections(body, rel)
    return Review(number=int(m.group(2)), batch=m.group(1), ident=ident, pull_request=data["pull_request"],
                  head=data["head"], range=data["range"], result=data["result"],
                  verdict=sections.get("Verdict", "").strip(),
                  findings=_findings(sections.get("Findings", "None."), rel, numbered=True),
                  earlier=_earlier(sections.get("Earlier findings", ""), rel))


def reviews(root, batch):
    """The batch's recorded reviews, by number; a `review-*.md` not named `review-<k>.md` is refused."""
    folder = Path(root) / batch_plan.BATCHES / str(batch_plan.number(_name(batch)))
    found = []
    for path in folder.glob("review-*.md"):
        rel = path.relative_to(root).as_posix()
        if not re.fullmatch(r"review-[1-9]\d*\.md", path.name):
            raise Refused("%s: id: the file name is not review-<k>.md" % rel)
        found.append(parse(shop_files.read(path, root), rel))
    return sorted(found, key=lambda r: r.number)


def _still_in(root, item):
    try:
        return backlog_items.find(root, item).status == "in-batch"
    except Refused:
        return False


def open_findings(root, batch):
    """The `fix now` findings no later review said `fixed` of, whose item is still `in-batch` (D10, D22); none of a
    batch that is merged or abandoned (review M2)."""
    plan = Path(root) / batch_plan.rel_of(_name(batch))
    if plan.is_file() and batch_plan.find(root, _name(batch)).status not in batch_plan.OPEN:
        return []
    found = {}
    for review in reviews(root, batch):
        for fid, said in review.earlier.items():
            if said == "fixed":
                found.pop(fid, None)
        found.update({f.fid: f for f in review.findings if f.triage == "fix now"})
    return [f for f in found.values() if f.item and _still_in(root, f.item)]


def next_fid(root, batch):
    return max((int(f.fid[1:]) for r in reviews(root, batch) for f in r.findings), default=0) + 1
