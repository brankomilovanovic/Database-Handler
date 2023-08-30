import typing

from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTabWidget


class ArangoDbZoneView(QWidget):
    def __init__(self, parent: None) -> None:
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self._close = None
        self.name = None

        # self.set_child_zone(QPushButton("Child Zone"))
        # self.set_parent_zone(QPushButton("Parent Zone"))

    def set_main_zone(self, zone):
        self.layout.insertWidget(0, zone)

    def set_close(self, clb):
        self._close = clb

    def close_zone(self):
        return self._close()

    # UI setup
    def _set_up_tabs(self):
        ...
        # self._add_tabs_widget()
        # self.child_tabs.setTabsClosable(True)
        # # self.tabbed.setMovable(True)
        # self.child_tabs.setContentsMargins(0, 0, 0, 0)
        # self.child_tabs.setStyleSheet("border:none;")
        #
        # self.child_tabs.tabCloseRequested.connect(self._closed_tab)
