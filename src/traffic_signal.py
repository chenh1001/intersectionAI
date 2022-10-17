from collections import namedtuple
from dataclasses import dataclass
from typing import Iterable
from configurable_object import ConfigurableObject
from copy import copy


class TrafficSignal(ConfigurableObject):

    def __init__(self, road, config=None) -> None:
        super().__init__(config)

        self.road = road
        self.is_active = False

    def set_default_config(self):
        self.slow_distance = 70
        self.slow_factor = 0.4
        self.stop_distance = 20
        self.x = 0

    # @property
    # def current_cycle(self):
    #     return self.cycle[self.current_cycle_index]

    # def update(self, time):
    #     k = (time // self.cycle_length) % len(self.cycle)
    #     self.current_cycle_index = int(k)


@dataclass
class Intersection:
    """Signals properties of an intersection"""

    signals_groups: Iterable[TrafficSignal]
    timers: Iterable[float]
    current_cycle_index: int = 0

    def get_active_signals_index(self, time):
        delta_time = time % sum(self.timers)
        timers_sums = [
            sum(self.timers[:i + 1]) for i, _ in enumerate(self.timers)
        ]
        for i, timers_sum in enumerate(timers_sums):
            if delta_time < timers_sum:
                break
        return i


class TrafficSignalManager(ConfigurableObject):

    def __init__(self, config=None) -> None:
        super().__init__(config)

        self.intersections = []

    @property
    def signals(self):
        for intersection in self.intersections:
            for signal_group in intersection.signals_groups:
                for signal in signal_group:
                    yield signal

    def add_traffic_signals_group(self, signal_groups, timers):
        assert len(signal_groups) == len(
            timers), "Signals groups and timers len should be equal."

        self.intersections.append(Intersection(signal_groups, timers))
        for signal_group in signal_groups:
            for signal in signal_group:
                signal.road.add_traffic_signal(signal)

    def update(self, time):
        for intersection in self.intersections:
            active_index = intersection.get_active_signals_index(time)
            for i, signal_group in enumerate(intersection.signals_groups):
                for signal in signal_group:
                    signal.is_active = i == active_index
