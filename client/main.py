from network import GameNetworkFactory

from kivy.app import App
from kivy.animation import Animation
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from kivy.properties import NumericProperty, ReferenceListProperty,\
    ObjectProperty
from kivy.vector import Vector
from random import randint
from kivy.clock import Clock

from twisted.internet import reactor


class PongBall(Widget):

    def move(self, x, y):
        x = x * self.pong_game.width - self.width/2
        y = y * self.pong_game.height - self.height/2
        anim = Animation(x=x, y=y, duration=0.1)
        anim.start(self)


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = vel
        self.ball.pong_game = self

    def update(self, dt):
        self.ball.move()

        #bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        #bounce ball off bottom or top
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1

        #went of to a side to score point?
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        self.player1.center_y = touch.y
        data = self.player1.center_y / float(self.height)
        data = "%f_" % data
        print(data)
        self.connection.write(data)

    def update_enemy(self, position):
        location = position * self.height - self.player2.height/2
        anim = Animation(y=location, duration=0.1)
        anim.start(self.player2)

    def update_ball(self, x, y):
        self.ball.move(x, y)


class PongApp(App):
    connection = None
    state = None

    player1_name = ""
    player2_name = None

    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.button = Button(text="Que for A Game", on_press=self.que_for_game)
        self.textinput = TextInput(hint_text="Enter Your Name")
        self.layout.add_widget(self.textinput)
        self.layout.add_widget(self.button)
        return self.layout
        # game = PongGame()
        # game.serve_ball()
        # Clock.schedule_interval(game.update, 1.0 / 60.0)
        # self.connect_to_server()
        # return game

    def que_for_game(self, what):
        self.state = "in_que"
        self.player1_name = self.textinput.text
        self.connect_to_server()
        self.layout.remove_widget(self.button)
        self.label = Label(text="Wait For A Player")
        self.layout.add_widget(self.label)

    def start_game(self):        
        self.layout.clear_widgets()
        self.game = PongGame()
        self.game.connection = self.connection
        self.game.serve_ball()
        # Clock.schedule_interval(self.game.update, 1.0 / 60.0)
        self.layout.add_widget(self.game)
        self.state = "in_game"

    def setup_gui(self):
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.send_message)
        self.label = Label(text='connecting...\n')
        self.layout = BoxLayout(orientation='vertical')
        self.layout.add_widget(self.label)
        self.layout.add_widget(self.textbox)
        return self.layout

    def connect_to_server(self):
        reactor.connectTCP('localhost', 8000, GameNetworkFactory(self))

    def on_connection(self, connection):
        self.connection = connection

    def send_message(self):
        pass

if __name__ == '__main__':
    PongApp().run()