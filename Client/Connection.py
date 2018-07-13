import socket
from termcolor import cprint
from Sending import Sending
from Receiving import Receiving
from NickManager import NickManager

class Connection():
    BUF_SIZE = 32#100
    ADDR = socket.gethostbyname(socket.gethostname())
    PORT = 8000

    def __init__(self, socket):
        self.nick = "###"
        self.currentRoom = ""
        self.inLobby = True
        self.b_receiving = False
        self.sock = socket
        self.listOfRooms = set()

    def showMenu(self):
        b_option = False
        while b_option == False:
            print("0 - close program")
            print("available rooms:")
            self.__displayListOfRooms()
            print("enter name of room to join")
            option = input()

            if option == "0":
                return "EXIT"
            b_option = self.__validOption(option)
        return option

    def __validOption(self, s_option):
        if s_option == "0":
            return True
        for roomName in self.listOfRooms:
            if roomName == s_option:
                return True
        return False

    def executeOption(self, option):
        if option == "EXIT":
            Sending.send(self.sock, option)
            response = Receiving.receive(self)
            if response == "EXIT":
                self.sock.close()
                cprint("you are disconnected", 'red')
                return
        if option.split("::")[0] == "JOIN":
            Sending.send(self.sock, option)#poinformuj serwer ze join
            #serwer czeka na nick
            if self.nick == "###":
                nick = NickManager.chooseNick(self)#uruchom opcje dajaca nowy nick
                self.nick = nick
            #else:
            #self.inLobby = False to juz w main jest
            self.currentRoom = option.split("::")[2]
            return
        if option.split("::")[0] == "ESCAPE":
            Sending.send(self.sock, option)# powiadom serwer ze chce wyjsc z rozmowy
            response = Receiving.receive(self)
            if response == "YOU_LEFT_ROOM":
                self.inLobby = True
                self.b_receiving = False
                self.currentRoom = "###"
                cprint("you leaved room", 'red')
                self.nick = "###"
                return
        Sending.send(self.sock, option)


    def __displayListOfRooms(self):
        stringListOfRooms = Receiving.getListOfRooms(self)

        arrayListOfRooms = stringListOfRooms.split("::")
        arrayListOfRooms.remove(arrayListOfRooms[0])#pierwszy element to rozm listy
        lastElement = len(arrayListOfRooms)#ostatni pusty daje w serwerze i split
        arrayListOfRooms.remove(arrayListOfRooms[lastElement-1])
        cprint(arrayListOfRooms, 'green')
        self.listOfRooms = arrayListOfRooms

