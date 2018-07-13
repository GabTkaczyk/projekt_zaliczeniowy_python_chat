import threading
from Receiving import Receiving
from ManagingRoomsAndNicks import ManagingRoomsAndNicks

class ClientThread(threading.Thread):
    def __init__(self, connection, list_of_rooms):
        threading.Thread.__init__(self)
        self.connection = connection
        self.listOfRooms = list_of_rooms
        self.receiving = Receiving(list_of_rooms, self.connection)

    def run(self):
        try:
            while True:
                success, frame = self.receiving.receiveAllFrame()
                if not frame:
                    break
                if not success:#jak wywali blad w receiveAllFrame
                    raise ConnectionError
                if frame.split("::")[0] == "EXIT":
                    self.__disconnectClient()
                    return
                if frame.split("::")[0] == "SEND_ME_LIST_OF_ROOMS":
                    self.__sendListOfRooms()
                    continue
                if frame.split("::")[0] == "JOIN":
                    nick = ManagingRoomsAndNicks.getNickFromUser(frame, self.connection, self.listOfRooms)
                    roomName = frame.split("::")[2]
                    ManagingRoomsAndNicks.addToRoom(nick, roomName, self.listOfRooms, self.connection)
                    continue
                if frame.split("::")[0] == "MSG":
                    print("{} said: {}".format(frame.split("::")[2], frame.split("::")[3]))
                    self.__directMessageToRooms(frame)
                    continue
                if frame.split("::")[0] == "ESCAPE":
                    for room in self.listOfRooms:
                        if room.nameOfRoom == frame.split("::")[2]:
                            room.detach(frame.split("::")[3])
                            room.notifyThatLeft(frame.split("::")[3])
                            self.connection.clientSocket.send("USER::DISCONNECTED".encode())
                            self.connection.clientSocket.send("YOU_LEFT_ROOM".encode())
                    continue
        except ConnectionError as err:
            print(err)
            self.connection.clientSocket.close()
            return

    def __directMessageToRooms(self, frame):
        arrayFrame = frame.split("::")
        for room in self.listOfRooms:
            if room.nameOfRoom == arrayFrame[1]:
                room.setState(arrayFrame[3], arrayFrame[2])

    def __disconnectClient(self):
        print("disconnecting client")
        self.connection.clientSocket.send("EXIT".encode())
        self.connection.clientSocket.close()

    def __sendListOfRooms(self):
        data = ""
        for room in self.listOfRooms:
            data += room.nameOfRoom
            data += "::"
        size = len(data)
        message = str(size) + "::" + data
        self.connection.clientSocket.send(message.encode())

