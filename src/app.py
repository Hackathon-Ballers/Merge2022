import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_session import Session
from user import *
from post import *
from textblob import TextBlob

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.secret_key = 'super secret key'
#Image Directory
uploads_dir = '/Users/jwang/Documents/Merge2022/src/assets'

@app.route('/')
def index():
    posts = []
    for post in getAllPosts():
        if post.belongs_to: continue
        post.authorId = getUser(post.author).id
        post.author_pfp = getUser(post.author).pfp
        post.totalComments = getTotalComments(post.id)
        posts.append(post)
    return render_template('index.html', current_user=session.get('user',None), posts=posts[::-1])

@app.route("/new", methods=["GET", "POST"])
def new():
    if not session.get('user'): return redirect("/login")
    if 'confirm' in request.args:
        print("griughreuighreiufgbreiugrb")
        title = session.get('title')
        content = session.get('content')
        author = session['user'].username
        if not title or not content: return redirect("/new")
        if not author: return redirect("/new")
        belongs_to = None
        createNewPost(title, content, author, belongs_to)
        return redirect("/")
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if not title or not content: return redirect("/new")
        tb_title = TextBlob(title)
        tb_content = TextBlob(content)
        if tb_title.sentiment.polarity < 0 or tb_content.sentiment.polarity < 0:
            session['title'] = title
            session['content'] = content
            return render_template('new.html', current_user=session['user'], classes_to_add="")
        createNewPost(title=title, content=content, author=session['user'].username, belongs_to=None)
        return redirect("/")
    return render_template('new.html', current_user=session['user'], classes_to_add="hidden")

@app.route('/post/<post_id>', methods=["GET", "POST"])
def post(post_id):
    if 'confirm' in request.args:
        comment = session['comment']
        if not comment: return redirect("/post/" + post_id)
        author = session['user'].username
        if not author: return redirect("/post/" + post_id)
        createNewPost(title="", content=comment, author=author, belongs_to=post_id)
    if not post_id: return redirect("/")
    post = getPostById(post_id)
    post.authorId = getUser(post.author).id
    post.author_pfp = getUser(post.author).pfp
    if not post: return redirect("/")
    comments = getPostWhereBelongsTo(post_id)
    for comment in comments:
        comment.authorId = getUser(comment.author).id
        comment.author_pfp = getUser(comment.author).pfp

    if request.method == "POST":
        if not session.get('user'): return redirect("/login")
        comment = request.form.get("comment")
        tb_comment = TextBlob(comment)
        if tb_comment.sentiment.polarity < 0:
            session['comment'] = comment
            print(post)
            return render_template('post.html', comments=comments, current_user=session.get('user', None), viewed_post=post, classes_to_add="")
        if not comment: return redirect("/post/" + post_id)
        createNewPost(title="", content=comment, author=session['user'].username, belongs_to=post_id)
        return redirect("/post/" + post_id)
    return render_template('post.html', comments=comments, current_user=session.get('user', None), viewed_post=post, classes_to_add="hidden")

@app.route('/user/<viewed_user_id>')
def user(viewed_user_id):
    if not viewed_user_id: return redirect("/")
    if not session.get('user'): return redirect("/login")
    viewed_user = getUserById(viewed_user_id)
    if not viewed_user: return redirect("/")
    posts = []
    for post in getAllPosts():
        if post.author == viewed_user.username:
            post.totalComments = getTotalComments(post.id)
            posts.append(post)
    viewed_user.total_posts = len(getPostsByAuthor(viewed_user.username))
    return render_template('user.html', current_user=session['user'], viewed_user=viewed_user, posts=posts[::-1])

@app.route('/user/<viewed_user_id>/edit', methods=["GET","POST"])
def edit_user(viewed_user_id):
    viewed_user = getUserById(viewed_user_id)
    if not viewed_user: return redirect("/")
    if not viewed_user_id: return redirect("/")
    if not session.get('user'): return redirect("/login")
    if str(viewed_user_id) != str(session['user'].id): return redirect(f"/user/{viewed_user_id}")
    print(session['user'])

    if request.method == "POST":
        username = request.form.get("username")
        education = request.form.get("education")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        bio = request.form.get("bio")

        print(request.files)

        # check if the post request has the file part
        print("checkpoint 1b")
        file = request.files['pfp']
        # if user does not select file, browser also
        # submit a empty part without filename
        if request.files['pfp'].filename != '':
            if file.filename == '':
                return redirect(f"/user/{viewed_user_id}/edit")
            filename = username + "_" + str(viewed_user_id) + ".png"

            file.save(os.path.join(uploads_dir, filename))
            print(filename)
            if password != confirm_password: return redirect(f"/user/{viewed_user_id}/edit")
            print("passed!")
            session['user'] = editUser(session['user'].id, filename, username, password, bio)
            return redirect(f"/user/{viewed_user_id}")
        session['user'] = editUser(session['user'].id, session['user'].pfp, username, password, bio)
    print(session['user'])
    return render_template('edit_profile.html', current_user=session['user'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in getAllUsers():
            if user.username != username or user.password != password: continue
            session['user'] = user
            return redirect("/")
        else:
            return redirect("/login")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        if password != confirm_password: return redirect("/register")
        session['user'] = createNewUser(None, username, password, None)
        return redirect("/")
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    print(session)
    return redirect("/login")

@app.route('/test')
def test():
    print(session['user'])
    return f"hello {session['user'].username}"

@app.errorhandler(404)
def not_found(error):
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)