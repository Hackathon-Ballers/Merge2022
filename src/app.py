from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

users = {
    "admin": "admin",
    "Jeff": "Jeff",
    "Joey": "Joey"
}


@app.route('/')
def index():
    if not session.get('username'): return redirect("/login")
    return render_template('index.html', uname=session['username'])



app.secret_key = 'super secret key'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)