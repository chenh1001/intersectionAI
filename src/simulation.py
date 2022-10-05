from road import Road
from vehicle_generator import VehicleGenerator

class Simulation:
    """Update roads and vehicles."""

    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.time: float = 0.0  # Time keeping
        self.frame_count: int = 0  # Frame count keeping
        self.d_time: float = 1 / 60  # Simulation time step
        self.roads = []  # Array to store roads
        self.generators = []
    
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

    def update(self):
        # Update every road
        for road in self.roads:
            road.update(self.d_time)
        
        # Add vehicles
        for gen in self.generators:
            gen.update()

        # Increment time
        self.time += self.d_time
        self.frame_count += 1

    def run(self, steps):
        for _ in range(steps):
            self.update()
        
      
