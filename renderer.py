import pygame
import pymunk.pygame_util
from constants import COLOR_BLACK

class Renderer:
    def __init__(self, window):
        self.window = window
        self.draw_options = pymunk.pygame_util.DrawOptions(window)
        # Flip y axis for debug draw if we want (0,0) at bottom, 
        # but Pygame standard is (0,0) at top. 
        # GRAVITY is (0, 980) so things fall down in Pygame space.

    def draw(self, space):
        self.window.fill(COLOR_BLACK)
        space.debug_draw(self.draw_options)
        pygame.display.update()
