from multimethod import multimethod

from pyArango.connection import Connection as ArangoConnection

from handlers.utils.Connection.Connection import Connection


class ArangoDBConnection(Connection):
    @multimethod
    def __init__(self):
        self.new = True

        self.name = ""

        self.protocol = "http"
        self.hostname = 'localhost'
        self.port = 8529
        self.database = ""

        self.user = ""

        self._conn = None

        self._saved = None

    @multimethod
    def __init__(self, conn: dict):
        self.new = False

        self.name = conn['name']
        self.hostname = conn['hostname']
        self.port = conn['port']
        self.user = conn['user']
        self.database = conn['database']

        self._conn = None

        self._saved = self.make_dict()

    def make_dict(self):
        return {
            'name': self.name,
            'hostname': self.hostname,
            'port': self.port,
            'user': self.user,
            'database': self.database
        }

    def connect(self, parent):
        try:
            password = self._enter_password_dialog(parent=parent)
            if not password:
                return False
            print(password)

            client = ArangoConnection(arangoURL=f"{self.protocol}://{self.hostname}:{self.port}",
                                      username=self.user,
                                      password=password)
            self._conn = client
            return True
        except Exception as e:
            print(e)
            return False

    def get_connection(self):
        if self._conn is None: ...
        return self._conn

    def close(self):
        if self._conn is None:
            self._conn.close()
            self._conn = None

    def connected(self):
        return self._conn is not None
