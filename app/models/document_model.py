from app import client
from pymilvus.client.types import LoadState

class Document:
    name = "DOCUMENTS"

    @staticmethod
    def find_by_id(id):
        return client.get(collection_name="DOCUMENTS", ids=id, output_fields=['name'])

    @staticmethod
    def load_collection():
        try:
            checkLoadCollection = client.get_load_state(
                collection_name=Document.name
            )
            if checkLoadCollection['state'] != LoadState.Loaded:
                client.load_collection(
                    collection_name=Document.name
                )
            return True
        except Exception as e:
            print(f"Error loading collection: {e}")
            return False

    @staticmethod
    def release_collection():
        try:
            checkLoadCollection = client.get_load_state(
                collection_name=Document.name
            )
            if checkLoadCollection['state'] == LoadState.Loaded:
                client.release_collection(
                    collection_name=Document.name
                )
            return True
        except Exception as e:
            print(f"Error releasing collection: {e}")
            return False

    @staticmethod
    def insert(vector):
        try:
            client.insert(
                collection_name=Document.name,
                data=vector
            )
        except Exception as e:
            print(f"Error inserting single vector: {e}")
            return False

    @staticmethod
    def upsert(vector):
        try:
            client.insert(
                collection_name=Document.name,
                data=vector
            )
        except Exception as e:
            print(f"Error inserting single vector: {e}")
            return False

    @staticmethod
    def get_all():
        try:
            # Document.load_collection()
            return client.query(
                collection_name=Document.name,
                output_fields=["id", "name"],
                limit=100,
                )
        except Exception as e:
            print(f"Error getting all entities: {e}")
            return None
