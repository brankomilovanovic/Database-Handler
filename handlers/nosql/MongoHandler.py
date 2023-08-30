from app.PluginLikeStuff.Plugin import Plugin
from handlers.Handler import Handler
from handlers.nosql.mongodb.Connection.MongoDbConnectionHandler import MongoDbConnectionHandler
from handlers.nosql.mongodb.Connection.MongoDbConnections import MongoDbConnections
from handlers.nosql.mongodb.Workspace.MongoWorkspaceHandler import MongoWorkspaceHandler
from handlers.nosql.mongodb.Zone.MongoDBZoneHandler import MongoDBZoneHandler

from handlers.rel.HandlerView import HandlerView


class MongoHandler(Handler, Plugin):
    def activate(self) -> bool:
        self.connectionHandler.activate()

        # UI Setup
        self.workspace.set_workspace(self.rel_dv_workspace.get_workspace())

        # Main Window UI Setup
        self.main_window_workspace.add_nosql_workspace(self.workspace, "MongoDB")

        # self.open(None, None, 1)

        return True

    def deactivate(self) -> bool:
        # self.workspace.close()
        self.connectionHandler.deactivate()
        return True

    def __init__(self):
        super().__init__()

        self.connections = MongoDbConnections()

        # UI Components
        self.workspace = HandlerView()
        self.rel_dv_workspace = MongoWorkspaceHandler()
        self.rel_dv_workspace.workspace.collection_clicked.connect(self.open)

        # Initialize
        self.connectionHandler = MongoDbConnectionHandler()

        #
        self.connections.subscribe(self.rel_dv_workspace.get_listener())


        # UI Setup
        self.workspace.set_workspace(self.rel_dv_workspace.get_workspace())

        # Main Window UI Setup

    def open(self, conn, database, collection):
        print(f"Opening new mongo handler with {conn} in {database} at {collection}")
        if self.workspace.is_in_zones(MongoDBZoneHandler.assemble_name(database, collection)):
            # print("Postoji u zonama")
            self.workspace.set_zone(MongoDBZoneHandler.assemble_name(database, collection))
        else:
            # print("Ne Postoji u zonama")
            self.workspace.add_zone(MongoDBZoneHandler(self.workspace,
                                                       self.connections.get(conn),
                                                       database,
                                                       collection))
