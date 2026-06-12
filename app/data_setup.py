import sqlite3                      # enable control of an sqlite database
import hashlib                      # for consistent hashes
import secrets                      # to generate ids

DB_FILE="data.db"

#=============================MAKE=TABLES=============================#

# users
def create_users_table():
    contents =  """
                CREATE TABLE IF NOT EXISTS users (
                    username        TEXT        NOT NULL    PRIMARY KEY,
                    password        TEXT        NOT NULL,
                    bio             TEXT        NOT NULL,
                    total_points    INTEGER     NOT NULL,
                    wins            INTEGER     NOT NULL,
                    runnerups       INTEGER     NOT NULL,
                    losses          INTEGER     NOT NULL
                )"""
    create_table(contents)

# groceries
def create_board_table():
    contents =  """
                CREATE TABLE IF NOT EXISTS board (
                    title           TEXT        NOT NULL,
                    row             INTEGER     NOT NULL,
                    column          INTEGER     NOT NULL,
                    quest_cat       TEXT        NOT NULL,
                    answer          TEXT,
                    wrong1          TEXT,
                    wrong2          TEXT,
                    wrong3          TEXT,
                    point_value     INTEGER,
                    chosen          INTEGER     NOT NULL
                )"""
    create_table(contents)

# favs
def create_game_table():
    contents = """
               CREATE TABLE IF NOT EXISTS game (
                   game_id          INTEGER      NOT NULL   PRIMARY KEY,
                   board            TEXT         NOT NULL,
                   player1	        TEXT	     NOT NULL,
                   player2          TEXT,
                   player3          TEXT,
                   points1          INTEGER      NOT NULL,
                   points2          INTEGER,
                   points3          INTEGER
               )"""
    create_table(contents)

def create_lobbies_table():
    contents = """
               CREATE TABLE IF NOT EXISTS lobbies (
                   lobby_id         TEXT         NOT NULL   PRIMARY KEY,
                   player1          TEXT,
                   player2	        TEXT,
                   player3          TEXT
               )"""
    create_table(contents)

#=============================GENERAL=HELPERS=============================#

def create_table(contents):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(contents)
    db.commit()
    db.close()
