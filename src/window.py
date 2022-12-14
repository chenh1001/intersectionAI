"""Window manager."""

from typing import Iterable, Tuple
import pygame
from pygame import gfxdraw
from math import sqrt
import numpy as np

from configurable_object import ConfigurableObject
from simulation import Simulation
from vehicle import Vehicle
from road import Point


class Window(ConfigurableObject):
    """Window class."""

    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 800
    BG_COLOR = (250, 250, 250)

    def __init__(self, sim: Simulation, config):
        super().__init__(config)

        # Simulation to draw
        self.sim: Simulation = sim

    def set_default_config(self):
        """Set default configuration."""

        self.fps = 60
        self.zoom = 2
        self.offset = (0, 0)

        self.mouse_last = (0, 0)
        self.mouse_down = False

    def init_window(self):
        # Create a pygame window
        self.screen = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.flip()

        # Fixed fps
        self.clock = pygame.time.Clock()

        # To draw text
        pygame.font.init()

    def update(self, with_draw=True):
        # Update window
        pygame.display.update()
        self.clock.tick(self.fps)
        if with_draw:
            self.draw()
            
    def convert(self, x, y=None):
        """Converts simulation coordinates to screen coordinates"""
        if isinstance(x, list):
            return [self.convert(e[0], e[1]) for e in x]
        if isinstance(x, tuple):
            return self.convert(*x)
        return (int(self.WINDOW_WIDTH / 2 + (x + self.offset[0]) * self.zoom),
                int(self.WINDOW_HEIGHT / 2 + (y + self.offset[1]) * self.zoom))

    def polygon(self, vertices, color, filled=True):
        converted_vertices = self.convert(vertices)
        gfxdraw.aapolygon(self.screen, converted_vertices, color)
        if filled:
            gfxdraw.filled_polygon(self.screen, converted_vertices, color)

    def rotated_box(self,
                    pos,
                    size,
                    angle=None,
                    cos=None,
                    sin=None,
                    centered=True,
                    color=(255, 0, 0),
                    filled=True):
        """Draws a rectangle center at *pos* with size *size* rotated anti-clockwise by *angle*."""
        x, y = pos
        l, h = size

        if angle:
            cos, sin = np.cos(angle), np.sin(angle)

        vertex = lambda e1, e2: (x + (e1 * l * cos + e2 * h * sin) / 2, y +
                                 (e1 * l * sin - e2 * h * cos) / 2)

        if centered:
            vertices = [
                vertex(*e) for e in [(-1, -1), (-1, 1), (1, 1), (1, -1)]
            ]
        else:
            vertices = [vertex(*e) for e in [(0, -1), (0, 1), (2, 1), (2, -1)]]

        self.polygon(vertices, color, filled=filled)

    def background(self, r, g, b):
        """Fills screen with one color."""

        self.screen.fill((r, g, b))

    def _draw_vehicle(self, vehicle: Vehicle):
        point, cos, sin = vehicle.get_position()
        self.rotated_box((point.x, point.y), (vehicle.length, vehicle.width),
                         cos=cos,
                         sin=sin,
                         centered=True,
                         color=(0, 0, 255))

    def draw_vehicles(self):
        for road in self.sim.roads:
            # Draw vehicles
            for vehicle in road.vehicles:
                self._draw_vehicle(vehicle)

    def _calc_line_points_by_width(self, point1: Point, point2: Point,
                                   width) -> Tuple[Point, Point]:

        if (point2.x - point1.x == 0):
            inverted_m = 0
        else:
            m = (point2.y - point1.y) / (point2.x - point1.x)
            if (m == 0):
                inverted_m = 999999999999
            else:
                inverted_m = -1 / m

        b0 = point1.y - inverted_m * point1.x

        a = inverted_m**2 + 1
        b = 2 * (inverted_m * (b0 - point1.y)) - 2 * point1.x
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
                   points: Iterable[Point],
                   color=(180, 180, 220),
                   filled=True):
        last_points = ()

        for i, point in enumerate(points):
            if i + 1 >= len(points):
                break

            next_point = points[i + 1]
            left_point, right_point = self._calc_line_points_by_width(
                point, next_point, width)

            # fill connections with last points if exists
            if last_points:
                last_point1, last_point2 = last_points
                self.polygon(
                    [right_point, last_point1, last_point2, left_point],
                    color,
                    filled=filled)
                self.polygon(
                    [right_point, last_point2, last_point1, left_point],
                    color,
                    filled=filled)

            next_left_point, next_right_point = self._calc_line_points_by_width(
                next_point, point, width)
            last_points = (next_left_point, next_right_point)
            self.polygon(
                [left_point, next_left_point, next_right_point, right_point],
                color,
                filled=filled)

    def draw_roads(self):
        """Draw all roads."""

        for road in self.sim.roads:
            self._draw_road(road.WIDTH, road.points)

    def draw_signals(self):
        """Draw all roads."""

        for signal in self.sim.traffic_signals_manager.signals:
            point, cos, sin = signal.road.get_position(
                signal.road.length - signal.x, signal.road)
            color = (0, 255, 0) if signal.is_active else (255, 0, 0)
            self.rotated_box((point.x, point.y), (10, signal.road.WIDTH * 2),
                             cos=cos,
                             sin=sin,
                             centered=True,
                             color=color)

    def draw(self):
        # Fill background
        self.background(*self.BG_COLOR)

        self.draw_roads()
        self.draw_signals()
        self.draw_vehicles()
