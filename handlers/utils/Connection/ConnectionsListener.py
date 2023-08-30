import abc

from handlers.rel.mysql.Connection.mysqlconnection import MySqlConnection
from handlers.utils.Connection.Connection import Connection


class ConnectionsListener(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def added(self, conn: Connection):
        raise NotImplementedError

    @abc.abstractmethod
    def removed(self, conn: Connection):
        raise NotImplementedError
