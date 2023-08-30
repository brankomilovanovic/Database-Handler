from multimethod import multimethod
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from handlers.utils.Connection.Connection import Connection


class MongoDbConnection(Connection):
    MAX_POOL_SIZE = 20

    @multimethod
    def __init__(self):
        self.new = True

        self.name = ""
        self.protocol = "mongodb"

        self.hostname = MongoClient.HOST
        self.port = MongoClient.PORT
        self.database = ""

        self.cluster_uri = None
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
        self.protocol = conn['protocol']
        self.cluster_uri = conn['cluster_uri']
        self.database = conn['database']

        self._conn = None

        self._saved = self.make_dict()

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.hostname != other.hostname:
            return False
        if self.port != other.port:
            return False
        if self.user != other.user:
            return False
        if self.protocol != other.protocol:
            return False
        if self.cluster_uri != other.cluster_uri:
            return False
        if self.database != other.database:
            return False

        return True

    def __str__(self):
        details = ""

        details += f"  Name: {self.name}"
        details += f"    User: {self.user}"
        details += f"    Hostname: {self.hostname}"
        details += f"    Port: {self.port}"
        details += f"    Database: {self.database}"
        details += f"    Protocol: {self.protocol}"
        details += f"    Cluster: {self.cluster_uri}"

        return details

    def make_dict(self):
        return {
            'name': self.name,
            'hostname': self.hostname,
            'port': self.port,
            'user': self.user,
            'database': self.database,
            'protocol': self.protocol,
            'cluster_uri': self.cluster_uri
        }

    def connect(self, parent):
        try:
            password = self._enter_password_dialog(parent=parent)
            if not password:
                return False
            print(password)

            client = None

            if self.cluster_uri:
                # Connection string for MongoDB Atlas cluster
                connection_string = f"{self.protocol}://{self.user}:{password}@{self.cluster_uri}/?retryWrites=true&w=majority"
                client = MongoClient(connection_string, server_api=ServerApi('1'))

            else:
                # Connection string for local MongoDB server
                connection_string = f"{self.protocol}://{self.user}:{password}@{self.hostname}:{self.port}/{self.database}"
                client = MongoClient(connection_string, )
            print(connection_string)

            self._conn = client
        # Send a ping to confirm a successful connection

            client.admin.command('ping')
            # print("Pinged your deployment. You successfully connected to MongoDB!")
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
