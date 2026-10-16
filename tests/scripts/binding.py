"""A scenario's step definition is the test whose docstring is its title
(decision/plugin-scenarios-run-as-unittest)."""

import re


def titles(feature_path):
    text = feature_path.read_text()
    return re.findall(r"^\s*Scenario(?: Outline)?:\s*(.+?)\s*$", text, re.M)


def missing(feature_path, *classes):
    docs = set()
    for cls in classes:
        for name in dir(cls):
            if name.startswith("test_"):
                docs.add((getattr(cls, name).__doc__ or "").strip())
    return [t for t in titles(feature_path) if t not in docs]
