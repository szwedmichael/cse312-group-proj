#File for Registering and Loggins For Users
from pymongo import MongoClient
import bcrypt
import hashlib
import secrets


mongo_client=MongoClient("mongo")
#Collections(so far): "credentials"
db=mongo_client["Vacationhub"]

#Regsiter User given username and two passwords entered
def registerUser(username, password1, password2):
    #Make sure passwords match
    if password1 != password2:
        return forbidden()
    #arbitrarily use password1
    password=password1
    #Make sure password is valid
    if passwordNotValid(password):
        return forbidden()
    #Check if username already exist
    if usernameExist(username):
        return forbidden()
    
    #Hash password with salt
    salt=bcrypt.gensalt()
    hashed_password=bcrypt.hashpw(password.encode(), salt)
    #Create XSFR token
    xsfr=secrets.token_hex(32)
    #Open database
    credentials_collection=db["credentials"]
    #Create dictionaty to insert into database
    to_insert={}
    to_insert["username"]=username
    to_insert["hashed_password"]=hashed_password
    to_insert["xsfr"]=xsfr

    #Insert credentials
    credentials_collection.insert_one(to_insert)
    return found()

def passwordNotValid(password):
    #All passwords valid
    return False

#Return whether or not that username is in use
def usernameExist(username):
    credentials_collection=db["credentials"]
    user=credentials_collection.find_one({"username":username})
    if user:
        return True
    return False

#TODO Add password requirements
#TODO Add 403 forbidden and 302 Found function; can add paramters if necessary

def loginUser(username, password):
    pass

def logoutUser(auth_token):
    pass