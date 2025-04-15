import pygame
from settings import *

class Controls:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        
        # Font setup
        self.font = pygame.font.Font(None, 32)
        self.title_font = pygame.font.Font(None, 48)
        
        # Colors
        self.text_color = (255, 255, 255)  # White text
        self.bg_color = (0, 0, 0, 180)  # Semi-transparent black background
        self.title_color = (255, 222, 32)  # Gold color for title
        
        # Control descriptions
        self.controls = [
            ("Movement", [
                ("LEFT ARROW", "     Move Left"),
                ("RIGHT ARROW", "     Move Right"),
            ]),
            ("Actions", [
                ("SPACE", "Jump"),
                ("X", "Block Attack"),
                ("ESC", "Pause Game"),
            ]),
            ("Overworld", [
                ("ENTER", "     Enter levels"),
                ("UP ARROW", "     Move Up"),
                ("DOWN ARROW", "     Move Down"),
                ("LEFT ARROW", "     Move Left"),
                ("RIGHT ARROW", "      Move Right"),
            ])
        ]
        
        # Create the control surface
        self.create_control_surface()
        
    def create_control_surface(self):
        # Calculate required height
        total_height = 80  # Initial padding
        line_height = 40
        section_padding = 30
        
        for section, bindings in self.controls:
            total_height += line_height  # Section title
            total_height += line_height * len(bindings)  # Bindings
            total_height += section_padding  # Padding between sections
            
        # Create the surface
        self.surface = pygame.Surface((400, total_height), pygame.SRCALPHA)
        self.surface.fill(self.bg_color)
        
        # Draw title
        title = self.title_font.render("Game Controls", True, self.title_color)
        title_rect = title.get_rect(centerx=self.surface.get_width() // 2, top=20)
        self.surface.blit(title, title_rect)
        
        # Draw controls
        y = 80
        for section, bindings in self.controls:
            # Draw section title
            section_text = self.title_font.render(section, True, self.title_color)
            section_rect = section_text.get_rect(left=30, top=y)
            self.surface.blit(section_text, section_rect)
            y += line_height
            
            # Draw bindings
            for key, action in bindings:
                key_text = self.font.render(key, True, self.text_color)
                action_text = self.font.render(action, True, self.text_color)
                
                key_rect = key_text.get_rect(left=50, top=y)
                action_rect = action_text.get_rect(left=200, top=y)
                
                self.surface.blit(key_text, key_rect)
                self.surface.blit(action_text, action_rect)
                y += line_height
            
            y += section_padding
            
        # Store the rect for positioning
        self.rect = self.surface.get_rect()
        
    def draw(self):
        # Center the controls on screen
        center_pos = (
            (WINDOW_WIDTH - self.rect.width) // 2,
            (WINDOW_HEIGHT - self.rect.height) // 2
        )
        self.display_surface.blit(self.surface, center_pos)
