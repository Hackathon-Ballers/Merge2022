from dataclasses import dataclass
import sqlite3

@dataclass
class User:
    id:int
    pfp:str #idk if this is the right name
    username:str
    password:str
    bio: str

def getAllUsers():
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("SELECT userId, pfp, username, password, bio FROM Users")
    users = []
    for user in c.fetchall():
        users.append(User(id=user[0], pfp=user[1], username=user[2], password=user[3], bio=user[4]))
    conn.close()
    return users

def getUserById(id):
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("SELECT userId, pfp, username, password, bio FROM Users WHERE userId=?", (id,))
    user = c.fetchone()
    conn.close()
    return User(id=user[0], pfp=user[1], username=user[2], password=user[3], bio=user[4])

def getUser(username):
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("SELECT userId, pfp, username, password, bio FROM Users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return User(id=user[0], pfp=user[1], username=user[2], password=user[3], bio=user[4])

def createNewUser(pfp, username, password, bio):
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("INSERT INTO Users (pfp, username, password, bio) VALUES (?, ?, ?, ?)", (pfp, username, password, bio))
    conn.commit()
    conn.close()
    return getUser(username)

if __name__ == "__main__":
    for user in getAllUsers():
        print(user)
    pfp = input("pfp: ")
    username = input("username: ")
    password = input("password: ")
    bio = input("bio: ")
    createNewUser(pfp, username, password)
