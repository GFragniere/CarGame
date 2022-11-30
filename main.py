import numpy as np
import os
import pygame
import constants

from CarGame.game import Game
from CarGame.player import PlayerState

os.chdir(os.path.dirname(os.path.abspath(__file__)))
os.environ["SDL_VIDEO_CENTERED"] = "1"
car_texture = pygame.image.load("image/red_car.png")
DEFAULT_SIZE_IMAGE = (24, 24)
new_image = pygame.transform.scale(car_texture, DEFAULT_SIZE_IMAGE)


class GameState:
    def __init__(self):
        self.x = 184
        self.y = 132

    def update(self, move_command_x, move_command_y):
        self.x += move_command_x
        self.y += move_command_y


class MyGame:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1280, 720))
        pygame.display.set_caption("Car Game")
        pygame.display.set_icon(pygame.image.load("image/car_game_icon.png"))
        self.rotated = pygame.transform.rotate(new_image, 0)
        self.clock = pygame.time.Clock()
        self.game_state = GameState()
        self.running = True
        self.move_command_x = 0
        self.move_command_y = 0
        self.move_inputs = {"w": (-24), "s": 24, "d": 24, "a": (-24)}
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
                elif event.key == pygame.K_KP5:
                    if not self.game.player_list[0].collision_speed_check(
                        self.game.game_map
                    ):
                        self.move_players()
                        break

                elif event.key == pygame.K_KP6:
                    if not self.game.player_list[0].collision_speed_check(
                        self.game.game_map, np.array([1, 0])
                    ):
                        self.move_command_x += self.move_inputs.get("d")
                        self.game.player_list[0].speed += constants.default_inputs.get(
                            "d"
                        )
                        self.move_players()
                        break

                elif event.key == pygame.K_KP4:
                    if not self.game.player_list[0].collision_speed_check(
                        self.game.game_map, np.array([(-1), 0])
                    ):
                        self.move_command_x += self.move_inputs.get("a")
                        self.game.player_list[0].speed += constants.default_inputs.get(
                            "a"
                        )
                        self.move_players()
                        break

                elif event.key == pygame.K_KP2:
                    if not self.game.player_list[0].collision_speed_check(
                        self.game.game_map, np.array([0, 1])
                    ):
                        self.move_command_y += self.move_inputs.get("s")
                        self.game.player_list[0].speed += constants.default_inputs.get(
                            "s"
                        )
                        self.move_players()
                        break

                elif event.key == pygame.K_KP8:
                    if not self.game.player_list[0].collision_speed_check(
                        self.game.game_map, np.array([0, (-1)])
                    ):
                        self.move_command_y += self.move_inputs.get("w")
                        self.game.player_list[0].speed += constants.default_inputs.get(
                            "w"
                        )
                        self.move_players()
                        break

                elif event.key == pygame.K_KP7:
                    if not self.game.player_list[0].collision_speed_check(
                        self.game.game_map, np.array([(-1), (-1)])
                    ):
                        self.move_command_y += self.move_inputs.get("w")
                        self.move_command_x += self.move_inputs.get("a")
                        self.game.player_list[0].speed += constants.default_inputs.get(
                            "w"
                        )
                        self.game.player_list[0].speed += constants.default_inputs.get(
                            "a"
                        )
                        self.move_players()
                        break

                elif event.key == pygame.K_KP1:
                    if not self.game.player_list[0].collision_speed_check(
                        self.game.game_map, np.array([(-1), 1])
                    ):
                        self.move_command_y += self.move_inputs.get("s")
                        self.move_command_x += self.move_inputs.get("a")
                        self.game.player_list[0].speed += constants.default_inputs.get(
                            "s"
                        )
                        self.game.player_list[0].speed += constants.default_inputs.get(
                            "a"
                        )
                        self.move_players()
                        break

                elif event.key == pygame.K_KP3:
                    if not self.game.player_list[0].collision_speed_check(
                        self.game.game_map, np.array([1, 1])
                    ):
                        self.move_command_y += self.move_inputs.get("s")
                        self.move_command_x += self.move_inputs.get("d")
                        self.game.player_list[0].speed += constants.default_inputs.get(
                            "s"
                        )
                        self.game.player_list[0].speed += constants.default_inputs.get(
                            "d"
                        )
                        self.move_players()
                        break

                elif event.key == pygame.K_KP9:
                    if not self.game.player_list[0].collision_speed_check(
                        self.game.game_map, np.array([1, (-1)])
                    ):
                        self.move_command_y += self.move_inputs.get("w")
                        self.move_command_x += self.move_inputs.get("d")
                        self.game.player_list[0].speed += constants.default_inputs.get(
                            "w"
                        )
                        self.game.player_list[0].speed += constants.default_inputs.get(
                            "d"
                        )
                        self.move_players()
                        break

    def update(self):
        self.game_state.update(self.move_command_x, self.move_command_y)
        if self.move_command_x < 0 and self.move_command_y == 0:
            self.rotated = pygame.transform.rotate(new_image, 90)
        if self.move_command_x < 0 and self.move_command_y > 0:
            self.rotated = pygame.transform.rotate(new_image, 135)
        if self.move_command_x == 0 and self.move_command_y > 0:
            self.rotated = pygame.transform.rotate(new_image, 180)
        if self.move_command_x > 0 and self.move_command_y > 0:
            self.rotated = pygame.transform.rotate(new_image, 225)
        if self.move_command_x > 0 and self.move_command_y == 0:
            self.rotated = pygame.transform.rotate(new_image, 270)
        if self.move_command_x > 0 and self.move_command_y < 0:
            self.rotated = pygame.transform.rotate(new_image, 315)
        if self.move_command_x == 0 and self.move_command_y < 0:
            self.rotated = pygame.transform.rotate(new_image, 0)
        if self.move_command_x < 0 and self.move_command_y < 0:
            self.rotated = pygame.transform.rotate(new_image, 45)

    def render(self):
        x = self.game_state.x
        y = self.game_state.y
        self.window.fill((188, 143, 143))
        pygame.draw.rect(
            self.window,
            (50, 50, 50),
            (160, 60, 960, 600),
        )
        pygame.draw.rect(
            self.window,
            (139, 69, 19),
            (160, 300, 672, 96),
        )
        pygame.draw.rect(
            self.window,
            (139, 69, 19),
            (832, 60, 288, 144),
        )
        pygame.draw.rect(
            self.window,
            (139, 69, 19),
            (160, 396, 144, 120),
        )
        pygame.draw.rect(
            self.window,
            (139, 69, 19),
            (496, 396, 48, 120),
        )
        pygame.draw.rect(
            self.window,
            (139, 69, 19),
            (784, 396, 48, 120),
        )
        pygame.draw.rect(
            self.window,
            (139, 69, 19),
            (232, 564, 120, 96),
        )
        pygame.draw.rect(
            self.window,
            (139, 69, 19),
            (352, 516, 48, 144),
        )
        pygame.draw.rect(
            self.window,
            (139, 69, 19),
            (640, 516, 48, 144),
        )
        pygame.draw.rect(
            self.window,
            (255, 255, 255),
            (160, 564, 72, 96),
        )
        self.draw_tiles()
        pygame.draw.rect(
            self.window,
            (47, 9, 9),
            (
                x + 1 + self.game.player_list[0].speed[0] * 24,
                y + 1 + self.game.player_list[0].speed[1] * 24,
                23,
                23,
            ),
        )
        self.window.blit(self.rotated, (x, y))

        if self.game.player_list[0].collision_speed_check(self.game.game_map):
            pygame.draw.polygon(
                self.window, (200, 50, 50), [(80, 60), (40, 130), (120, 130)]
            )
            pygame.draw.polygon(
                self.window, (255, 255, 255), [(80, 70), (48, 125), (112, 125)]
            )
            pygame.draw.rect(self.window, (0, 0, 0), (77, 85, 6, 20))
            pygame.draw.circle(self.window, (0, 0, 0), (80, 115), 4)
        pygame.display.update()

    def draw_tiles(self):
        for a in range(39):
            pygame.draw.line(
                self.window, (0, 0, 0), (184 + a * 24, 60), (184 + a * 24, 660)
            )

        for b in range(24):
            pygame.draw.line(
                self.window, (0, 0, 0), (160, 84 + b * 24), (1120, 84 + b * 24)
            )

    def run(self):
        while self.running:
            self.process_input()
            if not self.game.player_list[0].movement_validity():
                continue
            self.update()
            self.render()

    def player_check(self):
        if self.game.player_list[0].state_check == PlayerState.IS_OUT:
            self.running = False
        if self.game.player_list[0].state_check == PlayerState.HAS_WON:
            self.running = False

    def move_players(self):
        if self.game.player_list[0].path_checking(self.game.game_map) == 1:
            self.game.player_list[0].move()
        else:
            self.running = False
            print("Game ending, processing results...")


game = MyGame()
game.run()
pygame.quit()
