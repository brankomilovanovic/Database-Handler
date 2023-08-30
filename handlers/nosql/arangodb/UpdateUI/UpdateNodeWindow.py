from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QHBoxLayout, QLineEdit, QLabel, QWidget, QPushButton, QTextEdit, QComboBox
from handlers.rel.mysql.Connection.UI.statusBar import StatusBar
import json

class UpdateNodeWindow(QDialog):
    def __init__(self, parent, selected_node, clb, collection_names):
        super().__init__(parent)
        self.statusBar = StatusBar(self)
        self.clb = clb
        self.selected_node = selected_node

        self.setWindowTitle("Add node")
        self.setMinimumWidth(400)

        self.mainVLayout = QVBoxLayout()
        self.gridLayout = QGridLayout()
        self.buttonHLayout = QHBoxLayout()

        fields = QWidget(self)

        self.collectionName = QComboBox(self)
        self.collectionName.addItems(collection_names)
        self.collectionName.setCurrentText(self.selected_node['collectionName']) if self.selected_node['collectionName'] is not None else None
        self.collectionName.label = "Collection name"
        self.gridLayout.addWidget(QLabel(self.collectionName.label + ": ", self), 0, 0, Qt.AlignRight)
        self.gridLayout.addWidget(self.collectionName, 0, 1)
        self.collectionName.setEnabled(False)

        self._key = QLineEdit(self)
        self._key.label = "Key"
        self._key.setEnabled(False)
        self._key.setText(self.selected_node['_key']) if self.selected_node['_key'] is not None else None
        self.gridLayout.addWidget(QLabel(self._key.label + ": ", self), 1, 0, Qt.AlignRight)
        self.gridLayout.addWidget(self._key, 1, 1)

        self.document = QTextEdit(self)
        self.document.label = "Document body"
        self.document.setText(json.dumps(self.selected_node['document'], indent=4)) if self.selected_node['document'] is not None else None
        self.gridLayout.addWidget(QLabel(self.document.label + ": ", self), 2, 0, Qt.AlignRight)
        self.gridLayout.addWidget(self.document, 2, 1, 3, 1)

        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setRowStretch(2, 1)

        fields.setLayout(self.gridLayout)

        self.buttonHLayout = QHBoxLayout()

        self.save_btn = QPushButton(QIcon("assets/img/icon8/Fluent/icons8-save-32.png"), "Save")
        self.save_btn.clicked.connect(lambda: [self.save()])
        self.save_btn.setFixedHeight(40)

        self.cancel_btn = QPushButton(QIcon(), "Cancel")
        self.cancel_btn.clicked.connect(lambda: ([self.close()]))
        self.cancel_btn.setFixedHeight(40)

        self.buttonHLayout.addWidget(self.save_btn)
        self.buttonHLayout.addWidget(self.cancel_btn)

        self.mainVLayout.addWidget(fields)
        self.mainVLayout.addLayout(self.buttonHLayout)
        self.mainVLayout.addWidget(self.statusBar)

        self.setLayout(self.mainVLayout)
        self.show()

    def save(self):
        items = {}
        fields = ['collectionName', '_key', 'document']

        for field in fields:
            obj = getattr(self, field)
            if field == 'collectionName':
                items[field] = self.collectionName.currentText()
            elif isinstance(obj, QLineEdit):
                items[field] = obj.text()
            elif field == 'document':
                try:
                    items[field] = json.loads(obj.toPlainText())
                except ValueError:
                    self.showMessage("Invalid JSON format in the '{}' field!!".format(obj.label))
                    return
            elif isinstance(obj, QTextEdit):
                items[field] = obj.toPlainText()

            if items[field] == "" and field != '_key' and field != 'collectionName':
                self.showMessage("The '{}' field must be filled out !!".format(obj.label))
                return
        
        newObject = {
            'collectionName': items['collectionName'],
            'key': items['_key'],
            'document': items['document']
        }    

        self.clb(newObject)
       
    def showMessage(self, msg):
        self.statusBar.show()
        self.statusBar.showMessage(msg, 10000)