from settings import *
from level import Level
from pytmx.util_pygame import load_pygame
from os.path import join
from support import *
from data import Data
from debug import debug
from ui import UI
from overworld import Overworld
from mainmenu import MainMenu
import pygame


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('Super Pirate World')
        self.clock = pygame.time.Clock()
        self.import_assets()

        self.ui = UI(self.font, self.ui_frames)
        self.data = Data(self.ui)
        self.tmx_maps = {
            0: load_pygame(join('..', 'data', 'levels', 'omni.tmx')),
            1: load_pygame(join('..', 'data', 'levels', '1.tmx')),
            2: load_pygame(join('..', 'data', 'levels', '2.tmx')),
            3: load_pygame(join('..', 'data', 'levels', '3.tmx')),
            4: load_pygame(join('..', 'data', 'levels', '4.tmx')),
            5: load_pygame(join('..', 'data', 'levels', '5.tmx')),
        }
        self.tmx_overworld = load_pygame(join('..', 'data', 'overworld', 'overworld.tmx'))

        # Initialize game state
        self.game_state = 'menu'
        self.paused = False
        self.main_menu = MainMenu(self.start_game, self.start_tutorial, self.quit_game)
        self.current_stage = None
        self.bg_music.play(-1)

        # Game over setup
        self.game_over = False
        self.game_over_font = pygame.font.Font(None, 64)
        self.restart_font = pygame.font.Font(None, 32)
        self.create_game_over_surfaces()

    def start_game(self, name):
        self.game_state = 'overworld'
        self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)

    def start_tutorial(self, name):
        self.game_state = 'level'
        self.data.current_level = 0  # Set to omni.tmx
        self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files,
                                   self.data, self.switch_stage)

    def quit_game(self):
        pygame.quit()
        sys.exit()

    def switch_stage(self, target, unlock=0):
        self.paused = False  # Reset pause state when switching stages
        if target == 'level':
            self.game_state = 'level'
            self.current_stage = Level(self.tmx_maps[self.data.current_level], self.level_frames, self.audio_files,
                                       self.data, self.switch_stage)
        else:  # overworld
            self.game_state = 'overworld'
            if unlock > 0:
                self.data.unlocked_level = 6
            else:
                self.data.health -= 1
            self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)

    def import_assets(self):
        self.level_frames = {
            'flag': import_folder('..', 'graphics', 'level', 'flag'),
            # 'saw': import_folder('..', 'graphics', 'enemies', 'saw', 'animation'),
            'floor_spike': import_folder('..', 'graphics', 'enemies', 'floor_spikes'),
            'palms': import_sub_folders('..', 'graphics', 'level', 'palms'),
            'candle': import_folder('..', 'graphics', 'level', 'candle'),
            'window': import_folder('..', 'graphics', 'level', 'window'),
            'big_chain': import_folder('..', 'graphics', 'level', 'big_chains'),
            'small_chain': import_folder('..', 'graphics', 'level', 'small_chains'),
            'candle_light': import_folder('..', 'graphics', 'level', 'candle light'),
            'player': import_sub_folders('..', 'graphics', 'player'),
            'saw': import_folder('..', 'graphics', 'enemies', 'saw', 'animation'),
            'saw_chain': import_image('..', 'graphics', 'enemies', 'saw', 'saw_chain'),
            'helicopter': import_folder('..', 'graphics', 'level', 'helicopter'),
            'boat': import_folder('..', 'graphics', 'objects', 'boat'),
            'spike': import_image('..', 'graphics', 'enemies', 'spike_ball', 'Spiked Ball'),
            'spike_chain': import_image('..', 'graphics', 'enemies', 'spike_ball', 'spiked_chain'),
            'tooth': import_folder('..', 'graphics', 'enemies', 'tooth', 'run'),
            'shell': import_sub_folders('..', 'graphics', 'enemies', 'shell'),
            'pearl': import_image('..', 'graphics', 'enemies', 'bullets', 'pearl'),
            'items': import_sub_folders('..', 'graphics', 'items'),
            'particle': import_folder('..', 'graphics', 'effects', 'particle'),
            'water_top': import_folder('..', 'graphics', 'level', 'water', 'top'),
            'water_body': import_image('..', 'graphics', 'level', 'water', 'body'),
            'bg_tiles': import_folder_dict('..', 'graphics', 'level', 'bg', 'tiles'),
            'cloud_small': import_folder('..', 'graphics', 'level', 'clouds', 'small'),
            'cloud_large': import_image('..', 'graphics', 'level', 'clouds', 'large_cloud'),
        }
        self.font = pygame.font.Font(join('..', 'graphics', 'ui', 'runescape_uf.ttf'), 40)
        self.ui_frames = {
            'heart': import_folder('..', 'graphics', 'ui', 'heart'),
            'coin': import_image('..', 'graphics', 'ui', 'coin')
        }
        self.overworld_frames = {
            'palms': import_folder('..', 'graphics', 'overworld', 'palm'),
            'water': import_folder('..', 'graphics', 'overworld', 'water'),
            'path': import_folder_dict('..', 'graphics', 'overworld', 'path'),
            'icon': import_sub_folders('..', 'graphics', 'overworld', 'icon'),
        }

        self.audio_files = {
            'coin': pygame.mixer.Sound(join('..', 'audio', 'coin.wav')),
            'attack': pygame.mixer.Sound(join('..', 'audio', 'attack.wav')),
            'jump': pygame.mixer.Sound(join('..', 'audio', 'jump.wav')),
            'damage': pygame.mixer.Sound(join('..', 'audio', 'damage.wav')),
            'pearl': pygame.mixer.Sound(join('..', 'audio', 'pearl.wav')),
        }
        self.bg_music = pygame.mixer.Sound(join('..', 'audio', 'starlight_city.mp3'))
        self.bg_music.set_volume(0.5)

    def create_game_over_surfaces(self):
        # Create "Game Over" text
        self.game_over_text = self.game_over_font.render('Game Over', True, (255, 0, 0))
        self.game_over_rect = self.game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))

        # Create "Click anywhere to restart" text
        self.restart_text = self.restart_font.render('Click anywhere to restart', True, (255, 255, 255))
        self.restart_rect = self.restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))

    def check_game_over(self):
        if self.data.health <= 0:
            self.game_over = True
            return True
        return False

    def handle_game_over(self, events):
        # Draw game over screen
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(180)  # Semi-transparent black
        self.display_surface.blit(overlay, (0, 0))

        # Draw game over text
        self.display_surface.blit(self.game_over_text, self.game_over_rect)
        self.display_surface.blit(self.restart_text, self.restart_rect)

        # Check for click to restart
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Reset game state
                self.game_over = False
                self.data.health = 11  # Reset health
                self.data.coins = 0  # Reset coins
                self.data.current_level = 1  # Reset to first level
                self.data.unlocked_level = 1  # Reset unlocked levels
                self.game_state = 'overworld'  # Go to overworld instead of menu
                # Create new overworld instance with reset state
                self.current_stage = Overworld(self.tmx_overworld, self.data, self.overworld_frames, self.switch_stage)

    def run(self):
        while True:
            dt = self.clock.tick() / 1000
            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # Pass events to current stage for dialogue handling
                if self.current_stage:
                    self.current_stage.handle_event(event)
                # Allow pausing in both level and overworld states
                if self.game_state in ['level', 'overworld']:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                        if self.paused:
                            self.current_stage.pause_game(self.display_surface.copy())
                        else:
                            self.current_stage.unpause()

            if self.game_state == 'menu':
                self.main_menu.run(events)
            else:
                if self.game_over:
                    self.handle_game_over(events)
                else:
                    if self.check_game_over():
                        continue

                    if self.paused:
                        self.current_stage.run_pause_menu()
                        if not self.current_stage.paused:
                            self.paused = False
                    else:
                        self.current_stage.run(dt)
                        self.ui.update(dt)

            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()