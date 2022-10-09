from numpy.random import randint
from configurable_object import ConfigurableObject
from vehicle import Vehicle


class VehicleGenerator(ConfigurableObject):

    def __init__(self, sim, config=None):
        super().__init__(config)

        self.sim = sim
        self.upcoming_vehicle = self.generate_vehicle()

    def set_default_config(self):
        """Set default configuration."""

        self.vehicle_rate = 20
        self.vehicles = [(1, {})]
        self.last_added_time = 0

    def generate_vehicle(self):
        """Returns a random vehicle from self.vehicles with random proportions."""

        total = sum(pair[0] for pair in self.vehicles)
        r = randint(1, total + 1)
        for (weight, config) in self.vehicles:
            r -= weight
            if r <= 0:
                return Vehicle(config)

    def update(self):
        """Add vehicles."""

        if self.sim.time - self.last_added_time >= 60 / self.vehicle_rate:
            # If time elasped after last added vehicle is
            # greater than vehicle_period; generate a vehicle
            road = self.upcoming_vehicle.path[0]
            if len(road.vehicles) == 0\
               or road.vehicles[-1].x > self.upcoming_vehicle.s0 + self.upcoming_vehicle.length:
                # If there is space for the generated vehicle; add it
                road.vehicles.append(self.upcoming_vehicle)
                # Reset last_added_time and upcoming_vehicle
                self.last_added_time = self.sim.time
            self.upcoming_vehicle = self.generate_vehicle()
