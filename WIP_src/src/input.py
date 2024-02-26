from pynput import keyboard
#hwllo

class EventListener:
    pressed_key = None

    def __init__(self, pressed_key=None):
        self.listen_keyboard()

    @staticmethod
    def listen_keyboard():
        listener = keyboard.Listener(on_press=EventListener.on_press, on_release=EventListener.on_release)
        listener.start()

    @staticmethod
    def on_press(key):
        EventListener.pressed_key = key

    @staticmethod
    def on_release(key):
        EventListener.pressed_key = None

    def my_on_press(self, key):
        self.pressed_key = key

