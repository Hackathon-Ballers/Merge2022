from dataclasses import dataclass
from datetime import datetime
import sqlite3

@dataclass
class Post:
    title: str
    content: str
    author: str
    date: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    id: int = 0
    belongs_to:any = None
    totalComments:int = 0

def createNewPost(title, content, author, belongs_to):
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("INSERT INTO Posts (title, content, author, belongs_to) VALUES (?, ?, ?, ?)", (title, content, author, belongs_to))
    conn.commit()
    conn.close()
    #add return?

def getAllPosts():
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("SELECT postId, title, content, author, belongs_to FROM Posts")
    posts = []
    for post in c.fetchall():
        posts.append(Post(id=post[0], title=post[1], content=post[2], author=post[3], belongs_to=post[4]))
    conn.close()
    return posts

def getPostById(id):
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("SELECT postId, title, content, author, belongs_to FROM Posts WHERE postId=?", (id,))
    post = c.fetchone()
    if not post: return None
    conn.close()
    return Post(id=post[0], title=post[1], content=post[2], author=post[3], belongs_to=post[4])

def getPostWhereBelongsTo(belongs_to):
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("SELECT postId, title, content, author, belongs_to FROM Posts WHERE belongs_to=?", (belongs_to,))
    posts = []
    for post in c.fetchall():
        posts.append(Post(id=post[0], title=post[1], content=post[2], author=post[3], belongs_to=post[4]))
    conn.close()
    return posts

def getTotalComments(postId):
    return len(getPostWhereBelongsTo(postId))

if __name__ == "__main__":
    for post in getAllPosts():
        print(post)
    title = input("title: ")
    content = input("content: ")
    author = input("author: ")
    belongs_to = input("belongs_to: ")
    createNewPost(title, content, author, belongs_to)
    for post in getAllPosts():
        print(post)