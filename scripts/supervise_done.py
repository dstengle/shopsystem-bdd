"""`work run`'s done for an initiative (capability supervision r105, r109): once the kept branch review lists nothing to fix
now, an initiative whose work-items are green or withdrawn, whose requests are delivered and whose measurement and analysis
record are committed is set `done`, and that is committed on the initiative branch. Standard library only; a part of
supervise.Run."""
import re

import supervise_glossary
import workqueue
import workqueue_done
from supervise_worker import git

RECORDS = ".shop/records"


class Dones:
    """The part of supervise.Run that sets a finished initiative done."""

    def records_committed(self):
        """Whether the initiative's measurement and its analysis record are tracked and unmodified (read from git, r105)."""
        tracked = git(self.root, "ls-files", "--", RECORDS).stdout.split()
        wanted = (r"%s/measurements/[^/]*-%s\.md" % (RECORDS, re.escape(self.initiative)),
                  r"%s/[^/]*-%s-analysis\.md" % (RECORDS, re.escape(self.initiative)))
        found = [p for pattern in wanted for p in tracked if re.fullmatch(pattern, p)]
        if len(found) < len(wanted):
            return False
        return not git(self.root, "status", "--porcelain", "--", *found).stdout.strip()

    def set_glossary_done(self):
        """The done of an initiative that changes only the glossary (r161), with no branch review, measurement or analysis."""
        data, _ = workqueue.frontmatter((self.dir / "initiative.md").read_text())
        before = data.get("status")
        if before == "done" or not supervise_glossary.glossary_only_done(self.root, self.dir):
            return
        with self.lock:
            workqueue_done.mark(self.dir, self.root)
            self.log(**{"work-item": self.initiative, "before": before, "after": "done", "by": "work run"})
            self.commit(self.initiative, before, "done")

    def set_done(self):
        """The initiative's own transition to done (r105), logged and committed on the initiative branch (r109)."""
        data, _ = workqueue.frontmatter((self.dir / "initiative.md").read_text())
        before = data.get("status")
        if before == "done" or not self.records_committed() or not workqueue_done.holds(self.root, self.dir, data.get("id")):
            return
        with self.lock:
            workqueue_done.mark(self.dir, self.root)
            self.log(**{"work-item": self.initiative, "before": before, "after": "done", "by": "work run"})
            self.commit(self.initiative, before, "done")
