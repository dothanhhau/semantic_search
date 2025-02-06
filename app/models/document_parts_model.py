from app.__init__ import client
from pymilvus.client.types import LoadState

class DocumentParts:
    name = 'DOCUMENT_PARTS'

    @staticmethod
    def load_collection():
        try:
            checkLoadCollection = client.get_load_state(
                collection_name=DocumentParts.name
            )
            if checkLoadCollection['state'] != LoadState.Loaded:
                client.load_collection(
                    collection_name=DocumentParts.name
                )
        except Exception as e:
            print(f"Error loading collection: {e}")

    @staticmethod
    def release_collection():
        try:
            checkLoadCollection = client.get_load_state(
                collection_name=DocumentParts.name
            )
            if checkLoadCollection['state'] == LoadState.Loaded:
                client.release_collection(
                    collection_name=DocumentParts.name
                )
        except Exception as e:
            print(f"Error releasing collection: {e}")

    @staticmethod
    def search_all(vector, k):
        try:
            res = client.search(
                collection_name=DocumentParts.name,
                data=vector,
                limit=k,
                output_fields=['content']
            )
            return res
        except Exception as e:
            print(f"Error during search: {e}")
            return []

    @staticmethod
    def search_on_partition(vector, partition, k):
        try:
            res = client.search(
                collection_name=DocumentParts.name,
                partition_names=partition,
                data=vector,
                limit=k,
                output_fields=['content']
            )
            return res
        except Exception as e:
            print(f"Error during partitioned search: {e}")
            return []

    @staticmethod
    def create_partition(partition):
        try:
            client.create_partition(
                collection_name=DocumentParts.name,
                partition_name=partition,
            )
            return True
        except Exception as e:
            print(f"Error creating partition: {e}")
            return False

    @staticmethod
    def get_children(id):
        return ''

    @staticmethod
    def get_parents(id):
        return ''

    @staticmethod
    def get_document_id(id):
        return ''

    @staticmethod
    def delete_partition(partition):
        try:
            client.drop_partition(
                collection_name=DocumentParts.name,
                partition_name=partition,
            )
            return True
        except Exception as e:
            print(f"Error deleting partition: {e}")
            return False

    @staticmethod
    def insert_one(vector, partition):
        try:
            client.insert(
                collection_name=DocumentParts.name,
                data=[vector],
                partition_name=partition
            )
            return True
        except Exception as e:
            print(f"Error inserting single vector: {e}")
            return False

    @staticmethod
    def insert_many(vectors, partition):
        try:
            client.upsert(
                collection_name=DocumentParts.name,
                data=vectors,
                partition_name=partition
            )
            return True
        except Exception as e:
            print(f"Error inserting multiple vectors: {e}")
            return False

    @staticmethod
    def delete_one_by_id(id):
        try:
            client.delete(
                collection_name=DocumentParts.name,
                expr=f'id == {id}'
            )
            return True
        except Exception as e:
            print(f"Error deleting document by ID: {e}")
            return False

    @staticmethod
    def delete_many_by_ids(ids):
        try:
            conditions = ' OR '.join([f'id == {id}' for id in ids])
            client.delete(
                collection_name=DocumentParts.name,
                expr=conditions
            )
            return True
        except Exception as e:
            print(f"Error deleting multiple documents by IDs: {e}")
            return False

    @staticmethod
    def delete_one(vector, partition):
        try:
            client.delete(
                collection_name=DocumentParts.name,
                expr=f'vector == {vector}',
                partition_name=partition
            )
            return True
        except Exception as e:
            print(f"Error deleting single vector: {e}")
            return False

    @staticmethod
    def delete_many(vectors, partition):
        try:
            conditions = ' OR '.join([f'vector == {vector}' for vector in vectors])
            client.delete(
                collection_name=DocumentParts.name,
                expr=conditions,
                partition_name=partition
            )
            return True
        except Exception as e:
            print(f"Error deleting multiple vectors: {e}")
            return False
