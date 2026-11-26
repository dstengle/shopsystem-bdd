"""Where the product layer is kept (b602; decision 0102): the product file `.shop/product/product.toml` of the shop,
written and committed only by `spec product`, `spec actor` and `spec job` (`kept`). Its form: `id` and `purpose`,
`actors = [...]`, and a table `[jobs."<id>"]` of each job with its `actors`, `statement` and `needs` (`render`,
`read`); a file that does not read refused naming it."""
import tomllib
from pathlib import Path

import shop_files
from product_layer import empty
from shop_refused import Refused
from toml_edit import literal

REL = ".shop/product/product.toml"
HEADER = "# The product this bounded context belongs to; written by `spec product`, `spec actor` and `spec job`.\n"


def render(product):
    """The product file's text of a product (a part it lacks left out)."""
    lines = [HEADER]
    for key in ("id", "purpose"):
        if product.get(key):
            lines.append("%s = %s\n" % (key, literal(product[key])))
    lines.append("actors = %s\n" % literal(product.get("actors", [])))
    for ident, job in product.get("jobs", {}).items():
        lines.append("\n[jobs.%s]\n" % literal(ident))
        lines += ["%s = %s\n" % (key, literal(job.get(key, [] if key != "statement" else ""))) for key in
                  ("actors", "statement", "needs")]
    return "".join(lines)


def read(root):
    """The product kept in `root`, or an empty one with no file."""
    path = Path(root) / REL
    if not path.is_file():
        return empty()
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as why:
        raise Refused("%s: %s" % (REL, why)) from None
    jobs = {ident: {"actors": list(job.get("actors", [])), "statement": job.get("statement", ""),
                    "needs": list(job.get("needs", []))} for ident, job in data.get("jobs", {}).items()}
    return {"id": data.get("id"), "purpose": data.get("purpose"), "actors": list(data.get("actors", [])),
            "jobs": jobs}


def kept(root, product, message):
    """The product written and committed; nothing when the file already holds it."""
    path, text = Path(root) / REL, render(product)
    if path.is_file() and path.read_text(encoding="utf-8") == text:
        return False
    shop_files.committed(root, [REL], message, lambda: (path.parent.mkdir(parents=True, exist_ok=True),
                                                        path.write_text(text, encoding="utf-8")))
    return True
