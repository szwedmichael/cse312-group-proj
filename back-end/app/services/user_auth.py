# File for Registering and Loggins For Users
import bcrypt
import hashlib
import secrets
import uuid
from fastapi.responses import RedirectResponse
from fastapi import HTTPException, Depends
from app.core.database import MongoDataBase


class UserAuthService:
    def __init__(self, mongo_database: MongoDataBase = Depends()):
        self.db = mongo_database.db
        self.credentials_collection = mongo_database.get_collection("credentials")

    # Regsiter User given username and two passwords entered
    def registerUser(self, username, password1, password2):
        # Make sure passwords match
        if password1 != password2:
            raise HTTPException(status_code=403, detail="Passwords do not match")
        # arbitrarily use password1
        password = password1
        # Make sure password is valid
        if self.passwordNotValid(password):
            raise HTTPException(
                status_code=403, detail="Password does fit requirements"
            )
        # Check if username already exist
        if self.usernameExist(username):
            raise HTTPException(status_code=403, detail="Username already exists")

        # Hash password with salt
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt)
        # Create XSRF token
        xsrf = secrets.token_hex(32)
        # Create dictionaty to insert into database
        to_insert = {}
        to_insert["username"] = username
        to_insert["hashed_password"] = hashed_password
        to_insert["salt"] = salt
        to_insert["xsrf"] = xsrf

        # Insert credentials
        self.credentials_collection.insert_one(to_insert)
        return RedirectResponse(url="/", status_code=302)

    def passwordNotValid(self, password):
        # All passwords valid
        return False

    # Return whether or not that username is in use
    def usernameExist(self, username):
        user = self.credentials_collection.find_one({"username": username})
        if user:
            return True
        return False

    # TODO Add password requirements

    # Login user based on valid credentials
    def loginUser(self, username, password):
        allUsers = self.credentials_collection.find()

        # Insert authToken to a user who matches username and password
        for user in allUsers:
            # Match the username
            if username == user["username"]:
                matchedPasswords = bcrypt.checkpw(
                    password.encode(), user["hashed_password"]
                )

                # Match passwords
                if matchedPasswords:

                    # Generate random authToken, and get the hash of the authToken
                    authTokenValue = uuid.uuid4()
                    authToken = str(authTokenValue)
                    hashedAuthToken = hashlib.sha256(authToken.encode()).hexdigest()

                    # Update user profile in database with hashed_auth token
                    newContent = {
                        "username": username,
                        "hashed_password": user["hashed_password"],
                        "salt": user["salt"],
                        "xsrf": user["xsrf"],
                        "hashed_auth": hashedAuthToken,
                    }
                    self.credentials_collection.delete_one(user)
                    self.credentials_collection.insert_one(newContent)

                    # Redirect user back to home page with the set auth_token cookie
                    returnResponse = RedirectResponse(url="/", status_code=302)
                    returnResponse.set_cookie(
                        "auth_token", authToken, max_age=4000, httponly=True
                    )
                    return returnResponse

        # Any invalid login request will have a 403 response with invalid credentials
        raise HTTPException(status_code=403, detail="Invalid credentials")

    def logoutUser(self, auth_token: str):
        # check if auth token is not None
        if auth_token:
            # Hash auth
            hashed_auth = hashlib.sha256(auth_token.encode()).hexdigest()
            # find user docuement; fix key name and auth_token
            user = self.credentials_collection.find_one({"hashed_auth": hashed_auth})
            if user:
                username = user["username"]
                # Unset auth in data base
                self.credentials_collection.update_one(
                    {"username": username}, {"$unset": {"hashed_auth": ""}}
                )
                return RedirectResponse(url="/", status_code=302)
        raise HTTPException(status_code=403, detail="Invalid Logout Request")
