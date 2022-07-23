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

