**Le Fin**  
**Project: P05 — THIS IS JEOPARDY**
**Team: Pomegranates**  
**Roster: Jason Chan (PM), Artemis Lee, Ethan Cheung**  
--------------------------------------------------------

# **PROJECT DESCRIPTION:**

Users will be able to play a game of Jeopardy with friends. They may use pre-generated boards created from our database of questions, or they may make their own customizable gameboard. Upon playing a game, the user will reveal clues and take keyboard inputs from the players. A player will gain/lose points depending on if they give the correct answer. Obviously, whoever has the most points wins. Have fun\!

--------------------------------------------------------

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

--------------------------------------------------------

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

--------------------------------------------------------

# **COMPONENT MAP:**
``` mermaid
---
config:
  theme: neutral
  layout: dagre
---
flowchart TB
   L["__init__.py"] -- renders --> M["HTML templates"]
   M -- uses/links to --> Q["JS Files"]
   L -- uses --> N["data_setup.py"]
   L --> O["data.py"]
   M -- uses --> O
   O -- handles --> P["data.db"]
   O --> R["SQLite database"]
```


--------------------------------------------------------

# **FRONT END DIAGRAM:**
``` mermaid
---
config:
  theme: neutral
  layout: dagre
---
flowchart TB
    n1["Register"] --> n2["Login"]
    n2 --> n1 & n5["Home"]
    n5 --> n4["Profile"] & n6["Create"]
    n4 --> n3["Edit Profile"] & n5
    n3 --> n4
    n6 --> n7["Edit"] & n5
    n7 --> n6
    n9["Game"] --> n8["Buzzer"]
    n8 --> n9
    n5 --> n9

    n1@{ shape: rect}
    n2@{ shape: rect}
    n5@{ shape: rect}
    n4@{ shape: rect}
    n6@{ shape: rect}
    n3@{ shape: rect}
    n7@{ shape: rect}
    n9@{ shape: rect}
    n8@{ shape: rect}
```
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
