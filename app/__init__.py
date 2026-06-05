'''
TO DO LIST:

    HIGH PRIORITY
    figure out how socketio works
        make joining lobbies work
        alternate redirect users from the game board (game.html) to the clue (buzzer.html)
            ofc make the button work
            and ofc make answer choices work

    modify game table by adding two more rows
        game id
        board name (useful for tieing to board table)



    LOWER PRIORITY
    implement edit profile

    make custom boards playable in game

    when ending game, check if the board title starts with "randomally_generated_board" and if so, delete it

    leaderboards
'''


from flask import Flask, render_template, request, session, redirect, url_for, jsonify

import sqlite3
import datetime   #enable control of an sqlite database

# our helper db files
import data_setup
import data
from werkzeug.security import generate_password_hash, check_password_hash

# for OpenTDB api
import time
import random
import json
import urllib.request
import urllib.error
#import ssl
#context = ssl._create_unverified_context()
#response = urllib.request.urlopen("https://opentdb.com", context=context)

TRIVIA_POOL = [] # 2d array to create pre-generated boards
file_err = "file not found error"
url_err = "url error"

OPENTDB_COOLDOWN = 5.1 # Cooldown to avoid hitting rate limits
trivia_opentdb_call = 0.0 # stores the last OpenTDB call

DB_FILE="data.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

# ==================== ENSURE TABLES HAVE ALL COLUMNS ====================
conn = sqlite3.connect(DB_FILE)
c = conn.cursor()

# Add missing columns safely
try:
    c.execute("ALTER TABLE users ADD COLUMN bio TEXT NOT NULL DEFAULT 'No bio'")
except sqlite3.OperationalError:
    pass
try:
    c.execute("ALTER TABLE users ADD COLUMN total_points INTEGER NOT NULL DEFAULT 0")
except sqlite3.OperationalError:
    pass
try:
    c.execute("ALTER TABLE users ADD COLUMN wins INTEGER NOT NULL DEFAULT 0")
except sqlite3.OperationalError:
    pass
try:
    c.execute("ALTER TABLE users ADD COLUMN runnerups INTEGER NOT NULL DEFAULT 0")
except sqlite3.OperationalError:
    pass
try:
    c.execute("ALTER TABLE users ADD COLUMN losses INTEGER NOT NULL DEFAULT 0")
except sqlite3.OperationalError:
    pass

conn.commit()
conn.close()

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

@app.route("/create_board", methods=["GET", "POST"])
def create_board():
    if request.method == "POST":
        title = request.form["title"]

        data.create_new_board(title) # creates new board with the given title

        return redirect(url_for("create", board = title))

    return render_template("create_board.html")

@app.route("/create/<string:board>", methods=["GET", "POST"])
def create(board):
    board_text = data.get_board_text(board)
    return render_template("create.html", board_text = board_text, board = board)

############### get_data, opentdb_get, and refill_pool are the functions needed to generate the board from api. this works so don't worry about it. if you really need to know lmk. - jason ###############
############### get_data, opentdb_get, and refill_pool are the functions needed to generate the board from api. this works so don't worry about it. if you really need to know lmk. - jason ###############
############### get_data, opentdb_get, and refill_pool are the functions needed to generate the board from api. this works so don't worry about it. if you really need to know lmk. - jason ###############
############### get_data, opentdb_get, and refill_pool are the functions needed to generate the board from api. this works so don't worry about it. if you really need to know lmk. - jason ###############

# return the data string from the api url, or "url error"
def get_data(url):
    try:
        response = urllib.request.urlopen(url) # This sends the HTTP GET request to Nasa API and urlopen returns a response obj.
        data = json.loads(response.read().decode()) # This decodes the response, which is in bytes, into string and then loads the json string into a python dictionary: data.
        return data
    #except urllib.error.URLError as e:
        #return f"URL Error: {e}"
    except urllib.error.URLError:
        return url_err

def opentdb_get(url):
    global trivia_opentdb_call  # Global so it can update trivia_opentdb_call
    now = time.monotonic() # time_opentdb_call uses time.monotonic(). It's ideal to use this since we only need to track elapsed time
    wait = OPENTDB_COOLDOWN - (now - trivia_opentdb_call)
    if wait > 0:
        time.sleep(wait)
    trivia_opentdb_call = time.monotonic()
    return get_data(url) # fetches json if cooldown expires

def refill_pool(category):
    amount = 5
    #category = random.randint(9, 32) # the category numbers range from 9 to 32 for some reason
    url = f"https://opentdb.com/api.php?amount={amount}&category={category}" # api endpoint
    print("restarting\n\n")

    #for i in range(6):
    for _ in range(3): # a for loop to error handle, we sendata.setup_new_game()d OpenTDB a request up to 3 times if  an error is hit, if not we continue and refill the pool
        data = opentdb_get(url)
        print(data)
        print("asdasdasdasdasdasdasdasdasdasd\n")
        #print(data.get("response_code"))
        if data == url_err: #if there's any error fetching the json we continue
            continue
        if data.get("response_code") == 5:
            time.sleep(OPENTDB_COOLDOWN) #  If this is hit it means a ratelimit occured
            continue
        if data.get("response_code") == 0 and data.get("results"):
            #TRIVIA_POOL[difficulty].extend(data["results"]) # Response code 0 indicates success
            print("YESSSSS!!!!")
            TRIVIA_POOL.append(data["results"])
            #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            #print(TRIVIA_POOL)
            #print(i)
            #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            return True
        time.sleep(OPENTDB_COOLDOWN)
    print("bad bad bad!")
    return False # If true isn't returned that means OpenTDB did not refill the pool of questions, we need to try again.

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

        ################## FOR NOW, ALL GAMES WILL USE A PRE GENERATED BOARD FROM THE API ##################
        ################## FOR NOW, ALL GAMES WILL USE A PRE GENERATED BOARD FROM THE API ##################
        ################## FOR NOW, ALL GAMES WILL USE A PRE GENERATED BOARD FROM THE API ##################

        if True:
            category_list = list(range(9, 33)) # in the trivia api, the category variable is an int between 9 and 32 for some reason
            for i in range(6):
                random_index = random.randrange(len(category_list))
                category = category_list.pop(random_index) # randomally chooses and pops a category
                #print("randomally chosen category: ")
                #print(category)
                refill_pool(category)
                #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
                #print(TRIVIA_POOL)
                #print(i)
                #print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
            #print(category_list)
            title = "randomally_generated_board" + str(int(time.time() * 1000)) # title of board "is randomally_generated_board" + the current time
            data.create_board_from_api(TRIVIA_POOL, title)

        gameid = int(time.time() * 1000) # THIS IS TEMPORARYTHIS IS TEMPORARYTHIS IS TEMPORARYTHIS IS TEMPORARYTHIS IS TEMPORARYTHIS IS TEMPORARYTHIS IS TEMPORARY
        data.setup_new_game(title, gameid, username1, username2, username3)
        return redirect(url_for("game", gameid = gameid))

    return render_template("new_game.html")

@app.route("/<int:gameid>", methods=["GET", "POST"])
def game(gameid):

    #################### GETS BOARD, USERNAMES, AND CURRENT POINTS FROM GAMEID ####################
    #################### REFER TO COMMENT IN data.get_game_data ####################

    current_game_data = data.get_game_data(gameid)
    print("CURRENT GAME DATA")
    print(current_game_data)



    board = current_game_data[0]
    board_text = data.get_board_text(board)
    board_point_values = data.get_board_point_values(board)
    #print("TEXT")
    #print(board_text)
    print("VALS")
    print(board_point_values)
    return render_template(
        "game.html", gameid = gameid, board = board, current_game_data = current_game_data, # game data variables
        board_text = board_text, board_point_values = board_point_values # variables only to display in the html, no purpose in other stuff
    )


@app.route("/<int:gameid>/<int:row>/<int:column>", methods=["GET", "POST"])
def buzzer(gameid, row, column):

    #################### GETS BOARD, USERNAMES, AND CURRENT POINTS FROM GAMEID ####################
    #################### REFER TO COMMENT IN data.get_game_data ####################

    current_game_data = data.get_game_data(gameid)
    print("CURRENT GAME DATA")
    print(current_game_data)


    board = current_game_data[0]
    clue_text = data.get_board_text(board)[row][column]
    clue_point_value = data.get_board_point_values(board)[row][column]
    correct_answer = data.get_correct_answer(board, row, column)
    answer_choices = data.get_all_answers(board, row, column)

    data.chosen_clue(board, row, column)
    print(correct_answer)
    print(answer_choices)

    return render_template(
        "buzzer.html", gameid = gameid, row = row, column = column, board = board, current_game_data = current_game_data, correct_answer = correct_answer, answer_choices = answer_choices, # game data variables
        clue_text = clue_text, clue_point_value = clue_point_value # variables only to display in the html, no purpose in other stuff
    )


if __name__ == "__main__":
    app.debug=True
    app.run(host='0.0.0.0')
