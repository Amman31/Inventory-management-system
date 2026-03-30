from tkinter import Frame, Scrollbar, VERTICAL, HORIZONTAL, BOTH, END, X, Y, RIGHT, BOTTOM
from tkinter import ttk


def scrolled_treeview(parent, columns, headings, column_widths, relief="ridge", bd=3):
    # Frame
    frame = Frame(parent, bd=bd, relief=relief)
    # Vertical scrollbar
    scrolly = Scrollbar(frame, orient=VERTICAL)
    # Horizontal scrollbar
    scrollx = Scrollbar(frame, orient=HORIZONTAL)
    cols = tuple(columns)
    # Treeview
    tree = ttk.Treeview(
        frame,
        columns=cols,
        yscrollcommand=scrolly.set,
        xscrollcommand=scrollx.set,
    )
    # Horizontal scrollbar pack
    scrollx.pack(side=BOTTOM, fill=X)
    # Vertical scrollbar pack
    scrolly.pack(side=RIGHT, fill=Y)
    scrollx.config(command=tree.xview)
    scrolly.config(command=tree.yview)

    # For each column
    for col in cols:
        # Heading
        tree.heading(col, text=headings[col])
        # Column width
        tree.column(col, width=column_widths.get(col, 100))
    # Show headings
    tree["show"] = "headings"
    tree.pack(fill=BOTH, expand=1)
    return frame, tree

# Treeview replace rows
def treeview_replace_rows(tree, rows):
    tree.delete(*tree.get_children())    # Delete all rows
    for row in rows:
        tree.insert("", END, values=row)
