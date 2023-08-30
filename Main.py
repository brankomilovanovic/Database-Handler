import sys

from PyQt5.QtWidgets import QApplication

from handlers.nosql.MongoHandler import MongoHandler
from handlers.nosql.arangodb.ArangoHandler import ArangoHandler
from handlers.rel.RelDBActions import testings
from handlers.rel.mysql.MySqlHandler import MySqlHandler
from ui.window.MainWindow import MainWindow
from app.PluginLikeStuff.plugin_regisrty import PluginRegistry


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    # Handlers
    mysql_handler = MySqlHandler()

    plugin_regisrty = PluginRegistry()
    plugin_regisrty.register(mysql_handler)
    plugin_regisrty.register(MongoHandler())
    plugin_regisrty.register(ArangoHandler())

    window.show()
    app.exec()

if __name__ == '__main__':
    main()
