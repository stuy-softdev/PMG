**Le Fin**  
**Project: P05 — THIS IS JEOPARDY\!\!\!\!\!\!\!**  
**Team: Pomegranates**  
**Roster: Jason Chan (PM), Artemis Lee, Ethan Cheung**  
*\#\#\# \-------------------------------------------------------- \#\#\#*

# **PROJECT DESCRIPTION:** 

Users will be able to play a game of Jeopardy with friends. They may use pre-generated boards created from our database of questions, or they may make their own customizable gameboard. Upon playing a game, the user will reveal clues and take keyboard inputs from the players. A player will gain/lose points depending on if they give the correct answer. Obviously, whoever has the most points wins. Have fun\!

*\#\#\# \-------------------------------------------------------- \#\#\#*

# **PROGRAM COMPONENTS \+ EXPLANATION:**

## Python files

* *\_\_init\_\_.py*: The main file; serves app  
* *data\_setup.py*: Handles parsing of CSV file and creation of Sqlite3 database tables  
* *data.py*: Handles the data in the Sqlite3 grocery database and the user data (all stored in *data.db*)

## Templates

* *login.html*: The user can login to their account or register if they don’t have one. Redirects to the homepage.  
* *register.html*: The user will be able to register. Redirects to the homepage.  
* *home.html*: The homepage, which will allow users to start a new game with created boards/pre-generated boards, or start creating/editing a custom board.  
* *create.html*: The user can add categories and \# of clues, then for each clue, insert $, question, and answer. Each clue will be saved as a string by default, so users can save unfinished boards and complete them later.  
* *edit.html*: The user can edit their own boards.  
* *game.html*: Takes user input for the game, allowing them to choose what questions to answer (choosing a question will redirect a user to buzzer.html), and shows score lists.  
* *buzzer.html*: Allows users to "buzz in", taking user input times to determine who is allowed to answer first, and giving contestants a prompt that is compared to the actual answer to see if they're correct. Note that all players will be on the same computer, with each player on their own designated key to press.  
* *profile.html*: Allows users to see their username, description, points, current game, and high score  
* *edit\_profile.html*: Edit username or description.

## JavaScript files

* *buzzer.js*: Handles the buzzer inputs during a game.

## CSS files/FEF

* We will be using Tailwind because it is awesome. We will not be using a CSS file.

*\#\#\# \-------------------------------------------------------- \#\#\#*

# **DATABASE ORGANIZATION:**

## We will be using SQLite3 to organize our data; more specifically the user information, their saved boards, and current game stats. We will not be using any databases from external sources.

## 

## Tables:

users

| Variable Type | Variable Name | Variable Attribute(s) |
| :---- | :---- | :---- |
| STRING | username | PK NOT NULL |
| STRING | password | NOT NULL |

game

| Variable Type | Variable Name | Variable Attribute(s) |
| :---- | :---- | :---- |
| STRING | question | PK NOT NULL |
| STRING | answer | NOT NULL |
| INT | points | NOT NULL |
| STRING | category | NOT NULL |
| STRING | hint | NOT NULL |

userdata

| Variable Type | Variable Name | Variable Attribute(s) |
| :---- | :---- | :---- |
| INT | userpoints | FK (username) NOT NULL |
| STRING | currentgame | FK (username) NOT NULL |
| INT | highscore | FK (username) NOT NULL |

# **APIs:**

OpenTDB: Provides a whole bunch of trivia questions as requested. Responsive and easy to filter, but only outputs 50 questions at a time.

*\#\#\# \-------------------------------------------------------- \#\#\#*

# **COMPONENT MAP:**

![][image1]

*\#\#\# \-------------------------------------------------------- \#\#\#*

# **FRONT END DIAGRAM:**

# **TIMELINE:**

WEEK 1: 

* Get basic flask app and HTML template structure working  
* Login/Register  
* data\_setup.py completed or close to complete

WEEK 2: 

* Functions for data.py completed  
* OpenTDB API implementation  
* Users should be able to create/edit game boards

WEEK 3:

* Playing the game should be functional  
  * Displaying clues  
  * Buzzer inputs  
  * Keeping track of stats throughout the game  
* Any stretch goals we may have time for  
  * Being able to play other users’ custom boards  
  * Leaderboards for various stats (wins/losses, total points, correct responses, etc.

**TASK DELEGATION (**REALLY SUBJECT TO CHANGE\! DEVOS ARE NOT FULLY RESTRICTED TO ASSIGNED TASKS\!)**:**

| Task | Devo(s) | Deadline |
| :---- | :---- | :---- |
| Html stuff (page rendering) | DEC | 05-18 @ 11:06 |
| Tailwind stuff (styling) | DEC | 05-30 @ 23:59 |
| Database handling (making and applying data\_setup.py and data.py) | DJC | 05-21 @ 11:06 |
| API stuff (implementing OpenTDB API) | DJC | 05-21 @ 11:06 |
| Python stuff (making flask work) | DAL | 05-15 @ 23:59 |
| Javascript stuff (making buzzer work) | DAL | 05-26 @ 11:06 |
| Devlog | EVERYONE | 06-01 @ 08:00 |

[image1]: <data:image/png;base64,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>