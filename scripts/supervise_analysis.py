"""`work run`'s measure of a finished initiative and the analysis that follows it (capability supervision): once the kept
branch review lists nothing to fix now, `measure initiative` is run, and a `batch-analyst` session, which loads
analyzing-a-batch, writes the analysis record. Standard library only; a part of supervise.Run."""
import json
import shutil
import subprocess
import sys
import uuid

from supervise_worker import SCRIPTS

AGENT = "batch-analyst"
STAGE = "analysis"


class Analyses:
    """The part of supervise.Run that measures an initiative whose work is done and has it analysed."""

    def lists_nothing(self, kept):
        """Whether the kept review's result file is readable and its `questions`, the list r74 reads, is empty."""
        try:
            data = json.loads((kept / "result.json").read_text())
        except (OSError, ValueError):
            return False
        return isinstance(data, dict) and not data.get("questions")

    def analyse(self):
        """Run `measure initiative` from the repository root; when it writes the measurement, start the analysis session
        and keep its record in the main checkout. A refusal or a failed session is told on stderr, and is no fault."""
        done = subprocess.run([sys.executable, str(SCRIPTS / "measure"), "initiative", self.initiative],
                              cwd=self.root, capture_output=True, text=True)
        if done.returncode != 0:
            print("work run: `measure initiative %s` was refused, so there is no analysis: %s"
                  % (self.initiative, (done.stderr.strip() or done.stdout.strip())), file=sys.stderr)
            return
        measurement = self.root / done.stdout.strip().splitlines()[-1]
        tree = self.worktree(None, STAGE)
        try:
            here = tree / ".shop" / "scratch" / STAGE
            here.mkdir(parents=True)
            brief = here / "brief.md"
            brief.write_text(
                "# analysis of %s\n\nInitiative: %s\nAgent: %s\nScripts: %s\nMeasurement: %s\n"
                "Measurements: %s\nWorktree: %s\nRun directory: %s\nResult file: %s\n\n"
                "`work run` has written the measurement: read it with `measure show`, and do not run `measure "
                "initiative`. Write the analysis record as `analysis.md` in your run directory, and commit nothing. "
                "You start in your worktree: run every command from there and never change directory. Write the "
                "result file first, with the outcome `PARTIAL`, and keep it current as you work: JSON with `status`, "
                "`summary` and `questions`.\n"
                % (self.initiative, self.rel(self.dir), AGENT, SCRIPTS, measurement, measurement.parent, tree, here,
                   here / "result.json"))
            self.session(STAGE, AGENT, brief, str(uuid.uuid4()), tree, None)
            if (here / "analysis.md").is_file():
                record = self.root / ".shop" / "records" / ("%s-%s-analysis.md" % (measurement.name[:10], self.initiative))
                shutil.copy2(here / "analysis.md", record)
            else:
                print("work run: the analysis session of %s wrote no analysis record" % self.initiative, file=sys.stderr)
        finally:
            self.remove(tree)
