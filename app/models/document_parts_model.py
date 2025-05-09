from app import client
from pymilvus.client.types import LoadState
from pymilvus import AnnSearchRequest, WeightedRanker

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
        return client.get(
            collection_name=DocumentParts.name, 
            ids=id,
            # output_fields=['content', 'page', 'position', 'doc_id', 'rank']
        )

    @staticmethod
    def find_parent_id_has_rank_el_4(id):
        x = DocumentParts.find_by_id(id)
        if len(x):
            x = x[0]
            x['vector'] = []
            if (x['id'] == x['parents_id']) or (x['rank'] < 5):
                return x
            else:
                return DocumentParts.find_parent_id_has_rank_el_4(x['parents_id'])
        else:
            return {}

    @staticmethod
    def get_all_child_by_id(id):
        x = DocumentParts.find_by_id(id)
        res = []
        if len(x):
            x = x[0]
            x.pop('vector', None)
            res.append(x)
            # x['child_ids'] = list(x['child_ids'])
            if len(x['child_ids']):
                for y in x['child_ids']:
                    u = DocumentParts.get_all_child_by_id(y)
                    res += u

        return res
    
    @staticmethod
    def get_childs(id, id_child):
        id = str(id)
        data = DocumentParts.get_all_child_by_id(id)
        res = sorted(data, key=lambda x: x['key'])
        content = ''
        for x in res:
            if x['id'] == id_child:
                content += f'<mark>{x['content']}</mark>'
            else:
                content += x['content']
            content += '\n'
        parents = res[0]

        return {
            'id': parents['id'],
            'content': content,
            'doc_id': parents['doc_id'],
            'page': parents['page'],
            'position': parents['position']
        }

    @staticmethod
    def search_all(vector, k, next=0):
        try:
            res = client.search(
                collection_name=DocumentParts.name,
                data=vector,
                limit=k,
                anns_field='vector',
                output_fields=['content', 'page', 'position', 'doc_id', 'rank'],
                search_params= {
                    'offset': next
                }
            )
            return res
        except Exception as e:
            print(f"Error during search: {e}")
            return []

    @staticmethod
    def search_on_partition(vector, partition, k, next=0):
        try:
            res = client.search(
                collection_name=DocumentParts.name,
                partition_names=partition,
                data=vector,
                anns_field='vector',
                limit=k,
                output_fields=['content', 'page', 'position', 'doc_id', 'rank'],
                search_params= {
                    'offset': next
                }
            )
            return res
        except Exception as e:
            print(f"Error during partitioned search: {e}")
            return []

    @staticmethod
    def full_text_search(text, partition, k, next=0):
        search_params = {
            'params': {'drop_ratio_search': 0.2}, # Proportion of small vector values to ignore during the search
            'offset': next
        }
        
        return client.search(
            collection_name=DocumentParts.name, 
            partition_names=partition,
            data=text,
            anns_field='sparse_vector',
            limit=k,
            search_params=search_params,
            output_fields=['content', 'page', 'position', 'doc_id', 'rank'],
        )
    
    def hybrid_search(vector, text, partition, k, next=0):

        search_param_1 = {
            "data": vector,
            "anns_field": "vector",
            "param": {
                "metric_type": "COSINE",
                "params": {"nprobe": 10}
            },
            "limit": 25
        }
        request_1 = AnnSearchRequest(**search_param_1)

        search_param_2 = {
            "data": text,
            "anns_field": "sparse_vector",
            "param": {
                "metric_type": "BM25",
            },
            "limit": 25
        }
        request_2 = AnnSearchRequest(**search_param_2)

        reqs = [request_1, request_2]
        ranker = WeightedRanker(0.8, 0.3) 
        res = client.hybrid_search(
            collection_name=DocumentParts.name,
            partition_names=partition,
            reqs=reqs,                
            ranker=ranker,
            limit=k,
            output_fields=['content', 'page', 'position', 'doc_id', 'rank'],
            search_params= {
                'offset': next
            }
        )
        return res

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
            check = client.has_partition(
                collection_name=DocumentParts.name,
                partition_name=partition
            )
            if check:
                if DocumentParts.release_partition(partition):
                    client.drop_partition(
                        collection_name=DocumentParts.name,
                        partition_name=partition
                    )
                    return True
                else:
                    return False
            else:
                return True
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
                return True
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
                output_fields=['id', 'key', 'rank', 'content', 'page', 'parents_id'],
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
