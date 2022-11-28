from enum import Enum
from CarGame.game_map import GameMap
from CarGame.game_map import TileState
import numpy as np
import CarGame.constants as constants


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
    set_state(new_state)
        used to set the state of the player to a new one, when he wins or is out of the game.
    get_state()
        used by the game to know if the player should move or not, or if he won.
    path_checking()
        used to know if the player can go from his current position to his new one, without colliding with a player or
        going on/over a tile that can't be run on.
    """

    def __init__(
        self,
        number: int,
        position: np.ndarray,
        speed: np.ndarray,
        name: str,
        inputs: dict = constants.default_inputs,
    ):
        """
        Parameters
        ----------
        number:  int
            used to differentiate players numerically.
        name: str
            chosen by each player at the beginning of the game to recognize themselves.
        position: np.array([,])
            used to determine the player's position at any given time.
        speed: np.array([,])
            used to determine the player's speed at any given time.
        """
        self.number = number
        self.position = position
        self.speed = speed
        self.name = name
        self.inputs = inputs

    def move(self):
        """Uses the player speed and current location to make him go to a new tile."""
        self.position += self.speed

    def path_checking(self, game_map: GameMap, player_value: int):
        """Used to check if the player can go from his current position to the next one when moving.

        Depending on the values of the player's speed vector, we must adapt for which slope will be taken into account,
        either being a y/x slope or x/y slope.
        We also use the method from CarGame.operation: pathing to figure out which tiles are in the trajectory of the
        player.

        Parameters
        ----------
        game_map: GameMap
            the map on which the player is and is trying to move on.

        :returns: True if the path is clear,
        False if the player cannot go on the desired tile
        """
        path = 1
        if np.any(
            np.greater(
                (self.speed + self.position),
                np.array([39, 24]),
            )
        ):
            path = 2
            return path
        path_tile = game_map.get_tile_list_type(self.get_walk_coordinates(), player_value)
        if sum(path_tile) > 0:
            for elem in path_tile:
                if elem == TileState.WIN.value:
                    path = 3
                    break
                elif not elem == 0:
                    path = 2
                    break
        return path

    def get_position(self):
        """Used to return the player's position."""
        return self.position[0], self.position[1]

    def player_action(self, action: str):
        """Defines what the input will have as an effect on the player, depending on his number and if the wanted action
        is in the dictionary of said player.

        Parameters
        ----------
        action: str
            the input that will be checked within the player's assigned dictionary, to know if an action is available
            or not."""
        for v in action:
            if self.inputs.get(v) is not None:
                print(f"Set player {self.number} new speed.")
                self.speed += self.inputs.get(v)
                break

    def is_out(self):
        self.position = np.array([-1, -1])
        self.speed = np.array([0, 0])

    def state_check(self):
        """Checks all the players' state to know if the game should stop or not.

        Parameters
        ----------
        None.

        Returns
        -------
        1 if the game should continue.
        2 if all players are out.
        3 if one or more player has won."""
        if np.array_equal(self.position, np.array([-1, -1])):
            return PlayerState.IS_OUT
        if np.any(self.position < 0):
            self.is_out()
            return PlayerState.IS_OUT
        if np.array_equal(self.position, np.array([1, 23])):
            return PlayerState.HAS_WON
        return PlayerState.CAN_PLAY

    def player_move(self, game_map: GameMap, player_value: int):
        print(
            f"Player {self.number} :",
            self.name,
            ", you are on coordinates ",
            self.position,
            ", and your speed is ",
            self.speed,
            ".",
        )
        actions = input("Choose a desired input: ")
        self.player_action(actions)

        path_state = self.path_checking(game_map, player_value)
        if path_state == 1:
            game_map.modify_tile_list_state(self.get_walk_coordinates(), player_value)
            self.move()
        elif (
            path_state == 2
        ):
            self.is_out()
            print("Wow ", self.name, ", you blew it! Now you can watch from the bench!")
        elif path_state == 3:
            self.position = np.array([1, 23])

    def get_walk_coordinates(self):
        max_len = np.absolute(self.speed).max()
        if max_len == 0:
            return (self.position[0],), (self.position[1],)
        return self.transform_to_tuples_positions(
            np.array(
                [(self.speed / max_len * i).astype(int) for i in range(max_len + 1)]
            )
        )

    def transform_to_tuples_positions(self, array: np.array):
        for x in array:
            x += self.position
        return tuple([tuple(elem) for elem in array.T])
