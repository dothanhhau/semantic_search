import os
import argparse
from dotenv import load_dotenv
from pymilvus import DataType, MilvusClient

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

# Tạo schema cho DOCUMENTS
schema_documents = client.create_schema(auto_id=False, enable_dynamic_field=True)

# Thêm các trường vào schema của DOCUMENTS
schema_documents.add_field(field_name="id", datatype=DataType.VARCHAR, max_length=255, is_primary=True)
schema_documents.add_field(field_name="name", datatype=DataType.VARCHAR, max_length=255)
schema_documents.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=768)  
schema_documents.add_field(field_name="file_name", datatype=DataType.VARCHAR, max_length=255)

# Tạo schema cho DOCUMENT_PARTS
schema_document_parts = client.create_schema(auto_id=False, enable_dynamic_field=True)

# Thêm các trường vào schema của DOCUMENT_PARTS
schema_document_parts.add_field(field_name="id", datatype=DataType.VARCHAR, max_length=255, is_primary=True)
schema_document_parts.add_field(field_name="rank", datatype=DataType.INT16, nullable=True) 
schema_document_parts.add_field(field_name="key", datatype=DataType.INT16, nullable=True)
schema_document_parts.add_field(field_name="page", datatype=DataType.INT16, nullable=True)  
schema_document_parts.add_field(field_name="content", datatype=DataType.VARCHAR, max_length=65000)
schema_document_parts.add_field(field_name="child_ids", datatype=DataType.ARRAY, element_type=DataType.VARCHAR, max_length=255, max_capacity=255, nullable=True)
schema_document_parts.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=768) 
schema_document_parts.add_field(field_name="position", datatype=DataType.ARRAY, element_type=DataType.VARCHAR, max_length=64, max_capacity=64, nullable=True)
schema_document_parts.add_field(field_name="doc_id", datatype=DataType.VARCHAR, max_length=255)

# Thêm các trường vào schema của QUESTIONS
# schema_questions = client.create_schema(auto_id=False, enable_dynamic_field=True)

# schema_questions.add_field(field_name="id", datatype=DataType.VARCHAR, max_length=255, is_primary=True)
# schema_questions.add_field(field_name="content", datatype=DataType.VARCHAR, max_length=65000) # Câu hỏi
# schema_questions.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=768) # Vector của câu hỏi
# schema_questions.add_field(field_name="type", datatype=DataType.INT64, nullable=True) # Để lưu nhóm các câu hỏi tương tự chung 1 loại
# schema_questions.add_field(field_name="rating", datatype=DataType.INT8, nullable=True) # Để lưu đánh giá chất lượng của câu trả lời
# schema_questions.add_field(field_name="feedback", datatype=DataType.VARCHAR, max_length=65000, nullable=True) # Lưu phản hồi của người dùng
# schema_questions.add_field(field_name="answer_rating", datatype=DataType.ARRAY, element_type=DataType.JSON, max_length=5, max_capacity=5, nullable=True)
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

# Set index params cho DOCUMENTS, DOCUMENT_PARTS, QUESTIONS
index_params = client.prepare_index_params()
index_params.add_index(field_name="vector", index_type="IVF_FLAT", metric_type="COSINE", params={"nlist": 128})

# Tạo collection cho DOCUMENTS
client.create_collection(collection_name="DOCUMENTS", schema=schema_documents, index_params=index_params)

# Tạo collection cho DOCUMENT_PARTS
client.create_collection(collection_name="DOCUMENT_PARTS", schema=schema_document_parts, index_params=index_params)

# Tạo collection cho QUESTIONS
# client.create_collection(collection_name="QUESTIONS", schema=schema_questions, index_params=index_params)

# # Thêm các trường vào schema của ACCOUNTS
schema_questions = client.create_schema(auto_id=False, enable_dynamic_field=True)

schema_questions.add_field(field_name="id", datatype=DataType.VARCHAR, max_length=255, is_primary=True)
schema_questions.add_field(field_name="email", datatype=DataType.VARCHAR, max_length=255)
schema_questions.add_field(field_name="vector", datatype=DataType.SPARSE_FLOAT_VECTOR)
schema_questions.add_field(field_name="password", datatype=DataType.VARCHAR, max_length=255)
schema_questions.add_field(field_name="otp", datatype=DataType.VARCHAR, max_length=10)
schema_questions.add_field(field_name="role", datatype=DataType.INT8)


index_params_sparse_vector = client.prepare_index_params()
index_params_sparse_vector.add_index(field_name="vector", index_type="SPARSE_INVERTED_INDEX", metric_type="IP", params={"nlist": 128})
# Tạo collection cho ACCOUNTS
client.create_collection(collection_name="ACCOUNTS", schema=schema_questions, index_params=index_params_sparse_vector)