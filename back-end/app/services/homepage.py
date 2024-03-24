from fastapi import Depends
from fastapi.security import HTTPCookie
from app.core.database import MongoDataBase
import hashlib



class Homepage:
    def __init__(self, mongo_database: MongoDataBase = Depends()):
        self.db = mongo_database.db
        self.credentials_collection = mongo_database.get_collection("credentials")

    def checkUser(self, auth_token: str = HTTPCookie(alias="auth_token")):
        if not auth_token:
            return False

        hashed_auth = hashlib.sha256(auth_token.encode()).hexdigest()
        user_document = self.credentials_collection.find_one({"hashed_auth": hashed_auth})
        return bool(user_document)

