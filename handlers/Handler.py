from ui.menubar.MenuBar import MenuBar
from ui.statusbar.StatusBar import StatusBar
from ui.workspace.Workspace import Workspace


class Handler:
    def __init__(self):
        self.menu = MenuBar.instance()
        self.statusbar = StatusBar.instance()
        self.main_window_workspace = Workspace.instance()
