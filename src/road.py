from math import dist
from scipy.spatial import distance
from collections import deque
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])

class Road:
    WIDTH = 10

    def __init__(self, *points):
        self.points = list(points)
        for i, point in enumerate(self.points):
            self.points[i] = Point(point[0], point[1])

        self.vehicles = []

        self.init_properties()

    def init_properties(self):
        total_length = 0
        distances_array = [0]
        for i, point in enumerate(self.points):
            if not i + 1 < len(self.points):
                break
            total_length += distance.euclidean(point, self.points[i+1])
            distances_array.append(total_length)
        self.length = total_length
        self.distances_array = distances_array

    def update(self, d_time):
        if not self.vehicles:
            return

        # Update vehicles
        for i, vehicle in enumerate(self.vehicles):
            lead = self.vehicles[i-1] if i > 0 else None
            vehicle.update(lead, d_time)
            
        vehicle = self.vehicles[0]
        # If first vehicle is out of road bounds
        if vehicle.x >= self.length:
            vehicle.path.remove(self)
            # If vehicle has a next road
            if vehicle.path:
                # New length is the remaining path outside the current road
                vehicle.x -= self.length
                # vehicle.x = 0

                # Add it to the next road
                next_road = vehicle.path[0]
                # next_road = vehicle.path[vehicle.current_road_index]
                next_road.vehicles.append(vehicle)

            # In all cases, remove it from its road
            self.vehicles.remove(vehicle)
