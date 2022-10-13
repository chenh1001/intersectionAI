from itertools import cycle
from curve import curve_points
from simulation import Simulation
from window import Window
from traffic_signal import TrafficSignal

sim = Simulation()
# reut_roads = [
#     sim.create_road((1200, 500), (1200, 300), (1000, 300)),
#     sim.create_road((750, 500), (950, 500), (950, 300)),
#     sim.create_road((950, 500), (820, 330)),
#     sim.create_road((700, 500), (700, 300)),
#     sim.create_road((650, 500), (650, 300), (400, 300), (400, 500), (350, 500))
# ]

# Play with these
# n = 15
# a = 2
# b = 12
# l = 300

X = 50
L = 1000
A = 100
NORTH_START =  (0, -L)
NORTH_END =  (0, -A)
NORTH_F_START = (NORTH_START[0] - X, NORTH_START[1])
NORTH_F_END = (NORTH_START[0] - X, NORTH_END[1])
NORTH_B_START = (NORTH_START[0] + X, NORTH_START[1])
NORTH_B_END = (NORTH_START[0] + X, NORTH_END[1])

SOUTH_START =  (0, L)
SOUTH_END =  (0, A)
SOUTH_F_START = (SOUTH_START[0] + X, SOUTH_START[1])
SOUTH_F_END = (SOUTH_START[0] + X, SOUTH_END[1])
SOUTH_B_START = (SOUTH_START[0] - X, SOUTH_START[1])
SOUTH_B_END = (SOUTH_START[0] - X, SOUTH_END[1])

WEST_START = (-L, 0)
WEST_END = (-A, 0)
WEST_F_START = (WEST_START[0], WEST_START[1] + X)
WEST_F_END = (WEST_END[0], WEST_END[1] + X)
WEST_B_START = (WEST_START[0], WEST_START[1] - X)
WEST_B_END = (WEST_END[0], WEST_END[1] - X)

EAST_START = (L, 0)
EAST_END = (A, 0)
EAST_F_START = (EAST_START[0], EAST_START[1] - X)
EAST_F_END = (EAST_END[0], EAST_END[1] - X)
EAST_B_START = (EAST_START[0], EAST_START[1] + X)
EAST_B_END = (EAST_END[0], EAST_END[1] + X)

NORTH_F = sim.create_road(NORTH_F_START, NORTH_F_END)
SOUTH_F = sim.create_road(SOUTH_F_START, SOUTH_F_END)
WEST_F = sim.create_road(WEST_F_START, WEST_F_END)
EAST_F = sim.create_road(EAST_F_START, EAST_F_END)

NORTH_B = sim.create_road(NORTH_B_END, NORTH_B_START)
SOUTH_B = sim.create_road(SOUTH_B_END, SOUTH_B_START)
WEST_B = sim.create_road(WEST_B_END, WEST_B_START)
EAST_B = sim.create_road(EAST_B_END, EAST_B_START)

NORTH_EAST = sim.create_road(*curve_points(NORTH_F_END, EAST_B_END, (NORTH_F_END[0], EAST_B_END[1])))
NORTH_SOUTH = sim.create_road(NORTH_F_END, SOUTH_B_END)
NORTH_WEST = sim.create_road(*curve_points(NORTH_F_END, WEST_B_END, (NORTH_F_END[0], WEST_B_END[1])))

SOUTH_EAST = sim.create_road(*curve_points(SOUTH_F_END, EAST_B_END, (SOUTH_F_END[0], EAST_B_END[1])))
SOUTH_NORTH = sim.create_road(SOUTH_F_END, NORTH_B_END)
SOUTH_WEST = sim.create_road(*curve_points(SOUTH_F_END, WEST_B_END, (SOUTH_F_END[0], WEST_B_END[1])))

WEST_SOUTH = sim.create_road(*curve_points(WEST_F_END, SOUTH_B_END, (SOUTH_B_END[0], WEST_F_END[1])))
WEST_EAST = sim.create_road(WEST_F_END, EAST_B_END)
WEST_NORTH = sim.create_road(*curve_points(WEST_F_END, NORTH_B_END, (NORTH_B_END[0], WEST_F_END[1])))

EAST_SOUTH = sim.create_road(*curve_points(EAST_F_END, SOUTH_B_END, (SOUTH_B_END[0], EAST_F_END[1])))
EAST_WEST = sim.create_road(EAST_F_END, WEST_B_END)
EAST_NORTH = sim.create_road(*curve_points(EAST_F_END, NORTH_B_END, (NORTH_B_END[0], EAST_F_END[1])))


sim.create_traffic_signals_group([TrafficSignal(NORTH_F), TrafficSignal(SOUTH_F)],
                                 [TrafficSignal(WEST_F), TrafficSignal(EAST_F)],
                                 cycles=[(True, False), (False, True)])

sim.create_gen({
    'vehicle_rate':
    50,
    'vehicles': [
        [1, {
            'path': [NORTH_F, NORTH_EAST, EAST_B],
        }],
        [1, {
            'path': [NORTH_F, NORTH_WEST, WEST_B],
        }],
        [1, {
            'path': [NORTH_F, NORTH_SOUTH, SOUTH_B],
        }],
        [1, {
            'path': [SOUTH_F, SOUTH_EAST, EAST_B],
        }],
        [1, {
            'path': [SOUTH_F, SOUTH_WEST, WEST_B],
        }],
        [1, {
            'path': [SOUTH_F, SOUTH_NORTH, NORTH_B],
        }],
        [1, {
            'path': [WEST_F, WEST_EAST, EAST_B],
        }],
        [1, {
            'path': [WEST_F, WEST_SOUTH, SOUTH_B],
        }],
        [1, {
            'path': [WEST_F, WEST_NORTH, NORTH_B],
        }],
        [1, {
            'path': [EAST_F, EAST_WEST, WEST_B],
        }],
        [1, {
            'path': [EAST_F, EAST_SOUTH, SOUTH_B],
        }],
        [1, {
            'path': [EAST_F, EAST_NORTH, NORTH_B],
        }],
    ]
})
# Start simulation
win = Window(sim)
win.run(10)
