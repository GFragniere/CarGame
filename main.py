import numpy as np
import os
import pygame
import constants

from game import Game
from player import PlayerState

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
        self.game.new_player(1, "Didier", np.array([1, 3]))

    def process_input(self):

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
                        if not self.game.player_list[0].collision_speed_check(
                            self.game.game_map, constants.default_inputs.get(event.key)
                        ):
                            self.game.player_list[
                                0
                            ].speed += constants.default_inputs.get(event.key)
                            self.move_players()
                            break

    def render(self):
        self.window.fill((0, 0, 0))
        self.game.game_map.draw(self.window)
        self.game.player_list[0].draw(self.window)
        if self.game.player_list[0].collision_speed_check(
            self.game.game_map, np.array([0, 0])
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
            self.process_input()
            if not self.game.player_list[0].movement_validity():
                continue
            self.render()

    def move_players(self):
        if self.game.player_list[0].path_checking(self.game.game_map) == 1:
            self.game.player_list[0].plays()
        else:
            self.running = False
            print("Game ending, processing results...")


game = MyGame()
game.run()
pygame.quit()
