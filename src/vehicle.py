from math import dist
import numpy as np
from typing import List
from scipy.spatial.distance import euclidean
from configurable_object import ConfigurableObject
from road import Road, Point


class Vehicle(ConfigurableObject):

    def __init__(self, config=None):
        super().__init__(config)
        self.sqrt_ab = 2 * np.sqrt(self.a_max * self.b_max)
        self.stopped = False
        self.stopped_signal = None

    def set_default_config(self):
        self.length = 10  # Length of vehicle
        self.width = 8  # Length of vehicle
        self.s0 = 4  # min distance between vehicles
        self.v_max = 16.6
        self.a_max = 1.44
        self.b_max = 4.61
        self._v_max = self.v_max

        self.path: List[Road] = []

        self.x = 0  # Distance
        self.v = self.v_max  # Velocity
        self.a = 0  # Accelaration

    @property
    def current_road(self):
        if self.path:
            return self.path[0]

    def get_position(self):
        return Road.get_position(self.x, self.current_road) 

    def update(self, lead, dt):
        # Update position and velocity
        if self.v + self.a * dt < 0:
            self.x -= 1 / 2 * self.v * self.v / self.a
            self.v = 0
        else:
            self.v += self.a * dt
            self.x += self.v * dt + self.a * dt * dt / 2

        # Update acceleration, copy pasted formula
        alpha = 0
        if lead:
            delta_x = lead.x - self.x - lead.length
            delta_v = self.v - lead.v

            alpha = (self.s0 + max(
                0, self.v + delta_v * self.v / self.sqrt_ab)) / delta_x

        self.a = self.a_max * (1 - (self.v / self.v_max)**4 - alpha**2)

        if self.stopped: 
            self.a = -self.b_max * self.v / self.v_max
        
    def stop(self, signal):
        self.stopped = True
        self.stopped_signal = signal

    def unstop(self):
        self.stopped = False
        self.stopped_signal = None

    def slow(self, v, signal):
        self.v_max = v
        self.stopped_signal = signal

    def unslow(self):
        self.v_max = self._v_max
        self.stopped_signal = None
