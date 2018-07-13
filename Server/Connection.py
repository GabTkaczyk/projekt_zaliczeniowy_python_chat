import socket

class Connection:
    BUF_SIZE = 32#100
    ADRESS = socket.gethostbyname(socket.gethostname())
    PORT = 8000

    def __init__(self, clientSocket):
        self.clientSocket = clientSocket
        self.currentRoomName = "###"
        self.nick = "abc###"
