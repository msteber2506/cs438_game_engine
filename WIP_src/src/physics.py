from render import Frame, Drawable
import math


class Collision:

    def __init__(self):
        pass

    @staticmethod
    def intersect(rect1, rect2):
        if (rect1.xloc < rect2.xloc + rect2.width) and (rect1.xloc + rect1.width > rect2.xloc) and (
                rect1.yloc < rect2.yloc + rect2.height) and (rect1.height + rect1.yloc > rect2.yloc):
            return True
        return False

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2D(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2D(self.x / scalar, self.y / scalar)

    def magnitude(self):
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        mag = self.magnitude()
        if mag != 0:
            return Vector2D(self.x / mag, self.y / mag)
        else:
            return Vector2D(0, 0)

class Rigidbody2D:
    def __init__(self, shape, position, rotation, mass, moment_of_inertia, linear_velocity, angular_velocity):
        self.shape = shape
        self.position = position
        self.rotation = rotation
        self.mass = mass
        self.moment_of_inertia = moment_of_inertia
        self.linear_velocity = linear_velocity
        self.angular_velocity = angular_velocity
        self.forces = []

    def apply_force(self, force):
        self.forces.append(force)

    def update(self, dt):
        net_force = sum(self.forces, Vector2D(0, 0))

        # Runs Explicit Euler
        acceleration = net_force / self.mass
        self.linear_velocity += acceleration * dt
        self.position += self.linear_velocity * dt

        angular_acceleration = sum([torque / self.moment_of_inertia for torque in self.forces], 0)
        self.angular_velocity += angular_acceleration * dt
        self.rotation += self.angular_velocity * dt

        # Clear forces for the next step
        self.forces = []

class PhysicsWorld:
    def __init__(self):
        self.objects = []
        self.gravity = Vector2D(0, -9.8)

    def set_gravity(self, gravity):
        self.gravity = gravity

    def add_object(self, rigidbody):
        self.objects.append(rigidbody)

    def remove_object(self, rigidbody):
        self.objects.remove(rigidbody)

    def apply_forces(self):
        for obj in self.objects:
            obj.apply_force(self.gravity * obj.mass)

    def update(self, dt):
        for obj in self.objects:
            obj.update(dt)

    def simulate_step(self, dt):
        self.apply_forces()
        self.update(dt)

class ProjectileThrower:
    def __init__(self, projectile):
        self.projectile = projectile

