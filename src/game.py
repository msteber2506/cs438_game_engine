from render import Frame, Drawable
from player import Player
from input import EventListener
from physics import PhysicsWorld
import cv2
import time

class Game:

    def __init__(self, frame):
        self.frame = frame
        self.physics_world = PhysicsWorld()

    @staticmethod
    def tick(fps):
        interval = 1.0 / fps
        time.sleep(interval)

    def run(self, fps):
        while True:
            self.frame.render()
            self.physics_world.simulate_step(1 / fps)
            self.tick(fps)


if __name__ == '__main__':

    frame = Frame(500, 500)
    game = Game(frame)

    square = Drawable(500, 100, 0, 400)
    frame.addDrawable(square)

    player = Player(20, 20, 100, 100, r"resources/mario.png")
    frame.addDrawable(player)

    EventListener = EventListener()

    while True:
        # main game loop code goes here

        player.action(EventListener.pressed_key)
        player.move("down")

        # update and render frame
        frame.update()
        frame.render()
        Game.tick(60)
        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break
    cv2.destroyAllWindows()
