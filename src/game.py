from render import Frame, Drawable
from player import Player
from input import EventListener
from physics import PhysicsWorld
from network import Client, Server
import cv2
import time
import sys

HOST = "127.0.0.1"
PORT = 65432


class Game:

    def __init__(self, frame):
        self.frame = frame
        self.physics_world = PhysicsWorld()

    @staticmethod
    def tick(fps):
        interval = 1.0 / fps
        time.sleep(interval)


if __name__ == '__main__':

    argv = sys.argv[1:]

    frame = Frame(500, 500)
    game = Game(frame)

    square = Drawable(500, 100, 0, 400)
    frame.add_drawable(square)

    player = Player(20, 20, 100, 100, r"resources/mario.png")
    frame.add_drawable(player)

    EventListener = EventListener()

    if len(argv) > 0 and argv[0] == "c":
        client = Client()
        client.start_client()
    else:
        server = Server(HOST, PORT)
        server.start_server()

    while True:
        # main game loop code goes here
        player.action(EventListener.pressed_key)

        # update and render frame
        frame.update()
        frame.render()
        game.physics_world.simulate_step(1 / 60)
        Game.tick(60)
        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break
    cv2.destroyAllWindows()
