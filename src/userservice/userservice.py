from fastapi import FastAPI
import json
import mysql.connector
from pprint import pprint
import hashlib, uuid

app = FastAPI()
salt = uuid.uuid4().hex

database = mysql.connector.connect(
    host='krishusdata.mysql.database.azure.com',
    user='kmg',
    password='krissupersecretpassword0!',
    database='UserService',
)

cursor = database.cursor()

def ExecuteQuery(query, parameters):
    cursor.execute(query, parameters)
    database.commit()

@app.post("/insertUserInfo/")
def InsertUserInfo(username, password, gender, mail, birthdate, creationdate):
    if(username == None or password == None or gender == None or mail == None or birthdate == None or creationdate == None):
        return
    hashed_password = hashlib.sha512((password + salt).encode('utf-8')).hexdigest()
    ExecuteQuery("INSERT INTO userInfo VALUES(0, %s, %s, %s, %s, %s, %s)",(username, hashed_password, gender, mail, birthdate, creationdate))

InsertUserInfo('hej1', 'hej2', 'det', 'hej1@hej2.com', '1999-12-03 12:31:00', '1999-12-03 12:31:00')

@app.post("/deleteUser/")
def DeleteUser(userID):
    if(userID == None):
        return
    ExecuteQuery("DELETE FROM userInfo WHERE id=%s", (userID,))

#DeleteUser(4)

@app.get("/getUserInfo/")
def GetUser(userID):
    
    data = {
        "userInfo": []
    }
    cursor.execute("SELECT username, gender, mail, birthdate, creationdate FROM userInfo WHERE id=%s", (userID,))
    userResult = cursor.fetchone()
    username = userResult[0]
    gender = userResult[1]
    mail = userResult[2]
    birthdate = userResult[3]
    creationdate = userResult[4]
    data["userInfo"].append({"username": username, "gender": gender, "mail": mail, "birthdate": birthdate, "creationdate": creationdate})
    
    return data

pprint(GetUser(1))