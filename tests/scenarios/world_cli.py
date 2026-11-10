"""Shared handlers of the CLI pack's acts (grammar/packs/cli.md) in a codified-2 feature: "`tool` refuses `command`"
holds when the command the scenario ran exited with an error, as the pack defines refuse (U11's check of what it
changed runs after every generated scenario), and "`tool` names X" when what it printed says X: a code without its
backticks, a quoted text, or the text a capability's Givens bound an instance name to in the context's `named`.
`files_unchanged` is "`tool` does not change a <file>" where the file is one a Given wrote (the context's `files`)."""
from vocab import handler


def said(step):
    done = step.context.get("result")
    assert done is not None, "no command ran before: %s" % step.text
    return done.stdout + done.stderr


@handler("ThenDoes", "refuse")
def refuses(step):
    done = step.context.get("result")
    assert done is not None and done.returncode != 0, said(step)
    assert "Traceback" not in done.stderr, done.stderr


@handler("ThenDoes", "name")
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
