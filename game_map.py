import numpy as np
import pygame
import constants

# from CarGame.player import Player
from enum import Flag, auto


class TileState(Flag):
    PLAYER_1 = auto()  # 1
    PLAYER_2 = auto()  # 2
    PLAYER_3 = auto()  # 4
    PLAYER_4 = auto()  # 8
    PLAYER_5 = auto()  # 16
    PLAYER_6 = auto()  # 32
    PLAYER_7 = auto()  # 64
    PLAYER_8 = auto()  # 128
    WALL = auto()  # 256
    WIN = auto()  # 512


class GameMap:
    """A class containing all the information about the game map and the tiles it contains, in order to determine if
    the player can go on/over some tiles.

    Attributes
    ---------
    width: int
        used to determine the width (x coordinates) of the game map.
    height: int
        used to determine the height (y coordinates) of the game map.
    map: np.array((width, height))
        a 2D array containing the types of all tiles for each set of coordinates, allowing the game to know if the
        player can go on/over specific tiles.

    Methods
    -------
    create_finish_line(finish_x: int, finish_y: int, start_finish_x: int, start_finish_y: int)
        Creates where all players must race to in order to win.

    create_kill_zone(kill_zone_x: int, kill_one_y: int, kill_zone_start_x: int, kill_zone_start_y: int)
        Allows to create zones in which the player cannot go on/over.

    base_map():
        Allows to create a pre-made map, with the kill zones and finish zone already established
        (must be a 40 x by 25 y map).

    get_tile_list_type(index, value)
        Used to return the map of the game without a set value.

    modify_tile_list_state(index, tile_value)
        Used to modify a tile list with a tuple-tuple of indexes to a set value.

    remove_previous_move(value)
        Used to remove the previous move of a player (each player will leave a "trace" of his movement from the last turn),
        this method is used to erase this trace.
    """

    def __init__(self, width: int, height: int):
        """
        Parameters
        ----------
        width: int
            used to determine the width (x coordinate) of the game map.
        height: int
            used to determine the height (xy coordinate) of the game map.
        """
        self.width = width
        self.height = height
        self.map = np.zeros((width, height), dtype=int)

    def create_finish_line(
        self, finish_x: int, finish_y: int, start_finish_x: int, start_finish_y: int
    ):
        """
        Creates where all players must race to in order to win.

        Parameters
        ----------
        finish_x: int
            used to determine the width of the finish zone.
        finish_y:
            used to determine the height of the finish zone.
        start_finish_x:
            used to determine where the finish zone starts in x coordinates.
        start_finish_y:
            used to determine where the finish zone starts in y coordinates.
        """
        for x in range(finish_x):
            for y in range(finish_y):
                self.map[start_finish_x + x, start_finish_y + y] |= TileState.WIN.value

    def create_kill_zone(
        self,
        kill_zone_x: int,
        kill_one_y: int,
        kill_zone_start_x: int,
        kill_zone_start_y: int,
    ):
        """
        Allows to create zones in which the player cannot go on/over.

        Parameters
        ----------
        kill_zone_x: int
            used to determine the width of the kill zone.
        kill_one_y:
            used to determine the height of the kill zone.
        kill_zone_start_x:
            used to determine where the kill zone starts in x coordinates.
        kill_zone_start_y:
            used to determine where the kill zone starts in y coordinates.
        """
        for x in range(kill_zone_x):
            for y in range(kill_one_y):
                self.map[
                    kill_zone_start_x + x, kill_zone_start_y + y
                ] |= TileState.WALL.value

    def base_map(self):
        """
        Allows to create a pre-made map, with the kill zones and finish zone already established
        (must be a 40 x by 25 y map).
        """
        if self.width == 40 and self.height == 25:
            self.create_kill_zone(12, 6, 28, 0)
            self.create_kill_zone(28, 4, 0, 10)
            self.create_kill_zone(6, 5, 0, 14)
            self.create_kill_zone(2, 5, 14, 14)
            self.create_kill_zone(2, 5, 26, 14)
            self.create_kill_zone(2, 6, 8, 19)
            self.create_kill_zone(2, 6, 20, 19)
            self.create_kill_zone(5, 4, 3, 21)
            self.create_finish_line(3, 4, 0, 21)

    def get_tile_list_type(self, index: tuple, tile_value: int):
        """Used to return a set of tiles stored in a tuple of tuples of indexes for a specific player with his
        number associated value (refer to the TileState Flag class for values).

        Parameters
        ----------
        index: tuple
            a tuple of tuples of indexes that we want to analise and get the value of.

        tile_value: int
            the value of the player which has to make a move.
        """
        return list(self.map[index] & ~tile_value)

    def modify_tile_list_state(self, index: tuple, tile_value: int):
        """Used to modify a tile list with a tuple-tuple of indexes to a set value.

        Parameters
        ----------
        index: tuple
            a tuple of tuples of coordinates we want the tiles' value to be changed to.

        tile_value: int
            the value we want to modify the tiles values to.
        """
        self.map[index] |= tile_value

    def remove_previous_move(self, value: int):
        """Used to remove the previous move of a player (each player will leave a "trace" of his movement from the last turn),
        this method is used to erase this trace.

        Parameters
        ----------

        value: int
            the value from which the map has to be removed of.
        """
        self.map &= ~value

    def draw(self, window: pygame.display, tile_size: int):
        for a in range(self.width):
            for b in range(self.height):
                if self.map[a, b] == TileState.WALL.value:
                    pygame.draw.rect(
                        window,
                        (139, 69, 19),
                        (
                            a * tile_size,
                            b * tile_size,
                            tile_size,
                            tile_size,
                        ),
                    )
                elif self.map[a, b] == TileState.WIN.value:
                    pygame.draw.rect(
                        window,
                        (255, 255, 255),
                        (
                            a * tile_size,
                            b * tile_size,
                            tile_size,
                            tile_size,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        window,
                        (55 + self.map[a, b], 55, 55),
                        (
                            a * tile_size,
                            b * tile_size,
                            tile_size,
                            tile_size,
                        ),
                    )

        for x in range(self.width):
            pygame.draw.line(
                window,
                (0, 0, 0),
                (x * tile_size, 0),
                (x * tile_size, constants.window_height),
            )

        for y in range(self.height):
            pygame.draw.line(
                window,
                (0, 0, 0),
                (0, y * tile_size),
                (constants.window_width, y * tile_size),
            )
