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

road = sim.create_road(
    *curve_points((100, 100), (1200, 110), (600, 1400), resolution=30))

sim.create_traffic_signals_group([TrafficSignal(road, {"x": 1000})],
                                 [TrafficSignal(road, {"x": 400})],
                                 cycles=[(True, False), (False, True)])

sim.create_gen({
    'vehicle_rate':
    10,
    'vehicles': [
        [1, {
            'path': [road],
        }],
        # [1, {
        #     'path': reut_roads,
        # }]
    ]
})
# Start simulation
win = Window(sim)
win.run(10)
