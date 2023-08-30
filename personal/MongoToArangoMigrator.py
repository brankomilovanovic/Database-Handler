from pyArango.connection import *
from bson import ObjectId
from pyArango.connection import Connection as ArangoConnection
from pymongo import MongoClient
from pyArango.graph import Graph, EdgeDefinition

class MongoToArangoMigrator:
    def __init__(self, mongodb_client, mongodb_db, arangodb_url, arangodb_username, arangodb_password, arangodb_db):
        self.mongodb_client =  MongoClient(mongodb_client)  
        self.mongodb_db = self.mongodb_client[mongodb_db]

        self.arangodb_connection = ArangoConnection(arangoURL=arangodb_url, username=arangodb_username, password=arangodb_password)
        self.arangodb_db = self.arangodb_connection[arangodb_db]
        
    def create_arangodb_collections(self, arangodb_collection_names):
        for collection_name in arangodb_collection_names:
            if collection_name not in self.arangodb_db.collections:
                self.arangodb_db.createCollection(name=collection_name)

    def create_arangodb_collections_recursive(self, data, arangodb_collection_names):
        for key, value in data.items():
            if(key != 'naslov'):
                if isinstance(value, list):
                    collection_name = key
                    arangodb_collection_names.append(collection_name)
                if isinstance(value, dict):
                    collection_name = key
                    arangodb_collection_names.append(collection_name)
                    self.create_arangodb_collections_recursive(value, arangodb_collection_names)

    def migrate_mongodb_to_arangodb(self, mongodb_collection):
        self.mongodb_collection = self.mongodb_db[mongodb_collection]

        # Migracija podataka
        mongo_documents = self.mongodb_collection.find()
        for mongo_doc in mongo_documents:
            arangodb_collection_names = []
            self.create_arangodb_collections_recursive(mongo_doc, arangodb_collection_names)
            
            edge_definitions = self.create_edge_definitions(arangodb_collection_names)
            
            self.create_graph('nosql', 'myGraph', edge_definitions)

            for collection_name in arangodb_collection_names:
                self.remove_id(mongo_doc)
                document = self.find_value(mongo_doc, collection_name)
                if isinstance(document, dict):
                    self.insert_document_as_node('nosql', 'myGraph', document, collection_name)

    def remove_id(self, obj):
        if isinstance(obj, dict):
            if "_id" in obj:
                del obj["_id"]
            for key, value in obj.items():
                self.remove_id(value)
        elif isinstance(obj, list):
            for item in obj:
                self.remove_id(item)

    def remove_object(self, objekat):
        keys = [] 
        try:
            for kljuc, vrednost in objekat.items():
                if isinstance(vrednost, (dict, list)):
                    keys.append(kljuc)
            
            for key in keys:
                objekat.pop(key)
        except: 
            return objekat

        return objekat
            
    def find_value(self, obj, key):
        if isinstance(obj, dict):
            if key in obj:
                return obj[key]
            else:
                for value in obj.values():
                    result = self.find_value(value, key)
                    if result is not None:
                        return result
        elif isinstance(obj, list):
            for item in obj:
                result = self.find_value(item, key)
                if result is not None:
                    return result

        return None

    def create_edge_definitions(self, collection_names):
        edge_definitions = []

        for i in range(len(collection_names)):
            collection_name = f"edge_collection{i + 1}"
            edge_definition = {
                'collection': collection_name,
                'from': [collection_name],
                'to': [collection_names[(i + 1) % len(collection_names)]]
            }
            edge_definitions.append(edge_definition)

        return edge_definitions

    def create_graph(self, database_name, graph_name, edge_definitions):
        session = requests.Session()
        session.auth = ('root', 'root')

        graph_payload = {
            'name': graph_name,
            'edgeDefinitions': edge_definitions
        }

        create_graph_url = f'http://127.0.0.1:8529/_db/{database_name}/_api/gharial'
        response = session.post(create_graph_url, json=graph_payload)

        if response.status_code == 202:
            print(f"Graph '{graph_name}' created successfully.")
        else:
            print(f"Failed to create graph. Error: {response.text}")

    def insert_document_as_node(self, database_name, graph_name, document, collection):

        session = requests.Session()
        session.auth = ('root', 'root')

        insert_node_url = f'http://127.0.0.1:8529/_db/{database_name}/_api/gharial/{graph_name}/vertex/{collection}'
        response = session.post(insert_node_url, json=document)

        if response.status_code == 202:
            print("Node inserted successfully.", collection)
        else:
            print(f"Failed to insert node. Error: {response.text}")