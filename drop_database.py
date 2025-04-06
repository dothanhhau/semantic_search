from pymilvus import connections, utility
import os
import argparse
from dotenv import load_dotenv
from pymilvus import MilvusClient

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

# Lấy danh sách tất cả collection
collections = client.list_collections()

# Xóa từng collection
for collection in collections:
    client.drop_collection(
        collection_name=collection
    )
    print(f"Dropped collection: {collection}")

print("Done!")
