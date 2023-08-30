from PyQt5 import Qt, QtCore
from PyQt5.QtWidgets import QLayout, QVBoxLayout, QWidget, QTabWidget, QHBoxLayout

from handlers.rel.Workspace.RelDbWorkspaceView import RelDbWorkspaceView
from handlers.rel.mysql.Zone.ZoneHandler import ZoneHandler


class RelDbLayoutManger(QHBoxLayout):
    def __init__(self, parent):
        super().__init__(parent)
        self.zones = {}
        self.tabbed = QTabWidget(parent)
        self._set_up_tabs()

    # def __new__(cls, parent=None) -> QLayout:
    #     # Ovde bi se mogao npr. konkretan tip layouta izvuci iz konfiguracije i kao takav vratiti.
    #     return QVBoxLayout(parent)

    def set_workspace(self, workspace: QWidget):
        self.insertWidget(0, workspace)

    def is_in_zones(self, name):
        return name in self.zones

    def set_zone(self, name):
        self.tabbed.setCurrentWidget(self.zones[name].get_view())

    def add_zone(self, zone: ZoneHandler):
        if not self.is_in_zones(zone.name()):
            self.zones[zone.name()] = zone
            self.tabbed.addTab(zone.get_view(), zone.name())
        self.set_zone(zone.name())

    def _set_up_tabs(self):
        self._add_tabs_widget()
        self.tabbed.setTabsClosable(True)
        # self.tabbed.setMovable(True)
        self.tabbed.setContentsMargins(0, 0, 0, 0)
        self.tabbed.setStyleSheet("border:none;")

        self.tabbed.tabCloseRequested.connect(self._closed_tab)

    def _add_tabs_widget(self):
        self.addWidget(self.tabbed)

    def _closed_tab(self, index):
        # TODO: Poziv close metode u zone. I odgovor na close metodu ( Window da li da se zatvori ako su namestene izmene)
        view = self.tabbed.widget(index)
        if view.close_zone():
            self.tabbed.removeTab(index)
            self.zones.pop(view.name)
