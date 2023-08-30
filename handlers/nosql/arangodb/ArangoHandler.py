from app.PluginLikeStuff.Plugin import Plugin
from handlers.Handler import Handler
from handlers.nosql.arangodb.Connection.ArangoDBConnectionHandler import ArangoDBConnectionHandler
from handlers.nosql.arangodb.Connection.ArangoDBConnections import ArangoDBConnections
from handlers.nosql.arangodb.Workspace.ArangoWorkspaceHandler import ArangoWorkspaceHandler
from handlers.nosql.arangodb.Zone import ArangoDbZoneHandler
from handlers.nosql.arangodb.Zone.ArangoDbZoneHandler import ArangoDbZoneHandler
from handlers.rel.HandlerView import HandlerView


class ArangoHandler(Handler, Plugin):
    def activate(self) -> bool:
        self.connectionHandler.activate()

        # UI Setup
        # self.handler_workspace.set_workspace(self.workspace.get_workspace())  # TODO: uncomment

        # Main Window UI Setup
        self.main_window_workspace.add_nosql_workspace(self.handler_workspace, "ArangoDB")

        # self.open(None, None, 1)

        return True

    def deactivate(self) -> bool:
        # self.workspace.close()
        self.connectionHandler.deactivate()
        return True

    def __init__(self):
        super().__init__()

        self.connections = ArangoDBConnections()

        # UI Components
        self.handler_workspace = HandlerView()
        self.workspace = ArangoWorkspaceHandler()
        self.workspace.workspace.collection_clicked.connect(self.open) # TODO: Connect signal to open function

        # Initialize
        self.connectionHandler = ArangoDBConnectionHandler()

        #
        self.connections.subscribe(self.workspace.get_listener()) # TODO: uncomment

        # UI Setup
        self.handler_workspace.set_workspace(self.workspace.get_workspace())  # TODO: uncomment

        # Main Window UI Setup

    def open(self, conn, database, collection, type):
        print(f"Opening new arango handler with {conn} in {database} at {collection} with type {type}")
        if self.handler_workspace.is_in_zones(ArangoDbZoneHandler.assemble_name(database, collection)):
            # print("Postoji u zonama")
            self.handler_workspace.set_zone(ArangoDbZoneHandler.assemble_name(database, collection))
        else:
            # print("Ne Postoji u zonama")
            self.handler_workspace.add_zone(ArangoDbZoneHandler(self.handler_workspace,
                                                                self.connections.get(conn),
                                                                database,
                                                                collection,
                                                                type))
