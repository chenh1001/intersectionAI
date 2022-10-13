import enum
from road import Road
from vehicle_generator import VehicleGenerator
from configurable_object import ConfigurableObject


class Simulation(ConfigurableObject):
    """Update roads and vehicles."""

    def set_default_config(self):
        self.time: float = 0.0  # Time keeping
        self.frame_count: int = 0  # Frame count keeping
        self.d_time: float = 1 / 60  # Simulation time step
        self.roads = []  # Array to store roads
        self.generators = []
        self.traffic_signals = []

    def create_gen(self, config={}):
        gen = VehicleGenerator(self, config)
        self.generators.append(gen)
        return gen

    def create_road(self, *points):
        road = Road(*points)
        self.roads.append(road)
        return road

    def create_roads(self, roads):
        for road in roads:
            self.create_road(*road)

    def create_traffic_signals_group(self, *signal_groups, cycles=None):
        if not cycles:
            cycles = []
            number_of_cycles = len(signal_groups)
            for i, signal_group in enumerate(signal_groups):
                signal_cycle = [False] * number_of_cycles
                signal_cycle[i] = True
                cycles.append(signal_cycle)
        print("CYLES: {}".format(cycles))

        for cycle, signal_group in zip(cycles, signal_groups):
            for signal in signal_group:
                signal.road.add_traffic_signal(signal, cycle)
                self.traffic_signals.append(signal)

    def update(self):

        # Update every road
        for road in self.roads:
            road.update(self.d_time)

        # Add vehicles
        for gen in self.generators:
            gen.update()

        for signal in self.traffic_signals:
            signal.update(self.time)

        for road in self.roads:
            # If road has no vehicles, continue
            if len(road.vehicles) == 0: continue

            vehicle = road.vehicles[0]
            # If first vehicle is out of road bounds
            if vehicle.x >= road.length:
                vehicle.path.remove(road)
                # If vehicle has a next road
                if vehicle.path:
                    # New length is the remaining path outside the current road
                    vehicle.x -= road.length

                    # next_road = vehicle.path[vehicle.current_road_index]
                    vehicle.current_road.vehicles.append(vehicle)

                # In all cases, remove it from its road
                road.vehicles.remove(vehicle)

        # Increment time
        self.time += self.d_time
        self.frame_count += 1

    def run(self, steps):
        for _ in range(steps):
            self.update()
