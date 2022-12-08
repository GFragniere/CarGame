import numpy as np
import os
import pygame
import constants

from game import Game
from player import Player

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.environ["SDL_VIDEO_CENTERED"] = "1"


class MyGame:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode(constants.window_size)
        pygame.display.set_caption("Car Game")
        pygame.display.set_icon(pygame.image.load("image/car_game_icon.png"))
        self.clock = pygame.time.Clock()
        self.running = True
        self.game = Game()
        self.game.new_player(0, "temporary_name", np.array([1, 3]))
        self.game.new_player(1, "temporary_name", np.array([1, 4]))
        self.game.new_player(2, "temporary_name", np.array([1, 5]))
        self.game.new_player(3, "temporary_name", np.array([1, 6]))
        self.game.new_player(4, "temporary_name", np.array([1, 7]))
        self.game.new_player(5, "temporary_name", np.array([1, 8]))

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
                else:
                    if constants.default_inputs.get(event.key) is not None:
                        if not player.collision_speed_check(
                            self.game.game_map, constants.default_inputs.get(event.key)
                        ):
                            player.speed += constants.default_inputs.get(event.key)
                            self.move_player(player)
                            break

    def render(self):
        self.window.fill((0, 0, 0))
        self.game.draw(self.window, self.turn_count)
        for player in self.game.player_list:
            if player.collision_speed_check(self.game.game_map, np.array([0, 0])):
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
                    self.game.update(player)
                    self.process_input(player)
                    if not player.movement_validity():
                        continue
                    self.turn_count += 1
                    self.turn_count %= len(self.game.player_list)
                    self.render()
                    self.game.player_state_reset()


    def move_player(self, player: Player):
        if player.path_checking(self.game.game_map) == 1:
            self.game.game_map.modify_tile_list_state(
                player.get_walk_coordinates(), 2**player.number
            )
            player.plays()
        elif player.path_checking(self.game.game_map) == 2:
            player.is_out()
            self.running = False
            print("Game ending, processing results...")


game = MyGame()
game.run()
pygame.quit()
