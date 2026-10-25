"""`work start`: the initiative an accepted request begins (work-queue r22). Committed on the current branch (r25)."""
import datetime
import re
from pathlib import Path

import workqueue
from workqueue import Refused


def _highest(root):
    """The highest <n> of any initiative under .shop/work/, by its directory's leading i<n> and its id's."""
    numbers = []
    for path in sorted((Path(root) / workqueue.WORK).glob("*/initiative.md")):
        data, _ = workqueue.frontmatter(workqueue.read(path, root))
        for word in (path.parent.name, str(data.get("id", "")).rsplit("/", 1)[-1]):
            found = re.match(r"i(\d+)(?:-|$)", word)
            if found:
                numbers.append(int(found.group(1)))
    return max(numbers, default=0)


def start(root, request):
    """Write .shop/work/i<n>/initiative.md, a proposed capability-change initiative that fulfils the accepted request
    `request` and takes its source; return i<n>."""
    workqueue.entry(request, "request")
    path = Path(root) / workqueue.WORK / "requests" / (request + ".md")
    if not path.is_file():
        raise Refused("there is no request %s under %s" % (request, workqueue.WORK / "requests"))
    text = workqueue.read(path, root)
    data, body = workqueue.frontmatter(text)
    if data.get("status") != "accepted":
        raise Refused("%s is %s, not accepted; work start begins an initiative only for an accepted request"
                      % (request, data.get("status")))
    source = data.get("source") or []
    title = re.search(r"(?m)^# (.*)$", body)
    name = "i%d" % (_highest(root) + 1)
    directory = Path(root) / workqueue.WORK / name
    text = ("---\nid: initiative/%s/%s\nkind: capability-change\nstatus: proposed\nfulfils: %s\nsource: [%s]\ndate: %s\n---\n\n# %s\n"
            % (workqueue.context_path(root), name, data.get("id"), ", ".join(source), datetime.date.today().isoformat(),
               title.group(1) if title else request))

    def write():
        directory.mkdir(parents=True)
        (directory / "initiative.md").write_text(text)

    try:
        workqueue.committed(root, [str(workqueue.WORK / name / "initiative.md")],
                            "work: start %s, fulfilling %s" % (name, request), write)
    except Refused:
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()
        raise
    return name
