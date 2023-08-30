from handlers.nosql.arangodb.Connection.ArangoDBConnection import ArangoDBConnection
from handlers.nosql.arangodb.Workspace.ArangoWorkspaceView import ArangoWorkspaceView
from handlers.utils.Connection.ConnectionsListener import ConnectionsListener

from PyQt5.QtWidgets import QWidget


class ArangoWorkspaceHandler():
    class ArangoDBConnectionListener(ConnectionsListener):
    
        def __init__(self, add_clb, remove_clb):
            self.add_clb = add_clb
            self.remove_clb = remove_clb

        def added(self, conn: ArangoDBConnection):
            self.add_clb(conn)

        def removed(self, conn: ArangoDBConnection):
            self.remove_clb(conn)

    def __init__(self):
        self.listener = ArangoWorkspaceHandler.ArangoDBConnectionListener(self.added, self.removed)
        self.workspace = ArangoWorkspaceView() 

        
            
    def get_listener(self) -> ConnectionsListener:
        return self.listener
    
    
    def get_workspace(self) -> QWidget:
        return self.workspace
    


    def added(self, conn: ArangoDBConnection):
        print(f"New connection is in workspace :{conn.name}")
        self.workspace.connName = conn.name
        self.workspace.ArangoButton.clicked.connect(lambda: self.list_db_names_and_connections(conn))
        


    def removed(self, conn: ArangoDBConnection):
        print(f"{conn.name} Connection is removed")
    
    
    def list_db_names_and_connections(self, conn):
        data = {}
        _conn = conn.get_connection()
        databases = _conn.databases.keys() #all databases in the arango connection
        for db in databases:
            valid = []
            graphs = _conn[db].graphs
            for graph in graphs:
                valid.append(graph + ";" + "GRAPH")
            collections = _conn[db].collections
            for collection_name in collections:
                collection = collections[collection_name]
                if not collection.isSystem: #Getting collections only from the specific database, not the system

                    if(collection.__class__.__name__ == "Collection"):
                        valid.append(collection_name + ";" + "COLLECTION") 
                    else:
                        valid.append(collection_name + ";" + "EDGE") 
            data[db] = valid
        self.workspace.populate_arango_tree(data)





            
