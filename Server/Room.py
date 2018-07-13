class Room:
    #state
    #listOfObservers
    #nameOfRoom

    def __init__(self, nameOfRoom):
        self.listOfObservers = set()
        self.nameOfRoom = nameOfRoom
        self.state = ""

    def setState(self,msg, nick):
        self.state = msg
        self.__notifyAllObservers(nick)

    def notifyThatJoined(self, nick):
        newFrame = "[#-" + self.nameOfRoom + "-#]: " + nick + " joined to room"
        for obs in self.listOfObservers:
            obs.update(newFrame)

    def notifyThatLeft(self, nick):
        newFrame = "[#-" + self.nameOfRoom + "-#]: " + nick + " left from room"
        for obs in self.listOfObservers:
            obs.update(newFrame)
        print(newFrame)

    def attach(self, observer):
        self.listOfObservers.add(observer)

    def detach(self, nick):
        for observer in self.listOfObservers:
            if observer.nick == nick:
                self.listOfObservers.remove(observer)
                break

    def __notifyAllObservers(self, nick):
        newFrame = "[" + nick + "]:" + self.state
        self.__checkClientConnection()
        for obs in self.listOfObservers:
            if obs.nick != nick:
                obs.update(newFrame)

    def __checkClientConnection(self):
        disconnectClients = set()
        for obs in self.listOfObservers:
            if obs.checkIfLostConnection() == False:
                disconnectClients.add(obs)
        #wywalanie ich
        for obs in disconnectClients:
            self.detach(obs.nick)
        for obs in disconnectClients:
            self.notifyThatLeft(obs.nick)




