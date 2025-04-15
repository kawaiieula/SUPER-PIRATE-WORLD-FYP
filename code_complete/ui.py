from settings import * 
from sprites import AnimatedSprite
from random import randint
from timer import Timer
import os

class UI:
	def __init__(self, font, frames):
		self.display_surface = pygame.display.get_surface()
		self.sprites = pygame.sprite.Group()
		self.font = font

		# health / hearts 
		self.heart_frames = frames['heart']
		self.heart_surf_width = self.heart_frames[0].get_width()
		self.heart_padding = 6

		# coins 
		self.coin_amount = 0
		self.coin_timer = Timer(1000)
		self.coin_surf = frames['coin']

	def create_hearts(self, amount):
		for sprite in self.sprites:
			sprite.kill()
		for heart in range(amount):
			x = 10 + heart * (self.heart_surf_width + self.heart_padding)
			y = 10
			Heart((x,y), self.heart_frames, self.sprites)

	def display_text(self):
		if self.coin_timer.active:
			text_surf = self.font.render(str(self.coin_amount), False, '#33323d')
			text_rect = text_surf.get_frect(topleft = (16,34))
			self.display_surface.blit(text_surf, text_rect)

			coin_rect = self.coin_surf.get_frect(center = text_rect.bottomleft).move(0,-6)
			self.display_surface.blit(self.coin_surf, coin_rect)

	def show_coins(self, amount):
		self.coin_amount = amount
		self.coin_timer.activate()

	def update(self, dt):
		self.coin_timer.update()
		self.sprites.update(dt)
		self.sprites.draw(self.display_surface)
		self.display_text()

class Heart(AnimatedSprite):
	def __init__(self, pos, frames, groups):
		super().__init__(pos, frames, groups)
		self.active = False

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		if self.frame_index < len(self.frames):
			self.image = self.frames[int(self.frame_index)]
		else:
			self.active = False
			self.frame_index = 0

	def update(self, dt):
		if self.active:
			self.animate(dt)
		else:
			if randint(0,2000) == 1:
				self.active = True


class Button:

    def __init__(self, text, pos, width=150, height=150, on_click=None, text_color=(240, 220, 167, 255),
                 bg_color=(46, 66, 56, 255), bg_hover_color=(105, 235, 235), outline_color=(255, 255, 255),
                 font=None, outlines=True):

        self.on_click = on_click

        self.x = pos[0]
        self.y = pos[1]

        if font is None:
            font_path = '../font/LycheeSoda.ttf'
            font = pygame.font.Font(font_path, 50)
        self.font = font

        self.text = text

        self.text_color = text_color
        self.bg_normal_color = bg_color
        self.bg_hover_color = bg_hover_color
        self.bg_color = self.bg_normal_color
        self.outlines = outlines
        self.outline_color = outline_color

        self.width = width
        self.height = height

        self.shrink = 0.9
        self.normal_rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.shrunk_rect = self.normal_rect.scale_by(self.shrink)
        self.normal_outline_rect = pygame.Rect(self.normal_rect.x - 2, self.normal_rect.y - 2,
                                               self.normal_rect.width + 4, self.normal_rect.height + 4)
        self.shrunk_outline_rect = pygame.Rect(self.shrunk_rect.x - 2, self.shrunk_rect.y - 2,
                                               self.shrunk_rect.width + 4, self.shrunk_rect.height + 4)
        self.rect = self.normal_rect
        self.outline_rect = self.normal_outline_rect

        self.normal_text_image = self.font.render(self.text, False, self.text_color)
        self.normal_text_rect = self.normal_text_image.get_rect(center=self.normal_rect.center)
        self.shrunk_text_image = pygame.transform.scale_by(self.normal_text_image, self.shrink)
        self.shrunk_text_rect = self.shrunk_text_image.get_rect(center=self.shrunk_rect.center)
        self.text_image = self.normal_text_image
        self.text_rect = self.normal_text_rect

        self.pressed = False

    def draw(self, screen):

        if self.outlines:
            # outlines
            pygame.draw.rect(screen, self.outline_color, self.outline_rect, 0)

        # button
        pygame.draw.rect(screen, self.bg_color, self.rect)

        # text
        screen.blit(self.text_image, self.text_rect)

    def check_click(self):

        mouse_pos = pygame.mouse.get_pos()
        if self.normal_rect.collidepoint(mouse_pos):
            self.on_hover()
            if pygame.mouse.get_pressed()[0]:
                if not self.pressed:
                    self.on_press()
                    self.pressed = True
            else:
                if self.pressed:
                    self.on_release()
                    self.on_click()
                    self.pressed = False
        else:
            self.unhover()
            if self.pressed:
                self.pressed = False
                self.on_release()

    def on_hover(self):

        self.bg_color = self.bg_hover_color

    def unhover(self):

        self.bg_color = self.bg_normal_color

    def on_press(self):

        self.rect = self.shrunk_rect
        self.outline_rect = self.shrunk_outline_rect

        self.text_image = self.shrunk_text_image
        self.text_rect = self.shrunk_text_rect

    def on_release(self):

        self.rect = self.normal_rect
        self.outline_rect = self.normal_outline_rect

        self.text_image = self.normal_text_image
        self.text_rect = self.normal_text_rect


class Button2:

    def __init__(self, text, pos, width=150, height=150, on_click=None, text_color=(240, 220, 167, 255),
                 bg_color=(46, 66, 56, 255), bg_hover_color=(105, 235, 235), outline_color=(255, 255, 255),
                 font='../font/Horizon.ttf', outlines=True):

        self.on_click = on_click

        self.x = pos[0]
        self.y = pos[1]

        if font is None:
            font_path = '../font/Horizon.ttf'
            font = pygame.font.Font(font_path, 50)
        self.font = font

        self.text = text

        self.text_color = text_color
        self.bg_normal_color = bg_color
        self.bg_hover_color = bg_hover_color
        self.bg_color = self.bg_normal_color
        self.outlines = outlines
        self.outline_color = outline_color

        self.width = width
        self.height = height

        self.shrink = 0.9
        self.normal_rect = pygame.Rect((self.x, self.y), (self.width, self.height))
        self.shrunk_rect = self.normal_rect.scale_by(self.shrink)
        self.normal_outline_rect = pygame.Rect(self.normal_rect.x - 2, self.normal_rect.y - 2,
                                               self.normal_rect.width + 4, self.normal_rect.height + 4)
        self.shrunk_outline_rect = pygame.Rect(self.shrunk_rect.x - 2, self.shrunk_rect.y - 2,
                                               self.shrunk_rect.width + 4, self.shrunk_rect.height + 4)
        self.rect = self.normal_rect
        self.outline_rect = self.normal_outline_rect

        self.normal_text_image = self.font.render(self.text, False, self.text_color)
        self.normal_text_rect = self.normal_text_image.get_rect(center=self.normal_rect.center)
        self.shrunk_text_image = pygame.transform.scale_by(self.normal_text_image, self.shrink)
        self.shrunk_text_rect = self.shrunk_text_image.get_rect(center=self.shrunk_rect.center)
        self.text_image = self.normal_text_image
        self.text_rect = self.normal_text_rect

        self.pressed = False

    def draw(self, screen):

        if self.outlines:
            # outlines
            pygame.draw.rect(screen, self.outline_color, self.outline_rect, 0)

        # button
        pygame.draw.rect(screen, self.bg_color, self.rect)

        # text
        screen.blit(self.text_image, self.text_rect)

    def check_click(self):

        mouse_pos = pygame.mouse.get_pos()
        if self.normal_rect.collidepoint(mouse_pos):
            self.on_hover()
            if pygame.mouse.get_pressed()[0]:
                if not self.pressed:
                    self.on_press()
                    self.pressed = True
            else:
                if self.pressed:
                    self.on_release()
                    self.on_click()
                    self.pressed = False
        else:
            self.unhover()
            if self.pressed:
                self.pressed = False
                self.on_release()

    def on_hover(self):

        self.bg_color = self.bg_hover_color

    def unhover(self):

        self.bg_color = self.bg_normal_color

    def on_press(self):

        self.rect = self.shrunk_rect
        self.outline_rect = self.shrunk_outline_rect

        self.text_image = self.shrunk_text_image
        self.text_rect = self.shrunk_text_rect

    def on_release(self):

        self.rect = self.normal_rect
        self.outline_rect = self.normal_outline_rect

        self.text_image = self.normal_text_image
        self.text_rect = self.normal_text_rect


class RoundedButton(Button):

    def __init__(self, text, pos, width=150, height=150, on_click=None, text_color=(46, 66, 57, 255),
                 bg_color=(240, 220, 167, 255), bg_hover_color=(105, 235, 235), outline_color=(255, 255, 255),
                 font='../font/Horizon.ttf', radius=1, outlines=True):
        self.radius = radius
        super().__init__(text, pos, width, height, on_click, text_color, bg_color, bg_hover_color, outline_color,
                         font, outlines)

    def draw(self, screen):
        if self.outlines:
            # outlines
            pygame.draw.rect(screen, self.outline_color, self.outline_rect, 0, border_radius=self.radius)

        # button
        pygame.draw.rect(screen, self.bg_color, self.rect, border_radius=self.radius)

        # button text
        screen.blit(self.text_image, self.text_rect)


class Caption:

    def __init__(self, text):
        self.bg_color = (66, 66, 66)
        self.outline_color = (255, 255, 255)
        self.text_color = (255, 255, 255)

        lines = text.splitlines()

        font_path = '../font/LycheeSoda.ttf'
        self.font = pygame.font.Font(os.path.join(font_path), 50)
        self.text_image = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.text_image.set_colorkey((0, 0, 0))
        y = (SCREEN_HEIGHT / 8)
        biggest_line = 0
        height = 0
        nb_line = 0
        for i, l in enumerate(lines):
            line_image = self.font.render(l, False, self.text_color)
            x = (SCREEN_WIDTH - line_image.get_width()) / 2
            self.text_image.blit(line_image, (x, y + i * line_image.get_height()))
            if line_image.get_width() > biggest_line:
                biggest_line = line_image.get_width()
            height += line_image.get_height()
            nb_line += 1
        self.width = biggest_line * 1.2
        self.height = height + height / nb_line

        bg_x = (SCREEN_WIDTH - self.width) / 2
        bg_y = y - (height / nb_line) / 2
        self.rect = pygame.Rect((bg_x, bg_y), (self.width, self.height))
        self.outline_rect = pygame.Rect(bg_x - 2, bg_y - 2, self.rect.width + 4, self.rect.height + 4)

        self.text_rect = self.text_image.get_rect(center=self.rect.center)

    def draw(self, screen):
        # outline
        pygame.draw.rect(screen, self.outline_color, self.outline_rect, 0)

        # background
        pygame.draw.rect(screen, self.bg_color, self.rect)

        # text
        # screen.blit(self.text_image, self.text_rect)
        screen.blit(self.text_image, (0, 0))


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_active = (105, 105, 105)
        self.color_inactive = (0, 0, 0)
        self.color = self.color_inactive
        self.text = text
        self.font = pygame.font.Font('../font/LycheeSoda.ttf', 26)
        self.txt_surface = self.font.render(self.text, True, self.color)
        self.active = False
        self.first_click = True

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                if self.first_click:
                    self.text = ''
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.color_active if self.active else self.color_inactive
            self.txt_surface = self.font.render(self.text, True, self.color)
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.active = False
                    self.color = self.color_inactive
                    self.txt_surface = self.font.render(self.text, True, self.color)
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = self.font.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.rect.w, self.txt_surface.get_width() + 10)
        self.rect.x = self.rect.centerx - width / 2
        self.rect.w = width

    def draw(self, screen):
        # Blit the white background
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        # Blit the text
        screen.blit(self.txt_surface, (self.rect.centerx - self.txt_surface.get_width() / 2, self.rect.y + 5))
        # Blit the outline rect
        pygame.draw.rect(screen, self.color, self.rect, 2)


def draw_text(x, y, string, color, size, window):
    font = pygame.font.SysFont("Impact", size)
    text = font.render(string, True, color)
    textbox = text.get_rect()
    textbox.center = (x, y)
    window.blit(text, textbox)


def get_text_with_outlines(x, y, string, color, outline_color, size):
    surf = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    surf.set_colorkey((1, 1, 1))
    surf.fill((1, 1, 1))

    draw_text(x + 2, y - 2, string, outline_color, size, surf)
    # top right
    draw_text(x + 2, y - 2, string, outline_color, size, surf)
    # btm left
    draw_text(x - 2, y + 2, string, outline_color, size, surf)
    # btm right
    draw_text(x - 2, y + 2, string, outline_color, size, surf)

    # TEXT FILL
    draw_text(x, y, string, color, size, surf)

    return surf


def get_text_with_outlines2(x, y, string, color, outline_color, size):
    surf = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    surf.set_colorkey((1, 1, 1))
    surf.fill((1, 1, 1))

    draw_text(x + 2, y - 2, string, outline_color, size, surf)
    # top right
    draw_text(x + 2, y - 2, string, outline_color, size, surf)
    # btm left
    draw_text(x - 2, y + 2, string, outline_color, size, surf)
    # btm right
    draw_text(x - 2, y + 2, string, outline_color, size, surf)

    # TEXT FILL
    draw_text(x, y, string, color, size, surf)
    return surf