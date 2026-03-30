from tkinter import LabelFrame, RIDGE, ttk, Entry

from components.theme import Theme
from components.buttons import search_button

# Search label frame
def search_label_frame(
    parent,
    title,
    variable,
    values,
    text_variable,
    search_command,
    x,
    y,
    width,
    height,
    combo_width=180,
    entry_x=200,
    entry_y=10,
    btn_x=410,
    btn_y=9,
    btn_w=150,
    btn_h=30,
):
    # Search frame
    frame = LabelFrame(
        parent,
        text=title,
        font=Theme.FONT_GOUDY_SMALL_BOLD,
        bd=2,
        relief=RIDGE,
        bg=Theme.BG_WHITE,
    )
    frame.place(x=x, y=y, width=width, height=height)

    # Search combobox
    cmb = ttk.Combobox(
        frame,
        textvariable=variable,
        values=values,
        state="readonly",
        justify="center",
        font=Theme.FONT_GOUDY,
    )
    cmb.place(x=10, y=10, width=combo_width)

    # Search entry
    Entry(frame, textvariable=text_variable, font=Theme.FONT_GOUDY, bg=Theme.BG_ENTRY).place(
        x=entry_x, y=entry_y
    )
    # Search button
    search_button(parent=frame, command=search_command, x=btn_x, y=btn_y, width=btn_w, height=btn_h)
    return frame, cmb
