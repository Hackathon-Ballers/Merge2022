from cachelib import RedisCache
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_session import Session
from user import User

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

users = [
    User(id=1, pfp="https://i.imgur.com/XqQXQ.jpg", username="admin", password="admin"),
    User(id=2, pfp="https://i.imgur.com/XqQXQ.jpg", username="Jeff", password="Jeff"),
    User(id=3, pfp="https://i.imgur.com/XqQXQ.jpg", username="Joey", password="Joey"),
    User(id=4, pfp="https://i.imgur.com/XqQXQ.jpg", username="Eli", password="Eli"),
    User(id=5, pfp="https://i.imgur.com/XqQXQ.jpg", username="Jari", password="Jari")
]

posts = []

app.secret_key = 'super secret key'

@app.route('/')
def index():
    global posts
    if not session.get('username'): return redirect("/login")
    return render_template('index.html', current_user=session['username'], posts=posts[::-1])

@app.route("/new", methods=["GET", "POST"])
def new():
    if not session.get('username'): return redirect("/login")
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if not title or not content: return redirect("/new")
        posts.append({"title": title, "content": content, "author": session['username']})
        return redirect("/")
    return render_template('new.html', current_user=session['username'])

@app.route('/user/<viewed_username>')
def user(viewed_username):
    if not viewed_username: return redirect("/")
    if not session.get('username'): return redirect("/login")
    return render_template('user.html', current_user=session['username'], viewed_username=viewed_username)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        for user in users:
            if user.username != username or user.password != password: continue
            session['username'] = username
            return redirect("/")
        else:
            return redirect("/login")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    print(session)
    return redirect("/login")

@app.errorhandler(404)
def not_found(error):
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)