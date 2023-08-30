import mysql.connector
import threading
from handlers.rel.mysql.Connection.mysqlconnection import MySqlConnection
from handlers.rel.mysql.Metadata.MySqlMetadataSupplier import MySqlMetadataSupplier
from ui.window.MainWindow import MainWindow


class ModifyInterface:
    def perform_action(self, current_descriptor):
        pass


class ActionABS(ModifyInterface):
    def __init__(self, connection, metadata):
        self.connection = connection
        self.metadata = metadata
        self.column_names = [c.code_name for c in metadata.columns]
        self.table_name = metadata.codeName
        self.schema_name = metadata.schema
        self.primary_columns = [c.code_name for c in metadata.columns if c.primary]


class InsertAction(ActionABS):
    def __init__(self, connection, metadata) -> None:
        super().__init__(connection, metadata)
        self.result = []

    def perform_action(self, current_descriptor):
        self.result = []
        # values = current_descriptor.values
        values = list(current_descriptor.values())
        values_str = ', '.join(map(lambda v: f"'{v}'", values))
        success = False
        result_msg = "Error occurred during insert action"
        sql = f"INSERT INTO {self.schema_name}.{self.table_name} ({', '.join(self.column_names)}) VALUES ({values_str})"
        print(sql)

        conn = self.connection.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            conn.commit()
            result_msg = "Action insert completed successfully."
            success = True
        except mysql.connector.Error as error:
            result_msg = ("Error occurred during insert action:" + str(error))
            success = False
        finally:
            if cursor:
                cursor.close()
            conn.close()
        self.result = [success, result_msg]


class UpdateAction(ActionABS):
    def __init__(self, connection, metadata) -> None:
        super().__init__(connection, metadata)
        self.result = []

    def perform_action(self, current_descriptor):
        self.result = []
        success = False
        result_msg = "Error occurred during update action"
        set_clause = ', '.join(f"{column} = '{value}'" for column, value in current_descriptor.items() if
                               column not in self.primary_columns)
        condition = ' AND '.join(
            f"{column} = '{value}'" for column, value in current_descriptor.items() if column in self.primary_columns)

        sql = f"UPDATE {self.schema_name}.{self.table_name} SET {set_clause} WHERE {condition}"
        print(sql)

        conn = self.connection.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            conn.commit()
            result_msg = "Action update completed successfully."
            success = True
        except mysql.connector.Error as error:
            result_msg = ("Error occurred during update action:" + str(error))
            success = False
        finally:
            if cursor:
                cursor.close()
            conn.close()
        self.result = [success, result_msg]



class DeleteAction(ActionABS):
    def __init__(self, connection, metadata) -> None:
        super().__init__(connection, metadata)
        self.result = []

    def perform_action(self, current_descriptor):
        self.result = []
        condition = ' AND '.join(
            f"{column} = '{value}'" for column, value in current_descriptor.items() if column in self.primary_columns)

        sql = f"DELETE FROM {self.schema_name}.{self.table_name} WHERE {condition}"

        print(sql)

        conn = self.connection.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            conn.commit()
            result_msg = "Action update completed successfully."
            success = True
        except mysql.connector.Error as error:
            result_msg = ("Error occurred during update action:" + str(error))
            success = False
        finally:
            if cursor:
                cursor.close()
            conn.close()
        self.result = [success, result_msg]

class NavigateSearch:
    def search(self, current_descriptor):
        pass


class FilterAction(ActionABS):
    def __init__(self, connection, metadata) -> None:
        super().__init__(connection, metadata)
        self.result = []

    def perform_action(self, current_descriptor):
        self.result = []
        conditions = []
        values = []

        for column, value in current_descriptor.items():
            conditions.append(f"{column} LIKE %s")
            values.append(f"%{value}%")

        conditions_str = " AND ".join(conditions)
        sql = f"SELECT * FROM {self.schema_name}.{self.table_name} WHERE {conditions_str}"
        # print(values)
        print(sql)

        conn = self.connection.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, values)
            results = cursor.fetchall()

            # Process the results as needed
            for row in results:
                self.result.append(row)
                # print(row)
            # print(self.result)
            print("Action filter completed successfully.")
        except mysql.connector.Error as error:
            print("Error occurred during filter action:", error)
        finally:
            if cursor:
                cursor.close()

            conn.close()



class SearchAction(ActionABS):
    def __init__(self, connection, metadata) -> None:
        super().__init__(connection, metadata)
        self.result = []

    def perform_action(self, current_descriptor):
        self.result = []
        value = current_descriptor.get('value')  # Assuming the key is 'value'
        print(current_descriptor)
        if value is None or value == '':
            # print("Putanja 1")
            f_conditions_str = ""
            if 'default' in current_descriptor:
                if len(current_descriptor['default'].items()) > 0:
                    f_conditions_str = " WHERE "
                    # print(f_conditions_str)

                    for _column, _value in current_descriptor['default'].items():
                        f_conditions_str += f" {_column} = '{_value}'"
                        f_conditions_str += " AND "
                        # print(f_conditions_str)

                    f_conditions_str = f_conditions_str[:-len(" AND ")]
                    # print(f_conditions_str)
            else: ...
                # print("default value is not in current_descriptor")

            # Select all columns without any filtering conditions
            sql = f"SELECT * FROM {self.schema_name}.{self.table_name} {f_conditions_str}"
            values = []
        else:
            # print("Putanja 2")

            f_conditions = []
            f_conditions_str = ""
            if 'default' in current_descriptor:
                if len(current_descriptor['default'].items()) > 0:
                    for _column, _value in current_descriptor['default'].items():
                        f_conditions_str += f" AND {_column} = '{_value}'"


            conditions = []
            values = []

            for column in self.column_names:
                conditions.append(f"{column} LIKE %s")
                values.append(f"%{value}%")

            conditions_str = " OR ".join(conditions)
            sql = f"SELECT * FROM {self.schema_name}.{self.table_name} WHERE ({conditions_str}) {f_conditions_str}"
        print(sql)
        # print(values)

        conn = self.connection.get_connection()
        cursor = None
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, values)
            results = cursor.fetchall()
            # print("results:", results)

            # Process the results as needed
            for row in results:
                # print("result:", row)
                self.result.append(row)
                # print(row)

            print("Action select completed successfully.")
            # print(result)
        except mysql.connector.Error as error:
            print("Error occurred during select action:", error)
        finally:
            if cursor:
                cursor.close()
            conn.close()


class RelDBActions:
    def __init__(self, connection, metadata):
        self._conn = connection
        self.metadata = metadata
        self.insert_action = InsertAction(self._conn, self.metadata)
        self.update_action = UpdateAction(self._conn, self.metadata)
        self.delete_action = DeleteAction(self._conn, self.metadata)
        self.filter_action = FilterAction(self._conn, self.metadata)
        self.search_action = SearchAction(self._conn, self.metadata)

    def insert(self, current_descriptor):
        insert_thread = threading.Thread(target=self.insert_action.perform_action, args=(current_descriptor, ))
        insert_thread.start()
        insert_thread.join()
        print(self.insert_action.result)
        return self.insert_action.result

    def update(self, current_descriptor):
        update_thread = threading.Thread(target=self.update_action.perform_action, args=(current_descriptor, ))
        update_thread.start()
        update_thread.join()
        print(self.update_action.result)
        return self.update_action.result

    def delete(self, current_descriptor):
        delete_thread = threading.Thread(target=self.delete_action.perform_action, args=(current_descriptor, ))
        delete_thread.start()
        delete_thread.join()
        print(self.delete_action.result)
        return self.delete_action.result

    def filter(self, current_descriptor):
        filter_thread = threading.Thread(target=self.filter_action.perform_action, args=(current_descriptor, ))
        filter_thread.start()
        filter_thread.join()
        return self.filter_action.result

    def search(self, current_descriptor):
        search_thread = threading.Thread(target=self.search_action.perform_action, args=(current_descriptor, ))
        search_thread.start()
        search_thread.join()
        return self.search_action.result


def testings():
    _conn = MySqlConnection({
        "name": "connection",
        "method": "",
        "hostname": "localhost",
        "port": "3306",
        "user": "root",
        "schema": "",
    })
    _conn.connect(MainWindow.instance())

    metaS = MySqlMetadataSupplier(_conn, "drzava", "nosqlproject02")
    metaS.extract()

    rdba = RelDBActions(_conn, metaS.extract())

    print(rdba.insert({"DR_OZNAKA": "T", "DR_NAZIV": "treca"}))
    print(rdba.update({"DR_NAZIV": "Oman", "DR_OZNAKA": "O"}))
    # print(rdba.filter({"DR_NAZIV": "a"}))
    # print("\n search result =\n")
    print(rdba.filter({"DR_NAZIV": "a"}))
    # rdba.delete({"DR_NAZIV": "", "DR_OZNAKA": ""})
