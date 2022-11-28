from CarGame.game_map import GameMap
from CarGame.player import Player
from CarGame.player import PlayerState
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
    new_player(player_number: int, player_position: np.array([0, 0]), player_speed: np.array = np.array([0, 0]),
        player_state: PlayerState = 1)
        Used to create new players.
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
        player_name: str,
        player_position: np.array = np.array([0, 0]),
        player_speed: np.array = np.array([0, 0]),
    ):
        """Used to create new players and adds them to the player_list.
        If the user doesn't specify a speed or position, the default values of [0, 0] will be applied. As of the state,
        the default value is 1, corresponding to the "CAN_PLAY" state.

        Parameters
        ----------
        player_number: int
            used to differentiate the players with a number.

        player_name: str
            the player's name.

        player_position: np.array([,])
            used to determine the position of the player in the game grid.

        player_speed: np.array([,])
            used to determine the speed (and direction) of the player at any time.

        """
        new_player = Player(player_number, player_position, player_speed.copy(), player_name)
        self.player_list.append(new_player)

    def move_players(self, players_out: int, player_won: list):
        for player in self.player_list:
            self.update(player)
            if player.state_check() == PlayerState.CAN_PLAY:
                player.player_move(self.game_map, 2**(player.number-1))
            elif player.state_check() == PlayerState.IS_OUT:
                print("Sorry ", player.name, ", but you're out!")
                players_out += 1
            else:
                player_won.append(player)
        return players_out

    def update(self, player: Player):
        self.game_map.remove_previous_move(2**(player.number-1))
