from handlers.rel.Service.RelDbService import RelDbService


class MySqlService(RelDbService):
    def __init__(self, conn, schema, table):
        self.conn = None
        self.schema = None
        self.table = None

    def select(self, batch=None):
        db = self.conn.get_connection()
        cursor = db.cursor()

        cursor.execute(f"SELECT * FROM {self.schema}.{self.table};")

        return cursor.fetchall()

# class Repository:
#     def __init__(self, conn, schema, table):
#         ...

