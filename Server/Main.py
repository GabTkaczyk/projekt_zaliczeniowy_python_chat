from Room import Room
from Connection import Connection
from ClientThread import ClientThread
import socket

if __name__ == "__main__":
    listOfRooms = set()
    subjectPokoj1 = Room("pierwszy")
    subjectPokoj2 = Room("drugi")
    listOfRooms.add(subjectPokoj1)
    listOfRooms.add(subjectPokoj2)

    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(("0.0.0.0", Connection.PORT))
    serverSocket.listen(10)
    print("Server is listening on port {}".format(Connection.PORT))

    while True:
        try:
            clientSocket, clientAddress = serverSocket.accept()
            print("new client connected")
            ClientThread(Connection(clientSocket), listOfRooms).start()

        except socket.error as err:
            print(err)
        except ConnectionResetError as err:
            print("client disconnected")
            print(err)
            clientSocket.close()
