import sqlite3                      # enable control of an sqlite database
import hashlib                      # for consistent hashes
import secrets                      # to generate ids

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

    if not user_exists(username):
        db.commit()
        db.close()

        return False

    # use ? for unsafe/user provided variables
    passpointer = c.execute('SELECT password FROM users WHERE username = ?', (username,))
    real_pass = passpointer.fetchone()[0]

    db.commit()
    db.close()

    password = password.encode('utf-8')

    # hash password here
    if real_pass != str(hashlib.sha256(password).hexdigest()):
        return False

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

def edit_slot_contents(board, row, column, question, points, correct, wrong1, wrong2, wrong3):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    c.execute(
        'UPDATE board SET (quest_cat, point_value, answer, wrong1, wrong2, wrong3) = (?, ?, ?, ?, ?, ?) WHERE (title, row, column) = (?, ?, ?)',
        (question, int(points), correct, wrong1, wrong2, wrong3, board, row, column,)
    )

    db.commit()
    db.close()
    return

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
