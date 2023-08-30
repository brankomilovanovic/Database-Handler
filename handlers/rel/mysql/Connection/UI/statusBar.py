from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStatusBar, QWidget, QHBoxLayout, QPushButton, QLabel


class StatusBar(QStatusBar):
    def __init__(self, parent):
        super().__init__(parent)

    def show_msg(self, msg):
        self.show()
        self.showMessage(msg, 10)


class _StatusBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        # SET UP PARAMETERS
        # self.setStyleSheet(STYLES.statusBarNewConn)

        # LAYOUT
        self.main_h_layout = QHBoxLayout()

        # COMPONENTS
        # self.icon = QPixmap(icon.APPROVAL_I())
        # self.label_icon = QLabel(self)
        # self.label_icon.setPixmap(self.icon)
        # self.label_icon.setFixedWidth(16)
        # self.label_icon.setFixedHeight(16)

        btn = QPushButton(QIcon("assets/img/icon8/Fluent/icons8-approval-32.png"), "", self)
        btn.setEnabled(False)
        # btn.setStyleSheet(STYLES.btn_icon)

        self.label = QLabel("This is new status bar ??")

        # LAYOUT SET UP
        # self.main_h_layout.addWidget(self.icon_pixmap)
        # self.main_h_layout.addWidget(self.label_icon)
        self.main_h_layout.addWidget(btn)
        self.main_h_layout.addWidget(self.label)
        # SET UP
        self.setLayout(self.main_h_layout)
        self.show()

    def show_message_warning(self, msg):
        ...  # self.setWindowIcon(QIcon)

    def show_message_success(self, msg):
        ...  # self.setWindowIcon(QIcon)

    def hide(self):
        self.hide()
