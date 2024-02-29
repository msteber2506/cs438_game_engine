from render import Game, Frame, Drawable
from player import Player
from input import EventListener
import cv2


if __name__ == '__main__':

    # frame = Frame(500, 500)
    # game = Game(frame)

    # square = Drawable(500, 100, 0, 400)
    # frame.addDrawable(square)

    # player = Player(20, 20, 100, 100)
    # frame.addDrawable(player)

    EventListener = EventListener()

    background_path = '../../resources/Background.png'
    sprite_path = '../../resources/mario.png'
    frame = Frame(background_path)
    game = Game(frame)
    player = Player(sprite_path, frame)

    temp_var = 0
    while True:
        # main game loop code goes here

        #player.action(EventListener.pressed_key)
        # frame.update()
        # frame.render()

        temp_var += 1
        
        # Game.tick(30)
        # if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        #     break

        # if temp_var == 50:
        #     player.resize_factor = 0.7  # Update the resize factor
        #     player.sprite = player.resize_sprite(player.sprite, player.resize_factor)
            
        frame.render(player)

        Game.tick(30)
        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            break
        # elif key == ord('y'):
        #     player.resize_factor = 0.7  # Update the resize factor
        #     player.sprite = player.resize_sprite(player.sprite, player.resize_factor)
        # elif key == ord('u'):
        #     player.resize_factor = 1.3  # Update the resize factor
        #     player.sprite = player.resize_sprite(player.sprite, player.resize_factor)

        frame.render(player)

        player.action(key)

        frame.move_background(player)

    cv2.destroyAllWindows()