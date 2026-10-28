"""`work run`'s runs before a branch review (capability supervision, r154, r155): the whole suite, each work-item's
scenarios, each check a work-item names, `tools check`, `tools size`, `features deprecated` and `features bindings`, made
at the initiative branch's head in the review's worktree, and the text that gives them to the branch reviewer. Standard
library only; a part of supervise.Run."""
import shlex
import subprocess

import workqueue
from supervise_worker import SCRIPTS, with_scripts


def indented(text):
    """`text` with each line indented, so none of it begins a brief's line (`Head:` is read from the brief, r27, r50)."""
    return "".join("    %s\n" % line for line in text.splitlines())


class BranchRuns:
    """The part of supervise.Run that makes the runs a branch review starts from."""

    def branch_runs(self, tree):
        """Each run r154 names, made in `tree`: (title, command, exit code, output), in that order. The whole suite is
        the command a work-item's merge runs for it, so `.shop/delivery.toml`'s is the one used."""
        names = [name for name, _ in self.items()]
        commands = [("the whole suite", self.tests(names[0])["suite"])] if names else []
        commands += [("%s's scenarios" % name, self.tests(name)["work_item"]) for name in names]
        for name in names:
            check = workqueue.frontmatter((self.dir / (name + ".md")).read_text())[0].get("check")
            if isinstance(check, str) and check:
                commands.append(("%s's check" % name, shlex.split(check)))
        base = self.base()
        tools, features = ["python3", str(SCRIPTS / "tools")], ["python3", str(SCRIPTS / "features")]
        commands += [("tools check", tools + ["check"] + (["--base", base] if base else [])),
                     ("tools size", tools + ["size"]),
                     ("features deprecated", features + ["deprecated"]),
                     ("features bindings", features + ["bindings"])]
        return [self.branch_run(tree, title, command) for title, command in commands]

    def branch_run(self, tree, title, command):
        try:
            done = subprocess.run(command, cwd=tree, capture_output=True, text=True, env=with_scripts())
        except OSError as error:     # a command that cannot start is given as a run that did not
            return title, command, None, "could not be started: %s" % error
        return title, command, done.returncode, (done.stdout + done.stderr).strip()

    def runs_text(self, runs, head):
        """The brief's part about the runs: the commit they ran at, and each with its command, exit code and output."""
        text = "\n## Runs\n\nRan at: %s\n" % head
        for title, command, code, output in runs:
            text += "\n### %s\nCommand: %s\nExit code: %s\nOutput:\n%s" % (
                title, " ".join(shlex.quote(c) for c in command), "none" if code is None else code, indented(output))
        return text
