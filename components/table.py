from tkinter import Frame, Scrollbar, VERTICAL, HORIZONTAL, BOTH, END, X, Y, RIGHT, BOTTOM
from tkinter import ttk


def scrolled_treeview(parent, columns, headings, column_widths, relief="ridge", bd=3):
    """
    Build a Frame containing a Treeview with linked scrollbars.

    columns: iterable of internal column names (must match headings keys).
    headings: dict mapping column name -> display heading text.
    column_widths: dict mapping column name -> width in pixels.
    """
    frame = Frame(parent, bd=bd, relief=relief)
    scrolly = Scrollbar(frame, orient=VERTICAL)
    scrollx = Scrollbar(frame, orient=HORIZONTAL)
    cols = tuple(columns)
    tree = ttk.Treeview(
        frame,
        columns=cols,
        yscrollcommand=scrolly.set,
        xscrollcommand=scrollx.set,
    )
    scrollx.pack(side=BOTTOM, fill=X)
    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.config(command=tree.xview)
    scrolly.config(command=tree.yview)

    for col in cols:
        tree.heading(col, text=headings[col])
        tree.column(col, width=column_widths.get(col, 100))
    tree["show"] = "headings"
    tree.pack(fill=BOTH, expand=1)
    return frame, tree


def treeview_replace_rows(tree, rows):
    """Clear and refill a Treeview from row tuples."""
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert("", END, values=row)
