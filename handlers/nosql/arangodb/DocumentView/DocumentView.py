import json
from PyQt5.QtCore import QJsonDocument
from PyQt5.QtWidgets import QWidget, QTextEdit

class DocumentView(QTextEdit):
    def __init__(self, parent, cursor=None):
        super().__init__(parent)
        self.cursor = cursor

        # json_object = QJsonObject(self.json)
        # jsonDoc = QJsonDocument(self.json)
        # jsonString = doc.toJson(QJsonDocument.Indented)

        # Create QVariantMap and populate it
        # qvariant_map = QVariantMap(data_dict)

        # Create QJsonDocument from QVariantMap
        # json_document = QJsonDocument(qvariant_map)

        # Print the JSON document
        # print(json_document.toJson())
        self.setPlainText("".join(str(c) for c in self.cursor))
