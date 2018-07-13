
class Receiving():
    def __init__(self, connection):
        self.conn = connection

    def listen(self):
        self.conn.b_receiving = True
        while self.conn.b_receiving == True:
            try:
                try:
                    data = self.conn.sock.recv(self.conn.BUF_SIZE)
                except ConnectionAbortedError as err:
                    print("Receiving stopped".format(err))
                    break
            except ConnectionResetError as err:
                print("Server is down... {}".format(err))
                self.conn.sock.close()
                break
            if data.decode() == "USER::DISCONNECTED":
                break
            if not data:
                print("no data received, server is not responding")
                self.conn.sock.close()
                break
            print(data.decode())


    # def receiveAllFrame(connection):
    #     message = connection.sock.recv(connection.BUF_SIZE)
    #     message = message.decode()
    #     arrayMaessage = message.split("::")
    #     sizeOfListOfRooms = arrayMaessage[0]
    #     message = arrayMaessage[1]
    #     while len(message) < sizeOfListOfRooms:
    #         encodedMessage = connection.sock.recv(connection.BUF_SIZE)
    #         message += encodedMessage.decode()
    #     return message

    @staticmethod
    def receive(connection):
        message = connection.sock.recv(connection.BUF_SIZE)
        return message.decode()

    @staticmethod
    def getListOfRooms(connection):
        connection.sock.send("SEND_ME_LIST_OF_ROOMS".encode())
        stringListOfRooms = connection.sock.recv(connection.BUF_SIZE)
        return stringListOfRooms.decode()

