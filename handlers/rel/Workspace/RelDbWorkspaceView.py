import os

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox, QListWidget, QListWidgetItem
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QSize, Qt, pyqtSignal

from PyQt5 import uic


class RelDbWorkspaceView(QWidget):
    table_clicked = pyqtSignal(str, str, str)

    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi(f"handlers{os.path.sep}rel{os.path.sep}Workspace{os.path.sep}relWS.ui", self)
        self.relTabbedpane.tabCloseRequested.connect(lambda index: self.relTabbedpane.removeTab(index))
        self.connName = ""
        

    
        # Ovo je samo prof of concept metoda
    def display_dbs(self, schemas):

        for s in schemas:
            self.comboBox.addItem(s)

    def load_schema(self, tableList):
        dupes = False
        tab = QWidget()
        tab_layout = QVBoxLayout()
        tab.setLayout(tab_layout)
        
        for i in range(self.relTabbedpane.count()):
            tab_name = self.relTabbedpane.tabText(i)
            if tab_name == self.comboBox.currentText():
                dupes = True
                self.relTabbedpane.setCurrentIndex(i)

        if dupes == False:    
            self.relTabbedpane.addTab(tab, self.comboBox.currentText())
            self.relTabbedpane.setCurrentWidget(tab)

            self.listWidget = QListWidget()

            for i in tableList:
                item = QListWidgetItem(i)
                item.setIcon(QIcon(f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-relation-table-32.png"))
                self.listWidget.addItem(item)

            self.listWidget.itemDoubleClicked.connect(self.on_item_clicked)
            tab_layout.addWidget(self.listWidget)


    
    
    def resizeEvent(self, event):
        font = self.label.font()
        font_size = int(event.size().width() / 30)
        font.setPointSize(font_size)
        self.label.setFont(font)
        font2 = self.comboBox.font()
        font_size2 = int(event.size().width() / 30)
        font2.setPointSize(font_size2)
        self.comboBox.setFont(font2)


    def on_item_clicked(self, item):
        current_tab_name = self.relTabbedpane.tabText(self.relTabbedpane.currentIndex())
        self.table_clicked.emit(self.connName, current_tab_name, item.text())





    



