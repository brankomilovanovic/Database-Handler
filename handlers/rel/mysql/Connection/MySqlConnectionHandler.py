from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QMenu

from app.PluginLikeStuff.Plugin import Plugin
from handlers.rel.Workspace.RelDBWorkspaceHandler import RelDBWorkspaceHandler
from handlers.rel.mysql.Connection.UI.NewRelDBConnectionWindow import NewRelDBConnectionWindow
from handlers.rel.mysql.Connection.mysqlconnections import MySqlConnections
from ui.menubar.MenuBar import MenuBar
from ui.window.MainWindow import MainWindow


# TODO: Proveriti da li se konekcija zatvara nakon

class MySqlConnectionHandler(Plugin):
    def activate(self) -> bool:
        self.connection_menu = self.menubar.set_menu("Connection")

        self.mysql_menu = QMenu('MySql', self.connection_menu)
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
        NewRelDBConnectionWindow(MainWindow.instance())
