from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QHBoxLayout, QLineEdit, QLabel, QWidget, QPushButton
from handlers.rel.mysql.Connection.UI.statusBar import StatusBar
import mysql.connector

class RelDBExecuteProcedureWindow(QDialog):
    def __init__(self, clb, conn, procedure_metadata, procedure_name, default_values = []):
        super().__init__()
        self.statusBar = StatusBar(self)
        self.procedure_metadata = procedure_metadata
        self.procedure_name = procedure_name
        self.conn = conn
        self.clb = clb

        self.setWindowTitle("MySql Execute Procedure")
        self.setMinimumWidth(400)

        self.mainVLayout = QVBoxLayout()
        self.gridLayout = QGridLayout()
        self.buttonHLayout = QHBoxLayout()

        fields = QWidget(self)

        if(len(self.procedure_metadata) > 0):
            for i, column in enumerate(self.procedure_metadata):     
                label = column[0]

                setattr(self, label, QLineEdit(self))
                self.gridLayout.addWidget(QLabel(f"{label} : ", self), i, 1)
                self.gridLayout.addWidget(getattr(self, label), i, 2)

                placeholder_text = f"Enter {label} here"
                getattr(self, label).setPlaceholderText(placeholder_text)

                if i < len(default_values):
                    default_value = default_values[i]
                    if not isinstance(default_value, str):
                        default_value = str(default_value)
                    getattr(self, label).setText(default_value)
        else:
            self.gridLayout.addWidget(QLabel("Error, no metadata found !!"))
        
        fields.setLayout(self.gridLayout)

        self.buttonHLayout = QHBoxLayout()

        self.save_btn = QPushButton(QIcon("assets/img/icon8/Fluent/icons8-save-32.png"), "Execute")
        self.save_btn.clicked.connect(lambda: [self.execute()])

        self.cancel_btn = QPushButton(QIcon(), "Cancel")
        self.cancel_btn.clicked.connect(lambda: ([self.close()]))

        if(len(self.procedure_metadata) > 0):
            self.buttonHLayout.addWidget(self.save_btn)
        self.buttonHLayout.addWidget(self.cancel_btn)

        self.mainVLayout.addWidget(fields)
        self.mainVLayout.addLayout(self.buttonHLayout)
        self.mainVLayout.addWidget(self.statusBar)

        self.setLayout(self.mainVLayout)
        self.show()

    def execute(self):
        arguments = []
        
        if(self.validateColumns()):
            for i, column in enumerate(self.procedure_metadata):
                arguments.append(getattr(self, column[0]).text())

            try:
                _conn = self.conn.get_connection()
                cursor = _conn.cursor()

                cursor.callproc(self.procedure_name, arguments)
                _conn.commit()

                if cursor.stored_results():
                    result_set = cursor.stored_results()
                    results = list(result_set)

                    if len(results) > 0:
                        for result in results:
                            all_results = []
                            for row in result:
                                all_results.append(row)

                            if(len(all_results) == 0):
                                self.showMessage("No results !!")
                                return
                            
                            self.clb(all_results)
                    else:
                        cursor.execute("SELECT * FROM {}".format('temp_table'))
                        temp_table_results = cursor.fetchall()

                        if len(temp_table_results) == 0:   
                            self.showMessage("No results !!")
                            return 
                    
                        self.clb(temp_table_results)

                cursor.close()
                _conn.close()

            except mysql.connector.Error as error:
                self.showMessage("Error while executing procedure: {}".format(error))


    def showMessage(self, msg):
        self.statusBar.show()
        self.statusBar.showMessage(msg, 10000)

    def showColumnIcon(self, column):
        if(column.primary and column.foreign):
            return QLabel(self, pixmap=QPixmap("assets/img/primary_foreign_key.png").scaled(35, 20))
        elif(column.primary):
            return QLabel(self, pixmap=QPixmap("assets/img/primary-key.png").scaled(20, 20))
        elif(column.foreign):
           return QLabel(self, pixmap=QPixmap("assets/img/foreign-key.png").scaled(20, 20))
        else:
            return QLabel()

    def validateColumns(self):
        for i, column in enumerate(self.procedure_metadata):
            label = column[0]

            column_value = getattr(self, label).text()

            if(self.validateColumnType(column, column_value) == False):
                return False
            
        self.showMessage("")
        return True
    
    def validateColumnType(self, column, value):
        valid = True
        label = column[0]

        if(value):
            column_type = column[1].decode('utf-8')
            if(column_type == "int"):
                if(not value.isdigit()):
                    valid = False
                    self.showMessage("The {} field is not valid, it has to be a type {} !!".format(label, column_type))

            if(column_type == "float"):
                try:
                    if(not float(value)):
                        valid = False
                        self.showMessage("The {} field is not valid, it has to be a type float !!".format(label, column_type))
                except ValueError:
                    valid = False
                    self.showMessage("The {} field is not valid, it has to be a type float !!".format(label, column_type))  
        
        return valid