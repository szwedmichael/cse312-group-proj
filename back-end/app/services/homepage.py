from fastapi import Depends, Response
from fastapi.responses import JSONResponse
from app.core.database import MongoDataBase
import hashlib


class HomepageService:
    def __init__(self, mongo_database: MongoDataBase = Depends()):
        self.db = mongo_database.db
        self.credentials_collection = mongo_database.get_collection("credentials")

    def checkUser(self, auth_token: str):
        if not auth_token:
            return {"isAuthenticated": False}

        hashed_auth = hashlib.sha256(auth_token.encode()).hexdigest()
        user_document = self.credentials_collection.find_one(
            {"hashed_auth": hashed_auth}
        )
        return {"isAuthenticated": bool(user_document)}
