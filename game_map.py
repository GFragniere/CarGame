import enum

import numpy as np

# from CarGame.player import Player
from enum import Flag


class TileState(Flag):
    PLAYER_1 = enum.auto()
    PLAYER_2 = enum.auto()
    PLAYER_3 = enum.auto()
    PLAYER_4 = enum.auto()
    PLAYER_5 = enum.auto()
    PLAYER_6 = enum.auto()
    PLAYER_7 = enum.auto()
    PLAYER_8 = enum.auto()
    WALL = enum.auto()
    WIN = enum.auto()


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

    get_tile_type(x, y)
        Used to return the type of tile at a specific location.

    modify_tile_state(x, y, state)
        used to modify a specific tile's state in the desired state.
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

    def get_tile_type(self, x: int, y: int):
        """
        Used to return the type of tile at a specific location.

        Parameters
        ----------
        x: int
            the x coordinate of the tile we want to know the type
        y:
            the y coordinate of the tile we want to know the type

        Returns
        -------
        The type of the tile (1 is empty, 2 has a player, 3 will "kill" the player, 4 makes the player win) for
        a set pair of coordinates.
        """
        return int(self.map[x, y])

    def get_tile_list_type(self, index: tuple, tile_value: int):
        return list(self.map[index] & ~tile_value)

    def modify_tile_state(self, x: int, y: int, state: int):
        """Used to modify a tile's state.

        Parameters
        ----------
        x: int
            the x coordinate of the tile that has to be modified.
        y: int
            the y coordinate of the tile that has to be modified.
        state: int
            the state that the tile has to be changed to.
        """
        self.map[x, y] = state

    def modify_tile_list_state(self, index: tuple, tile_value: int):
        self.map[index] |= tile_value

    def remove_previous_move(self, value: int):
        self.map &= ~value
