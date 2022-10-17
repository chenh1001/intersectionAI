from itertools import cycle
from curve import curve_points
from simulation import Simulation
from window import Window
from traffic_signal import TrafficSignal
from road import Road

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

X = 30
L = 1000
A = 150
B = Road.WIDTH * 2

# North
NORTH_START = (0, -L)
NORTH_END = (0, -A)
NORTH_F_RIGHT_START = (NORTH_START[0] - X - B, NORTH_START[1])
NORTH_F_RIGHT_END = (NORTH_START[0] - X - B, NORTH_END[1])
NORTH_F_LEFT_START = (NORTH_START[0] - X, NORTH_START[1])
NORTH_F_LEFT_END = (NORTH_START[0] - X, NORTH_END[1])

NORTH_B_RIGHT_START = (NORTH_START[0] + X + B, NORTH_START[1])
NORTH_B_RIGHT_END = (NORTH_START[0] + X + B, NORTH_END[1])
NORTH_B_LEFT_START = (NORTH_START[0] + X, NORTH_START[1])
NORTH_B_LEFT_END = (NORTH_START[0] + X, NORTH_END[1])

# South
SOUTH_START = (0, L)
SOUTH_END = (0, A)
SOUTH_F_RIGHT_START = (SOUTH_START[0] + X + B, SOUTH_START[1])
SOUTH_F_RIGHT_END = (SOUTH_START[0] + X + B, SOUTH_END[1])
SOUTH_F_LEFT_START = (SOUTH_START[0] + X, SOUTH_START[1])
SOUTH_F_LEFT_END = (SOUTH_START[0] + X, SOUTH_END[1])

SOUTH_B_RIGHT_START = (SOUTH_START[0] - X - B, SOUTH_START[1])
SOUTH_B_RIGHT_END = (SOUTH_START[0] - X - B, SOUTH_END[1])
SOUTH_B_LEFT_START = (SOUTH_START[0] - X, SOUTH_START[1])
SOUTH_B_LEFT_END = (SOUTH_START[0] - X, SOUTH_END[1])

# West
WEST_START = (-L, 0)
WEST_END = (-A, 0)
WEST_F_RIGHT_START = (WEST_START[0], WEST_START[1] + X + B)
WEST_F_RIGHT_END = (WEST_END[0], WEST_END[1] + X + B)
WEST_F_LEFT_START = (WEST_START[0], WEST_START[1] + X)
WEST_F_LEFT_END = (WEST_END[0], WEST_END[1] + X)

WEST_B_RIGHT_START = (WEST_START[0], WEST_START[1] - X - B)
WEST_B_RIGHT_END = (WEST_END[0], WEST_END[1] - X - B)
WEST_B_LEFT_START = (WEST_START[0], WEST_START[1] - X)
WEST_B_LEFT_END = (WEST_END[0], WEST_END[1] - X)

# East
EAST_START = (L, 0)
EAST_END = (A, 0)
EAST_F_RIGHT_START = (EAST_START[0], EAST_START[1] - X - B)
EAST_F_RIGHT_END = (EAST_END[0], EAST_END[1] - X - B)
EAST_F_LEFT_START = (EAST_START[0], EAST_START[1] - X)
EAST_F_LEFT_END = (EAST_END[0], EAST_END[1] - X)

EAST_B_RIGHT_START = (EAST_START[0], EAST_START[1] + X + B)
EAST_B_RIGHT_END = (EAST_END[0], EAST_END[1] + X + B)
EAST_B_LEFT_START = (EAST_START[0], EAST_START[1] + X)
EAST_B_LEFT_END = (EAST_END[0], EAST_END[1] + X)

NORTH_F_RIGHT = sim.create_road(NORTH_F_RIGHT_START, NORTH_F_RIGHT_END)
NORTH_F_LEFT = sim.create_road(NORTH_F_LEFT_START, NORTH_F_LEFT_END)
SOUTH_F_RIGHT = sim.create_road(SOUTH_F_RIGHT_START, SOUTH_F_RIGHT_END)
SOUTH_F_LEFT = sim.create_road(SOUTH_F_LEFT_START, SOUTH_F_LEFT_END)
WEST_F_RIGHT = sim.create_road(WEST_F_RIGHT_START, WEST_F_RIGHT_END)
WEST_F_LEFT = sim.create_road(WEST_F_LEFT_START, WEST_F_LEFT_END)
EAST_F_RIGHT = sim.create_road(EAST_F_RIGHT_START, EAST_F_RIGHT_END)
EAST_F_LEFT = sim.create_road(EAST_F_LEFT_START, EAST_F_LEFT_END)

NORTH_B_RIGHT = sim.create_road(NORTH_B_RIGHT_END, NORTH_B_RIGHT_START)
NORTH_B_LEFT = sim.create_road(NORTH_B_LEFT_END, NORTH_B_LEFT_START)
SOUTH_B_RIGHT = sim.create_road(SOUTH_B_RIGHT_END, SOUTH_B_RIGHT_START)
SOUTH_B_LEFT = sim.create_road(SOUTH_B_LEFT_END, SOUTH_B_LEFT_START)
WEST_B_RIGHT = sim.create_road(WEST_B_RIGHT_END, WEST_B_RIGHT_START)
WEST_B_LEFT = sim.create_road(WEST_B_LEFT_END, WEST_B_LEFT_START)
EAST_B_RIGHT = sim.create_road(EAST_B_RIGHT_END, EAST_B_RIGHT_START)
EAST_B_LEFT = sim.create_road(EAST_B_LEFT_END, EAST_B_LEFT_START)

# Connections
NORTH_EAST = sim.create_road(
    *curve_points(NORTH_F_LEFT_END, EAST_B_LEFT_END, (NORTH_F_LEFT_END[0],
                                                      EAST_B_LEFT_END[1])))
NORTH_SOUTH_RIGHT = sim.create_road(NORTH_F_RIGHT_END, SOUTH_B_RIGHT_END)
NORTH_WEST = sim.create_road(
    *curve_points(NORTH_F_RIGHT_END, WEST_B_RIGHT_END, (NORTH_F_RIGHT_END[0],
                                                        WEST_B_RIGHT_END[1])))

SOUTH_EAST = sim.create_road(
    *curve_points(SOUTH_F_RIGHT_END, EAST_B_RIGHT_END, (SOUTH_F_RIGHT_END[0],
                                                        EAST_B_RIGHT_END[1])))
SOUTH_NORTH_RIGHT = sim.create_road(SOUTH_F_RIGHT_END, NORTH_B_RIGHT_END)
SOUTH_WEST = sim.create_road(
    *curve_points(SOUTH_F_LEFT_END, WEST_B_LEFT_END, (SOUTH_F_LEFT_END[0],
                                                      WEST_B_LEFT_END[1])))

WEST_SOUTH = sim.create_road(
    *curve_points(WEST_F_RIGHT_END, SOUTH_B_RIGHT_END, (SOUTH_B_RIGHT_END[0],
                                                        WEST_F_RIGHT_END[1])))
WEST_EAST_RIGHT = sim.create_road(WEST_F_RIGHT_END, EAST_B_RIGHT_END)
WEST_NORTH = sim.create_road(
    *curve_points(WEST_F_LEFT_END, NORTH_B_LEFT_END, (NORTH_B_LEFT_END[0],
                                                      WEST_F_LEFT_END[1])))

EAST_SOUTH = sim.create_road(
    *curve_points(EAST_F_LEFT_END, SOUTH_B_LEFT_END, (SOUTH_B_LEFT_END[0],
                                                      EAST_F_LEFT_END[1])))
EAST_WEST_RIGHT = sim.create_road(EAST_F_RIGHT_END, WEST_B_RIGHT_END)
EAST_NORTH = sim.create_road(
    *curve_points(EAST_F_RIGHT_END, NORTH_B_RIGHT_END, (NORTH_B_RIGHT_END[0],
                                                        EAST_F_RIGHT_END[1])))

sim.create_traffic_signals_group([
    TrafficSignal(NORTH_F_RIGHT),
    TrafficSignal(SOUTH_F_RIGHT)
], [
    TrafficSignal(NORTH_F_LEFT),
    TrafficSignal(SOUTH_F_LEFT)
], [
    TrafficSignal(WEST_F_RIGHT),
    TrafficSignal(EAST_F_RIGHT)
], [
    TrafficSignal(WEST_F_LEFT),
    TrafficSignal(EAST_F_LEFT)
], timers=[20, 60, 20, 60])

sim.create_gen({
    'vehicle_rate':
    15,
    'vehicles': [
        [2, {
            'path': [NORTH_F_LEFT, NORTH_EAST, EAST_B_LEFT],
        }],
        [1, {
            'path': [NORTH_F_RIGHT, NORTH_WEST, WEST_B_RIGHT],
        }],
        [1, {
            'path': [NORTH_F_RIGHT, NORTH_SOUTH_RIGHT, SOUTH_B_RIGHT],
        }],
        [1, {
            'path': [SOUTH_F_RIGHT, SOUTH_EAST, EAST_B_RIGHT],
        }],
        [2, {
            'path': [SOUTH_F_LEFT, SOUTH_WEST, WEST_B_LEFT],
        }],
        [1, {
            'path': [SOUTH_F_RIGHT, SOUTH_NORTH_RIGHT, NORTH_B_RIGHT],
        }],
        [1, {
            'path': [WEST_F_RIGHT, WEST_EAST_RIGHT, EAST_B_RIGHT],
        }],
        [1, {
            'path': [WEST_F_RIGHT, WEST_SOUTH, SOUTH_B_RIGHT],
        }],
        [2, {
            'path': [WEST_F_LEFT, WEST_NORTH, NORTH_B_LEFT],
        }],
        [1, {
            'path': [EAST_F_RIGHT, EAST_WEST_RIGHT, WEST_B_RIGHT],
        }],
        [2, {
            'path': [EAST_F_LEFT, EAST_SOUTH, SOUTH_B_LEFT],
        }],
        [1, {
            'path': [EAST_F_RIGHT, EAST_NORTH, NORTH_B_RIGHT],
        }],
    ]
})

# Start simulation
win = Window(sim)
win.run(30)
