import pygame
from settings import *
from ui import Button, get_text_with_outlines, InputBox, RoundedButton, Button2, get_text_with_outlines2
import os
import tkinter
from controls import Controls


class MainMenu:

    def __init__(self, start_game, start_tutorial, quit_game):
        self.display_surface = pygame.display.get_surface()

        self.input_cooldown = 300
        self.last_input = 301

        self.start_game = start_game
        self.start_tutorial = start_tutorial

        # Background
        background_path = '../graphics/BG/bgimg.jpg'
        self.background = pygame.image.load(os.path.join(background_path))
        self.background = pygame.transform.scale_by(self.background, SCREEN_WIDTH / self.background.get_width())

        # Title
        self.font = pygame.font.Font(None, 70)
        title = 'Super Pirate'
        self.title_image = self.font.render(title, False, (255, 222, 32, 255))
        self.title_rect = self.title_image.get_rect(centerx=SCREEN_WIDTH / 2, y=50)

        self.font = pygame.font.Font(None, 70)
        title2 = 'World'  # Split the title into two lines
        self.title_image2 = self.font.render(title2, False, (255, 222, 32, 255))
        self.title_rect2 = self.title_image2.get_rect(centerx=SCREEN_WIDTH / 2, y=50)

        self.button_font = pygame.font.Font('../font/horizon.otf', 20)
        self.buttons = [
            RoundedButton(text="Start",
                          pos=((SCREEN_WIDTH - 170) / 2, (SCREEN_HEIGHT - -290) / 2 - 75),
                          width=170,
                          height=50,
                          radius=20,
                          outlines=False,
                          font=self.button_font,
                          on_click=self.start_level),
            Button2(text="Controls",
                    pos=((SCREEN_WIDTH - 200) / 2, (SCREEN_HEIGHT - -300) / 2),
                    width=200,
                    height=50,
                    outlines=False,
                    font=self.button_font,
                    on_click=self.show_controls),
            Button2(text="Exit",
                    pos=((SCREEN_WIDTH - 200) / 2, (SCREEN_HEIGHT - -320) / 2 + 60),
                    width=200,
                    height=50,
                    outlines=False,
                    font=self.button_font,
                    on_click=quit_game),
        ]
        self.title_image = get_text_with_outlines(SCREEN_WIDTH / 2, 180, title, (255, 222, 32, 255), (238, 97, 5, 255),
                                                  120)
        self.title_image2 = get_text_with_outlines2(SCREEN_WIDTH / 2, 290, title2, (255, 222, 32, 255),
                                                    (238, 97, 5, 255), 120)

        w = 250
        self.input_box = InputBox((SCREEN_WIDTH - w) / 2, (SCREEN_HEIGHT - 50) / 2 - -35, w, 32, 'Enter your name')

        # pop up
        popup_font = pygame.font.Font(None, 30)
        popup_text = "You need to write a name"
        self.popup = Popup(popup_font, popup_text)
        self.popup_pos = ((SCREEN_WIDTH - self.popup.rect.width) / 2, 20)
        self.popup_shown = False
        self.popup_time = 0
        self.popup_duration = 2000

        # Replace the controls popup with the new Controls class
        self.controls = Controls()
        self.controls_shown = False

    def check_name(self):
        name = self.input_box.text
        if name == 'Enter your name' or name == '':
            self.popup_shown = True
            self.popup_time = pygame.time.get_ticks()
            return False
        else:
            return True

    def update_popup(self):
        if self.popup_shown:
            now = pygame.time.get_ticks()
            if now - self.popup_time > self.popup_duration:
                self.popup_shown = False

    def start_tuto(self):
        name = self.input_box.text
        if self.check_name():
            self.start_tutorial(name=name)

    def start_level(self):
        name = self.input_box.text
        if self.check_name():
            self.start_game(name=name)

    def show_controls(self):
        self.controls_shown = True

    def run(self, events):
        # Background
        self.display_surface.blit(self.background, (0, 0))

        # Title
        self.display_surface.blit(self.title_image, (0, 0))
        self.display_surface.blit(self.title_image2, (0, 0))

        # If controls are shown, draw them and check for click to close
        if self.controls_shown:
            self.controls.draw()
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.controls_shown = False
                    break
        else:
            # Only handle other UI elements if controls aren't shown
            # Buttons
            for index, button in enumerate(self.buttons):
                button.check_click()
                button.draw(self.display_surface)

            # Text box
            for event in events:
                self.input_box.handle_event(event)
            self.input_box.update()
            self.input_box.draw(self.display_surface)

            # Regular popup
            self.update_popup()
            if self.popup_shown:
                self.popup.draw(self.display_surface, self.popup_pos)

        pygame.display.flip()


class Popup:
    FOREGROUND_COLOUR = (0, 0, 0)  # dark chocolate brown
    BACKGROUND_COLOUR = (255, 255, 255)  # sepia yellowish white
    SIDE_MARGIN = 7  # size of corners and margin
    LINE_SPACING = 1  # pixels between lines

    def __init__(self, font, message):
        # First render the text to an image, line by line

        self.image = self._textToBitmap(font, message)
        self.rect = self.image.get_rect()

    def draw(self, screen, position):

        x, y = position
        self.rect.topleft = (x, y)
        screen.blit(self.image, self.rect)  # draw the rendered-text

    def _textToBitmap(self, font, message):
        """ Given a (possibly) multiline text message
            convert it into a bitmap represenation with the
            given font """

        height_tally = 2 * self.SIDE_MARGIN  # height-sum of message lines
        maximum_width = 0  # maximum message width
        message_lines = []  # the text-rendered image
        message_rects = []  # where it's painted to
        # cleanup messages, remove blank lines, et.al
        for line in message.split('\n'):  # for each line
            if (len(line) == 0):
                line = ' '  # make empty lines non-empty
            # Make each line into a bitmap
            message_line = font.render(line, True, self.FOREGROUND_COLOUR, self.BACKGROUND_COLOUR)
            message_lines.append(message_line)
            # do the statistics to determine the bounding-box
            maximum_width = max(maximum_width, message_line.get_width())
            height_tally += self.LINE_SPACING + message_line.get_height()
            # remember where to draw it later
            position_rect = message_line.get_rect()
            if (len(message_rects) == 0):
                position_rect.move_ip(self.SIDE_MARGIN, self.SIDE_MARGIN)
            else:
                y_cursor = message_rects[-1].bottom + self.LINE_SPACING + 1
                position_rect.move_ip(self.SIDE_MARGIN, y_cursor)
            message_rects.append(position_rect)
        # Render the underlying text-box
        maximum_width += 2 * self.SIDE_MARGIN  # add the margin
        image = pygame.Surface((maximum_width, height_tally), pygame.SRCALPHA)  # transparent bitmap
        image.fill(self.BACKGROUND_COLOUR)
        # draw the lines of text
        for i in range(len(message_lines)):
            image.blit(message_lines[i], message_rects[i])
        return image