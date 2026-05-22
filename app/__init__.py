from flask import Flask, render_template, request, session, redirect, url_for, jsonify

import sqlite3
import datetime   #enable control of an sqlite database

# our helper db files
import data_setup
import data
from werkzeug.security import generate_password_hash, check_password_hash

DB_FILE="data.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

# create tables
data_setup.create_users_table()
data_setup.create_board_table()
data_setup.create_game_table()

app = Flask(__name__)
app.secret_key = "secret"

@app.route("/logout")
def logout():
    session.pop('username', None) # remove username from session
    return redirect(url_for('login'))

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("data.db")
        c = conn.cursor()

        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = c.fetchone()
        conn.close()

        if result and check_password_hash(result[0], password):
            session["user"] = username
            return redirect(url_for("home"))
        else:
            return render_template("login.html", invalid="Invalid username or password")

    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])

        conn = sqlite3.connect("data.db")
        c = conn.cursor()

        try:
            c.execute("INSERT INTO users (username, password, bio, total_points, wins, runnerups, losses) VALUES (?, ?, ?, ?, ?, ?, ?)",
                      (username, password, "No bio", 0, 0, 0, 0))
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", invalid="Username already exists")

        conn.close()

        session["user"] = username
        return redirect(url_for("home"))

    return render_template("register.html")


@app.route("/home", methods=["GET", "POST"])
def home():
    return render_template("home.html")

@app.route("/create_new", methods=["GET", "POST"])
def create_new():
    if request.method == "POST":
        title = request.form["title"]

        data.create_new_board(title)

        return redirect(url_for("create", board = title))

    return render_template("create_new.html")

@app.route("/create/<string:board>", methods=["GET", "POST"])
def create(board):
    board_text = data.get_board_text(board)
    return render_template("create.html", board_text = board_text, board = board)

@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    return render_template("edit.html")

@app.route("/edit/<string:board>/<int:row>/<int:column>", methods=["GET", "POST"])
def edit(board, row, column):
    if request.method == "POST":
        if row == 0:
            category = request.form["category"]

            data.edit_category(board, row, column, category)

            return redirect(url_for("create", board = board))

        else:
            question = request.form["question"]
            points = request.form["points"]
            correct = request.form["correct"]
            wrong1 = request.form["wrong1"]
            wrong2 = request.form["wrong2"] # IF NOTHING INPUTTED, IT IS AN EMPTY STRING
            wrong3 = request.form["wrong3"]

            data.edit_question(board, row, column, question, points, correct, wrong1, wrong2, wrong3)

            return redirect(url_for("create", board = board))

    return render_template("edit.html", board = board, row = row, column = column)

@app.route("/new_game", methods=["GET", "POST"])
def new_game():
    if request.method == "POST":
        username1 = request.form["username1"]
        username2 = request.form["username2"]
        username3 = request.form["username3"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        password3 = request.form["password3"]

        print(username1)
        print(username2)
        print(username3)
        print(password1)
        print(password2)
        print(password3)

        if not username1 == "":
            if not data.auth(username1, password1):
                return render_template("new_game.html", invalid="Username or password is incorrect for Player 1")
        if not username2 == "":
            if not data.auth(username2, password2):
                return render_template("new_game.html", invalid="Username or password is incorrect for Player 2")
        if not username3 == "":
            if not data.auth(username3, password3):
                return render_template("new_game.html", invalid="Username or password is incorrect for Player 3")

        return redirect(url_for("game"))

    return render_template("new_game.html")

@app.route("/game", methods=["GET", "POST"])
def game():
    return render_template("game.html")
    
@app.route("/profile", methods=["GET", "POST"])
def profile():
    username = session["user"]
    desc = "Hello, It's Me Crewmate I am the good guy on the spaceship. And I complete, all the tasks"
    gc = 0
    wc = 0
    lc = 0
        
    return render_template("profile.html", username=username, description = desc, game_count=gc, win_count=wc, lose_count=lc)


if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
