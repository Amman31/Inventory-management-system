def configure_crud_window(root, geometry="1100x500+320+220"):
    root.geometry(geometry)
    root.config(bg="white")
    root.resizable(False, False)
    root.focus_force()
