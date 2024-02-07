from render import Game, Frame, Drawable
from physics import Collision
from player import Player
import cv2
from pynput.keyboard import Key, Listener



if __name__ == '__main__':

    frame = Frame(500, 500)
    game = Game(frame)

    square = Drawable(500, 100, 0, 400)
    frame.addDrawable(square)

    player = Player(20,20, 100, 100)
    frame.addDrawable(player)

    while True:
        # main game loop code goes here
        # if not Collision.intersect(player, square):
        #     player.yloc += 5

        # Update the player sprite based on user keypresses
        with Listener(on_press=player.move) as listener:
            listener.join()


        # update and render frame
        frame.update()
        frame.render()
        Game.tick(30)
        if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
            break
    cv2.destroyAllWindows()