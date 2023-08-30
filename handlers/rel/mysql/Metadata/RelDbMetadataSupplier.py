import abc


class RelDbMetaDataSupplier(metaclass=abc.ABCMeta):

    def __init__(self, conn, table, schema=None):
        self._conn = conn
        self._table = table
        self._schema = schema

    @abc.abstractmethod
    def extract(self):
        ...

    @abc.abstractmethod
    def store(self):
        ...
