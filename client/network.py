#install_twisted_rector must be called before importing the reactor
from kivy.support import install_twisted_reactor
install_twisted_reactor()


#A simple Client that send messages to the echo server
from twisted.internet import protocol
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.clock import Clock

class GameNetworkClient(protocol.Protocol):

    def connectionMade(self):
        self.factory.app.on_connection(self.transport)
        name = str(self.factory.app.textinput.text)
        self.transport.write("find a match:%s_" % name)

    def dataReceived(self, data):
        print(data)
        try:
            data_list = data.split('_')
        except:
            pass
        while data_list != []:
            what = data_list.pop(0)

            if self.factory.app.state == "in_que":
                if self.factory.app.player2_name or self.factory.app.player2_name == "":
                    if what == "match is starting":
                        self.factory.app.start_game()
                else:
                    what = what.split(':')
                    if what[0] == "ename":
                        self.factory.app.player2_name = what[1]
                    else:
                        print('wtf data')
                        print(what)

            elif self.factory.app.state == "in_game":
                if what == "epoint":
                    self.factory.app.game.player2.score += 1
                elif what == "upoint":
                    self.factory.app.game.player1.score += 1
                elif what == "enemy left the match":
                    self.exit_popup()
                else:
                    what = what.split(':')
                    if what[0] == "ball":
                        ball_position = what[1].split(',')
                        self.factory.app.game.update_ball(float(ball_position[0]), float(ball_position[1]))
                    elif what[0] == "enemy":
                        self.factory.app.game.update_enemy(float(what[1]))                        

    def exit_popup(self):
        pu = Popup(title='Game Notification',
                    content=Label(text='The Enemy Ran Away !'),
                    size_hint=(0.5, 0.5), auto_dismiss=False)
        pu.open()
        Clock.schedule_once(self.exit_game, 4)

    def exit_game(self, dt):
        import sys
        sys.exit(0)



class GameNetworkFactory(protocol.ClientFactory):

    protocol = GameNetworkClient

    def __init__(self, app):
        self.app = app

    def clientConnectionLost(self, conn, reason):
        print("connection lost")

    def clientConnectionFailed(self, conn, reason):
        print("connection failed")
        print(reason)