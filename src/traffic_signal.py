from configurable_object import ConfigurableObject


class TrafficSignal(ConfigurableObject):

    def __init__(self, road, config=None) -> None:
        super().__init__(config)

        self.road = road

    def set_default_config(self):
        self.cycle = [False, True]
        self.slow_distance = 70
        self.slow_factor = 0.4
        self.stop_distance = 20
        self.x = 0

        self.current_cycle_index = 0
        self.last_t = 0
        self.cycle_length = 60

    @property
    def current_cycle(self):
        return self.cycle[self.current_cycle_index]

    def update(self, time):
        k = (time // self.cycle_length) % len(self.cycle)
        self.current_cycle_index = int(k)
