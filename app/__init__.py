from flask import Flask, render_template, request, session, redirect, url_for, jsonify

import sqlite3, datetime   #enable control of an sqlite database

# our helper db files
import data_setup, data

DB_FILE="data.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

# create tables
data_setup.create_users_table()
data_setup.create_game_table()
data_setup.create_userdata_table()

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/", methods=['GET', 'POST'])
def login():

    # stored active session, take user to response page
    if 'username' in session:
        return redirect(url_for("home"))

    if 'username' in request.form:
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        # check if password is correct, if not then reload page
        if not data.auth(username, password):
            return render_template("login.html", error="Username or password is incorrect")

        # if password is correct redirect home
        session["username"] = username
        return redirect(url_for("home"))

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop('username', None) # remove username from session
    return redirect(url_for('login'))

@app.route('/register', methods=["GET", "POST"])
def register():

    if request.method == 'POST':
        username = request.form.get('username').strip().lower()
        password = request.form.get('password').strip()

        # reload page if no username or password was entered
        if not username or not password:
            return render_template("register.html", error="No username or password inputted")

        # puts user into database unless if there's an error
        execute_register = data.add_user(username, password)
        if execute_register == "success":
            session['username'] = username
            return redirect(url_for("home"))
        else:
            return render_template("register.html", error = execute_register)
    return render_template("register.html")

@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/create", methods=["GET", "POST"])
def create():
    return render_template("create.html")

@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    return render_template("edit.html")

@app.route("/edit", methods=["GET", "POST"])
def edit():
    return render_template("edit.html")

@app.route("/game", methods=["GET", "POST"])
def game():
    return render_template("game.html")

@app.route("/profile", methods=["GET", "POST"])
def profile():
    return render_template("profile.html")

if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
