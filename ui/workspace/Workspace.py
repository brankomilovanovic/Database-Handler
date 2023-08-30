from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTabWidget
from handlers.rel.Workspace.RelDbWorkspaceView import RelDbWorkspaceView

from ui.statusbar.StatusBar import StatusBar
from ui.workspace.LayoutManager import _LayoutManager
from PyQt5.QtCore import pyqtSignal


class Workspace(QWidget):
    widget_added = pyqtSignal()
    __instance = None

    @staticmethod
    def instance():
        return Workspace.__instance

    def __init__(self, parent=None):
        super().__init__(parent)
        Workspace.__instance = self
        self.relDbView = ""
        self.tabs = None

        # properties
        self._statusbar = StatusBar.instance()

        # layout
        self.layout = _LayoutManager(self)

        # style
        # self.setStyleSheet("border: 1px solid red;")

        self._statusbar.showMessage("Workspace created")

        # Mock part
        # button = QPushButton("Button")
        # self.add_workspace(button)

    def add_workspace(self, widget):
        self.layout.insertWidget(0, widget)

        for widget in self.children():
            print(widget)
        self.relDbView = self.findChild(RelDbWorkspaceView)
        self.widget_added.emit()
        # self.relDbView.table_clicked.connect(self.on_table_clicked)

    def add_nosql_workspace(self, widget, name):
        if self.tabs == None:
            self.tabs = QTabWidget(self)
            self.layout.addWidget(self.tabs)

        self.tabs.addTab(widget, name)
    # def on_table_clicked(self, conn_name, tab_name, item_name):
    #      print(f"Clicked item {item_name} in schema {tab_name} using connection {conn_name}")
