from road import Point
from scipy.spatial.distance import euclidean
from copy import copy


class Vehicle:

    def __init__(self, config={}):
        # Calculate properties
        self.length = 10  # Length of vehicle
        self.width = 8  # Length of vehicle
        self.s0 = 4  # min distance between vehicles
        self.v_max = 16.6
        self.a_max = 1.44
        self.b_max = 4.61

        self.path = list()

        self.x = 0  # Distance
        self.v = self.v_max  # Velocity
        self.a = 0  # Accelaration

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, copy(val))

    @property
    def current_road(self):
        if self.path:
            return self.path[0]

    def get_position(self):
        # If out of roads, return None
        if not self.path:
            return None

        current_road = self.current_road
        for i, distance in enumerate(current_road.distances_array):
            if self.x < distance:
                break
        p1, p2 = current_road.points[i - 1], current_road.points[i]
        length = self.x - distance
        whole_distance = euclidean(p2, p1)
        angle_cos = (p2.x - p1.x) / whole_distance
        angle_sin = (p2.y - p1.y) / whole_distance
        x = p2.x + angle_cos * length
        y = p2.y + angle_sin * length

        # Point ,cos, sin
        return (Point(x, y), angle_cos, angle_sin)

    def update(self, lead, dt):
        # Update position and velocity
        if self.v + self.a * dt < 0:
            self.x -= 1 / 2 * self.v * self.v / self.a
            self.v = 0
        else:
            self.v += self.a * dt
            self.x += self.v * dt + self.a * dt * dt / 2
        # Update acceleration, copy pasted formula
        # alpha = 0
        # if lead:
        #     delta_x = lead.x - self.x - lead.length
        #     delta_v = self.v - lead.v

        #     alpha = (self.s0 + max(0, self.v + delta_v*self.v/self.sqrt_ab)) / delta_x

        # self.a = self.a_max * (1-(self.v/self.v_max)**4 - alpha**2)
