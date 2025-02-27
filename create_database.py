import os
from dotenv import load_dotenv
from pymilvus import DataType, MilvusClient

load_dotenv()

client = MilvusClient(
    uri=str(os.getenv('URL_MILVUS')), 
    token=str(os.getenv('TOKEN_MILVUS'))
)

schema_documents = client.create_schema(auto_id=False, enable_dynamic_field=True)

# Thêm các trường vào schema của DOCUMENTS
schema_documents.add_field(field_name="id", datatype=DataType.VARCHAR, max_length=255, is_primary=True)
schema_documents.add_field(field_name="name", datatype=DataType.VARCHAR, max_length=255)
schema_documents.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=768)  # Vector của DOCUMENTS.name
schema_documents.add_field(field_name="file_name", datatype=DataType.VARCHAR, max_length=255)

# Tạo schema cho collection DOCUMENT_PARTS
schema_document_parts = client.create_schema(auto_id=False, enable_dynamic_field=True)

# Thêm các trường vào schema của DOCUMENT_PARTS
schema_document_parts.add_field(field_name="id", datatype=DataType.VARCHAR, max_length=255, is_primary=True)
schema_document_parts.add_field(field_name="rank", datatype=DataType.INT16, nullable=True)  # Vector của DOCUMENT_PARTS.content
schema_document_parts.add_field(field_name="page", datatype=DataType.INT16, nullable=True)  # Vector của DOCUMENT_PARTS.content
schema_document_parts.add_field(field_name="content", datatype=DataType.VARCHAR, max_length=65000)
schema_document_parts.add_field(field_name="child_ids", datatype=DataType.ARRAY, element_type=DataType.VARCHAR, max_length=255, max_capacity=64, nullable=True, default_value=[])
schema_document_parts.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=768)  # Vector của DOCUMENT_PARTS.content
schema_document_parts.add_field(field_name="position", datatype=DataType.ARRAY, element_type=DataType.VARCHAR, max_length=255, max_capacity=64, nullable=True)
schema_document_parts.add_field(field_name="doc_id", datatype=DataType.VARCHAR, max_length=255)

# Set index params cho DOCUMENTS và DOCUMENT_PARTS
index_params = client.prepare_index_params()
index_params.add_index(field_name="vector", index_type="IVF_FLAT", metric_type="COSINE", params={"nlist": 128})

# Tạo collection cho DOCUMENTS
client.create_collection(collection_name="DOCUMENTS", schema=schema_documents, index_params=index_params)

# Tạo collection cho DOCUMENT_PARTS
client.create_collection(collection_name="DOCUMENT_PARTS", schema=schema_document_parts, index_params=index_params)