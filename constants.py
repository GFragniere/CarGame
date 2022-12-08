import numpy as np
import pygame
from game_map import GameMap

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

base_map = GameMap(40, 25)
base_map.base_map()

default_positions = {
    0: np.array([1, 1]),
    1: np.array([1, 8]),
    2: np.array([1, 7]),
    3: np.array([1, 6]),
    4: np.array([1, 5]),
    5: np.array([1, 4]),
    6: np.array([1, 3]),
    7: np.array([1, 2]),
}
