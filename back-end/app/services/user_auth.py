#File for Registering and Loggins For Users
from pymongo import MongoClient
import bcrypt
import hashlib
import secrets


CRLF="\r\n"
nosniff="X-Content-Type-Options: nosniff"+CRLF +CRLF


mongo_client=MongoClient("mongo")
#Collections(so far): "credentials"
db=mongo_client["Vacationhub"]

#Regsiter User given username and two passwords entered
def registerUser(username, password1, password2):
    #Make sure passwords match
    if password1 != password2:
        return serve403("Passwords do not match")
    #arbitrarily use password1
    password=password1
    #Make sure password is valid
    if passwordNotValid(password):
        return serve403("Password does fit requirements")
    #Check if username already exist
    if usernameExist(username):
        return serve403("Username already exists")
    
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
    to_insert["salt"]=salt
    to_insert["xsfr"]=xsfr

    #Insert credentials
    credentials_collection.insert_one(to_insert)
    return serve302()

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

def loginUser(username, password):
    pass

def logoutUser(auth_token):
    credentials_collection=db["credentials"]
    #check if auth token is not None
    if auth_token:
        #Hash auth
        hashed_auth=hashlib.sha256(auth_token.encode()).hexdigest()
        #find user docuement; fix key name and auth_token
        user=credentials_collection.find_one({"hashed_auth":hashed_auth})
        if user:
            username=user["username"]
            #Unset auth in data base
            credentials_collection.update_one({"username":username}, {'$unset': {"hashed_auth": ''}})
            serve302()
    serve403("Invalid Logout Request")

#Forbidden Response
def serve403(message):
    global CRLF
    global nosniff
    status="HTTP/1.1 403 Forbidden" +CRLF
    content_type="Content-Type: text/plain" +CRLF
    body=message.encode()
    content_lentgh="Content-Length: " + str(len(body))+CRLF

    return (status + content_type + content_lentgh + nosniff).encode()+body

#Found Response
def serve302():
    global CRLF
    global nosniff
    status="HTTP/1.1 302 Found" +CRLF
    #Location to go after signing in; to be changed
    location="Location: /"+CRLF

    return (status + location + nosniff).encode()


