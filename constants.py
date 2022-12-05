import numpy as np
import pygame

default_inputs = {
    pygame.K_KP8: np.array([0, -1]),
    pygame.K_KP4: np.array([-1, 0]),
    pygame.K_KP2: np.array([0, 1]),
    pygame.K_KP6: np.array([1, 0]),
    pygame.K_KP9: np.array([1, -1]),
    pygame.K_KP3: np.array([1, 1]),
    pygame.K_KP1: np.array([-1, 1]),
    pygame.K_KP7: np.array([-1, -1]),
    pygame.K_KP5: np.array([0, 0]),
}
"""The base inputs for the player stored in a dictionary."""

window_width = 1280
window_height = 800
window_size = (window_width, window_height)

tile_width = 32
tile_height = tile_width

DEFAULT_SIZE = (32, 32)
