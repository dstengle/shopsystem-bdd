"""What `work run` gives a branch review to read (capability supervision, r156, r157): the commits from the initiative
branch's base to its head, each with its work-item or none, the change of that range less `.shop/`, and the files to
read. Standard library only; a part of supervise.Run."""
import json
import re

import workqueue
from supervise_branch_runs import indented
from supervise_worker import git

TRANSITION = re.compile(r"^(?:work(?: answer| withdraw| retry)?: (\S+) \S+ -> \S+|work add: [^/\s]+/(\S+) drafted)$")


class ReviewRead:
    """The part of supervise.Run that writes what a branch review is given to read."""

    def merged_commits(self):
        """{commit: work-item} of each `merged` line of log.jsonl: a merge is a fast-forward, so the commits it brought
        are the merge of the work-item's branch."""
        path = self.dir / "log.jsonl"
        found = {}
        for text in path.read_text().splitlines() if path.is_file() else []:
            try:
                line = json.loads(text)
            except ValueError:
                continue
            if line.get("event") == "merged":
                found.update({sha: line.get("work-item") for sha in line.get("commits", [])})
        return found

    def commits_text(self, base, head):
        """The commits from `base` to `head`, oldest first, each as `<commit> <work-item or none> <subject>`: the
        work-item whose merge brought it or whose transition it is, else none; and the change less `.shop/`."""
        merged = self.merged_commits()
        names = [name for name, _ in self.items()]
        text = "\n## Commits\n\n"
        if base is None:
            return text + "The initiative has no base.\n"
        for line in git(self.root, "log", "--reverse", "--format=%H %s", "%s..%s" % (base, head)).stdout.splitlines():
            sha, subject = line.split(" ", 1)
            found = TRANSITION.match(subject)
            name = found and (found.group(1) or found.group(2))
            owner = merged.get(sha) or (name if name in names else "none")
            text += "    %s %s %s\n" % (sha, owner, subject)
        change = git(self.root, "diff", base, head, "--", ".", ":(exclude).shop").stdout
        return text + "\n## Change\n\nThe change from %s to %s, without the workflow's own files:\n\n%s" % (base, head, indented(change))

    def read_text(self):
        """The `Read:` list: the capabilities the work-items are under, the design-decisions those rest on, and each
        work-item's plan, implementer's report and review findings from its stage directories."""
        names = [name for name, _ in self.items()]
        unders = []
        for name in names:
            under = workqueue.frontmatter((self.dir / (name + ".md")).read_text())[0].get("under")
            if isinstance(under, str) and under and under not in unders:
                unders.append(under)
        files = ["spec/capabilities/%s.md" % under for under in unders]
        for under in unders:
            path = self.root / "spec" / "capabilities" / (under + ".md")
            rests = workqueue.frontmatter(path.read_text())[0].get("rests_on") if path.is_file() else None
            files += [d for d in rests or [] if d not in files]
        for name in names:
            for stage in sorted(p for p in (self.dir / "runs" / name).glob("*") if p.is_dir()):
                files += [self.rel(stage / f) for f in ("plan.md", "report.md", "findings.md") if (stage / f).is_file()]
        return "\nRead:\n" + "".join("- %s\n" % f for f in files)
