from scipy.spatial import distance
from collections import namedtuple

Point = namedtuple("Point", ["x", "y"])


class Road:
    WIDTH = 10

    def __init__(self, *points):
        self.points = list(points)
        for i, point in enumerate(self.points):
            self.points[i] = Point(point[0], point[1])

        self.vehicles = []
        self.signals = []
        self.init_properties()

    def init_properties(self):
        total_length = 0
        distances_array = [0]
        for i, point in enumerate(self.points):
            if not i + 1 < len(self.points):
                break
            total_length += distance.euclidean(point, self.points[i + 1])
            distances_array.append(total_length)
        self.length = total_length
        self.distances_array = distances_array

    def add_traffic_signal(self, signal, cycle):
        signal.cycle = cycle
        self.signals.append(signal)

    def update(self, d_time):
        if not self.vehicles:
            return

        # Update vehicles
        for i, vehicle in enumerate(self.vehicles):
            lead = self.vehicles[i - 1] if i > 0 else None
            vehicle.update(lead, d_time)

            for traffic_signal in self.signals:

                if traffic_signal.current_cycle:
                    # If traffic signal is green or doesn't exist
                    # Then let vehicles pass
                    if traffic_signal == vehicle.stopped_signal:
                        vehicle.unstop()
                        vehicle.unslow()
                else:
                    if vehicle.x > self.length - traffic_signal.x:
                        vehicle.unstop()
                        vehicle.unslow()
                    # If traffic signal is red
                    if not vehicle.stopped and vehicle.x >= self.length - traffic_signal.x - traffic_signal.slow_distance and\
                        vehicle.x < self.length - traffic_signal.x - traffic_signal.stop_distance:
                        # Slow vehicles in slowing zone
                        vehicle.slow(
                            traffic_signal.slow_factor * vehicle._v_max,
                            traffic_signal)
                    if vehicle.x >= self.length - traffic_signal.x - traffic_signal.stop_distance and\
                        vehicle.x <= self.length - traffic_signal.x - traffic_signal.stop_distance / 2:
                        # Stop vehicles in the stop zone
                        vehicle.stop(traffic_signal)

    @staticmethod
    def get_position(x, road):
        for i, total_distance in enumerate(road.distances_array):
            if x < total_distance:
                break
        p1, p2 = road.points[i - 1], road.points[i]
        length = x - total_distance
        whole_distance = distance.euclidean(p2, p1)
        angle_cos = (p2.x - p1.x) / whole_distance
        angle_sin = (p2.y - p1.y) / whole_distance
        x = p2.x + angle_cos * length
        y = p2.y + angle_sin * length

        # Point ,cos, sin
        return (Point(x, y), angle_cos, angle_sin)
