from PyQt5.QtWidgets import QInputDialog, QLineEdit


class PasswordDialogInput(QInputDialog):
    def __init__(self, parent):
        super().__init__(parent)

        self.setTextEchoMode(QLineEdit.Password)
