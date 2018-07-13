from Observer import Observer
import time

class ManagingRoomsAndNicks:

    @staticmethod
    def __nickBusy(nick, listOfRooms):
        for room in listOfRooms:
            for obs in room.listOfObservers:
                if nick == obs.nick:
                    return True
        return False

    @staticmethod
    def createNewNick(connection, listOfRooms):
        while True:
            nick = connection.clientSocket.recv(connection.BUF_SIZE).decode()
            if ManagingRoomsAndNicks.__nickBusy(nick, listOfRooms):
                response = "NOT_REGISTERED"
                connection.clientSocket.send(response.encode())
            else:
                response = "YOU_ARE_REGISTERED"
                connection.clientSocket.send(response.encode())
                time.sleep(1)
                return nick

    @staticmethod
    def addToRoom(nick, roomName, listOfRooms, connection):
        for room in listOfRooms:
            if room.nameOfRoom == roomName:
                Observer(room, nick, connection.clientSocket)
                room.notifyThatJoined(nick)

    @staticmethod
    def getNickFromUser(frame, connection, listOfRooms):
        if frame.split("::")[3] == "###":
            nick = ManagingRoomsAndNicks.createNewNick(connection, listOfRooms)
        else:
            nick = frame.split("::")[3]
        return nick

