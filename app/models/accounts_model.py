from app import client
from app.utils.hashing import hash_password, verify_password
from uuid import uuid1
from pymilvus.client.types import LoadState

class AccountModel:
    name = "ACCOUNTS"

    @classmethod
    def create_account(cls, account):
        cls.load_collection()

        account = {
            "id": str(uuid1()),
            "email": account["email"],
            "password": account["password"],
            "role": int(account["role"]),
            "vector": {0: 0.0},  # Placeholder for future vector data
            "otp": ""
        }
        return client.insert(cls.name, [account])

    @staticmethod
    def load_collection():
        try:
            checkLoadCollection = client.get_load_state(
                collection_name=AccountModel.name
            )
            if checkLoadCollection['state'] != LoadState.Loaded:
                client.load_collection(
                    collection_name=AccountModel.name
                )
            return True
        except Exception as e:
            print(f"Error loading collection: {e}")
            return False

    @staticmethod
    def release_collection():
            try:
                checkLoadCollection = client.get_load_state(
                    collection_name=AccountModel.name
                )
                if checkLoadCollection['state'] == LoadState.Loaded:
                    client.release_collection(
                        collection_name=AccountModel.name
                    )
                return True
            except Exception as e:
                print(f"Error releasing collection: {e}")
                return False

    @classmethod
    def find_by_email(cls, email: str):
        cls.load_collection()
        result = client.query(cls.name, filter=f'email == "{email}"')
        return result[0] if result else None

    @classmethod
    def verify_credentials(cls, email: str, password: str):
        cls.load_collection()
        account = cls.find_by_email(email)
        if account and verify_password(password, account["password"]):
            return account
        return None

    @classmethod
    def update_account(cls, email: str, update_data: dict):
        cls.load_collection()
        return client.update(cls.name, filter=f'email == "{email}"', update=update_data)

    @classmethod
    def delete_account(cls, email: str):
        cls.load_collection()
        return client.delete(cls.name, filter=f'email == "{email}"')
