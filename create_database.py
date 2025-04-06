import os
import argparse
from dotenv import load_dotenv
from pymilvus import DataType, MilvusClient, Function, FunctionType

# Tải các biến môi trường từ file .env
load_dotenv()

# Khởi tạo argparse để nhận tham số từ dòng lệnh
parser = argparse.ArgumentParser(description="Chọn client Milvus")
parser.add_argument('client_type', choices=['local', 'server'], help="Chọn loại client Milvus")
args = parser.parse_args()

# Chọn client dựa trên tham số dòng lệnh
if args.client_type == 'local':
    client = MilvusClient()
elif args.client_type == 'server':
    client = MilvusClient(
        uri=str(os.getenv('URL_MILVUS')), 
        token=str(os.getenv('TOKEN_MILVUS'))
    )

# Tiếp tục các bước còn lại trong mã của bạn

dimention = 768 
# dimention = 1024

# Tạo schema cho DOCUMENTS
schema_documents = client.create_schema(auto_id=False, enable_dynamic_field=True)
# Thêm các trường vào schema của DOCUMENTS
schema_documents.add_field(field_name="id", datatype=DataType.VARCHAR, max_length=255, is_primary=True)
schema_documents.add_field(field_name="name", datatype=DataType.VARCHAR, max_length=255)
schema_documents.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=dimention)  
schema_documents.add_field(field_name="file_name", datatype=DataType.VARCHAR, max_length=255)
print('Create schema for DOCUMENTS success')


# Tạo schema cho DOCUMENT_PARTS
schema_document_parts = client.create_schema(auto_id=False, enable_dynamic_field=True)
schema_document_parts.add_field(field_name="id", datatype=DataType.VARCHAR, max_length=255, is_primary=True)
schema_document_parts.add_field(field_name="rank", datatype=DataType.INT16, nullable=True) 
schema_document_parts.add_field(field_name="key", datatype=DataType.DOUBLE, nullable=True)
schema_document_parts.add_field(field_name="page", datatype=DataType.INT16, nullable=True)  
schema_document_parts.add_field(field_name="content", datatype=DataType.VARCHAR, max_length=65000, enable_analyzer=True)
schema_document_parts.add_field(field_name="parents_id", datatype=DataType.VARCHAR, max_length=255)
schema_document_parts.add_field(field_name="child_ids", datatype=DataType.ARRAY, element_type=DataType.VARCHAR, max_length=255, max_capacity=255, nullable=True)
schema_document_parts.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=dimention) 
schema_document_parts.add_field(field_name="sparse_vector", datatype=DataType.SPARSE_FLOAT_VECTOR) 
schema_document_parts.add_field(field_name="position", datatype=DataType.ARRAY, element_type=DataType.VARCHAR, max_length=255, max_capacity=255, nullable=True)
schema_document_parts.add_field(field_name="doc_id", datatype=DataType.VARCHAR, max_length=255)
bm25_function = Function(
    name="text_bm25_emb", # Function name
    input_field_names="content", # Name of the VARCHAR field containing raw text data
    output_field_names="sparse_vector", # Name of the SPARSE_FLOAT_VECTOR field reserved to store generated embeddings
    function_type=FunctionType.BM25,
)
schema_document_parts.add_function(bm25_function)
print('Create schema for DOCUMENT_PARTS success')


# Thêm các trường vào schema của QUESTIONS
schema_questions = client.create_schema(auto_id=False, enable_dynamic_field=True)
schema_questions.add_field(field_name="id", datatype=DataType.VARCHAR, max_length=255, is_primary=True)
schema_questions.add_field(field_name="content", datatype=DataType.VARCHAR, max_length=65000) # Câu hỏi
schema_questions.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=dimention) # Vector của câu hỏi
schema_questions.add_field(field_name="type", datatype=DataType.INT64, nullable=True) # Để lưu nhóm các câu hỏi tương tự chung 1 loại
schema_questions.add_field(field_name="rating", datatype=DataType.INT8, nullable=True) # Để lưu đánh giá chất lượng của câu trả lời
schema_questions.add_field(field_name="feedback", datatype=DataType.VARCHAR, max_length=65000, nullable=True) # Lưu phản hồi của người dùng
# schema_questions.add_field(field_name="answer_rating", datatype=DataType.ARRAY, element_type=DataType.JSON, max_length=5, max_capacity=5, nullable=True)
print('Create schema for QUESTIONS success')


"""
Để lưu đánh giá chất lượng của từng câu trả lời của hệ thống
Cấu trúc json
[
    {
        "id": "1",
        "rating": 4
    },
    {
        "id": "2",
        "rating": 1
    },
    {
        "id": "3",
        "rating": 5
    },
    {
        "id": "4",
        "rating": 2
    },
    {
        "id": "5",
        "rating": 5
    }
]
"""

# # Thêm các trường vào schema của ACCOUNTS
schema_accounts = client.create_schema(auto_id=False, enable_dynamic_field=True)
schema_accounts.add_field(field_name="id", datatype=DataType.VARCHAR, max_length=255, is_primary=True)
schema_accounts.add_field(field_name="email", datatype=DataType.VARCHAR, max_length=255)
schema_accounts.add_field(field_name="vector", datatype=DataType.SPARSE_FLOAT_VECTOR)
schema_accounts.add_field(field_name="password", datatype=DataType.VARCHAR, max_length=255)
# schema_accounts.add_field(field_name="otp", datatype=DataType.VARCHAR, max_length=10)
schema_accounts.add_field(field_name="role", datatype=DataType.INT8)
print('Create schema for ACCOUNTS success')


# Set index params cho DOCUMENTS, QUESTIONS
index_params1 = client.prepare_index_params()
index_params1.add_index(field_name="vector", index_type="IVF_FLAT", metric_type="COSINE", params={"nlist": 128})
print('Prepare index 1 success')

# Set index params cho ACCOUNTS
index_params2 = client.prepare_index_params()
index_params2.add_index(field_name="vector", index_type="SPARSE_INVERTED_INDEX", metric_type="IP", params={"nlist": 128})
print('Prepare index 2 success')

# Set index params cho DOCUMENT_PARTS
index_params3 = client.prepare_index_params()
index_params3.add_index(field_name="vector", index_type="IVF_FLAT", metric_type="COSINE", params={"nlist": 128})
index_params3.add_index(
    field_name="sparse_vector",
    index_name="sparse_inverted_index",
    index_type="SPARSE_INVERTED_INDEX", # Inverted index type for sparse vectors
    metric_type="BM25",
    params={
        "inverted_index_algo": "DAAT_MAXSCORE", # Algorithm for building and querying the index. Valid values: DAAT_MAXSCORE, DAAT_WAND, TAAT_NAIVE.
        "bm25_k1": 1.2,
        "bm25_b": 0.75
    }, 
)
print('Prepare index 3 success')

# Tạo collection cho DOCUMENTS
client.create_collection(collection_name="DOCUMENTS", schema=schema_documents, index_params=index_params1)
print('Create collection DOCUMENTS success')

# Tạo collection cho DOCUMENT_PARTS
client.create_collection(collection_name="DOCUMENT_PARTS", schema=schema_document_parts, index_params=index_params3)
print('Create collection DOCUMENT_PARTS success')

# Tạo collection cho QUESTIONS
client.create_collection(collection_name="QUESTIONS", schema=schema_questions, index_params=index_params1)
print('Create collection QUESTIONS success')

# Tạo collection cho ACCOUNTS
client.create_collection(collection_name="ACCOUNTS", schema=schema_accounts, index_params=index_params2)
print('Create collection ACCOUNTS success')
