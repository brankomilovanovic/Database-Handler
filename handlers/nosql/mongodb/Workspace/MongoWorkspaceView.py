import os
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import uic
from PyQt5.QtCore import QSize, Qt, pyqtSignal

class MongoWorkspaceView(QWidget):
    collection_clicked = pyqtSignal(str, str, str)
    def __init__(self):
        super().__init__()
        uic.loadUi(f"handlers{os.path.sep}nosql{os.path.sep}mongodb{os.path.sep}Workspace{os.path.sep}mongoWS.ui", self)
        self.connName = ""


    def populate_mongo_tree(self, data):
        if data is not None:
            self.mongoTree.setHeaderLabels(["Databases & Collections"])
            self.mongoTree.clear()
            items = []
            for key, values in data.items():
                item = QTreeWidgetItem([key])
                item.setIcon(0, QIcon(f"assets{os.path.sep}img{os.path.sep}iconmonstr-database-10-16.png"))
                for value in values:
                    ext = value.split(".")[-1].upper()
                    child = QTreeWidgetItem([value, ext])
                    child.setIcon(0, QIcon(f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-folder-32.png"))
                    item.addChild(child)
                items.append(item)

            self.mongoTree.insertTopLevelItems(0, items)
            self.mongoTree.itemDoubleClicked.connect(self.on_item_clicked)

    
    def on_item_clicked(self, item):

        # current_tab_name = self.relTabbedpane.tabText(self.relTabbedpane.currentIndex())
        try:

            self.collection_clicked.emit(self.connName, item.parent().text(0), item.text(0))

        except AttributeError:
            print("Clicked database instead of collection")