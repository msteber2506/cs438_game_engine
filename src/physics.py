from render import Frame, Drawable


class Collision:

    def __init__(self):
        pass

    @staticmethod
    def intersect(rect1, rect2):
        if (rect1.xloc < rect2.xloc + rect2.width) and (rect1.xloc + rect1.width > rect2.xloc) and (
                rect1.yloc < rect2.yloc + rect2.height) and (rect1.height + rect1.yloc > rect2.yloc):
            return True
        return False
