# Configure CRUD window
def configure_crud_window(root, geometry="1100x500+320+220"):
    root.geometry(geometry)    # Set geometry
    root.config(bg="white")
    root.resizable(False, False)    # Set resizable
    root.focus_force()
