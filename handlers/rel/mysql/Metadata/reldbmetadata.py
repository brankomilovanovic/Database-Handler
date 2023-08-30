import csv
import json

import os

from multimethod import multimethod

from handlers.rel.mysql.Metadata.RelDbMetadataSupplier import RelDbMetaDataSupplier

METADATA_EXTRA_NAME = "_metadata.json"


class RelDbMetaData:
    class Column:
        @multimethod
        def __init__(self):
            self.label = None
            self.code_name = None
            self.primary = None
            self.foreign = None
            self.type = None
            self.max_l = None
            self.notnull = None
            self.default = None
            self.ordinal_pos = None

        @multimethod
        def __init__(self,
                     label: str, code_name: str,
                     primary: bool, foreign: bool,
                     _type: str, max_l: int, notnull: bool, default: str,
                     ordinal_pos: int):
            self.label = label
            self.code_name = code_name
            self.primary = primary
            self.foreign = foreign
            self.type = _type
            self.max_l = max_l
            self.notnull = notnull
            self.default = default
            self.ordinal_pos = ordinal_pos

        def create(self, _dict: dict):
            self.code_name = _dict['code_name']
            self.label = _dict['label']
            self.primary = _dict['primary']
            self.foreign = _dict['foreign']
            self.type = _dict['type']
            self.type = _dict['type']
            self.max_l = _dict['max_l']
            self.notnull = _dict['not_null']
            self.default = _dict['default']
            self.ordinal_pos = _dict['ordinal_pos']
            return self

        def __str__(self):
            details = ''
            details += f'  label   : {self.label}\n'
            details += f'    code_name    : {self.code_name}\n'
            details += f'    primary    : {self.primary}\n'
            details += f'    foreign    : {self.foreign}\n'
            details += f'    type    : {self.type}\n'
            details += f'    max_l    : {self.max_l}\n'
            details += f'    notnull    : {self.notnull}\n'
            details += f'    default    : {self.default}\n'
            details += f'    ordinal_pos    : {self.ordinal_pos}\n'

            return details

    class RelationMeta:
        class Point:
            @multimethod
            def __init__(self):
                self.code_name = None
                self.referenced_code_name = None

            @multimethod
            def __init__(self,
                         code_name,
                         referenced_code_name):
                self.code_name = code_name
                self.referenced_code_name = referenced_code_name
            def create(self, _dict: dict):
                ...

            def __str__(self):
                details = ''
                details += f'         code_name   : {self.code_name}\n'
                details += f'         referenced_code_name    : {self.referenced_code_name}\n'
                return details

        @multimethod
        def __init__(self):
            self.table_code_name = None
            self.ref_table_code_name = None
            self.relation_name = None
            self.points = []

        def create(self, _dict: dict):
            self.table_code_name = _dict['table_code_name']
            self.ref_table_code_name = _dict['ref_table_code_name']
            self.relation_name = _dict['relation_name']
            self.points = _dict['points']

            return self

        def __str__(self):
            details = ''
            details += f'  relation_name    : {self.relation_name}\n'
            details += f'     table_code_name   : {self.table_code_name}\n'
            details += f'     ref_table_code_name    : {self.ref_table_code_name}\n'
            details += f'     points    : \n'

            for p in self.points:
                details += "       point\n" + str(p) + "\n"
            return details

    def __init__(self):
        self.columns = []
        self.codeName = None
        self.name = None
        self.schema = None
        self.parentRelation = []
        self.childRelation = []

    def get_headers_names(self):
        return list(map(lambda header: header["name"], self.headers))

    def get(self, header_name):
        for index, header in enumerate(self.metadata["headers"]):
            if header["name"] == header_name:
                return index, header
        return None

    def get_header_position_by_name(self, col_name):
        for pos, header in enumerate(self.metadata["headers"]):
            if header["name"] == col_name:
                return pos

    @staticmethod
    def blank_meta():
        return {
            'headers': [],
            'name': '',
            'schema': '',
            'relation': {
                'parent': [],
                'child': []
            }
        }

    @staticmethod
    def blank_header():
        return {
            'label': '',
            'code_name': '',
            'primary': False,
            'foreign': False,
            'type': '',
            'min_l': 1,
            'max_l': 1,
            'not_null': True
        }

    def __str__(self):
        details = ''
        details += f'codeName   : {self.codeName}\n'
        details += f'name    : {self.name}\n'
        details += f'schema    : {self.schema}\n'
        details += f'colums    : \n'
        for p in self.columns:
            details += "" + str(p)

        details += f'parent    : \n'
        for p in self.parentRelation:
            details += "" + str(p)

        details += f'child    : \n'
        for p in self.childRelation:
            details += "" + str(p)

        return details
