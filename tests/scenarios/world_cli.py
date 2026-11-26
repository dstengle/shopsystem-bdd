"""Handlers of the CLI pack's acts (grammar/packs/cli.md) in analysis-tools' feature, which analysis_tools_handlers_thens
adds to world_four's chain of it: "`tool` refuses `command`" holds when the command the scenario ran exited with an error, as the pack defines refuse (U11's check of what it
changed runs after every generated scenario), and "`tool` names X" when what it printed says X: a code without its
backticks, a quoted text, or the text a capability's Givens bound an instance name to in the context's `named`.
`files_unchanged` is "`tool` does not change a <file>" where the file is one a Given wrote (the context's `files`).
A usage error, argparse's `usage:` on stderr with exit 2, is no refusal (b686); exit 2 alone is one."""
import re


def said(step):
    done = step.context.get("result")
    assert done is not None, "no command ran before: %s" % step.text
    return done.stdout + done.stderr


def usage_error(done):
    """Whether a run's result is argparse's usage error: exit 2 with its `usage:` text on stderr."""
    return done.returncode == 2 and re.search(r"^usage: ", done.stderr, re.MULTILINE) is not None


def refuses(step):
    done = step.context.get("result")
    assert done is not None and done.returncode != 0, said(step)
    assert "Traceback" not in done.stderr, done.stderr
    assert not usage_error(done), ("a usage error, no refusal", done.stderr)


def names(step):
    bound = step.context.get("named", {})
    for np in step.nps:
        last = np.split()[-1]
        want = bound[last] if last in bound and not np.startswith(("`", '"')) else (
            np if np.startswith(("`", '"')) else last).strip("`").strip('"')
        assert want in said(step), (np, want, said(step))


def files_unchanged(step):
    """Every file a Given wrote into the scenario's repository (the context's `files`, path to text) is as written."""
    for path, text in step.context.get("files", {}).items():
        assert (step.repo / path).read_text() == text, path
