import pygame
from pygame import gfxdraw

from configurable_object import ConfigurableObject
from window import Window


class simulationManager(ConfigurableObject):

    def __init__(self, sim, config=None) -> None:
        super().__init__(config)

        self.sim = sim

    def run(self, steps_per_update):
        """Shows a window visualizing the simulation and runs the loop function."""

        window = Window(self.sim, {})
        window.init_window()

        # Draw loop
        running = True
        while running:
            # Update simulation
            self.sim.run(steps_per_update)

            # Draw simulation
            window.update(with_draw=True)

            # Handle all events
            for event in pygame.event.get():
                # Quit program if window is closed
                if event.type == pygame.QUIT:
                    running = False
                # Handle mouse events
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # If mouse button down
                    if event.button == 1:
                        # Left click
                        x, y = pygame.mouse.get_pos()
                        x0, y0 = window.offset
                        window.mouse_last = (x - x0 * window.zoom,
                                           y - y0 * window.zoom)
                        window.mouse_down = True
                    if event.button == 4:
                        # Mouse wheel up
                        window.zoom *= (window.zoom**2 + window.zoom / 4 +
                                      1) / (window.zoom**2 + 1)
                    if event.button == 5:
                        # Mouse wheel down
                        window.zoom *= (window.zoom**2 + 1) / (window.zoom**2 +
                                                           window.zoom / 4 + 1)
                elif event.type == pygame.MOUSEMOTION:
                    # Drag content
                    if window.mouse_down:
                        x1, y1 = window.mouse_last
                        x2, y2 = pygame.mouse.get_pos()
                        window.offset = ((x2 - x1) / window.zoom,
                                       (y2 - y1) / window.zoom)
                elif event.type == pygame.MOUSEBUTTONUP:
                    window.mouse_down = False
