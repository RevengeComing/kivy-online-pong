from .protocol import GameServerProtocol

from twisted.internet.protocol import Factory


class GameServerFactory(Factory):
    numConnections = 0

    looking_for_opponent = []
    online_matches = []

    finished_matches = []

    def __init__(self):
        print "Server is Running..."

    def buildProtocol(self, addr):
        return GameServerProtocol(self)