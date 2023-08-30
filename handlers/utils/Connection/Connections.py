import json

from multimethod import multimethod

from handlers.utils.Connection.ConnectionsListener import ConnectionsListener
from handlers.utils.Connection.Connection import Connection


class Connections:

    def subscribe(self, callback: ConnectionsListener):
        print("New connection listener")
        self._subscriptions.append(callback)

        for conn in self.connections:
            callback.added(conn)

    def __getitem__(self, item: int) -> Connection:
        return self.connections[item]

    def __iter__(self):
        for conn_ in self.connections:
            yield conn_

    def __len__(self):
        return len(self.connections)

    def load_connections(self) -> list[dict]:
        """
        Returns list of raw connections from connections.json

        :return: List of, raw connection dict objects, just loaded from connections.json
        """
        try:
            connections_file = open(self._CONNECTIONS_PATH, 'r')
            connections = json.load(connections_file)
            connections_file.close()
            return connections
        except IOError:
            raise IOError

    def _load_connections(self):
        try:
            self._set_up(self.load_connections())
        except IOError:
            raise IOError

    def save_all_stored_connections(self) -> bool:
        """
        Saves current list of connections(from stored connections) it is, to connections.json  file

        :return: Return success of saving connections to connections.json file
        """
        for conn in self.stored_connections:
            conn.save()

        return self._save(self._connections_json())

    def _connections_json(self) -> list[dict]:
        """
        Returns list of all stored(but not necessarily connected) connections in 'Connections" object as they are in moment of function calling

        :return: List of all connections, every connection is dict with all parameters necessary for
                 making server connection (name, method, hostname, port, user, schema)
        """

        return [conn.make_dict() for conn in self.stored_connections]

    def _save(self, connections_json: list[dict]) -> bool:  # TODO: Docs
        connections_file = None
        print(f"Cuvam {connections_json}")
        try:
            with open(self._CONNECTIONS_PATH, 'w') as connections_file:
                connections_file.write(json.dumps(connections_json, indent=4))
                return True
        except FileNotFoundError:
            return False
        finally:
            if connections_file is not None and not connections_file.closed:
                connections_file.close()

    def get(self, name: str):
        for c in self.connections:
            if c.name == name:
                return c

        return None

    def get_index(self, _conn):
        for i, conn in enumerate(self.stored_connections):
            if conn == _conn:
                return i

    def add(self, conn: Connection) -> bool:
        """
        Adds new connection at the end of connections list, no validation is performed, "conn" object just have to be
        type of 'Connection"

        If parm: "conn" is not type od "Connection" False will be returned, otherwise True

        :param conn: Connection object

        :return: Success of adding new connection

        """
        if not isinstance(conn, Connection):
            return False
        if conn in self.connections:
            return False

        self.connections.append(conn)
        if conn not in self.stored_connections:
            self.stored_connections.append(conn)
        print(f"New connection {conn.name} at {conn.hostname} at {conn.port}")

        for c in self._subscriptions:
            c.added(conn)
        return True

    def is_name_available(self, conn: Connection) -> bool:
        """
        Checks is provided name available

        :param conn: The connection whose name is being checked

        :return: Is provided name founded in already created/saved connections
        """
        # print("Is connection name available ", conn.name)
        for _conn in self.connections + self.stored_connections:
            if _conn.is_same_name(conn.name):
                return False
        return True

