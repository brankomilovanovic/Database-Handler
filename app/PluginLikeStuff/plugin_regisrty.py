from ui.menubar.MenuBar import MenuBar
from app.PluginLikeStuff.Plugin import Plugin

from PyQt5.QtGui import QIcon, QImage
from PyQt5.QtWidgets import QAction, QMenu
from PyQt5 import QtCore
from functools import partial
import os

import json
from pathlib import Path


class PluginRegistry:

    def __init__(self, plugins : Plugin = []) -> None:
        self.menu_bar = MenuBar.instance()
        self.plugins_menu = None
        self.plugin_submenus : QMenu = []
        self.plugins = plugins

        self.PATH = f"app{os.path.sep}PluginLikeStuff{os.path.sep}config{os.path.sep}plugins.json"



    #Singleton
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(PluginRegistry, cls).__new__(cls)

        return cls.instance
    

    def register(self, plugin : Plugin):
        self.plugins_menu = self.menu_bar.set_menu("Plugins")

        plugin_name = type(plugin).__name__
        
        submenu = QMenu(plugin_name,  self.plugins_menu)
        self.plugins_menu.addMenu(submenu)
        self.plugin_submenus.append(submenu)

        activate_action = QAction(QIcon(f"assets{os.path.sep}img{os.path.sep}iconmonstr-check-mark-14-64.png"), "Activate", self.plugins_menu)
        deactivate_action = QAction(QIcon(f"assets{os.path.sep}img{os.path.sep}closeDoc.png"), "Deactivate", self.plugins_menu)

        if self.check_if_activated(plugin):
            plugin.activate()
            activate_action.setDisabled(True)
            submenu.setIcon(QIcon(f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-green-circle-32.png"))
        else:
            deactivate_action.setDisabled(True)
            submenu.setIcon(QIcon(f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-unavailable-32.png"))

 
        activate_action.triggered.connect(partial(self.activate_plugin, plugin))
        deactivate_action.triggered.connect(partial(self.deactivate_plugin, plugin))
        
        submenu.addAction(activate_action)
        submenu.addAction(deactivate_action)

        self.plugins.append(plugin)
        self.save_configuration(plugin_name)



    def activate_plugin(self, plugin : Plugin):

        if not self.check_if_activated(plugin):

            plugins = self.load_plugins()

            for p in plugins:
                if p["name"] == type(plugin).__name__:
                    p["activated"] = True


            with open(self.PATH, "w") as file:
                json.dump(plugins, file, indent=4)


            for submenu in self.plugin_submenus:
                if submenu.title() == type(plugin).__name__:
                    submenu.actions()[0].setDisabled(True)
                    submenu.actions()[1].setEnabled(True)
                    submenu.setIcon(QIcon(f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-green-circle-32.png"))


            print("Aktiviran", plugin)
            plugin.activate()

    
    def deactivate_plugin(self, plugin : Plugin):

        if self.check_if_activated(plugin):
        
            plugins = self.load_plugins()

            for p in plugins:
                if p["name"] == type(plugin).__name__:
                    p["activated"] = False

            with open(self.PATH, "w") as file:
                json.dump(plugins, file, indent=4)

            
            for submenu in self.plugin_submenus:
                if submenu.title() == type(plugin).__name__:
                    submenu.actions()[0].setEnabled(True)
                    submenu.actions()[1].setDisabled(True)
                    submenu.setIcon(QIcon(f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-unavailable-32.png"))


            print("Deaktiviran", plugin)
            plugin.deactivate()


    def check_if_activated(self, plugin : Plugin) -> bool:
        '''
            Vraca True ukoliko je plugin u konfiguraciji vec aktivan, u suprotnom vraca False
        '''
        plugins = self.load_plugins()

        for p in plugins:
            if p["name"] == type(plugin).__name__ and p["activated"] == True:
                return True
      
        return False



    def save_configuration(self, plugin_name):
        plugins = self.load_plugins()
        
        plugin = {"name": plugin_name, "activated": False} # Po defaultu dodaje plugin ukoliko vec nije registrovan

        if not any(plugin_name in p.values() for p in plugins):
            plugins.append(plugin)

            with open(self.PATH, "w") as file:
                json.dump(plugins, file, indent=4)
        
    
    def get_plugin(self, name) -> Plugin:
        for plugin in self.plugins:
            if type(plugin).__name__ == name:
                return plugin


    def load_plugins(self):

        if not os.path.exists(self.PATH):
            os.makedirs(os.path.dirname(self.PATH), exist_ok=True)

            with open(self.PATH, "w") as file:
                json.dump([], file)

        
        with open(self.PATH, "r") as file:
            plugins = json.load(file)
        
        return plugins
        