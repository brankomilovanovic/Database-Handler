from handlers.nosql.arangodb.Workspace.LoadGraphFromDB_Test import ViewClass, load_graph_from_db  ## import viewclass from GraphView2.py, fix this
from handlers.nosql.mongodb.DocumentView.DocumentView import DocumentView
from handlers.rel.mysql.Zone.Zone import ZoneView
from handlers.nosql.arangodb.InsertUI.AddNodeWindow import AddNodeWindow
from handlers.nosql.arangodb.UpdateUI.UpdateNodeWindow import UpdateNodeWindow
from handlers.nosql.arangodb.Actions.ArangoDBActions import ArangoDBActions

from PyQt5.QtWidgets import QToolBar, QVBoxLayout, QWidget
from PyQt5.QtGui import QIcon

class ArangoDbZoneHandler:
    def __init__(self, parent, pool, database, collection, type):
        self._name = ArangoDbZoneHandler.assemble_name(database, collection)
        self.parent = parent
        self.view = ZoneView(parent)
        self.view.set_close(self.close)
        self.view.name = self._name
        self.type = type

        self.collection = collection

        conn = pool.get_connection()

        self.db = conn[database]

        self.actions = ArangoDBActions(pool, database)

        if(self.type == 'collections'):
            col = self.db[collection]

            docs = col.fetchAll()
            self.docView = DocumentView(self.view, str(docs))

            self.view.set_parent_zone(self.docView)
        else:
            # graph json
            # graph_as_json = load_graph_from_db(self.db, collection)

            # GRAPH VIEW HERE ..

            self.widget = QWidget()
            self.widget_layout = QVBoxLayout(self.widget)

            self.toolbar = QToolBar()

            self.action_insert = self.toolbar.addAction(QIcon("assets/img/icon8/Fluent/icons8-plus-math-32.png"), "Insert")
            self.action_insert.triggered.connect(self.insert_node)

            self.action_update = self.toolbar.addAction(QIcon("assets/img/icon8/Fluent/icons8-edit-32.png"), "Update")
            self.action_update.triggered.connect(self.update_node)

            self.action_delete = self.toolbar.addAction(QIcon("assets/img/icon8/Fluent/icons8-delete-32.png"), "Delete")
            self.action_delete.triggered.connect(self.delete_node)

            self.widget_layout.addWidget(self.toolbar)

            self.graphView = ViewClass()  # Should be imported from the GraphView2.py file, MODIFY THIS
            self.widget_layout.addWidget(self.graphView)

            self.view.set_parent_zone(self.widget) 
            self.sceneClass = self.graphView.s

            self.unique_graph, self.loaded_graph, self.collection_names = load_graph_from_db(self.db, self.collection, {})
            self.sceneClass.createGraphFromJson(self.unique_graph) # Loading and viewing

            print(self.collection_names) ## Collection names 
            print('Graph visualization')


        # Child zone

    def close(self) -> bool:
        print(f"ZoneHandler : Closing zone {self._name}")
        self.view.close()
        return True

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_view(self):
        return self.view

    @staticmethod
    def assemble_name(database, collection):
        return f'{database}.{collection}'

    @staticmethod
    def name_format():
        return 'database.collection'
    
    def insert_node(self):
        def clb(value):
            payload = self.actions.create(value)
            if(len(payload) > 0 and payload[2]):
                f.close()
                self.unique_graph, self.loaded_graph, self.collection_names = load_graph_from_db(self.db, self.collection, self.loaded_graph)
                self.sceneClass.createGraphFromJson(self.unique_graph) # Loading and viewing
            else:
                f.showMessage("Error adding node")

        f = AddNodeWindow(self.parent, clb, self.collection_names)
        f.exec()

    def update_node(self):
        if(self.sceneClass.selected_item):
            try:
                self.node = self.actions.get({
                    "collectionName": self.sceneClass.selected_item.key.split("/")[0], 
                    "key": self.sceneClass.selected_item.key
                })

                if(self.node[1]):
                    self.selected_node = {
                        "collectionName": self.node[2]['_id'].split("/")[0], 
                        "_key": self.node[2]['_key'],
                        "document": self.node[2]['body']
                    }
                    def clb(value):
                        payload = self.actions.update(value)
                        if(len(payload) > 0 and payload[1]):
                            f.close()
                        else:
                            f.showMessage("Error updating node")
                        
                    f = UpdateNodeWindow(self.parent, self.selected_node, clb, self.collection_names)
                    f.exec()
            except:
                return
    
    def delete_node(self):
        if(self.sceneClass.selected_item):
            try:
                self.selected_node = {
                    "collectionName": self.sceneClass.selected_item.key.split("/")[0], 
                    "key": self.sceneClass.selected_item.name
                }

                payload = self.actions.delete(self.selected_node)
                if(len(payload) > 0 and payload[1]):
                    self.sceneClass.deleteSelectedItem()
            except: 
                return