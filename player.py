import math
from enum import Enum
from game_map import GameMap
from game_map import TileState
import numpy as np
import pygame
import os
import constants as constants

os.chdir(os.path.dirname(os.path.abspath(__file__)))


class PlayerState(Enum):
    """Defines in which state the player currently is.

    Arguments
    ---------
    1: CAN_PLAY
        if in this state, the player can act normally.
    2: IS_OUT
        if in this state, the player has lost and cannot move until the end.
    3: HAS_WON
        if in this state, the player will be declared (one of the) winner(s) at the end of the turn.
    """

    CAN_PLAY = 1
    IS_OUT = 2
    HAS_WON = 3


class Player:
    """A class for the players in the game.

    Arguments
    ---------
    number: int
        used by the game to differentiate players to know which one should play.
    name: str
        chosen by the players at the beginning of the game to allow them to recognize themselves.
    position: np.array([,])
        used by the game to know where the player is on the grid.
    speed: np.array([,])
        used by the game to make the player move.


    Methods
    -------
    move()
        Used to make the player go to his next tile, based on his current speed and position.

    path_checking(game_map)
        used to know if the player can go from his current position to his new one, without colliding with a player or
        going on/over a tile that can't be run on.

    is_out()
        used to put the player in the "IS_OUT" state to return the type more easily.

    state_check()
        used to know if the player can play, is out or has won.

    get_walk_coordinates()
        used to determine which tiles the player is going to go over on his next move.

    transform_to_tuples_positions(array)
        used to transform an array containing arrays of coordinates to a tuple of tuples of indexes.

    collision_speed_check(game_map, speed = None)
        used to know if the player can make a specific move or not (the speed being the desired change in the player's
        speed) without being automatically being out of the game.

    movement_validity()
        used to know if the player has made a valid move in his turn, in order not to skip his turn completely.

    draw(window, tile_size)
        A method used to draw the player's car image, rotating according to his direction, as well as the tile
        he would land on in his next move if he keeps the same speed.


    """

    def __init__(
        self,
        number: int,
        position: np.ndarray,
        speed: np.ndarray,
        name: str,
        inputs: dict = constants.default_inputs,
        texture=pygame.image.load("image/red_car.png"),
    ):
        """
        Parameters
        ----------
        number:  int
            used to differentiate players numerically.
        position: np.array([,])
            used to determine the player's position at any given time.
        speed: np.array([,])
            used to determine the player's speed at any given time.
        name: str
            chosen by each player at the beginning of the game to recognize themselves.
        inputs: dict (optional)
            the dictionary of the player's movement possibilities, has a default value of constants.default_inputs.
        texture (optional)
            the texture of the player on the game, defaulting to a red car.
        """
        self.number = number
        self.position = position
        self.speed = speed
        self.name = name
        self.inputs = inputs
        self.texture = texture
        self.scaled_texture = None
        self.displayed_texture = None
        self.has_played = True

    def plays(self):
        """Uses the player speed and current location to make him go to a new tile."""
        self.position += self.speed
        self.has_played = True

    def path_checking(self, game_map: GameMap, velocity=None):
        """Used to check if the player can go from his current position to the next one when moving.

        We are calling on the method get_walk_coordinates to return the values of each tile the player will go through,
        to allow us to know how the path is, and if the player can make a move or not, as well as the method state_check
        to know if the player could even make a move in the first place.

        Parameters
        ----------
        game_map: GameMap
            the map on which the player is and is trying to move on.

        :returns: A number, based on the state of the path:
         1 if the path is clear;
          2 if the path will lead to a crash;
         3 if the path will lead to a win.
        """
        if velocity is None:
            velocity = self.speed.copy()
        if self.state_check() == PlayerState.IS_OUT:
            path = 2
            return path
        path = 1
        if np.any(
            np.greater(
                (velocity + self.position),
                np.array([game_map.width - 1, game_map.height - 1]),
            )
        ) or np.any(np.less((self.position + velocity), np.array([0, 0]))):
            path = 2
            return path
        path_tile = game_map.get_tile_list_type(
            self.get_walk_coordinates(velocity), 2**self.number
        )
        if sum(path_tile) > 0:
            for elem in path_tile:
                if elem == TileState.WIN.value:
                    path = 3
                elif not elem == 0:
                    path = 2
                    break
        return path

    def is_out(self):
        """Used to put the player in the "IS_OUT" state to return the type more easily."""
        self.position = np.array([-1, -1])
        self.speed = np.array([0, 0])

    def state_check(self):
        """Checks a player's state to know if he can play, is out or has won.

        Parameters
        ----------
        None.

        :return:  CAN_PLAY if the player can play, IS_OUT if the player is out of the game,
        HAS_WON if the player has won.
        """
        if np.array_equal(self.position, np.array([-1, -1])):
            return PlayerState.IS_OUT
        if np.any(self.position < 0):
            self.is_out()
            return PlayerState.IS_OUT
        if np.array_equal(self.position, np.array([1, 23])):
            return PlayerState.HAS_WON
        return PlayerState.CAN_PLAY

    def get_walk_coordinates(self, velocity=None):
        """Used to determine which tiles the player is going to go over on his next move.

        :return: a tuple of tuples of indexes with the coordinates on the map of the tiles that will be walked on.
        """
        if velocity is None:
            velocity = self.speed.copy()
        max_len = np.absolute(velocity).max()
        if max_len == 0:
            return (self.position[0],), (self.position[1],)
        return self.transform_to_tuples_positions(
            np.array([(velocity / max_len * i).astype(int) for i in range(max_len + 1)])
        )

    def transform_to_tuples_positions(self, array: np.array):
        """Used to transform an array containing arrays of coordinates to a tuple of tuples of indexes.

        Parameters
        ----------
        array: np.array
            the array containing the coordinates array.

        :return: a tuple of tuples for coordinates.
        """
        for x in array:
            x += self.position
        return tuple([tuple(elem) for elem in array.T])

    def collision_speed_check(self, game_map: GameMap, acceleration: np.array):
        """Used to know if the player can make a specific move or not (the speed being the desired change
        in the player's speed) without being automatically being out of the game.

        Parameters
        ----------
        game_map: GameMap
            the map on which the player is evolving.
        speed: np.array([,])
            the speed modification the player desires to make

        :return: True if the movement will lead to lose, False if the path is safe.
        """
        x = int(self.speed[0] + acceleration[0])
        y = int(self.speed[1] + acceleration[1])
        x_interval = round((x**2 + abs(x)) / 2)
        y_interval = round((y**2 + abs(y)) / 2)
        path1 = self.path_checking(
            game_map, np.array([np.sign(x) * x_interval, np.sign(y) * y_interval])
        )
        path2 = self.path_checking(game_map, np.array([x, y]))
        if self.position[0] + x_interval < 0 or self.position[1] + y_interval < 0:
            return True
        if path1 == 2 or path2 == 2:
            return True
        return False

    def movement_validity(self):
        """Used to know if the player has made a valid move in his turn, in order not to skip his turn completely.

        :return: True if the player has made a valid move, False if not.
        """
        if self.has_played:
            return True
        else:
            return False

    def draw(self, window: pygame.display, tile_size: int, turn: int):
        """A method used to draw the player's car image, rotating according to his direction, as well as the tile
        he would land on in his next move if he keeps the same speed.

        Parameters
        ----------

        window: pygame.display
            the window on which the player's image and next move have to be drawn on

        tile_size: int
            the size of a tile in the current window size
        """
        if self.scaled_texture is None:
            self.scaled_texture = pygame.transform.scale(
                self.texture, (tile_size, tile_size)
            )
        if self.displayed_texture is None:
            self.displayed_texture = self.scaled_texture
        if self.speed[1] == 0:
            angle = 180 + (90 * np.sign(self.speed[0]))
        elif self.speed[1] > 0:
            angle = 180 + math.degrees(math.atan(self.speed[0] / self.speed[1]))
        else:
            angle = math.degrees(math.atan(self.speed[0] / self.speed[1]))
        self.displayed_texture = pygame.transform.rotate(self.scaled_texture, angle)
        pygame.draw.rect(
            window,
            (47, 9, 9),
            (
                (self.speed[0] + self.position[0]) * tile_size,
                (self.speed[1] + self.position[1]) * tile_size,
                tile_size,
                tile_size,
            ),
        )
        window.blit(self.displayed_texture, (self.position * tile_size))
        if turn == self.number:
            self.draw_arrow(window, tile_size)

    def draw_arrow(self, window, tile_size: int):
        player_pos = self.position * tile_size
        pygame.draw.rect(
            window, (200, 200, 200), (player_pos[0] + 12, player_pos[1] - 32, 8, 16)
        )

    def can_play(self):
        self.has_played = False
