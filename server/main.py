from twisted.internet import reactor 
from core.factory import GameServerFactory

reactor.listenTCP(8000, GameServerFactory() )
reactor.run()