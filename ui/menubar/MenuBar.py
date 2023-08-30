import sys
from xmlrpc.client import Boolean

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMenuBar, QMenu, QAction, QMessageBox


class MenuBar(QMenuBar):
    __instance = None

    @staticmethod
    def instance():
        return MenuBar.__instance

    def __init__(self, parent=None):
        super().__init__(parent)
        MenuBar.__instance = self
        self.menus = {}

        # Menu setup
        self.menus["File"] = QMenu("File", self)
        self.menus["Edit"] = QMenu("Edit", self)
        self.menus["View"] = QMenu("View", self)
        self.menus["Help"] = QMenu("Help", self)

        self.addMenu(self.menus["File"])
        self.addMenu(self.menus["Edit"])
        self.addMenu(self.menus["View"])
        self.addMenu(self.menus["Help"])

        # FILE menu

        # file menu - CLOSE
        self.exitAct = QAction(QIcon("assets/img/icon8/Fluent/icons8-shutdown-32.png"), '&Exit', self)
        self.exitAct.setShortcut('Ctrl+Q')
        self.exitAct.setStatusTip('Exit application')
        self.exitAct.triggered.connect(self.close_application)

        self.menus["File"].addAction(self.exitAct)

        # EDIT menu

        # VIEW menu

        # HELP menu

    def close_application(self):
        choice = QMessageBox.question(self,
                                      'Closing menu',
                                      'Do you want to exit the application?',
                                      QMessageBox.Yes | QMessageBox.No)

        if choice == QMessageBox.Yes:
            print("Closing the application.")
            sys.exit()
        else:
            pass

    # TODO: Ideja za poziv metoda za reaktivno dodavenj menual

    # Ideja je da se meniji mogu dodavati reaktivno proizoljno u dubinu, i usmesto prostih QAction mogu se dodati i
    # reaktivni(ili bilo koji drugi compleksni) prikazi u meniu, napr konkecija za listi konekcija sa tackom (zelena, crvena) koja se reaktivno menja u zavisnosti
    # od aktivnosti konekcije, i pritom omogucacan konektovanje klikom na konekciju

    # connection.mysql.new
    # connection.edit
    # connection.mysql.recent.localhost@igor *
    # connection.mysql.recent.localhost@marko x
    def set_menu(self, menu: str, pos: int = None) -> QMenu:
        if menu not in self.menus:
            self.menus[menu] = QMenu(menu, self)
            self.addMenu(self.menus[menu])

        return self.menus[menu]

    def get_menu(self, menu: str) -> bool | QMenu:
        if menu not in self.menus:
            return False
        return self.menus[menu]

    # def set_submenu(self, submenu: [str], icon: str, callback, statustip=None,
    #                 shortcut=None) -> bool:
    #
    #     menu = self.set_menu(submenu[0])
    #
    #     # newaction = QAction(QIcon(icon), submenu, menu)
    #
    #     return True
