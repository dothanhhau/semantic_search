from pymilvus import MilvusClient

# Kết nối đến Milvus
client = MilvusClient()

collections = client.list_collections()

for x in collections:
    COLLECTION_NAME = x
    # Kiểm tra collection đã tồn tại chưa
    if client.has_collection(COLLECTION_NAME):
        # Kiểm tra trạng thái load
        state = client.get_load_state(collection_name=COLLECTION_NAME)

        if state != "Loaded":
            print(f"Loading collection: {COLLECTION_NAME}...")
            client.load_collection(collection_name=COLLECTION_NAME) 
            print(f"Collection {COLLECTION_NAME} is now loaded.")
        else:
            print(f"Collection {COLLECTION_NAME} is already loaded.")
    else:
        print(f"Collection {COLLECTION_NAME} does not exist!")
