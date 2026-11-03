"""`work run`'s formulate round, a script with no session (the GF conversion's design §13): for each capability an
approved capability-proposal names, `features generate`, then `features generate --check` and `model check` with no row
it did not give before, and the feature files committed. A guarantees capability has no feature and is passed over; a
capability whose file is not codified, a generation that fails or a new row is the round's fault, and nothing is
committed. The round still runs under the round lock, one at a time across initiatives (supervision r95). Standard
library only; a part of supervise.Run."""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import workqueue
from supervise_faults import Fault
from supervise_outputs import drafted, is_guarantees

SCRIPTS = Path(__file__).resolve().parent
REQUIREMENT = re.compile(r"^([a-z0-9]+(?:-[a-z0-9]+)*)#[rg]\d+")


def capabilities(lists):
    """The capabilities the ids of a proposal's `adds`, `changes` and `removes` name, in the order first named; a
    `term/<term>` id names none."""
    found = []
    for field in ("adds", "changes", "removes"):
        for one in lists.get(field) or []:
            m = REQUIREMENT.match(str(one))
            if m and m.group(1) not in found:
                found.append(m.group(1))
    return found


def parse_rows(text):
    """The rows `model check` prints, as (rule, row) pairs: the rows under each rule's heading, and each file problem
    or unresolved reference as a row of its own; the counts and the closing line left out."""
    found, rule = set(), None
    for line in text.splitlines():
        if not line.strip() or re.match(r"^\d+ violations", line):
            continue
        if line.startswith(" ") and rule:
            found.add((rule, line.strip()))
        elif line.startswith(("file:", "unresolved:", "warning ")):
            found.add((line.split(":", 1)[0].split()[0], line.strip()))
            rule = None
        else:
            rule = line.split()[0]
    return found


def rows(root):
    """The rows of `model check` on the checkout `root`; a run that fails is the round's fault."""
    done = run(root, "model", "--root", str(root), "check", "--limit", "100000")
    if done.returncode not in (0, 1):
        raise Fault("model check failed: %s" % (done.stderr.strip() or done.stdout.strip())[-2000:])
    return parse_rows(done.stdout)


def run(root, script, *args):
    return subprocess.run([sys.executable, str(SCRIPTS / script), *args], cwd=root, capture_output=True, text=True)


def git(root, *args):
    done = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
    if done.returncode != 0:
        raise Fault("git %s failed: %s" % (" ".join(args), (done.stderr.strip() or done.stdout.strip())))
    return done.stdout


def restore(root):
    """features/ as committed: what the round wrote taken back."""
    subprocess.run(["git", "checkout", "--", "features"], cwd=root, capture_output=True)
    subprocess.run(["git", "clean", "-fdq", "--", "features"], cwd=root, capture_output=True)


def script(root, name, caps):
    """The formulate round of the proposal `name` over the capabilities `caps` in the checkout `root`: its result."""
    root = Path(root)
    import spec_read
    service = [c for c in caps if not is_guarantees(root, c)]
    for cap in service:
        if not spec_read.codified(root / "spec" / "capabilities" / ("%s.md" % cap)):
            raise Fault("spec/capabilities/%s.md is not codified: run `migrate upgrade`" % cap)
    written = ["features/%s.feature" % c for c in service]
    if service:
        before = rows(root)
        try:
            for args in (service, ["--check", *service]):
                done = run(root, "features", "generate", "--root", str(root), *args)
                if done.returncode != 0:
                    raise Fault("features generate %s failed: %s" % (" ".join(args), (done.stderr.strip() or
                                                                                    done.stdout.strip())))
            new = sorted(rows(root) - before)
            if new:
                raise Fault("model check gives rows it did not give before generation: %s"
                            % "; ".join("%s %s" % pair for pair in new))
        except Fault:
            restore(root)
            raise
        git(root, "add", "--", *written)
    commit = None
    if service and git(root, "diff", "--cached", "--name-only", "--", *written).strip():
        git(root, "commit", "-q", "-m", "features: %s generated from %s" % (name, ", ".join(service)), "--", *written)
        commit = git(root, "rev-parse", "HEAD").strip()
    summary = ("generated %s" % ", ".join(written)) if service else "no service capability: no feature to generate"
    return {"status": "DONE", "summary": summary, "generated": written, "commit": commit, "questions": []}


class Formulate:
    """The part of supervise.Run that runs a formulate round: the script in the round's worktree, its result kept in the
    round's stage directory as a session's would be, with no session.json."""

    def formulate_script(self, name, tree, label):
        """(result, None) of the formulate round of the proposal `name` in `tree`; its faults are raised as Fault."""
        lists, _ = workqueue.frontmatter((self.dir / (name + ".md")).read_text())
        data = script(tree, name, capabilities(lists))
        _, kept = self.run_dir(name, "formulate")
        with self.lock:
            kept.mkdir(parents=True, exist_ok=True)
            (kept / "result.json").write_text(json.dumps(data, indent=2) + "\n")
            self.own.add(self.rel(kept))
        return data, None


def preview(root, drafts, cap, out):
    """The gate's preview (design §13): the feature `features generate` would write for capability `cap` with the
    drafts under `drafts` laid over `root`'s spec/, written to `out`/<cap>.feature. (its path, None), or (None, why
    there is none)."""
    import features_generate
    import features_vocab
    import spec_grammar
    import spec_read
    tmp = Path(tempfile.mkdtemp(prefix="preview-"))
    try:
        drafted(root, drafts, tmp)
        path = tmp / "spec" / "capabilities" / ("%s.md" % cap)
        if not spec_read.codified(path):
            return None, "spec/capabilities/%s.md is not codified" % cap
        if is_guarantees(tmp, cap):
            return None, "%s is a guarantees capability: it has no scenarios" % cap
        try:
            text = features_generate.generate(tmp, path)
        except (features_generate.GenerateError, features_vocab.StepError, spec_grammar.GrammarError) as why:
            return None, "it cannot be generated: %s" % why
        Path(out).mkdir(parents=True, exist_ok=True)
        shown = Path(out) / ("%s.feature" % cap)
        shown.write_text(text)
        return shown, None
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
