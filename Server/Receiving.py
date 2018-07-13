class Receiving:
    def __init__(self, listOfRooms, connection):
        self.listOfRooms = listOfRooms
        self.conn = connection

    def receiveAllFrame(self):
        try:
            frame = self.conn.clientSocket.recv(self.conn.BUF_SIZE).decode()
            if frame == "SEND_ME_LIST_OF_ROOMS" or frame == "EXIT":
                return True, frame
            if frame.split("::")[0] == "MSG":
                arrayFrame = frame.split("::")
                sizeFromThirdArg = arrayFrame[1]
                message = frame[(5 +len(sizeFromThirdArg) + 2):]
                while len(message) < int(sizeFromThirdArg):
                    message += self.conn.clientSocket.recv(self.conn.BUF_SIZE).decode()
                message = "MSG::" + message
                return True, message
        except ConnectionError as err:
            print("Error while receiving frame. {}".format(err))
            return False, "###"
        return True, frame