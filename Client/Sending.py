import threading

class Sending(threading.Thread):
    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.conn = connection

    def run(self):
        while True:
            if self.conn.inLobby == False:
                print("welcome in currentRoom " + self.conn.currentRoom)
                print("( empty message to exit )")

                while True:
                    message = input()
                    if message == "":
                        self.conn.b_receiving = False
                        frame = Sending.prepareOptionToSendToServer("ESCAPE", self.conn)
                        self.conn.executeOption(frame)
                        break
                    try:
                        message = Sending.prepareOptionToSendToServer("MSG::" + message, self.conn)
                        Sending.send(self.conn.sock, message)
                        continue
                    except ConnectionResetError as err:
                        print("Server is down... {}".format(err))
                        print(err)
                        self.conn.sock.close()
                        break

    @staticmethod
    def send(sock, message):
        sock.send(message.encode())

    def prepareOptionToSendToServer(option, conn):
        if option in conn.listOfRooms:
            messageForServer = option + "::" + conn.nick
            size = len(messageForServer)
            #wysyla JOIN::size::<nazwa pokoju>::<nick>
            messageForServer = "JOIN::" + str(size) + "::" + messageForServer
            return messageForServer
        if option == "CREATE":
            print("bedzie create")  # todo jeszcze delete pokoj
            #na serwerze moze - nazwa pokoju nie moze byc create ani escape ani delete
        if option == "ESCAPE":
            #wysyla ESCAPAE::<rozm>::<roomName>::<nick>
            messageForServer = conn.currentRoom + "::" + conn.nick
            size = len(messageForServer)
            messageForServer = "ESCAPE::" + str(size) + "::" + messageForServer
            return messageForServer
        if option.split("::")[0] == "MSG":
            messageFromUser = option.split("::")[1]
            messageForServer = conn.currentRoom + "::" + conn.nick + "::" + messageFromUser
            size = len(messageForServer)
            messageForServer = "MSG::" + str(size) + "::" + messageForServer
            return messageForServer



