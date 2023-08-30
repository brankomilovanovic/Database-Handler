import os
from enum import Enum

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton, QInputDialog, QAction, \
    QAbstractItemView

from handlers.rel.Table.FilterUI.FilterWindow import FilterWindow
from handlers.rel.Table.InsertUI.InsertWindow import InsertWindow
from handlers.rel.Table.UpdateUI.UpdateWindow import UpdateWindow
from handlers.rel.Table.components.Options import Options
from handlers.rel.Table.components.TableToolbar import TableToolBar


class Slot(Enum):
    SELECT = "Select"


class TableCRUDActions:
    def __init__(self, param):
        self.insert = param['insert'] if 'insert' in param else None
        self.update = param['update'] if 'update' in param else None
        self.delete = param['delete'] if 'delete' in param else None
        self.filter = param['filter'] if 'filter' in param else None
        self.search = param['search'] if 'search' in param else None


class Table(QWidget):
    def __init__(self, parent, actions, metadata, toolbar=True):
        super().__init__(parent)
        self.actions = TableCRUDActions(actions)
        self.metadata = metadata
        self.model = []
        self.default = {}
        self.fixed = False
        self.selectedRow = {}
        self.subscriptions = {
            Slot.SELECT: []
        }
        self.layout = QVBoxLayout(self)

        self.toolbar = None
        if toolbar:
            self._set_up_toolbar()

        self.table = QTableWidget(self)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.cellClicked.connect(lambda r, c: self.emit(Slot.SELECT, self.model[r]))
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.layout.addWidget(self.table)

        self._set_up_table_headers()
        self.load()

    def load(self, model=None):
        self.clear()
        print(self.default)
        self.model = model if model is not None else self.actions.search({'value': '', 'default': self.default})
        self.table.setRowCount(len(self.model))

        for i, r in enumerate(self.model):
            for col_i, col in enumerate(self.metadata.columns):
                self.table.setItem(i, col_i, QTableWidgetItem(str(r[col.code_name])))

        self.table.setCurrentIndex(self.table.model().index(0, 0))
        if len(self.model) > 0:
            self.emit(Slot.SELECT, self.model[0])

    def set_default(self, value: dict):
        self.default = value

    def set_selected_row(self, value: dict):
        self.selectedRow = value

    def set_fixed(self, fixed: bool):
        self.fixed = fixed

    def clear(self):
        self.set_selected_row({})

        for i in range(self.table.rowCount()):
            self.table.removeRow(i)

        # self.table.clear()
        self.table.clearContents()
        self.table.setRowCount(0)

    # Set ups
    def _set_up_table_headers(self):
        # print(f'Columns count is {len(self.metadata.columns)}')
        self.table.setColumnCount(len(self.metadata.columns))
        for i, h in enumerate(self.metadata.columns):
            # print(f"Setting up table headers for {h.code_name} with label {h.label} at pos {i}")
            _header = QTableWidgetItem(str(h.label))
            # print(_header)
            self.table.setHorizontalHeaderItem(i, _header)

    def makeAction(self, params):
        _icon = QIcon(params['icon'])
        # print("Icon je ", _icon.isNull())
        _name = '' if os.path.exists(params['icon']) else params['name']
        _button = QPushButton()
        _button.setIcon(_icon)
        _button.setText(_name)
        _button.setIconSize(QSize(32, 32))
        _button.clicked.connect(params['clb'])
        return _button

    def _set_up_toolbar(self):
        self.toolbar = TableToolBar(self)
        self.layout.addWidget(self.toolbar, -1)

        self.toolbar.addWidget(self.makeAction({
            'icon': f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-reset-32.png",
            'name': "Refresh",
            'clb': lambda x: self.load()
        }))

        if self.actions.search:
            self.toolbar.addWidget(self.makeAction({
                'icon': f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-search-32.png",
                'name': "Search",
                'clb': self._search
            }))

        if self.actions.filter:
            self.toolbar.addWidget(self.makeAction({
                'icon': f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-filter-32.png",
                'name': "Search",
                'clb': self._filter
            }))

        self.toolbar.add_spacing()

        if self.actions.insert:
            self.toolbar.addWidget(self.makeAction({
                'icon': f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-plus-math-32.png",
                'name': "Insert",
                'clb': self._insert
            }))

        if self.actions.update:
            self.toolbar.addWidget(self.makeAction({
                'icon': f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-edit-32.png",
                'name': "Insert",
                'clb': self._update
            }))

        if self.actions.delete:
            self.toolbar.addWidget(self.makeAction({
                'icon': f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-delete-32.png",
                'name': "Delete",
                'clb': self._delete
            }))

        self.toolbar.add_separator()
        self.toolbar.add_spacing()

        self.toolbar.addWidget(self.makeAction({
            'icon': f'assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-skip-to-start-48.png',
            'name': "Skip to start",
            'clb': lambda _: self._select(0)
        }))
        self.toolbar.addWidget(self.makeAction({
            'icon': f'assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-previous-48.png',
            'name': "Previous record",
            'clb': lambda _: self._select(sorted(self.table.selectionModel().selectedRows(), reverse=True)[0].row() - 1)
        }))

        self.toolbar.addWidget(self.makeAction({
            'icon': f'assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-next-48(1).png',
            'name': "Next record",
            'clb': lambda _: self._select(
                sorted(self.table.selectionModel().selectedRows(), reverse=True)[-1].row() + 1)
        }))

        self.toolbar.addWidget(self.makeAction({
            'icon': f'assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-next-48.png',
            'name': "Next record",
            'clb': lambda _: self._select(len(self.model) - 1)
        }))

    # Subscription
    def subscribe(self, slot: Slot, clb):
        self.subscriptions[slot].append(clb)

    def emit(self, slot: Slot, obj):
        self.set_selected_row(obj)
        for c in self.subscriptions[slot]:
            c(obj)

    # Functions
    def _select(self, index):
        if index <= 0:
            index = 0
        elif index >= len(self.model) - 1:
            index = len(self.model) - 1

        self.table.setCurrentIndex(self.table.model().index(index, 0))

        if len(self.model) > 0 and index <= len(self.model) - 1:
            self.emit(Slot.SELECT, self.model[index])

    def _search(self, txt=None):
        if txt is None or txt is False:
            txt, _ = QInputDialog.getText(self, 'Find', "Find in data:")
        self.load(self.actions.search({'value': txt, 'default': self.default}))

    def _insert(self):
        def clb(value):
            payload = self.actions.insert(value)
            if (payload[0]):
                mock = {} 
                for k, v in self.default.items():
                    mock[k] = v

                f.close()
                if len(mock) > 0:
                    self.load(self.actions.filter(mock))
                else:
                    self.load()
            else:
                f.showMessage(payload[1])

        f = InsertWindow(self, self.metadata.columns, clb, self.default, self.fixed)
        f.exec()

    def _update(self):
        def clb(value):
            payload = self.actions.update(value)
            if(payload[0]):
                mock = {} 
                for k, v in self.default.items():
                    mock[k] = v

                f.close()
                if len(mock) > 0:
                    self.load(self.actions.filter(mock))
                else:
                    self.load()

            else:
                f.showMessage(payload[1])

        if(len(self.selectedRow) != 0):
            f = UpdateWindow(self, self.metadata.columns, clb, self.default, self.fixed, self.selectedRow)
            f.exec()

    def _filter(self):
        def clb(value):
            mock = {}  # adaptation for action
            for k, v in value.items():
                mock[k] = v['value']

            self.load(self.actions.filter(mock))

        f = FilterWindow(self, self.metadata.columns, clb, self.default, self.fixed)
        f.exec()

    def _delete(self):
        for index in sorted(self.table.selectionModel().selectedRows(), reverse=True):
            self.actions.delete(self.model[index.row()])
        self.load()

    # Hierarchical movement
    def set_up_hierarchical_movement(self, clb):
        self.toolbar.add_spacing()
        def callback(params):
            clb(params['schema'], params['table'])

        if (len(self.metadata.parentRelation) > 0):
            parent = Options(self.toolbar, QIcon(f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-slide-up-32.png"))

            for p in self.metadata.parentRelation:
                _action = QAction(f"{p.relation_name}.{p.ref_table_code_name}", parent)
                _action.param = {
                    'schema': self.metadata.schema,
                    'table': p.ref_table_code_name
                }
                _action.clb = callback
                parent.addSelfCallableAction(_action)
            self.toolbar.addWidget(parent)

        if (len(self.metadata.childRelation) > 0):
            child = Options(self.toolbar, QIcon(f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-down-button-32.png"))

            for p in self.metadata.childRelation:
                _action = QAction(f"{p.relation_name}.{p.table_code_name}", child)
                _action.param = {
                    'schema': self.metadata.schema,
                    'table': p.table_code_name
                }
                _action.clb = callback
                child.addSelfCallableAction(_action)
            self.toolbar.addWidget(child)

    def add_upgrade_to_parent_zone(self, clb):
        self.toolbar.add_spacing()

        self.toolbar.addWidget(self.makeAction({
            'icon': f"assets{os.path.sep}img{os.path.sep}icon8{os.path.sep}Fluent{os.path.sep}icons8-up-arrow-32.png",
            'name': "Upgrade to parent zone",
            'tip': "Upgrade to parent zone",
            'clb': lambda _: clb(self.metadata.schema, self.metadata.codeName)
        }))
