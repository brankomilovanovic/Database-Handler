from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QHBoxLayout, QLineEdit, QLabel, QWidget, QPushButton
from handlers.rel.mysql.Connection.UI.statusBar import StatusBar

class UpdateWindow(QDialog):
    def __init__(self, parent, columns, clb, default, fixed, selectedRow):
        super().__init__(parent)
        self.statusBar = StatusBar(self)
        self.columns = columns
        self.clb = clb

        self.setWindowTitle("Update")
        self.setMinimumWidth(400)

        self.mainVLayout = QVBoxLayout()
        self.gridLayout = QGridLayout()
        self.buttonHLayout = QHBoxLayout()

        fields = QWidget(self)

        if(self.columns):
            for i, column in enumerate(self.columns):  
                                
                label = self.getLabel(column)

                setattr(self, label, QLineEdit(self))
                self.gridLayout.addWidget(self.showColumnIcon(column), i, 0, Qt.AlignRight)
                self.gridLayout.addWidget(QLabel(f"{label} : ", self), i, 1)
                self.gridLayout.addWidget(getattr(self, label), i, 2)

                placeholder_text = f"Enter {label} here"
                getattr(self, label).setPlaceholderText(placeholder_text)

                default_label = self.get_code_name(label)
                if default_label in default and fixed:
                    getattr(self, label).setText(str(selectedRow[default_label]) if selectedRow[default_label] else str(default[default_label]))
                    getattr(self, label).setEnabled(False)

                if default_label in selectedRow:
                    getattr(self, label).setText(str(selectedRow[default_label]))
                    if(column.primary):
                        getattr(self, label).setEnabled(False)

                getattr(self, label).textChanged.connect(lambda text, col=column: self.validateColumn(text, col))
        else:
            self.gridLayout.addWidget(QLabel("Error, no columns found !!"))
        
        fields.setLayout(self.gridLayout)

        self.buttonHLayout = QHBoxLayout()

        self.save_btn = QPushButton(QIcon("assets/img/icon8/Fluent/icons8-save-32.png"), "Save")
        self.save_btn.clicked.connect(lambda: [self.save()])

        self.cancel_btn = QPushButton(QIcon(), "Cancel")
        self.cancel_btn.clicked.connect(lambda: ([self.close()]))

        if(self.columns):
            self.buttonHLayout.addWidget(self.save_btn)
        self.buttonHLayout.addWidget(self.cancel_btn)

        self.mainVLayout.addWidget(fields)
        self.mainVLayout.addLayout(self.buttonHLayout)
        self.mainVLayout.addWidget(self.statusBar)

        self.setLayout(self.mainVLayout)
        self.show()

    def getLabel(self, column):
        return str(column.label.strip() or column.code_name)

    def save(self):
        newItem = {}
        
        if(self.validateColumns()):
            for i, column in enumerate(self.columns):
                label = self.getLabel(column)
                column_value = getattr(self, label).text()
                code = self.get_code_name(label)
                newItem[code] = column_value

            self.clb(newItem)

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
        for i, column in enumerate(self.columns):
            label = self.getLabel(column)

            column_value = getattr(self, label).text()

            if(self.validateColumnType(column, column_value) == False):
                return False

            if(column.notnull == False):
                if(column_value == ""):
                    self.showMessage("The '{}' field must be filled out !!".format(label))
                    return False

            if(column.max_l != None):
                if(column.max_l < len(column_value)):
                    self.showMessage("The {} field must not have more than {} characters!!".format(label, column.max_l))
                    return False
            
        self.showMessage("")
        return True
    
    def validateColumnType(self, column, value):
        valid = True
        label = self.getLabel(column)

        if(value):
            if(column.type == "int"):
                if(not value.isdigit()):
                    valid = False
                    self.showMessage("The {} field is not valid, it has to be a type {} !!".format(label, column.type))

            if(column.type == "float"):
                try:
                    if(not float(value)):
                        valid = False
                        self.showMessage("The {} field is not valid, it has to be a type float !!".format(label, column.type))
                except ValueError:
                    valid = False
                    self.showMessage("The {} field is not valid, it has to be a type float !!".format(label, column.type))  
        
        return valid
        
    def validateColumn(self, value, column):
        label = self.getLabel(column)
        self.showMessage("")
        
        if(self.validateColumnType(column, value) == False):
            return False

        if(column.notnull == False):
            if(value == ""):
                self.showMessage("The '{}' field must be filled out !!".format(label))

        if(column.max_l != None):
            if(column.max_l < len(value)):
                self.showMessage("The {} field must not have more than {} characters!!".format(label, column.max_l))

    def get_code_name(self, label):
        for column in self.columns:
            if column.label == label:
                return column.code_name
        return label
    
    def get_label_by_code_name(self, code_name):
        for column in self.columns:
            if column.code_name == code_name:
                return self.getLabel(column)
        return column.code_name
