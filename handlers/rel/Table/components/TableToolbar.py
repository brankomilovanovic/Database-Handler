from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton, QFrame, QToolBar, QLabel, QAction
from multimethod import multimethod


class TableToolBar(QToolBar):
    def __init__(self, parent):
        super().__init__(parent)


        # self.layout = QHBoxLayout(self)

        # Style setting

        # self.setSpacing(1)
        # self.setAlignment(Qt.AlignLeft)
        # self.setContentsMargins(10, 0, 0, 0)

    # @multimethod
    # def add_option(self, option: QWidget):
    #     self.layout.addWidget(option)

    def addToolAction(self, action: QAction):
        action.setParent(self)
        self.addAction(action)

    def add_spacing(self):
        lable = QLabel()
        lable.setFixedWidth(20)
        self.addWidget(lable)

    def add_separator(self):...
        # line = QFrame(self)
        # line.setFrameShape(QFrame.VLine)
        # line.setFrameShadow(QFrame.Sunken)
        # line.setLineWidth(1)
        #
        #
        # self.layout.addWidget(line)
