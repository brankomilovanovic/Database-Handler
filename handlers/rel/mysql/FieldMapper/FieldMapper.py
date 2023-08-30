import mysql.connector
class FieldMapper:
    __instances = {}

    def __new__(cls, conn, schema):

        if conn.name in cls.__instances:
            if schema in cls.__instances[conn.name]:
                print(f"Already existing instance with schema:{schema}")
                return cls.__instances[conn.name][schema]
        else:
            print(f"Creating new FieldMapper with schema:{schema}")
            cls.__instances[conn.name] = {}
        
        new_instance = super(FieldMapper, cls).__new__(cls)
        new_instance.schema = schema
        new_instance.conn = conn
        cls.__instances[conn.name][schema] = new_instance
        print(cls.__instances)
        return new_instance

        

    def get_sc(self):
        return self.schema

    def get_conn(self):
        return self.conn
    
    def get_field_label(self, table, column):
        try:
            _conn = self.conn.get_connection()
            cursor = _conn.cursor()
            cursor.execute(f"USE {self.schema}")
            cursor.execute(f"SELECT logicki_naziv FROM field_mapper WHERE tabela_fizicki_naziv = '{table}' AND fizicki_naziv = '{column}'")
            name = cursor.fetchall()
            # cursor.close()
            # _conn.close()
            return name[0][0]
        except:
            return None
        finally:
            if cursor:
                cursor.close()
            if _conn:
                _conn.close()
    
    
    def get_table_label(self, table):
        try:
            _conn = self.conn.get_connection()
            cursor = _conn.cursor()
            cursor.execute(f"USE {self.schema}")
            cursor.execute(f"SELECT tabela_logicki_naziv FROM field_mapper WHERE tabela_fizicki_naziv = '{table}'")
            name = cursor.fetchall()
            return name[0][0]
        except Exception as e:
            print(f"Error occurred: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            if _conn:
                _conn.close()




