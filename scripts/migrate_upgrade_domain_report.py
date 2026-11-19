"""What the upgrade step "the domain contract" leaves for a session to reword (the domain contract design, §9.6),
read off the old lexicon, the lines (file, id, text) and the scaffold (migrate_upgrade_domain_scaffold), by file and
id: each line that runs a command, with the operation and the parameters the scaffold gave it; each line that says
print, exit or `--json` (a response is the envelope's outcome and content now); each `Kind of: tool` entry (now a
service); each verb and adjective the scaffold names no element of; each line naming git's or GitHub's acts (their
words are the store's and the issue host's adapters'); each relation row between kinds that are no objects; and the
programs `spec/adapters/cli.toml` must name. Until a line is reworded, `spec check` refuses it (v_m1, v_p) and
refuses `imports: [cli]` (v_t21)."""
import re

NAME = "the domain contract"
SAYS = (("print", r"\bprints?\b"), ("exit", r"\bexits?\b"), ("--json", r"`--json`"))
MECHANISMS = r"\b(commits?|push(?:es)?|branch(?:es)?|pull requests?|issues?|worktrees?|remotes?)\b"


def _note(what):
    return "%s: %s" % (NAME, what)


def requests(built):
    return [_note("%s %s requests %s.%s(%s) through `%s`: reword it in the request's words, \"When the person <verb>s "
                  "... with the <parameter> ...\", and its response in the service's (\"the %s service shall ...\")"
                  % (rel, ident, svc, op, ", ".join(params), code, svc))
            for rel, ident, svc, op, params, code in built.requests]


def responses(said):
    out = []
    for rel, ident, text in said:
        words = [w for w, pattern in SAYS if re.search(pattern, text)]
        if words:
            out.append(_note("%s %s says %s: a response is the outcome and the content of the service's response "
                             "now (return, complete, refuse and name, keep)" % (rel, ident, " and ".join(words))))
    return out


def tools(lexicon, built):
    return [_note("%s, %s: Kind of: tool: the tool is the service %s now, said \"the %s service\"; its program is "
                  "the CLI adapter's" % (t.term, t.where, built.tools[t.term], built.tools[t.term]))
            for t in lexicon.of("actor") if t.term in built.tools]


def unmapped(built):
    out = []
    for t in built.unmapped():
        if t.category == "condition":
            out.append(_note("%s, %s: an adjective that names no element of the model: make it a value of an "
                             "attribute and name it (→ value <object>.<attribute> <value>)" % (t.term, t.where)))
        elif t.frame.split()[:1] and t.frame.split()[0] in ("tool", *built.tools):
            out.append(_note("%s, %s: a tool's act: name an operation of a service (→ operation <service>.<name>) "
                             "or say it in the request pack's words (keep, return, complete)" % (t.term, t.where)))
        else:
            out.append(_note("%s, %s: a verb that names no operation or relation of the model: name one (→ operation "
                             "<service>.<name>, → relation <object>.<phrase>)" % (t.term, t.where)))
    return out


def mechanisms(said):
    out = []
    for rel, ident, text in said:
        found = sorted({m.lower() for m in re.findall(MECHANISMS, text, re.IGNORECASE)})
        if found:
            out.append(_note("%s %s names %s: git's and GitHub's acts are the store's and the issue host's adapters'; "
                             "say what happens between the parties (keep, share, send) and record the mechanism as "
                             "a design-decision" % (rel, ident, ", ".join(found))))
    return out


def rows(built):
    return [_note("%s the row %s | %s | %s names a kind that is no object of the model: declare it, or drop the row"
                  % (r.where, r.k1, r.word, r.k2)) for r in built.skipped]


def programs(built):
    names = sorted(built.tools.values())
    return [_note("spec/adapters/cli.toml: name the program of each tool under [programs]: %s" % ", ".join(names))] \
        if names else []


def notes(lexicon, said, built):
    return (requests(built) + responses(said) + tools(lexicon, built) + unmapped(built) + mechanisms(said)
            + rows(built) + programs(built)
            + [_note("until each line above is reworded, `spec check` refuses it (v_p, v_m1): the CLI pack's words "
                     "(run, option, print, exit) are no longer read")])
