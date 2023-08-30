import json
from handlers.nosql.arangodb.Connection.ArangoDBConnection import ArangoDBConnection
from pyArango.connection import Database
import threading
from pyArango.theExceptions import DeletionError, CreationError, UpdateError, QueryError


class ActionABS:
    def __init__(self, connection : ArangoDBConnection, database_name) -> None:
        self.connection = connection
        self.database_name = database_name



class CreateAction(ActionABS):
    
    def __init__(self, connecetion : ArangoDBConnection, database_name) -> None:
        super().__init__(connecetion, database_name)


    def perform_action(self, current_descriptor):
        self.result = []

        conn = self.connection.get_connection()

        db : Database = conn[self.database_name]

        aql = "INSERT @doc in @@collectionName LET newDoc = NEW RETURN newDoc"
        bind = {
            "doc": current_descriptor["document"],
            "@collectionName": current_descriptor["collectionName"]
        }

        try:
            query_result = db.AQLQuery(query=aql, bindVars=bind) #graph.createVertex(collectionName=current_descriptor["collectionName"], docAttributes=current_descriptor["document"])
            print(query_result)
            result_msg = "Document created succsesfully."
            succes = True
            
        except CreationError as error:
            result_msg = "An error occured during document insertion: " + str(error)
            succes = False
        
        self.result = [query_result[0]._id, result_msg, succes]
            


class GetAction(ActionABS):
    def __init__(self, connection: ArangoDBConnection, database_name) -> None:
        super().__init__(connection, database_name)

    def perform_action(self, current_descriptor):
        self.result = []

        conn = self.connection.get_connection()

        db: Database = conn[self.database_name]

        aql = "FOR doc IN @@collectionName FILTER doc._id == @key RETURN doc"
        bind = {
            "key": current_descriptor["key"],
            "@collectionName": current_descriptor["collectionName"]
        }

        try:
            result = db.AQLQuery(query=aql, bindVars=bind)
            if result:
                document = result.response['result'][0]
                document.update({"body": {k: v for k, v in document.items() if k not in ["_key", "_id", "_rev"]}})
                result_msg = "Document retrieved successfully."
                success = True
            else:
                document = None
                result_msg = "Document not found."
                success = False
        except QueryError as error:
            document = None
            result_msg = "An error occurred during document retrieval: " + str(error)
            success = False

        self.result = [result_msg, success, document]


class DeleteAction(ActionABS):

    def __init__(self, connection: ArangoDBConnection, database_name) -> None:
        super().__init__(connection, database_name)
    

    def perform_action(self, current_descriptor):
        self.result = []

        conn = self.connection.get_connection()

        db : Database = conn[self.database_name]

        aql = "REMOVE @key IN @@collectionName"
        bind = {
            "key": current_descriptor["key"],
            "@collectionName": current_descriptor["collectionName"]
        }

        try:
            db.AQLQuery(query=aql, bindVars=bind)   # graph.deleteVertex(document=current_descriptor)
            result_msg = "Document deleted succsesfully."
            succes = True

        except DeletionError as error:
            result_msg = "An error occured during document deletion: " + str(error)
            succes = False
        
        self.result = [result_msg, succes]



class UpdateAction(ActionABS):
    
    def __init__(self, connection: ArangoDBConnection, database_name) -> None:
        super().__init__(connection, database_name)
    

    def perform_action(self, current_descriptor):
        self.result = []

        conn = self.connection.get_connection()

        db : Database = conn[self.database_name]

        aql = "UPDATE @key WITH @doc IN @@collectionName LET updatedDoc = NEW RETURN updatedDoc"
        bind = {
            "key": current_descriptor["key"],
            "doc": current_descriptor["document"],
            "@collectionName": current_descriptor["collectionName"]
        }

        try:
            query_result = db.AQLQuery(query=aql, bindVars=bind)  
            result_msg = "Document updated succsesfully."
            succes = True

        except UpdateError as error:
            result_msg = "An error occured during document update: " + str(error)
            succes = False
        
        self.result = [query_result[0], result_msg, succes]


class ArangoDBActions:

    def __init__(self, connection, database_name) -> None:
        self.connection = connection
        self.database_name = database_name
        self.create_action = CreateAction(self.connection, self.database_name)
        self.delete_action = DeleteAction(self.connection, self.database_name)
        self.update_action = UpdateAction(self.connection, self.database_name)
        self.get_action = GetAction(self.connection, self.database_name)
    


    def create(self, current_descriptor):
        create_thread = threading.Thread(target=self.create_action.perform_action, args=(current_descriptor, ))
        create_thread.start()
        create_thread.join()
        print(self.create_action.result)

        return self.create_action.result
    

    def delete(self, current_descriptor):
        create_thread = threading.Thread(target=self.delete_action.perform_action, args=(current_descriptor, ))
        create_thread.start()
        create_thread.join()
        print(self.delete_action.result)

        return self.delete_action.result


    def update(self, current_descriptor):
        update_thread = threading.Thread(target=self.update_action.perform_action, args=(current_descriptor, ))
        update_thread.start()
        update_thread.join()
        print(self.update_action.result)

        return self.update_action.result
    
    def get(self, current_descriptor):
        update_thread = threading.Thread(target=self.get_action.perform_action, args=(current_descriptor, ))
        update_thread.start()
        update_thread.join()
        print(self.get_action.result)
        
        return self.get_action.result




def arango_testing(conn : ArangoDBConnection):

    arango_actions = ArangoDBActions(conn, "_system")

    #kreiranje cvora
    arango_actions.create(
        {
            "collectionName": "testCollection1",
            "document": {
                "_key": "Marko34",
                "ime": "Marko",
                "godine": 34
            }
        }
    )

    #kreiranje veze
    arango_actions.create(
        {
            "collectionName": "testVeze",
            "document": {
                "_from": "testCollection1/Marko34",
                "_to": "testCollection2/stefan35",
                "_key": "markostefan",
                "poznajuSe": True
            }
        }
    )

    #brisanje veze
    arango_actions.delete({"key": "markostefan", "collectionName": "testVeze"})

    #update veze
    arango_actions.update({"key": "markostefan", "collectionName": "testVeze", "document": {
        "updated": True,
    }})
    