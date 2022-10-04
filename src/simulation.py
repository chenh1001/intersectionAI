from road import Road

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

            if len(road.vehicles) == 0: continue
            
            vehicle = road.vehicles[0]
            # If first vehicle is out of road bounds
            if vehicle.x >= road.length:
                # If vehicle has a next road
                if vehicle.current_road_index + 1 < len(vehicle.path):
                    # New length is the remaining path outside the current road
                    vehicle.x = vehicle.x - road.length

                    # Add it to the next road
                    vehicle.current_road_index += 1
                    next_road_index = vehicle.path[vehicle.current_road_index]
                    self.roads[next_road_index].vehicles.append(vehicle)

                # In all cases, remove it from its road
                road.vehicles.pop(vehicle)

        # Increment time
        self.time += self.d_time
        self.frame_count += 1

    def run(self, steps):
        for _ in range(steps):
            self.update()
