# File for managaing posts to the server
import hashlib
import html
import uuid
from fastapi import HTTPException, Depends
from app.core.database import MongoDataBase


class ManagePostService:

    def __init__(self, mongo_database: MongoDataBase = Depends()):
        self.db = mongo_database.db
        self.credentials_collection = mongo_database.get_collection("credentials")
        self.post_collection = mongo_database.get_collection("posts")

    # body contains something like: {"location": "Buffalo, NY", "description": "I went to Niagara Falls and it was awesome", "date": MM/YYYY, "xsrf":xsrf}
    def addPost(self, htmlXSRF, body, authToken: str):
        # Verify user exists
        validUser = self.validUser(authToken)
        if not validUser:
            return HTTPException(status_code=404, detail="Invalid User")

        # Obtains username and creates an id for the post
        user = self.credentials_collection.find_one({"hashed_auth": validUser})
        username = user["username"]
        post_id = uuid.uuid4()

        # Obtains XSRF tokens
        userXSRF = user["xsrf"]

        # Verifies XSRF tokens
        if userXSRF != htmlXSRF:
            return HTTPException(status_code=403, detail="Post Rejected!")

        # HTML escape any message from user
        location = html.escape(body.location)
        description = html.escape(body.description)
        # Might have to not do this if it is parsed as a datetime and not string
        date = html.escape(body.date)

        # Insert content into database
        content = {
            "username": username,
            "id": post_id,
            "content": {"location": location, "description": description, "date": date},
        }
        self.post_collection.insert_one(content)

        return content

    def likePost(self, post_id, auth_token: str):
        # Get post document
        post_document = self.post_collection.find_one({"id": post_id})
        # Check if it exists
        if not post_document:
            return HTTPException(status_code=404, detail="Post Does Not Exists")
        # Check if valid user
        user = self.validUser(auth_token)
        if not user:
            return HTTPException(status_code=404, detail="Invalid User")
        username = user["username"]
        # Check if list of users who interacted already exists
        if "users_liked" in post_document:
            # Get users that liked the post
            users_liked = post_document["users_liked"]
            # If user is not in list add them
            if username not in post_document["users_liked"]:
                users_liked.append(username)
        else:
            # Else Assume this user is the first like
            users_liked = [username]
        # Get number of likes
        likes = len(users_liked)
        # Set list of users and number of likes
        self.post_collection.update_one(
            {"id": post_id}, {"$set": {"users_liked": users_liked, "likes": likes}}
        )

        return {"post_id": post_id, "likes": likes, "like_status": True}

    def unlikePost(self, post_id, auth_token: str):
        # Get post document
        post_document = self.post_collection.find_one({"id": post_id})
        # Check if it exists
        if not post_document:
            return HTTPException(status_code=404, detail="Post Does Not Exists")
        # Check if valid user
        user = self.validUser(auth_token)
        if not user:
            return HTTPException(status_code=404, detail="Invalid User")
        username = user["username"]
        # Should never be able to unlike a post without any likes
        if "users_liked" not in post_document:
            return HTTPException(status_code=403, detail="There are Already Zero Likes")
        users_liked = post_document["users_liked"]
        # Exception if user is not in liked list
        if username not in users_liked:
            return HTTPException(status_code=404, detail="User Never Liked")
        users_liked.remove(username)
        likes = len(users_liked)
        # Update users liked and number of likes
        self.post_collection.update_one(
            {"id": post_id}, {"$set": {"users_liked": users_liked, "likes": likes}}
        )

        return {"post_id": post_id, "likes": likes, "like_status": False}

    def validUser(self, auth_token):
        if auth_token:
            hashed_auth = hashlib.sha256(auth_token.encode()).hexdigest()
            # find user docuement and return it
            return self.credentials_collection.find_one({"hashed_auth": hashed_auth})
        # Else return None
        return None
