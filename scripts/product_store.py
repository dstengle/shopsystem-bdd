"""Where the product layer is kept (b602; decision 0102): the product file `.shop/product/product.toml` of the shop,
written and committed only by `spec product`, `spec actor`, `spec job`, `spec subdomain` and `spec context` (`kept`).
Its form: `id` and `purpose`, `actors = [...]`, a table `[jobs."<id>"]` of each job with its `actors`, `statement`
and `needs`, and the domain map (b642): a table `[subdomains."<id>"]` of each subdomain with its `type` and `serves`,
and `[contexts."<id>"]` of each bounded context with its `addresses` and `shop`, none for a provider (`render`,
`read`); a product detail, any other key or table of the file, kept whole by `read` and written back by `render` after
the parts of the form (b673, product r8-r10); a file that does not read refused naming it, and one whose parts are not
of their types (its jobs no table of jobs, its actors no list of texts) refused as product not in the product form,
naming it (r11-r13)."""
import datetime
import tomllib
from pathlib import Path

import shop_files
from product_layer import empty
from shop_refused import Refused
from toml_edit import literal, name

REL = ".shop/product/product.toml"
HEADER = ("# The product this bounded context belongs to; written by `spec product`, `actor`, `job`, `subdomain` and "
          "`context`.\n")
FORM = ("id", "purpose", "actors", "jobs", "subdomains", "contexts")
# each table of tables of the form: its fields in order, and those that are lists of texts
TABLES = {"jobs": (("actors", "statement", "needs"), ("actors", "needs")),
          "subdomains": (("type", "serves"), ("serves",)), "contexts": (("addresses", "shop"), ("addresses",))}


def _literal(value):
    """A value as a TOML literal, a date or a time among them."""
    if isinstance(value, (datetime.date, datetime.time)):
        return value.isoformat()
    if isinstance(value, list):
        return "[%s]" % ", ".join(_literal(v) for v in value)
    if isinstance(value, dict):
        return "{ %s }" % ", ".join("%s = %s" % (name((k,)), _literal(v)) for k, v in value.items())
    return literal(value)


def _table(path, data, known=()):
    """The lines of the table `path`: its known keys, then its other values, then each table under it."""
    keys = list(known) + [k for k in data if k not in known]
    lines = ["%s = %s\n" % (name((k,)), _literal(data[k])) for k in keys if not isinstance(data.get(k), dict)]
    for key in [k for k in keys if isinstance(data.get(k), dict)]:
        lines += ["\n[%s]\n" % name(path + (key,))] + _table(path + (key,), data[key])
    return lines


def render(product):
    """The product file's text of a product (an id or a purpose it lacks left out), every other key of it, a product
    detail, written back after the parts of the product form it sits beside."""
    rest = {k: v for k, v in product.items() if k not in FORM}
    head = {k: product.get(k) for k in ("id", "purpose") if product.get(k)}
    head["actors"] = product.get("actors", [])
    lines = [HEADER] + _table((), {**head, **{k: v for k, v in rest.items() if not isinstance(v, dict)}})
    for ident, job in product.get("jobs", {}).items():
        job = {"actors": [], "statement": "", "needs": [], **job}
        lines += ["\n[jobs.%s]\n" % literal(ident)] + _table(("jobs", ident), job, ("actors", "statement", "needs"))
    for part in ("subdomains", "contexts"):
        for ident, entry in product.get(part, {}).items():
            lines += ["\n[%s.%s]\n" % (part, literal(ident))] + _table((part, ident), entry,
                                                                            [f for f in TABLES[part][0] if f in entry])
    return "".join(lines + _table((), {k: v for k, v in rest.items() if isinstance(v, dict)}))


def _formed(data):
    """Why the parsed file is not of the product form, or None."""
    for key in ("id", "purpose"):
        if not isinstance(data.get(key, ""), str):
            return "its %s is no text" % key
    if not _texts(data.get("actors", [])):
        return "its actors are no list of texts"
    for part, (fields, lists) in TABLES.items():
        if not isinstance(data.get(part, {}), dict):
            return "its %s are no table of %s" % (part, part)
        for ident, entry in data.get(part, {}).items():
            if not isinstance(entry, dict):
                return "its %s %s is no table" % (part, ident)
            if not all(_texts(entry.get(f, [])) if f in lists else isinstance(entry.get(f, ""), str) for f in fields):
                return "its %s %s's %s are not of their types" % (part, ident, ", ".join(fields))
    return None


def _texts(value):
    return isinstance(value, list) and all(isinstance(v, str) for v in value)


def read(root):
    """The product kept in `root`, every key of its file kept, or an empty one with no file; a file not of the product
    form refused naming it."""
    path = Path(root) / REL
    if not path.is_file():
        return empty()
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as why:
        raise Refused("%s: %s" % (REL, why)) from None
    why = _formed(data)
    if why:
        raise Refused("{names} is not of the product form (%s)" % why, reason="product not in the product form",
                      names=["file:%s" % REL])
    jobs = {ident: {"actors": [], "statement": "", "needs": [], **job} for ident, job in data.get("jobs", {}).items()}
    return {**data, "id": data.get("id"), "purpose": data.get("purpose"), "actors": list(data.get("actors", [])),
            "jobs": jobs}


def kept(root, product, message):
    """The product written and committed; nothing when the file already holds it."""
    path, text = Path(root) / REL, render(product)
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return False
    shop_files.committed(root, [REL], message, lambda: (path.parent.mkdir(parents=True, exist_ok=True),
                                                        path.write_text(text, encoding="utf-8")))
    return True
