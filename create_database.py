import os
from dotenv import load_dotenv
from pymilvus import FieldSchema, DataType, MilvusClient, CollectionSchema

load_dotenv()

client = MilvusClient(
    uri=str(os.getenv('URL_MILVUS')), 
    token=str(os.getenv('TOKEN_MILVUS'))
)

database_structure = {
    'DOCUMENTS': [
        FieldSchema(name='id', dtype=DataType.VARCHAR, max_length=255, is_primary=True), 
        FieldSchema(name='name', dtype=DataType.VARCHAR, max_length=255),
        FieldSchema(name='vector', dtype=DataType.FLOAT_VECTOR, dim=768), # Vector của DOCUMENTS.name
        FieldSchema(name='file_name', dtype=DataType.VARCHAR, max_length=255)
    ],
    'DOCUMENT_PARTS': [
        FieldSchema(name='id', dtype=DataType.VARCHAR, max_length=255, is_primary=True),
        FieldSchema(name="doc_id", dtype=DataType.VARCHAR, max_length=255),
        FieldSchema(name='content', dtype=DataType.VARCHAR, max_length=65000),
        FieldSchema(name='vector', dtype=DataType.FLOAT_VECTOR, dim=768), # Vector của DOCUMENT_PARTS.content
        FieldSchema(name='page', dtype=DataType.INT16, nullable=True), # Vector của DOCUMENT_PARTS.content
        FieldSchema(name='rank', dtype=DataType.INT16, nullable=True), # Vector của DOCUMENT_PARTS.content
        FieldSchema(name='position', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_length=255, max_capacity=64, nullable=True),
        FieldSchema(name='child_ids', dtype=DataType.ARRAY, element_type=DataType.VARCHAR, max_length=255, max_capacity=64, nullable=True),
    ],
}

index_params = MilvusClient.prepare_index_params()
index_params.add_index(
    field_name="vector",
    metric_type="COSINE",
    index_type="IVF_FLAT",
    index_name="vector_index",
    params={ "nlist": 128 }
)

# Create DOCUMENTS collection
fields = CollectionSchema(database_structure["DOCUMENTS"])
client.create_collection(collection_name="DOCUMENTS", schema=fields)
client.create_index(
    collection_name="DOCUMENTS",
    index_params=index_params
)

# Create DOCUMENT_PARTS collection
fields = CollectionSchema(database_structure["DOCUMENT_PARTS"])
client.create_collection(collection_name="DOCUMENT_PARTS", schema=fields)
client.create_index(
    collection_name="DOCUMENT_PARTS",
    index_params=index_params
)