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
                    password        TEXT        NOT NULL
                )"""
    create_table(contents)

# groceries
def create_game_table():
    contents =  """
                CREATE TABLE IF NOT EXISTS game (
                    question        TEXT        NOT NULL    PRIMARY KEY,
                    answer          TEXT        NOT NULL,
                    points          INTEGER     NOT NULL,
                    category        TEXT        NOT NULL,
                    hint            TEXT        NOT NULL
                )"""
    create_table(contents)

# favs
def create_userdata_table():
    contents = """
               CREATE TABLE IF NOT EXISTS favs (
                   userpoints       INTEGER      NOT NULL,
                   currentgame	    TEXT	     NOT NULL,
                   highscore        INTEGER      NOT NULL
               )"""
    create_table(contents)


#=============================GENERAL=HELPERS=============================#

def create_table(contents):
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()
    c.execute(contents)
    db.commit()
    db.close()
