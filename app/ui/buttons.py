from tkinter import Button, Label

from app.ui.theme import Theme


def search_button(parent, command, x, y, width=150, height=30):
    btn = Button(
        parent,
        text="Search",
        command=command,
        font=Theme.FONT_GOUDY,
        bg=Theme.BTN_SEARCH,
        fg="white",
        cursor="hand2",
    )
    btn.place(x=x, y=y, width=width, height=height)
    return btn

def dashboard_menu_button(parent, text, font=None, bg="#4d636d", fg="white"):
    lbl = Label(parent, text=text, font=font or ("times new roman", 12), bg=bg, fg=fg)
    lbl.pack(side="bottom", fill="x")
    return lbl

def crud_action_buttons(parent, commands, positions):
    """
    Place Save / Update / Delete / Clear with shared styling.

    commands: dict with keys save, update, delete, clear (callables).
    positions: list of (x, y, width, height) for each button in that order.
    """
    labels = ("Save", "Update", "Delete", "Clear")
    keys = ("save", "update", "delete", "clear")
    colors = (Theme.BTN_SAVE, Theme.BTN_UPDATE, Theme.BTN_DELETE, Theme.BTN_CLEAR)
    buttons = []
    for label, key, color, pos in zip(labels, keys, colors, positions):
        x, y, w, h = pos
        btn = Button(
            parent,
            text=label,
            command=commands[key],
            font=Theme.FONT_GOUDY,
            bg=color,
            fg="white",
            cursor="hand2",
        )
        btn.place(x=x, y=y, width=w, height=h)
        buttons.append(btn)
    return buttons


def primary_title_bar(parent, text, x, y, width, height=None, font=None):
    """Single-line header strip used across CRUD screens."""
    kw = {
        "text": text,
        "font": font or Theme.FONT_GOUDY,
        "bg": Theme.BG_TITLE_BLUE,
        "fg": "white",
    }
    lbl = Label(parent, **kw)
    if height is not None:
        lbl.place(x=x, y=y, width=width, height=height)
    else:
        lbl.place(x=x, y=y, width=width)
    return lbl


def pack_footer_label(parent, text, font=None, bg="#4d636d", fg="white"):
    lbl = Label(parent, text=text, font=font or ("times new roman", 12), bg=bg, fg=fg)
    lbl.pack(side="bottom", fill="x")
    return lbl