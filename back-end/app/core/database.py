from pymongo import MongoClient


class MongoDataBase:
    def __init__(self):
        self.client = MongoClient("mongo")
        self.db = self.client["Vacationhub"]

    def get_collection(self, collection_name: str):
        return self.db[collection_name]

    def close(self):
        self.client.close()
