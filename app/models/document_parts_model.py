from app import client
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
            return True
        except Exception as e:
            print(f"Error loading collection: {e}")
            return False

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
            return True
        except Exception as e:
            print(f"Error releasing collection: {e}")
            return False

    @staticmethod
    def release_partition(partition):
        try:
            while True:
                checkLoadCollection = client.get_load_state(
                    collection_name=DocumentParts.name,
                    partition_name=partition
                )
                if checkLoadCollection['state'] == LoadState.Loaded:
                    client.release_partitions(
                        collection_name=DocumentParts.name,
                        partition_names=[partition]
                    )
                else:
                    break
            return True
        except Exception as e:
            print(f"Error releasing collection: {e}")
            return False

    @staticmethod
    def find_by_id(id):
        return client.get(collection_name=DocumentParts.name, ids=id)

    @staticmethod
    def search_all(vector, k):
        try:
            res = client.search(
                collection_name=DocumentParts.name,
                data=vector,
                limit=k,
                output_fields=['content', 'page', 'position', 'doc_id']
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
                output_fields=['content', 'page', 'position', 'doc_id']
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
    def drop_partition(partition):
        try:
            if DocumentParts.release_partition(partition):
                client.drop_partition(
                    collection_name=DocumentParts.name,
                    partition_name=partition
                )
                return True
            else:
                return False
        except Exception as e:
            print('Err', e)
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
    def insert(data, partition):
        try:
            client.insert(
                collection_name=DocumentParts.name,
                data=data,
                partition_name=partition
            )
            return True
        except Exception as e:
            print(f"Error inserting single vector: {e}")
            return False

    @staticmethod
    def upsert(data, partition=''):
        try:
            if partition:
                client.upsert(
                    collection_name=DocumentParts.name,
                    data=data,
                    partition_name=partition
                )
                return True
            else:
                client.upsert(
                    collection_name=DocumentParts.name,
                    data=data
                )
        except Exception as e:
            print(f"Error inserting multiple vectors: {e}")
            return False

    @staticmethod
    def get_data_by_partition_id(partiton):
        try:
            filter_condition = f"doc_id == '{partiton}'"
            return client.query(
                collection_name=DocumentParts.name,
                filter=filter_condition,
                output_fields=['id', 'key', 'rank', 'content', 'page'],
                limit=1000,
            )
        except Exception as e:
            print(f"Error inserting multiple vectors: {e}")
            return []

    @staticmethod
    def delete_one_by_id(id):
        try:
            client.delete(
                collection_name=DocumentParts.name,
                ids=[id]
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
