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
if args.client_type == 'server':
    client = MilvusClient(
        uri=str(os.getenv('URL_MILVUS')), 
        token=str(os.getenv('TOKEN_MILVUS'))
    )
else:
    client = MilvusClient()

client.drop_collection(
    collection_name='DOCUMENTS'
)

client.drop_collection(
    collection_name='DOCUMENT_PARTS'
)

client.drop_collection(
    collection_name='QUESTIONS'
)
