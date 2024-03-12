#File for managaing posts to the server
import hashlib
from fastapi import HTTPException, Depends
from app.core.database import MongoDataBase

class ManagePostService:

    def __init__(self,mongo_database: MongoDataBase = Depends()):
        self.db = mongo_database.db
        self.credentials_collection = mongo_database.get_collection("credentials")
        self.post_collection = mongo_database.get_collection("posts")

    def addPost(self):
        #THINGS TO KEEP IN MIND
        #create a unique id for each post
        #keep track of who posted it
        pass

    def likePost(self, post_id, auth_token):
        #Get post document
        post_document=self.post_collection.find_one({"id":post_id})
        #Check if it exists
        if not post_document:
            return HTTPException(status_code=404, detail="Post Does Not Exists")
        #Check if valid user
        user=self.validUser(auth_token)
        if not user:
            return HTTPException(status_code=404, detail="Invalid User")
        username=user["username"]
        #Check if list of users who interacted already exists
        if "users_liked" in post_document:
            #Get users that liked the post
            users_liked=post_document["users_liked"]
            #If user is not in list add them
            if username not in post_document["users_liked"]:
                users_liked.append(username)
        else:
            #Else Assume this user is the first like
            users_liked=[username]
        #Get number of likes
        likes=len(users_liked)
        #Set list of users and number of likes
        self.post_collection.update_one(
            {"id":post_id, "$set":{"users_liked":users_liked, "likes":likes}}
            )
        
        return {"likes":likes}


    def unlikePost(self, post_id, auth_token):
        #Get post document
        post_document=self.post_collection.find_one({"id":post_id})
        #Check if it exists
        if not post_document:
            return HTTPException(status_code=404, detail="Post Does Not Exists")
        #Check if valid user
        user=self.validUser(auth_token)
        if not user:
            return HTTPException(status_code=404, detail="Invalid User")
        username=user["username"]
        #Should never be able to unlike a post without any likes
        if "users_liked" not in post_document:
            return HTTPException(status_code=403, detail="There are Already Zero Likes")
        users_liked=post_document["users_liked"]
        #Exception if user is not in liked list
        if username not in users_liked:
            return HTTPException(status_code=404, detail="User Never Liked")
        users_liked.remove(username)
        likes=len(users_liked)
        #Update users liked and number of likes
        self.post_collection.update_one(
            {"id":post_id, "$set":{"users_liked":users_liked, "likes":likes}}
            )
        return {"likes":likes}
        

    def validUser(self,auth_token):
        if auth_token:
            hashed_auth = hashlib.sha256(auth_token.encode()).hexdigest()
            # find user docuement and return it
            return self.credentials_collection.find_one({"hashed_auth": hashed_auth})
        #Else return None
        return None
            
    
