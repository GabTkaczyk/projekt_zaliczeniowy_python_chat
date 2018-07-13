class Observer:
    def __init__(self, subject, nick, socket):
        self.subject = subject
        self.subject.attach(self)
        self.nick = nick
        self.socket = socket

    def update(self, frame):
        self.socket.send(frame.encode())

    def checkIfLostConnection(self):
        if "[closed]" in str(self.socket):
            self.socket.close()
            return False
        return True

