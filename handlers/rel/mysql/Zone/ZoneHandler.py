from PyQt5.QtWidgets import QWidget, QTabWidget

from handlers.rel.RelDBActions import RelDBActions
from handlers.rel.Table.Table import Table, Slot
from handlers.rel.mysql.Metadata.MySqlMetadataSupplier import MySqlMetadataSupplier
from handlers.rel.mysql.Zone.Zone import ZoneView


class ZoneHandler:
    def __init__(self, parent, conn, table, schema, clb):
        _supplier = MySqlMetadataSupplier(conn, table, schema)
        self.metadata = _supplier.extract()
        self.actions = RelDBActions(conn, self.metadata)
        self._name = ZoneHandler.assemble_name(self.metadata.schema, self.metadata.codeName)
        self.view = ZoneView(parent)
        self.view.set_close(self.close)
        self.view.name = self._name
        self.childTabs = None
        self.child = []

        self.table = Table(self.view, {
            'search': self.actions.search,
            'delete': self.actions.delete,
            'insert': self.actions.insert,
            'filter': self.actions.filter,
            'update': self.actions.update,
        }, self.metadata)
        self.table.subscribe(Slot.SELECT, self.selected)
        self.table.set_up_hierarchical_movement(clb)

        self.view.set_parent_zone(self.table)

        # Child zone
        if len(self.metadata.childRelation) > 0:
            self.childTabs = QTabWidget(self.view)
            self.view.set_child_zone(self.childTabs)

            for c in self.metadata.childRelation:
                __supplier = MySqlMetadataSupplier(conn, c.table_code_name, self.metadata.schema)
                __metadata = __supplier.extract()
                __actions = RelDBActions(conn, __metadata)
                __table = Table(self.childTabs,
                                {'search': __actions.search,
                                 'filter': __actions.filter,
                                 'insert': __actions.insert,
                                 'update': __actions.update,
                                 'delete': __actions.delete},
                                __metadata, True)
                __table.set_fixed(True)
                __table.add_upgrade_to_parent_zone(clb)
                self.childTabs.addTab(__table, f'{c.table_code_name}.{c.relation_name}')

                self.child.append((c, __table))
            self.view.set_child_zone(self.childTabs)

        # first item selected mock up
        self.selected(self.table.model[0])

    def close(self) -> bool:
        print(f"ZoneHandler : Closing zone {self._name}")
        self.view.close()
        return True

    def selected(self, obj):
        for c, t in self.child:
            params = {}
            for p in c.points:
                params[p.code_name] = obj[p.referenced_code_name]
            t.set_default(params)
            t.load(t.actions.filter(params))

    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_view(self):
        return self.view

    @staticmethod
    def assemble_name(schema, table):
        return f'{schema}.{table}'

    @staticmethod
    def name_format():
        return 'schema.table'
