import pygame
import os
from CarGame.game import Game
import constants
from CarGame.player import PlayerState
import numpy as np

os.environ["SDL_VIDEO_CENTERED"] = "1"
car_texture = pygame.image.load("image/My project.png")
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
                elif event.key == pygame.K_d:
                    self.move_command_x += self.move_inputs.get("d")
                    self.game.player_list[0].speed += constants.default_inputs.get("d")
                elif event.key == pygame.K_a:
                    self.move_command_x += self.move_inputs.get("a")
                    self.game.player_list[0].speed += constants.default_inputs.get("a")
                elif event.key == pygame.K_s:
                    self.move_command_y += self.move_inputs.get("s")
                    self.game.player_list[0].speed += constants.default_inputs.get("s")
                elif event.key == pygame.K_w:
                    self.move_command_y += self.move_inputs.get("w")
                    self.game.player_list[0].speed += constants.default_inputs.get("w")

    def update(self):
        self.game_state.update(self.move_command_x, self.move_command_y)
        if self.game.player_list[0].path_checking(self.game.game_map, 1) == 1:
            self.game.player_list[0].move()
        else:
            self.running = False
            print("Game ending, processing results...")
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
            (0, 0, 0),
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
        self.window.blit(self.rotated, (x, y))
        pygame.display.update()

    def run(self):
        while self.running:
            self.process_input()
            self.update()
            self.render()
            self.clock.tick(8)

    def player_check(self):
        if self.game.player_list[0].state_check == PlayerState.IS_OUT:
            self.running = False
        if self.game.player_list[0].state_check == PlayerState.HAS_WON:
            self.running = False


game = MyGame()
game.run()
pygame.quit()
