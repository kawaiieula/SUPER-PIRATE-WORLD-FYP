import pygame
from settings import *

class Dialogue:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        
        # Font setup
        self.font = pygame.font.Font('../font/horizon.otf', 30)  # Increased font size
        
        # Colors (matching Super Pirate World theme)
        self.box_color = (0, 0, 0, 200)  # More opaque black background
        self.text_color = (255, 222, 32)  # Gold color
        self.name_color = (238, 97, 5)    # Orange color
        
        # Dialogue box setup - made bigger and centered
        self.box_height = 200  # Increased height
        self.padding = 60
        self.box_rect = pygame.Rect(
            self.padding,
            WINDOW_HEIGHT // 2 - self.box_height // 2,  # Centered vertically
            WINDOW_WIDTH - (2 * self.padding),
            self.box_height
        )
        
        # Dialogue content
        self.dialogues = [
            ("???", "Ahoy there, brave soul! Welcome to the Pirate's Isle."),
            ("???", "These waters be treacherous, filled with dangers and treasures alike."),
            ("???", "Ye'll need quick wit and quicker reflexes to survive here."),
            ("???", "But fear not! For great rewards await those who dare to venture forth."),
            ("???", "As you progress,there will be more will come to join you in this Adventure."),
            ("???", "Now go forth and prove yourself worthy of being called a true pirate!"),
        ]
        
        self.current_dialogue = 0
        self.active = True
        
        # Navigation prompt
        self.prompt_font = pygame.font.Font('../font/horizon.otf', 24)  # Increased prompt font size
        self.prompt_text = "Press E to continue, Q for previous, TAB to skip"  # Updated prompt text
        
    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []
        current_width = 0
        
        for word in words:
            word_surface = font.render(word + ' ', True, self.text_color)
            word_width = word_surface.get_width()
            
            if current_width + word_width <= max_width:
                current_line.append(word)
                current_width += word_width
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_width = word_width
                
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines
        
    def draw_text(self, text, color, pos, font=None, max_width=None):
        font = font or self.font
        
        if max_width:
            lines = self.wrap_text(text, font, max_width)
            y = pos[1]
            for line in lines:
                text_surf = font.render(line, True, color)
                text_rect = text_surf.get_rect(topleft=(pos[0], y))
                self.display_surface.blit(text_surf, text_rect)
                y += font.get_height()
        else:
            text_surf = font.render(text, True, color)
            text_rect = text_surf.get_rect(topleft=pos)
            self.display_surface.blit(text_surf, text_rect)
        
    def draw(self):
        if not self.active:
            return
            
        # Draw semi-transparent overlay for the whole screen
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.display_surface.blit(overlay, (0, 0))
            
        # Draw dialogue box background
        dialogue_surface = pygame.Surface((self.box_rect.width, self.box_rect.height), pygame.SRCALPHA)
        dialogue_surface.fill(self.box_color)
        self.display_surface.blit(dialogue_surface, self.box_rect)
        
        # Draw current dialogue
        if 0 <= self.current_dialogue < len(self.dialogues):
            name, text = self.dialogues[self.current_dialogue]
            
            # Draw speaker name
            name_pos = (self.box_rect.x + 30, self.box_rect.y + 30)
            self.draw_text(name, self.name_color, name_pos)
            
            # Draw dialogue text with word wrap
            text_pos = (self.box_rect.x + 30, self.box_rect.y + 90)
            self.draw_text(text, self.text_color, text_pos, 
                          max_width=self.box_rect.width - 60)
            
            # Draw navigation prompt at bottom of box (moved up by increasing the offset)
            prompt_pos = (self.box_rect.x + 30, self.box_rect.bottom + 10)  # Changed from -50 to -70
            self.draw_text(self.prompt_text, (255, 255, 255), 
                          prompt_pos, self.prompt_font)
    
    def handle_input(self, event):
        if not self.active:
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:  # Next dialogue
                self.current_dialogue += 1
                if self.current_dialogue >= len(self.dialogues):
                    self.active = False
            elif event.key == pygame.K_q:  # Previous dialogue
                self.current_dialogue = max(0, self.current_dialogue - 1)
            elif event.key == pygame.K_TAB:  # Skip dialogue
                self.active = False 