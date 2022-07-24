from dataclasses import dataclass
import sqlite3
from post import Post

@dataclass
class User:
    id:int
    pfp:str #idk if this is the right name
    username:str
    password:str
    bio: str
    education: str = ""
    total_posts: int = 0

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
    c.execute("SELECT userId, pfp, username, password, bio, education FROM Users WHERE userId=?", (id,))
    user = c.fetchone()
    if not user: return None
    conn.close()
    return User(id=user[0], pfp=user[1], username=user[2], password=user[3], bio=user[4], education=user[5])

def getUser(username):
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("SELECT userId, pfp, username, password, bio, education FROM Users WHERE username=?", (username,))
    user = c.fetchone()
    conn.close()
    return User(id=user[0], pfp=user[1], username=user[2], password=user[3], bio=user[4], education=user[5])

def createNewUser(pfp, username, password, bio):
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("INSERT INTO Users (pfp, username, password, bio) VALUES (?, ?, ?, ?)", (pfp, username, password, bio))
    conn.commit()
    conn.close()
    return getUser(username)

def getPostsByAuthor(username):
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("SELECT postId, title, content, author, belongs_to, date FROM Posts WHERE author=?", (username,))
    posts = []
    for post in c.fetchall():
        print(post)
        posts.append(Post(id=post[0], title=post[1], content=post[2], author=post[3], belongs_to=post[4], date=post[5]))
    conn.close()
    return posts

def editUser(userId, pfp, username, password, bio, education):
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("UPDATE Users SET pfp=?, username=?, password=?, bio=?, education=? WHERE userId=?", (pfp, username, password, bio, education, userId))
    conn.commit()
    conn.close()
    return getUserById(userId)

if __name__ == "__main__":
    for user in getAllUsers():
        print(user)
    pfp = input("pfp: ")
    username = input("username: ")
    password = input("password: ")
    bio = input("bio: ")
    createNewUser(pfp, username, password)
