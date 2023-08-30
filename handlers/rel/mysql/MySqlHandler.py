from PyQt5.QtWidgets import QWidget

from app.PluginLikeStuff.Plugin import Plugin
from handlers.rel.RelDBHandler import RelDBHandler
from handlers.rel.HandlerView import HandlerView
from handlers.rel.Workspace.RelDBWorkspaceHandler import RelDBWorkspaceHandler
from handlers.rel.mysql.Connection.MySqlConnectionHandler import MySqlConnectionHandler
from handlers.rel.mysql.Connection.mysqlconnections import MySqlConnections
from handlers.rel.mysql.Service.MySqlService import MySqlService
from handlers.rel.mysql.Workspace.MySqlWorkspaceHandler import MySqlWorkspaceHandler
from handlers.rel.mysql.Zone.Zone import ZoneView
from handlers.rel.mysql.Zone.ZoneHandler import ZoneHandler
from ui.workspace.Workspace import Workspace


class MySqlHandler(RelDBHandler, Plugin):
    def activate(self) -> bool:
        self.connectionHandler.activate()

        # UI Setup
        self.workspace.set_workspace(self.rel_dv_workspace.get_workspace())

        # Main Window UI Setup
        self.main_window_workspace.add_workspace(self.workspace)

        return True

    def deactivate(self) -> bool:
        self.workspace.close()
        self.connectionHandler.deactivate()
        return True

    def __init__(self):
        super().__init__()

        self.connections = MySqlConnections()

        # UI Components
        self.workspace = HandlerView()
        self.rel_dv_workspace = MySqlWorkspaceHandler()
        self.rel_dv_workspace.workspace.table_clicked.connect(self.open)

        # Initialize
        self.connectionHandler = MySqlConnectionHandler()

        #
        self.connections.subscribe(self.rel_dv_workspace.get_listener())

        # UI Setup
        # self.workspace.set_workspace(self.rel_dv_workspace.get_workspace())

        # Main Window UI Setup
        # self.main_window_workspace.add_workspace(self.workspace)

        # Mock part
        # self.open(None, None, 1)
        # self.open(None, None, 2)
        # self.open(None, None, 3)
        # self.open(None, None, 4)

    def open(self, conn, schema, table):
        if self.workspace.is_in_zones(ZoneHandler.assemble_name(schema, table)):
            # print("Postoji u zonama")
            self.workspace.set_zone(ZoneHandler.assemble_name(schema, table))
        else:
            # print("Ne Postoji u zonama")
            self.workspace.add_zone(ZoneHandler(self.workspace,
                                                MySqlConnections().get(conn),
                                                table,
                                                schema,
                                                lambda s, t: self.open(conn, s, t)))
