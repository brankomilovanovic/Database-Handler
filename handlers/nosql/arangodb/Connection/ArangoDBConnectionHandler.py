from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenu, QAction

from app.PluginLikeStuff.Plugin import Plugin
from handlers.nosql.arangodb.Connection.UI.NewArangoDbConnectionWindow import NewArangoDbConnectionWindow
from ui.menubar.MenuBar import MenuBar
from ui.window.MainWindow import MainWindow


class ArangoDBConnectionHandler(Plugin):
    def activate(self) -> bool:
        self.connection_menu = self.menubar.set_menu("Connection")

        self.mysql_menu = QMenu('ArangoDB', self.connection_menu)
        self.connection_menu.addMenu(self.mysql_menu)

        connectAct = QAction(QIcon(), "Connect", self.connection_menu)
        connectAct.triggered.connect(self.connect)
        self.mysql_menu.addAction(connectAct)

    def deactivate(self) -> bool:
        self.connection_menu.clear()
        self.connection_menu.setVisible(False)

    def __init__(self):
        self.mysql_menu = None
        self.connection_menu = None
        self.menubar = MenuBar.instance()

        # Menu Setup

    def connect(self):
        NewArangoDbConnectionWindow(MainWindow.instance())
