from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow

from ui.menubar.MenuBar import MenuBar
from ui.statusbar.StatusBar import StatusBar
from ui.workspace.Workspace import Workspace


class MainWindow(QMainWindow):
    __instance = None

    @staticmethod
    def instance():
        return MainWindow.__instance
    def __init__(self):
        super().__init__()
        MainWindow.__instance = self

        # Main styling

        self.resize(600, 480)
        self.setWindowTitle("PlyInfo")
        self.setWindowIcon(QIcon("../assets/img/icons8-edit-file-64.png"))

        # Main-components

        self._statusbar = StatusBar(self)
        self._menubar = MenuBar(self)
        self._workspace = Workspace(self)
        # _toolbar =
        self._workspace.widget_added.connect(self.on_widget_added)

        # Main-components arrangements
        self.setMenuBar(self._menubar)
        self.setStatusBar(self._statusbar)
        self.setCentralWidget(self._workspace)

        # TODO: Dodati ove funkcionalnosti i neke tome slicne u plugin koji dodaje u setting ove opcije
        # style scheet se za main window mora setovati od jednom sa svim postavkama
        self.setStyleSheet("QWidget { "
                           "font-size: 18px;"
                           "icon-size: 34px 34px; "
                           "},")

    # def setup_workspace_signals(self):
    #     self._workspace.relDbView.table_clicked.connect(self.on_table_clicked)
    
    def on_widget_added(self):
        self._workspace.relDbView.table_clicked.connect(self.on_relDB_workspace_table_clicked)
    
    def on_relDB_workspace_table_clicked(self, conn_name, tab_name, item_name):
        print(f"Clicked item {item_name} in schema {tab_name} using connection {conn_name}")





# The method that will be used as the slot


