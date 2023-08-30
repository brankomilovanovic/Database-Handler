import os
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from PyQt5.QtGui import QFont, QIcon
from PyQt5 import uic
from PyQt5.QtCore import QSize, Qt, pyqtSignal

class ArangoWorkspaceView(QWidget):
    collection_clicked = pyqtSignal(str, str, str, str)  
    def __init__(self):
        super().__init__()
        uic.loadUi(f"handlers{os.path.sep}nosql{os.path.sep}arangodb{os.path.sep}Workspace{os.path.sep}arangoWS.ui", self)
        self.connName = ""


    def populate_arango_tree(self, data):
        if data is not None:
            self.arangoTree.setHeaderLabels(["Databases, Collections & Graphs"])
            self.arangoTree.clear()
            items = []
            for key, values in data.items():

                database = QTreeWidgetItem([key])
                database.setIcon(0, QIcon(f"assets{os.path.sep}img{os.path.sep}iconmonstr-database-10-16.png"))
                collections = QTreeWidgetItem(['collections'])
                graphs = QTreeWidgetItem(['graphs'])

                for value in values:
                    ext = value.split(".")[-1].upper()
                    parts = value.split(';')
                    child = QTreeWidgetItem([parts[0], ext])
                    if(parts[1] == "COLLECTION"):
                        child.setIcon(0, QIcon(f"assets{os.path.sep}img{os.path.sep}document-icon-36561.png"))
                        collections.addChild(child)
                    elif(parts[1] == "GRAPH"):
                        child.setIcon(0, QIcon(f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-unit-32.png"))
                        graphs.addChild(child)
                    else:
                        child.setIcon(0, QIcon(f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-network-32.png"))
                        collections.addChild(child)
                
                database.addChild(collections)
                database.addChild(graphs)
                items.append(database)

            self.arangoTree.insertTopLevelItems(0, items)
            self.arangoTree.itemDoubleClicked.connect(self.on_item_clicked)
    
    def on_item_clicked(self, item):
    
      
        try:

            self.collection_clicked.emit(self.connName, item.parent().parent().text(0), item.text(0), item.parent().text(0))

        except AttributeError:
            print("Clicked database instead of collection or graph")
