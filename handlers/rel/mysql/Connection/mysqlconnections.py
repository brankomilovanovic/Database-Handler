import os

from multimethod import multimethod

from handlers.rel.mysql.Connection.mysqlconnection import MySqlConnection
from handlers.utils.Connection.Connections import Connections


class MySqlConnections(Connections):
    __instance = None

    # def __init__(self):
    #     Connections.__instance = self
    #
    #     self.connections = []
    #     self._subscriptions = []
    #
    #     self._CONNECTIONS_PATH = f'cache{os.path.sep}mysql{os.path.sep}connections{os.path.sep}connections.json'
    #     try:
    #         self._load_connections()
    #         print("Uspesno ucitavanje")
    #     except IOError:
    #         print("There is no connections, so we will create all necessary files, and folders")
    #         os.makedirs(os.path.dirname(self._CONNECTIONS_PATH), exist_ok=True)
    #         self._save(self.connections)
    #         self.load_connections()

    def __new__(cls):
        if MySqlConnections.__instance is None:
            connections = super(MySqlConnections, cls).__new__(cls)

            MySqlConnections.__instance = connections

            connections.connections = []
            connections.stored_connections = []
            connections._subscriptions = []

            connections._CONNECTIONS_PATH = f'cache{os.path.sep}mysql{os.path.sep}connections{os.path.sep}connections.json'
            try:
                connections._load_connections()
                print("Uspesno ucitavanje")
            except IOError:
                print("There is no connections, so we will create all necessary files, and folders")
                os.makedirs(os.path.dirname(connections._CONNECTIONS_PATH), exist_ok=True)
                connections._save(connections.connections)
                connections._load_connections()
        return MySqlConnections.__instance

    @staticmethod
    def instance():
        return MySqlConnections.__instance

    def _set_up(self, _connections: list[dict]) -> None:
        """
        For every raw connection dict from file connections.json or eny other source, creates 'Connection" object and
        saves it in the list of connections

        :param _connections: List of connections loaded form connections.json, every connection must be in dict format

        :return: None
        """
        self.stored_connections = []
        for connection in _connections:
            self.stored_connections.append(MySqlConnection(connection))

    @multimethod
    def delete_connection(self, index: int) -> bool:
        """
        The connection at the index position is deleted from the list of connections.

        Delete is not saved permanently, to permanently remove connection it is necessary to call save
        method, after this method is successfully finished.

        :type: int
        :param index: The connection position ( or index, starts from 0 ) , ( connection ) which should be removed from
                      the list of connections

        :exception : Parm "conn" not exist in list

        :return: Success of deleting connection from list of connections
        """

        for c in self._subscriptions:
            c.added(self.connections.__getitem__(index))

        self.connections.pop(index)

        return self.save_all_stored_connections()

    @multimethod
    def delete_connection(self, conn: MySqlConnection) -> bool:
        """
        Delete is not saved permanently, to permanently remove connection it is necessary to call save
        method, after this method is successfully finished.

        Delete is not saved permanently, to permanently remove connection it is necessary to call save
        function

        :type: bool
        :param conn: The Connection object to delete from the list

        :exception : Parm "conn" not exist in list

        :return: Success of deleting connection from list of connections
        """
        for index, conn_ in enumerate(self.connections):
            if conn_ is conn:
                return self.delete_connection(index)

        return False

    @multimethod
    def save(self, index: int) -> bool:
        """
        The connection ( it's changes ) at the index position is saved to connections.json file

        :type index: int
        :param index: Index of connection

        :exception : If the index of connection is greater than length of all connections or les than 0, IndexError
                     will be raised

        :return: Return success of saving changes to connections.json file
        """
        if index < 0 or index > len(self.connections):
            raise IndexError

        raw_connections = self.load_connections()
        if index < len(raw_connections):
            raw_connections[index] = self.connections[index].make_dict()
        else:
            raw_connections.append(self.connections[index].make_dict())
        self.connections[index].save_all_stored_connections()

        return self._save(raw_connections)

    @multimethod
    def save(self, conn: MySqlConnection) -> bool:
        """
        Saves the parm: 'conn" to connections.json file, if "conn" is found in list of connections stored in
        "Connections" object.

        :type conn: MySqlConnection
        :param conn: Connection object, for saving in connections.json file

        :exception : If the parm "conn" is not found in list of the connection,

        :return: Return success of saving changes to connections.json file
        """
        # for index, conn_ in enumerate(self.connections):
        #     if conn_ is conn:
        #         return self.save(index)
        saved = False
        # cons = self.load_connections()

        for i, c in enumerate(self.stored_connections):
            # print("c saved: ", c._saved)
            # print("conn saved: ", conn._saved)

            if c._saved == conn._saved:
                self.stored_connections[i] = conn
                saved = True
        if not saved:
            # print(f"Dodajem  {str(conn)} u self.stored_connections ")
            self.stored_connections.append(conn)
        self.save_all_stored_connections()

        # cons.append(conn.make_dict())
        # self._save(cons)

        return False

    def save_as(self, conn: MySqlConnection):
        if self.is_name_available(conn):
            self.stored_connections.append(conn)
            cons = self.load_connections()
            cons.append(conn.make_dict())
            self._save(cons)
            self._load_connections()

            for i, c in enumerate(self.stored_connections):
                for s in self.connections:
                    if c._saved == s._saved:
                        self.stored_connections[i] = s
