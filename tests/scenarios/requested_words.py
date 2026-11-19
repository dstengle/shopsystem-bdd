"""The words of a request's step as the CLI's handlers read them (requested.legacy, the domain contract design §9.4):
the kinds and states a capability's handlers know by their words before the reword (`renamed`, `reverbed`), a
request's thing named by what it belongs to (`owner`), a Then's text in the CLI's spelling ("`work` writes the item
i1" for "the backlog service keeps the item i1", `retext`) and a When's ("the person runs `model parse` on the
fragment f1", `runs_text`)."""
import re

# the words a capability's handlers know a kind by, before the domain contract renamed it
RENAMES = {"requests": {"context request": "request", "entry": "comment", "field": "entry"},
           "intake": {"context request": "request", "entry": "comment", "line reason": "reason"},
           "batches": {"proposed change": "pull request", "kept change": "commit", "workspace": "worktree",
                       "context request": "request", "entry": "comment"},
           "telemetry": {"proposed change": "pull request"},
           "migration-tools": {"this plugin": "`migrate`"},
           "backlog": {"shared workspace": "upstream branch", "workspace name": "branch name",
                       "workspace": "git branch"}}
# the verbs a capability's handlers know a state by, before the reword: (new term, old term, old third person)
VERB_RENAMES = {"batches": [("break", "fail", "fails"), ("succeed", "pass", "passes"), ("meet", "pass", "passes")],
                "backlog": [("meet", "pass", "passes")], "readiness": [("meet", "pass", "passes")]}


def renamed(call, cap):
    """The kinds the handlers of the capability the scenario moved from know by an older word, said so."""
    table = RENAMES.get(cap, {})
    def say(text):
        for new, old in table.items():
            if new.startswith("this "):     # a phrase said whole
                text = text.replace(new, old) if text else text
                continue
            text = re.sub(r"\b(the|a|an|no|every|this|each|that) %s(s?)\b" % new, r"\1 %s\2" % old,
                          text) if text else text
        return text
    call.text, call.subject = say(call.text), say(call.subject)
    call.nps = [say(np) for np in call.nps]
    call.kind = table.get(call.kind, call.kind)
    if call.template.startswith("Given") or call.template.endswith("K_A"):
        call.term = table.get(call.term, call.term)
    if call.template in ("GivenDoes", "GivenDoesNot") and call.term == "holds" and call.nps == ["this repository"]:
        call.term = call.event = "check out"        # a workspace that holds this repository is checked out there
        call.subject, call.nps = "this repository", [call.subject]
        call.text = "this repository checks out %s" % call.nps[0]


def reverbed(call, cap):
    for new, old, said in VERB_RENAMES.get(cap, []):
        if new == "meet" and call.nps != ["this readiness bar"]:   # a bar check is still met
            continue
        if call.template in ("GivenDoes", "GivenDoesNot", "ThenDoes", "ThenDoesNot") and call.term == new:
            call.term = call.event = old
            call.text = re.sub(r"\b%ss\b" % new, said, call.text, count=1)
            call.text = re.sub(r"\b%s\b" % new, old, call.text, count=1)


def owner(call, texts, kind):
    """A request's thing named as what a `kind` has ("the context request c1 has the turn t1"): the `kind` it is
    of, as the CLI's handlers name a request's thing by its request."""
    out = []
    for name in call.names:
        found = [m for t in texts for m in re.findall(r"^the %s (\w+) (?:has|holds) the [a-z ]+ %s$" % (kind, name), t)]
        out.append(found[0] if found else name)
    call.names = out


S3 = {"refuse": "refuses", "return": "returns", "complete": "completes", "fail": "fails", "notify": "notifies",
      "keep": "keeps", "change": "changes", "print": "prints"}
WORDS = {"ThenRefuses": "refuses this request", "ThenCompletes": "completes the request",
         "ThenFails": "fails this check"}
SAID = {"ThenCompletes": "exits successfully", "ThenFails": "exits with an error"}


def retext(text, program, template, verb, chosen):
    """The step's text as the CLI's handlers read it: "`work` writes the item i1" for "the backlog service keeps the
    item i1"; "`work` refuses `work decision`" for "... refuses this request"."""
    if program:
        text = re.sub(r"^the [a-z ]+ service ", program + " ", text)
    if template == "ThenNotifies":     # the party told is the hook's session, not what the output shows
        text = re.sub(r" notifies (the|this) [a-z ]+? [a-z]*\d* ?of ", " notifies ", text, count=1)
    if template in WORDS:
        return text.replace(WORDS[template], SAID.get(template) or "refuses %s" % chosen)
    if verb is None:
        return text
    for new in ("keeps", "returns", "notifies", "changes"):
        text = re.sub(r"^(\S+) %s " % new, r"\1 %s " % S3.get(verb, verb + "s"), text)
    for new in ("keep", "return", "notify", "change"):
        text = re.sub(r"^(\S+) does not %s " % new, r"\1 does not %s " % verb, text)
    return text


def runs_text(call, chosen):
    """The When as the CLI's handlers read it: "the person runs `model parse` on the fragment f1"."""
    subject = call.subject or "the person"
    things = [m.group(0) for m in re.finditer(r"\bthe (?:[a-z-]+ ){0,2}?[a-z-]+ [a-z]+\d+\b", call.text)
              if not subject.endswith(m.group(0))]
    return "%s runs %s%s" % (subject, chosen, " on " + " and ".join(things) if things else "")
