from render import Drawable
import numpy as np

class Collision:

    def __init__(self):
        pass

    @staticmethod
    def intersect(rect1, rect2):
        if (rect1.xloc < rect2.xloc + rect2.width) and (rect1.xloc + rect1.width > rect2.xloc) and (
                rect1.yloc < rect2.yloc + rect2.height) and (rect1.height + rect1.yloc > rect2.yloc):

            return True
        return False


'''
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
'''


class PhysicsWorld:
    def __init__(self, gravity=(0, 9.8)):
        self.gravity = np.array(gravity, dtype=float)
        self.objects = []

    def add_object(self, obj):
        self.objects.append(obj)

    def remove_object(self, obj):
        if obj in self.objects:
            self.objects.remove(obj)

    def simulate_step(self, dt):
        for obj in self.objects:
            obj.apply_force(self.gravity * obj.mass)

        # Step 2: Run numerical integration (Explicit Euler)
        for obj in self.objects:
            obj.update(dt)

class PhysicsObject(Drawable):
    def __init__(self, x, y, mass, width, height, rotation, sprite):
        super().__init__(width, height, x, y)
        self.mass = mass
        self.velocity = np.array([0.0, 0.0], dtype=float)
        self.acceleration = np.array([0.0, 0.0], dtype=float)
        self.sprite = sprite
        self.rotation = rotation

    def apply_force(self, force):
        # Newton's second law: F = ma => a = F/m
        self.acceleration += force / self.mass

    def update(self, dt):
        # Update velocity based on acceleration
        self.velocity += self.acceleration * dt
        
        # Update position based on velocity
        super().xloc += self.velocity[0] * dt
        super().yloc += self.velocity[1] * dt

        # Reset acceleration for next frame
        self.acceleration = np.array([0.0, 0.0], dtype=float)

    def draw(self, frame):
        frame.draw(self)

    def get_midpoint_of_edge(self):
        # Calculate corner coordinates relative to center
        half_width = self.width / 2
        half_height = self.height / 2
        corners = np.array([[-half_width, half_height], [half_width, half_height],
                            [half_width, -half_height], [-half_width, -half_height]])

        # Rotate corners
        rotation_matrix = np.array([[np.cos(np.radians(self.rotation)), -np.sin(np.radians(self.rotation))],
                                    [np.sin(np.radians(self.rotation)), np.cos(np.radians(self.rotation))]])
        rotated_corners = np.dot(corners, rotation_matrix.T)
        midpoint = (rotated_corners[1] + rotated_corners[2]) / 2

        # Translate midpoint to absolute coordinates
        absolute_midpoint = midpoint + np.array([self.xloc, self.yloc])

        return tuple(absolute_midpoint)

class ProjectileThrower:
    def __init__(self, projectile):
        self.projectile = projectile

class Projectile(PhysicsObject):
    def __init__(self, x, y, mass, velocity_x, velocity_y, width, height, rotation, sprite):
        super().__init__(x, y, mass, width, height, rotation, sprite)
        self.velocity = np.array([velocity_x, velocity_y], dtype=float)

    def update(self, dt):
        # Apply gravitational acceleration
        self.acceleration += np.array([0.0, -9.8])  # Assuming gravity is in the negative y-direction

        # Update velocity using Explicit Euler
        self.velocity += self.acceleration * dt

        # Update position using Explicit Euler
        self.xloc += self.velocity[0] * dt
        self.yloc += self.velocity[1] * dt

        # Update rotation angle
        self.rotation_angle = np.arctan2(self.velocity[1], self.velocity[0]) * 180 / np.pi

        # Reset acceleration for next frame
        self.acceleration = np.array([0.0, 0.0], dtype=float)
