"""What `work line` prints of a requirement it reworded and of the terms it wrote or reworded (b829, drafting r103,
r105-r107), as it prints the requirement it adds with its id (backlog_lines' `added`, drafting r98): the item's label,
then what it did and what it wrote, so the person sees the text the item now holds."""
from backlog_items import label, one_line


def reworded(item, ident, text, changed=True):
    """`<label>: <cap>#r<n> reworded: <line>`, or of a reword to the text the item holds already
    `<label>: <cap>#r<n> unchanged: <line>`."""
    return "%s: %s %s: %s" % (label(item), ident, "reworded" if changed else "unchanged", text.strip())


def terms(item, said, bullets):
    """What `--term` wrote (`said`, "a vocabulary entry of notes"), then each term on a line of its own."""
    written = [one_line(b, "term") for b in bullets or ()]
    head = "%s: %s" % (label(item), said)
    if len(written) == 1:
        return "%s: %s" % (head, written[0])
    return "\n".join([head + (":" if written else "")] + ["  %s" % b for b in written])


def term_reworded(item, term, entry, changed=True):
    """`<label>: term <t> reworded: <entry>`, or of a reword to the entry the item holds already
    `<label>: term <t> unchanged: <entry>`."""
    return "%s: term %s %s: %s" % (label(item), term, "reworded" if changed else "unchanged", entry.strip())
