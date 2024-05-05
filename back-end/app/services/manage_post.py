# File for managaing posts to the server
import hashlib
import html
import uuid
import magic
import random
import json
import datetime
from fastapi import HTTPException, Depends, UploadFile
from app.core.database import MongoDataBase


# Gets the mimeType of a file based on fileBytes
def getMime(fileBytes):
    # Create an instance of Magic
    newMime = magic.Magic(mimeType=True)
    # Obtain mimeType from the fileBytes
    mimeType = newMime.from_buffer(fileBytes)
    return mimeType


class ManagePostService:
    randomOrderOfPosts = False

    def __init__(self, mongo_database: MongoDataBase = Depends()):
        self.db = mongo_database.db
        self.credentials_collection = mongo_database.get_collection("credentials")
        self.post_collection = mongo_database.get_collection("posts")

    # body contains something like: {"location": "Buffalo, NY", "description": "I went to Niagara Falls and it was awesome", "date": MM/YYYY, "xsrf":xsrf}
    # Body formatted in models/manage_post.py/PostModel
    # TODO: Use file
    def addPost(self, body, file: UploadFile, authToken: str):
        # Verify user exists
        validUser = self.validUser(authToken)
        if not validUser:
            raise HTTPException(status_code=404, detail="Invalid User")

        # Obtains username and creates an id for the post
        hashed_auth = validUser["hashed_auth"]
        user = self.credentials_collection.find_one({"hashed_auth": hashed_auth})
        username = user["username"]
        post_id = str(uuid.uuid4())

        # HTML escape any message from user
        location = html.escape(body.location)
        description = html.escape(body.description)
        # Might have to not do this if it is parsed as a datetime and not string
        date = html.escape(body.date)

        # if len(location) == 22 or len(date) == 9 or len(description) == 152:
        #     raise HTTPException(status_code=403, detail="Nice try")
        day=body.day
        if (day != ""):
            day=int(body.day)
            month=body.month
            year=body.year
            hour=body.hour
            minute=body.minute

            time=datetime.datetime(year, month, day, hour, minute)
            et_offset = datetime.timedelta(hours=-4)
            utc_current_time=datetime.datetime.now()
            current_time=utc_current_time + et_offset
            if (time > current_time):
                time_remaining=(time-current_time).total_seconds()
            else:
                time_remaining=0
        else:
            time=datetime.datetime.now()
        # If there's no file, obtain the noUpload.jpg
        mimeType = "text/plain"
        if file == None:
            mimeType == "image/jpeg"
            file_path = "app/static/images/noUpload.jpg"

        # If there is a file, get the mimeType and write the file
        else:
            file_path = f"app/static/images/{post_id}.jpg"
            with open(file_path, "wb") as f:
                contents = file.file.read()
                f.write(contents)
            file.file.close()

        # Insert content into database
        content = {
            "username": username,
            "id": post_id,
            "content": {"location": location, "description": description, "date": date},
            "likes": 0,
            "file_path": file_path,
            "mimeType": mimeType,
            "time_stamp":time,
            "time_remaning": time_remaining
        }

        self.post_collection.insert_one(content)
        del content["_id"]
        return content

    def likePost(self, post_id, auth_token: str):
        # Get post document
        post_document = self.post_collection.find_one({"id": post_id})
        # Check if it exists
        if not post_document:
            raise HTTPException(status_code=404, detail="Post Does Not Exists")
        # Check if valid user
        user = self.validUser(auth_token)
        if not user:
            raise HTTPException(status_code=404, detail="Invalid User")
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
            raise HTTPException(status_code=404, detail="Post Does Not Exists")
        # Check if valid user
        user = self.validUser(auth_token)
        if not user:
            raise HTTPException(status_code=404, detail="Invalid User")
        username = user["username"]
        # Should never be able to unlike a post without any likes
        if "users_liked" not in post_document:
            return {"post_id": post_id, "likes": 0, "like_status": False}
        users_liked = post_document["users_liked"]
        # Exception if user is not in liked list
        if username not in users_liked:
            return {"post_id": post_id, "likes": len(users_liked), "like_status": False}
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

    def listPosts(self):
        all_post = self.post_collection.find({})
        post_list = []

        for post in all_post:
            info = {}
            try:
                post_time=post["time_stamp"]
                print("scheduled post time: ", post_time)
            except:
                post_time=datetime.datetime.now()
            et_offset = datetime.timedelta(hours=-4)
            utc_current_time=datetime.datetime.now()
            current_time=utc_current_time + et_offset
            print("current time: ", current_time)
            if post_time <= current_time:
                info["username"] = post["username"]
                info["id"] = post["id"]
                info["content"] = post["content"]
                info["likes"] = post["likes"]
                info["file"] = post["file_path"]
                post_list.append(info)

        # json_list = json.dumps(post_list)

        # If the user clicked the random button, randomize the posts
        if self.randomOrderOfPosts:
            random.shuffle(post_list)

        # [::-1] reverses the list
        return post_list[::-1]

    # Radomizes posts for the PP3 Creativity - call only when user hits radomize button
    def randomizePosts(self):
        # Determine if the list should be randomized or unrandomized
        self.randomOrderOfPosts = not self.randomOrderOfPosts
        post_list = self.listPosts()

        if self.randomOrderOfPosts:
            random.shuffle(post_list)
        return post_list
