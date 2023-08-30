from types import NoneType

from PyQt5.QtWidgets import QStatusBar


# TODO: Status bar se ne prikazuje

class StatusBar(QStatusBar):
    __instance = None

    @staticmethod
    def instance():
        return StatusBar.__instance

    def __init__(self, parent=None):
        #Set up
        super().__init__(parent)
        StatusBar.__instance = self

        # Style
        self.setStyleSheet("border-top: 1px solid gray;")

        self.showMessage("Status bar")

    def showMessage(self, message: str):
        print(f"Status bar should display message: {message} for  sec")
        super().showMessage(message)
