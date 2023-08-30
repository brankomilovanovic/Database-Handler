from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QGridLayout, QHBoxLayout, QLineEdit, QLabel, QComboBox, QTabWidget, \
    QWidget, QPushButton

from assets.config.settings import CONNECTION_FORBIDDEN_NAMES
from handlers.nosql.mongodb.Connection.MongoDbConnection import MongoDbConnection
from handlers.nosql.mongodb.Connection.MongoDbConnections import MongoDbConnections
# from handlers.nosql.mongodb.Connection.MongoDbConnection import MongoDbConnection
# from handlers.nosql.mongodb.Connection.MongoDbConnections import MongoDbConnections
from handlers.rel.mysql.Connection.UI.DescriptionLabel import DescriptionLabel
from handlers.rel.mysql.Connection.UI.statusBar import StatusBar


# TODO: Dodati close dugme za zatvranje konekcija, i pri tome je izbaciti iz objekta Connections
# TODO: Konekcija se dodaje u objekat Connection samo kada je aktivirana, i to od strane spoljasnje komponente koja omogucava njeno otvrarenje i zatvaranje

class NewMongoDbConnectionWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.statusBar = StatusBar(self)
        self.connections = MongoDbConnections()
        # self.stored_connections = self.connections.stored_connections
        # self.connections.add(Connection())
        self._connection = MongoDbConnection()
        self._protocols = {
            0 : 'mongodb',
            1 : 'mongodb+srv'
        }

        self.setWindowTitle("Create new MongoDB Connectionconnection")
        self.setFixedWidth(800)
        self.setFixedHeight(600)
        # self.setStyleSheet(STYLES.newConnButtons)

        self.mainVLayout = QVBoxLayout()
        self.first = QGridLayout()
        self.parametersGridLayout = QGridLayout()
        self.buttonHLayout = QHBoxLayout()

        # NAME
        self.name_i = QLineEdit(self)
        self.name_i.textEdited.connect(
            lambda text1: [setattr(self.connection, 'name', text1),
                           self._update_savedConnections(),
                           self._update_buttons()])
        self.name_i.editingFinished.connect(lambda: [self.name_changed(self.name_i.text())])
        self.first.addWidget(QLabel("Connection name : ", self), 0, 0, Qt.AlignRight)
        self.first.addWidget(self.name_i, 0, 1)
        self.first.addWidget(DescriptionLabel("Type a name for connection", self), 0, 3)

        # # SAVED CONNECTIONS
        self.savedConnections = QComboBox(self)
        # ako je samo jedna konekcija, to znaci da ima samo trenutno editovana konekcija #TODO: Napraviti bolji mehanizam za ovaj problem
        # self.savedConnections.addItems([conn.name for conn in self.connections.stored_connections])
        # self.savedConnections.currentIndexChanged.connect(
        #     lambda index: [setattr(self, 'current_conn_index', index), self._update_buttons()])
        self.first.addWidget(QLabel("Saved connections : ", self), 1, 0, Qt.AlignRight)
        self.first.addWidget(self.savedConnections, 1, 1)
        self.first.addWidget(DescriptionLabel("Select from saved connections", self), 1, 3)

        # Protocl
        self.protocl_i = QComboBox(self)
        self.protocl_i.addItems([v for k, v in self._protocols.items()])
        # self.method_i.currentIndexChanged.connect(lambda text: setattr(self.connection, 'method', text))
        self.first.addWidget(QLabel("Connection protocol : ", self), 2, 0, Qt.AlignRight)
        self.first.addWidget(self.protocl_i, 2, 1)
        self.first.addWidget(DescriptionLabel("Protocol to use to connect to MongoDB server", self), 2, 3)


        tabs = QTabWidget(self)
        parameters = QWidget(self)

        # HOSTNAME
        self.hostname_i = QLineEdit(self)
        self.hostname_i.textEdited.connect(
            lambda text: [setattr(self.connection, 'hostname', text),
                          self._update_buttons()])
        # self.hostname_i.editingFinished.connect(self._update_buttons)
        self.parametersGridLayout.addWidget(QLabel("Hostname : ", self), 0, 0, Qt.AlignRight)
        self.parametersGridLayout.addWidget(self.hostname_i, 0, 1)
        self.parametersGridLayout.addWidget(DescriptionLabel("Name or IP address of server host", self), 0, 3)

        # PORT
        self.port_i = QLineEdit(self)
        self.port_i.textEdited.connect(
            lambda text: [setattr(self.connection, 'port', text),
                          self._update_buttons()])
        # self.port_i.editingFinished.connect(self._update_buttons)
        self.parametersGridLayout.addWidget(QLabel("Port : ", self), 1, 0, Qt.AlignRight)
        self.parametersGridLayout.addWidget(self.port_i, 1, 1)
        self.parametersGridLayout.addWidget(DescriptionLabel("TCP / IP port", self), 1, 3)


        # DATABASE
        self.database_i = QLineEdit(self)
        self.database_i.textEdited.connect(
            lambda text: [setattr(self.connection, 'database', text),
                          self._update_buttons()])
        # self.port_i.editingFinished.connect(self._update_buttons)
        self.parametersGridLayout.addWidget(QLabel("Database : ", self), 2, 0, Qt.AlignRight)
        self.parametersGridLayout.addWidget(self.database_i, 2, 1)
        self.parametersGridLayout.addWidget(DescriptionLabel("Default database", self), 2, 3)


        # CLUSTER URI
        self.clusteruri_i = QLineEdit(self)
        self.clusteruri_i.textEdited.connect(
            lambda text: [setattr(self.connection, 'cluster_uri', text),
                          self._update_buttons()])
        # self.port_i.editingFinished.connect(self._update_buttons)
        self.parametersGridLayout.addWidget(QLabel("Cluster URI : ", self), 3, 0, Qt.AlignRight)
        self.parametersGridLayout.addWidget(self.clusteruri_i, 3, 1)
        self.parametersGridLayout.addWidget(DescriptionLabel("Cluster URI", self), 2, 3)

        # USERNAME
        self.user_i = QLineEdit(self)
        self.user_i.textEdited.connect(
            lambda text: [setattr(self.connection, 'user', text), self._update_buttons()])
        # self.user_i.editingFinished.connect(self._update_buttons)
        self.parametersGridLayout.addWidget(QLabel("Username : ", self), 4, 0, Qt.AlignRight)
        self.parametersGridLayout.addWidget(self.user_i, 4, 1)
        self.parametersGridLayout.addWidget(DescriptionLabel("Name of the user to connect with : ", self), 4, 3)

        self.parametersGridLayout.setColumnStretch(0, 1)
        self.parametersGridLayout.setColumnStretch(1, 3)
        self.parametersGridLayout.setColumnStretch(2, 1)

        parameters.setLayout(self.parametersGridLayout)
        tabs.addTab(parameters, "Parameters")

        # BUTTON LAYOUT
        self.buttonHLayout = QHBoxLayout()

        # BUTTONS
        self.mock_btn = QPushButton()
        self.mock_btn.hide()

        self.save_as_btn = QPushButton(QIcon("assets/img/icon8/Fluent/icons8-save-32.png"), "Save As")
        self.save_as_btn.clicked.connect(lambda: [self.save_as(),
                                                  self._update_buttons(),
                                                  self._load_current_connections(),
                                                  self.set_last_index()])

        self.save_btn = QPushButton(QIcon("assets/img/icon8/Fluent/icons8-save-32.png"), "Save")
        self.save_btn.clicked.connect(lambda: [self.save()])

        self.connect_btn = QPushButton("Connect")
        self.connect_btn.clicked.connect(
            lambda: [self.connect()])

        self.test_btn = QPushButton(QIcon("assets/img/icon8/Fluent/icons8-test-tube-32.png"), "Test")
        self.test_btn.clicked.connect(lambda: ([self.connection.test(self)]))

        # BUTTONS LAYOUT SETUP
        self.buttonHLayout.addWidget(self.mock_btn)
        self.buttonHLayout.addWidget(self.test_btn)
        self.buttonHLayout.addWidget(self.connect_btn)
        self.buttonHLayout.addWidget(self.save_btn)
        self.buttonHLayout.addWidget(self.save_as_btn)

        # MAIN LAYOUT SETUP
        self.mainVLayout.addLayout(self.first)
        self.mainVLayout.addWidget(tabs)
        self.mainVLayout.addLayout(self.buttonHLayout)
        self.mainVLayout.addWidget(self.statusBar)

        # MAIN SET Up
        self.setLayout(self.mainVLayout)
        self.show()

        # CURRENT CONNECTION
        # self._current_conn_index = 0
        self._update_buttons()
        self._load_current_connections()

        # self.connection = self.connection.restore()
        self.savedConnections.currentIndexChanged.connect(
            lambda index: [setattr(self, 'current_conn_index', index), self._update_buttons()])

        self.protocl_i.currentIndexChanged.connect(
            lambda index: [setattr(self, 'current_protocol_index', index), self._update_buttons()])

        self.current_protocol_index = 0

        # SET UP PARAMETERS FOR NEW CONN
        # self.savedConnections.setCurrentIndex(self.current_conn_index)

    def _update_savedConnections(self, index=None, conn=None):
        ...

    # if index is None:
    #     index = self.current_conn_index
    # if conn is None:
    #     conn = self.connection
    #
    # self.savedConnections.setItemText(index,
    #                                   conn.name)

    def _set_conn_params(self, conn: MongoDbConnection):
        self.name_i.setText(conn.name)
        self.hostname_i.setText(conn.hostname)
        self.port_i.setText(conn.port)
        self.user_i.setText(conn.user)
        self.clusteruri_i.setText(conn.cluster_uri)
        self.database_i.setText(conn.database)
        self.protocl_i.setCurrentIndex(0 if conn.protocol == 'mongodb' else 1)

    def _update_buttons(self):
        try:
            if self.name_i.text() in CONNECTION_FORBIDDEN_NAMES:
                self.save_btn.setEnabled(False)
                self.save_btn.setToolTip(f"Connection with this name cannot be saved")
            elif self.connection.is_saved():
                self.save_btn.setEnabled(False)
                self.save_btn.setToolTip(f"There is not changes to be saved")
            else:
                self.save_btn.setEnabled(True)
                self.save_btn.setToolTip(f"Save changes to '{self.connection.name}'")

            if self.connection.connected():
                self.connect_btn.setIcon((QIcon("assets/img/icon8/Fluent/icons8-green-circle-32.png")))
            else:
                self.connect_btn.setIcon((QIcon("assets/img/icon8/Fluent/icons8-cloud-cross-32.png")))

            if self.connection.new or self.connection.name == self.connection._saved["name"]:
                self.save_as_btn.setEnabled(False)
                self.save_as_btn.setToolTip(f"Connection can't be saved as new connection if name is not changed")
            else:
                self.save_as_btn.setEnabled(True)
                self.save_as_btn.setToolTip(f"Save connection as '{self.connection.name}'")
        except:
            pass

    def name_changed(self, text):
        if self.connections.is_name_available(self.connection):
            return True
        else:
            self.showMessage("Name already exist, please pick another connection name !!")
            return False

    def save(self):
        # print ("Save connection: ", str(self.connection))
        if self.connection.name in CONNECTION_FORBIDDEN_NAMES:
            self.showMessage("Can not save connection without name, you must enter some name !!")
            return
        if self.name_changed(self.connection.name):
            # print("Saving self.connection", str(self.connection))
            # print("Saved connection", self.connection._saved)
            self.connections.save(self.connection)
            index = self.connections.get_index(self.connection)
            # self.connection = Connection(self.connection.make_dict())
            self._update_buttons()
            self._load_current_connections()
            self.savedConnections.setCurrentIndex(index)

            self.showMessage("Connection successfully saved ")

    def save_as(self):
        if self.connection.name in CONNECTION_FORBIDDEN_NAMES:
            self.showMessage("Can not save connection without name, you must enter some name !!")
            return
        # if not self.connections.is_name_available(self.connection.name):
        #     self.showMessage("Please enter unique connection name")
        #     return

        if self.name_changed(self.connection.name):
            # new_conn_from_current = Connection(self.connection.make_dict())
            # # self.connections.save(new_conn_from_current)
            # # self.connection.restore()
            #
            # self.connection = Connection(self.connection.make_dict())
            self.connections.save_as(self.connection)

            # self._update_savedConnections()

            self.showMessage("Connection successfully saved ")

            # self.savedConnections.addItems([self.connection.name])
            # self.savedConnections.setCurrentIndex(len(self.connections) - 1)

    def set_last_index(self):
        self.savedConnections.setCurrentIndex(len(self.connections.stored_connections) - 1)

    def showMessage(self, msg):
        self.statusBar.show()
        self.statusBar.showMessage(msg, 10000)

    def _load_current_connections(self):
        self.savedConnections.clear()

        cons = [c for c in self.connections.stored_connections]
        # if self._connection not in cons:
        #     cons.append(self._connection)
        self.savedConnections.addItems([conn.name for conn in self.connections.stored_connections])

    def connect(self):
        if self.connection.connect(self):
            self.connections.add(self.connection)
        else:
            self.showMessage("Connection failed")

        self._update_buttons()

    @property
    def current_conn_index(self):
        return self._current_conn_index

    @current_conn_index.setter
    def current_conn_index(self, new_value):
        # print("Novi index: %s" % new_value)
        try:
            self._current_conn_index = new_value
            self.connection = self.connections.stored_connections[new_value]
            self._set_conn_params(self._connection)
        except:
            pass


    @property
    def current_protocol_index(self):
        return self._current_protocol_index

    @current_protocol_index.setter
    def current_protocol_index(self, new_value):
        print("Novi index: %s" % new_value)
        try:
            self._current_protocol_index = new_value
            self.connection.protocol = self._protocols[new_value]
            if new_value == 1:
                self.hostname_i.setText('')
                self.hostname_i.setDisabled(True)
                self.port_i.setText('')
                self.port_i.setDisabled(True)
                self.database_i.setText('')
                self.database_i.setDisabled(True)
                self.clusteruri_i.setDisabled(False)

                self.connection.hostname = None
                self.connection.port = None
                self.connection.database = None
            if new_value == 0:
                self.hostname_i.setDisabled(False)
                self.port_i.setDisabled(False)
                self.database_i.setDisabled(False)
                self.clusteruri_i.setText('')
                self.clusteruri_i.setDisabled(True)

                self.connection.cluster_uri = None
        except:
            pass

    @property
    def connection(self):
        return self._connection

    @connection.setter
    def connection(self, new_value):
        self._connection = new_value
