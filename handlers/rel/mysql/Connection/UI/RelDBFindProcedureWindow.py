from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QHBoxLayout, QLineEdit, QLabel, QPushButton, QWidget, QComboBox
from handlers.rel import mysql

from handlers.rel.mysql.Connection.UI.statusBar import StatusBar

class RelDBFindProcedureWindow(QDialog):
    def __init__(self, clb, conn):
        super().__init__()
        self.statusBar = StatusBar(self)
        self.clb = clb
        self.conn = conn

        self.setWindowTitle("MySql Find Procedure")
        self.setMinimumWidth(500)

        self.mainVLayout = QVBoxLayout()
        self.formLayout = QFormLayout()
        self.buttonHLayout = QHBoxLayout()

        _conn = self.conn.get_connection()
        cursor = _conn.cursor()
        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()
        database_names = [db[0] for db in databases]
        cursor.close()
        _conn.close()

        self.database = QComboBox(self)
        self.database.label = "Baza podataka"
        self.database.addItems(database_names)
        self.formLayout.addRow(QLabel(self.database.label + ": ", self), self.database)
        if conn.schema != '' and conn.schema in database_names:
            index = self.database.findText(conn.schema)
            self.database.setCurrentIndex(index)
        self.database.currentIndexChanged.connect(lambda: self.populate_procedures(self.database.currentText()))

        self.procedura = QComboBox(self)
        self.procedura.label = "Procedura"
        self.formLayout.addRow(QLabel(self.procedura.label + ": ", self), self.procedura)

        self.execute_btn = QPushButton(QIcon(), "Execute")
        self.execute_btn.clicked.connect(self.save)
        self.execute_btn.setFixedHeight(30)

        self.cancel_btn = QPushButton(QIcon(), "Cancel")
        self.cancel_btn.clicked.connect(self.close)
        self.cancel_btn.setFixedHeight(30)

        self.buttonHLayout.addWidget(self.execute_btn)
        self.buttonHLayout.addWidget(self.cancel_btn)

        self.change_choose_procedure = QPushButton(QIcon(), "Unesite rucno proceduru")
        self.change_choose_procedure.clicked.connect(lambda: self.change_procedure_select(QLineEdit()))
        self.change_choose_procedure.setFixedHeight(30)

        self.formLayout.addRow("", self.change_choose_procedure)

        self.populate_procedures(conn.schema)

        fields = QWidget()
        fields.setLayout(self.formLayout)

        self.mainVLayout.addWidget(fields)
        self.mainVLayout.addLayout(self.buttonHLayout)
        self.mainVLayout.addWidget(self.statusBar)

        self.setLayout(self.mainVLayout)

    def change_procedure_select(self, field):
        self.formLayout.removeRow(self.procedura)
        self.formLayout.removeRow(self.change_choose_procedure)

        self.procedura = field
        self.procedura.label = "Procedura"
        self.formLayout.addRow(QLabel(self.procedura.label + ": ", self), self.procedura)

        if isinstance(field, QLineEdit):
            self.change_choose_procedure = QPushButton(QIcon(), "Odaberite sacuvanu proceduru")
            self.change_choose_procedure.clicked.connect(lambda: self.change_procedure_select(QComboBox()))
            self.change_choose_procedure.setFixedHeight(30)
        else:
            self.change_choose_procedure = QPushButton(QIcon(), "Unesite rucno proceduru")
            self.change_choose_procedure.clicked.connect(lambda: self.change_procedure_select(QLineEdit()))
            self.change_choose_procedure.setFixedHeight(30)
            self.populate_procedures(self.database.currentText().strip())

        self.formLayout.addRow("", self.change_choose_procedure)

    def populate_procedures(self, database):
        if(database and isinstance(self.procedura, QComboBox)):
            self.procedura.clear() 

            _conn = self.conn.get_connection()
            cursor = _conn.cursor()
            cursor.execute("SHOW PROCEDURE STATUS WHERE Db = %s", (database,))
            procedures = cursor.fetchall()
            procedure_names = [procedure[1] for procedure in procedures]

            for procedure_name in procedure_names:
                self.procedura.addItem(procedure_name)

            cursor.close()
            _conn.close()

    def save(self):
        procedure = {}
        fields = {
            'database': self.database,
            'procedura': self.procedura
        }

        for field_name, field in fields.items():
            if isinstance(field, QComboBox):
                value = field.currentText().strip()
            else:
                value = field.text().strip()
            procedure[field_name.lower()] = value

        empty_fields = [fields[field_name].label for field_name, value in procedure.items() if value == '']
        if empty_fields:
            self.showMessage("The following fields must be filled out: {}".format(", ".join(empty_fields)))
            return
        
        self.fetchProcedure(procedure)

    def fetchProcedure(self, procedure):
        _conn = self.conn.get_connection()
        cursor = _conn.cursor()

        query = """
            SELECT
                PARAMETER_NAME,
                DATA_TYPE
            FROM
                information_schema.PARAMETERS
            WHERE
                SPECIFIC_SCHEMA = %s
                AND SPECIFIC_NAME = %s
            ORDER BY
                ORDINAL_POSITION
        """

        try:
            cursor.execute(query, (procedure['database'], procedure['procedura']))
            rows = cursor.fetchall()

            if len(rows) == 0:
                self.showMessage("This procedure '{}' does not exist".format(procedure['procedura']))
            else:
                self.clb(rows, procedure['procedura'])

        except:
            self.showMessage("Error fetch procedure information: {}".format(procedure['procedura']))

        cursor.close()
        _conn.close()

    def showMessage(self, msg):
        self.statusBar.show()
        self.statusBar.showMessage(msg, 10000)
