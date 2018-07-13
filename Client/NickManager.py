class NickManager:

    @staticmethod
    def __validNick(nick):
        if not nick:
            print("nick can't be empty")
            return False
        if nick == "###":
            print("choose another nick")
            return False
        return True

    @staticmethod
    def chooseNick(connection):
        print("enter your nick")
        while True:
            nick = input()
            b_nick =  NickManager.__validNick(nick)
            if b_nick:
                #wysylam serwerowi nick do spr
                connection.sock.send(nick.encode())
                response = connection.sock.recv(connection.BUF_SIZE).decode()
                if response == "YOU_ARE_REGISTERED":
                    return nick
                else:
                    print("nick id in use or incorrect")
