import numpy as np

class Vehicle:
    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

        # Calculate properties
        self.init_properties()

    def set_default_config(self):    
        self.length = 4 # Length of vehicle
        self.s0 = 4 # min distance between vehicles
        self.v_max = 16.6
        self.a_max = 1.44
        self.b_max = 4.61

        self.path = []
        self.current_road_index = 0

        self.x = 0 # Distance
        self.v = self.v_max # Velocity
        self.a = 0 # Accelaration

    def init_properties(self):
        self.sqrt_ab = 2*np.sqrt(self.a_max*self.b_max)

    def update(self, lead, dt):
        # Update position and velocity
        if self.v + self.a*dt < 0:
            self.x -= 1/2*self.v*self.v/self.a
            self.v = 0
        else:
            self.v += self.a*dt
            self.x += self.v*dt + self.a*dt*dt/2
        
        # Update acceleration, copy pasted formula
        # alpha = 0
        # if lead:
        #     delta_x = lead.x - self.x - lead.length
        #     delta_v = self.v - lead.v

        #     alpha = (self.s0 + max(0, self.v + delta_v*self.v/self.sqrt_ab)) / delta_x

        # self.a = self.a_max * (1-(self.v/self.v_max)**4 - alpha**2)
