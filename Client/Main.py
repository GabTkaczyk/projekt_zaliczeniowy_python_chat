import sys
import socket
from Connection import Connection
from Sending import Sending
from Receiving import Receiving

if __name__ == "__main__":

    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        conn = Connection(socket)
        socket.connect((conn.ADDR, conn.PORT))
        sending = Sending(conn)
        sending.start()
        receiving = Receiving(conn)
        print("Connected successfully")
        while True:
            if conn.inLobby == True:
                option = conn.showMenu()
                print("you choosed {}".format(option))
                if option == "EXIT":
                    conn.executeOption(option)
                    sys.exit(0)
                option = Sending.prepareOptionToSendToServer(option, conn)
                conn.executeOption(option)
                conn.inLobby = False
                receiving.listen()
    except ConnectionError as err:
        print(err)