from flask_socketio import SocketIO, join_room, emit


socket = SocketIO(async_mode='gevent')


def define_lobby(lobbyid): #makes array with lobbyid, player1 name, player2 name, player3 name, player4 name in that order

    lobby_array = [lobbyid, "NA", "NA", "NA", "NA"]
    lobby_array_string = ", ".join(lobby_array)
    c.execute("INSERT INTO lobbies (" + lobbyid "," + user1 + "," + user2 + "," + user3 + "," + user4 + ") VALUES (?, ?, ?, ?, ?)") #creates a row in SQLite with lobby data
    
    return lobby_array


def join_lobby(userid, lobby_array):
    lobbyid = lobby_array[0]
    
    if userid not in lobby_array:
        if x != lobbyid and x == "NA":
            x = userid #replaces last empty slot in the lobby array with the user's id and allows them to join
    

#this part is just me screwing around with socket commands


@socketio.on('join')
def create_lobby_socket():
    lobby_id = on_join
    username = session[username]
    
    join_room(lobby_id)
    emit('status', f"{username} has entered the room.", to=room)
    