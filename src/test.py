from curve import curve_road
from simulation import Simulation
from window import Window

sim = Simulation()
sim.create_road((100, 100), (100, 500), (500, 500), (500, 100))
# sim.create_road(curve_road((100, 100), (500, 500), (500, 100)))

# Start simulation
win = Window(sim)
win.run()
