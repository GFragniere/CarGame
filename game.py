from game_map import GameMap
from player import Player
from player import PlayerState
import numpy as np


class Game:
    """
    A class used to handle the players and the tiles of the game.

    Attributes
    ----------
    player_list: list
        a list containing all players in the game.
    game_map: GameMap
        a map of the game containing all the tiles.

    Methods
    -------
    new_player(player_number, name, player_position, player_speed)
        Used to create new players.

    move_players(player, action)
        Defines what the input will have as an effect on the player, depending on his number and if the wanted action
        is in the dictionary of said player.

    update(self, player: Player):
        used to remove the previous move of the player.
    """

    def __init__(self):
        """
        Parameters
        ----------
        None.
        """
        self.player_list = []
        self.game_map = GameMap(40, 25)
        self.game_map.base_map()

    def new_player(
        self,
        player_number: int,
        name: str,
        player_position: np.array = np.array([0, 0]),
        player_speed: np.array = np.array([0, 0]),
    ):
        """Used to create new players and adds them to the player_list.
        If the user doesn't specify a speed or position, the default values of [0, 0] will be applied.

        Parameters
        ----------
        player_number: int
            used to differentiate the players with a number.

        name: str
            the player's name.

        player_position: np.array([,])
            used to determine the position of the player in the game grid.

        player_speed: np.array([,])
            used to determine the speed (and direction) of the player at any time.

        """
        new_player = Player(player_number, player_position, player_speed.copy(), name)
        self.player_list.append(new_player)

    """def move_players(self, players_out: int, player_won: list):
        for player in self.player_list:
            self.update(player)
            if player.state_check() == PlayerState.CAN_PLAY:
                player.player_move(self.game_map, 2 ** (player.number - 1))
            elif player.state_check() == PlayerState.IS_OUT:
                print("Sorry ", player.name, ", but you're out!")
                players_out += 1
            else:
                player_won.append(player)
        return players_out"""

    def update(self, player: Player):
        """Used to remove the previous move of the player."""
        self.game_map.remove_previous_move(2 ** (player.number - 1))
