from PyQt5.QtWidgets import QWidget

from handlers.rel.Workspace.RelDbWorkspaceView import RelDbWorkspaceView
from handlers.rel.mysql.Connection.UI.RelDBExecuteProcedureWindow import RelDBExecuteProcedureWindow
from handlers.rel.mysql.Connection.UI.RelDBFindProcedureWindow import RelDBFindProcedureWindow
from handlers.utils.Connection.ConnectionsListener import ConnectionsListener
from handlers.rel.mysql.Connection.mysqlconnection import MySqlConnection
from personal.PersonalMongoDB import PersonalMongoDB


class RelDBWorkspaceHandler:


    class RelDBConnectionListener(ConnectionsListener):

        def __init__(self, add_clb, remove_clb):
            
            self.add_clb = add_clb
            self.remove_clb = remove_clb

        def added(self, conn: MySqlConnection):
            self.add_clb(conn)

        def removed(self, conn: MySqlConnection):
            self.remove_clb(conn)

    def __init__(self):
        self.listener = RelDBWorkspaceHandler.RelDBConnectionListener(self.added, self.removed)
        self.workspace = RelDbWorkspaceView()

    def get_listener(self) -> ConnectionsListener:
        return self.listener

    # Prilikom dodavanja proveriti da li je konekcija vec ostvaran, napraiti connections lista koje su aktive.
    def added(self, conn: MySqlConnection):
        # TODO: Prof of concept / Srediti metodu i videti koji probelmi postije u ovom pristupu
        print(f"New connection is in workspace :{conn.name}")
        _conn = conn.get_connection()
    
        cursor = _conn.cursor()

        # cursor.execute("SHOW TABLES;")
        cursor.execute("SHOW DATABASES;")

        self.workspace.connName = conn.name
        for table_name in cursor:
            self.workspace.display_dbs([table_name[0]])

        

        cursor.close()
        _conn.close()
        self.workspace.loadSchema.clicked.connect(lambda: self.fill_tab(conn))
        self.workspace.loadProcedure.clicked.connect(lambda: self.find_procedure(conn))

    def removed(self, conn: MySqlConnection):
        print(f"{conn.name} Connection is removed")

    def get_workspace(self) -> QWidget:
        return self.workspace

    def find_procedure(self, conn):
        def clb(value, procedure):
            if len(value) > 0:
                f.close()
                self.exec_procedure(conn, value, procedure)

        f = RelDBFindProcedureWindow(clb, conn)
        f.exec()
    
    def exec_procedure(self, conn, procedure_values, procedure_name):
        def clb(value):
            if len(value) > 0:
                if(procedure_name == 'BrankoPersonalFindSoftwareProcessProcedure'):
                    PersonalMongoDB(value, conn)
                f.close()

        f = RelDBExecuteProcedureWindow(clb, conn, procedure_values, procedure_name)
        f.exec()

    def fill_tab(self, conn: MySqlConnection):
        table_list = []
        _conn = conn.get_connection()
        cursor = _conn.cursor()
        table_schema = self.workspace.comboBox.currentText()
        cursor.execute("SELECT * FROM information_schema.tables WHERE table_schema = %s", (table_schema,))
        for table_name in cursor:
            table_list.append(table_name[2])

        self.workspace.load_schema(table_list)
        cursor.close()
        _conn.close()
    
        
    

