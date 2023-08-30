from PyQt5.QtWidgets import QWidget

from handlers.nosql.mongodb.Connection.MongoDbConnection import MongoDbConnection
from handlers.nosql.mongodb.Workspace.MongoWorkspaceView import MongoWorkspaceView
from handlers.utils.Connection.ConnectionsListener import ConnectionsListener


class MongoWorkspaceHandler:
    class MongoDBConnectionListener(ConnectionsListener):

        def __init__(self, add_clb, remove_clb):
            self.add_clb = add_clb
            self.remove_clb = remove_clb

        def added(self, conn: MongoDbConnection):
            self.add_clb(conn)

        def removed(self, conn: MongoDbConnection):
            self.remove_clb(conn)

    def __init__(self):
        self.listener = MongoWorkspaceHandler.MongoDBConnectionListener(self.added, self.removed)
        self.workspace = MongoWorkspaceView() 

        
            
    def get_listener(self) -> ConnectionsListener:
        return self.listener
    
    
    def get_workspace(self) -> QWidget:
        return self.workspace
    


    def added(self, conn: MongoDbConnection):
        print(f"New connection is in workspace :{conn.name}")
        self.workspace.connName = conn.name
        self.workspace.MongoButton.clicked.connect(lambda: self.list_db_names_and_connections(conn))
        


    def removed(self, conn: MongoDbConnection):
        print(f"{conn.name} Connection is removed")
    
    
    def list_db_names_and_connections(self, conn):
        data = {}
        _conn = conn.get_connection()
        databases = _conn.list_database_names()
        for db in databases:
            data[db] = _conn[db].list_collection_names()
        self.workspace.populate_mongo_tree(data)




