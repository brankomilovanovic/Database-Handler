from pymongo import MongoClient
from bson import ObjectId
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QHBoxLayout, QComboBox, QLabel, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from handlers.rel.mysql.Connection.UI.RelDBExecuteProcedureWindow import RelDBExecuteProcedureWindow
from handlers.rel.mysql.Connection.UI.statusBar import StatusBar
import mysql.connector
from pyArango.connection import *
from personal.MongoToArangoMigrator import MongoToArangoMigrator

class PersonalMongoDB(QDialog):
    def __init__(self, procedure_results, conn):
        super().__init__()
        self.statusBar = StatusBar(self)
        self.procedure_results = procedure_results
        self.conn = conn
        self.procedure_name = 'BrankoPersonalFetchSoftwareProcessProcedure'

        self.setWindowTitle("Branko Personal - Select software process")
        self.setMinimumWidth(600)

        self.mainVLayout = QVBoxLayout()
        self.gridLayout = QGridLayout()
        self.buttonHLayout = QHBoxLayout()

        fields = QWidget(self)

        self.select_software_process = QComboBox()
        for item in self.procedure_results:
            selected_values = {
                'id_procesa': str(item[2]),
                'drzava': str(item[1]),
                'naziv_procesa': str(item[3]),
                'nazvi_subjekta': str(item[5])
            }
            self.select_software_process.addItem(', '.join(f'{value}' for key, value in selected_values.items()))
            
        self.gridLayout.addWidget(self.select_software_process)
        
        fields.setLayout(self.gridLayout)

        self.buttonHLayout = QHBoxLayout()

        self.save_btn = QPushButton(QIcon("assets/img/icon8/Fluent/icons8-save-32.png"), "Execute")
        self.save_btn.clicked.connect(lambda: [self.execute()])

        self.cancel_btn = QPushButton(QIcon(), "Cancel")
        self.cancel_btn.clicked.connect(lambda: ([self.close()]))

        self.buttonHLayout.addWidget(self.save_btn)
        self.buttonHLayout.addWidget(self.cancel_btn)

        self.mainVLayout.addWidget(fields)
        self.mainVLayout.addLayout(self.buttonHLayout)
        self.mainVLayout.addWidget(self.statusBar)

        self.setLayout(self.mainVLayout)
        self.show()
    
    def execute(self):
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
            cursor.execute(query, ('nosql', self.procedure_name))
            rows = cursor.fetchall()

            if len(rows) == 0:
                self.showMessage("This procedure '{}' does not exist".format(self.procedure_name))
            else:
                self.hide()
                self.fetch_document(rows)

        except mysql.connector.Error as error:
                self.showMessage("Error while procedure procedure: {}".format(error))

        cursor.close()
        _conn.close()

    def find_document(self, target_item):
        for item in self.procedure_results:
            if int(item[2]) == int(target_item[0]):
                return item
        return None

    
    def fetch_document(self, rows):
        selected_document = self.find_document(self.select_software_process.currentText().strip().split(", "))
        if(selected_document):
            default_values = [selected_document[0], selected_document[4], selected_document[2], selected_document[3]]
            def clb(value):
                if(len(value) > 0):
                    self.select_document(value)
                    f.close()

            f = RelDBExecuteProcedureWindow(clb, self.conn, rows, self.procedure_name, default_values)
            f.exec()

    def select_document(self, value):
        self.select_software_process.clear()
        for item in value:
            self.select_software_process.addItem(', '.join(str(value) for value in item))

        self.save_btn.clicked.disconnect()
        self.save_btn.clicked.connect(lambda: self.generate_document())
        self.save_btn.setText("Generate Document")
        self.setWindowTitle("Branko Personal - Choose document")

        self.show()

    def showMessage(self, msg):
        self.statusBar.show()
        self.statusBar.showMessage(msg, 10000)

    def fetch_projects(self, proces_id):
        _conn = self.conn.get_connection()
        cursor = _conn.cursor()
        sql = f"SELECT TIPP_D, PROJ_ID, PROJ_REVIZIJA, PROJ_NAZIV, PROJ_DATOKON, PROJ_STVARNI_ZAVRSETAK, ID_PROCESA FROM nosql.projekat_realizacije_softvera WHERE ID_PROCESA = {proces_id}"
        cursor.execute(sql)
        projekti = cursor.fetchall()
        cursor.close()
        _conn.close()
        return projekti

    def generate_document(self):
        if(self.select_software_process.currentText()):
            document = self.select_software_process.currentText().strip().split(", ")
            projekti = self.fetch_projects(document[2])

            document.extend(projekti[0])

            print(document)

            client = MongoClient("mongodb://localhost:27017")
            db = client["nosql"]

            # if "personal_branko" in db.list_collection_names():
            #     db["personal_branko"].drop()

            collection = db["personal_branko"]

            generated_document = {
                "_id": ObjectId(),
                "naslov": {
                    "_id": ObjectId(),
                    "naslov1": "Dokument koji sadrzi strukturu aktivnosti za zadati",
                    "naslov2": f"model procesa {document[0]}, {document[1]}, {document[2]}, {document[3]}"
                },
                "softverski_proces": {
                    "_id": ObjectId(),
                    "drzava": document[0],
                    "kompanija": document[1],
                    "id_procesa": document[2],
                    "naziv_modela": document[3],
                    "struktura_procesa": {
                        "_id": ObjectId(),
                        "aktivnosti": document[4],
                        "verzija": document[5],
                        "struktura_aktivnosti": {
                            "_id": ObjectId(),
                            "datum_formiranja": document[6],
                            "naziv_aktivnosti": document[7],
                            "projekti": []
                        }
                    }
                }
            }

            for projekat in projekti:
                projekat_document = {
                    "_id": ObjectId(),
                    "tip_projekta": projekat[0],
                    "id_projekta": projekat[1],
                    "revizija": projekat[2],
                    "naziv": projekat[3],
                    "planirani_zavrsetak": projekat[4].isoformat(),
                    "stvarni_zavrsetak": projekat[5].isoformat(),
                    "id_procesa": projekat[6],
                }

                generated_document["softverski_proces"]["struktura_procesa"]["struktura_aktivnosti"]["projekti"].append(projekat_document)

            collection.insert_one(generated_document)
            client.close()

            migrator = MongoToArangoMigrator("mongodb://localhost:27017", "nosql", "http://localhost:8529", "root", "root", "nosql")
            migrator.migrate_mongodb_to_arangodb("personal_branko")
            
            self.close()