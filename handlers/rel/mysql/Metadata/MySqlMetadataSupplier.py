from handlers.rel.mysql.FieldMapper.FieldMapper import FieldMapper
from handlers.rel.mysql.Metadata.RelDbMetadataSupplier import RelDbMetaDataSupplier
from handlers.rel.mysql.Metadata.reldbmetadata import RelDbMetaData


def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))


def format_mysql(cursor_results):
    arr = []
    for row in cursor_results:
        for data in row.fetchall():
            arr.append(data)
    return arr


class MySqlMetadataSupplier(RelDbMetaDataSupplier):

    def __init__(self, conn, table, schema=None):
        super().__init__(conn, table, schema)
        self.metadata_c = None
        self.fm = FieldMapper(conn, schema)

    def table(self):
        return f"'{self._schema}.{self._table}'" if self._schema else f"'{self._table}'"

    # def _extract_column(self, column: str):
    #     conn = self._conn.get_connection()
    #     cursor = conn.cursor(dictionary=True)
    #
    #     ccolumn = RelDbMetaData.Column()
    #
    #     cursor.execute(self._column_sql(column))
    #     c = cursor.fetchone()
    #
    #     ccolumn.create()
    #
    #     cursor.close()
    #     return ccolumn

    def _extract_columns(self):
        conn = self._conn.get_connection()
        cursor = conn.cursor(dictionary=True)
        column = []

        cursor.execute(self._columns_sql())
        _columns = cursor.fetchall()

        cursor.execute(self._referencing_to())
        _foreign_keys = cursor.fetchall()
        _this_table_foreign_keys = [r['COLUMN_NAME'] for r in _foreign_keys]

        for c in _columns:
            label = self.fm.get_field_label(self._table, c['COLUMN_NAME'])
            # print(f"Meta: Labela za {c['COLUMN_NAME']} je {label} i label is not non? {label is not None}")
            column.append(RelDbMetaData.Column().create({
                'label': label if label is not None else c['COLUMN_NAME'],
                'code_name': c['COLUMN_NAME'],
                'primary': True if c['COLUMN_KEY'] == 'PRI' else False,
                'foreign': c['COLUMN_NAME'] in _this_table_foreign_keys,
                'type': c["DATA_TYPE"],
                # 'min_l': c['CHARACTER_MINIMUM_LENGTH'],
                'max_l': c['CHARACTER_MAXIMUM_LENGTH'],
                'not_null': c['IS_NULLABLE'] == 'YES',
                'default': c['COLUMN_DEFAULT'],
                'ordinal_pos': c['ORDINAL_POSITION'],
            }))

        cursor.close()
        conn.close()
        return column

    def _extract_parent_relation(self):
        conn = self._conn.get_connection()
        cursor = conn.cursor(dictionary=True)
        relations = []

        cursor.execute(self._referencing_to())
        _columns = cursor.fetchall()
        _relations = {}

        for c in _columns:
            if c["CONSTRAINT_NAME"] in _relations:
                _relations[c["CONSTRAINT_NAME"]].append(c)
            else:
                _relations[c["CONSTRAINT_NAME"]] = [c]

        for k, v in _relations.items():
            relations.append(RelDbMetaData.RelationMeta().create({
                'table_code_name': self._table,
                'ref_table_code_name': v[0]['REFERENCED_TABLE_NAME'],
                'relation_name': k,
                'points': [RelDbMetaData.RelationMeta.Point(_p['COLUMN_NAME'], _p['REFERENCED_COLUMN_NAME'])
                           for _p in v],
                # 'points': [{'point': RelDbMetaData.RelationMeta.Point(_p['COLUMN_NAME'], None),
                #             'referenced_point': RelDbMetaData.RelationMeta.Point(_p['REFERENCED_COLUMN_NAME'], None)
                #             } for _p in v],
            }))

        cursor.close()
        conn.close()
        return relations

    def _extract_child_relation(self):
        conn = self._conn.get_connection()
        cursor = conn.cursor(dictionary=True)
        relations = []

        cursor.execute(self._referenced_by())
        _columns = cursor.fetchall()
        _relations = {}

        for c in _columns:
            if c["CONSTRAINT_NAME"] in _relations:
                _relations[c["CONSTRAINT_NAME"]].append(c)
            else:
                _relations[c["CONSTRAINT_NAME"]] = [c]

        for k, v in _relations.items():
            relations.append(RelDbMetaData.RelationMeta().create({
                'table_code_name': v[0]["TABLE_NAME"],
                'ref_table_code_name': self._table,
                'relation_name': k,
                'points': [RelDbMetaData.RelationMeta.Point(_p['COLUMN_NAME'], _p['REFERENCED_COLUMN_NAME'])
                           for _p in v],
                # 'points': [{'point': RelDbMetaData.RelationMeta.Point(_p['COLUMN_NAME'], None),
                #             'referenced_point': RelDbMetaData.RelationMeta.Point(_p['REFERENCED_COLUMN_NAME'], None)
                #             } for _p in v],
            }))

        cursor.close()
        conn.close()
        return relations

    def extract(self):
        metadata = RelDbMetaData()
        metadata.columns = self._extract_columns()

        metadata.codeName = self._table
        metadata.schema = self._schema
        metadata.name = self.fm.get_table_label(self._table) if self.fm.get_table_label(self._table) else self._table

        metadata.parentRelation = self._extract_parent_relation()
        metadata.childRelation = self._extract_child_relation()

        return metadata

    def store(self):
        pass

    def _columns_sql(self):
        return f"SELECT * " \
               f"FROM information_schema.columns" \
               f" WHERE table_schema = '{self._schema}' AND table_name = '{self._table}';"

    def _column_sql(self, column: str) -> str:
        return f"SELECT * " \
               f"FROM information_schema.columns" \
               f" WHERE table_schema = '{self._schema}'" \
               f" AND table_name = '{self._table}'" \
               f"AND COLUMN_NAME = {column};"

    def _referencing_to(self):
        return f"SELECT TABLE_NAME,COLUMN_NAME,CONSTRAINT_NAME, REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME" \
               f" FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE" \
               f" WHERE REFERENCED_TABLE_SCHEMA = '{self._schema}' AND TABLE_NAME = '{self._table}'; "

    def _referenced_by(self):
        return f"SELECT TABLE_NAME,COLUMN_NAME,CONSTRAINT_NAME, REFERENCED_TABLE_NAME,REFERENCED_COLUMN_NAME" \
               f" FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE" \
               f" WHERE REFERENCED_TABLE_SCHEMA = '{self._schema}' AND REFERENCED_TABLE_NAME = '{self._table}'; "
