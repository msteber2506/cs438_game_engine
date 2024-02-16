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

class PhysicsObject:
    def __init__(self, x=0, y=0, vx=0, vy=0):
        self.x = x  # initial x position
        self.y = y  # initial y position
        self.vx = vx  # initial velocity in x direction
        self.vy = vy  # initial velocity in y direction
    
    def update(self, dt):
        # Update position using kinematic equations
        self.x += self.vx * dt
        self.y += self.vy * dt

class PhysicsSystem:
    def __init__(self):
        self.objects = []
    
    def add_object(self, obj):
        self.objects.append(obj)
    
    def update(self, dt):
        for obj in self.objects:
            obj.update(dt)