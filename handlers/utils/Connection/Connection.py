from abc import ABC, abstractmethod

from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog, QLineEdit


class Connection(ABC):

    @abstractmethod
    def make_dict(self) -> dict: ...

    @abstractmethod
    def connect(self, parent): ...

    @abstractmethod
    def get_connection(self) : ...

    @abstractmethod
    def close(self): ...

    def test(self, parent: QWidget) -> bool:
        try:
            test = self.connect(parent=parent)
            if test:
                msg = QMessageBox(QMessageBox.Information,
                                  f'Succeeded',
                                  f'Test connection was successful .')
                msg.exec_()
            else:
                msg = QMessageBox(QMessageBox.Warning,
                                  f'Failed',
                                  f"Test connection wasn't successful !!"
                                  )
                msg.exec_()
            return test
        finally:
            self.close()

    @abstractmethod
    def connected(self): ...


    def _not_valid_password_msg_box(self, parent: QWidget) -> bool:
        return QMessageBox(QMessageBox.Icon.Warning,
                           f"Invalid password",
                           f"The password you entered for user {self.user}, is not valid",
                           (QMessageBox.Cancel | QMessageBox.Retry),
                           parent).exec()

    def _enter_password_dialog(self, parent: QWidget) -> str:
        password, ok = QInputDialog.getText(parent,
                                            'Password',
                                            f"Enter a password for {self.user}: ",
                                            QLineEdit.Password)

        return password if ok else False

    def is_saved(self):
        return self.make_dict() == self._saved

    def save(self):
        self._saved = self.make_dict()
        self.new = False
        # self.close()

    def is_same_name(self, other_name: str) -> bool:
        if self._saved is not None:
            return self._saved["name"] == other_name
        return False
