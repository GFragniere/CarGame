import numpy as np
import os
import pygame
import constants

from game import Game
from game_map import GameMap
from player import Player
from player import PlayerState

os.environ["SDL_VIDEO_CENTERED"] = "1"


class MyGame:
    def __init__(self, map_number: int):
        pygame.init()
        self.window = pygame.display.set_mode(constants.window_size)
        pygame.display.set_caption("Car Game")
        pygame.display.set_icon(pygame.image.load("image/car_game_icon.png"))
        self.clock = pygame.time.Clock()
        self.running = True
        self.position_grid = np.genfromtxt("positions/position"+str(map_number)+".csv", dtype=int, delimiter=",")
        self.game = Game(map_number)
        self.collision_help = True
        self.turn_count = 0

    def process_input(self, player: Player):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    break
                elif event.key == pygame.K_h:
                    self.collision_help = not self.collision_help
                else:
                    if constants.default_inputs.get(event.key) is not None:
                        if not player.collision_speed_check(
                            self.game.game_map, constants.default_inputs.get(event.key), self.collision_help
                        ):
                            player.speed += constants.default_inputs.get(event.key)
                            self.move_player(player)
                            break

    def render(self):
        self.window.fill((0, 0, 0))
        self.game.draw(self.window, self.turn_count)
        if self.collision_help:
            pygame.draw.rect(self.window, (200, 200, 200), (constants.window_width - self.game.game_map.width, 0, 30, 30))
        for player in self.game.player_list:
            if (
                player.collision_speed_check(self.game.game_map, np.array([0, 0]), self.collision_help)
                and player.state_check(self.game.game_map) != PlayerState.IS_OUT
            ):
                pygame.draw.polygon(
                    self.window, (200, 50, 50), [(80, 60), (40, 130), (120, 130)]
                )
                pygame.draw.polygon(
                    self.window, (255, 255, 255), [(80, 70), (48, 125), (112, 125)]
                )
                pygame.draw.rect(self.window, (0, 0, 0), (77, 85, 6, 20))
                pygame.draw.circle(self.window, (0, 0, 0), (80, 115), 4)
        pygame.display.update()

    def run(self):
        while self.running:
            for player in self.game.player_list:
                if player.number == self.turn_count:
                    if player.state_check(self.game.game_map) == PlayerState.IS_OUT:
                        player.has_played = True
                    else:
                        self.game.update(player)
                        self.render()
                        self.process_input(player)
                        if self.end_of_player(player, self.game.game_map):
                            continue
                        if not player.movement_validity():
                            continue
                    self.turn_count += 1
                    self.turn_count %= len(self.game.player_list)
                    self.game.player_state_reset()
                    self.end_of_game()

    def move_player(self, player: Player):
        if player.path_checking(self.game.game_map) == 1:
            self.game.game_map.modify_tile_list_state(
                player.get_walk_coordinates(), 2**player.number
            )
            player.plays()
        elif player.path_checking(self.game.game_map) == 2:
            player.is_out()
            print("Game ending, processing results...")
        elif player.path_checking(self.game.game_map) == 3:
            print("Congratulations for reaching the end,", player.name, "!")
            player.plays()

    def end_of_game(self):
        players_out = 0
        players_won = 0
        for player in self.game.player_list:
            if player.state_check(self.game.game_map) == PlayerState.IS_OUT:
                players_out += 1
            elif player.state_check(self.game.game_map) == PlayerState.HAS_WON:
                players_won += 1
        if players_out == len(self.game.player_list):
            self.running = False
            print("Everyone is out, game is over!")
        if players_won > 0:
            self.running = False

    def end_of_player(self, player: Player, game_map: GameMap):
        """Used to determine if the player should be taken out of the game due to impossibility to save himself.

        Parameters
        ----------

        game_map: GameMap
            the map on which the player is evolving.

        :return:
        True if the player should be taken out of the game, False if he can still play.
        """
        outcomes = []
        for i, elem in constants.default_inputs.items():
            outcomes.append(player.collision_speed_check(game_map, elem, self.collision_help))
        if np.all(outcomes):
            player.is_out()
            return True
        return False


can_start = False

while not can_start:
    try:
        player_count = int(input("Please chose how much player will play (max 8): "))
        if not 0 < player_count < 9:
            print("Invalid number. Please try again")
        else:
            can_start = True
        map_number = int(input("On which map do you want to play? (Maps go from 1 to 5) "))
        if not 0 < map_number < 6:
            print("Not a valid map number, try again!")
            can_start = False
    except ValueError:
        print("That's not a number, try again!")
        can_start = False


name_list = []
for a in range(player_count):
    name_list.append(input("Player #" + str(a + 1) + ", choose your name: "))

game = MyGame(map_number)

for a in range(player_count):
    if a == 0:
        game.game.new_player(a, name_list[a], game.position_grid[player_count - 1])
    else:
        game.game.new_player(a, name_list[a], game.position_grid[a - 1])


game.run()
pygame.quit()
