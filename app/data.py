import sqlite3                      # enable control of an sqlite database
import hashlib                      # for consistent hashes
import secrets                      # to generate ids
from werkzeug.security import generate_password_hash, check_password_hash

DB_FILE="data.db"

#=============================USERS=============================#


# returns a list of usernames
def get_all_users():

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    data = c.execute('SELECT username FROM users').fetchall()

    db.commit()
    db.close()

    return clean_list(data)


# returns whether or not a user exists
def user_exists(username):
    all_users = get_all_users()
    for user in all_users:
        if (user == username):
            return True
    return False


# checks if provided password in login attempt matches user password
def auth(username, password):

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    print("11")

    if not user_exists(username):
        db.commit()
        db.close()
        print("22")

        return False
    '''
    # use ? for unsafe/user provided variables
    passpointer = c.execute('SELECT password FROM users WHERE username = ?', (username,))
    real_pass = passpointer.fetchone()[0]

    db.commit()
    db.close()

    password = password.encode('utf-8')

    # hash password here
    if real_pass != str(hashlib.sha256(password).hexdigest()):
        print("33")
        return False
    '''
    hashed_password = c.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchone()
    if not check_password_hash(hashed_password[0], password):
        print("55")
        return False

    print("44")
    return True


# adds a new user's data to user table
def add_user(username, password):

    if user_exists(username):
        return "Username already exists"

    if password == "":
        return "Password cannot be empty"

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # hash password here
    password = password.encode('utf-8')
    password = str(hashlib.sha256(password).hexdigest())

    # use ? for unsafe/user provided variables
    c.execute('INSERT INTO users VALUES (?, ?)', (username, password,))

    db.commit()
    db.close()

    return "success"

#=============================GAME==============================#

# upon start of a new game, resets board and creates a game id with that board tied to it
def setup_new_game(board, game_id, user1, user2, user3):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute(
        'UPDATE board SET chosen = 0 WHERE title = ?',
        (board,)
    )

    c.execute(
        'INSERT INTO game VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (game_id, board, user1, user2, user3, 0, 0, 0,)
    )

    db.commit()
    db.close()

# when a clue is chosen, the chosen column in the db is set to 1 to prevent that clue to be chosen again
def chosen_clue(board, row, column):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute(
        'UPDATE board SET chosen = 1 WHERE (title, row, column) = (?, ?, ?)',
        (board, row, column,)
    )

    db.commit()
    db.close()

# gets the correct answer of a clue
def get_correct_answer(board, row, column):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    answer = c.execute(
        'SELECT answer FROM board WHERE (title, row, column) = (?, ?, ?)',
        (board, row, column,)
    ).fetchone()

    db.commit()
    db.close()

    answer = answer[0]

    return answer

# returns a list of all possible answers of a clue, including nulls
def get_all_answers(board, row, column):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    choices = []

    choices.append(c.execute(
        'SELECT answer FROM board WHERE (title, row, column) = (?, ?, ?)',
        (board, row, column,)
    ).fetchone())
    choices.append(c.execute(
        'SELECT wrong1 FROM board WHERE (title, row, column) = (?, ?, ?)',
        (board, row, column,)
    ).fetchone())
    choices.append(c.execute(
        'SELECT wrong2 FROM board WHERE (title, row, column) = (?, ?, ?)',
        (board, row, column,)
    ).fetchone())
    choices.append(c.execute(
        'SELECT wrong3 FROM board WHERE (title, row, column) = (?, ?, ?)',
        (board, row, column,)
    ).fetchone())

    db.commit()
    db.close()

    choices = clean_list(choices)

    return choices

# given the game_id, returns an array of the data in the game table except for the game_id, in that order
# for example, board is the first item in the array, player1 is the second item, etc.
def get_game_data(game_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    game_data = []

    game_data.append(c.execute(
        'SELECT board FROM game WHERE game_id = ?', (game_id,)
    ).fetchone())
    game_data.append(c.execute(
        'SELECT player1 FROM game WHERE game_id = ?', (game_id,)
    ).fetchone())
    game_data.append(c.execute(
        'SELECT player2 FROM game WHERE game_id = ?', (game_id,)
    ).fetchone())
    game_data.append(c.execute(
        'SELECT player3 FROM game WHERE game_id = ?', (game_id,)
    ).fetchone())
    game_data.append(c.execute(
        'SELECT points1 FROM game WHERE game_id = ?', (game_id,)
    ).fetchone())
    game_data.append(c.execute(
        'SELECT points2 FROM game WHERE game_id = ?', (game_id,)
    ).fetchone())
    game_data.append(c.execute(
        'SELECT points3 FROM game WHERE game_id = ?', (game_id,)
    ).fetchone())

    db.commit()
    db.close()

    game_data = clean_list(game_data)

    return game_data


#=============================BOARD==============================#

# creats a new board with placeholder text and null values for each board
def create_new_board(title):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    for row in range(6):
        for column in range(6):
            c.execute(
                'INSERT INTO board VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (title, row, column, "Placeholder Text", None, None, None, None, None, 0,)
            )

    db.commit()
    db.close()

# creates a new board with the given data as the parameter. this board is deleted after the game using it ends
def create_board_from_api(data, title):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #create_new_board("pp")
    #print(title)
    create_new_board(title)

    for column in range(6):
        edit_question(
            title, 0, column, data[column][0]["category"], 0, None, None, None, None
        )

    for column in range(6): # column first bc data is sorted by category
        for row in range(5):
            if (data[column][row]["type"] == "boolean"):
                edit_question(
                    title, row + 1, column, data[column][row]["question"], (row + 1) * 200, data[column][row]["correct_answer"], data[column][row]["incorrect_answers"][0], None, None
                )
            else:
                edit_question(
                    title, row + 1, column, data[column][row]["question"], (row + 1) * 200, data[column][row]["correct_answer"], data[column][row]["incorrect_answers"][0], data[column][row]["incorrect_answers"][1], data[column][row]["incorrect_answers"][2]
                )
            #print(data[column][row])
            #print("\n\n\n\n\nawawsdasdugyewgfuygfhdiuguitgu\n\n\n\n\n")

    db.commit()
    db.close()

# returns a 2d array of all of the text in a board
def get_board_text(title):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    board_text = []

    for row in range(6):
        board_text.append(c.execute(
                             'SELECT quest_cat FROM board WHERE (title, row) = (?, ?)',
                             (title, row,)
                         ).fetchall()
                     )

    board_text = clean_list_2d(board_text)
    return board_text

def get_board_point_values(title):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    board_point_values = []

    for row in range(6):
        board_point_values.append(c.execute(
                             'SELECT point_value FROM board WHERE (title, row) = (?, ?)',
                             (title, row,)
                         ).fetchall()
                     )

    board_point_values = clean_list_2d(board_point_values)
    return board_point_values

# updates the board db with user inputted clues, with null values added for some vars if not inputted
def edit_question(board, row, column, question, points, correct, wrong1, wrong2, wrong3):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if wrong2 == "":
        wrong2 = None
    if wrong3 == "":
        wrong3 = None

    c.execute(
        'UPDATE board SET (quest_cat, point_value, answer, wrong1, wrong2, wrong3) = (?, ?, ?, ?, ?, ?) WHERE (title, row, column) = (?, ?, ?)',
        (question, int(points), correct, wrong1, wrong2, wrong3, board, row, column,)
    )

    db.commit()
    db.close()
    return

# updates the board db with user inputted categories
def edit_category(board, row, column, category):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute(
        'UPDATE board SET (quest_cat) = (?) WHERE (title, row, column) = (?, ?, ?)',
        (category, board, row, column,)
    )

    db.commit()
    db.close()
    return

#=============================LOBBIES=============================#

# returns an array of a lobby given the lobby_id. returns "No lobby found" if there isn't a lobby by that lobby_id
def get_lobby_array(lobby_id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    lobby_array = c.execute("SELECT * FROM lobbies WHERE lobby_id = ?" , (lobby_id,)).fetchone()

    print("456456456456")
    print(lobby_array)

    if lobby_array == None:
        return "No lobby found"

    # clean_list doesn't work when there's a None in the array, so i'm doing this instead
    returning_the_lobby_array = []

    for item in lobby_array:
        returning_the_lobby_array.append(item)

    return returning_the_lobby_array

# removes the user from the room that they are connected in and returns True. if the user is not in any room in the first place, returns False.
def remove_user_from_lobby(username):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    is_user_in_room = c.execute(
        "SELECT * FROM lobbies WHERE player1 = ? OR player2 = ? OR player3 = ?",
        (username, username, username,)
    ).fetchone()

    if is_user_in_room == None:
        return False

    else:
        for i in range(1,4):
            if is_user_in_room[i] == username:
                c.execute("UPDATE lobbies SET " + "player" + str(i) + " = ? WHERE lobby_id = ?",
                    (None, is_user_in_room[0],)
                )

    db.commit()
    db.close()
    return True

#=============================HELPERS=============================#


# turn a list of tuples (returned by .fetchall()) into a 1d list
def clean_list(raw_output):
    clean_output = []
    for lst in raw_output:
        for item in lst:
            if str(item) != 'None' and item != "":
                clean_output += [item]
    return clean_output


# turn a list of tuples (returned by .fetchall()) into a 2d list
def clean_list_2d(raw_output):
    clean_output = []

    for lst in raw_output:
        clean_output += [clean_list(lst)]

    return clean_output


# convert a list of data into a dictionary
def list_to_dict(keys, values):
    if len(keys) != len(values):
        print("list_to_dict: length keys != length values")
        return {}
    dict = {}
    for i in range(len(keys)):
        dict[keys[i]] = values[i]
    return dict


# convert a 2d list of data to a list of dictionaries
def list_2d_to_dict_list(keys, values):
    lst = []
    for val_sublst in values:
        lst += [list_to_dict(keys, val_sublst)]
    return lst


# get_field: return one value from the table based on another value in that row (an "id")
def get_field(table, ID_fieldname, ID, field):
    lst = get_field_list(table, ID_fieldname, ID, field)
    if (len(lst) == 0):
        return 'None'
    return lst[0]


# get_field_list: return all values in a specific field (column) in a row with a matching "id" item
def get_field_list(table, col_name, ID, field):

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # use ? for unsafe/user provided variables
    data = c.execute(f'SELECT {field} FROM {table} WHERE {col_name} = ?', (ID,)).fetchall()

    db.commit()
    db.close()

    return clean_list(data)


# get_row_list: return all rows that have an "id" field matching the given argument
def get_row_list(table, col_name, ID):

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # use ? for unsafe/user provided variables
    data = c.execute(f'SELECT * FROM {table} WHERE {col_name} = ?', (ID,)).fetchall()

    db.commit()
    db.close()

    return clean_list_2d(data)


# return a list of all items in a column of the table
def get_col_list(table, col_name):

    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # no unsafe/user-provided vars here, safe to use f-strings
    data = c.execute(f'SELECT {col_name} FROM {table}').fetchall()

    db.commit()
    db.close()

    return clean_list(data)


# delete_row: delete a row of data from the table
def delete_row(table, ID_fieldname, id):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    # use ? for unsafe/user provided variables
    c.execute(f'DELETE FROM {table} WHERE {ID_fieldname} = ?', (id,))

    db.commit()
    db.close()


# generate an id
def gen_id():
    # use secrets module to generate a random 32-byte string
    return secrets.token_hex(32)
