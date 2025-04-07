import socket
from _thread import *
from game import Game
import pickle
import os


#ngrok tcp 5555

os.system("cls")

server = "192.168.211.40"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    
                    if data == "draw":
                        game.draw()
                    elif data in ["red", "green", "yellow", "blue"]:
                        game.wild_update(data)
                    elif data != "get":
                        game.play(data)

                    if game.ready:
                        game.update_time()

                    reply = game
                    conn.sendall(pickle.dumps(reply))
            else:
                break
        except:
            break

    print(f"Lost Connection With Game {gameId}")
    
    try:
        del games[gameId]
        print(f"Closing Game: {gameId}")
    except:
        pass
    idCount -= 1
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount-1) // 4
    if idCount % 4 == 1:
        games[gameId] = Game()
        print(f"Creating game {gameId}")
    else:
        p = (idCount - 1) % 4
        if p == 3:
            games[gameId].ready = True
    
    p += 1

    start_new_thread(threaded_client, (conn, p, gameId))

