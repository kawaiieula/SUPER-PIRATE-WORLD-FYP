import pygame
from ui import Button
from settings import *
import os


class PauseScreen:

    def __init__(self, unpause, quit_game):
        self.display_surface = pygame.display.get_surface()

        self.unpause = unpause
        self.quit_game = quit_game

        # Caption :
        font_path = '../font/LycheeSoda.ttf'
        self.font = pygame.font.Font(os.path.join(font_path), 70)
        self.button_font = pygame.font.Font(os.path.join(font_path), 50)
        self.title = 'GAME PAUSED'
        self.title_image = self.font.render(self.title, False, (255, 255, 255))
        self.title_rect = self.title_image.get_rect(centerx=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 6)

        self.buttons = []
        self.button_selected = 0

        # Restart Button
        button_width = 350
        button_height = 100
        button_x = SCREEN_WIDTH / 2 - 1.25 * button_width
        button_y = (SCREEN_HEIGHT - button_height) / 2
        self.restart_btn = Button(pos=(button_x, button_y),
                                  text='RESUME',
                                  width=button_width,
                                  height=button_height,
                                  bg_color=(66, 66, 66),
                                  bg_hover_color=(33, 33, 33),
                                  font=self.button_font,
                                  on_click=self.unpause)

        # Exit Button
        button_x = SCREEN_WIDTH / 2 + button_width / 4
        button_y = (SCREEN_HEIGHT - button_height) / 2
        self.menu_btn = Button(pos=(button_x, button_y),
                               text='EXIT',
                               width=button_width,
                               height=button_height,
                               bg_color=(66, 66, 66),
                               bg_hover_color=(33, 33, 33),
                               font=self.button_font,
                               on_click=self.quit_game)

        self.buttons = [self.restart_btn, self.menu_btn]
        self.bg = None

    def run(self):
        self.display_surface.blit(self.bg, (0, 0))

        # Caption
        self.display_surface.blit(self.title_image, self.title_rect)

        # Buttons
        for button in self.buttons:
            button.check_click()
            button.draw(self.display_surface)

        # Update the screen
        pygame.display.flip()
