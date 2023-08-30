from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QToolButton, QMenu


class Options(QToolButton):
    def __init__(self, parent, icon):
        super().__init__(parent)

        self.setIcon(icon)
        self.setIconSize(QSize(32, 32))

        self.menu = QMenu(self)

        self.setMenu(self.menu)

        self.setPopupMode(QToolButton.MenuButtonPopup)


    def addMenuAction(self, action):
        self.menu.addAction(action)

    def addSelfCallableAction(self, action):
        self.menu.addAction(action)
        action.triggered.connect(self.call)

    def call(self):
        sender = self.sender()
        sender.clb(sender.param)
