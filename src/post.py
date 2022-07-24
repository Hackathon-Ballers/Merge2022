from dataclasses import dataclass
from datetime import datetime
import sqlite3
import user

@dataclass
class Post:
    title: str
    content: str
    author: str
    date: str
    id: int = 0
    totalViews:int = 0
    author_pfp: str = "default.png"
    authorId: int = -1
    belongs_to:any = None
    totalComments:int = 0

def createNewPost(title, content, author, belongs_to):
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("INSERT INTO Posts (title, content, author, date, belongs_to, views) VALUES (?, ?, ?, ?, ?, ?)", (title, content, author, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), belongs_to, 0))
    conn.commit()
    conn.close()
    return getPostById(c.lastrowid)

def getAllPosts():
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("SELECT postId, title, content, author, date, belongs_to FROM Posts")
    posts = []
    for post in c.fetchall():
        posts.append(Post(id=post[0], title=post[1], content=post[2], author=post[3], date=post[4], belongs_to=post[5]))
    conn.close()
    return posts

def getPostById(id):
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("SELECT postId, title, content, author, date, belongs_to , views FROM Posts WHERE postId=?", (id,))
    post = c.fetchone()
    if not post: return None
    conn.close()
    return Post(id=post[0], title=post[1], content=post[2], author=post[3], date=post[4], belongs_to=post[5], totalViews=post[6])

def getPostWhereBelongsTo(belongs_to):
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("SELECT postId, title, content, author, date, belongs_to FROM Posts WHERE belongs_to=?", (belongs_to,))
    posts = []
    for post in c.fetchall():
        posts.append(Post(id=post[0], title=post[1], content=post[2], author=post[3], date=post[4], belongs_to=post[5]))
    conn.close()
    return posts

def updateViewCount(post_id):
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    c.execute("UPDATE Posts SET views=views + 1 WHERE postId=?", (post_id,))
    print("ok updated")
    conn.commit()
    conn.close()

def getTotalComments(postId):
    return len(getPostWhereBelongsTo(postId))

def renamePostsByAuthor(prev_author, new_author):
    posts = user.getPostsByAuthor(prev_author)
    conn = sqlite3.connect('stackunderflow.db')
    c = conn.cursor()
    for post in posts:
        c.execute("UPDATE Posts SET author=? WHERE postId=?", (new_author, post.id,))
    conn.commit()
    conn.close()


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