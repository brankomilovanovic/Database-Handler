from PyQt5.QtWidgets import QLabel, QWidget


class DescriptionLabel(QLabel):
    def __init__(self, text: str, parent: QWidget):
        super().__init__(text, parent)
        self.setMaximumWidth(300)
        self.setWordWrap(True)
        self.setStyleSheet("QLabel{"
                           "font-size: 8pt;}")
