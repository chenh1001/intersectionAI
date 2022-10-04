"""Window manager."""

from typing import Iterable, Tuple
import pygame
from pygame import gfxdraw
from math import sqrt

from simulation import Simulation
from vehicle import Vehicle
from road import Road, Point


class Window:
    """Window class."""

    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900
    BG_COLOR = (250, 250, 250)

    def __init__(self, sim: Simulation, config={}):
        # Simulation to draw
        self.sim: Simulation = sim

        # Set default configurations
        self.set_default_config()

        # Update configurations
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        """Set default configuration."""

        self.fps = 20
        self.zoom = 5
        self.offset = (0, 0)

        self.mouse_last = (0, 0)
        self.mouse_down = False

    def run(self):
        """Shows a window visualizing the simulation and runs the loop function."""

        # Create a pygame window
        self.screen = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.flip()

        # Fixed fps
        clock = pygame.time.Clock()

        # To draw text
        pygame.font.init()

        # Draw loop
        running = True
        self.draw()
        while running:
            # Update simulation
            # self.sim.update()

            # Update window
            pygame.display.update()
            clock.tick(self.fps)

    def polygon(self, vertices, color, filled=True):
        gfxdraw.aapolygon(self.screen, vertices, color)
        if filled:
            gfxdraw.filled_polygon(self.screen, vertices, color)

    def background(self, r, g, b):
        """Fills screen with one color."""

        self.screen.fill((r, g, b))

    def _draw_vehicle(self, vehicle: Vehicle, road: Road):
        pass

    def draw_vehicles(self):
        for road in self.sim.roads:
            # Draw vehicles
            for vehicle in road.vehicles:
                self._draw_vehicle(vehicle, road)

    @staticmethod
    def _incline(point1, point2):
        return (point2.y - point1.y) / (point2.x - point1.x)

    def _calc_line_points_by_width(self, point1: Point, point2: Point,
                                   width) -> Tuple[Point, Point]:

        if (point2.x - point1.x == 0):
            inverted_m = 0
        else:
            m = self._incline(point1, point2)
            if (m == 0):
                inverted_m = 999999999999
            else:
                inverted_m = -1 / m

        b0 = point1.y - inverted_m * point1.x

        a = inverted_m**2 + 1
        b = 2 * (inverted_m * (b0 - point1.y)) -2 * point1.x
        c = point1.x**2 + (b0 - point1.y)**2 - width**2

        # calculate the discriminant
        d = (b**2) - (4 * a * c)

        # find two solutions
        x1 = (-b - sqrt(d)) / (2 * a)
        x2 = (-b + sqrt(d)) / (2 * a)

        y1 = x1 * inverted_m + b0
        y2 = x2 * inverted_m + b0

        return Point(x1, y1), Point(x2, y2)

    def _draw_road(self,
                   width,
                   *points: Iterable[Point],
                   color=(0, 0, 255),
                   filled=False):
        last_points = ()
        right_points = []
        left_points = []

        for i, point in enumerate(points):
            if i + 1 >= len(points):
                break
            # next_point = points[i + 1]
            # left_point, right_point = self._calc_line_points_by_width(
            #     point, next_point, width)
            # l_incline = self._incline(left_point, next_point)
            # r_incline = self._incline(right_point, next_point)
            # if l_incline > r_incline:
            #     right_points.append(right_point)
            #     left_points.append(left_point) 
            # else:
            #     right_points.append(left_point)
            #     left_points.append(right_point) 

            # left_point, right_point = self._calc_line_points_by_width(
            #     next_point, point, width)
            # l_incline = self._incline(left_point, point)
            # r_incline = self._incline(right_point, point)
            # if l_incline > r_incline:
            #     right_points.append(right_point)
            #     left_points.append(left_point) 
            # else:
            #     right_points.append(left_point)
            #     left_points.append(right_point) 

            next_point = points[i + 1]
            left_point, right_point = self._calc_line_points_by_width(
                point, next_point, width)
            
            # fill connections with last points if exists
            if last_points:
                last_point1, last_point2 = last_points
                self.polygon([right_point, last_point1, last_point2, left_point], color, filled=filled)
                self.polygon([right_point, last_point2, last_point1, left_point], color, filled=filled)

            next_left_point, next_right_point = self._calc_line_points_by_width(
                next_point, point, width)
            last_points = (next_left_point, next_right_point)
            self.polygon([left_point, next_left_point, next_right_point, right_point], color, filled=filled)
        # right_points.reverse()
        # polygon = left_points + right_points
        # self.polygon(polygon, color, filled=filled)


    def draw_roads(self):
        """Draw all roads."""

        for road in self.sim.roads:
            self._draw_road(road.WIDTH, *road.points)

    def draw(self):
        # Fill background
        self.background(*self.BG_COLOR)

        # self.draw_vehicles()
        self.draw_roads()
