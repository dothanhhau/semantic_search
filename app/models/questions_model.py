from app import client
from pymilvus.client.types import LoadState

class Questions:
    name = "QUESTIONS"

    @staticmethod
    def find_by_id(id):
        return client.get(collection_name=Questions.name, ids=id)

    @staticmethod
    def delete_by_id(id):
        try:
            client.delete(
                collection_name=Questions.name,
                ids=[id]
            )
            return True
        except Exception as e:
            print('Err', e)
            return False

    @staticmethod
    def load_collection():
        try:
            checkLoadCollection = client.get_load_state(
                collection_name=Questions.name
            )
            if checkLoadCollection['state'] != LoadState.Loaded:
                client.load_collection(
                    collection_name=Questions.name
                )
            return True
        except Exception as e:
            print(f"Error loading collection: {e}")
            return False

    @staticmethod
    def release_collection():
        try:
            checkLoadCollection = client.get_load_state(
                collection_name=Questions.name
            )
            if checkLoadCollection['state'] == LoadState.Loaded:
                client.release_collection(
                    collection_name=Questions.name
                )
            return True
        except Exception as e:
            print(f"Error releasing collection: {e}")
            return False

    @staticmethod
    def insert(data):
        try:
            client.insert(
                collection_name=Questions.name,
                data=data
            )
            return True
        except Exception as e:
            print(f"Error inserting vector: {e}")
            return False

    @staticmethod
    def upsert(data):
        try:
            client.upsert(
                collection_name=Questions.name,
                data=data
            )
            return True
        except Exception as e:
            print(f"Error upserting vector: {e}")
            return False

    @staticmethod
    def search_vector(vector, k=5):
        try:
            return client.search(
                collection_name=Questions.name,
                data=vector,
                limit=k
            )
        except Exception as e:
            print(f"Error upserting vector: {e}")
            return []

    @staticmethod
    def get_all():
        try:
            # Questions.load_collection()
            return client.query(
                collection_name=Questions.name,
                limit=100,
            )
        except Exception as e:
            print(f"Error getting all entities: {e}")
            return []
