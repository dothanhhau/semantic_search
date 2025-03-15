from pymilvus import connections, utility

# Kết nối đến Milvus
connections.connect("default", host="localhost", port="19530")

# Lấy danh sách tất cả collection
collections = utility.list_collections()

# Xóa từng collection
for collection in collections:
    utility.drop_collection(collection)
    print(f"Dropped collection: {collection}")

print("Done!")
