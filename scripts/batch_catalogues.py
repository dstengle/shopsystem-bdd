"""The catalogues `work batch start` writes again on the batch's branch (batches r48, r49; b333): the rule catalogue
`grammar/rules.md` and the construct catalogue `grammar/constructs.md`, each as `model rules --write` and `model
constructs --write` write it, when the bounded context keeps it or a line the batch lays cites one of its codes;
their entries list the lines citing each code, so the lines a batch lays change them. A catalogue that cannot be
written (an example that does not do what it says, an uncovered function a grammar item brings) is left as it is and
its problems given back, for the batch brief to name and that item's task to mend, never refusing the start."""
from pathlib import Path


def _cited(citing, laid):
    """Whether a line of `laid` (`<cap>#r<n>` ids) cites a code, by the catalogue's `citing`."""
    return any(set(ids) & set(laid) for ids in citing.values())


def _rules(tree, laid):
    import model_rules
    path = Path(tree) / model_rules.CATALOGUE
    if not path.is_file() and not _cited(model_rules.citing(tree), laid):
        return path, None, []
    entries = model_rules.rules()
    problems = model_rules.wrong(entries)
    return path, None if problems else model_rules.render(tree, entries), problems


def _constructs(tree, laid):
    import model_constructs
    path = Path(tree) / model_constructs.CATALOGUE
    if not path.is_file() and not _cited(model_constructs.citing(tree), laid):
        return path, None, []
    done, problems = model_constructs.entries(model_constructs.Grammar())
    return path, None if problems else model_constructs.render(tree, done), problems


def write(tree, laid):
    """Of the lines `laid` (`<cap>#r<n>` ids): (the paths changed, the problems of each catalogue that could not be
    written, each `<path>: <problem>`)."""
    changed, problems = [], []
    for made in (_rules, _constructs):
        path, text, found = made(tree, laid)
        rel = path.relative_to(tree).as_posix()
        problems += ["%s: %s" % (rel, p) for p in found]
        if text is not None and (not path.is_file() or path.read_text() != text):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
            changed.append(rel)
    return changed, problems
