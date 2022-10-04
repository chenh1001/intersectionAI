from scipy.spatial import distance
from collections import deque
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])

class Road:
    WIDTH = 10

    def __init__(self, *points):
        self.points = list(points)
        print("POINT ARE {}".format(self.points))
        for i, point in enumerate(self.points):
            self.points[i] = Point(point[0], point[1])

        self.vehicles = deque()

        self.init_properties()

    def init_properties(self):
        total_length = 0
        for i, point in enumerate(self.points):
            if not i + 1 < len(self.points):
                break
            total_length += distance.euclidean(point, self.points[i+1])
        self.length = total_length

    def update(self, d_time):
        n = len(self.vehicles)

        if n > 0:
            # Update first vehicle
            self.vehicles[0].update(None, d_time)
            # Update other vehicles
            for i in range(1, n):
                lead = self.vehicles[i-1]
                self.vehicles[i].update(lead, d_time)
