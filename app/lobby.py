from flask_socketio import SocketIO, join_room, leave_room, emit


socket = SocketIO(async_mode='gevent')


def define_lobby(lobbyid): #makes array with lobbyid, player1 name, player2 name, player3 name in that order

    lobby_array = [lobbyid, None, None, None]
    lobby_array_string = ", ".join(lobby_array)
    c.execute("INSERT INTO lobbies (" + lobbyid "," + user1 + "," + user2 + "," + user3 + ") VALUES (?, ?, ?, ?, ?)") #creates a row in SQLite with lobby data

    return lobby_array


def join_lobby(userid, lobby_array):
    lobbyid = lobby_array[0]

    if userid not in lobby_array:
        if x != lobbyid and x == None:
            x = userid #replaces last empty slot in the lobby array with the user's id and allows them to join


#this part is just me screwing around with socket commands


@socketio.on('join')
def join_lobby_socket():
    #check to see if lobbyid already exists, if not, add to sqlite
    lobby_id = data['lobby_id']
    username = session['username']

    join_room(lobby_id)
    emit('message', username + "has entered the room.", to=lobby_id)


@app.route("/lobby", methods=['GET', 'POST'])
def lobby():
    if request.method == "POST":
        emit('join', { lobby_id : request.form["lobby_id"] }) #this should/could maybe work?????? idk if app functions can call emits but if they can this is literally all i need to do hopefully
    




@socketio.on('buzzer_pressed')
def buzzer_pressed_socket(data):
    
    if data['answer'] == session["correct_answer"]:
        
    
