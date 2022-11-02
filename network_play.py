# connect to external player using given ip and port
# play chess game with external player
# assume same program is running on designated ip and port
import socket
import chess
import threading

# global variables
# socket for communication
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# board for game
board = chess.Board()
# default port number
default_port = 7777

# main function
def main(ip, port):
    # ip: ip address of external player
    # port: port of external player
    # check if given ip and port are valid and connect
    if check_ip(ip) and check_port(port):
        connect(ip, port)

# check if given ip is valid
def check_ip(ip):
    # ip: ip address of external player
    # check if ip is valid
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        print("Invalid ip address")
        return False

# check if given port is valid
def check_port(port):
    # port: port of external player
    # check if port is valid
    try:
        port = int(port)
        if port > 0 and port < 65536:
            return True
        else:
            print("Invalid port number")
            return False
    except ValueError:
        print("Invalid port number")
        return False

# connect to external player
def connect(ip, port):
    # ip: ip address of external player
    # port: port of external player
    # connect to external player
    global s
    s.connect((ip, port))
    # start thread to receive messages from external player
    t = threading.Thread(target=receive)
    t.start()
    # start thread to send messages to external player
    t = threading.Thread(target=send)
    t.start()

# receive messages from external player
def receive():
    global s
    global board
    while True:
        # receive message
        msg = s.recv(1024)
        # decode message
        msg = msg.decode()
        # if message is valid
        if msg != "":
            # if message is a move
            if msg[0] == "m":
                # get move from message
                move = chess.Move.from_uci(msg[1:])
                # make move on board
                board.push(move)
                # print board
                print(board)
            # if message is a reset
            elif msg == "r":
                # reset board
                board.reset()
                # print board
                print(board)
            # if message is a quit
            elif msg == "q":
                # close socket
                s.close()
                # exit program
                exit()

# send messages to external player
def send():
    global s
    global board
    while True:
        # get move from user
        move = input()
        # if move is valid
        if move != "":
            # if move is a reset
            if move == "reset":
                # send reset message
                s.send("r".encode())
            # if move is a quit
            elif move == "quit":
                # send quit message
                s.send("q".encode())
                # close socket
                s.close()
                # exit program
                exit()
            # if move is a move
            else:
                # check if move is valid
                if chess.Move.from_uci(move) in board.legal_moves:
                    # send move message
                    s.send(("m" + move).encode())
                    # make move on board
                    board.push(chess.Move.from_uci(move))
                    # print board
                    print(board)
                else:
                    print("Invalid move")

if __name__ == "__main__":
    # get ip from user
    ip = input("Enter ip: ")
    # get port from user
    port = int(input("Enter port: "))
    # call main function
    main(ip, port)