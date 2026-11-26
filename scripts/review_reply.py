"""The reply of `pr-reviewer` read from its dispatch's transcript (b697, review-guarantees r13): the relay of a
dispatch's reply to the session that dispatched it escapes `<`, `>` and `&`, so a findings file that session saves is
not the reply as given; the transcript holds it as given. Its reply is the text of its last assistant row that holds
text (`reply`); the transcript is the one `--reply` names, else the newest pr-reviewer dispatch of the session's store
(Claude Code's project directory of the root, measure_batch_read's) whose prompt names the review's brief (`found`)."""
import json

from measure_batch_read import project_dir
from shop_files import Refused
from transcripts import json_rows

AGENT = "pr-reviewer"


def _text(content):
    """The text of a message's content: a string, or its text blocks joined."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text")
    return ""


def _message(row):
    return row.get("message") if isinstance(row.get("message"), dict) else row


def reply(path, command):
    """The text of the last assistant row of the transcript `path` that holds text; refused, naming the file, when
    it has none or does not read."""
    try:
        rows = json_rows(path)
    except (OSError, Refused) as failed:
        raise Refused("%s: the transcript %s does not read: %s" % (command, path, failed)) from None
    texts = [t for t in (_text(_message(r).get("content")) for r in rows if r.get("type") == "assistant") if t.strip()]
    if not texts:
        raise Refused("%s: the transcript %s holds no reply" % (command, path))
    return texts[-1]


def _prompt(path):
    """The text of the transcript's first user row, '' when it has none or does not read."""
    try:
        rows = json_rows(path)
    except (OSError, Refused):
        return ""
    return next((_text(_message(r).get("content")) for r in rows if r.get("type") == "user"), "")


def _pr_reviewer(meta):
    try:
        kind = json.loads(meta.read_text(encoding="utf-8")).get("agentType")
    except (OSError, ValueError, AttributeError):
        return False
    return isinstance(kind, str) and kind.split(":")[-1] == AGENT


def found(root, brief):
    """The newest transcript of a pr-reviewer dispatch in the session's store whose prompt names `brief`, else None."""
    names = {str(brief), str(brief.resolve())}
    where = project_dir(root)
    if not where.is_dir():
        return None
    hits = []
    for meta in where.rglob("agent-*.meta.json"):
        path = meta.with_name(meta.name[:-len(".meta.json")] + ".jsonl")
        if path.is_file() and _pr_reviewer(meta) and any(n in _prompt(path) for n in names):
            hits.append((path.stat().st_mtime, str(path), path))
    return max(hits)[2] if hits else None
