from handlers.nosql.mongodb.DocumentView.DocumentView import DocumentView
from handlers.rel.mysql.Zone.Zone import ZoneView


class MongoDBZoneHandler:
    def __init__(self, parent, pool, database, collection):
        self._name = MongoDBZoneHandler.assemble_name(database, collection)
        self.view = ZoneView(parent)
        self.view.set_close(self.close)
        self.view.name = self._name

        conn = pool.get_connection()

        db = conn.get_database(database)
        col = db.get_collection(collection)

        docs = col.find()

        self.docView = DocumentView(self.view, docs)

        self.view.set_parent_zone(self.docView)

        # Child zone

    def close(self) -> bool:
        print(f"ZoneHandler : Closing zone {self._name}")
        self.view.close()
        return True

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_view(self):
        return self.view

    @staticmethod
    def assemble_name(database, collection):
        return f'{database}.{collection}'

    @staticmethod
    def name_format():
        return 'database.collection'
