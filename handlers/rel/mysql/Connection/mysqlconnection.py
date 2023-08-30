import mysql.connector
from typing import Union

from PyQt5.QtWidgets import QWidget, QMessageBox, QInputDialog, QLineEdit
from multimethod import multimethod
from mysql.connector import Error
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection

from handlers.rel.mysql.Connection.connection_template import CONNECTION_T
from handlers.utils.Connection.Connection import Connection


class MySqlConnection(Connection):
    @multimethod
    def __init__(self, conn: Union[dict, None] = None):
        self.new = False
        if conn is None:
            self.new = True
            conn = CONNECTION_T()

        self.name = conn["name"]
        self.method = conn["method"]
        self.hostname = conn["hostname"]
        self.port = conn["port"]
        self.user = conn["user"]
        self.schema = conn["schema"]

        self._saved = self.make_dict() if not self.new else None

        self._conn = None
        self._pool = None

    # def __init__(self):
    #

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.method != other.method:
            return False
        if self.hostname != other.hostname:
            return False
        if self.port != other.port:
            return False
        if self.user != other.user:
            return False
        if self.schema != other.schema:
            return False

        return True

    def __str__(self):
        details = ""

        details += f"  Name: {self.name}"
        details += f"    User: {self.user}"
        details += f"    Hostname: {self.hostname}"
        details += f"    Port: {self.port}"
        details += f"    Schema: {self.name}"
        details += f"    Methods: {self.method}"

        return details
    def make_dict(self):
        return {
            "name": self.name,
            "method": self.method,
            "hostname": self.hostname,
            "port": self.port,
            "user": self.user,
            "schema": self.schema
        }

    def connect(self, parent: QWidget) -> bool:
        try:
            password = self._enter_password_dialog(parent=parent)
            if not password:
                return False
            print(password)

            self._conn = mysql.connector.connect(host=self.hostname,
                                                 database=self.schema,
                                                 user=self.user,
                                                 password=password)
            if self._conn.is_connected():
                return True

        except Error as e:
            print(e)
            if e.errno == 1045:
                if self._not_valid_password_msg_box(parent) == QMessageBox.Retry:
                    return self.connect(parent)
                return False

        finally:
            ...

    def make_pool_party(self, parent: QWidget, party_name: str = None) -> bool:
        if party_name is None:
            party_name = f'{self.name}/{self.user}@{self.hostname}:{self.port}-{self.schema}'
        try:
            password = self._enter_password_dialog(parent=parent)
            if not password:
                return False

            self._pool = MySQLConnectionPool(pool_name=party_name,
                                             pool_size=32,
                                             database=self.schema,
                                             user=self.user,
                                             password=password)
            return True
        except Error as e:
            if e.errno == 1045:
                if self._not_valid_password_msg_box(parent) == QMessageBox.Retry:
                    return self.make_pool_party(parent, party_name)
                return False

    def get_connection(self) -> PooledMySQLConnection | bool:
        if self._pool is not None:
            return self._pool.get_connection()

        if self._conn is not None:
            return self._conn
        else:
            return False

    def close(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

        if self._pool is not None:
            self._pool.close()
            self._pool = None


    #
    # def _not_valid_password_msg_box(self, parent: QWidget) -> bool:
    #     return QMessageBox(QMessageBox.Icon.Warning,
    #                        f"Invalid password",
    #                        f"The password you entered for user {self.user}, is not valid",
    #                        (QMessageBox.Cancel | QMessageBox.Retry),
    #                        parent).exec()
    #
    # def _enter_password_dialog(self, parent: QWidget) -> str:
    #     password, ok = QInputDialog.getText(parent,
    #                                         'Password',
    #                                         f"Enter a password for {self.user}: ",
    #                                         QLineEdit.Password)
    #
    #     return password if ok else False

    def connected(self):
        return self._conn is not None or self._pool is not None


    def restore(self):
        self.name = self._saved["name"]
        self.method = self._saved["method"]
        self.hostname = self._saved["hostname"]
        self.port = self._saved["port"]
        self.user = self._saved["user"]
        self.schema = self._saved["schema"]

    '''def _changed(self):
        print("vise nije sacuavno 1")
        self.saved = False

    def _critical_change(self):
        print("vise nije sacuavno2")
        self.saved = False
        self.test = False

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_value):
        self._critical_change()
        self._name = new_value

    @property
    def method(self):
        return self._method

    @method.setter
    def method(self, new_value):
        self._critical_change()
        self._method = new_value

    @property
    def hostname(self):
        return self._hostname

    @hostname.setter
    def hostname(self, new_value):
        self._critical_change()
        self._hostname = new_value

    @property
    def port(self):
        return self._port

    @port.setter
    def port(self, new_value):
        self._critical_change()
        self._port = new_value

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, new_value):
        self._critical_change()
        self._user = new_value

    @property
    def schema(self):
        return self._schema

    @schema.setter
    def schema(self, new_value):
        self._critical_change()
        self._schema = new_value'''
