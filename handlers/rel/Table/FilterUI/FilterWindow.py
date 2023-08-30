from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QHBoxLayout, QLineEdit, QLabel, QWidget, QPushButton
from handlers.rel.mysql.Connection.UI.statusBar import StatusBar

class FilterWindow(QDialog):
    def __init__(self, parent, columns, clb, default, fixed):
        super().__init__(parent)
        self.statusBar = StatusBar(self)
        self.columns = columns
        self.clb = clb
        self.exactColumns = []

        self.setWindowTitle("Filter table")
        self.setMinimumWidth(400)

        self.mainVLayout = QVBoxLayout()
        self.gridLayout = QGridLayout()
        self.buttonHLayout = QHBoxLayout()

        fields = QWidget(self)

        if(self.columns):
            for i, column in enumerate(self.columns):

                label = self.getLabel(column)

                setattr(self, label, QLineEdit(self))
                self.gridLayout.addWidget(QLabel(f"{label} : ", self), i, 1)
                self.gridLayout.addWidget(getattr(self, label), i, 2)

                self.exact_btn = QPushButton(QIcon(), "Exact")
                self.exact_btn.setStyleSheet("padding: 2px 5px;")
                self.exact_btn.clicked.connect(lambda text, col=column: self.exact(col))
                self.gridLayout.addWidget(self.exact_btn, i, 3)

                placeholder_text = f"Enter {label} here"
                getattr(self, label).setPlaceholderText(placeholder_text)

                default_label = self.get_code_name(label)
                if default_label in default and fixed:
                    getattr(self, label).setText(str(default[default_label]))
                    getattr(self, label).setEnabled(False)
                
                getattr(self, label).textChanged.connect(lambda text, col=column: self.validateColumn(text, col))
        else:
            self.gridLayout.addWidget(QLabel("Error, no columns found !!"))
        
        fields.setLayout(self.gridLayout)

        self.buttonHLayout = QHBoxLayout()

        self.filter_btn = QPushButton(QIcon("assets/img/icon8/Fluent/icons8-search-32.png"), "Filter")
        self.filter_btn.clicked.connect(lambda: [self.filter()])

        self.cancel_clear = QPushButton(QIcon("assets/img/icon8/Fluent/icons8-reset-32.png"), "Clear")
        self.cancel_clear.clicked.connect(lambda: ([self.clear()]))

        if(self.columns):
            self.buttonHLayout.addWidget(self.filter_btn)
        self.buttonHLayout.addWidget(self.cancel_clear)

        self.mainVLayout.addWidget(fields)
        self.mainVLayout.addLayout(self.buttonHLayout)
        self.mainVLayout.addWidget(self.statusBar)

        self.setLayout(self.mainVLayout)
        self.show()

    def getLabel(self, column):
        return str(column.label.strip() or column.code_name)
    
    def exact(self, column):
        sender = self.sender()
        label = self.getLabel(column)

        if label in self.exactColumns:
            sender.setStyleSheet("padding: 2px 5px;")
            self.exactColumns.remove(label)
        else:
            sender.setStyleSheet("background-color: #8bc34a; padding: 2px 5px;")
            self.exactColumns.append(label)

    def filter(self):
        items = {}
        searchItems = {}

        if(self.validateColumns()):
            for i, column in enumerate(self.columns):
                label = self.getLabel(column)
                column_value = getattr(self, label).text()
                items[label] = column_value

            if all(value == '' for value in items.values()):
                self.showMessage("All fields are empty !!")
                return
            
            for key, value in items.items():
                exact = key in self.exactColumns
                if(value != ""):
                    code_name = self.get_code_name(key)
                    searchItems[code_name] = {"value": value, "exact": exact}
            
            self.clb(searchItems)

    def clear(self):
        for column in self.columns:
            field = getattr(self, self.getLabel(column))
            if field.isEnabled():
                field.setText("")

    def showMessage(self, msg):
        self.statusBar.show()
        self.statusBar.showMessage(msg, 10000)

    def validateColumns(self):
        for i, column in enumerate(self.columns):
            label = self.getLabel(column)

            column_value = getattr(self, label).text()

            if(self.validateColumnType(column, column_value) == False):
                return False

            if(column.max_l != None):
                if(column.max_l < len(column_value)):
                    self.showMessage("The {} field must not have more than {} characters !!".format(label, column.max_l))
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

        self.showMessage("")
        
        if(self.validateColumnType(column, value) == False):
            return False

        if(column.max_l != None):
            if(column.max_l < len(value)):
                self.showMessage("The {} field must not have more than {} characters !!".format(self.getLabel(column), column.max_l))

    def get_code_name(self, label):
        for item in self.columns:
            if item.label == label:
                return item.code_name
        return label
