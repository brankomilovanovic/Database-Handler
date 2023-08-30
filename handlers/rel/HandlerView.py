from PyQt5.QtWidgets import QWidget

from handlers.rel.RelDbLayoutManger import RelDbLayoutManger
from handlers.rel.Workspace.RelDbWorkspaceView import RelDbWorkspaceView


class HandlerView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = RelDbLayoutManger(self)

    def set_workspace(self, workspace: QWidget):
        self.layout.set_workspace(workspace)

    def add_zone(self, zone):
        self.layout.add_zone(zone)

    def is_in_zones(self, name):
        return self.layout.is_in_zones(name)

    def set_zone(self, name):
        self.layout.set_zone(name)

