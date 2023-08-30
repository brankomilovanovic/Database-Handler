from PyQt5.QtCore import QJsonDocument
from PyQt5.QtWidgets import QWidget, QTextEdit

from PyQt5.QtGui import QColor
import json
from bson import json_util

class DocumentView(QTextEdit):
    def __init__(self, parent, cursor=None):
        super().__init__(parent)
        self.cursor = cursor

        list_cursor = list(self.cursor)
        text = json.dumps(list_cursor, indent=4, default=str)

        data = json.loads(text)
        
        self.insertPlainText(text)  
        # self.insertPlainText(f'<span style="color: {color};">{text}</span>') 

        self.setReadOnly(True) 
